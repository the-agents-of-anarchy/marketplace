# A3: habilis-network and the agent-habilis org

Date: 2026-10-16.

## Sources read

- habilis-network at 8722df5cb0251c95e63bb3618854ee56b1f70cc5 (commit 2026-10-15). Read: `README.md`, `crates/habilis-network/README.md`, workspace `Cargo.toml` (fork pins, lint notes), `FORKED.md` (1-40), `docs/architecture.md` (1-16, 60-82, 145-245, 380-462, 625-712), `crates/habilis-network/src/lib.rs` (1-40), `transport/send.rs` (18-100, 140-160, 280-330), `transport/mod.rs` (14-17), `gossip/broadcast.rs` (76-108, 398-412), `gossip/recv.rs` (370-456, 980-1020, 1057-1070, 1662-1680), `gossip/antientropy.rs` (255-318), `daemon/state.rs` (616, 1016, 1339), `daemon/message_log.rs` (336-388), `habilis-network-util/src/tuning.rs` (16, 38, 136, 146, 708), `habilis-network-util/src/bounded_queue.rs` (1-40), `examples/mesh_peer.rs` (39-47), test headers of `late_joiner_backfill_loopback.rs`, `missed_chat_backfill_loopback.rs`, `resend_after_loss_loopback.rs`.
- agent-swarm at 106b7093d37f202aaaca7803cd7c8db82413e04a (release 0.12.4, 2026-10-15). Read: `crates/agent-gossip/src/mcp/mod.rs` (tool names and descriptions), `crates/agent-gossip-wasm-client/Cargo.toml` (21), root `Cargo.toml` (47).
- Spec `spec/blueprint.md` lines 1-63 (Part 1) and 107-118 (2.3 invariants).
- `gh repo list agent-habilis` (18 repos) and `gh api repos/agent-habilis/habilis-network`.

## The org

| Repo | Pushed | Stars | Note |
| --- | --- | --- | --- |
| agent-gossip | 2026-10-16 | 8 | Upstream line. habilis-network is a fork of it (FORKED.md:1-10). Not read. |
| habilis-network | 2026-10-16 | 1 | Read below. |
| agent-share | 2026-10-13 | 4 | Peer-to-peer folder sharing. Not read. |
| agent-statusline | 2026-10-13 | 4 | Not relevant. |
| agent-graph, agent-backlog, agent-inject, agent-mock | 2026-07 to 2026-10 | 0 | Not read. |
| iroh, iroh-gossip, iroh-address-lookups, noq | 2026-07 to 2026-10 | 0 | Forks of upstream crates that habilis-network pins. |
| swarm-discovery, net-tools, netdev, RFC, homebrew-tap, llm-coding-benchmark | 2026-06 to 2026-10 | 0 | Not read. |

## habilis-network

### habilis-network (github.com/agent-habilis/habilis-network, 8722df5, iroh 1.0.3 fork)

