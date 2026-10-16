# P3a: presence in Peersey and Tunnet
Date: 2026-10-16.

## Sources read
- Peersey, commit 24ebec219b755cbba2aaac719ce4f97a72c5da2b (shallow clone, one commit): `Cargo.toml`, `src/room.rs`, `src/lib.rs`, `src/content.rs`, `examples/chat.rs` (presence and send paths), `tests/` (grep only).
- Tunnet, commit 75b317be0653e8906b33eb46f49d70cc0906dae7 (shallow clone, one commit): `crates/tunnet-core/src/direct/presence.rs` (whole), `direct/mod.rs`, `direct/membership.rs` (header and neighbor events), `direct/grants.rs` (record structs and signers), `node.rs`, `identity.rs`, `iroh_pool.rs` (liveness, idle sweeper), `local_api/handlers.rs` (online field), `secret_store/`, `send.rs` (stream use), `tunnet-agent/src/runtime/mesh.rs` and `actors/presence.rs` (wiring), `tunnet-common/src/lib.rs` (topic derivation), workspace `Cargo.toml` and `Cargo.lock`.
- iroh-gossip-rendezvous 0.2.1 from the crates.io tarball, extracted to `/tmp/ra-src/crates-p3a/rv/`: `src/gossip_glue.rs`, `src/builder.rs`, `src/rendezvous.rs`, `src/protocol.rs` (signing, grep), `src/merge.rs`, `src/wire.rs`, `PROTOCOL.md` §3, §5, §9 (checked against source, not trusted alone).
- iroh-gossip 0.99.0 and 0.101.0 from the crates.io tarballs: `src/api.rs`, `src/net.rs`, `src/proto/hyparview.rs`, `src/proto/plumtree.rs`.
- Spec `spec/blueprint.md`: D3, D4, D12, D18, D19, D20, section 3.4. D13 and D21 appeared in the same excerpt; cited where relevant.
- crates.io API metadata for `peersey`, `iroh-gossip-rendezvous`, `tunnet-core`, `iroh-gossip`.

Versions: estafette measures iroh 1.3.0 and iroh-gossip 0.101.0. Tunnet matches that pair. Peersey does not: it pins iroh 1.0.0-rc.0 and uses iroh-gossip 0.99.

## Peersey (github.com/antepodeum/Peersey, 24ebec2, iroh 1.0.0-rc.0)

### What it does for this scope
Peersey is a pub/sub room library. A room is joined by a public name or a private 256-bit key. Membership and presence are the direct gossip neighbors of the room's topic. Presence in the chat example is one announcement per neighbor-up event. Messages are gossip broadcasts.

### How, in code
- Presence source: the room exposes raw iroh-gossip `NeighborUp` and `NeighborDown` as `PeerJoined` and `PeerLeft` (`src/room.rs:116-124`). The sender field of each received message is dropped (`src/room.rs:120-122`). The gossip layer reports `delivered_from` on every message (`iroh-gossip 0.99.0 src/api.rs:371`), but the room does not read it.
- Who is online: the chat counts `peers.len() + 1`, where `peers` is only the set of gossip neighbors (`examples/chat.rs:290-292`, `:408`). It is not a room roster.
- Presence announcement: on `PeerJoined` the chat broadcasts `ChatPacket::Presence { peer, name, online_for_ms }` to the whole room (`examples/chat.rs:766-776`). The packet type is at `examples/chat.rs:40-47`. The receiver keys the entry on the `peer` field inside the payload (`examples/chat.rs:294-318`), not on the gossip sender.
- Departure: `PeerLeft` removes the entry and writes a "left" feed line (`examples/chat.rs:321-327`, `:778`). No message is sent to other members. The removal is local.
- Heartbeat: none in the chat. `examples/chat.rs` has no `interval`, `sleep`, or tick. The rendezvous crate runs jittered DHT loops (`PROTOCOL.md` §5, HealLoop and WriteLoop). Those write and read DHT slots to find peers. They do not carry liveness.
- Clean stop: `room.shutdown()` (`examples/chat.rs:706`) calls `Rendezvous::shutdown` (`src/rendezvous.rs:152-162`). That calls the gossip actor's `shutdown` before closing the endpoint (`src/gossip_glue.rs:135-141`). The gossip actor sends `Disconnect { alive: false }` to each active neighbor (`iroh-gossip 0.99.0 src/net.rs:259-265`, `:388-392`; `src/proto/hyparview.rs:356-359`). Neighbors then see `NeighborDown`.
- Unclean exit: `Rendezvous` drop only cancels its tasks (`src/rendezvous.rs:164-170`). It sends no `Disconnect`. Neighbors learn of the loss from the closed connection.
- Crash latency: the time until `NeighborDown` after a crash depends on iroh's connection idle timeout. I did not read that code.
- Identity: the room's peer id is `rendezvous.node_id()` (`src/room.rs:169-173`). The rendezvous builder makes a fresh secret key when none is set (`src/gossip_glue.rs:94`, `iroh-gossip-rendezvous src/builder.rs:118`). Each room join therefore gets a new endpoint id.
- Second key: the content node has a persistent identity in `identity.key` (`src/content.rs:67-80`, `:154-158`). It is a separate endpoint from the room. A single process running both has two endpoint ids.
- Messages: `room.send` is a gossip broadcast (`src/room.rs:156-159`). Chat messages go through it (`examples/chat.rs:742-743`). No stream, no ack.
- File and live streams: direct QUIC streams on the content endpoint (`src/content.rs`, `src/live.rs:26`, `HANDSHAKE_TIMEOUT`). These are separate from the room.

