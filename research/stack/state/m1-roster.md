# Peer table / roster

2026-10-16. Clones in `/tmp/ra-state/`, `--depth 50`.

| repo | SHA |
|---|---|
| habilis-network | `8722df5cb0251c95e63bb3618854ee56b1f70cc5` |
| iroh-smol-kv | `4eb7050aa7d653061824d58e8f338c9cfe6169a9` |
| Tunnet | `75b317be0653e8906b33eb46f49d70cc0906dae7` |

Scope: spec 3.8 only. All `path:line` below are at these SHAs. "Not run" means read only.

Four distinct mechanisms turn up, not one. Habilis has two: a roster by receipt time, and a per-origin versioned table with tombstones. Tunnet has two: signed beacons with expiry, and a signed member doc. smol-kv has a third: per-key last-writer-wins with horizon expiry.

## Per project

### habilis-network

Source of truth for the roster: `crates/habilis-network/src/daemon/state.rs`, `.../lifecycle/{mod,membership,heartbeat}.rs`. Docs: `AGENTS.md:18-25,99-113`, `docs/architecture.md:371-378`.

**Key and fields.** Keyed by `Nickname`, a display label, not by key. There is no `Peer` struct. The entry is spread over parallel maps, one per layer:

| field | type | line | role |
|---|---|---|---|
| `peers` | `HashSet<Nickname>` | state.rs:341 | membership: who is present |
| `last_seen` | `HashMap<Nickname, Instant>` | state.rs:344 | local receive time of any message |
| `peer_endpoints` | `HashMap<Nickname, EndpointAddr>` | state.rs:354 | nickname to node id, last writer wins |
| `quiet` | `BoundedFifoSet<Nickname>` cap 1024 | state.rs:367 | silent but returnable |
| `quiet_since` | `HashMap<Nickname, Instant>` | state.rs:374 | recency of quiet peers |
| `surfaced` | `HashSet<Nickname>` | state.rs:383 | which arrivals the operator was shown |
| `proven_endpoints` | `ProvenEndpoints` | state.rs:272 | signing key to endpoint, proven |

`RosterEntry` (state.rs:134) is a derived view: nickname, `last_seen_secs_ago`, `quiet`, `reach`, `transport`. `roster_snapshot` (state.rs:1072) joins the maps at read time and sorts by recency. `count = peers.len() + 1`.

**Update rule: no version, no announcement timestamp.** Liveness is the local receive instant of any authenticated frame.
- `ingest` (recv.rs:487) order: parse; drop own key; verify Ed25519 signature (recv.rs:519); mesh-id gate; dedup via `mark_seen`; then `lifecycle::observe`.
- `observe` (lifecycle/mod.rs:58) sets `last_seen[author] = Instant::now()` for every message kind. The comment calls this the "implicit heartbeat: any received message updates last_seen". A missed `Joined` self-heals from any later frame.
- `membership::compute` (membership.rs:32): `joined_new` if the author is not in `peers` and the kind is not `Left`, `State` or `Meta`. `returned` if the author is in `quiet`. `apply` (membership.rs:69) inserts into `peers`, removes from `quiet`.
- The comment at membership.rs:38-41 gives why `State`/`Meta` do not count: "anti-entropy backfill replays historical state whose author may have long since left, and resurrecting them would forge membership".
- `Alive` is the keepalive: `tick_alive` (heartbeat.rs:16) broadcasts only if nothing was sent for `ALIVE_INTERVAL` 30 s. A chatty node sends none.

**Stale and replayed announcements.** Defence is dedup plus signature, not timestamps.
- Signature check runs before dedup (recv.rs:507-519), so a forgery cannot occupy a victim's id slot. The dedup key is `SHA-256(pubkey || id)`, so reusing a victim's id does not suppress the victim (test `mark_seen_keys_on_pubkey_not_id`, state.rs:3515).
- `seen` is a `BoundedFifoSet<DedupKey>` of `SEEN_IDS_CAP = 2 x MESSAGE_LOG_SIZE = 2000` (tuning.rs:24, state.rs:609). Their reason (tuning.rs:19-22): anti-entropy resends anything still in the 1000-entry log, so the dedup set must outlive it, or a resend "would be reprocessed and re-surfaced". A compile-time assert ties the two.
- `Alive` and `PeerInfo` are not logged (`is_loggable`, recv.rs:1662, tests recv.rs:1746-1771), so anti-entropy never replays them. `Joined` and `Left` are logged, so they can be replayed.
- Timestamps are used only for the join horizon: a frame stamped before `joined_at` is not surfaced (lifecycle/mod.rs:81). Not for roster freshness.
- `PeerInfo` endpoint binding is last-writer-wins by arrival (recv.rs:1503-1506). A separate proof, the endpoint key signing the frame's signing key, gates the one use that matters: where a point-to-point answer goes (endpoint_proof.rs:1-8). Their own doc names the residual: an endpoint that keeps its key across runs "lets an old `PeerInfo` be replayed to put back the old signer", and that peer is then answered on gossip until its next `PeerInfo` (endpoint_proof.rs:46-55).

