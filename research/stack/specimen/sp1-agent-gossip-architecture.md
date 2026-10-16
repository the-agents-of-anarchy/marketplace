# agent-gossip: architecture and presence

Date: 2026-10-16.

Repos and commits read:

- `agent-habilis/agent-gossip` at `2c5e132` (HEAD, 531 commits). Latest release 0.12.4 at `106b709`.
- `agent-habilis/agent-swarm` URL. It redirects to the same repo, with the same HEAD `2c5e132`.
- `agent-habilis/habilis-network` at `8722df5` (HEAD, 105 commits). Pinned rev `795c4f8` is an ancestor of HEAD.

Line numbers below refer to these commits.

## What it is

agent-gossip is the application layer of a serverless mesh for AI agent sessions. It exposes one A2A-shaped data model through three frontends: a CLI, an MCP stdio server, and a Rust library. Its mesh transport, identity, routing, gating, and healing live in a separate engine crate, `habilis-network`, which agent-gossip consumes by git rev. The app's own code is the A2A layer, the frontends, and the shipped binary with its skills.

## Crate layout

agent-gossip workspace, `Cargo.toml:1-20`:

- `crates/agent-gossip`: the app. Modules `a2a` (data model, gossip binding, task state machine), `api` (library `MeshSession`), `bridge` (HTTP tunnel for `a2a expose` and `a2a connect`), `cli`, `mcp`, `output`, `harness` (test-only, feature-gated), `events`.
- `crates/agent-gossip-test-fixtures`: shared harness for the 18 integration binaries (crate README). It depends back on the app as a dev-dependency.
- `crates/slot-template`: build-time renderer for the multi-file skills into the single-file `SKILL.md` tree the binary embeds.
- `crates/tasks`: the `cargo task` runner.
- `crates/agent-gossip-wasm-client`: browser client. Excluded from the workspace, with its own lockfile. Not read.

habilis-network workspace, `crates/`: 16 crates. The engine is `habilis-network`. The rest are leaf crates: `-protocol` (wire vocabulary over `iroh-base` only), `-util` (tuning constants), `-doc` (automerge), `-logging`, `-chunks`, `-stream`, `-stream-cli`, `-netplay`, `-ffi` (C ABI for mallorca), `-wasm`, `-bench-wasm`, and four transport crates: `-iroh-gossip-transport`, `-iroh-multihop-transport`, `-iroh-webrtc-transport`, `-iroh-transport-util`.

## How it works

### One event loop, three frontends

The engine runs one `tokio::select!` loop. Source: `habilis-network/crates/habilis-network/src/daemon/event_loop.rs:674` and `:786`. Its arms cover IPC, HTTP, gossip events, probe outcomes, timers, and quit.

The app plugs into the loop through two traits:

- `NodeApp` handles inbound app frames: `classify` and `on_app_frame`. Source: `habilis-network/.../gossip/app.rs:52`.
- `NodeDriver` adds timers, startup and tick hooks, and typed IPC, session, and HTTP inputs. Source: `habilis-network/.../daemon/app.rs:18`.

`A2aApp` implements both once: `crates/agent-gossip/src/a2a/node.rs:25` and `:94`. Each frontend builds an `A2aApp` and calls `setup_mesh`, then one of two entry points into the same loop:

- Library: `MeshSession::join` at `crates/agent-gossip/src/api/session.rs:41` calls `join_decoded` (`:81`, `setup_mesh` at `:91`), then `InProcessSession::spawn` (`:158`). That calls `Node::spawn` (`api/inproc.rs:52`), which spawns `daemon::run` (`habilis-network/.../daemon/node.rs:108`). `daemon::run` is `event_loop::run` (`daemon/mod.rs:59`).
- MCP: `mcp/session.rs:34` to `:56` wrap `InProcessSession::create_poll`, `join_poll`, and `topic_poll` (`api/inproc.rs:76` to `:120`). The MCP server runs the loop inside its own process, poll-only and silent.
- CLI: `create`, `join`, and `topic` call `setup_mesh` (`crates/agent-gossip/src/cli/mod.rs:286`) and then `run_event_loop` (`:11`, the same `event_loop::run`). With `--owner-pid` the CLI re-executes itself detached in a new session (`cli/mod.rs:164` to `:196`). Other commands reach the daemon over a Unix socket (`cli/mod.rs:750` onward, `cli/ipc.rs`).

