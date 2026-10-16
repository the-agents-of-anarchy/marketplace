# Node lifecycle with a persistent identity

Date: 2026-10-16. Mechanic M4. Tests the hypothesis in `docs/orchestration_log/history/2026-10-16-node-as-identity.md` (N: card key = iroh endpoint key; flock on sidecar settles D6/D7).

Repos, all under `/tmp/ra-state/`:

| Repo | Checkout | Commit read |
|---|---|---|
| agent-gossip | `agent-gossip-m4` | `2c5e1321d9c9d0f3af46675a886fc406b3f65613` |
| habilis-network (engine under agent-gossip) | `habilis-network-795` (git archive) | `795c4f88fdbfe01ad89a6872753f942ec75595a4`, the rev agent-gossip pins (Cargo.toml:47). HEAD `8722df5` differs in daemon/ files; not used. |
| mcpmesh | `mcpmesh` | `555dc1d6a6a5d429729898d508f5068cdc0e2794` |
| Tunnet | `Tunnet` | `75b317be0653e8906b33eb46f49d70cc0906dae7` |
| iroh-gossip | `iroh-gossip` | `2ce78afe09d89d41d123f28eac19bdc831609cc8` (0.101.0) |
| iroh-relay | `~/.cargo/registry/src/*/iroh-relay-1.3.0` | crate 1.3.0 |

mcpmesh history is squashed to release commits ("formula: 0.47.0"). Its "why" comes from code comments and docs, not commits.

## Verdict on N's three unknowns

| Unknown | Finding | Evidence strength |
|---|---|---|
| 1. flock released by kernel on kill | Holds on macOS (run by me). Three projects rely on it. None tests a SIGKILLed holder. Linux not run. | Run, one platform |
| 2. Peer holds stale connection, same key returns | iroh-gossip replaces the send path at once; old connection lingers silently; no NeighborDown/NeighborUp predicted. Issue #10 was exactly this stall; fixed in #43. | Source read plus one test run. Event stream not observed. |
| 3. Dial during window, which instance answers | Relay: newest registration wins, old gets `SameEndpointIdConnected`, re-promoted on unregister. Direct path: not found in any source read. | Relay source and unrun test only |

## Per project

### agent-gossip (daemon, `--owner-pid`, `setsid`, bell lock)

Identity: not persistent. Each daemon start calls `Identity::generate()` (habilis-network-795 `crates/habilis-network/src/daemon/setup.rs:698`). The endpoint key is "new each run by default" (`transport/endpoint_proof.rs:57`). So agent-gossip has no same-key restart. It does carry the mechanics around one.

**Single instance: no lock on the daemon.** Collision guard is a check, not a lock.
- `run_session` reads the state file and asks `live_owner_of` before any network setup (`crates/agent-gossip/src/cli/mod.rs:236-247`). Refusal text: "state file ... already in use by ... A state file has one writer".
- `live_owner_of` (`cli/session.rs:228`) requires a live daemon to answer on its socket with matching mesh, nickname, and pid (`confirm_owner`, `session.rs:204`). Pid alone is untrusted because of reuse (doc `session.rs:197-203`).
- The socket bind unlinks any existing socket without a liveness test (`transport/ipc.rs:101`). Safe only because the check above ran first. Check-then-act, no atomicity.

**Bell lock (not the daemon).** The bell is the CLI waiter. One per (mesh, nickname).
- `cli/bell.rs:23-41`: open file 0600 `{nick}.bell`, `try_lock()` exclusive, retry 10 ms for 500 ms, so a probe's momentary shared lock does not read as a rival.
- `is_armed` (`bell.rs:46-51`) probes with `try_lock_shared`; `WouldBlock` means armed.
- Why, their words (`bell.rs:13-22`): "An OS lock, not daemon state: the kernel drops it the instant the bell dies ... The file is never unlinked: removing it while another bell holds it would split the lock across two inodes."

