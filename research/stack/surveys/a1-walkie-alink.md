# A1: agent-to-agent messaging prior art, walkie and alink

Date: 2026-10-16. Scope per the brief and the owner: addressing, delivery to a session, storage for absent agents, membership gating, presence, and what estafette could take. Spec read: `spec/blueprint.md` Part 1 (lines 1-63), D23, D28, D29, plus D30 for context only.

Evidence is code. Nothing was compiled or run. Where a README claim is not borne out by code, the discrepancy is listed, not resolved.

## Sources read

- walkie: `Squadrant-AI/walkie` at `54b5fa3053291724da894ef5fddf9039de1c6cf8` (clone `/tmp/ra-src/walkie`). Cargo.toml, Cargo.lock (iroh 1.3.0), README.md, skill/SKILL.md, src/main.rs, cli.rs (parts), daemon.rs (parts), session.rs (parts), proto.rs, ipc.rs, ticket.rs, invite.rs, net.rs (parts), paths.rs (parts), tests/ listing and grep.
- alink: `dstotijn/alink` at `b97d274ee7c9427a6a9a5a788e14dfd1032f3ce8` (clone `/tmp/ra-src/alink`). Cargo.toml, Cargo.lock (iroh 1.3.0), README.md, skills/alink/SKILL.md (grep, lines 1-40 and 110-141), src/proto.rs, node.rs (parts), store.rs (parts), control.rs, config.rs (parts), handler.rs (parts), main.rs (parts), ticket.rs (grep).

## walkie (`Squadrant-AI/walkie`, v0.1.2, iroh 1.3.0)

### What it does for this scope

A two-party room. Two agents join by a single-use invite, send text, and pull replies with `wait`. The transport is end-to-end encrypted QUIC over iroh. Delivery is pull-only: the peer's agent must run `wait` to see anything.

### How, in code

- **Agent surface is a CLI, not MCP.** Subcommands: `open`, `join`, `send`, `wait`, `status`, `rooms`, `leave`, `rejoin`, `end`, `update` (`src/main.rs:32-72`). The agent drives them through a shell tool, guided by `skill/SKILL.md`.
- **One daemon per room.** The CLI talks to a per-room Unix socket (`src/paths.rs:114`, request enum `src/ipc.rs:12-26`: Info, Send, Wait, AckBatch, Status, Leave, End).
- **Wire to peer.** ALPN `walkie/1` (`src/net.rs:13`). Length-prefixed JSON frames, 256 KiB cap (`src/proto.rs:8`). Frame enum at `src/proto.rs:25-42`: Hello, Welcome, Reject, Resume, Msg, AckStored, AckRead, Waiting, Leave, End.
- **Addressing.** No names and no handles. The peer is the other side of the room. Message IDs are role-prefixed, `h1`, `j1` (`src/session.rs:352-356`, test). `--reply-to` names an ID.
- **Send attempts nothing.** `Session::send` checks only the Ended state, the 16 KiB body cap, and the outbox caps (`src/session.rs:84-107`). It appends to an in-memory outbox and returns an ID. The CLI prints the ID and exits 0 (`src/cli.rs:264-280`). The sender learns delivery later, through `status` (`src/cli.rs:359`, "outbound unread-by-peer").
- **Two acks.** `AckStored` on receipt releases nothing. The outbox is pruned only on `AckRead` (`src/session.rs:182-189`). Reconnect resends the unacked tail (`src/session.rs:120-140`, `on_peer_resume`).
- **Leave.** Leave waits until the peer has stored everything (`src/daemon.rs:774-778`). The report then names undelivered messages as dropped (`src/cli.rs:404`).
- **Persistence.** The only file written is the ticket: room, role, room secret key, peer ID and address, token, expiry (`src/ticket.rs:12-22`). It is written 0600 by atomic rename (`src/ticket.rs:32-45`). The outbox and inbox live in `Session` (`src/session.rs:41-48`), which has no serialization. A rejoin builds a fresh `Session` (`src/daemon.rs:198-200`).
- **Presence.** The peer sends `Wire::Waiting` when it enters `wait` (`src/daemon.rs:581`, `:632`). The receiver records `peer_last_waited` (`src/session.rs:192-194`). `status` shows it (`src/cli.rs:345`). No gossip. Presence is the live link plus this frame.
- **Membership gate.** Invite string `walkie1:<ticket>.<token>` (`src/invite.rs:6-7`, `:39-45`). The room ID is derived from the token (`src/invite.rs:29`). The host accepts a Hello only if the token matches, in constant time, before expiry (`src/daemon.rs:63-80`, `src/invite.rs:34`). After the first accept the peer's key is pinned, and reconnects are welcome without a token (`src/daemon.rs:63-70`, comment at `:107`).
- **Identity.** A per-room key pair (README, "each room has a fresh key pair"). The room secret is stored in plaintext in the ticket file (`src/ticket.rs:14`; README, Known limits).
- **Discovery.** The invite carries the host's endpoint address. The joiner dials that address (`src/net.rs:106-119`). The endpoint uses the `N0` preset (`src/net.rs:61-62`). No iroh-gossip, no address lookup beyond these.
- **Hooks.** None. No push into a running agent (README, Known limits: "pull-only (`wait`), no push").