### Crates it uses
- `iroh = "=1.0.0-rc.0"` (`Cargo.toml:15`).
- `iroh-gossip = "0.99"` (`Cargo.toml:17`), resolved to 0.99.0 through the rendezvous lock.
- `iroh-gossip-rendezvous = "0.2.1"` (`Cargo.toml:18`). Its own deps include `iroh 1.0.0-rc.0`, `iroh-gossip 0.99.0`, `ed25519-dalek 3.0.0-pre.7`, `chacha20poly1305 0.10`, `mainline 6`.
- `iroh-blobs = 0.101.0` (`Cargo.toml:16`) for files.
- Peersey has no Cargo.lock in the clone.

### Maturity
- Peersey: one published version, 0.2.0, on 2026-08-20. 16 downloads (crates.io). Clone is shallow, so no release history in git.
- Presence tests: the chat example has unit tests for the presence packet round trip and `on_peer_joined` (`examples/chat.rs:~960-1000`). `tests/` has no presence or neighbor test (grep).
- Rendezvous 0.2.1: three versions, 284 downloads, last release 2026-05-11. It has `tests/two_node_bootstrap.rs` and `tests/stateright_model.rs`. I did not run them, and I did not check which test covers neighbor events.

### What estafette could take
- Crate: nothing for presence. The rendezvous crate is DHT-based bootstrap. It has no presence signal, and its PROTOCOL.md §5 says "Leave: no protocol action."
- Pattern: announce once on each new neighbor, so a late joiner learns the others. This is the shape of D18 without a claim.

### Against the spec
- D12: messages travel over gossip (`src/room.rs:156-159`, `examples/chat.rs:742-743`). D12 rejects this, citing no ack and every node seeing every message. Peersey does it on purpose.
- D4: nothing binds a presence name or peer id to a key beyond the payload itself. The receiver trusts the `peer` and `name` fields (`examples/chat.rs:294-300`). Any room member can announce any peer id. The consequence D4 names, "any node could announce itself as any card," is live here.
- D3: the room key is fresh per join (`src/gossip_glue.rs:94`). That matches D3. It also means a room member has no stable identity across rejoins. Only the self-reported name persists.
- D18: presence is broadcast to the whole room (`examples/chat.rs:774`), not sent as a direct reply to the new neighbor. D18 says reply "directly to that node."
- D19: no application-level departure is sent. The only departure signal is iroh-gossip's `Disconnect`, and only on clean gossip-actor shutdown (`src/gossip_glue.rs:135-141`). A process that exits without calling `shutdown` gives no departure.
- D20: `NeighborDown` removes the peer at once, with no probe (`examples/chat.rs:321-327`). A gossip-topology change looks the same as a departure in the feed. D20 predicted this under "If you change this."


## Tunnet (github.com/tunnetio/Tunnet, 75b317b, iroh 1.3.0, iroh-gossip 0.101.0)

### What it does for this scope
Tunnet's core crate runs a Direct-mode mesh. Presence is a signed beacon sent every 30 seconds to a gossip topic, with a 90-second expiry. The online verdict combines that beacon with the state of the pool's direct QUIC connection. Membership is a separate iroh-docs document, and gossip neighbor events are logged there but not acted on.

