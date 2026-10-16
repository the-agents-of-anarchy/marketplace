# Duplicate suppression and local inbox

Date: 2026-10-16. Spec read: D25, D33, 3.11, and step 7-8 of the receive validation (blueprint.md:271, 323, 580-588, 756-775).

Sources (all read from source; READMEs treated as hypotheses):

| Repo | Commit | How obtained |
|---|---|---|
| iroh-gossip | 2ce78afe09d89d41d123f28eac19bdc831609cc8 (tag v0.101.0) | `/tmp/ra-state/iroh-gossip` |
| agent-gossip | 2c5e1321d9c9d0f3af46675a886fc406b3f65613 (main) | tarball files fetched by raw URL into `/tmp/ra-state/m3-agent-gossip-tar` (repo is 595 MB; clones stalled) |
| habilis-network (engine under agent-gossip) | 8722df5cb0251c95e63bb3618854ee56b1f70cc5 | `/tmp/ra-state/habilis-network` |
| walkie | 54b5fa3053291724da894ef5fddf9039de1c6cf8 (main) | tarball `/tmp/ra-state/m3-walkie-tar` |

Paths below: `ig:` iroh-gossip, `ag:` agent-gossip `crates/agent-gossip/src/`, `hn:` habilis-network `crates/`, `wk:` walkie.

## Per project

### iroh-gossip 0.101.0 — dedup only; no inbox cursor

**Id.** `MessageId` = blake3 of content, 32 bytes (`ig:src/proto/plumtree.rs:27-37`). Receiver recomputes and drops a mismatch as "spoofed" (`plumtree.rs:214`, `:491-499`).

**Set.** `received_messages: TimeBoundCache<MessageId, ()>` (`plumtree.rs:367`). Time window, not count window.
- Insert on own swarm broadcast (`:476`) and on first receipt (`:511`), expiry `now + message_id_retention`.
- Default `message_id_retention` 90 s, `message_cache_retention` 30 s, `cache_evict_interval` 1 s (`:325-327`).
- Doc: id retention "should be at least as long as message_cache_retention, usually will be longer to not accidentally receive messages multiple times" (`:281-285`).

**Structure.** `TimeBoundCache` = `HashMap<K,(Instant,V)>` + `TimerMap` min-heap of `(expiry, seq, key)` (`ig:src/proto/util.rs:317-380`). Sweep by timer: `on_evict_cache_timer` calls `expire_until(now)` on both caches and re-arms (`plumtree.rs:681-688`). Re-inserting a key with a later expiry leaves a stale heap entry. `expire_until` skips it when the map's expiry differs (`util.rs:366-384`).

**Eviction order.** Earliest expiry first. No size bound: set size = rate x 90 s.

**Duplicate path.** Known id: sender moved to lazy set, `Prune` sent, no event to app (`plumtree.rs:504-507`). New id: store, forward, emit `Event::Received` (`:509-545`).

**Edges that bite.**
- Identical content = identical id. Two legitimate sends of equal bytes within 90 s collapse to one. The app must put a nonce or counter in the payload.
- `Scope::Neighbors` messages skip `received_messages` entirely (`:473-483` guard `if let DeliveryScope::Swarm`; receive branch `:509` same guard) and are always emitted.
- After 90 s a replay is delivered again.

**Local consumer buffer.** Two layers, no seq, no replay.
1. Per-topic `tokio::sync::broadcast::channel(256)` (`ig:src/net.rs:53`, `:824`). Overflow overwrites oldest; the receiver gets `Lagged(n)`.
2. Per-subscriber irpc mpsc, default capacity 2048 (`ig:src/api.rs:21`, `JoinOptions::subscription_capacity` `:392-406`).
- `topic_subscriber_loop` maps `Lagged` to `Event::Lagged` and keeps looping (`net.rs:933-949`).
- Doc comment on `subscription_capacity` says on overflow "the message will be dropped, and the subscriber will be closed... should be closed and re-opened" (`api.rs:388-396`). The code at `net.rs:942` does not close. Doc and code disagree.
- Multiple consumers: each `subscribe` gets its own receiver from the same broadcast. Persistence: none.

