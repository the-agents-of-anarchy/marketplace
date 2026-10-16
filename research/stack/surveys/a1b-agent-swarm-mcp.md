# Agent-swarm MCP and session layer (A1b)

Date: 2026-10-16. Scope: agent-swarm MCP server, session wrapper, and the daemon and hook code that the MCP path does and does not use. Source for this report: the brief at `research/stack/surveys/brief.md` and the spec sections D28-D31, 3.10, 3.11.

## Sources read

- agent-swarm at `106b7093d37f202aaaca7803cd7c8db82413e04a` (release 0.12.4, 2026-10-15), clone at `/tmp/ra-src/agent-swarm`.
- `crates/agent-gossip/src/mcp/mod.rs` (1-100, 100-330, 330-430, 420-1030 by tool signature and selected bodies; 1060-1070 for `ok_json`).
- `crates/agent-gossip/src/mcp/session.rs` (1-60, 200-245).
- `crates/agent-gossip/src/api/inproc.rs` (15-60).
- `crates/agent-gossip/src/lib.rs` (90-110).
- `crates/agent-gossip/src/cli/bell.rs` (1-60).
- `crates/agent-gossip/src/cli/session.rs` (400-440).
- `crates/agent-gossip/src/cli/mod.rs` (755-770).
- `crates/agent-gossip/src/cli/agent.rs` (580-600).
- `crates/agent-gossip/src/a2a/surfaced.rs` (280-292, 468-492).
- `skills/shared/bell-hook.yaml`, root `Cargo.toml` (line 47), `crates/agent-gossip/Cargo.toml`.
- habilis-network at `8722df5cb0251c95e63bb3618854ee56b1f70cc5` (main), clone at `/tmp/ra-src/habilis-network`: `crates/habilis-network-protocol/src/identity.rs` (1-40), `crates/habilis-network/src/membership/app.rs` (1002-1013).
- Spec `spec/blueprint.md`: 2.8 (D28-D31, lines 288-315), 3.10 (686-755), 3.11 (756-775). Section 3.12 (bridge contract) printed in the same read; it is not in scope and is noted only where compared.

## Tool list and input fields

Nineteen tools, registered in one `#[tool_router]` impl (`mcp/mod.rs:423`). The module doc lists the same nineteen (`mcp/mod.rs:1-25`). The habilis report counted eighteen names. It omitted `a2a_call`, at `mod.rs:813`.

| Tool | Fn line | Input fields (type, required or optional, default) |
|---|---|---|
| create_gossip | 428 | name (string, opt), nickname (string, opt), lookup (list of mdns, dht, relay; default empty), relay_urls (list, opt), transport (list of udp, webrtc, multihop, gossip, relay; default empty), advertise (bool, false), directory (string, opt), password (string, opt) |
| join_gossip | 501 | gossip (string, req), nickname (opt), password (opt) |
| topic_gossip | 535 | string (string, req), nickname (opt) |
| discover_gossips | 577 | directory (opt, default global) |
| leave_gossip | 561 | none |
| send_broadcast | 631 | text (string, req) |
| send_msg | 646 | to (string, req, a nickname), text (string, req) |
| fetch_messages | 663 | after (u64, opt), long (bool, false) |
| gossip_info | 712 | none |
| ping | 730 | none |
| gossip_version | 740 | none |
| gossip_manual | 752 | none |
| task_status | 764 | task_id (req), state (req, one of working, input-required, completed, failed, canceled), note (opt) |
| task_artifact | 781 | task_id (req), text (string, default empty), file (opt), file_name (opt), file_mime (opt) |
| a2a_call | 813 | to (req), method (req), params (JSON, default object), timeout_secs (u64, default 45, `a2a/tuning.rs:41`) |
| apply_state_merge | 850 | merge (JSON, req; RFC 7386 patch) |
| get_state | 866 | none |
| apply_meta_merge | 879 | merge (JSON, req; RFC 7386 patch) |
| get_meta | 895 | none |

Notes on the schemas:
- `CreateMeshArgs` alone carries `#[serde(deny_unknown_fields)]` (`mod.rs:106`). The other argument structs, as read, do not.
- Schema text is `schemars` output from doc comments on each field (`mod.rs:105-317`).

## How the MCP server reaches the engine