- What it does for this scope: a serverless gossip engine, version 0.6.0, that a host process links as a library. It carries signed messages, a shared CRDT document, and byte streams among members of a mesh derived from a seed. Its README says it "moves, signs, routes, and heals bytes between peers. It does not know what the bytes mean" (`crates/habilis-network/README.md:3-4`). It is not published (`crates/habilis-network/src/lib.rs:5-7`).
- Components and split: the engine (`crates/habilis-network`), wire types (`-protocol`), CRDT (`-doc`), logging, 1-1 byte streams (`-stream`, `-stream-cli`), content chunks, game rollback netcode (`-netplay`), a C ABI (`-ffi`), a browser build (`-wasm`), and TypeScript packages. The architecture says a mesh join "is a function call, not a daemon" (`docs/architecture.md` Abstract).
- No MCP server and no messaging CLI live in this repo. A grep for `rmcp` finds nothing in the manifests. `transport/mod.rs:16` calls the MCP stdio server "a separate, consumer-side path." The messaging CLI and MCP server sit in agent-swarm (below).
- Transport: iroh QUIC links, with iroh pinned to a fork at git rev `0e7cdb4` (`Cargo.toml:121`) and iroh-gossip to a fork at `28676ce` (`Cargo.toml:157`). No crates.io release is used. The brief records iroh 1.3.0 from crates.io, so the two diverge.
- Routing: broadcasts ride iroh-gossip. Directed messages ride a unicast QUIC stream on `habilis-mesh/unicast/1`, and gossip never carries them (`docs/architecture.md` 7.4). A gossip payload is capped at 3840 bytes (`docs/architecture.md` 7.3).
- Discovery: mDNS, the mainline DHT, and a five-rung relay ladder, with a beacon member that the joiner dials at the rendezvous endpoint (`docs/architecture.md` 1.1, 5.2-5.3). The join id carries the seed (`docs/architecture.md` 4.3).
- Presence: `Presence` joined, left, and alive messages on gossip (`docs/architecture.md` 7.2). Alive is a periodic keepalive with `ALIVE_INTERVAL` 30 s and `ALIVE_TIMEOUT` 90 s (`habilis-network-util/src/tuning.rs:136`, `:146`). The brief says "no heartbeats." This code contradicts that line for habilis.
- Identity: three keys. The iroh endpoint key is minted per endpoint. The author key is Ed25519, minted per process, and "a restart mints a new message key" (`docs/architecture.md` 4.1, 11). No persistent card identity exists here.
- Membership: a mesh is closed by possession of its join id, which carries the 32-byte seed. The architecture calls the id "the bearer credential" (`docs/architecture.md` 4.3). Invite tickets default to 24 hours (4.5).
- Topic meshes: the seed is `SHA256(domain || trimmed string)` (`docs/architecture.md` 4.4). Anyone who knows the string joins. Openness rests on the string, not on a secret. The agent-swarm tool description states this openly (`agent-swarm crates/agent-gossip/src/mcp/mod.rs:533`).
- Sealing: directed bodies use an ephemeral X25519 key and ChaCha20-Poly1305. The signature covers the ciphertext, so a relay verifies the frame and cannot open it (`docs/architecture.md` 4.6). Broadcast bodies stay plaintext to members, and password meshes drop them (4.5).
- Names: no nickname collision adjustment found. A grep for taken, collision, adjust, rename, and suffix over `crates/habilis-network/src` found no nickname handling. Not read in depth.
- Session reception, inside the engine: an NDJSON Unix socket, tagged by `command`, with a 0700 runtime directory and a 0600 socket. It has no in-band authentication (`docs/architecture.md` 10.3). The real command enum lives app-side. The enum at `transport/ipc.rs:339` is a test stand-in.
- Session reception, in agent-swarm: 18 tool functions in `crates/agent-gossip/src/mcp/mod.rs` (19 `#[tool(` matches): create_gossip, join_gossip, topic_gossip, leave_gossip, discover_gossips, send_broadcast, send_msg, fetch_messages, gossip_info, ping, gossip_version, gossip_manual, task_status, task_artifact, apply_state_merge, get_state, apply_meta_merge, get_meta. Input schemas were not extracted. Reception is pull: `fetch_messages` keeps a per-session cursor (`mod.rs:663-669`, description at `:426`).
- Maturity: created 2026-10-02, last push 2026-10-16, 9 open issues, 0 releases, 0 forks. About 40 loopback integration test files under `crates/habilis-network/tests`, plus in-source unit tests. Nothing was run.

### Storage for absent members

Four places hold a message. Each is checked against invariant I6 ("the network keeps no message for an absent member") and I7 ("send tells the truth about delivery").

- **Directed send, addressee endpoint unknown, node meshed.** The caller gets an error. Nothing is stored (`transport/send.rs:74-90`, `gossip/broadcast.rs:76-95`). Consistent with I6 and I7.
- **Node not yet meshed.** A directed frame goes into `pending_outbound`, and the send returns `Delivered::Done` (`gossip/broadcast.rs:96-100`). `Done` here means buffered, not delivered. The type's own doc says `Done` is "Sent, or handed to a warm connection" (`transport/send.rs:23-25`). Against I7.
- **Held frame, endpoint known, only a relay path, no direct path proven.** The frame is parked in `pending_outbound`, capped at 1024 (`tuning.rs:38`). It is requeued at every flush (`gossip/recv.rs:435-455`). Neither `flush_pending` nor `requeue` (`recv.rs:377-456`) has an expiry. The queue rejects the newest item when full, so an ordered prefix survives (`bounded_queue.rs:1-14`). Against I6 if the addressee is absent. Whether a departure removes the endpoint on this path (`daemon/state.rs:1339`) was not traced.
- **Message log, 1000 entries (`tuning.rs:16`).** Anti-entropy re-sends broadcasts a peer missed (`gossip/antientropy.rs:255-296`). The backfill tests show a node that was absent receives chat it missed on its first link (`missed_chat_backfill_loopback.rs`, `late_joiner_backfill_loopback.rs`). Against Part 1 section 1.4 in practice: a returning member receives what was said while it was away.
- **Message log, directed frames.** Inbound directed frames enter the log only when the app's `classify` sets `loggable` (`gossip/recv.rs:985-992`). Own directed frames are never retained (`recv.rs:1068`). A re-send of a directed frame goes only to its addressee (`daemon/message_log.rs:362-383`). So a logged directed frame can wait for an absent addressee if the app opts in. The example app sets `loggable: false` (`examples/mesh_peer.rs:43`).
- The resend outbox holds 256 frames (`tuning.rs:708`). It is transient.

## Against the spec