**Status transitions.** Three states, derived, no stored enum.

| state | where it lives | entered by | left by |
|---|---|---|---|
| active | in `peers` | first non-`Left` frame; return from quiet | sweep, `Left` |
| quiet | in `quiet` (cap 1024) | sweep: silent past `ALIVE_TIMEOUT` 90 s and `surfaced` | any frame from the nickname (`returned`); FIFO eviction past cap |
| gone | in no set | `Left` | next frame re-adds it as new |

- Sweep: `tick_sweep` (heartbeat.rs:41) runs every `SWEEP_INTERVAL` 10 s (tuning.rs:157, event_loop.rs:1343). Worst-case ghost window is `alive_timeout + sweep_interval` (tuning.rs:141-142). Timeout is 3x the keepalive: "3x absorbs one or two lost gossip rounds".
- Quiet entry also keeps `quiet_since` so recency still shows, and keeps the endpoint binding so a returned peer is addressable at once (heartbeat.rs:62-69).
- **Ghost rule:** a peer learned only through pre-join backlog was never `surfaced`. The sweep evicts it silently and does not move it to `quiet` (heartbeat.rs:70-82). Tests: `sweep_evicts_unsurfaced_peer_silently` (heartbeat.rs:313), `sweeping_a_ghost_owes_nothing` (heartbeat.rs:223).
- `Left` (lifecycle/mod.rs:150-168): remove from `peers`, forget endpoint binding and warm unicast connection, remove from `quiet` and `surfaced`. "A graceful goodbye, unlike a silence timeout, drops the dial hint." No tombstone: a later frame from the same nickname re-enters as new.
- Sweep side effect: a silent known peer arms a return to the rendezvous (`owe_rendezvous_return`, heartbeat.rs:62-66), because silence may mean a partition. Estafette has no rendezvous, so this part does not transfer.

**Expiry and memory bounds.**

| collection | bound | where |
|---|---|---|
| `quiet` | FIFO cap 1024 | tuning.rs:437, test `quiet_field_is_capped` state.rs:3429 |
| `quiet_since` | pruned to `quiet` membership each sweep | heartbeat.rs:92-98 |
| `peer_endpoints` | pruned to `peers` union `quiet` each sweep | heartbeat.rs:99-107 |
| `known_endpoints` | FIFO cap 64 | tuning.rs:47, test state.rs:3238 |
| `seen` | FIFO cap 2000 | above |
| `ProvenEndpoints` | cap; at cap drops oldest unlinked pair, else refuses the new one | endpoint_proof.rs:46-90 |
| parked link vectors | one per author, cap 256 | state.rs:70-90 |
| `peers`, `last_seen`, `surfaced` | no cap; bounded in time by the 90 s sweep | not capped in code |

The `quiet` doc says it is "the one unbounded collection we own" that needed a cap, because "a churn / sybil stream of one-shot nicknames would grow it without bound" (tuning.rs:430-435). The `BoundedFifoSet` doc: re-insert is a no-op, "recency isn't load-bearing" (bounded_fifo_set.rs:1-9). Flap test `app_state_stays_bounded_under_flap_churn` (state.rs:3907): 10 000 flaps, no collection grows with flap count. Its comment links this to a 2026 soak with a 4.6 GB climb that sat below their layer.