### Crates it uses for this

From Cargo.toml: iroh 1 (resolved 1.3.0), iroh-tickets 1, tokio 1, serde and serde_json 1, clap 4, subtle 2 (token compare), sha2 0.10, rand 0.8, data-encoding 2, libc 0.2. No rmcp. No iroh-gossip.

### Maturity

- Version 0.1.2. HEAD commit dated 2026-10-11.
- Tests present for this mechanism: `src/net.rs` loopback handshake and frames, wrong token rejected, unpinned key refused, pinned key reconnects (`src/net.rs:249-392`). `src/session.rs` unit tests for outbox retention, resend after restart, and stored versus read acks. `tests/e2e.rs`, `tests/e2e_relay.rs`, `tests/cli_smoke.rs` present, not read.
- Release count: not checked.

### What estafette could take

- Pattern: separate stored ack from read ack (`src/proto.rs:35-38`, `src/session.rs:182-189`).
- Pattern: constant-time token compare with the `subtle` crate (`src/invite.rs:34`).
- Pattern: 0600 file written by atomic rename (`src/ticket.rs:32-45`).
- Nothing from the room logic.

### Against the spec

- **D23, no store-and-forward: contradicted.** The sender's outbox holds messages for a peer that has not read them, with resend on reconnect (`src/session.rs:84-107`, `:120-140`). The receiver holds stored unread messages in an inbox (`src/session.rs:143-171`). Both are memory only. Leave drops what is undelivered (`src/cli.rs:404`).
- **§1.5, "delivered now or not at all": contradicted.** `send` succeeds with no delivery check (`src/cli.rs:264-280`).
- **D28, static MCP tools: no evidence either way.** walkie has no MCP surface. It is a CLI with a skill.
- **D29, effective handles: no evidence either way.** walkie has no handles.

### Discrepancy: README guarantees versus code

- README, Guarantees: "Messages survive dropped connections, `leave`/`rejoin` and a killed daemon."
- Code: no path writes the outbox or inbox to disk. The grep for `outbox` outside `src/session.rs` returns nothing, and `Session` has no serialization. Survival across a dropped link holds, because the daemon keeps memory. Survival across a killed daemon does not hold, by the code.
- Tests: no test kills or restarts the daemon mid-message (grep of `tests/` for kill, restart, survive returns nothing).
- Not run. A kill test would settle it.

## alink (`dstotijn/alink`, v0.1.0, iroh 1.3.0)

### What it does for this scope

Pairwise agent messaging with a durable outbox. An agent sends to a paired peer by local name. A node retries delivery for up to seven days. Messages carry threads and requests with a lifecycle. Peers can name handlers that run a local command.

### How, in code