**Why, by their account.** Plumtree paper design: duplicate arrival is the signal that prunes the tree edge. Cache comments at `plumtree.rs:272-285`. No issue or commit message found explaining 90 s. History in the shallow clone is 50 commits; `-S message_id_retention` finds only the iroh 0.90 port commit 1523227.

**Tests.**
- `TimeBoundCache` expiry and re-insert: `ig:src/proto/util.rs:503-531` (`time_bound_cache`).
- Simulator asserts no app-level duplicate: `ig:src/proto/sim.rs:997` panics on a repeated `Event::Received`.
- No test of `Lagged`. `net.rs:1440` only logs it in a join test.
- Run: `cargo test --lib time_bound_cache` passed (1 passed, 0 failed).

### agent-gossip — local ring with monotonic seq, long-poll, bell

Two separate buffers, deliberately (`ag:a2a/surfaced.rs:16-30`): the engine's `MessageLog` (cross-node anti-entropy) and a local `SurfacedEvents` ring (what was shown to the agent). Quote: mixing "would couple a local cursor to the cross-node eviction order and break anti-entropy convergence — hence two buffers."

**Dedup (engine, habilis-network).**
- Key `DedupKey = SHA-256(author_pubkey_hex ‖ id_bytes)[..16]` (`hn:habilis-network-protocol/src/identity.rs:110-121`, doc `:104-109`).
- Why author-bound: a forged message reusing a victim's id gets another key, so it cannot suppress the genuine one.
- Set: `seen: BoundedFifoSet<DedupKey>`, capacity `SEEN_IDS_CAP = MESSAGE_LOG_SIZE * 2 = 2000` (`hn:habilis-network/src/daemon/state.rs:607-608, 1015`; `hn:habilis-network-util/src/tuning.rs:12-24`).
- `BoundedFifoSet` = `HashSet` + `VecDeque`; evict oldest insert; re-insert is a no-op with no recency bump (`hn:habilis-network-util/src/bounded_fifo_set.rs:1-50`).
- Why 2x: anti-entropy re-sends anything still in the log; "a resend whose id had scrolled out of this set would be reprocessed and re-surfaced. Derived, so the two cannot drift" (`tuning.rs:19-24`).
- Order of gates in `ingest` (`hn:habilis-network/src/gossip/recv.rs:488-548`): parse; self-echo drop by pubkey; signature verify; mesh check; then `mark_seen`. Comment: verify before dedup so a forged copy cannot "poison the dedup window with a replayed id and suppress the genuine signed copy" (`:511-516`). A duplicate is dropped before it re-heartbeats, re-logs, or re-prints (`:536-541`).
- Second dedup inside the log: `MessageLog.keys: HashSet<DedupKey>`; `push` of a held key is a no-op; the key leaves with an evicted message (`hn:.../daemon/message_log.rs:98-117`). Evicted frames can be held again.
- Log eviction is deterministic across nodes: drop the smallest eviction key within the author holding the most messages (`message_log.rs:159-190`). A flooder exhausts its own share.

**Inbox ring.** `SurfacedEvents { capacity, next_seq, events: VecDeque<SurfacedEvent{seq,event}>, latest_waking_seq }` (`ag:a2a/surfaced.rs:35-48`).
- `seq` starts at 1; 0 means "before anything" (`:51-63`).
- `push` assigns seq, appends, pops front while over capacity (`:68-78`). Oldest drops first.
- Capacity `SURFACED_EVENTS_CAP = POLL_RESPONSE_MAX_MSGS = 1000` (`ag:a2a/tuning.rs:53-74`). Sized equal to the response cap so no event is dropped between selection and read (`:68-73`).
- In-memory only; a restart starts at seq 1 and `last_served` 0 (`surfaced.rs:243-246` comment "In-memory only").

**Cursor and gap.** `since(after)` returns every event with `seq > after` (`:101-120`).
- Gap rule: `missed_before = Some(oldest_seq)` when `after != 0 && after < oldest.seq - 1` (`:106-110`).
- `after == 0` returns the whole buffer, no gap. A cursor at newest returns empty.
- The gap is rendered as a leading line `{"event":"gap","missed_before":N}` with no seq, built at render time and never pushed into the ring (`:196-215`). Reason: pushing would feed back into the ring being polled.
- Response truncated to 1000 reports the same gap (`:333-345`).
- Why gap exists: without it "the loss is indistinguishable from 'nothing happened'" (`:128-134`).