**Convergence.** No table exchange. Each node derives its roster from frames it saw.
- A `Joined` re-floods our own `PeerInfo` and re-announces our `Joined`, "so late joiners seed their roster" (lifecycle/mod.rs:186-210). New peers also trigger `greet_new_peer` (recv.rs:563, 1437).
- Repair of missed frames is anti-entropy over the message log: periodic `Digest` of 70-id windows, resend under a budget (`docs/architecture.md:448-454`). Alive is excluded, so keepalive loss is repaired only by the next keepalive.
- Two nodes can hold different rosters for up to the ghost window. Nothing reconciles them directly.

**Versioned per-origin table with tombstones (link vectors).** The one place habilis orders announcements. `crates/habilis-network-iroh-multihop-transport/src/topology.rs`.
- Entry: `LinkVector { origin, seq, underlay, links, sig }` (topology.rs:39-56). Signed by the origin key over a domain-separated payload (topology.rs:36-37, 60-68).
- `seq` is wall-clock ms. Generator: `seq = max(now_ms, last_seq + 1)` (multihop lib.rs:496-507), so a restart with the same key still wins over its own older vectors.
- `ingest_at` (topology.rs:192-228) accepts only if all hold: signature valid; `wall_ms - seq <= max_age` (45 s, topology.rs:23); `seq > tombstone.seq` if a tombstone exists; `seq > held.seq`. Equal seq is refused.
- `remove` (on `Left`) and `expire_older_than` (silent past `max_age`) both write `Tombstone { seq, at }` and drop the vector (topology.rs:239-270). Tombstones live one `max_age`, then are forgotten. Doc (topology.rs:116-120): "so the last vector of a peer that left cannot come back as if new (a late joiner gets it again through anti-entropy)".
- A newer vector clears the tombstone, so an expired node returns with its next vector (topology.rs:220).
- Clock skew: a vector more than `max_age` behind our clock is refused, logged once per `max_age` globally, "so that a flood of keys cannot grow it" (topology.rs:170-177).
- Origin must equal the endpoint the roster binds to the frame's author, else dropped. A vector that beats its `PeerInfo` is parked, one per author, cap 256 (recv.rs:777-830). The comment: "a signature proves who made the vector, not that the origin is a member: anyone holding the mesh id can mint keys".
- Cadence: vector every `LINKSTATE_INTERVAL` 15 s (tuning.rs:69), age 45 s = 3 intervals. CHANGELOG:55-65 records the design.

**Tests.**
- Roster: `lifecycle/membership.rs:100-183` (first sight, `Left` never joins, quiet returns, apply). `lifecycle/heartbeat.rs:125-368` (sweep to quiet, ghost silent, endpoint kept for return, endpoint pruning, recency kept, keeps recent, noop on empty). `state.rs:3238-3441` (caps). `recv.rs:1746-1771` (loggability).
- Vector table: `topology.rs:432-612`: `a_vector_that_claims_another_origin_is_refused` (:432), `a_stale_vector_ages_out` (:486), `a_copy_of_an_old_vector_does_not_keep_a_gone_peer_alive` (:511), `a_vector_that_was_expired_does_not_come_back` (:524), `a_vector_of_a_peer_that_left_does_not_come_back` (:541), `a_node_whose_vector_expired_returns_with_its_next_one` (:557), `a_vector_older_than_the_max_age_is_refused` (:570), `after_a_restart_the_first_new_vector_wins` (:588), `newer_vector_supersedes_older` (:602).
- Ran: all pass. See "Test runs".

### iroh-smol-kv

One file: `src/lib.rs` (1210 lines). A gossip KV, not a roster. A roster is a use case on top: each member writes its own key and others read it.

**Key and fields.** Two levels: `scope: PublicKey` (the writer) then `key: Bytes`. Value `SignedValue { timestamp: u64 ns, value: Bytes, signature: [u8;64] }` (lib.rs:45-55). Signature covers `(key, timestamp, value)` via postcard (lib.rs:93-99, 481-514). A write needs the scope's secret key, so a scope is owned by its signer.

State: `rpds::HashTrieMapSync<PublicKey, RedBlackTreeMapSync<Bytes, SignedValue>>` (lib.rs:483-485). Persistent structures: `snapshot()` is a clone (lib.rs:489) and costs O(1). Subscribers and the anti-entropy task iterate a frozen snapshot with no lock, on a single-owner actor (`Actor::run`, lib.rs:723).

