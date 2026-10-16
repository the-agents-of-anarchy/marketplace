# F2 foundation survey: iroh-gossip 0.101.0

Date: 2026-10-16.

Sources read: clone at /tmp/ra-src/f2-gossip, commit 2ce78afe09d89d41d123f28eac19bdc831609cc8 (2026-06-15). Version confirmed at Cargo.toml:3. The crate depends on `iroh = "1"` and on `irpc` 0.17.0 (optional, default `net` feature). Files: Cargo.toml, CHANGELOG.md, src/lib.rs, src/api.rs, src/net.rs (parts), src/net/util.rs (parts), src/net/address_lookup.rs (head), src/proto.rs, src/proto/topic.rs, src/proto/state.rs, src/proto/plumtree.rs (parts), src/proto/hyparview.rs (parts), .github/workflows/ci.yaml, spec/blueprint.md lines 592-674 (3.7 and 3.8). The presence report cites commit 6cbbafa; line numbers here are for 2ce78af. I grepped the presence report only for overlap. No code was run; every finding comes from reading.

## Answers

1. **Join and subscribe.** `subscribe` takes a topic id and a `Vec<EndpointId>` of bootstrap ids, and returns without waiting (api.rs:157). `subscribe_and_join` also awaits the first neighbor (api.rs:140). `subscribe_with_opts` takes `JoinOptions`, which holds a `BTreeSet` of bootstrap ids and a subscription capacity (api.rs:123, 387). Bootstrap ids become a join command at subscribe time (net.rs:641). Peers found later go through `GossipSender::join_peers` (api.rs:192). `GossipTopic` has no `join_peers`; the caller must `split()` first (api.rs:227). Dialing needs an address: the gossip layer registers a lookup service that records addresses seen in Join and ForwardJoin messages, kept five minutes (net.rs:186-194; src/net/address_lookup.rs, `RetentionOpts::default`). I did not test `join_peers` with an id that has no known address.

2. **Events and NeighborDown.** `Event` has four variants: `NeighborUp`, `NeighborDown`, `Received`, and `Lagged` (api.rs:336). The gossip layer emits `NeighborDown` in one function, `remove_active_by_index` (hyparview.rs:639-646). Three paths reach it:
   - **Connection closed.** The net layer sends `PeerDisconnected` (net.rs:584), and `handle_connection_closed` removes an active peer (hyparview.rs:346).
   - **Received Disconnect.** An active peer sends a Disconnect (hyparview.rs:330).
   - **Random eviction.** A Join is accepted with high priority while the active view is full, and a random active peer is dropped (hyparview.rs:380, 713-717). The dropped peer also receives a Disconnect.

   It does not fire when this node quits: `handle_quit` removes peers and sends Disconnect with no event (hyparview.rs:356-361). It does not fire on a failed dial to an already-active peer: net.rs:441 sends `PeerDisconnected` only for peers that are not active. The gossip layer has no heartbeat or keepalive; a grep of src finds none. A silent peer is therefore reported only when its connection closes. I did not read iroh's idle timeout.

   `Lagged` is produced when the topic broadcast channel, sized 256, overflows (net.rs:54, 824, 942). Events are then lost, possibly including `NeighborDown`. `GossipReceiver::neighbors()` is updated only from events it reads (api.rs, `impl Stream for GossipReceiver`), so it can drift after `Lagged`. Not measured.

3. **Original author.** The gossip layer does not expose it. `Message` has `content`, `scope`, and `delivered_from` (api.rs:363). `delivered_from` is the previous hop, and the doc says it is not the author (api.rs:363-372; plumtree.rs:93-95). The wire `Gossip` carries `id`, `content`, and `scope` only (plumtree.rs:153-160). `DeliveryScope::Swarm(Round)` gives hops from the original broadcaster (plumtree.rs:174-181). There are two exceptions where `delivered_from` is the origin. A round-0 Swarm message and a Neighbors message are direct from their origin (`is_direct`, plumtree.rs:185-188). Neighbors messages are never relayed, because `on_gossip` forwards only Swarm messages (plumtree.rs:509-530). For any relayed message, the author must be inside `content`, signed by the application.

4. **broadcast versus broadcast_neighbors.** `broadcast` uses Swarm scope. It pushes the full message to eager peers and queues an IHave for lazy peers after the dispatch timer (plumtree.rs:467-486, 703-716, 718-735). `broadcast_neighbors` uses Neighbors scope. Only the eager push runs, and `lazy_push` returns early for Neighbors (plumtree.rs:718-722). Lazy neighbors therefore do not receive a neighbors-scope message. Neighbors messages are not recorded or cached (plumtree.rs:509-511 records only Swarm). A broadcast does not echo to the local node, because its id is recorded locally (plumtree.rs:467-486).

   Size settings:

   | Setting | Value | Where |
   |---|---|---|
   | Default `max_message_size` | 4096 bytes | proto.rs:69; topic.rs:200 |
   | Minimum, asserted at construction | 512 bytes | proto.rs:72; state.rs:177 |
   | Setter | `Builder::max_message_size` | net.rs:154 |
   | Message id retention | 90 s | plumtree.rs:326 |
   | Message cache retention | 30 s | plumtree.rs:325 |

   The limit applies to the whole serialized frame, envelope included. The writer rejects a frame at or above the limit (net/util.rs:384-386). The reader rejects a frame above it (net/util.rs:365-367). `broadcast` performs no size check (api.rs:180-184, then net.rs:506). An oversized broadcast therefore fails in the send loop. That error ends the loop (net/util.rs:225, 234) and `connection_loop` returns it (net.rs:897-898), which closes the connection to that peer. This is from reading, not a run. The exact content limit depends on postcard's envelope size, which I did not measure. The doc says all nodes on a network should use one value (topic.rs:183-191).