**Consumer model.** Daemon-side read cursor `last_served`, not per-client.
- Plain `poll` (no `--after`): serve everything above `last_served`, advance it (`surfaced.rs:476-513`).
- `--after N` is a hidden debug/recovery read that does not touch the cursor (`ag:cli/args/poll.rs:31-36`).
- One daemon serves one agent session (mesh + nickname identify it; `PollIdentity` `poll.rs:8-12`). I found no per-client cursor table.
- Read receipts: `receipted: BTreeSet<u64>` of seqs already receipted, pruned to the ring with `split_off(oldest)` (`surfaced.rs:430-444`).

**Long-poll and bell.**
- Long-poll max 60 s (`tuning.rs:46`). If the buffer holds news, answer now; else park a `PollWaiter{baseline, deadline, responder}`. Waiters capped at 64; over the cap the call degrades to an immediate empty reply (`tuning.rs:76-80`; `surfaced.rs:404-420`).
- Bell = cursor-less `poll --long`. Parks until `latest_waking_seq > last_served`, read live at fulfillment (`surfaced.rs:488-507, 531-562`). Live baseline closes the re-arm race both ways.
- "Waking" excludes state/meta echoes and own task echoes (`:35-48`, tests below). They sit in the ring and ride along with the next waking batch.
- A bell never advances `last_served` (its output is discarded) (`:243`).
- At shutdown parked waiters get `{"shutdown":true}` so the bell exits 0 (`:151-157, 593-597`).
- Single bell per session enforced by an OS file lock `<mesh runtime dir>/<nick>.bell`, not daemon state, so the kernel releases it when the bell dies (`ag:cli/bell.rs:10-47`). Shared-lock probe `is_armed` (`:49-56`).

**Tests** (`ag:a2a/surfaced.rs`, not run):
- `first_poll_returns_all_no_eviction` :730, `cursor_at_evicted_seq_is_not_a_gap` :780, `evicted_cursor_flags_gap` :796, `evicted_cursor_renders_a_leading_gap_marker` ~:818, `oldest_drop_keeps_recent_window` :871.
- Waiters: `waiter_fulfilled_by_a_new_event` :883, `waiter_expires_empty_at_deadline` :909, `bell_armed_into_unserved_backlog_fires_immediately` :1109, `bell_is_not_woken_by_a_foreground_poll_serving_the_backlog` :1128, `bell_ignores_meta_but_delivers_it_with_the_next_waking_batch` :1056, `shutdown_drain_sends_the_sentinel_to_json_waiters_only` :1162.
- Dedup: `a_frame_pushed_twice_is_held_once`, `an_evicted_frame_can_be_held_again` (`hn:.../message_log.rs:503-519`); `mark_seen_delegates_dedup` (`hn:.../state.rs:3444`); `dedup_key16_is_pinned_for_a_fixed_pubkey_and_id` golden (`identity.rs:281`); bounded set tests `bounded_fifo_set.rs:94-150`.

**Why, by their account.** History of surfaced.rs (GitHub API, 2026-07 to 2026-10): "fix: refuse a turn that ends with the gossip bell unarmed (#8)", "fix: keep tasks alive and the gossip bell armed (#15)", "feat: add delivery receipts and reader liveness (#56)". Rationale text is in the code comments quoted above. I did not read PR bodies.

### walkie — per-direction sequence, no id set; ack-gated inbox

Two peers only. The CLI talks to its daemon over a Unix socket; the daemon owns all state.

**Dedup = contiguous seq.** `Session.recv_highest`. A `Msg{seq}` is accepted only if `seq == recv_highest + 1`; a duplicate (lower) and a gap (higher) are both silently dropped (`wk:src/session.rs:155-168`). Accept replies `AckStored{seq}`. No set, no window, O(1) state.

**Inbox.** `inbox: VecDeque<InEntry{seq: Option<u64>, item}>` (`session.rs:47`). Presence events enter with `seq: None`. The inbox itself has no bound. The bound lives on the sender: `outbox` capped at 1000 messages or 1 MiB, counting unread; over the cap `send` fails "outbox full (peer has not read 1000 messages / 1 MiB)" (`session.rs:8-9, 83-90`; spec 6.2 "Outbox cap"). Back-pressure to the sender, not drop at the receiver.

