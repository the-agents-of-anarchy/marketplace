# Presence over gossip, as n0 does it

2026-10-15. Spec: D18, D19, D20, 3.7, 3.8 read.
Sources read (shallow clones, depth 1):
- iroh-gossip 6cbbafa865c1b60c813dd8f12f78a54a45c1ecb1 (2026-10-15): `examples/chat.rs` whole; `src/api.rs` 180-360; `src/proto/hyparview.rs` 19-25, 105-118, 222-232, 905-920; `src/proto/plumtree.rs` 26-38; grep of `src/net.rs`, `src/proto.rs`.
- iroh-smol-kv 4eb7050aa7d653061824d58e8f338c9cfe6169a9 (2026-06-15): `src/lib.rs` 1-140, 360-396, 484-540, 596-668, 720-900; `examples/test.rs` 15-60; `Cargo.toml`.
- iroh-workshop-39c3 9775e6fd0d346b6d30635c01c05902d9eae7d2d9 (2025-12-28): `gossip1/src/main.rs` whole; `gossip4/src/main.rs` and `message.rs` whole; README Gossip 1-4.

## Answer table

| Question | chat.rs (iroh-gossip) | iroh-smol-kv | workshop gossip1-4 |
|---|---|---|---|
| Who is present | Not tracked. Names learned from `AboutMe` broadcast at join (`chat.rs:159-163, 195-198`). Unnamed peers appear only when they speak. | Not tracked. Present = scopes with non-expired entries in the replicated map (`lib.rs:609-632`). | Prints `NeighborUp` (`gossip1:75`, `gossip4:132`). No table. |
| Late joiner | Gets nothing. `AboutMe` sent once; a joiner after it sees raw key until that peer speaks (`chat.rs:200-202`). | Pull-less push anti-entropy: on every `NeighborUp`, republish whole state to neighbors over 10 s (`lib.rs:797-800`). | Nothing. gossip1 server broadcasts "welcome" once after first subscriber (`gossip1:46-49`). |
| Departure / crash | Neither detected. `NeighborUp`/`NeighborDown` ignored (`chat.rs:192`, only `Event::Received` matched). | No departure message. Entry expires after horizon (24 h default, 30 s DEBUG) (`lib.rs:602-632, 875-899`). `NeighborDown` only traced (`lib.rs:802-805`). | gossip1 joiner exits on `NeighborDown` (`gossip1:79-82`). gossip4 prints it (`gossip4:135`). |
| Signed | Yes. Ed25519 by the endpoint secret key; envelope `{from, data, signature}` in postcard (`chat.rs:225-260`). | Yes. Per-entry Ed25519 over postcard `(key, timestamp, value)` by the writer's key, which doubles as scope (`lib.rs:372-395, 496-510`). | gossip4 only. Signature over `(nonce, contents)` by endpoint key (`message.rs:36-48`). gossip1 sends plain bytes. |
| Heartbeat | None. | None as liveness. Periodic anti-entropy republish every 300 s (30 s DEBUG) (`lib.rs:889, 876`). That is a de facto refresh that keeps entries inside the horizon. | None. |

## Per project

### chat.rs (n0-computer/iroh-gossip, 6cbbafa, iroh 1 / iroh-gossip 0.101.0)
- What it does for this scope: signed chat. Presence is a name announcement, nothing else. It is not a presence protocol.
- How, in code:
  - Join: `subscribe_and_join(topic, peer_ids)` with peers from a base32 ticket of `EndpointAddr`s (`chat.rs:84-88, 145-155`). Addresses go into a `MemoryLookup` (`chat.rs:111, 151-153`).
  - Announce: one `Message::AboutMe{name}` after join, only if `--name` is set (`chat.rs:158-163`).
  - Sign: key is the endpoint's own secret key (`chat.rs:161`, `sign_and_encode(endpoint.secret_key(), ..)`). Key is random per start unless `--secret-key` is passed (`chat.rs:92-95`). Identity = transport key. No card/node split.
  - Receive: `names: HashMap<PublicKey,String>` in the loop. Only `Event::Received` is handled (`chat.rs:190-207`). `NeighborUp`, `NeighborDown`, `Lagged` fall through silently.
  - Error path: `verify_and_decode(..)?` inside the loop (`chat.rs:193`). One bad signature or undecodable payload returns Err and ends the subscribe task. Nothing restarts it.
  - Sender identity is `from` inside the payload, not `delivered_from`. The envelope signature binds `from` to `data` (`chat.rs:236-240`).
