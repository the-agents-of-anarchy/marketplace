# SP4: habilis-network internals

Date: 2026-10-16.

Repos and commits read:

- `agent-habilis/habilis-network` main at `8722df5` (2026-10-15). Line numbers below are at this commit unless marked otherwise.
- `agent-habilis/iroh` main at `c45bea2` (2026-10-12). The engine pins rev `0e7cdb4`.
- `agent-habilis/iroh-gossip` main at `28676ce` (2026-10-12). The engine pins the same rev.
- `agent-habilis/agent-gossip` main at `2c5e132`, and its divergence commit `f81b052`.
- Issues read: habilis-network #3, #7, #8. Issue list read in full (#3 to #21).
- Releases: none (`gh release list` is empty). CHANGELOG has `0.5.0` (2026-07-31) and `0.6.0` (2026-08-30).
- Nothing was built or tested.

## What it is

`habilis-network` is the Rust engine of a gossip mesh for software agents. Members are identified by Ed25519 keys and talk over iroh QUIC. Chat and presence travel on a gossip overlay. Shared state is an automerge document per channel. Anti-entropy repairs gaps. The engine has four transports: iroh direct and relay, WebRTC, multihop, and a partly built gossip-as-transport. Around the engine sit a C ABI, a wasm build, TypeScript packages, a one-to-one byte stream crate, and a rollback netcode crate. The engine is unpublished and consumed by git pin.

## How it works

### Crate layering

| Crate | Role | Relation to engine |
|---|---|---|
| `habilis-network` | Gossip, membership, anti-entropy, transport selection | Engine |
| `-iroh-webrtc-transport` | iroh custom transport over a WebRTC data channel | Engine dependency, wired in `transport/webrtc.rs` |
| `-iroh-multihop-transport` | Source-routed relay through peers | Engine feature `multihop` |
| `-iroh-gossip-transport` | Gossip frames carried as QUIC packets | Engine holds its handle (`transport/admission.rs:287`, `:989`) |
| `-stream` | One producer, one consumer, bytes over one QUIC stream | Sibling consumer, does not join gossip |
| `-netplay` | GGPO-style rollback netcode for games | Sibling consumer through `ops::send_app` |
| `-ffi`, `-wasm` | C ABI and wasm-bindgen binding | Binding |

### Transport policy

The mesh id carries two lists: lookups (`mdns`, `dht`, `relay`) and transports (`udp`, `webrtc`, `multihop`, `gossip`, `relay`). Per `docs/architecture.md` section 9.1, the default transport set is `udp,webrtc,multihop,gossip`. The relay carries only bootstrap, JSEP signalling, and NAT frames by default. Payload uses a path only after iroh selects a non-relay path. The doc says an inbound payload connection is held unread until a direct path appears, then closed after `PROBE_DEADLINE`. I did not trace that gate in code. Treat it as a doc claim.

### WebRTC

- The signalling ALPN is `habilis-mesh/webrtc-signal/1` (`transport/webrtc.rs:42`).
- Each offer or answer rides one short-lived relay connection, and the connection closes after one envelope each way (`transport/webrtc.rs` module doc).
- The lower endpoint id offers (`docs/architecture.md` 9.2).
- One admission table holds one slot per peer for both roles. The ceiling counts attached sessions only (`transport/admission.rs` module doc).
- TURN is refused by policy (`docs/architecture.md` 9.2). I found no TURN code. The native backend gathers STUN candidates itself (`habilis-network-iroh-webrtc-transport/src/native/stun.rs`).
- The crate has two backends, `native` (str0m on tokio) and `web` (`RTCPeerConnection`), and neither is a default feature (crate README).

### Multihop

