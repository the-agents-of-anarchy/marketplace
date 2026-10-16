# iroh-gossip admission and frame size

Source: iroh-gossip 0.101.0 (`/tmp/ra-src/f2-gossip/Cargo.toml:3`). Spec: `spec/blueprint.md` sections 3.4, 3.7, 3.14.

## Q1 Admission

**Answer: yes.** A node that knows the 32-byte topic id and one bootstrap node id joins the swarm and receives every broadcast the swarm relays to it. The only checks are topic id equality and ALPN. There is no auth hook, and no check on the joiner's identity beyond the transport.

Trace:

1. **Join request.** `Command::Join(peers)` becomes `RequestJoin(peer)`, which sends `Message::Join(me_data)` to the contact (`src/proto/hyparview.rs:322-327`). `me_data` is the local `PeerData` set at construction (`src/proto/state.rs`, `State::with_rng`, `me_data` argument). iroh-gossip itself adds no card fields.
2. **Stream header carries the topic.** Each topic opens a stream whose first frame is `StreamHeader { topic_id }` (`src/net/util.rs:59-60`, `:283`). That id is the only topic routing key on the wire.
3. **Connection accept checks no node id.** `Gossip::accept` forwards every connection to `handle_connection` (`src/net.rs:129-135`). The doc says the embedder must check ALPN (`src/net.rs:243-245`). `handle_connection` keys peer state by `conn.remote_id()` and does no allow check (`src/net.rs:395-396`, `:525-537`).
4. **Topic gate is equality only.** `InEventMapped::TopicEvent` creates state only on `Command::Join` (`src/proto/state.rs:247-255`). An incoming message for a topic with no state is dropped, because the lookup is `states.get_mut(&topic)` (`src/proto/state.rs:262-264`). So a receiver must have joined that topic, and the topic id is the only key.
5. **Membership accepts any peer.** `on_join` calls `add_active(peer, ..., Priority::High, ...)` (`src/proto/hyparview.rs:380-383`). `add_active` rejects only `peer == self.me` (`:702-704`). A High-priority peer is always accepted and a random member is evicted if the view is full (`:712-717`). The contact replies with `Neighbor` (`:708`, `:739-740`).
6. **Broadcast path.** `on_neighbor_up` puts the peer in the eager set (`src/proto/plumtree.rs:664-665`). Eager peers receive each full payload (`src/proto/plumtree.rs`, `broadcast` doc, "Will be pushed in full to eager peers").
7. **No hook.** A search of `src/` for `authori`, `allowlist`, `whitelist`, `filter_peer`, `admission`, `accept_peer`, `hook` returned nothing.

Consequences for estafette:

- The per-payload MAC is the only check on what a member accepts. It is not a delivery gate. Gossip relays before the application checks (`src/proto/plumtree.rs:502-508`, comment: "emit to application and forward to peers"). The only check in the gossip layer is that the message id equals the blake3 hash of the content (`:490-500`).
- An outsider with the topic id receives every Presence frame in plaintext. The spec encrypts only per hop, through QUIC (`spec/blueprint.md:185`). The application does not encrypt payloads.
- The outsider cannot forge or verify MACs. The topic id and the mac key are two separate BLAKE3 `derive` outputs of one network secret (`spec/blueprint.md:474-478`). Knowing the topic id does not give the mac key, assuming BLAKE3 derive_key behaves as a PRF.
- The outsider also relays unverifiable payloads it injects. Members forward them before the MAC check.

## Q2 Frame size

**Measure.** `max_message_size` bounds the postcard body of the wire frame, not the payload alone. The 4-byte u32 length prefix is excluded from the check.

- Write: `len >= max_message_size` is an error (`src/net/util.rs:381-387`). So the body must be strictly less than the limit.
- Read: `size > max_message_size` is an error (`src/net/util.rs:362-368`).
- Default: `DEFAULT_MAX_MESSAGE_SIZE = 4096` (`src/proto.rs:69`). Minimum: 512 (`src/proto.rs:72`).

