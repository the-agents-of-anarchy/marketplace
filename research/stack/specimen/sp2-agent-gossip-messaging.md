# agent-gossip: messaging and identity

Date: 2026-10-16.

Repos and commits read:
- `AG`: github.com/agent-habilis/agent-gossip, `origin/main` at `2c5e132` (531 commits). The newest commit on any ref, `09c95dc`, is on `origin/fix-completed-task-not-found` and was not read.
- `HN`: github.com/agent-habilis/habilis-network, `origin/main` at `8722df5` (105 commits). AG's commit `5faf662` pins this SHA.
- Paths are relative to `crates/`. Line numbers refer to those commits.

## What it is

agent-gossip is a command-line tool and library that lets coding agents form a peer mesh and exchange messages. Its messaging has two planes. A broadcast goes to every member over gossip. A directed message (`msg`) goes to one member over a unicast connection, sealed to that member's X25519 key. The engine, HN, owns keys, routing, dedup, and the message log. AG owns the chat and task semantics, the card that publishes each member's keys, and the receipts. Most identity claims are carried by a nickname, and a nickname is a label that nothing enforces as unique.

## How it works

### Keys and where they live

| Key | Made by | Lifetime | Where it lives |
|---|---|---|---|
| Ed25519 identity (signs every authored frame) | `Identity::generate()`, called in daemon setup (`HN:crates/habilis-network/src/daemon/setup.rs:692`) | one daemon process | memory only, in an `Arc` on the daemon |
| X25519 seal key | derived from the Ed25519 seed with label `habilis-mesh/x25519-enc/v1` (`HN:crates/habilis-network-protocol/src/identity.rs:70-92`) | same as the Ed25519 key | memory only. Its public half is published in the card's `mesh-seal` extension (`AG:crates/agent-gossip/src/a2a/card.rs:78-84`) |
| Per-frame ephemeral X25519 | fresh per sealed frame (`HN:crates/habilis-network-protocol/src/seal.rs:62-67`) | one frame | in the envelope field `epk` |
| iroh transport `EndpointId` | `mint_secret()`, a fresh random key per endpoint build (`HN:crates/habilis-network/src/lookup/mod.rs:891-895`, used at lines 821 and 994) | one process | memory only, advertised in `PeerInfo` and in the card's endpoint hint (`AG:card.rs:152-158`) |

The session identity that the state file exposes has four fields: `mesh`, `name`, `nickname`, and `topic` (`HN:crates/habilis-network/src/daemon/state_file.rs:259-265`). I found no signing or sealing key in that reader. The writer was not read. A restart therefore mints new keys for all three.

### How names map to keys

- A nickname is a display label. The default is a random `word-word` pair from a 1024-word list (`HN:crates/habilis-network-protocol/src/mesh/name.rs:127-129`, `wordlist.rs:116-122`). That gives 1,048,576 possible names.
- The receiver does not pin a nickname to a key. The engine says so: the nickname is "a non-unique display label and is deliberately **not** pinned/claimed" (`HN:crates/habilis-network/src/gossip/recv.rs:547-551`).
- Four lookups use the nickname as the key:
  - Endpoint binding: `peer_endpoints` is keyed by nickname, and `bind_peer_endpoint` overwrites it (`HN:crates/habilis-network/src/daemon/state.rs:2053-2074`).
  - Seal key: `peer_seal_key` reads `/peers/<nick>/card` from the meta document (`AG:card.rs:122-145`).
  - Addressee test: `addressed_to_us` compares `to == us` on the nickname (`HN:recv.rs:1362-1365`).
  - Card ownership: the card-forgery gate in the meta document compares nicknames, not keys (`HN:crates/habilis-network-doc/src/lib.rs:10-16, 221-243`).
- The signing key is bound to an endpoint by `PeerInfo`. Anti-entropy answers go only to the endpoint that the key proved (`HN:state.rs:269-272`, `HN:transport/send.rs:161-177`).

### Directed messages (`msg`)

