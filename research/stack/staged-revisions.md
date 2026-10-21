# Staged revisions: intended spec text

Step 5 of research/stack/mechanic.md. Each entry is a ruled change (ledger.md "Staged revisions") with the spec sections it touches and the text it intends. Nothing here is applied: spec/blueprint.md changes only in one batch, on the owner's word. Open, not staged: C7 (relays topology, waits on E8) and the S16 experiment.

Drafted 2026-10-19 by claude-fable-5-1 (resident-anarchist) from the rulings in the journal and the evidence in research/stack/experiments/. Where a ruling leaves a parameter open, the entry says so.

## S14 first: node as identity (it reshapes most other entries)

Ruling: the card key is the iroh endpoint key; one live holder per card by an exclusive lock on the card's key file, taken before the endpoint is built; the Claim struct, the tie-break and the Displaced state retire; gossip payloads keep a signature by the card key. Evidence: e5-restart.md, state/m4-lifecycle.md, history/2026-10-16-node-as-identity.md.

- Vocabulary (2.2): remove `claim`, `transport key`. `member` becomes "A card held by a running node." `node` becomes "One binary process; after init, its endpoint key is its card's key."
- D2: add: "The sidecar is also the node's endpoint key. The binary takes an exclusive advisory lock on the sidecar file before it builds the endpoint and holds it for the life of the process."
- D3: replace with "D3 — The card key is the node key. Decision: after init, the node's iroh endpoint uses the card's secret key. Reason: one identity, proven by TLS on every direct connection; iroh 1.3 never evicts its per-peer address cache, so a fresh key per session leaks an entry on every long-lived node; churn fixes in iroh-gossip are unreleased. Rejected: a fresh transport key per session bound by a signed claim (the design before this revision). If you change this: every structure that names a node changes, and the lock no longer settles one holder."
- D4: replace with "D4 — Gossip payloads are signed by the card key. Decision: every gossip payload carries the sender's card public key and an Ed25519 signature by it over the postcard encoding with the signature field zeroed. Reason: gossip hides the author (delivered_from is the previous hop); on direct streams TLS already proves the remote card."
- D6: replace with "D6 — One live holder per card, by a lock. Decision: init takes a non-blocking exclusive lock on the card's sidecar; if the lock is held, init returns card_held. The lock file is never unlinked; the kernel releases it on any exit. Reason: cards are local to one machine (D8), so a second holder can only be a local process. Measured: the lock is free 6.5-10.4 ms after a SIGKILL; a restart takes it on the first try. Rejected: timestamp tie-break with probe (needs a protocol; a copied sidecar defeats any rule). If you change this: two live holders starve each other silently (measured)."
- D7: replace with "D7 — The sidecar lock is the only lock." (no lock file, pid file, or index is added; the lock sits on a file that exists).
- D10: add: "The endpoint is built after the card is chosen."
- D17: the message carries no claim; the receiver takes the sender's card from the connection's TLS-authenticated remote id; the MAC stays.
- D30, 3.9: remove Displaced. States: Unclaimed --init ok--> Claimed; any state --stdin closed or signal--> Stopping --> exit. Before init only the inbox listener runs.
- D32: "Each process is one node; after init, its endpoint key is its card's key."
- 3.1: remove `transport key`; `card public key` is also the node id.
- 3.4: remove the Claim struct, the tie-break paragraph, and the probe-replacement paragraph. Add the payload signature rule (as D4).
- 3.6: Message drops `from: Claim`; validation steps 3 and 4 become one step: "the remote id of the connection is the sender's card". Introduce and IntroduceAck drop `claim`. ProbeAck drops `claim`.
- 3.7: Presence, Departure, Unreachable carry `card: [u8; 32]` and `sig: [u8; 64]`; Unreachable's `reporter: Claim` becomes `reporter: [u8; 32]` with the signature over the payload.
- 3.8: remove the rows "card known, another node, earlier/later by the tie-break order" and "Presence received for your own card from another node". `list_cards`' `held` comes from trying the lock (no observer wait).
- 3.10: `card_held` means the sidecar lock is taken. `init`: take the lock, build the endpoint, subscribe.
- 3.15: test 6 becomes "Two processes on one machine init one card within 100 ms: exactly one Claimed, the other card_held"; test 18 "B is killed and restarted with the same card: within one second A's send to B is delivered" (measured: 0.2-1.0 s); test 20 per S12.
- 3.16: replace "Do not replace a held claim without a probe" with "Do not hold a card without its sidecar lock".