**Update rule.** Per (scope, key), strict newer timestamp wins (lib.rs:513-541).
```
Some(existing) if existing.timestamp >= value.timestamp => Err(ValueTooOld)
_ => insert
```
Equal timestamp keeps the existing value, whichever arrived first. Remote values go through `insert_signed_value`, which verifies the signature against `scope` first (lib.rs:496-511). Local puts skip verification (lib.rs:513). A new valid value is also pushed to subscribers via a `broadcast` channel (lib.rs:823).

**Stale and replayed.**
- Replay of an old signed value: rejected by the timestamp rule, or by the horizon check at receipt: `value.timestamp < now - horizon` is dropped before insert (lib.rs:817-823). Docs at lib.rs:870-873 say expired values "are removed, and will not be re-added".
- No tombstone, no delete. Absence is expiry only.

**Expiry.** `ExpiryConfig { horizon, check_interval }`. Defaults: horizon 24 h, "purge every hour" (lib.rs:885-897). `DEBUG`: 30 s horizon, 10 s check (lib.rs:874-883). Entries are judged by the writer's timestamp, not by receive time. `apply_horizon` (lib.rs:609-634) removes entries below `now - horizon`, drops empty scopes, and emits `SubscribeItem::Expired((scope, key, last_ts))` to subscribers (lib.rs:848-852). So presence is "write a key every N seconds; liveness is the age of its timestamp".

**Convergence: periodic full republish.**
- `anti_entropy` (lib.rs:636-668): snapshot, shuffle, publish every entry with `broadcast_neighbors`, spaced evenly over `anti_entropy_interval`. Default 300 s; `fast_anti_entropy_interval` 10 s (lib.rs:885-897).
- `NeighborUp` restarts it with the fast interval (lib.rs:797-801): "New peer, starting fast anti-entropy".
- A local `put` broadcasts to the whole topic at once (lib.rs:750).
- Cost is O(entries) messages per round per node. There is no digest, no diff, no pull.

**Memory bounds.** None on scope count, key count or value size beyond the gossip message limit. Anyone on the topic can mint a scope key. Entries die only by horizon. Subscribers get a `broadcast::channel(32)`: a lagging subscriber's `recv` errors and its stream ends (lib.rs:591, 705-707).

**Why, by their account.** Sparse. README: "A tiny in memory replicated key value store that syncs via an iroh-gossip topic". Module doc: "Entries in the database expire after not being modified for a certain duration" (lib.rs:12-13). Commit history is terse (`3f0b23d Add expiry to cli exmaple`; `6872d4f Add broadcasting of internal updates`). Issue #5 (a user asks about sharding), answer from a user, not the maintainer: it "replicates across all clients... more useful for things like room membership and such - this is an eventually consistent replicated k/v store."

**Open issues that bear on the mechanism.**
- #4 (open): with three or more nodes, a value written soon after join is sometimes never seen on some nodes. A 3 s sleep before the write avoids it. Reporter is not sure whether the fault is in the kv layer or iroh-gossip. Unresolved.
- #8 (open, PR): `check_interval` is a config field that nothing reads. The purge period is hard-coded 30 s (lib.rs:732; `check_interval` appears only at lib.rs:871, 880, 895).

**Tests.** None. No `#[test]`, no `tests/` dir (grep over `src/` and `examples/`). `examples/test.rs` is a manual two-put script. Nothing run.

### Tunnet

Two mechanisms, split by purpose. `crates/tunnet-core/src/direct/{presence,membership,grants}.rs`, `.../node.rs`, `.../routing.rs`. Managed mode is a server database and is out of scope.

**A. Presence beacons (liveness).** `presence.rs`.

Entry: `PresenceBeacon { network_id, endpoint_id, hostname, mesh_ip, agent_version, issued_at, expires_at, sig }` (presence.rs:21-33). Signed by the endpoint's own Ed25519 key over all fields but `sig` (presence.rs:113-142). `endpoint_id` is the key hex, so the signature check also proves ownership of the id.

Table: `PresenceTable { peers: Arc<Mutex<HashMap<String, PresenceBeacon>>> }`, keyed by `endpoint_id` hex (presence.rs:36-40).