1. `send_msg` rejects a body over 64 MiB (`AG:send.rs:981-1002`, ceiling in `HN:crates/habilis-network-util/src/consts.rs:71`).
2. `seal_directed` looks up the addressee's seal key in the meta document. If the key is absent, it returns an error and never sends in plaintext (`AG:send.rs:854-876`).
3. The sealing is in `HN:crates/habilis-network-protocol/src/seal.rs:62-87`. A fresh ephemeral X25519 key does ECDH with the recipient's public key. The shared secret goes through `derive_secret` with label `habilis-mesh/seal/v1`, then ChaCha20-Poly1305 with that label as associated data. The envelope is JSON with base58 fields and version `x25519-chacha20poly1305/1`.
4. The frame is built and signed by `broadcast_directed_frame` (`AG:send.rs:581-634`). The Ed25519 signature covers the canonical bytes, which include the sealed body (`HN:crates/habilis-network-protocol/src/message/mod.rs:1019-1024`). The sender's identity therefore rests on the outer signature, not on the box.
5. A frame larger than 3840 bytes is split into shards (`AG:send.rs:636-720`).
6. `deliver` routes a directed message only to a unicast connection. Gossip never carries it (`HN:crates/habilis-network/src/transport/send.rs:1-6, 48-61, 150-159`). Routing returns one of three results: a unicast endpoint, a `Held` error when the only path is a lookup-only relay, or an `Undeliverable` error when no endpoint is known.
7. The receiver checks the nickname, then decrypts the body in place. A frame sealed to it that fails to open is dropped with a warning (`HN:crates/habilis-network/src/gossip/recv.rs:583-597, 1355-1358`). A relay forwards the opaque frame and does not read it (`HN:recv.rs:583-586`). The comment says a relay also retains it. I did not trace that retention.

The engine's generic send primitive does not seal anything. Its documentation says a directed App frame sent through that primitive "rides in plaintext" unless the application seals it (`HN:crates/habilis-network/src/gossip/broadcast.rs:38-41`). AG's `msg` path seals in AG code before calling the engine.

### Broadcasts

1. On a public gossip, the body is plaintext and signed. Each frame carries a per-author sequence number, a `prev` hash, and DAG parents (`AG:send.rs:369-388`, `build_msg` at lines 144-173).
2. On a passworded gossip, the body is encrypted with the mesh-derived channel key before it is chained or logged (`AG:send.rs:357-365`). Receivers refuse a plaintext broadcast body on such a mesh (`HN:crates/habilis-network/src/gossip/broadcast.rs:43-46`).
3. The frame goes out on the gossip plane. A re-send from anti-entropy gets a fresh nonce, so the gossip layer does not drop it as a repeat of a payload it saw in the last 90 seconds (`HN:crates/habilis-network/src/gossip/antientropy.rs:302-307`).

### Receipts

- The receiver sends a `delivered` receipt when a directed message is fresh for it, meaning it surfaced, is addressed to it, is loggable, and is not a replay (`AG:node.rs:49-57, 749`).
- The receipt is sealed and sent unicast (`AG:receipt.rs:58-84`). It is fire-and-forget: it is never retried and never acknowledged (`AG:receipt.rs:24-26`).
- A `read` receipt is sent when a foreground poll serves the frame (`AG:receipt.rs:40-56`).
- The sender prints an echo only after the unicast send succeeds (`AG:CHANGELOG.md`, 0.12.4 entry, line 7).

### Delivery and absent recipients

"Sent" means the unicast write or its handoff succeeded. It does not mean the recipient's application read the message. `deliver` returns at once: a warm connection gives its verdict immediately, and a cold peer is dialed by a task whose verdict arrives later (`HN:transport/send.rs:24, 30-40`). The `delivered` receipt is the only proof that the recipient's daemon received the message.

Product code has no retry for a directed message. The retries that do exist are these:
- The card publish retries with doubling waits (`AG:node.rs:124-127, 340-350`).
- A lost shard is re-requested from the sender's cache (`AG:send.rs:1524-1531`).
- Frames buffered while the node is not meshed are re-sent on each meshed edge (`HN:recv.rs:370-454`).