**Overhead the library budgets.** `postcard_header_size()` is 33 bytes: topic id 32 plus outer discriminant 1 (`src/proto/state.rs:49-57`). `topic.rs:244-245` sets the payload budget to `max - 33`, and plumtree stores it (`src/proto/plumtree.rs:382`, `:401`). Plumtree uses that field only for IHave chunking (`src/proto/plumtree.rs:448-453`).

**Overhead the budget misses.** Gossip frames add these fields beyond the 33 bytes: inner discriminant 1, `MessageId` 32 (`src/proto/plumtree.rs:27-28`, `:153-158`), content length varint 2 for 128 to 16383 bytes, and `DeliveryScope` 2 (`:173-178`, `Swarm(Round)` with a one-byte round). That is 37 bytes the budget does not cover. `broadcast` does not check size before sending (`src/api.rs:180-183`, `src/net.rs:506-512`). The only check is in `write_frame`. A payload at the budget limit therefore fails to write.

**Presence size, worst case (spec 3.7 and 3.4).**

| Field | Bytes |
|---|---|
| `v` | 1 |
| `claim`: v 1, card 32, node 32, ts varint 10, handle 1+32, sig 64 | 172 |
| `handle`: length 1, up to 32 | 33 |
| `public`: length varint 2, up to 4096 | 4098 |
| `attached` | 1 |
| `ts` varint | 10 |
| `mac` | 32 |
| **Presence payload** | **4347** |

**Wire body around the Presence payload (Swarm broadcast, round under 128).**

| Field | Bytes |
|---|---|
| topic id | 32 |
| topic::Message discriminant (Gossip) | 1 |
| plumtree::Message discriminant (Gossip) | 1 |
| MessageId | 32 |
| content length varint (4347) | 2 |
| content (Presence) | 4347 |
| DeliveryScope `Swarm(Round)`, one-byte round | 2 |
| **Body** | **4417** |

The body must be less than `max_message_size`, so the minimum setting is 4418. Round values change the scope width: 128 to 16383 hops adds one byte (minimum 4419), and the full u16 range adds two (minimum 4420).

**Default 4096 cannot carry the spec's own maximum Presence.** The largest content that fits 4096 is 4025 bytes (`66 + 2 + n + 2 <= 4095`). A Presence is 251 bytes plus the public length, so with a 32-byte handle the public mapping must stay at or below 3774 bytes.

**Minimum setting: `max_message_size` = 4418 for rounds under 128, 4420 to cover every round.** Set it to at least 4420.

**Consequence of an oversize write.** `write_frame` returns `WriteError::TooLarge` (`src/net/util.rs:384-386`). The send loop returns that error (`src/net/util.rs:223-227`, `:274-293`). I did not trace what tears down the connection after that.

**Spec gaps found while doing this.**

- Section 3.4 is titled "Cryptography". The Claim struct sits inside it, so the brief's "3.4 Claim" label is a section name mismatch.
- `blueprint.md` does not define the handle grammar. The 32-byte cap is the brief's assumption, not a spec value. Without a cap the Presence size has no upper bound and no minimum setting exists.
- The `v` field has no stated integer type. A varint of 1 is one byte for any integer type, so the arithmetic is unaffected.

## Not read

- No code was executed, and no test was written or run. Every byte count is derived by hand from postcard's encoding rules. Confirm with a serialized-size test before relying on the 4418 figure.
- The body of the plumtree forward step was not read. The claim that relays forward before the application check rests on the comment at `src/proto/plumtree.rs:507-508`.
- The connection teardown after a write error was not traced.
- The hyparview `free_random_slot_in_active_view` path was not read.
- `Cargo.lock` and the postcard version were not checked.
- The sim, the tests, and `src/bin/sim.rs` were not read.
- Spec sections 3.5, 3.6, 3.8 and the rest of the spec were not read. The Probe and Introduce validation rules were out of scope.