- In-process, no socket, no daemon. `AgentGossipServer` holds `Option<Session>` behind a mutex (`mcp/mod.rs:91-93`). `Session` wraps `InProcessSession` (`mcp/session.rs:22-26`).
- `InProcessSession::spawn` calls `habilis_network::runtime::Node::spawn` in the MCP process (`api/inproc.rs:36-53`). The MCP path creates and joins poll-only: `create_poll`, `join_poll`, `topic_poll` (`api/inproc.rs:72-118`).
- The MCP server starts no daemon. The daemon exists only for the CLI path (see below).
- Transport: rmcp over stdio (`mcp/mod.rs:80-86`). One mesh per MCP server instance. Create, leave, and join can cycle (`mcp/mod.rs:41-42` doc).

## How messages reach the agent

- MCP path: poll only. The module doc says `notifications/message` exists but no major client surfaces it (`mcp/mod.rs:27-31`).
- The server instructions state it as a rule, opening with "NO PUSH" and "POLL" (`mcp/mod.rs:925-928`).
- Long-poll: `fetch_messages(long=true)` parks up to about 60 s (`mcp/mod.rs:203-218`, argument doc). Empty result means the window elapsed.
- CLI and Claude Code path, outside MCP:
  - A Stop hook, from `skills/shared/bell-hook.yaml`, runs `agent-gossip bell-check --session-pid "$PPID" || true` with a 15 s timeout.
  - `bell_check` prints `{"decision":"block", ...}` when an owned session has no armed bell after a grace period (`cli/session.rs:411-436`). This refuses the end of the turn.
  - A bell is an `agent-gossip poll --long` process holding an OS file lock `<mesh runtime>/<nickname>.bell` (`cli/bell.rs:15-60`). It re-issues an IPC `Poll{long}` to the local daemon (`cli/mod.rs:757-770`).
  - Each Claude Code bell ends itself at `--max-secs 7000` under the harness limit of 7200000 ms (`cli/agent.rs:584-599`, test).
  - The daemon answers a long poll at once when an unserved waking event exists, otherwise parks it (`a2a/surfaced.rs:468-492`).
  - Wake mechanism: the bell exiting as a background task. Inferred from `cli/agent.rs:585` and `a2a/surfaced.rs:284-291`. The harness side was not traced.
- The Claude Code skill also reads the CLI's `--output json` stream directly (`mcp/mod.rs:37-40`). This is a live push that does not use MCP.
- No hook code exists in `mcp/`. `hook` matches in the crate sit in `cli/agent.rs` (skill front matter, 331-390) and `cli/session.rs` (bell check).

## Inbox cursor model

- Per MCP session, in process memory: `last_delivered_seq: Mutex<Option<u64>>` (`mcp/session.rs:22-26`).
- Cursor-less call (`after` absent) returns events past the cursor and advances it (`mcp/session.rs:214-226`).
- Explicit `after` is a non-mutating replay. It does not move the cursor (`mcp/session.rs:203-212`).
- Default cursor is 0, so the first call returns full history, about 200 events per the doc (`mcp/session.rs:233-237`; `mcp/mod.rs:203-218`).
- `missed_before` is set when the cursor aged out of the event ring (`FetchMessagesResult`, `mcp/mod.rs:386-400`).
- The CLI path keeps a separate daemon-side read cursor, `last_served` (`a2a/surfaced.rs:280-292`). It starts at 0 on a fresh daemon. Its bell reads never advance it.
- The MCP cursor is independent of the daemon cursor. The source says so at `mcp/session.rs:228-232`.

## Identity binding

- agent-swarm binds no key. A session is a nickname (`word-word`, random by default) passed to create or join (`mcp/mod.rs:107-163`). Invalid nicknames are rejected (`mcp/mod.rs:468`, `516`).
- Engine identity (habilis-network, read at `8722df5`): a per-peer Ed25519 identity that signs every authored frame (`protocol/identity.rs:66`).
- The key is ephemeral. It is minted per create or join and held in memory for the process lifetime. A restart mints a new key under the same nickname (`protocol/identity.rs:14-19`).
- The nickname is a display label, bound to the key trust-on-first-use by receivers (`protocol/identity.rs:11-12`, `27-30`).
- Not located: the production call site that generates the key. Grep found only test sites.
- Version caveat: root `Cargo.toml:47` pins habilis-network at `795c4f88`. That object is not in the shallow clone, so every engine claim above is read at `8722df5` (main) and is unverified at the pin.

## Against the spec