**Ownership by a parent: `--owner-pid`.**
- Flow: `detach_if_owned` (`cli/mod.rs:164-199`). Validate owner (`:171`), re-spawn self with `--detached-child`, `pre_exec(setsid)` (`:187`), launcher `exit(0)`. Why `setsid` and not `process_group(0)`: "Claude Code also walks processes by session id" (`:183`).
- Output streams: a pipe or socket is replaced by null so the launcher's caller reads EOF (`detached_stdio`, `:205-222`). Files and ttys inherited so startup errors reach the skill's `.stderr`.
- Validation (`habilis-network-795 daemon/shutdown.rs:154-170`): refuse pid 0, 1, self, or dead. Zombie counts dead (`util/process.rs:43,67`: `live_start_time` returns `None` for state Z).
- Watch (`shutdown.rs:176-199, 238-246`): `Owner { pid, start }`; every `PPID_WATCH_INTERVAL` (1500 ms, `habilis-network-util/src/tuning.rs:195`) compare `live_start_time(pid)` to the start captured at launch. Start time defeats pid reuse. Mismatch feeds the same quit channel as SIGTERM.
- Without an owner: compare `getppid()` to the original, not to 1, because systemd reparents to a subreaper (`shutdown.rs:250-262`). Skipped when original ppid is 1.
- Signals: ctrl-c, SIGTERM, SIGHUP, SIGQUIT all take the graceful path; "Only SIGKILL stays uncatchable" (`shutdown.rs:111`).
- Ownership lookup for tools: `owned_by` (`cli/session.rs:76`) matches daemon ancestry or the recorded `owner_pid` and its ancestry.

**Shutdown order** (`shutdown.rs:32-60`): app waiters failed, then state file removed first, then `Left` broadcast signed, then 500 ms sleep so it propagates. State file goes first so a kill in the sleep cannot strand a fresh-looking file.

**Stale state clearing.** `discover()` (`cli/session.rs:43-70`) walks every `*.json` state file under the runtime base. Live means `is_alive(pid)` and `comm_of(pid) == "agent-gossip"`. Else the file is deleted and counted as `cleaned`. Doc: leftovers of SIGKILL or power loss "stop rendering as ghost sessions".

**Restart against a stale connection, their experience.** They hit the same-id pathology on the beacon rendezvous id, which successive members reuse:
- `beacon/mod.rs:486-492`: the rival probe dials from a throwaway endpoint because an ex-holder carries "stale per-id connection state ... the reused-endpoint-id pathology of iroh-gossip#10". A dial from it "joins that dead state and times out".
- `daemon/heal.rs:133-141`: on a resume edge "a reused endpoint id can be stuck behind a stale accepted rendezvous connection (iroh-gossip#10)"; remedy is a direct re-dial of remembered peers (`rebridge_known`).
- `daemon/shutdown.rs:46-52` and `gossip/broadcast.rs:293-301`: the `Left` is deliberately not mirrored over unicast, because a `Left` landing while a survivor's gossip still holds the dying beacon's link re-stands the beacon into a stale connection and stalls.
- These comments are at pinned rev 795c4f8 and name a fork-based engine. Whether their iroh-gossip fork carries the #43 fix is not established here.

**Replay with a stable key.** `transport/endpoint_proof.rs:48-58`: an endpoint that keeps its key across runs lets an old `PeerInfo` be replayed to restore the old signer. Their remedy for an unproven signer: answer on gossip, not point to point.

**Tests.**
- `tests/gossip_network.rs:~900-965`: second daemon on a held state file exits non-zero with "already in use"; first daemon unharmed. Not run.
- `gossip_network.rs:3561` `detached_daemon_follows_its_owner`: launcher returns under 2 s with empty stderr; daemon is its own pgid leader and not a child of the launcher; `session` and `bell-check` find it via owner; killing the owner removes the state file within 15 s. Not run.
- `gossip_network.rs:3729` `owner_pid_rejects_init_and_dead_owner`: owners 1, dead, zombie each exit 1 with one stderr line. Not run.
- `shutdown.rs:279-395` (engine): owner watch stays while owner lives, quits on exit, on unreaped zombie, and on pid reissue (simulated with `start + 1`; the test says a real reissue changing start time "is a property of the OS"). Not run.
- `tests/lossless_receive.rs:251,405`: bell exits cleanly when daemon leaves, errors when daemon crashes. Not run.

### mcpmesh (stable endpoint key, redb lock)