Rules:
- Publish every `PRESENCE_PUBLISH_INTERVAL` 30 s; `expires_at = issued_at + PRESENCE_TTL` 90 s (presence.rs:19-20, 154-165). TTL is 3x the interval, same ratio as habilis.
- Receive (presence.rs:188-208): deserialize; `verify_beacon(beacon, now)` fails if `expires_at < now` or signature bad; then `upsert`. `upsert` is an unconditional `insert` by key (presence.rs:46-48). No comparison of `issued_at` against the held beacon.
- Expiry is stored in the signed beacon, so each reader judges it with its own clock. Entries are physically removed by `remove_expired` on the publisher's 30 s tick (presence.rs:231; apply: presence.rs:50). Reads check `expires_at > now` and never trust the physical presence (presence.rs:46-75).
- Sender's own beacon is built fresh each tick, so there is no resend of old state.

States: three-valued, from `presence_status` (presence.rs:62-66): `None` never seen, `Some(true)` live, `Some(false)` expired. `node.rs:185-209` merges tables across networks; "never-seen peers stay unknown (None) so cold-start does not flood Offline". No `Gone` or departure message exists: a stopped node ages out after at most 90 s plus up to 30 s until the next sweep.

Composition into the visible status (`local_api/handlers.rs:487-500`): `online = Some(true)` if the connection pool has a live link to the peer, else the presence verdict. `last_seen` is pool activity if any, else `now - beacon.issued_at`. So transport truth overrides gossip presence.

Memory: the table is not capped. A valid signature from any key on the network topic inserts an entry. The topic is `blake3(network_id)` (tunnet-common lib.rs:513). Reads are keyed by roster peers, so entries of non-members are inert, but they stay until their `expires_at`.

**B. Member records (membership).** `membership.rs`, `grants.rs`.

Membership is a replicated iroh-docs document, one per network (membership.rs:1-9). Keys: `meta/genesis`, `meta/epoch`, `peers/<endpoint_id>/record`, `peers/<endpoint_id>/metadata`, `revocations/<endpoint_id>`, `policy/v1/bundle`. The coordinator signs everything that grants membership.

`SignedMemberRecord` (grants.rs:33-46): `endpoint_id, hostname, ipv4, tags, status, sequence, joined_at, grant, endpoint_sig, coordinator`. Despite the field name, `endpoint_sig` is verified against the coordinator key (grants.rs:289).

Update rule, in `rebuild_from_doc` (membership.rs:691-900), run on every `InsertLocal`, `InsertRemote`, `ContentReady`, `SyncFinished` (membership.rs:379-392):
1. Load genesis, epoch records and revocations; keep only coordinator-verified ones. `min_epoch` is the max verified epoch.
2. For each `peers/<id>/record`: skip if revoked; verify schema, grant (`min_epoch`), signature; check address plan; skip `status == "kicked"`.
3. Several authors can write the same key, and iroh-docs returns each. Keep the one with the highest `sequence`: `record.sequence > held.sequence` (membership.rs:815). Metadata (SSH key, endpoint-signed) uses the same rule (membership.rs:877).
4. Reject the whole rebuild if two members carry one IPv4 (membership.rs:884-895).
5. Replace the members map, then `project_runtime` replaces the routing table: `RoutingTable` is an `ArcSwap<Tables>`; `replace_network_with_plan` rebuilds all lookup maps and swaps atomically (routing.rs:456-503, 531+; membership.rs:569-586, 902-931).

Departure: `kick_peer` (membership.rs:652-689): bump the signed epoch, write a signed `Revocation`, remove from the local map. The epoch bump invalidates every older grant; the revocation is the authority ("Epoch bump invalidates prior grants; revocation is membership authority"). A 5 s tick applies kicks queued in a file (membership.rs:995-1004).

Quirk: coordinator admission sets `sequence` to the constant 1 for a new member and 2 for a re-admission (membership.rs:525-531), not a counter.

Why, by their account: PR #24 ("redesign direct address allocation and membership authority"): "signed Genesis the authority for the network's peer allocation range, makes the coordinator the only peer-IP allocator, and makes signed membership the only `EndpointId -> IP` authority". Docs (`apps/docs/products/mesh/gossip.md:5-9`): the control plane gives authoritative config on a 30 s poll; gossip gives "sub-second presence updates".

Convergence: delegated to iroh-docs sync. The roster is a pure function of the doc, recomputed whole, so any two nodes with the same doc hold the same table. Bound: members are coordinator-admitted, so size follows admissions.