So the frontends differ in process boundary, not in loop code. The README claim "nothing is reimplemented per binding" holds for the loop and the app.

The library and MCP sessions hold the loop inside their process. Dropping one only aborts the loop task (`habilis-network/.../daemon/node.rs:255` to `:262`). The graceful path is `leave()`. I did not trace what `leave()` sends to peers.

### Joining a mesh

- A join id decodes to the mesh config. Topic, rendezvous identity, and loopback port ladder derive locally. The engine doc says the first network contact is relay registration. Source: `habilis-network/docs/architecture.md:205` to `:212`.
- A topic mesh seeds from `SHA256(domain || trimmed string)`. Source: `habilis-network-protocol/src/crypto.rs:55` to `:58`. The doc at `docs/architecture.md:181` says the same, and the code matches it.
- Lookups are `mdns`, `dht`, and `relay`, set by `--lookup` and combined with `--transport`. Source: crate README and the changelog for 0.9.0 (commit `83d7d38`).
- The relay ladder's rung 0 is `https://relay.agent-habilis.com/`, marked in the code as "ours". Source: `habilis-network/crates/habilis-network/src/lookup/relay.rs:55` to `:63`.
- The rendezvous identity is seed-derived. A member co-hosts it as a beacon. Public meshes use an ephemeral port found by node id through pkarr. Private meshes use a deterministic loopback port ladder. Source: `habilis-network/.../beacon/mod.rs:1` to `:20`.
- Directory: `create --advertise` re-broadcasts into a directory, and `discover` browses it. Sources: `crates/agent-gossip/src/api/advertise.rs`, `api/directory.rs`.

### Presence

Presence has two layers. The engine decides whether a member is present on the transport. The app adds task beats, reader state, receipts, and the local bell.

Engine layer:

- Presence messages carry one of three subtypes: `Joined`, `Left`, `Alive`. Source: `habilis-network-protocol/src/message/mod.rs:99` to `:103`.
- Presence is updated on received traffic. The lifecycle module's `observe` runs for every received message. Source: `habilis-network/.../lifecycle/mod.rs:58` and the module doc.
- A member sends `Alive` only when it has broadcast nothing for `ALIVE_INTERVAL`, 30 s. Chatty members send no keepalive. Source: `lifecycle/heartbeat.rs:16` to `:30`, `tuning.rs:136`.
- A sweep runs every `SWEEP_INTERVAL`, 10 s. It evicts any member unheard for more than `ALIVE_TIMEOUT`, 90 s. Source: `tuning.rs:146` and `:157`, `lifecycle/heartbeat.rs:41`.
- Eviction emits a timeout event only for members whose arrival was surfaced. Ghosts seen only through backlog are dropped silently. Source: the `tick_sweep` doc, `heartbeat.rs:41`.
- A graceful departure sends `Left`. A returning quiet member is marked `returned`. Sources: `lifecycle/mod.rs:147` to `:185`, `membership.rs:13` to `:21`.
- The timeout is a hidden flag, `--alive-timeout-secs`. Source: crate README.
- The earlier survey of iroh-gossip, `research/stack/surveys/f2-gossip.md:16`, reports that the gossip layer has no heartbeat. I did not re-check that claim here. The `Alive` keepalive is the engine's own addition.

App layer:

- Task beats: a status update tagged `mesh:beat` keeps a task alive. Both daemons beat every live task. A party cancels after 2 minutes with no leg or beat from the other. Sources: `crates/agent-gossip/src/a2a/extensions.rs:8`, `CHANGELOG.md` for 0.11.1.
- Reader liveness is pulled, not published. `ask_readers` sends `mesh/reader.get` to each live peer that has an endpoint, with one shared 500 ms deadline. A peer that misses the deadline keeps its row with no `reader` key. Source: `crates/agent-gossip/src/a2a/peer_path.rs:103` to `:168`.
- Delivery receipts: `delivered` when the recipient daemon takes the frame, `read` when its agent polls it. Receipts are sealed and sent unicast. Source: `crates/agent-gossip/src/a2a/receipt.rs:1` to `:60`.
- The bell is a local file lock held by a long-poll process. The earlier survey, `research/stack/surveys/a1b-agent-swarm-mcp.md:66`, describes it. I did not re-read it.