### How, in code
- Topic: `blake3(network_id bytes)` (`crates/tunnet-common/src/lib.rs:513-515`). The network id is a UUID, not a secret.
- Beacon: fields are network id, endpoint id, hostname, mesh ip, agent version, issued and expiry times, and a hex signature (`crates/tunnet-core/src/direct/presence.rs:21-34`). These fields go over gossip in clear JSON.
- Endpoint id: `endpoint_id` is the hex of the beacon signer's verifying key (`presence.rs:163`). The signer is the node identity key (`crates/tunnet-agent/src/runtime/mesh.rs:878-926`).
- Receive: the receiver parses the beacon, checks the expiry and the signature against the `endpoint_id` key, then upserts it (`presence.rs:189-208`, verify at `:144-153`). It does not check the gossip sender. The other gossip events are dropped at `presence.rs:209`.
- Publish: a 30-second ticker (`presence.rs:19`, `:227`) rebuilds and broadcasts the beacon (`:232-246`). It also prunes expired entries (`:231`). The TTL is 90 seconds (`:18`, `:171`).
- Online verdict: `peer_presence_online` returns true for any unexpired beacon, false for only expired entries, and none for never seen (`crates/tunnet-core/src/node.rs:185-205`).
- Composition: the local API reports `online = true` if the pool has a live connection, and otherwise uses the presence verdict (`crates/tunnet-core/src/local_api/handlers.rs:486-500`). Pool liveness is `live_conn().is_some()` (`crates/tunnet-core/src/iroh_pool.rs`, `fn has_live`). That is an open connection, not a probe. Direct mode closes idle connections after 120 seconds (`iroh_pool.rs:28`, `:3-4`). The idle sweeper ticks every 10 seconds (`iroh_pool.rs:1009`).
- Last seen: the pool's last activity, or else the earliest unexpired beacon issue time (`node.rs:211-219`, `handlers.rs:488-490`).
- Neighbor events in membership: logged only (`crates/tunnet-core/src/direct/membership.rs:393-398`).
- Departure: no beacon is sent on stop. Stopping the presence actor cancels its task (`crates/tunnet-agent/src/actors/presence.rs`, `on_stop` and the `ShutdownPresence` handler). Peers learn of a stop only when the beacon expires.
- Crash: the same as a clean stop. Derived from the 30-second publish interval and the 90-second TTL, a crashed peer with no live connection shows online for 60 to 90 seconds after the crash. I did not measure this.
- Replay: beacons carry no nonce and the receiver does not bind them to the gossip sender. A captured beacon is accepted until its expiry. This is derived from `presence.rs:144-153` and `:193-201`. I did not test it.
- Identity: one persistent `AgentIdentity` holds 32 secret bytes and its verifying key (`crates/tunnet-core/src/identity.rs:4-7`). The bytes are stored by the secret store (`secret_store/persist.rs:33`, `secret_store/mod.rs:84`). The iroh endpoint secret is built from those same bytes (`node.rs:388-399`, `:590-592`). The endpoint key is therefore long-lived.
- Rotation: a new identity is made only by an explicit command (`crates/tunnet-core/src/direct/connect.rs:297-306`, `rotate_identity`).
- Member record: `SignedMemberRecord` carries `endpoint_id`, `grant`, and a field named `endpoint_sig` (`crates/tunnet-core/src/direct/grants.rs:33-46`). `sign_member_record` signs that record with the coordinator key (`grants.rs:257-265`). The field name says endpoint, but the signer is the coordinator.
- Member metadata: `SignedMemberMetadata` is signed with the endpoint key (`grants.rs:205-212`, `sign_member_metadata`). It is produced at `membership.rs:624`.
- Messages: a message opens a bidirectional QUIC stream on the send ALPN and writes an offer (`crates/tunnet-core/src/send.rs:493-495`).
- Other heartbeats, not presence: a 15-second heartbeat in `sync.rs:324` (not read), and a 20-second edge control ping in `crates/tunnet-core/src/tunnel.rs:289`.
- Claim: no `Claim` type exists in the workspace. A search for `struct Claim`, `Claim {`, `sign_claim`, and `verify_claim` found nothing. Spec section 3.4 is not implemented under that name.