**Tests.**
- Presence: two unit tests only, `presence_sign_verify_roundtrip` (presence.rs:265) and `presence_expiry_rejected` (presence.rs:279). No test for upsert ordering, sweep, or the `None/Some` composition.
- Membership: `grants.rs` tests for grant epoch (`grant_rejects_low_epoch` :509, `epoch_roundtrip` :734). `peers_for_sync_*` (membership.rs:1200-1217). `tests/direct_join_iroh.rs` covers the join handshake with a mock authority (invite replay, revocation of invites, approval), not `rebuild_from_doc` or sequence selection (grep for `sequence|kick` finds only the mock's `sequence: 1`).
- Ran: both presence tests pass. See "Test runs".

## Options this gives estafette

Each option answers a row of spec 3.8. Estafette today: no timestamp or sequence field on Presence, `last_seen` and `Online|Unreachable|Gone` set by events, `Gone` kept 3600 s, then removed.

1. **Liveness from local receive time of any authenticated frame.** One `last_seen` per card, refreshed by every validated frame (Presence, Introduce, any message), swept on a timer. Cost: one map, one tick; no clocks compared; a missed Presence heals from the next frame. Replay can refresh a card if the dedup set misses it. Proven by habilis (`lifecycle/mod.rs:58`, `heartbeat.rs:41`). Estafette's "Message received and validated: treat `from` as Presence" row is already this rule.
2. **Keepalive at 30 s, silence timeout at 90 s, sweep at 10 s.** Timeout 3x the interval; worst-case stale window equals timeout plus sweep period. Send keepalive only when nothing else was sent. Cost: up to 100 s before a crashed peer shows silent. Proven by habilis (tuning.rs:136-157) and, for 30/90, Tunnet (presence.rs:19-20).
3. **Two-step departure: Unreachable (kept, returnable, bounded) then removal.** Habilis `quiet` is the analogue of `Unreachable`: kept with last-heard time and endpoint binding so a returning peer is reachable at once; FIFO cap 1024; drained on return. `Left` removes immediately and drops dial hints. Cost: a cap and a recency companion map. Proven by habilis.
4. **Ghost rule.** A card learned only from replayed or backfilled traffic, never shown as arriving, is dropped silently at timeout and never enters the `Unreachable` set. Needs a `surfaced`-like flag per card. Cost: one flag. Proven by habilis (heartbeat.rs:70-82, tests 223, 313). Estafette has an inbox replay to a local bridge, so the same backfill hazard exists.
5. **Signed announcement carrying its own expiry (Tunnet beacon).** `issued_at` and `expires_at` inside the signed Presence; reader checks `expires_at > now`; reads never trust the physical row. Cost: depends on the signer's clock for the interval; Tunnet's receive path does a plain `insert`, with no ordering and no cap on `expires_at - issued_at`. If used, add what habilis adds in option 6. Proven by Tunnet (presence.rs:62-75, 144-150, 188-208).
6. **Per-card monotonic `seq` + max age + tombstone (habilis link vector).** `seq = max(now_ms, last+1)`; accept only if the signature holds, age within `max_age`, `seq` above the tombstone, `seq` above the held one; equal is refused. `Gone` writes a tombstone of the highest seq for one `max_age`. Closes replay of a departed card's last Presence. Cost: clocks within `max_age` (45 s there) or announcements are refused, so log the refusal once per `max_age`; one tombstone map pruned each tick. Proven by habilis with nine unit tests (topology.rs:432-612). This is the only fully tested stale/replay answer among the three. A `Gone` tombstone of 3600 s would match estafette's 3600 s keep.
7. **Bind the node key to the card, and prove it once.** Roster maps card to node id from a signed frame, last writer wins. Habilis adds a proof (the node key signs the card key) and gates only the sensitive use (directed replies) on it; unproven senders are answered on gossip. If the card is the node key (reconsidered), the proof disappears: the signature already proves both. Habilis names the cost of not proving: replay of an old announcement re-binds an old signer (endpoint_proof.rs:46-55).
8. **Bound every side map to the live set plus the returnable set.** Each sweep, retain `endpoint`/`recency` maps only for active and quiet cards (heartbeat.rs:92-107). Cap each growth-by-stranger set with FIFO. Cost: one retain per sweep. Proven by habilis with tests.
9. **Dedup set at 2x the replay buffer.** Estafette's inbox holds 1000 frames and replays them; a dedup set of 2000 ids, tied by a compile-time assert, stops a replayed frame from re-heartbeating or re-announcing. Proven by habilis (tuning.rs:16-26). Estafette's duplicate set size is not in 3.8, so this is a check against whatever it is.
10. **Three-valued status for display.** Unknown (never seen), online, offline; transport truth (live direct link) overrides gossip presence; never-seen is unknown, not offline. Cost: one `Option<bool>`. Proven by Tunnet (node.rs:185-209, handlers.rs:487-500). Maps to estafette `Online | Unreachable | Gone` plus "no entry".
11. **Periodic full republish plus fast round on new neighbor (smol-kv).** For convergence without a digest: every member re-announces its own card on a slow timer (300 s there) and on `NeighborUp` at a faster rate. For a roster the republished item is only the member's own Presence, so the cost is O(1) per member, not O(entries) as in smol-kv. Estafette 3.8 already sends Presence on `NeighborUp`/change events; the periodic part is the addition.
12. **Recompute the table from an authoritative source instead of patching.** Tunnet rebuilds the whole member map from the doc on each change and swaps it atomically, so it cannot drift. Applies only if estafette ever holds a signed membership set; it holds none now.

## Test runs

All run on 2026-10-16 with `cargo test` at the SHAs above. Logs: `/tmp/ra-state/m1-*.log`.

| repo | command filter | result |
|---|---|---|
| habilis-network | `-p habilis-network-iroh-multihop-transport --lib topology` | 23 passed, 0 failed (includes all nine vector tests named above) |
| habilis-network | `-p habilis-network --lib` filters `lifecycle::`, `quiet_field_is_capped`, `known_endpoints_field_is_capped`, `mark_seen_keys_on_pubkey_not_id`, `is_loggable_tests`, `app_state_stays_bounded` | 26 passed, 0 failed |
| Tunnet | `-p tunnet-core --lib direct::presence` | 2 passed, 0 failed |
| iroh-smol-kv | none | no tests exist, nothing to run |

Not run: Tunnet `direct_join_iroh` (join handshake, not roster rules), habilis integration tests, any claim marked "by reading".

## What could make this wrong

- **Habilis keys the roster by nickname, not by key.** Its own docs say the nickname is "a non-unique display label" and that identity is the signing key (recv.rs:547-553), yet `peers`, `last_seen`, `quiet` and `peer_endpoints` are keyed by nickname. Two keys sharing one nickname merge into one entry. I found no code that separates them; I did not test it. Estafette keys by card, so it avoids this, but habilis does not prove that a key-keyed roster works the same.
- **Left replay.** `handle_presence` removes the author on any non-duplicate `Left` without checking `surfaceable` (lifecycle/mod.rs:150-153); only the app callback is gated. A `Left` replayed after the 2000-id dedup window could drop a live peer until its next frame. By reading only. Not tested, and I did not see a test either way.
- **Habilis liveness uses local receive time**, so it never needs peer clock agreement for the roster. Only the link-vector table does. If estafette picks option 5 or 6 it takes on the clock-skew refusal habilis documents (topology.rs:150-155).
- **Tunnet presence has no ordering test.** `upsert` is an unconditional overwrite, so an older unexpired beacon replaces a newer one. `verify_beacon` does not bound `expires_at - issued_at`. I read this from code; nothing exercises it. I treat option 5 as unproven on replay.
- **smol-kv is the least evidenced.** No tests; open issue #4 reports lost values with three nodes; `check_interval` is unused. A local `put` calls `.expect("inserting local value should always work")` (lib.rs:747): a wall clock that steps back makes that `expect` panic inside the actor. By reading; I did not run it. Its timestamps come from the writer's clock with no bound against the future.
- **Thin "why".** Habilis explains itself in code comments, `AGENTS.md`, `CHANGELOG.md` and issues. Tunnet explains membership in PR #24 and has almost nothing on presence. smol-kv has no design text beyond the README. Where a reason is missing I say so; I did not infer one.
- **Scale.** Habilis states a full mesh of 65 or fewer has zero membership churn (`docs/architecture.md:703`). Its roster numbers come from small meshes (a soak of about 10 members, state.rs:3905). I found no evidence at large size.
- **Commit depth.** Clones are `--depth 50`. History before that, including who first chose the 30/90 s values, was not read.
- **Not read:** habilis `netplay` lobby roster; Tunnet Managed-mode presence in `tunnet-control`; iroh-docs itself (the sync under Tunnet membership).