The test harness has `a2a_call_retrying`, which re-sends a call on a 10 s per-attempt timeout (`AG:crates/agent-gossip-test-fixtures/src/lib.rs:519, 1071, 1125`, commit `69e6a4d`). It is not product behaviour.

What happens to a directed message for an absent agent depends on where the failure occurs:

| Case | Result to the sender | Stored? | Later delivery |
|---|---|---|---|
| Sender meshed, no endpoint known | error: `undeliverable: no known endpoint` (`HN:transport/send.rs:74-89`) | no (`?` returns before `retain_leg`, `AG:send.rs:1307`) | none |
| Recipient's card not replicated | error: `cannot seal to '<nick>'` (`AG:send.rs:854-876`) | no | none |
| Endpoint known, dial fails | error reported to the caller (`AG:CHANGELOG.md`, 0.12.0, line 65) | no. The log keeps a frame only after its send succeeds (`AG:send.rs:1356-1371`) | none automatic |
| Sender not meshed | accepted and echoed | yes, in the log and in the pending buffer | sent on the next meshed edge. A failed frame is re-queued. The buffer holds 1024 frames (`HN:tuning.rs:38`). I saw no age limit in the flush path |
| Sent successfully, recipient offline later | accepted | yes, in the log of 1000 entries (`HN:tuning.rs:16`) | a later digest reply re-sends it by unicast, if the recipient's endpoint is known then. Otherwise the resend is dropped with a debug log (`HN:gossip/antientropy.rs:296-321`) |

A frame whose shard group has more than 16 shards is not logged (`AG:send.rs:688-690`). Such a message is not backfilled. Its lost shards are repaired only from the sender's cache.

### Ordering

- Directed frames carry no sequence number and do not touch the author's chain (`AG:send.rs:959-974`). The receiver's surfaced ring records them in the order it saw them (`AG:tuning.rs:60-66`). The code does not guarantee order across resends or across senders. I did not trace the unicast stream handling, so the order within one stream is not verified.
- Broadcast frames carry a per-author `seq`, a `prev` hash, and DAG parents (`AG:send.rs:369-388`). A gap in that chain reads to peers as a fork (`AG:send.rs:967-974`).

### Size limits

| Limit | Value | Source |
|---|---|---|
| One wire frame | 3840 bytes | `HN:crates/habilis-network-util/src/consts.rs:45` |
| Logical body input, msg and broadcast | 64 MiB | `consts.rs:71`, `AG:send.rs:345` |
| Sealed body ceiling, RPC path | 96 MiB | `consts.rs:78` |
| Shards per group | 65,536 | `consts.rs:54` |
| Shards per logged group | 16 | `consts.rs:61`, `AG:send.rs:688` |
| Message log entries | 1000 | `HN:tuning.rs:16` |
| Pending buffer while not meshed | 1024 frames | `HN:tuning.rs:38` |
| Live tasks held per peer | 64 | `AG:crates/agent-gossip/src/a2a/tuning.rs:93` |
| Task records across all peers | 1024 | `AG:tuning.rs:100` |

Sealing inflates a body by about 1.4 times, according to the comment at `AG:send.rs:464-467`. The RPC comment says 1.37 times (`AG:send.rs:1771`). By my arithmetic, a 3840-byte frame therefore carries roughly 2.7 kilobytes of plaintext, before shard headers.

## Why, by their own account