## S12: announcement ordering

Ruling: per-member seq = max(now_ms, last+1); keep the highest; ignore older than a max age; tombstone a departed member's last seq. Evidence: e4-presence.md scenario 6 (tombstone and max age each cover one case), state/m1-roster.md.

- 3.7: Presence and Departure carry `seq: u64` (replaces `ts` and the claim's `ts`). Unreachable keeps `ts` (it reports an observation, not a member's own state).
- 3.8: "A node accepts a Presence or Departure only if its signature verifies, its seq is above the seq held for that card, above any tombstone for that card, and not older than the max age by the receiver's clock. A Departure leaves a tombstone of its seq, kept for the max age." A member's own seq generator: `seq = max(now_ms, last_seq + 1)`.
- 3.14: add `announcement max age 300 seconds` (owner ruling; tolerates drifted clocks; a shorter value silently hides a machine whose clock is off).

## S15: announce when joined

- 3.8: the row "init succeeds" becomes "init succeeds: subscribe; when the topic reports joined, send Presence". Evidence: e4-presence.md (Presence at join is lost; tables never fill).
- D18: add "The first Presence follows the gossip layer's joined signal."

## S17: departure

- 3.8 stop row: "process stops: broadcast Departure, release the sidecar lock, wait 5000 ms, exit."
- 3.14: "departure wait at exit" becomes 5000 ms.
- D19: add "The broadcast only queues the Departure; the wait is what delivers it (measured: immediate exit reached 0-2 of 4 peers; 1000 ms reached 4 of 4). The lock is released first so a restart on the same card is never blocked; a late Departure carries a lower seq than the new session's Presence and is ignored (S12)."

## S2: idle timeout