- Routes are source routes of at most 8 hops (`habilis-network-iroh-multihop-transport/src/addr.rs:30`).
- Native nodes advertise link cost 10. Browser nodes advertise 100 (`src/lib.rs:151`, `:163-165`). The cost is part of the signed link vector.
- A relay forwards opaque cells on a dedicated underlay endpoint (`src/underlay.rs` module doc). The application endpoint is separate, so QUIC stays end to end.
- The engine enables multihop only when the mesh policy names it and UDP or WebRTC is present (issue #7 cites `daemon/setup.rs:684`).

### Byte streams

- ALPN `habilis-network/stream/1` (`habilis-network-stream/src/lib.rs:24`).
- `StreamOpts` takes lookups and a transport list. The default transport list is `udp,webrtc`. `multihop` and `gossip` are refused (`src/node.rs:39-49`).
- `StreamHash` holds the producer's endpoint address, lookups, transport policy, a public id, and a private secret (`src/hash.rs:128-139`). The hash is a bearer ticket. Whoever holds it can take the one consumer slot (crate README).
- `Refused` has five variants: `Unknown`, `Taken`, `RelayRefused`, `Abandoned`, `AtCap` (`src/read.rs:18-33`).

### Netplay

- Only inputs cross the network. Each peer simulates ahead and rolls back on contradiction (`habilis-network-netplay/src/lib.rs` module doc).
- Input frames must carry `loggable: false`. A `true` would put every input into the message log and anti-entropy. The comment calls this a correctness requirement (`mesh/driver.rs:116-125`).
- Lobby messages go to each roster member individually. The code comment says broadcast bodies are not mesh-key sealed, so a passworded mesh drops them (`mesh/driver.rs:225-229`).
- The engine's ordinary message delivery is the transport. The netplay crate is transport-agnostic through its own `Transport` trait (`src/transport.rs:120-128`).

### Anti-entropy

Anti-entropy has two planes of state. Chat and presence live in a per-member message log. State and meta live in automerge documents and are not in the log.

**What is logged.** `is_loggable` (`gossip/recv.rs:1662-1682`) excludes these kinds from the message log: presence `Alive`, `PeerInfo`, digests, `LinkState`, `Ping`, `Pong`, `State`, and `Meta`. Joined and left presence are logged. App frames defer to the app's `classify`. Durable state is kept in its own un-pruned log.

**How long.** The log holds `MESSAGE_LOG_SIZE` = 1000 messages (`crates/habilis-network-util/src/tuning.rs:16`). On overflow, `push` removes one message, not the oldest (`daemon/message_log.rs:110-122`). The victim is the smallest eviction key of the fullest author (`eviction_index`, `message_log.rs:159-181`). I found no age-based eviction in `message_log.rs`. Retention is a count, not a time. The dedup set is twice the log size (`tuning.rs:24`).

**Digest cycle.** Every `ANTIENTROPY_INTERVAL` = 10 s, each member broadcasts a chat digest (`tuning.rs:57`). The digest advertises up to two windows of 70 ids each. The windows are timestamp ranges with a rolling cursor (`gossip/antientropy.rs` module doc; `tuning.rs:100`).

**Who answers.** A digest is answered by at most `ANTIENTROPY_ANSWERERS` = 3 members. Each member ranks itself by a hash of the digest id and its nickname, and answers if fewer than three members rank ahead of it (`answers_digest`, `antientropy.rs:353-365`; `answer_rank`, `:329`). The rank uses the answerer's own member view. Two members with different views may disagree on who answers. That follows from the code, but I did not test it.

**What is sent.** An answerer resends up to `ANTIENTROPY_MAX_RESEND` = 64 messages per digest (`tuning.rs:106`). The receiver's `have` set suppresses duplicates across overlapping windows (`antientropy.rs:255-296`). A broadcast resend goes back on gossip. A directed resend goes only to its addressee (`resendable_to`, `message_log.rs:383`).

**State and meta.** The state digest carries automerge heads (`HeadsBody`, `antientropy.rs:113-123`). `handle_state_digest` (`:887`) answers point-to-point to the asker when a unicast path exists, otherwise on gossip. The answer is the change set since the asker's heads (`missing_frames`, `:986`). The answer ends with the answerer's own heads, so the asker asks again while behind.

**Rate limits.**

| Constant | Value | Where |
|---|---|---|
| `ANTIENTROPY_SERVES_PER_WINDOW` (unicast, per asker per channel) | 8 | `tuning.rs:717` |
| `ANTIENTROPY_SERVE_COOLDOWN` | 5 s | `tuning.rs:692` |
| Gossip serves per window | 1 | `antientropy.rs:483-486` |
| `FAST_ROUND_MIN_INTERVAL` | 200 ms | `tuning.rs:722` |
| `FAST_ROUND_RETRY` | 400 ms | `tuning.rs:731` |
| `RESEND_OUTBOX_CAP` | 256 | `tuning.rs:708` |

**Returning member.** A returning member's own digest shows a gap, and holders resend what they still retain. A chat backlog is therefore bounded by the 1000-message log of each answerer, minus evictions. A state backlog is bounded by the document, served in rounds of at most 8 answers of 64 frames per asker per 5 s on the unicast plane. From the constants alone, a chat digest round can carry at most 3 times 64, or 192, resends. I did not measure that.

### Nicknames

- A nickname has 1 to 32 Unicode scalar values (`protocol/src/ident.rs:26`, `:29`).
- It forbids control characters, whitespace, bidi controls, and `< > # / \` (`ident.rs:31-46`).
- The type validates on deserialize, so an inbound author that fails the check is rejected at parse (`protocol/src/nickname.rs` doc).
- Generated names are `word-word` pairs from a curated list (`Nickname::random`, `nickname.rs:65-71`).
- Identity is the Ed25519 key. The key is ephemeral, minted per process (`protocol/src/identity.rs:14-16`).
- The receive path dedups on a key-bound hash. A nickname is not pinned or claimed (`gossip/recv.rs:540-553`).
- The roster is a set of nicknames (`lifecycle/membership.rs:72`, `:75`; `daemon/state.rs:224`, `:333`). Two keys with one nickname share one roster entry. I found no collision handling.

### FFI and TypeScript packages

These are descriptions from manifests and READMEs. I did not read their code.

- `habilis-network-ffi` is a C ABI over the engine. A C program links one static library, and the event loop runs in the caller's process with no daemon (crate README).
- `habilis-network-wasm` is a wasm-bindgen `MeshPeer` class for browsers.
- `packages/habilis-network-api` holds the TypeScript types both backends implement.
- `packages/habilis-network-ffi` loads the C ABI with `dlopen` under Bun, Deno, and Node.
- `packages/habilis-network-wasm` is the browser backend behind the API types.
- `packages/habilis-network-stream-web` is a browser tab acting as one end of a stream.
- All four packages are `"private": true`.

## Why, by their own account

The fork has three stated reasons. Each is quoted from the repo.

- Binary size. `FORKED.md` (Why): "A cost measurement in the original host repo (`docs/ffi-cost.md`) measured the engine at **39.4 MiB of a 40.7 MiB release binary." It adds: "Cargo features cannot be selected per-consumer across a dependency edge, so making that closure optional required crate boundaries."
- Outgrowing its host. Root commit `86bd79d` (2026-07-31): "The engine was vendored inside mallorca, a graphics app, and had outgrown it: it carries its own toolchain pin, 22 test suites, and upstream-fork obligations that have nothing to do with an Odin renderer."
- Owning its pins. Root commit `86bd79d`: the iroh and iroh-gossip forks "were re-homed from agent-habilis to fofoca-network, so this workspace owns its entire pin surface."

The reason for the split from agent-gossip is in `VENDORED.md`. Mallorca vendored "a subset of the `agent-habilis/agent-gossip` engine as a self-contained Cargo workspace, so mallorca can build a C static library (`fofoca-ffi`)." Its base commit is `f81b052`.

The reversal of the crate extraction for the multihop transport is argued in `FORKED.md` change 20. The reason given is that "a separate repo bought nothing and cost a rev pin to bump on every change."

The pin rule is in `FORKED.md` ("Fork pins"): a fork belongs on a dependency edge when no crate outside our control names it from crates.io. Otherwise it must be a `[patch]`, and patches are not inherited by consumers.

## How it evolved

Dates are commit dates. SHAs are habilis-network commits unless marked.

| Date | Event | Commit or source |
|---|---|---|
| 2026-07-20 | Upstream iroh release `e5c710a`. Fork later sits on upstream `0438766` (2026-07-31). | iroh first-parent history |
| 2026-07-30 | agent-gossip divergence commit `f81b052`, "split chat into msg to one peer and broadcast to all." Same tree as agent-gossip main `6226382`, different parent. | agent-gossip |
| 2026-07-31 | Engine extracted from mallorca into its own repo, as `fofoca`. | `86bd79d` |
| 2026-08-04 | WebRTC transport crate added. Multihop crate taken back in-repo. | `8d2d98e`, `07a7c9b` |
| 2026-08-04 | Blob transfer crate replaced by a verified byte store. | `a1d0e39` |
| 2026-08-04 | Engine builds for the browser. Changes from agent-share's vendored fork merged back. | `dc8ba0e` (FORKED change 22) |
| 2026-08-05 | agent-gossip stops vendoring and consumes the fofoca engine. | agent-gossip `98f517c` |
| 2026-08-05 | Blob-offload side channel restored behind a default-off feature. | `b1dc62f` (FORKED change 25) |
| 2026-08-05 | Each fork pinned on its own dependency edge. Consumers stop carrying patch tables. | `3638d01`, `ce1acf5` |
| 2026-08-10 | Rollback netcode and light-cycles game added. | `d6d625f` |
| 2026-08-30 | Blob crate removed for the chunk store. | `4b6f00b` |
| 2026-09-23 | iroh fork gains patches on custom-transport path selection. iroh-gossip fork gains connection-leak and neighbor fixes. | iroh `aef12f2`, iroh-gossip `640ec29` |
| 2026-09-27 | Direct-path byte streams added. The commit message says the `fofoca-pipe` surface is gone. | `4628d36` (PR #4) |
| 2026-10-02 | Rename from fofoca to habilis-network. Forks move back to agent-habilis. | `9b7b65f`, `61daa92`, iroh `c814688` |
| 2026-10-12 | iroh-gossip fork gains LeavePeers and NeighborPeers. iroh pin moves to `0e7cdb4`. | iroh-gossip `28676ce` |
| 2026-10-13 | Gossip-as-transport and connection ceiling land. agent-gossip moves its engine references to habilis-network. | `1801b04` (PR #2), agent-gossip `23c3c0c` (PR #38) |

Patterns in the history:

- The multihop crate left the repo and came back (FORKED changes 13 and 20).
- The blob crate was deleted, then its transport half was restored under a feature (FORKED changes 18 and 25).
- The iroh forks moved to one organization and back (FORKED change 14).
- `public-surface.txt` was deleted because nothing checked it (FORKED change 15).

### iroh fork patches

The fork's main is upstream `0438766` plus Caio Gondim's commits. The commits, and what each changes:

- `aef12f2` (2026-09-23): three changes. It adopts mapped-address eviction from upstream iroh#4294. It drains relay tasks with `join_next` instead of `join_all`, so a cancelled task cannot panic shutdown. It adds tests. The code is in the pinned rev at `iroh/src/socket/remote_map.rs:237-241` and `iroh/src/socket/transports/relay/actor.rs:1380-1389`. The commit's source SHA `dcbdc15` is not on main. The same change was re-applied under a new SHA.
- `66003af` (2026-09-24): opens a custom-transport path after the relay is selected (fofoca-network/iroh#2 in the pin comment).
- `715eb56`, `c2e81ee`, `2b4bdd4`: open a late custom path on a selected custom connection, and when the selected IP path is lost.
- `51e891c` (2026-10-07): queues a retried path open once. The pin comment says the queue doubled at each 333 ms retry and "took gigabytes in a mesh of 24."
- `42216cd`: documents the cost of a custom path after the pair has left IP.
- `8a24827`: adds a `selector-test-utils` feature for testing a path selector outside iroh.
- `9fae989`: the `connecting` event names the relay and dialer addresses.
- `4ee8ec2`: adds `Endpoint::add_endpoint_addr`, which gives a remote an address without a dial.
- `0e7cdb4` (2026-10-09): a relay learned after a connection exists becomes a path of that connection.

The path-selection commits I checked all touch `iroh/src/socket/remote_map/remote_state.rs`. The netwatch and portmapper repoint is in `iroh/Cargo.toml:57` and `:101` at the pinned rev. It points at net-tools rev `e029602`, branch `fix/rtm-miss-storm-0.19.1`, which carries the RTM_MISS fix. That fix is not in the iroh repo.

### iroh-gossip fork patches

Fork base is upstream `f128b98` (2026-07-30). The fork's own commits:

- `640ec29` (2026-09-23): closes superseded connections instead of leaking them. It replaces a `join!` with `select!` in `connection_loop` (`src/net/util.rs:119`, `:231` at `640ec29`). It also fixes a send loop that never broke on a closed channel. The source commit `f7ddfcc` is on a fix branch. The Cargo pin cites upstream PR `n0-computer/iroh-gossip#147`. I could not find `#147` in the local history, so I did not verify it upstream.
- `e66061b`, `5d57f94`: move the iroh pin.
- `28676ce` (2026-10-12): adds `LeavePeers`, `NeighborPeers`, and connection fixes. The message lists a dial-crossing rule, a neighbor ping-pong guard, a join-walk fix, and a `Join` storm fix. It also repurposes a wire field. `Disconnect::left` reuses the obsolete `_respond` slot (`src/proto/hyparview.rs:508`). Postcard writes by position, so the bytes stay the same. The iroh-gossip FORKED.md documents this in its only section.

## Where it strains

Each item is checked against code or a named issue. Items marked "doc" are doc-versus-code mismatches.

- **Nickname doc contradicts code (doc).** `protocol/src/identity.rs:11` and `:31` say a nickname is bound to its key "trust-on-first-use by receivers." `gossip/recv.rs:546-553` says a nickname "is deliberately **not** pinned/claimed." The code wins at runtime. The doc describes a behavior that does not exist.
- **Roster collapses same-nickname members.** The roster is a nickname-keyed set (`daemon/state.rs:333`). Two keys under one nickname count once, so the reported peer count undercounts.
- **Missing doc (doc).** `identity.rs` cites `docs/history-integrity.md` twice. The file is absent at `8722df5`. `docs/` holds only `architecture.md` and `perf/`.
- **FORKED.md lists crates that do not exist (doc, issue #8).** The crate layout names `habilis-network-reassembly`, `-directory`, and `-blobs`. `crates/` holds none of them. It omits `-chunks`, `-stream`, `-netplay`, `-wasm`, and `-iroh-gossip-transport`. Issue #8 also names a Cargo.toml comment and a CHANGELOG line that do not match the tree.
- **Directory mesh always carries multihop policy (issue #7).** `directory_config` sets `transport: TransportPolicy::default()` (`crates/habilis-network-protocol/src/directory.rs:79`). The default turns multihop on (`protocol/src/mesh/transport.rs:116-122`). A directory carries only small advertisements, so each member opens an underlay it does not use.
- **Native reader cannot attach to a tab stream with mdns or dht in its hash (issue #3, open).** The reader fails with `RelayRefused`. The stream's own README says a hash is a bearer ticket, so the defect is in path choice, not in the hash.
- **Gossip-as-transport is partly built.** Its README says "Status: Phase 6 of PR #2, built in steps. Step 2 is the frame codec." The engine nonetheless holds its handle (`transport/admission.rs:287`, `:989`).
- **Identity is ephemeral by design (self-flagged).** A restart mints a new key, so peers that pinned the old key see a new identity (`identity.rs:14-16`). The doc calls on-disk persistence "a documented follow-up."
- **Anti-entropy has no time bound (observation).** Retention is a count of 1000 per member. A long absence can outlast the log of every holder, and the gap is then lost.
- **Eviction favors quiet authors (self-described).** `eviction_index` drops the fullest author's oldest-key message first (`message_log.rs:159-181`). The code calls this deliberate, so that the retained set is a pure function of the message set.
- **Derived backfill ceiling (constants, not measured).** At most about 192 chat resends per 10 s digest round, from 3 answerers times 64. State rounds are bounded at 8 answers of 64 frames per asker per 5 s.
- **Lobby fan-out cost (self-described).** Lobby messages go to each roster member individually, because broadcast bodies are not sealed (`netplay/src/mesh/driver.rs:225-229`). Each lobby message costs one send per peer.
- **Fork costs stated in pin comments.** Each custom address keeps one more path id and its keep-alive while connections live. Each idle path sends one PING per 5 s, read from code. A crossing can hold an extra connection for up to 30 s (root `Cargo.toml` pin comments; FORKED.md "Fork pins").
- **Wire field repurposed (iroh-gossip).** `Disconnect::left` reuses `_respond`. Bytes are unchanged, so old peers ignore the field. A later upstream change to that field will conflict (iroh-gossip FORKED.md).
- **Pins point at objects not in the clone.** agent-gossip main pins habilis rev `795c4f8` (`Cargo.toml:47`). That commit is not in any ref of the habilis clone. Habilis main is at `8722df5`.
- **The divergence SHA is orphaned.** FORKED.md and VENDORED.md cite `f81b052`. It is not reachable from agent-gossip main. Its tree equals main commit `6226382`, but its parent is `0203e35`, not `7a89c54`. So agent-gossip history was rewritten after the fork point.
- **Cited upstream commit missing.** FORKED.md change 24 cites upstream `0b9f438` for the directed-frame fix. It is not in the agent-gossip clone. The same subject appears on agent-gossip main as `0216a54` (2026-08-02). I did not compare trees.
- **Issue count moved.** The earlier survey counted 9 open issues. The issue list read now shows 7 open (#3, #7, #8, #9, #19, #20, #21) and 7 closed.

## Observations for the owner

- The engine is one repo with four live transports, and each has a different admission path. WebRTC is gated by one slot table, multihop by route cost, streams by refusal enum, and gossip by probe.
- Retention and backfill both use one knob, the 1000-message log. Chat history is therefore bounded by count, while state history is bounded by the document.
- Identity is a per-process key, and the nickname is not bound to it at runtime. Peers cannot tell a restart from a new member by name.
- The fork's history is harder to follow than its manifests suggest. The divergence commit, the iroh mapped-address fix, and the directed-frame fix each live under a different SHA than the one cited.
- The iroh fork has many path-selection commits in one file. Its own pin comments document the cost of each in prose, not in tests I read.
- Docs and code disagree in three places: nickname binding, crate layout, and the directory transport default. The FORKED.md file has been the source of most of the drift.

## Not read

- `gossip/antientropy.rs`: the function bodies of `ask`, `ask_back`, `FastRounds`, and `missing_frames`. I read signatures, constants, and the module doc. The test names were read, not the tests.
- `transport/webrtc.rs` (4161 lines), `transport/admission.rs`, `transport/probe.rs`, `transport/path.rs`, `transport/underlay_webrtc.rs`. I read module docs only.
- The multihop `topology.rs` and `underlay.rs` bodies. The route cap and cost constants were checked, not the Dijkstra run or the forwarder.
- Stream `produce.rs` and `read.rs` bodies, and netplay `protocol.rs` and `session.rs` bodies.
- iroh `remote_state.rs` and the path selector code. Only commit subjects and file names were read.
- iroh-gossip connection code. Only commit subjects, the pin comments, and the FORKED.md file were read.
- Upstream PR numbers cited in the fork pins (`iroh-gossip#147`, `net-tools#203`). Not checked upstream.
- Branches `fix-multihop-transport` (`41dd822`) and `fix-loopback-room-split`, which issue #7 and #8 cite.
- The FFI and TypeScript package sources and tests.
- Nickname collision analysis beyond the code paths named above. No probability estimate was made.
- No tests were run. The 40 loopback test files are unread except for the headers the earlier survey read.