- On identity, the engine states: "The key is currently **in-process / ephemeral** — minted once per `create`/`join` and held in memory for the process lifetime. A process restart therefore mints a *new* key" (`HN:identity.rs:13-16`). It calls durable identity "a documented follow-up" (`identity.rs:16-18`).
- On nicknames, the engine states: "the `author` nickname is a non-unique display label and is deliberately **not** pinned/claimed, so a nickname is never 'burned' by a restart on a long-lived mesh" (`HN:recv.rs:547-551`). AG's card code says the same: "identity is per-session; nicknames are never burned" (`AG:node.rs:326-327`).
- On directed messages, commit `6226382` says: "A msg travels unicast and is sealed to its recipient, so only the sender and the recipient ever surface it."
- On backfill, commit `0216a54` says that anti-entropy "re-broadcast every log entry a peer was missing, and both parties retain a directed frame, so a msg between two peers reached the whole gossip during backfill." Its fix makes "backfill … exactly as reliable as the original send."
- On requests before a link exists, commit `69e6a4d` says: "A request sent while the overlay has no live link is lost … It failed 7 of 40 local runs." The fix is a test-side retry.
- On the card, the 0.12.0 changelog says that without frame-sized merges, "every directed message and task to that member failed with 'cards still propagating'" (`AG:CHANGELOG.md:77`).
- On restarts, the 0.11.1 changelog says: "A daemon restart forgets what it surfaced, so one more replay can show after a restart" (`AG:CHANGELOG.md:118`).
- The README says that the frame "travels point-to-point and is sealed to the recipient, so the peers relaying it cannot read it" (`AG:README.md:157-160`).
- Open issue #28 proposes keeping a session's signing key "for the life of the agent session" (smaller design, not built). Open issue #29 says a restart "gets a new random nickname, so peers lose track of it and its open tasks."

## How it evolved

Dates are commit or release dates. Each entry names the commit or release it rests on.