- 3.14: add `QUIC idle timeout 10000 milliseconds` (set via the endpoint's transport config). Evidence: e3-kill.md (crash noticed at ~33 s by default, ~13 s at 10 s), e4 (~15 s plus a 3 s probe: every peer Unreachable at ~18 s).

## S10, S19: direct protocol timeouts, no retries

- 3.6: add "A node keeps one connection per peer and reuses it; each request opens a new bidirectional stream. A server waits at most the read timeout for a request's bytes, then resets that stream; the connection stays."
- 3.10 send algorithm: step 3 "Use the held connection to the peer, or dial `card` (S20)."; on any failure "drop the held connection; return the error." No retry.
- 3.14: add `server read timeout 10000 milliseconds`.
- 3.16: add "Do not retry a send at the transport level."
- Note (e5): a request on a held connection to a killed node hangs until the idle timeout and then fails; with S2 at 10 s that matches the ack timeout. Ruled as: no retries, clean errors.

## S11: no duplicate suppression

- D25: remove. 3.6 step 7: remove. 3.14: remove `duplicate set`. 3.15 test 17: remove. Reason to record: each send mints a fresh id and the binary never retries, so a duplicate set would never fire; an agent sending twice sends two messages.

## S18: inbox

- 3.11: unchanged mechanics (ring of the last 1000 frames, `since`). Add: "Nothing is removed by reading. The node does not track what was read. The sender's ack means the message entered the inbox. Gaps, limits, and what fits a harness's context are the bridge's business."
- D22: "The ack means the message is in the recipient's inbox" (already so); add "never that it was read".

## S20: address lookup

- 3.7, 3.8: Presence and IntroduceAck carry `addr`: the sender's full current endpoint address (relay URL and direct addresses; the id is the card). On receipt a node replaces that card's entry in its address lookup (replace, never merge: merging piled up stale addresses in e6). Re-announce (S13) carries the new address.
- 3.10 send step 3: "Dial the peer's card id; the address comes from the lookup fed by Presence and Introduce." Evidence: e8-failover.md (gossip's built-in lookup learns only direct neighbors; a 5-node mesh was undialable by id until announcements carried addresses), e6-lookup.md (~14 ms first dial among adjacent nodes, ~1 s after a restart on a new port).
- 3.3, 3.13: the invitation carries each bootstrap node's full endpoint address (id plus relay URL), since the bootstrap must be dialable before the mesh exists.
- D15: moves to 2.12 Deferred ("local network discovery (mDNS)").

## S13: re-announce triggers

- 3.8 row "endpoint reports a network change or a relay reconnect" becomes "the home relay's status changes, or the node's own address set changes (iroh `home_relay_status`, `watch_addr`): send Presence". Evidence: e1-api.md check 6 (relay status reports loss and reconnect; the address watcher is silent on relay loss).

## S1, S9: gossip frame

- 3.5, 3.14: the serialized `public` mapping is capped at 3072 bytes (owner ruling), so the largest Presence, address included, fits the default 4096-byte gossip frame with about 0.5 KB headroom (gossip adds 38 bytes; e2-size.md). Verify the worst case with a size test at application.
- 3.7: add "A node checks every payload's encoded size against the gossip frame limit before broadcasting and never sends a larger one (an oversize broadcast returns Ok, is lost, and leaves the link dead: measured)."
- 3.16: add "Do not broadcast a payload larger than the gossip frame limit."

## S5: hex

- 3.1: card public key, card secret key, network secret, fingerprint: lowercase hexadecimal (64, 64, 64, 8 characters). Node id: the card public key in the same form (iroh's own text form).

## S6: no presence encryption

- 1.6 or D13: add "Presence is authenticated, not encrypted. A party holding the topic id can read presence; the secret proves who wrote it." (S16 then closes the topic to outsiders at connection time.)

## S16: gossip admission (needs the experiment)

- Owner confirmed the mechanism: the after_handshake hook, both ways.
- D13, 3.6: "On every gossip connection, in both directions, each side proves the network secret: the verifier sends a 32-byte random nonce on a new bi-stream; the prover answers keyed_hash(gate key, nonce || verifier id || prover id), gate key = derive_key("messaging gate v1", secret); timeout 3 s; failure closes the connection. The gate runs in the endpoint's after_handshake hook, so neither accepted nor gossip-dialed connections reach the gossip layer unproven." Evidence: e9-gate.md (outsider gets nothing in both directions; ~1-2 ms per connection; about 60 lines, no new crate). An accept-loop-only wrapper, the shape in the ruling's wording, cannot verify an acceptor that gossip dials, and a lying acceptor read Presence: the owner confirms the hook mechanism at application.
- 3.14: add `gate timeout 3000 milliseconds`. 3.4: add the gate key derivation. Note: the secret must be high-entropy (a captured nonce and proof allow an offline guess).

## Stack D-records (Part 2) and the manifest (Part 3)

New D-records, each with Decision, Reason, Rejected, If you change this:
- S3: the relay ships behind a cargo feature (`relay`), compiled only into infrastructure builds.
- S4: cards are parsed with yaml-rust2; our own converter turns `public` into JSON bytes. Rejected: serde YAML crates on unsafe-libyaml (RUSTSEC-2024-0449).
- S7: iroh-gossip pinned to 0.101.0 exactly; upgrade when the churn fixes ship (#161, #178, #189), with a mixed-version join test.
- S8: the direct protocol is written by hand on iroh streams. Rejected: irpc 0.17 (fixed 16 MiB cap, allocates before the body, closes the connection on a bad frame).
- Manifest table in Part 3 (3.2): crates with exact versions and features, compiled at application time from the rulings: iroh 1.3.0, iroh-gossip 0.101.0, iroh-relay 1.3.0 `server` (feature-gated), rmcp 3.5.1 (`server`, `transport-io`), clap 4 (`derive`), serde, postcard, serde_json, blake3, data-encoding, uuid (`v7`), tokio (`signal` added), toml, yaml-rust2, libc. Exact counts by `cargo tree` at application time.