## Relation to habilis-network

Direction in code: agent-gossip depends on habilis-network. The root manifest pins `habilis-network` by rev `795c4f8` at `Cargo.toml:47`. The app's `[dependencies]` add it with the `blob` feature. No habilis crate depends on agent-gossip. The engine is `publish = false`, and it has three consumers: agent-gossip, agent-share, and mallorca through the C ABI. Source: `habilis-network/crates/habilis-network/src/lib.rs:5` to `:7`, `agent-gossip/AGENTS.md:78` to `:82`.

The pin is not the engine's head. `795c4f8` is the commit that holds PR #16. The changelog for 0.12.2 says so. The engine's main is at `8722df5`, 105 commits.

History of the engine, from both repos:

- Through 2026-07-05, the engine lived inside agent-gossip's `src`. Commit `7da270b` moved it into an `agent-habilis-gossip` crate in the same repo.
- 2026-07-31, habilis-network commit `86bd79d` "extract fofoca from the mallorca repo". The engine had been vendored inside mallorca, a separate app.
- 2026-08-05, agent-gossip commit `98f517c` "consume the fofoca engine instead of vendoring it". Its body says the repo "kept its own copy, so the two drifted." It then pinned the engine by rev.
- 2026-10-13, commit `23c3c0c` "move the engine from fofoca to habilis-network", released as 0.12.0.

FORKED.md in habilis-network says the workspace "began as a verbatim vendoring" of agent-gossip, and names divergence commit `f81b0529`. That SHA exists in agent-gossip's history, as a 2026-07-30 chat commit. habilis-network's own history starts at the 2026-07-31 mallorca extraction and does not contain that SHA. So the fork claim cannot be checked from the engine's history. habilis-network issue #8 says FORKED.md does not match its tree.

The current relationship is consumer and engine. The word "fork" describes history, not the current dependency.

Copies across the boundary: agent-gossip holds its own copy of the transport ids (`crates/agent-gossip/src/a2a/peer_path.rs:8` to `:10`) and of `LookupSet::any`. habilis-network issue #9, open, asks the engine to export them.

## Relation to A2A

A2A appears in five places in the code. None is an HTTP transport for the mesh.

- Data model. Types for `Task`, `Message`, `Part`, `Artifact`, `TaskState`, and `AgentCard` follow A2A v1.0. Source: `crates/agent-gossip/src/a2a/model/mod.rs:9` (`PROTOCOL_VERSION = "1.0"`).
- Gossip binding. The agent card declares `protocol_binding = GOSSIP_BINDING`, `https://agent-habilis.dev/a2a/binding/gossip/v1`. Source: `a2a/card.rs:50`, `a2a/extensions.rs:1`. A2A objects travel as engine app frames with tags `a2a_broadcast`, `a2a_msg`, `a2a_status`, `a2a_artifact`, `a2a_req`, `a2a_resp`, and `a2a_receipt`. Source: `a2a/wire.rs`. The classifier rejects a frame whose tag and addressing disagree. Source: `a2a/node.rs:487` onward.
- Directed RPC. `a2a_req` and `a2a_resp` carry JSON-RPC-style operations, such as `SendMessage`. Source: `a2a/rpc.rs:69` and `:125`.
- Localhost binding. `--a2a-serve [PORT]` starts a local HTTP JSON-RPC 2.0 server with a bearer token, and serves the card at the well-known path. Source: `cli/args/shared.rs:30` to `:37`, `a2a/http.rs`.
- Bridge. `a2a expose` and `a2a connect` tunnel plain A2A HTTP over the mesh with their own ALPN. The module doc says the bridge is "not A2A core." Source: `a2a/mod.rs:23` to `:25`.

So "built on A2A" means three things in code: the object shapes, a custom binding identifier, and a local JSON-RPC face. The wire is the engine's frames over iroh. I did not run the A2A contract tests, so I cannot say how closely the binding conforms.