- **2026-07-30, chat split.** Chat had one shape, a broadcast to everyone. The split added a unicast, sealed `msg` (`AG:6226382`). Its commit message says the old reply field "is gone."
- **2026-08-02, directed frames stop leaking.** Backfill re-broadcast directed frames to the whole gossip. The fix sends a directed frame only to its addressee (`AG:0216a54`). The engine made the same fix on 2026-08-05 (`HN:71e99dd`).
- **2026-08-05, engine consumed.** AG stopped vendoring the engine and began to consume it as a dependency (`AG:98f517c`). The engine was then named fofoca, later habilis-network (`HN:9b7b65f`, 2026-10-02).
- **2026-08-28, relay policy.** The engine held a graft until a direct path was proven (`HN:277ec71`). It refused unicast on a relayed path when the relay was lookup-only (`HN:c629e44`).
- **2026-09-25, directed send off the caller's task.** The dial moved to its own task (`HN:4ec7f60`, AG 0.12.0 changelog lines 63-65).
- **2026-09-25, replay suppression (AG 0.11.1).** The daemon stopped surfacing a chat it already showed. The surfaced set is lost on restart.
- **2026-10-13, card in frame-sized merges (AG 0.12.0).** The seal key goes first. A failed merge is retried with longer waits. Issue #41 was closed the same day.
- **2026-10-15, delivery receipts (AG 0.12.4, `AG:30d8747`, PR #56).** `delivered` and `read` receipts appear. Older peers send none.
- **2026-10-15, engine newtypes (`HN:8722df5`).** Keys and ids became typed in a breaking refactor, per the `!` in the subject.

The identity module's file history runs back to 2026-07-31, under the name fofoca (`HN:86bd79d`). I did not check whether the ephemeral-key note was in that first version.

## Where it strains

- **Nicknames collide silently.** Open issue #28 describes the effects. Rosters are keyed by nickname, and a `Left` from one holder removes the name for both. Both holders write the same card entry. The issue's two parked designs are unbuilt.
- **Restarts change every key.** Open issue #29 describes an agent that rejoins under a new nickname after a daemon death. Its open tasks are lost. The issue says a rejoin under the old nickname would be refused as a duplicate until the dead key times out, about 90 s.
- **Browser peers never get a seal key.** Open issue #2 reports that directed sends to a browser peer fail every time. The error says "cards still propagating," and the issue says the message is wrong, because the browser client never publishes a card to the meta document.
- **Card publish failed silently before 0.12.0.** Issue #41 describes a card of 4840 bytes against a 3840-byte frame. Every directed send failed for more than 25 minutes, and the only trace was a WARN line. The fix sends the card in pieces. In the window between pieces, `/peers/<nick>/card` holds only the first keys (`AG:CHANGELOG.md:81`).
- **Stale seal key after restart (inferred, not reproduced).** A sender seals to the card it holds. A restarted peer's old card stays until the new one merges (`AG:node.rs:322-327`). A frame sealed to the old key fails to open at the restarted peer, which drops it with a WARN and sends no receipt. The sender's unicast write succeeded, so the sender sees no error.
- **Large directed messages are not backfilled.** A group of more than 16 shards is never logged (`AG:send.rs:688-690`). Only the shard-repair RPC can recover a lost shard.
- **Bystander flakes.** Open issue #42 says the directed-message-to-bystander test fails under host load. The failure count and log were not recorded.
- **Associated data is a constant.** The AEAD associated data is a fixed label, not the sender or recipient keys (`HN:seal.rs:30, 75-78`). Sender binding comes only from the outer signature.
- **Documentation disagrees with the code in five places:**
  1. `HN:identity.rs:10-11, 15-17` and `HN:message/mod.rs:1029-1030` describe trust-on-first-use binding of nicknames to keys, and say peers that pinned a key flag a new one. The receive path says nicknames are not pinned (`HN:recv.rs:547-551`). I found no trust-on-first-use code in the current tree. Only comments mention it.
  2. `HN:identity.rs:17-18` cites `docs/history-integrity.md`. That file does not exist on any ref I checked.
  3. `AG:tuning.rs:29-36` says a directed request "rides the gossip overlay unlogged" and is dropped when no link exists. The engine says a directed frame never rides gossip (`HN:transport/send.rs:1-6`), and the RPC sender calls the unicast path (`AG:send.rs:1768`). Commit `69e6a4d` reports the loss, and I did not trace its mechanism.
  4. The README says every message is "verified on receipt" (`AG:README.md:66-67`). The signature is checked, but the key is not checked against the nickname, so the claim holds only in the narrow cryptographic sense.
  5. The README says the mesh is "backfilling missed messages" (`AG:README.md:22`). Backfill covers directed frames only while the recipient's endpoint is known, and never covers groups above 16 shards.

## Observations for the owner

- The nickname routes a message, selects the seal key, and binds the endpoint. The key authenticates the author. Nothing binds the two, so they can disagree.
- Identity lasts one process. Anything that must outlive a process, such as an open task, depends on the nickname matching. The engine does not check that.
- For a sender, success means the bytes left the daemon. The `delivered` receipt is the only sign that the recipient's daemon received them, and it is sent once, with no retry.
- The product retries cards and shards only. A directed message is retried by the caller or not at all.
- Directed-message semantics changed in three steps: broadcast-only chat, then sealed unicast with backfill fixed on 2026-08-02, then receipts on 2026-10-15.
- The authors' own design notes for #28 and #29 would persist the session key. That is a proposal, not code.

## Not read

- The unicast pool, dial, and stream code (`HN:transport/pool.rs`, `send_unicast`). This is why ordering within one stream is unverified.
- The multihop relay forwarding path. I used only the comment at `HN:recv.rs:583-586` about relay retention.
- The meta-document merge, `decrypt_broadcast`, the mesh-password key derivation, and `seal_symmetric` (`HN:seal.rs:159-185`). I read only the comments.
- AG `surfaced.rs`, `task.rs`, `session.rs`, `peer_path.rs`, `ipc.rs`, `http.rs`, and the rest of `rpc.rs`.
- The agent-swarm repo. It was not in scope.
- History before 2026-07-17, under the agent-square name. A pickaxe search over the blobless clone timed out and was stopped. The dates of the seal extension and the card layout are therefore approximate.
- Issue comments. I read issue bodies only.
- Running any test or reproducing any failure.
- The earlier surveys. I grepped `a3-habilis.md` and `a1b-agent-swarm-mcp.md` for identity, sealing, and backfill. Both agree with the ephemeral key, the signed ciphertext, and the lack of nickname handling. I did not repeat them.
- `HN:docs/architecture.md`, which the survey cites for the sealing and identity sections. I did not read it directly.