- **D28, six tools, static.** Static: yes. The router is compile-time and no runtime change was seen (`mcp/mod.rs:423`). Count: no. Nineteen tools, not six. None of the spec names `list_cards`, `init`, or `inbox` appears. The spec's count and names are contradicted. Its static-list rationale holds.
- **D29, effective handle only.** Contradicted in form. `send_msg` takes `to` as a nickname (`mcp/mod.rs:194-201`). The spec's effective handle is not a field here. Engine peer lookup is keyed by a string name. The one lookup I read is test-gated (`membership/app.rs:1002-1013`). The production uniqueness rule was not traced.
- **D30, identity status in every response.** Absent. No `you`, `status`, or claim field appears in `mcp/`. The only identity-like state is `not_in_mesh_error` (`mcp/mod.rs:1021-1026`). A lost tie-break or displacement has no signal path here.
- **D31, five message fields.** Contradicted. Inbound events are full event objects with `seq`, `event`, `type`, `display`, `self`, and transient kinds such as presence and `ping_report` (`mcp/mod.rs:386-400`, `EVENT SHAPE` at `mcp/mod.rs:936`).
- **3.10, envelope and error codes.** Not implemented. Success returns `ok_json` of a result struct (`mcp/mod.rs:1069`). Errors are JSON-RPC errors (`invalid_params`, `invalid_request`, `internal_error`). The closed code list of 3.10 does not exist here.
- **3.11, inbox socket.** Not present in the MCP path. The MCP reads through a poll call, not a socket. The CLI daemon has a local IPC socket under the runtime base (`lib.rs:94-101`). Its frame shape was not compared. Two differences from 3.11 are visible: `seq` is per daemon and starts at 0 (`a2a/surfaced.rs:288-289`), where the spec starts at 1. The ring size was not read.

## Estafette's six static tools against agent-swarm

| Estafette (spec 3.10) | agent-swarm nearest | Difference |
|---|---|---|
| `list_cards` | none | No card concept. Identity is a nickname. |
| `init` | `create_gossip`, `join_gossip`, `topic_gossip` | Joins a gossip by id or topic string, not a claimed card. Returns no handle or inbox path. |
| `peers` | `gossip_info` (roster, `mcp/mod.rs:712`), `ping` (`mcp/mod.rs:730`) | Roster is inside a status call, not its own tool. |
| `send` | `send_msg` (`mcp/mod.rs:646`) | Addresses by nickname. Returns the full authoritative record. |
| `broadcast` | `send_broadcast` (`mcp/mod.rs:631`) | Whole gossip only. Estafette takes a `to` list. |
| `inbox` | `fetch_messages` (`mcp/mod.rs:663`) | Cursor advances on cursor-less calls. Long-poll available. |

## Cross-project observations

- **Pull with a cursor, no MCP push.** agent-swarm's MCP and estafette's spec 3.11 both read by cursor. Both state that MCP notifications are unused. agent-swarm states it in code (`mcp/mod.rs:27-31`, `925-928`).
- **Push by hook, Claude Code only.** agent-swarm pushes through a Stop hook that refuses a turn end while a bell is unarmed (`cli/session.rs:411-436`). Estafette's bridge (spec 3.12, read in passing) uses a SessionStart hook to start a bridge that injects notices. The two designs differ in where the enforcement sits.
- **Identity, opposite choices.** Estafette's spec ties identity to a persisted card. The engine agent-swarm uses mints a new key per process (`protocol/identity.rs:14-19`). The engine's own doc names persistence as a follow-up. This is a fact for the synthesis to weigh against the card decision.
- **Two runtimes in one product.** The MCP path is in-process. The CLI path is a per-session daemon with its own cursor and IPC. Both exist in one binary. The MCP path does not reach the daemon.

## Not read

- `mcp/mod.rs` bodies for `gossip_info`, `task_status`, `task_artifact`, `a2a_call`, `get_state`, and the `ok_json` helper body (`mcp/mod.rs:1069`).
- `mcp/mod.rs` tests and `tests/mcp_stdio.rs` (1401 lines). Those would confirm schemas by snapshot.
- `a2a/send.rs` routing beyond the unknown-peer check (`a2a/send.rs:1626-1640`).
- The daemon event loop, its socket permissions, and the IPC wire format.
- The surfaced-event ring capacity (`a2a/surfaced.rs`).
- The skill files other than `skills/shared/bell-hook.yaml`.
- The wasm client (`crates/agent-gossip-wasm-client`).
- The engine at the pinned revision `795c4f88`, which is absent from the shallow clone. Engine claims are read at `8722df5` only.
- The production site that generates the engine identity key, and the production nickname uniqueness rule.
- Harness-side wake mechanics for background tasks. The bell's wake is inferred, not traced.
- Spec 3.12 in full. It was read only in passing, for the comparison above.