**Identity.** One Ed25519 device key, 32 raw bytes, 0600. The iroh `SecretKey` is built from it (`node/src/daemon/boot.rs:260`, key at `:234`). Endpoint id is therefore deterministic from the file. First run mints, later runs reload.
- Mint (`trust/src/keys.rs:54-85`): write 0600 temp file in the same dir with a per-call unique name, `fsync`, publish with `hard_link`. `hard_link` fails if the target exists, so a key is never overwritten and a racing writer loses cleanly. Loser loops back and loads the winner's key (`:25-52`, 4 tries then error).
- An embedder may supply the key instead; then no key file is read or written (`boot.rs:218-232`, `BootOverrides::device_key`).

**Single instance, two layers.**
1. Process shell (`cli/src/daemonshell.rs:21-52, 58-71`): per-uid `flock` exclusive non-blocking on `<runtime>/mcpmesh.lock`, taken "BEFORE anything else so the stale-socket unlink and the state.redb open are single-daemon-safe". Loser logs and `return Ok(())` (exit 0). Lock lives as the `File` for process lifetime; file never unlinked. Windows has no flock; the control-pipe bind with `FILE_FLAG_FIRST_PIPE_INSTANCE` is the singleton, so `serve_forever` binds first.
2. Data root (`node/src/node.rs:11-45`): "one node per root, enforced by redb's exclusive database lock". The root holds `config/device.key` and `data/state.redb`. A redb open refusal anywhere in the error chain maps to typed `StartError::DataDirInUse`. This is the layer that binds identity to a lock: the lock file lives in the same root as the key.
- Embedded nodes: "its own mesh identity under its own root ... never touches the per-user daemon's ... singleton lock" (`node.rs:1-4`, `daemonshell.rs:1-4`).

**Start order (`boot.rs:38-260`).**
1. flock (shell).
2. Bind control socket first (`boot.rs:45`). Stale socket unlinked inside `bind_local` with "NO liveness guard of its own", sound because the flock already excludes a live daemon (`node/src/ipc.rs:43-50`).
3. Config and device key.
4. Validate config that could fail open (presence mode, rates, local discovery), "BEFORE binding a socket" (`:243-256`).
5. Bind the iroh endpoint with endpoint hooks UNARMED, so every gated ALPN fails closed (`:257-260`). "Nothing dials between this bind and that arm."
6. Open the peer store (redb, blocking thread), build gate, arm hooks, start accept loop.

**Shutdown** (`boot.rs:97-119`, `shutdown_booted`): stop accepting, abort loops, and await the gate loop that owns the redb lock ("aborting without awaiting only SCHEDULES the drop (#61)"), then `endpoint.close()`. A leaked task holding the lock made a restart on the same root fail; the fix is the awaited teardown.

**Auto-start convergence** (`cli/src/client.rs:50-121`): try connect to the socket; if dead, spawn detached daemon and poll-connect with capped backoff (20 ms to 200 ms, 10 s deadline). A child that exits non-zero fails fast with its stderr. Exit zero means it lost the flock; keep polling for the winner's socket.