**Replay and reconnect.** On every (re)connect both sides send `Resume{recv_highest, send_base, read_upto}` (`session.rs:110-117`). `on_peer_resume` resends outbox items with `seq > peer.recv_highest`, trims outbox to `seq > read_upto`, and sets `next_seq = max(next_seq, recv_highest+1)` so a restarted sender never reuses a seq the peer holds unread (`session.rs:121-141`; spec 6.2).

**Two acks.** `stored` (in inbox; presence only) and `read` (only after the local consumer acked the batch). Sender keeps a message until `read` (`session.rs:182-190`, spec 5.2/6.2).

**Consumer protocol.** `wait` takes a batch; `ack_batch(id)` releases it.
- `take_batch` returns the existing `pending` batch unchanged if one is unacked, so a killed consumer gets the same batch, same ids (`session.rs:241-248`).
- Batch limited to 20 000 chars (`frame.rs:6`) so a harness never truncates it; always at least one item (`session.rs:253-258`).
- `ack_batch` with a wrong id is refused; the right id emits `AckRead{max seq}` (`:269-292`).
- Guarantee stated: "An agent may see a message twice, never zero times. Ids are stable, so duplicates are recognizable." (spec 5.2).
- Multiple consumers: one `waiter` slot; a new `wait` preempts the old, which gets `Resp::Preempted` and exits 1 without ack (`wk:src/daemon.rs:624-640`; spec 5.2 "Preemption"). Reason: an orphaned wait from a harness timeout must not block the real one.
- IPC: newline-delimited JSON `Req`/`Resp` on a Unix socket; server checks peer uid with `peer_cred` (`wk:src/ipc.rs:10-92`). A different uid is refused. Socket path from room name (`paths.rs`).

**Persistence.** None for messages: "Inbox and outbox live in memory only" (spec 6.2). Crash semantics: received messages survive a `kill -9` of the receiver because the peer still holds them; unacked sends from the killed side are lost. The ticket (pinned peer id) is persisted.

**Tests.**
- Unit, `wk:src/session.rs`: `receive_dedupes_and_ignores_gaps_and_acks_stored` :372; `read_ack_only_after_batch_ack` :387; `redelivers_unacked_batch_with_same_ids` :404; `send_rejects_oversize_and_full_outbox` :479; `outbox_byte_cap_is_one_mib` :492; `resume_resends_only_what_peer_lacks` :510; `resume_read_upto_recovers_a_lost_ack_read` :529; `restarted_sender_never_reuses_seq_peer_holds_unread` :542.
- E2E, `wk:tests/e2e.rs`: `killed_wait_is_redelivered` :112; `kill9_receiver_daemon_loses_nothing` :176; `leave_rejoin_both_sides_no_dupes_no_gaps` :136; `second_wait_preempts_first` :332; `messages_queue_while_not_waiting` :99.
- Not run: not built in this pass.

## Options this gives estafette

Spec today: duplicate set unspecified in size; inbox 1000 frames, `seq` per process life, client sends `{"since":N}`, no gap signal, no ack back. Options map onto those.