- Part 1 section 1.4, "No mailbox waits for the absent." Broadcast backfill to returning members behaves like a mailbox for broadcasts. Evidence: `gossip/antientropy.rs:255-296`, `missed_chat_backfill_loopback.rs` header.
- Part 1 section 1.5, "Delivered means the message reached the door." An unmeshed send reports `Done` for a buffered frame. Evidence: `gossip/broadcast.rs:96-100`.
- I6, held frames. A frame for a relay-only addressee has no expiry in the flush path. Evidence: `gossip/recv.rs:377-456`.
- I6, opt-in directed logging. An app can keep a directed frame for an absent addressee through `classify`. Evidence: `gossip/recv.rs:985-992`, `daemon/message_log.rs:362-383`.
- Brief fact "no heartbeats." Habilis sends a 30 s alive keepalive. Evidence: `tuning.rs:136`.
- Brief fact "six static tools." Agent-swarm's MCP server registers 18 functions. I4 requires a static list, which both satisfy. The count itself is a fact for the synthesis to weigh, not a violation.
- Part 1 section 1.2, "A card is a persistent self." Habilis has no durable author identity, and its own architecture lists that as missing (`docs/architecture.md` 11).
- Part 1 section 1.3, names adjusted on collision. No counterpart found.
- I2, I3, I5, I1: no conflict found in the code read. I1 holds in the sense that the engine dispatches on an opaque tag (`docs/architecture.md` 10.2).

## What estafette can learn

- **Validates:** the engine stays apart from the app and dispatches on an opaque tag (`docs/architecture.md` 2 goal 3, 10.2). A local socket with filesystem permissions and no in-band auth is the same design as estafette's inbox (`docs/architecture.md` 10.3).
- **Validates:** a pull inbox with a per-session cursor (`agent-swarm mcp/mod.rs:663-669`).
- **Copy, pattern:** an exact wire version gate that rejects loudly (`docs/architecture.md` 7.1).
- **Copy, pattern:** a bounded queue that rejects the newest item, for an ordered send chain (`bounded_queue.rs:1-14`).
- **Copy, pattern:** a directed frame is re-sent only to its addressee (`daemon/message_log.rs:362-383`). Relevant only if estafette keeps any retained log.
- **Copy, pattern:** sealed directed bodies with an ephemeral key and a signature over ciphertext (`docs/architecture.md` 4.6). The brief's MAC keyed from the network secret has no forward secrecy and no per-message signature. Part 3 was not read to confirm this.
- **Trap:** `Done` for a buffered frame (`gossip/broadcast.rs:96-100`).
- **Trap:** anti-entropy backfill to returning members. If estafette adds gossip repair, it conflicts with Part 1 section 1.4 unless the window is bounded to the presence window.
- **Trap:** an ephemeral author key. Habilis itself flags it as not durable (`docs/architecture.md` 11). This supports estafette's persistent card.
- **Trap:** openness by string (`docs/architecture.md` 4.4) differs from closed by secret. Estafette must keep its secret high entropy.
- **Trap:** git-rev pins on forks. Agent-swarm pins habilis-network at `795c4f8` (`crates/agent-gossip-wasm-client/Cargo.toml:21`), and habilis main is at `8722df5`.
- **Check against estafette's pinned iroh 1.3.0:** fixes habilis carries as fork patches. These are iroh#4294 (mapped address eviction), a relay teardown drain, an RTM_MISS fix in netwatch and portmapper (`Cargo.toml:116-119`), a 10 ms retry loop in swarm-discovery fixed by rkuhn/swarm-discovery#28 (`Cargo.toml:137-138`), and iroh-gossip's connection-churn leak, n0-computer/iroh-gossip#147 (`Cargo.toml:146-156`). Estafette should confirm whether 1.3.0 already carries them.
- **Crate to depend on:** none usable unchanged. Habilis-network is unpublished and depends on forked git revs.

## Cross-project observations

- Habilis-network and agent-swarm both build on iroh, iroh-gossip, Ed25519-signed messages, and a Unix socket. Both pin the same family of forks by git rev.
- Agent-swarm's `crates/agent-gossip` is the upstream line that habilis-network forked. Its MCP server is the consumer layer, and habilis-network is the engine under it (`FORKED.md:6-7`, divergence commit `f81b0529`).
- Agent-swarm's wasm client depends on habilis-network at `795c4f8`. How far that trails main was not measured.

## Not read

- MCP tool input schemas, and any hook mechanism. Only names were extracted from agent-swarm.
- habilis-network stream, netplay, WebRTC and multihop transports, FFI, TypeScript packages, nickname handling, and the chat example.
- Spec Part 2 decisions (sections 2.4-2.12) and Part 3. The brief limited this survey to Part 1 and 2.3.
- Org repos other than the listing: agent-gossip, agent-share, agent-graph, agent-backlog, agent-inject, agent-mock, and RFC.
- Agent-swarm beyond `mcp/mod.rs` and the wasm-client manifest.
- Test execution. Nothing was run.