**Duplicate identity elsewhere (#134).** Two nodes from copies of one root present one endpoint id; the relay serves one and tells the displaced client `Status::SameEndpointIdConnected`. iroh exposes it only as a log line, so mcpmesh matches that line with a `tracing` layer (`node/src/diag.rs:1-76`) and exposes `self_network.identity_conflict_epoch` (docs/local-protocol.md:1321-1335). Their ruling: advisory only, "must never gate authorization, refuse a peer, or stop a node" (`diag.rs:41-45`), because a relay can forge it. Sticky timestamp, because the relay announces once.

**Peers holding a connection to a restarted node.** Dial side keeps a weak cache of one connection per remote (`node/src/daemon/conn_cache.rs:1-50`). An entry that no longer upgrades or has `close_reason()` set is skipped and a fresh dial replaces it. Doc admits "a peer that restarts while a dial is in flight can leave the loser of that race alive for its session" (`:31`).

**Tests.**
- `cli/tests/first_run.rs:12` `first_run_mints_key_second_run_reuses_it`: same endpoint id across two process runs. Not run.
- `trust/src/keys.rs:325` first call mints, second reloads same key. Not run.
- `cli/tests/daemon_autostart.rs:219-260`: a directly spawned second daemon "must LOSE the flock race" and exit 0; original keeps serving. Not run.
- `daemon_autostart.rs:287` `racing_ensure_daemon_calls_converge_on_one_daemon`. Not run.
- `cli/tests/harness/mod.rs:60-92`: shutdown helper waits until the socket refuses and a probe `flock` succeeds, so tests assert the lock is released after clean exit. Clean exit only.
- `node/tests/start.rs:106` `a_second_node_on_the_same_root_is_refused` (typed `DataDirInUse`); `:80` `shutdown_frees_the_root_even_with_a_live_subscription_attached` (restart on same root within 5 s). Not run.
- `node/src/daemon/conn_cache.rs:715` `a_closed_connection_is_not_reused`: peer closes (a sever), dialer's next session gets a new connection (accept count 2). The close is peer-initiated and clean, not a dead peer.

### Tunnet (persisted identity key, rotation)

**Identity.** `AgentIdentity { secret_bytes: [u8;32], signing_key }` (`crates/tunnet-core/src/identity.rs`). Endpoint id = hex of the verifying key; the iroh `SecretKey` is built from the same bytes (`tunnet-core/src/node.rs:388,590`). Stored inside an AES-256-GCM sealed payload `state.enc` plus `state.enc.meta`, tiered by platform (TPM/DPAPI, Android keystore, macOS keychain, derived-from-machine, plaintext opt-out) (`secret_store/mod.rs:1-12`). Each file written with `atomic_write_private`: `AtomicWriteFile`, mode 0600 not inherited, `fsync`, commit (`tunnet-common/src/persistence.rs:11-44`). The two files are two separate atomic writes (`secret_store/mod.rs:202,206`).

**Single instance: one coordinator per machine per network, not per key.**
- `coordinator::acquire(network_id)` (`coordinator/unix.rs:24-60`), up to 5 tries: if the socket exists and connects, become a thin `Client`. If connect fails, unlink the socket. Then `flock(LOCK_EX|LOCK_NB)` on `$TUNNET_RUNTIME_DIR/tunnet-{network_id}.lock`; winner unlinks any socket, binds the Unix socket, becomes `Coordinator`. Loser sleeps 150 ms and retries.
- The lock fd is leaked on purpose (`std::mem::forget(file)`, `unix.rs:79`), and in the node the lock holder is forgotten too (`tunnet/src/node.rs:257`). So the file is never unlinked in production, and the kernel frees the lock at exit.
- A `Client` process drops its loaded identity unused (`node.rs:230`); only the coordinator builds the endpoint. Other processes proxy `open_stream` and `list_peers` over the socket (`coordinator/mod.rs:1-12`).
- Order in `bootstrap` (`node.rs:195-260`): identity already loaded, then `acquire`, then endpoint built inside `bootstrap_coordinator`, then the coordinator socket served. Lock precedes endpoint bind.
- Windows: named pipe plus named mutex (same module doc).

**Rotation.** `rotate_identity` (`tunnet-core/src/direct/connect.rs:295-316`): `AgentIdentity::generate()`, `persist_agent` with the existing networks, return the new contact id derived from the new endpoint id. Exposed as `POST /v1/direct/connect/rotate` (`local_api/router.rs:135,1192`), CLI `tunnet connect rotate` (`tunnet-cli/src/cmds_direct.rs:265`). The function does not touch the running endpoint; the new key is what the next load reads. Rotation changes the contact id; no old-to-new link is written. No test for rotation found by grep.

**Tests.** `coordinator/mod.rs:169` `acquire_first_process_is_coordinator` only. `secret_store/mod.rs:624` asserts mode 0600. `persistence.rs:52-100` asserts replace-existing and 0600-not-inherited. Not run.

### iroh-gossip and iroh-relay (the layer N's unknowns 2 and 3 live in)

**Gossip, issue history.** n0-computer/iroh-gossip#10 "can't re-establish severed gossip connection until the old connection times out" (opened for a program that panicked and restarted with the same key). Maintainer comment 2025-02-03: if an accepted connection is running, "we reject any new ones", so stale accepted connections must time out first; proposed principle "you're in charge of the connections you initiate, and the other side is in charge of theirs". Frando 2025-03-21 pointed to #43 and asked for real-world testing. Issue closed completed 2025-03-24.

**Gossip, 0.101.0 mechanism (`src/net.rs`).**
- `PeerState::accept_conn` (`:773-802`): a new connection for a known peer id becomes the active send path at once; the old id goes to `other_conns`; dropping the old `send_tx` ends its send loop "which will also notify the peer that the old connection may be dropped".
- `handle_connection_task_finished` (`:564-595`): `PeerDisconnected` fires only if the closing connection is the active one; otherwise it is removed from `other_conns` and logged "remaining N other connections".
- Protocol layer (`src/proto/hyparview.rs:694-745`): `add_active` for a peer already in the active view returns without emitting `NeighborUp`; `NeighborDown` is emitted only on removal from the active view (`:645`).
- Inference from these three, not observed: a same-key restart whose new connection lands before the old one dies produces neither NeighborDown nor NeighborUp at the receiver. If the old active connection dies first, NeighborDown then NeighborUp.

**Gossip test.** `src/net.rs:1646` `can_die_and_reconnect`: spawn a broadcaster with key K, receive its message, cancel it abruptly, spawn a new one with the same K, assert a second message arrives within 5 s ("the reconnect with the same endpoint id worked"). I ran it: `cargo test --lib can_die_and_reconnect`, 1 passed in 0.31 s (log `/tmp/ra-state/m4-iroh-gossip-test.log`). The kill is cancellation of a thread's runtime in the same process. Whether QUIC sends a close frame on that drop was not checked, so the test may not exercise a stale accepted connection.

**Relay mechanism (iroh-relay 1.3.0 `src/server/clients.rs:76-100`).** `register`: if the endpoint id is already registered, the new client becomes `active`, the old is pushed to `inactive` and sent `Status::SameEndpointIdConnected`. `unregister` (`:109-170`): if the active one leaves and an inactive exists, the latest inactive is promoted and told `Healthy`. Test `test_clients_same_endpoint_id` (`:348`): datagrams go to the old client, then to the new one after registration, old gets the status frame, and after the new disconnects the old is active again. Not run.

## Options this gives estafette

Each: what, cost, proof.

1. **Exclusive flock on the card sidecar, held for process life; take it before building the endpoint.** Cost: about 15 lines; one fd for process life; loser maps to `card_held`. Proof: mcpmesh `daemonshell.rs:58-71` (non-blocking exclusive, `WouldBlock` is the loser), Tunnet `unix.rs:75`, agent-gossip `bell.rs:34`. Closest precedent to N is mcpmesh's redb root lock, which sits beside the device key and yields typed `DataDirInUse` (`node.rs:36-45`, `tests/start.rs:106`). Practice the three share: never unlink the lock file (agent-gossip states why, `bell.rs:13-22`); the kernel is the only releaser.
2. **Order: lock, then key, then bind, then arm, then serve.** Cost: none beyond ordering. Proof: mcpmesh `boot.rs:45-260`, including an endpoint bound with hooks unarmed so gated ALPNs fail closed until the store exists. Fits D10/3.9: inbox socket at process start, lock and endpoint at `init`. agent-gossip binds its IPC socket before marking ready so ready never precedes an accepting socket (`transport/ipc.rs:84-87`).
3. **Stale socket cleanup under the lock, unconditionally.** Cost: one `remove_file`. Proof: mcpmesh `ipc.rs:43-50` argues it is safe only because the lock already excludes a live holder; Tunnet `unix.rs:42` does the same. agent-gossip unlinks with no lock and relies on a prior check (`ipc.rs:101`), which is weaker. Estafette's pid-named inbox socket (D33) is not at risk of this collision; the card lock and sidecar are the shared resource.
4. **Parent ownership by stdio close.** Estafette is a stdio MCP child of the harness, so 3.9's "stdin closed or signal -> Stopping" is the owner link. If the node is ever detached, copy `Owner { pid, start_time }` polled at 1.5 s: validate at start (not 0, 1, self, dead, zombie), quit when start time changes (`shutdown.rs:171-199`). Cost: about 60 lines plus a per-OS start-time reader (`/proc/<pid>/stat` field 22 on Linux, `proc_bsdinfo` on macOS, `process.rs:43,67`). Proof: agent-gossip tests at `shutdown.rs:279-395` and `gossip_network.rs:3561`.
5. **Departure order.** Remove the externally visible state first, then announce, then sleep to let it propagate. Cost: 500 ms on exit. Proof: agent-gossip `shutdown.rs:32-60`. Maps to D18-D20 Departure.
6. **Same-key return against a stale connection: do nothing extra at the gossip layer.** iroh-gossip 0.101.0 swaps the send path on the new inbound connection (`net.rs:773-802`), and the test at `net.rs:1646` covers a same-key reconnect. Cost: none. Not covered: a hard kill that leaves a live-looking accepted connection. Add an estafette test for it (see below). Fallback if it stalls: direct re-dial of remembered peers on the restart edge (agent-gossip `heal.rs:133-141`, `rebridge_known`).
7. **Do not mirror a departure over a second path to peers that may still hold the dead link.** Proof: agent-gossip `shutdown.rs:46-52` (`Left` gossip only) after hitting a stall in that case. Applies to Departure under N only if estafette also sends it direct (D18-D20 say direct stream for Introduce, gossip for presence).
8. **Key file mint: temp file 0600, fsync, `hard_link` to publish.** Cost: about 40 lines. Proof: mcpmesh `keys.rs:54-85`, tested at `keys.rs:325` and `first_run.rs:12`. Gives no-overwrite and race-safe first creation, which matters if two sessions both run first-time `init` for one new card. Tunnet's route is `AtomicWriteFile` with rename semantics (`persistence.rs:11-24`), which replaces.
9. **Duplicate-identity detection via the relay.** Only meaningful when a relay is used. Cost: a `tracing` layer; advisory only. Proof: mcpmesh `diag.rs` (rule: never gate on it). Covers the copied-sidecar case that D8 puts out of scope.
10. **Replay guard on a stable key.** agent-gossip names the risk (`endpoint_proof.rs:48-58`): a stable endpoint key lets an old signed presence be replayed to restore an old state. N's `ts` ordering (older ignored) is the same kind of guard; the project's choice was to avoid the problem by minting a key per run.
11. **Rotation = new identity, new contact id.** Tunnet generates and persists a new key and returns the new id (`connect.rs:295-316`); the running node is not re-keyed in that call. Under N a card key rotation changes the member's node id for every peer.

## What could make this wrong

- Unknown 1: I ran one process kill on Darwin 24.3.0 only (`/tmp/m4-scripts/flock_kill.py`). Linux, a killed process that had forked children, and a lock on a network filesystem were not tested. A forked child that inherits the fd keeps the lock alive after the parent dies; Rust std opens with close-on-exec so spawned programs do not inherit, a plain `fork` does (general knowledge, not read from these sources).
- No project tests a SIGKILLed lock holder. Their tests cover clean shutdown (mcpmesh harness) or a lost race.
- Unknown 2 is inference from `net.rs` and `hyparview.rs`. No test records the event stream across a same-key restart. `can_die_and_reconnect` passes in 0.31 s, which is consistent with both "new connection replaced the old" and "old connection was closed on drop".
- Unknown 3: the direct (non-relay) path was not read. Which instance answers during the gap before the new process binds is not shown by any source I read; the relay source shows only newest-wins.
- Idle timeout: N assumes 10 s. I did not read estafette's transport config or iroh's default. mcpmesh sets keepalive and idle explicitly (`net/src/endpoint.rs:654-700`) and says the negotiated idle timeout is the minimum of both sides.
- agent-gossip's engine comments cite #10 as current at the pinned rev. The engine uses a fork of iroh; I did not check whether the fork carries #43.
- agent-gossip has no persistent key, so none of its lifecycle code was exercised with a same-key restart. Its owner-pid and state-file mechanics transfer to N only by analogy.
- Tunnet's lock is per network, not per key: two profiles with different keys on one machine and one network share one coordinator. Tunnet does not demonstrate lock-per-identity.
- Tests marked "Not run" were read, not executed. Only `can_die_and_reconnect` and my flock script ran.
- mcpmesh version in the pinned checkout is the formula 0.58.0; comments cite iroh 1.0.1 and 1.0.3. The estafette stack reads iroh 1.3.0 in the registry. Relay behavior was read at 1.3.0; gossip at 0.101.0.