1. **Bounded FIFO id set, size tied to what can be re-sent.** `HashSet` + `VecDeque`, evict oldest, re-insert is a no-op. Cost: one set, O(1). Proof: agent-gossip `BoundedFifoSet` (`bounded_fifo_set.rs:17-50`). Size rule: at least 2x the largest window a sender can retry within. Their rule is 2x the log because anti-entropy re-sends from the log; estafette retries come from a sender outbox, so size to the sender retry horizon, not the inbox.
2. **Time-expiring id set.** Map + min-heap on expiry, sweep on a timer. Cost: unbounded under flood, but self-sizing. Proof: iroh-gossip 90 s. Fits if ids are content hashes and the retry window is short. Note the identical-content collapse.
3. **Author-bound dedup key.** `SHA-256(sender_key ‖ id)[..16]`, check after signature and mac verify. Cost: one hash. Proof: habilis-network (`recv.rs:511-541`). Spec 3.6 already verifies mac and `from.sig` before the id check (steps 2-4 before 7), so ordering matches. A random-id message id from another member cannot suppress yours only if the key includes the sender. The spec's D25 keys on id alone.
4. **Per-direction contiguous seq instead of an id set.** Receiver keeps one integer per sender; accept `seq == highest+1`, drop lower and higher. Cost: O(1) per peer, needs a sender-side outbox and a resume exchange to avoid loss on drop-higher. Proof: walkie. Only fits a peer-to-peer pair; with no mailbox and no resume in estafette, "drop higher" would lose messages, so it needs the resume handshake or a window.
5. **Gap marker on replay.** When `since` is older than the oldest retained seq, send a leading frame with `missed_before` and no seq; synthesize it at write time and never store it. Cost: one branch. Proof: agent-gossip (`surfaced.rs:101-120, 196-215`). `since: 0` means "everything, no gap".
6. **Ring sized equal to the per-read cap.** Make buffer size = max frames one reconnect returns, so nothing is evicted between selection and read. Proof: agent-gossip (`tuning.rs:68-73`). Estafette's 1000 for both already satisfies this; state the rule.
7. **Ack-gated release (end-to-end read ack).** Sender keeps until the local consumer acked; same-id redelivery on retry; stated "twice, never zero". Cost: an ack frame back to the sender and an outbox. Proof: walkie. Conflicts with estafette's no-mailbox, since it adds read-ack state on the sender. A cheaper form: `accepted` stays "stored in inbox" and the bridge dedups by id (spec 3.12 already says frames carry `id`).
8. **Back-pressure instead of drop.** Refuse `accepted: true` when the inbox is full. Cost: sender sees failure. Proof: walkie caps the outbox, not the inbox. Estafette's D24 and D25 retry semantics make a refusal retryable; a drop-oldest ring cannot refuse.
9. **Long-poll with live baseline for a bell.** Not needed for a socket that pushes (3.11 streams live frames). Relevant only if a bridge cannot hold a socket. Proof: agent-gossip.
10. **Multiple consumers.** Two models in evidence: walkie preempts (one consumer, newest wins); agent-gossip has one daemon cursor with `--after` as a stateless side read; iroh-gossip gives each subscriber its own receiver on a broadcast. Estafette 3.11 already gives each client its own `since`, which is the stateless side-read model; no server-side cursor is needed.
11. **Subscriber lag handling.** iroh-gossip's two-layer buffer with a `Lagged` event is the model for a slow socket client: if a client's write queue fills, mark it lagged and close it; it reconnects with `since`. Their doc says close, their code does not (see above), so pick one and test it.
12. **Deterministic eviction under flood.** Evict from the sender holding the most frames. Proof: habilis-network `eviction_index`. Only matters if the 1000-frame ring must survive one chatty member; plain oldest-first lets one sender push out everyone's history.

## What could make this wrong

- **Mostly not run.** Only the iroh-gossip `time_bound_cache` test was executed (passed). Walkie and agent-gossip were fetched as source only, not built.
- **agent-gossip history not read.** The repo is 595 MB and clones stalled; I read files at one SHA by raw URL and saw commit titles from the API, not diffs or PR bodies. "Why" is from code comments, not from review discussion.
- **"Per-session cursor" in the prompt.** In source the cursor is per daemon (`last_served`), and a daemon is one session. I found no table of per-client cursors. If a different file holds one, I missed it. I did not read `ag:a2a/ipc.rs`, `ag:api/session.rs` or `ag:mcp/session.rs` line by line.
- **Bell lock is CLI-side.** The OS lock is in `cli/bell.rs`; whether the in-process (MCP) path has an equivalent I did not check.
- **iroh-gossip is not a consumer inbox.** It has a dedup set and a lossy broadcast channel. Replay, seq and cursors do not exist there. I report only what the source shows.
- **Mismatch iroh-gossip doc vs code on lag** (`api.rs:392` vs `net.rs:942`) is read from one tag; a later commit may have changed either.
- **Walkie is two-party.** Contiguous-seq dedup rests on a single peer per direction. Estafette has many senders, so option 4 would need one counter per sender and a resume handshake.
- **Size figures are defaults** (1000, 2000, 90 s, 64, 256, 2048) read from constants; none was measured under load.
- **Spec comparison is mine.** Statements about D25 using id-only keys and 3.11 having no gap signal come from the spec text at lines 271-277 and 756-775 only; I did not read other sections.