- Crates: iroh 1 (`default-features=false`, dev-dep with features), postcard 1, serde 1, serde-byte-array 0.1.2, data-encoding, clap, n0-future, n0-error (`Cargo.toml:36-111`, dev section).
- Maturity: iroh-gossip is under active development (last commit same day as survey). Example has no test. Core library tests exist for neighbor events (`src/net.rs:2828, 2838, 3098-3114`), not for chat.
- What estafette could take: pattern: sign-the-bytes envelope `{from, data, signature}` (`chat.rs:225-260`). Nothing for presence.
- Against the spec: 
  - D18/D19/D20: none. The example has no introduction, departure, or probe.
  - 3.7 "drop any payload whose mac does not verify": the example does the opposite (`?` aborts the loop, `chat.rs:193`). Drop-and-continue must be written explicitly.
  - 3.7 binding of `claim.node` to the card through the claim signature: the example binds the signing key to the gossip identity directly, so it is not comparable.

### iroh-smol-kv (n0-computer/iroh-smol-kv, 4eb7050, 0.4.0, iroh 1 / iroh-gossip 0.101.0)
- What it does for this scope: replicated map `(scope=PublicKey, key, SignedValue)` over one gossip topic. Closest n0 analogue of "state that new joiners must catch up on". Presence could be a key per node with expiry.
- How, in code:
  - Write: `WriteScope::put` stamps nanosecond timestamp, signs postcard `SigningData{key,timestamp,value}` with the writer key (`lib.rs:372-395`). `GossipMessage::SignedValue(scope,key,value)` is the only wire message (`lib.rs:80-83`).
  - Receive: verify signature against `scope` (`lib.rs:496-510`). Last-writer-wins on timestamp: reject if `existing.timestamp >= new` (`lib.rs:524-530`). Skip values below the expiry horizon (`lib.rs:809-814`). Malformed postcard is dropped and the loop continues (`lib.rs:803-808`, trace and `continue`).
  - Late joiner: on `NeighborUp`, restart anti-entropy with `fast_anti_entropy_interval` (10 s): publish every known entry in random order, spaced evenly over the interval, via `broadcast_neighbors` (`lib.rs:636-667, 797-800`). Push only. No request, no digest, no diff. Cost per `NeighborUp` is the whole state to all neighbors, not just the new one.
  - Steady state: the same loop reruns every `anti_entropy_interval` (300 s default) (`lib.rs:835-842, 889`). This republishes other nodes' entries too, so a departed node's entry keeps circulating until its horizon.
  - Departure/crash: no tombstone, no departure message. Entries vanish when `timestamp < now - horizon` (`lib.rs:609-632`). A live writer must re-`put` within the horizon to stay visible. The library does not do that itself.
  - Expiry sweep period: hard-coded 30 s (`lib.rs:731-734`). `ExpiryConfig::check_interval` is declared (`lib.rs:871`) and set (`lib.rs:880, 895`) but never read (grep shows no other use). Documented knob does nothing.
  - Clock: timestamps from the writer's wall clock (`current_timestamp`, `lib.rs:926`). Horizon compares against the reader's clock (`lib.rs:602-606`). Clock skew shifts expiry. Not handled.
  - Key: the example uses the endpoint secret key as the write key (`examples/test.rs:22, 56`). Library takes any `SecretKey` (`lib.rs:416`).
- Crates: ed25519-dalek 3.0.0-rc.0 (`signature` feature), postcard 1.1.3, rpds 1.1.1, bytes 1.10.1, irpc 0.17.0, iroh 1, iroh-gossip 0.101.0 (`Cargo.toml:14-53`). Also serde_big_array, sync_wrapper, rand (seen in `lib.rs` imports; versions not read).
- Maturity: version 0.4.0, tags none, `git log` shallow (1 commit visible). Last commit 2026-06-15. No `#[test]` in `src/` or `examples/` (grep). Behavior above is read from source only, not run.
- What estafette could take: nothing to depend on for presence. Pattern: refresh-on-`NeighborUp` republish is the n0 answer to late join. It is state push, where D18 uses direct introduction (reply to the one new node).
- Against the spec:
  - D18 "no periodic traffic": smol-kv has periodic traffic (300 s default). It trades traffic growth for no per-peer handshake. D18 rests on the claim that heartbeats grow with member count. In smol-kv the republish grows with entries x neighbors per event, and the code does not measure it.
  - D19: smol-kv has no departure message. Gone-ness comes only from the horizon (24 h default). Evidence that n0's own state library does not model clean exit.
  - D20/3.8 "gossip reports neighbor down -> probe": smol-kv ignores `NeighborDown` (`lib.rs:802-805`). No contrary design.
  - 3.8 `last_seen`/`ts`: smol-kv's LWW uses `>=` on timestamp and drops ties (`lib.rs:524`). Spec Presence `ts: u64` has no stated tie rule; two Presence with equal `ts` from one node, if compared by `ts` alone, would drop the second. Unit of `ts` is not stated in 3.7.