## Why, by their own account

- The app's crate README gives the reason for the split. The payload stays opaque to the transport, and an app assumption that leaked downward would break the other consumers. Source: `crates/agent-gossip/README.md`, "Why the app and the engine are separate".
- The 0.12.0 changelog states the engine rename and the breaking id change. It gives no reason. Source: `CHANGELOG.md`, 0.12.0.
- Commit `98f517c` gives the reason for ending vendoring: the copy drifted, and fixes lived only in one repo. Source: its commit body.
- habilis-network commit `86bd79d` gives the reason for extracting the engine from mallorca: the engine "had outgrown" its host app.
- The README says the mesh is "a custom A2A binding (spec §12)". Source: root `README.md`, section "A2A".

## How it evolved

Releases, from GitHub dates. Tags `v0.2.0`, `v0.4.0`, and `v0.4.1` have no GitHub release. Entries for releases before 0.10.0 use commit subjects in each tag range. The repo's changelog starts at 0.10.0.

| Release | Date | Architecture change |
|---|---|---|
| v0.4.2 to v0.4.4 | 06-03 to 06-05 | Engine still in the app. Iroh and iroh-gossip run as leak-fix forks (`2157f76`, `1076a3a`). Inbound message validation hardened (`v0.4.4` range). |
| v0.7.1 | 07-25 | Native A2A v1.0 adopted on 07-03 (`115ac1c`), with directed frames on unicast (`a624769`). Engine moved into a crate in the same repo on 07-05 (`7da270b`). Leak-fix fork patches dropped on 07-05 (`42e8523`). Directed-over-gossip transport removed 07-11 (`5dc1507`). Repo named agent-gossip 07-04, agent-mesh 07-05, agent-square 07-06, and agent-gossip again 07-17. |
| v0.7.2, v0.7.3, v0.7.4 | 07-25 to 07-27 | Skills and bell work. Orchestrate skill with 2-minute stall detection. |
| v0.8.0 | 08-13 | Engine consumed by rev from 08-05 (`98f517c`) instead of vendored. Bridge local port gated. Task label carried to the worker. |
| v0.9.0 | 09-22 | Lookup and transport split: `--lookup` and `--transport` replace the old flags, and `--public` is dropped (`83d7d38`, 09-21). Browser peer added 08-14 (`165c559`). |
| v0.10.0 | 09-24 | Release changesets. Stop hook refuses a turn with the bell unarmed. No engine change. |
| v0.11.0 | 09-24 | Topic gossips may use relay transport. The transport becomes part of the topic id. |
| v0.11.1 | 09-25 | Both daemons beat every live task. Silent tasks cancel after 2 minutes. Full-disk log writes stop aborting the daemon. Replayed chat and task legs no longer surface. |
| v0.11.2 | 09-27 | Short task ids in the todo view. No architecture change. |
| v0.11.3 | 09-30 | Daemon survives the 2-hour background limit. |
| v0.12.0 | 10-13 | Engine renamed fofoca to habilis-network (`23c3c0c`). Mesh ids and tickets become version 2, so older gossips stop working. Default transport `udp,webrtc,gossip`. Relay carries payload only with relay lookup. |
| v0.12.1 | 10-13 | File attach on `a2a call`. Engine pinned to `88f8c3d`. |
| v0.12.2 | 10-14 | Loopback rooms heal after a split. Engine pinned to `795c4f8`. |
| v0.12.3 | 10-15 | Release flow changed in CI only. |
| v0.12.4 | 10-15 | Delivery receipts and reader liveness (`30d8747`). |

Other fixed points in the history:

- 05-18: initial commit. Commit `c4f2500` points references at `agent-habilis/swarm`, the repo's name at that time.
- 05-24: relay ladder with deterministic bootstrap failover (`8de4ed0`).
- 05-26: iroh 1.0 release candidate (`69ca1c2`).
- 05-27: environment-variable config replaced with constants and hidden flags (`b83c9fc`).
- 06-29: shared state split into a `state` channel and a `meta` channel (`673311c`).
- 07-11: interactive surface removed, JSON-only output (`4dd28ee`).
- 07-30: A2A and the product name stripped from the engine (`5fe1194`). Engine public surface narrowed to six role-based modules (`170efe0`).