- **Agent surface is a CLI plus a Unix socket, not MCP.** Subcommands: `init`, `whoami`, `serve`, `invite`, `join`, `peers`, `send`, `reply`, `run`, `wait`, `listen`, `inbox`, `requests`, `cancel`, `outbox`, `skill`, `show`, `rename`, `remove` (`src/main.rs:54-176`).
- **Node owns the endpoint.** `alink serve` runs one node. Other CLI calls use it over a control socket when it runs (`src/control.rs:18-40`: Flush, Join, FetchCard, Addr; `src/main.rs:349-366`, `Access::Remote`). Otherwise they start a temporary node (README, One node per identity).
- **Addressing by local name.** `alink send alice-claude ...`. Names live in the local `peers` table, `name TEXT NOT NULL UNIQUE` (`src/store.rs:17-22`). Resolution is in `src/store.rs:204-225`. The peer's own card name is advisory (`src/proto.rs:197-203`).
- **Keys underneath.** Each node has a persistent endpoint key loaded from its home (`src/node.rs:608-640`, `home.load_secret_key()`). Frames address peers by endpoint ID (`src/node.rs:191-199`, `peer_by_id`).
- **Wire to peer.** ALPN `alink/1` (`src/proto.rs:13`). Frames: Deliver, Join, GetCard (`src/proto.rs:25-38`). Replies: Ack, which means "durably stored by the receiver", Rejected, Joined, Card (`src/proto.rs:41-56`). Envelope fields: id, thread_id, reply_to, created_at, payload (`src/proto.rs:60-72`). Frame cap 16 MiB (`src/proto.rs:16`).
- **Receive stores before acking.** Inbound Deliver goes to `receive`, which inserts into SQLite and then acks (`src/node.rs:252-283`, `:383`). A duplicate ID is acked again without a second insert (`src/node.rs:283-284`).
- **Outbox and retry.** Messages are a SQLite table with delivery states queued, delivered, failed, expired (`src/store.rs:49`). Retention is `DELIVERY_TTL = 7 days` (`src/store.rs:15`). Expiry runs in `expire_outgoing` (`src/store.rs:424-434`). A flush loop runs every 2 s or when notified (`src/node.rs:26-28`, `:402-412`). Failed peers get a per-peer backoff (`src/store.rs:401-421`).
- **Reconnect triggers flush.** An inbound connection from a known peer resets its backoff and wakes the outbox (`src/node.rs:145-156`). `greet_peers` contacts every peer on serve start (`src/node.rs:569-580`).
- **Sender learns at send time.** `send` tries delivery at once. If the peer is unreachable the CLI says the message is queued (`src/main.rs:1138`, `:1215-1217`).
- **Push into a session is a shell hook.** `alink listen --notify <cmd>` runs `sh -c <cmd>` per new batch, with `ALINK_COUNT`, `ALINK_FROM`, `ALINK_THREADS`, `ALINK_MESSAGE_IDS` in the environment (`src/main.rs:913-925`). The skill recommends watching `listen --json` with a background monitor instead (`skills/alink/SKILL.md`, around lines 113-141).
- **Membership gate.** Invite string `alink://invite/...` (`src/ticket.rs:9`). Default TTL 24 h (`src/main.rs:69-70`). Invite check: secret compared in constant time, single use via `used_at`, expiry (`src/store.rs:271-294`). The invite is consumed on join (`src/node.rs:242`). The joiner is stored as a peer on success (`src/node.rs:535-541`).
- **Inbound gate.** Deliver and GetCard are refused unless the remote endpoint is in the local peers table (`src/node.rs:191-214`). Pairing is bilateral. Each side keeps its own roster. There is no network-wide list.
- **Presence.** `last_seen_at` on the peer row, touched on inbound connection and on join or card fetch (`src/store.rs:189-192`, `src/node.rs:150`, `:542`). Shown by `peers` (`src/main.rs:619`, `:643`, `:1358`). No gossip and no announcement.
- **Handlers.** A paired peer names a handler. The local config supplies the command, and the request text goes to its stdin (`src/handler.rs:241-265`). Per-handler allowlist by peer name or ID, `"*"` allowed (`src/config.rs:179-181`, `:203`).
- **Network mode.** `N0` preset by default, `Minimal` with relays disabled in `local` mode (`src/node.rs:608-625`).

### Crates it uses for this

From Cargo.toml: iroh 1.3.0, rusqlite 0.40.2 bundled, ulid 3.0.0, toml 1.1.6, data-encoding 2.11.1, serde and serde_json, tokio 1.53.2, clap 4.6.7, rand 0.10.3, humantime 2.4.0.

### Maturity