### Crates it uses (presence path)
- `iroh 1.3.0` (workspace `Cargo.toml:156`, `Cargo.lock:3949`).
- `iroh-gossip 0.101.0` (workspace `Cargo.toml:160`, `Cargo.lock:4124`).
- `iroh-docs` (membership), `ed25519-dalek` (signing), `blake3` (topic), `jiff` (times), `uuid`, `serde_json`, `hex`, `parking_lot`. I did not check versions for these beyond the workspace file.

### Maturity
- `tunnet-core` on crates.io: 0.7.0, updated 2026-07-18, 74 downloads.
- Clone: one commit, last 2026-10-15, no tags. Release history was not available from the shallow clone.
- Tests for presence: `presence.rs:264-286` covers sign and verify and the expiry rule. No test found covers the gossip receive path or the online composition.

### What estafette could take
- Crate: nothing for presence as such. The signed-beacon scheme and the connection-plus-beacon online verdict are code, not a crate.
- Pattern: sign the presence record with the endpoint's own key and check the signature against the endpoint id in the record. This is the same binding as D4 for presence.
- Pattern: combine an open-connection check with the beacon for the online verdict. This is closer to a probe than the beacon alone.

### Against the spec
- D3: the identity key persists and is the endpoint key (`node.rs:388-399`, `secret_store/persist.rs:33`). Each session does not get a new transport key. Rotation is explicit (`connect.rs:297-306`). The spec's reason for D3 is that the transport key carries no identity. Here the transport key is the identity, so the question is whether the spec intends to keep the two apart.
- D4 and 3.4: the claim the spec describes is not implemented. Binding comes from the coordinator's signature on the member record (`grants.rs:257-265`) and from the endpoint's own signature on beacons and metadata (`presence.rs:138-153`, `grants.rs:205-212`). The spec's D4 rejects a central registry. A coordinator signature is a central attestation.
- D12: consistent. Presence travels over gossip (`presence.rs:187-251`). Messages travel over direct streams (`send.rs:493-495`).
- D13: the topic is derived from a UUID that appears in clear in every beacon (`presence.rs:23`, `tunnet-common/src/lib.rs:513-515`). The spec derives the topic from a shared secret. Membership is not decided by the topic here.
- D18: rejected. The spec says "Periodic heartbeats: constant traffic that grows with the member count." Tunnet broadcasts a beacon every 30 seconds to the whole topic (`presence.rs:227`, `:246`).
- D19: the spec says a clean stop "sends a departure." Tunnet sends nothing on stop, so a stop and a crash look the same (`actors/presence.rs`).
- D20: Tunnet does not probe or announce unreachability. It ignores gossip neighbor events for presence (`presence.rs:209`) and logs them in membership (`membership.rs:393-398`). Its online verdict includes an open connection, which is the nearest thing to a direct check.

## Cross-project observations
- Both apps use iroh-gossip's neighbor events as the only signal of joins, and neither has the spec's join-by-claim step. Peersey uses the events directly (`src/room.rs:118-119`). Tunnet ignores them for presence (`presence.rs:209`).
- Neither app gets the sender of a gossip message from the gossip layer. `delivered_from` is the previous hop in the relay path, not the author (`iroh-gossip 0.99.0 src/proto/plumtree.rs:88-100`). Neither iroh-gossip 0.99 nor 0.101 signs messages (grep for `SignedMessage` and `signature` found nothing in either). Authorship must therefore come from the application.
- Tunnet authenticates its beacons at the application layer. Peersey does not authenticate its presence or chat packets at all (`examples/chat.rs:294-300`, `room.rs:120-122`).
- Departure is the weak point for both. Peersey gets a departure only when iroh-gossip's actor shuts down cleanly (`src/gossip_glue.rs:135-141`). Tunnet gets none.
- Periodic traffic appears in both. Peersey's rendezvous crate runs jittered DHT loops (`PROTOCOL.md` §5). Tunnet broadcasts beacons every 30 seconds. Neither uses periodic traffic as a departure signal.

## Not read
- iroh's QUIC idle timeout, which sets crash-detection latency for both apps.
- iroh-gossip HyParView and Plumtree internals beyond the disconnect and quit paths.
- The rendezvous crate's DHT slot logic beyond PROTOCOL.md §3 and §5, and its test suites (not run).
- Tunnet `sync.rs` heartbeat and `ping.rs` (not read; not presence).
- Tunnet `membership.rs` beyond the neighbor events and the metadata call site.
- Peersey `live.rs` and `content.rs` beyond the identity path.
- No application was run and no test suite was executed.