5. **Duplicates.** The dedup key is the blake3 hash of the content, not the author (plumtree.rs:26-37). For Swarm messages, a second copy of identical bytes within 90 s emits no event and prunes the sender (`on_gossip`, plumtree.rs:490-530). Two different authors who send identical bytes therefore collide. After the window expires, identical bytes are delivered again (plumtree.rs:326, 681-688). A payload can be delivered twice: after the window, or when the same bytes are broadcast again.

   Neighbors messages are not recorded (plumtree.rs:509), so each identical Neighbors message emits an event. The duplicate check in `on_gossip` ignores scope. A Neighbors copy whose bytes were already seen as Swarm is therefore suppressed and prunes the sender. No plumtree unit test covers Neighbors scope; a grep of plumtree.rs after line 700 finds no match.

6. **Stability.** CHANGELOG entries after 0.95.0 up to 0.101.0 are six: 0.96.0 through 0.101.0 (CHANGELOG.md lines 5-44). Four are marked **breaking**: 0.97.0, 0.99.0, 0.100.0, and 0.101.0. The 0.95.0 entry is also marked breaking, so five if 0.95.0 counts. Two iroh version bumps are unmarked, in 0.96.0 and 0.98.0. The unmarked bumps matter because `Gossip::spawn` takes an iroh `Endpoint` (net.rs:184), so an iroh bump changes a public type. The CHANGELOG holds 23 version entries in total. I found no stated reason for staying below 1.0. A repo-wide search for semver, stability, 1.0, unstable, and API-change wording matched only dependency versions and the CI semver job (.github/workflows/ci.yaml:178-206), which compares against origin/main on each PR.

7. **irpc in the public API.** Yes, in three places, all reachable through the default `net` feature. `ApiError` is public and non-exhaustive, and its `Rpc` variant holds an `irpc::Error` (api.rs:42-45). Three public `From` impls convert irpc channel errors into `ApiError` (api.rs:50-66). The crate does not re-export irpc (src/lib.rs), so a caller that matches `Rpc { source }` must depend on irpc 0.17 directly. Not public: `Request` is `pub(crate)` (api.rs:28), and the sender's field is private (api.rs:172). `GossipApi::connect` takes a `noq::Endpoint` under the `rpc` feature (api.rs:97), which exposes noq the same way.

## Estafette fit

- **Crate or pattern:** the crate is a candidate topic transport, since it provides HyParView membership and Plumtree broadcast. The Neighbors scope is a one-hop pattern, usable only if the spec needs messages that must not relay.
- **Against 3.7, frame size:** 3.7 caps `public` at 4096 bytes. The default frame cap is also 4096 bytes, and it covers the whole frame, including the claim, handle, and mac. A full `public` field cannot fit at the default. 3.7 does not state the configured value. I did not read 3.14, where it may be set.
- **Against 3.8, Departure wait:** 3.8 says to send Departure, wait at most 1000 ms, then exit. `broadcast` returns once the command is queued, not once it is sent (api.rs:180-184), and no flush call is public. The wait is the only delivery guarantee.
- **Against 3.8, neighbor down:** 3.8 acts on "gossip reports a neighbor down." The library reports it only on connection close, a received Disconnect, or random eviction (Answer 2). A silent peer is found only when its connection closes.
- **Against 3.7 and 3.8, duplicate Presence:** 3.7 does not give the unit or resolution of `ts`. Identical bytes within 90 s are suppressed (Answer 5). If `ts` is coarse, a repeated Presence after an attached change can be dropped.
- **Consistent with 3.7, origin:** 3.7 binds `claim.node` by signature because gossip gives no origin (Answer 3).

## Not read

- examples/chat.rs, examples/setup.rs, tests/sim.rs, simulations/, src/proto/sim.rs.
- Most of src/net.rs; the RecvLoop body in src/net/util.rs.
- The IHave and Graft handling and optimize_tree in src/proto/plumtree.rs.
- The irpc 0.17.0 source; the bounded-channel await semantics are assumed.
- iroh 1.x internals: address lookup, the QUIC idle timeout.
- docs.rs and the crates.io registry.
- Spec sections other than 3.7 and 3.8, including 3.14.
- Live behavior: nothing was executed.