### iroh-workshop-39c3 (n0-computer/iroh-workshop-39c3, 9775e6f, iroh 0.95.1 / iroh-gossip 0.95.0)
- What it does for this scope: teaching code. Gossip 1-4 progress from "bootstrap node broadcasts once" to signed, nonce-unique messages. Workshop pins an old alpha (`Cargo.toml` workspace deps: iroh 0.95.1, iroh-gossip 0.95.0; README "Note: the workshop is using an *alpha* version of iroh"). APIs differ from the 1.x line the others use.
- How, in code:
  - Presence: none beyond printing `NeighborUp` / `NeighborDown` (`gossip1/src/main.rs:75-82`, `gossip4/src/main.rs:132-136`). The gossip1 joiner treats `NeighborDown` as "left" and exits (`gossip1:79-82`).
  - Late joiner: gossip1 server calls `topic.joined().await` then broadcasts "welcome" once (`gossip1:46-49`). Later joiners get nothing. `joined()` consumes the first `NeighborUp` (`iroh-gossip/src/api.rs:294-298`).
  - Signing: gossip4 `SignedMessage{nonce, contents, author, signature}`; signature over postcard `(nonce, contents)` by the endpoint key (`message.rs:15-48`). Nonce is a process-global atomic counter (`message.rs:11`).
  - Why nonce: gossip deduplicates by content (README Gossip 2; confirmed in iroh-gossip `src/proto/plumtree.rs:26-37`, `MessageId` = blake3 of content). Two identical broadcasts collapse into one.
  - Forwarder vs author: gossip4 prints `msg.author` and `message.delivered_from` separately (`gossip4:148-151`). `delivered_from` is the forwarding hop. Same distinction as spec 3.7.
  - Error path: `decode(..)?` and `verify()?` inside the listener (`gossip4:145-146`). A bad payload ends the listener, and `race` then ends the node (`gossip4:70-76`).
- Crates: iroh 0.95.1, iroh-gossip 0.95.0, iroh-tickets 0.2.0, n0-future 0.1.3, postcard, serde, tokio (`Cargo.toml`, workspace deps).
- Maturity: 1 commit visible, last 2025-12-28. No tests (gossip dirs hold only `src/main.rs`, `message.rs`, `util.rs`).
- What estafette could take: nothing. Teaching value only: content-dedup trap.
- Against the spec:
  - 3.7: identical Presence bytes from one node are dropped by gossip. Spec `Presence` carries `ts`, so repeats differ only if `ts` changes. Two Presence sent within one `ts` unit with identical fields (for example attach then detach flip back to the same values) would be byte-identical and deduped. Unit of `ts` unstated; check.
  - D20 "gossip layer changes neighbors for its own reasons": supported. `NeighborDown` is emitted on any active-view removal (`iroh-gossip src/proto/hyparview.rs:918`). `Disconnect` carries `alive` = "closing the connection only because our limits are reached" (`hyparview.rs:225-232`). The workshop's "Neighbour left" reading (gossip1:79-82) is the false-departure inference D20 rejects.

## Cross-project observations
- None of the three runs a presence protocol. Presence is absent (chat), implicit via state expiry (smol-kv), or neighbor-event printing (workshop). D18-D20 have no n0 precedent to copy or contradict; they are original.
- Signing is by the transport key in all three (`chat.rs:161`, `smol-kv examples/test.rs:56`, `message.rs:36-48`). No card/node split. Spec's claim (card key signs claim binding ephemeral node) has no precedent here.
- Late-join handling in n0 code is "republish on `NeighborUp`" (smol-kv `lib.rs:797-800`), push to neighbors. Spec: introduce to the new neighbor only (D18, 3.8 row "neighbor up").
- Departure in n0 code is expiry or nothing. No example sends a farewell (D19). Closest wire-level analogue is the gossip layer's own `Disconnect{alive}` (`hyparview.rs:225-232`), which is below the application.
- Dedup by content hash (plumtree.rs:26-37) is documented in the workshop and relevant to any payload that can repeat.
- Error handling split: chat.rs and gossip4 abort on a bad payload (`?`); smol-kv drops and continues (`lib.rs:803-808`).
- `GossipReceiver::neighbors()` and `joined()` exist (`iroh-gossip src/api.rs:287-310`). A node can read its current neighbor set without tracking events.

## Not read
- Rest of `iroh-gossip/src/net.rs` (about 3100 lines) beyond grep hits. Real behavior of `NeighborUp` emission order on reconnect not verified by running.
- `iroh-smol-kv/examples/cli.rs`, `iroh-smol-kv-uniffi`, `uniffi-example`, util/filter code.
- workshop `echo1-3`, `gossip2`, `gossip3` source (README and gossip4 cover them), `util.rs` key storage.
- Nothing was executed. No behavior claimed here was observed at runtime.
- Git history depth: all clones were depth 1; "last commit" dates are tip dates only; release counts not checked.