- Version 0.1.0. README calls it early software: "The wire protocol, config format and CLI may change between 0.x releases." HEAD commit dated 2026-10-08.
- Tests for this mechanism: a backoff unit test in `src/store.rs` (around line 779). The `tests/` directory exists, not read.
- Release count: not checked.

### What estafette could take

- Pattern: write to durable storage, then ack. Ack a duplicate again without a second insert (`src/node.rs:273-284`).
- Pattern: `listen --notify` environment-variable hook (`src/main.rs:913-925`).
- Pattern: constant-time secret compare on invites, single use, expiry (`src/store.rs:271-294`). The defining file of `constant_time_eq` was not read.
- Nothing from the outbox, which is the part D23 forbids.

### Against the spec

- **D23, no store-and-forward: contradicted.** Outgoing messages sit in a durable outbox for up to seven days (`src/store.rs:15`, `:424-434`). Incoming messages are stored durably before the ack (`src/node.rs:273-283`).
- **§1.3, names: different mechanism.** Collisions are resolved at local insert by suffixing (`-2`, `-3`, ...), against the local table only (`src/store.rs:161-167`). Nothing is presence-aware.
- **§1.5, sender learns: partly matched.** The sender learns "queued" at send time (`src/main.rs:1215-1217`). Delivery later is learned by status. The message is still held after a "queued" answer (contrary to "delivered now or not at all").
- **§1.6, incoming words carry no authority: contradicted if handlers were adopted.** A paired peer can cause a local command to run with its text on stdin (`src/handler.rs:241-265`, `src/config.rs:179-181`).
- **D28, static MCP tools: no evidence either way.** alink has no MCP surface. The lock file has no rmcp.
- **D29, effective handles: partly matched in shape.** The sender addresses a peer by a local handle, not a key (`src/store.rs:204-225`). The handle is local to each side, so two sides can call the same peer by different names.

## Cross-project observations

- **Both hold messages for absent peers.** walkie keeps an outbox until read (`src/session.rs:84-107`, `:182-189`). alink keeps a seven-day outbox (`src/store.rs:15`). Both sit against D23. Both are the default of this prior art, not an edge case.
- **Neither has an MCP surface or a gossip layer.** No rmcp and no iroh-gossip in either Cargo.lock. Both reach the agent through a CLI and a skill. alink adds a shell hook (`src/main.rs:913-925`).
- **Both use a local Unix socket between the CLI and the one daemon or node** (`src/ipc.rs:12-26`; `src/control.rs:18-40`). A second process reaches the daemon through that socket.
- **Both gate on single-use invites with expiry and constant-time compare.** walkie: 10 min default (README, Commands table), `src/invite.rs:34`. alink: 24 h default (`src/main.rs:69-70`), `src/store.rs:271-294`.
- **Both pair bilaterally, with no roster.** walkie has one peer per room (`src/daemon.rs:63-70`). alink has a local peers table (`src/store.rs:17-22`).
- **Both are on iroh 1.3.0 with N0 defaults.** Both use an ALPN string (`walkie/1`, `alink/1`) and dial by endpoint ID or ticket address.
- **Presence is a link property or a last-seen timestamp in both.** walkie: `Wait` frame (`src/proto.rs:41`). alink: `last_seen_at` (`src/store.rs:189-192`). Neither announces arrival or departure to the network.

## Not read

- walkie: `src/update.rs`, `src/exit.rs`, `src/frame.rs`, `src/model.rs`, most of `src/cli.rs`, `src/daemon.rs` after line 200 except the cited ranges, `docs/` (specs, spikes, explainer), `install.sh`, `scripts/`, `tests/` contents.
- alink: `src/util.rs`, `src/config.rs` beyond the cited ranges, `src/handler.rs` beyond the cited ranges, `src/store.rs` beyond the cited ranges, the `tests/` directory, `SECURITY.md`, `install.sh`, `deny.toml`, `skills/alink/references/service.md`, `skills/alink/SKILL.md` beyond lines 1-40 and 110-141.
- iroh 1.3.0 source: the contents of the `N0` and `Minimal` presets were not checked.
- Not verified by running: the README claim about survival after a killed daemon (walkie), and the five-minute backoff cap (alink, `src/store.rs:401-421` not read in full).
- Release counts for both projects.