## Where it strains

- **Drop without leave.** `Node::drop` aborts the loop and runs no leave path (`daemon/node.rs:255`). I did not trace whether peers receive `Left`. A silent member is evicted only after the 90 s sweep, by my reading of `heartbeat.rs`.
- **Reader state is pulled, and the wording says otherwise.** Commit `30d8747` is titled "publish reader liveness". The code queries each peer, with a 500 ms deadline, in `peer_path.rs:103` to `:168`. A slow peer shows no reader key. That reads as unknown, not absent.
- **Presence cost is not measured.** Each idle member sends one `Alive` every 30 s, and each receiver tracks every member. The repo has `benches/idle_cost.rs`. I did not read it.
- **Doc and code mismatches.** The root README says there is "nothing to host", but rung 0 of the default relay ladder is the project's own host (`lookup/relay.rs:63`). habilis-network issue #8 says FORKED.md and a changelog line do not match the tree.
- **Known limits, self-flagged.** The 0.12.0 changelog says directory sessions run with multihop on. habilis-network issue #7 says the same. The 0.11.1 changelog says a full disk can still abort the engine's daemon through the state-file heartbeat. That is "still open, in the engine".
- **Open app issues, agent-gossip.** #29: a daemon that dies is not rejoined, and the rejoin gets a new random nickname, so open tasks are lost. #37: no stuck-task status check. #28: a join with a live peer's nickname does not fail. #2: a native peer cannot message a browser peer. #42: two tests fail under host load.
- **Open engine issues.** #9: agent-gossip copies two engine items by hand. #3: a stream reader never attaches to some producers.
- **Pin drift.** The app pins `795c4f8`. The engine's main is at `8722df5`. Consumers must bump by hand.
- **Corrections to earlier surveys.** `research/stack/surveys/a3-habilis.md:85` and `:86` call habilis-network a fork that agent-gossip "upstream" produced. The current code shows a consumer, not a fork. `a3-habilis.md:8` and `:16` list agent-swarm and agent-gossip as two repos. The swarm URL redirects to agent-gossip, and both clones have HEAD `2c5e132`.

## Observations for the owner

- The loop is one code path. The frontends differ only in process boundary. A library or MCP member lives exactly as long as its host process.
- Presence has two layers. Engine liveness (`Alive`, sweep) decides reachability. App beats, reader pulls, receipts, and the bell decide whether a task or a reader is active.
- The repo name has cycled: swarm, gossip, mesh, square, gossip. The engine name has cycled too: fofoca, then habilis-network. The crate has been named agent-gossip since 07-17.
- The engine routes on tag and addressee and never parses the body, per its README. The app parses bodies in its own classifier.
- A2A here is a vocabulary, a custom binding identifier, and a local JSON-RPC face. The wire is the engine's frames over iroh, not HTTP.

## Not read

- agent-gossip: bodies of `mcp/mod.rs`, `a2a/send.rs`, `a2a/task.rs`, `a2a/session.rs`; `bridge/*` internals; `cli/bell.rs` (only through the earlier survey); `api/tests.rs`; the integration tests (names only, from the README); `benches/`; `docs/manual.txt`; `docs/identity-binding.md`; `HABILIS_NETWORK_CHANGES.md`; `AGENTS.md` (grepped only); the wasm client; `packages/`.
- habilis-network: most of `daemon/` (heal, timers, state); the `gossip/` receive path beyond the app seam; `transport/` beyond the search hits; `lookup/mdns.rs` and `lookup/dht.rs`; beacon internals beyond the module doc; `membership.rs` beyond its signatures; `docs/architecture.md` sections 7 to 11; FORKED.md beyond its first 60 lines.
- Other repos: agent-share and mallorca were not cloned. The surveys `a1b-agent-swarm-mcp.md`, `a3-habilis.md`, and `f2-gossip.md` are cited, not re-read.
- GitHub: issue titles for both repos. Full bodies were read only for agent-gossip #29 and habilis-network #8 and #9. PR threads and release notes for v0.4.2 through v0.9.0 were not read.
- No tests, builds, or benchmarks were run.
