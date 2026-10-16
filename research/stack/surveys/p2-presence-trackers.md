# P2: finding peers without a fixed bootstrap node

Date: 2026-10-16. Scope: how two projects find the first peer on a gossip topic, and whether either replaces the bootstrap member of D14.

## Sources read

- iroh-gossip-rendezvous, commit 871c688 (shallow clone at /tmp/ra-src/iroh-gossip-rendezvous): Cargo.toml, Cargo.lock, src/lib.rs, src/builder.rs, src/keys.rs, src/crypto.rs, src/gossip_glue.rs, src/protocol.rs (initial_join, spawn_loops, build_record), src/dht/mainline.rs, tests/two_node_bootstrap.rs, README.md, CHANGELOG.md.
- distributed-topic-tracker, commit dadc44f (shallow clone at /tmp/ra-src/distributed-topic-tracker): Cargo.toml, Cargo.lock, README.md, src/lib.rs, src/crypto/keys.rs, src/crypto/record.rs, src/gossip/sender.rs, src/gossip/topic/bootstrap.rs (lines 1-225, 365-403), src/gossip/topic/topic.rs (lines 140-200, 370-400, 445-470), src/dht.rs (lines 1-60, 170-180), examples/simple.rs, tests/tests.rs (names only).
- mainline 6.1.2 and 7.0.0 crate tarballs from static.crates.io, src/rpc.rs (default bootstrap list only).
- iroh 1.3.0 from the local cargo registry, src/endpoint/presets.rs (N0 preset only).
- Spec: spec/blueprint.md, D13, D14, D15, D42, D43, section 3.4.
- Repo metadata via gh api (dates, star counts, tag and commit counts).

No tests were run. No network runs against the Mainline DHT were made.

## iroh-gossip-rendezvous (github.com/swaits/iroh-gossip-rendezvous, commit 871c688)

- **What it does for this scope:** derives DHT slot keys and a gossip topic from a human passphrase and an app salt. Nodes write signed, encrypted peer lists into public Mainline DHT slots. A newcomer reads the slots, gets node ids, and joins the gossip topic.
- **First peer, in code:** `initial_join` reads all K slots in parallel and joins whatever ids it finds (`src/protocol.rs:173-212`). With no ids found, the node runs alone. The write loop's first iteration publishes at once, so the first node becomes findable without a member (`src/protocol.rs`, `spawn_loops`, first-iteration comment). Default write period is 300 s (`src/builder.rs:33`), heal period 30 s (`src/builder.rs:35`), failure retry 15 s (`src/builder.rs:41`).
- **Topic and key derivation:** HKDF-SHA256 with salt = app salt and input key material = the passphrase bytes, unstretched (`src/keys.rs:47-53`). Topic id = expand with info `"topic"` (`src/keys.rs:56-63`). Per-slot Ed25519 signing key and wrapper key come from info strings `sk25519:` and `wrap:` (`src/keys.rs:82-104`). The slot address is the public verifying key, so it is public (`src/keys.rs:6-9`).
- **Record protection:** each record is sealed with a one-time key, wrapped under an epoch key derived from the slot wrapper key (`src/crypto.rs:55-60`, `src/crypto.rs:70-117`, `src/crypto.rs:119-150`).
- **Against spec 3.4:** the topic id is not BLAKE3 `derive_key` with `"messaging topic v1"`. It is HKDF-SHA256 with different labels, and it comes from a passphrase, not a 32-byte secret. No wire MAC exists. `broadcast` passes bytes through (`src/rendezvous.rs:101`).
- **How peers authenticate:**
  - DHT slot writes are signed by a key derived from the passphrase, so a valid signature shows passphrase knowledge, not node identity (`src/keys.rs:82-92`). I did not trace the mainline read-side verify path.
  - Records are decryptable only with passphrase-derived keys (`src/crypto.rs:119-150`).
  - Node identity is the iroh endpoint key. The gossip accept loop takes any connection on the gossip ALPN with no membership check (`src/gossip_glue.rs:152-180`). Ids are joined with no proof step (`src/gossip_glue.rs:60`).
  - Nodes vouch for other ids inside records (`src/protocol.rs`, test `vouching_propagates_ids_across_slots`, near line 1063). Vouched ids get no check beyond the record's AEAD.
- **Always-on node or public DHT:** no always-on node. It needs the public Mainline DHT. Default bootstrap routers are `router.bittorrent.com`, `dht.transmissionbt.com`, `dht.libtorrent.org`, `relay.pkarr.org` (`mainline 6.1.2 src/rpc.rs:42-47`). Endpoints use the iroh N0 preset when none is supplied (`src/gossip_glue.rs:91-100`). That preset adds n0 Pkarr publish and resolve, n0 DNS lookup, and default relay mode (iroh 1.3.0 `src/endpoint/presets.rs:116-135`). The rendezvous pins iroh 1.0.0-rc.0, so I did not read that version's preset.
- **Crates it uses:** iroh `=1.0.0-rc.0` (`Cargo.toml:91`), iroh-gossip `0.99` (lock 0.99.0; `Cargo.toml:92`), mainline `6` with async (`Cargo.toml:93`), hkdf `0.13`, sha2 `0.11`, chacha20poly1305 `0.10`, blake3 `1`, zeroize `1`, ed25519-dalek `=3.0.0-pre.7` (`Cargo.toml:103-107`), rand `0.9`, tokio-util, futures-lite, bytes, tracing, thiserror 2, async-trait, mutants.
- **Maturity:** created 2026-04-22, last push 2026-05-13, about 13 commits (paged count), 2 stars. The API returned one tag, `v0.1.0`. `Cargo.toml` and `CHANGELOG.md` say 0.2.1. Mechanism tests: `tests/two_node_bootstrap.rs` uses an in-memory DHT injected through the `test-support` feature (lines 1-5, 15, 28). The real Mainline path is gated behind the `mainline-live` feature (`Cargo.toml`, nightly lane only).
- **What estafette could take:**
  - Crate: nothing as a dependency. The iroh pin differs from estafette's iroh 1.3.0 and iroh-gossip 0.101.0.
  - Pattern: a stable address derived from a secret, not from a node key (`src/keys.rs:6-9`).
- **Against the spec:**
  - D14, rejected option "membership lookup in a public DHT": this project is that option (`src/builder.rs:365-372`, `Cargo.toml:93`).
  - D14, reason "transport keys are ephemeral, so nothing else has a stable address": the mechanism here has a stable address that is a secret-derived slot key, not a node key (`src/keys.rs:6-9`). This is evidence against the reason as stated, not a verdict.
  - D13, secret strength: the passphrase feeds HKDF with no stretching (`src/keys.rs:47-53`). Slot address and wrapper key both derive from it, and the records are public. An observer who knows the app salt could test guesses offline by fetching a record and attempting decryption (`src/crypto.rs:119-150`). I did not run this. The spec does not state the entropy of the secret in D13 or 3.4, so the synthesis has to decide it.

## distributed-topic-tracker (github.com/rustonbsd/distributed-topic-tracker, commit dadc44f)

- **What it does for this scope:** finds peers on a topic name through public Mainline DHT slots. Each node writes a signed record to a per-minute slot. The record's peer list is encrypted with a key derived from an optional initial secret. A newcomer reads the current and previous minute, then joins the gossip topic by endpoint id.
- **First peer, in code:** the bootstrap loop reads records for the previous and current minute (`src/gossip/topic/bootstrap.rs`, around lines 140-160). With no records, it signs its own record with an empty peer list and publishes it (around lines 160-190). It retries after `no_peers_retry_interval` (`bootstrap.rs:213`). Joins are by endpoint id (`src/gossip/sender.rs:82`).
- **Topic and key derivation:** the topic id is SHA-512 of the topic name, first 32 bytes (`src/crypto/record.rs:60-68`). It has no key, so anyone who knows the name derives it. The per-minute DHT signing key is SHA-512 of topic hash and minute (`src/crypto/keys.rs:103-111`). The slot salt is SHA-512 of `"salt"`, topic hash and minute (`src/crypto/keys.rs:139-149`). The initial secret enters only through SHA-512 truncated to 32 bytes (`src/crypto/record.rs:212-215`) and then the encryption key derivation (`src/crypto/keys.rs:113-136`). The secret is any byte string. The example uses `b"my-initial-secret"` (`examples/simple.rs`, README lines 56-61).
- **Against spec 3.4:** the topic id is unkeyed. Spec 3.4 keys it from the secret. The initial secret does not touch the topic id at all, and the primitive is SHA-512, not BLAKE3 `derive_key`. No wire MAC exists. Application payloads go out as raw bytes (`src/gossip/sender.rs:42`).
- **How peers authenticate:**
  - Each record is Ed25519-signed by the publishing node's key over topic, minute, public key and content. Verification uses `verify_strict` and checks topic and minute (`src/crypto/record.rs:486-511`, `src/crypto/record.rs:547-562`). A verified record binds content to a node key.
  - Membership is decryption. Records are HPKE-encrypted to a key derived from the initial secret (`src/crypto/record.rs:566` onward, `src/crypto/keys.rs:113-136`).
  - Nothing proves membership node-to-node. Gossip payloads carry no signature or MAC at this layer (`src/gossip/sender.rs:42`). I did not read the receiver path in full.
- **Always-on node or public DHT:** no always-on node. It needs the public Mainline DHT. Default bootstrap routers match the rendezvous project (`mainline 7.0.0 src/rpc.rs:43-47`). The examples and the topic tests use the iroh N0 preset (`examples/simple.rs:16`, `src/gossip/topic/topic.rs:378`), so it inherits the same n0 Pkarr and DNS and relay dependence as the rendezvous project.
- **Crates it uses:** iroh `1` (lock 1.0.0; `Cargo.toml:35`), iroh-gossip `0.101` (lock 0.101.0; `Cargo.toml:38`), mainline `7` with async (`Cargo.toml:46`), ed25519-dalek `3.0.0-rc.0` (`Cargo.toml:22`), ed25519-dalek-hpke `0.0.5` (`Cargo.toml:25`), sha2 `0.11` (`Cargo.toml:19`), rand `0.10` (`Cargo.toml:47`), getrandom `0.4`, chrono (clock), actor-helper `0.3`, postcard `1` (`Cargo.toml:56`), serde, tracing, tracing-subscriber `0.3` (`Cargo.toml:60`, listed under regular dependencies).
- **Maturity:** created 2025-07-12, last push 2026-06-15, about 137 commits (paged count), 42 stars, no tags returned by the API. Mechanism tests are in `tests/tests.rs`: record round trip (line 13), record verification (line 50), HPKE round trip (line 77), secret rotation (line 151), deterministic keys (lines 188-222), topic id (line 238), multi-receiver events (line 253). No test covers the first-peer DHT path in those names. The README claims an end-to-end run (`README.md:112`, `test-e2e.sh`). I did not run it.
- **What estafette could take:**
  - Crate: none recommended by this survey. The project pulls three crates the tree lacks: ed25519-dalek-hpke, actor-helper, and mainline 7. The iroh and iroh-gossip versions match the tree's lines.
  - Pattern: per-minute slot addressing from the topic hash (`src/crypto/keys.rs:103-149`). Records signed by the node key (`src/crypto/record.rs:486-562`).
- **Against the spec:**
  - D13, membership is possession of the secret: this project's topic id is public (`src/crypto/record.rs:60-68`). The secret protects only record contents. A copy of this derivation would make the topic name the only access input, which D13 rejects.
  - D13, secret strength: the initial secret goes through unstretched SHA-512 (`src/crypto/record.rs:212-215`), and the example value is a short phrase. Records are public, so the same offline check as the rendezvous project applies. Not run.
  - D14, rejected option "membership lookup in a public DHT": this project is that option (`src/dht.rs:176-178`, `mainline 7.0.0 src/rpc.rs:43-47`).
  - D14, reason "a relay is needed anyway": this project does not run a relay. It relies on n0 relays through the N0 preset (`examples/simple.rs:16`).

## Cross-project observations

- **No always-on node in either.** Both find the first peer by writing a signed record to a public Mainline DHT slot. A node that starts alone publishes itself and waits. A later node reads the slot and joins. This meets D14's stated consequence, "a node that starts alone has nobody to ask", through the DHT instead of a member.
- **Both depend on the public Mainline DHT.** That is the option D14 rejects. Both use the same four default routers (`mainline 6.1.2 src/rpc.rs:42-47`, `mainline 7.0.0 src/rpc.rs:43-47`).
- **Both still depend on n0 services.** Both use the iroh N0 preset for endpoints (`src/gossip_glue.rs:91-100`, `examples/simple.rs:16`). That preset adds n0 Pkarr publish and resolve, n0 DNS, and default relays (`iroh 1.3.0 src/endpoint/presets.rs:116-135`). Neither runs a relay of its own, so the relay role in D14 stays outside both.
- **Neither topic id is the spec's derivation.** Spec 3.4 is BLAKE3 `derive_key` with `"messaging topic v1"`. The rendezvous project uses HKDF-SHA256 from a passphrase (`src/keys.rs:47-63`). DTT uses unkeyed SHA-512 of a name (`src/crypto/record.rs:60-68`).
- **Neither authenticates application traffic at the wire layer.** Spec 3.4 requires a MAC keyed from the secret. Neither project has one. DTT signs records, and the rendezvous project AEAD-protects DHT records. Gossip payloads carry neither.
- **Both use slot addresses derived from a shared input.** That shared input is a passphrase in one and a topic name in the other. Both make the slot public. Both expose the secret's strength to offline checks, which D13 leaves open.
- **The iroh 1.x lines differ.** Rendezvous pins iroh 1.0.0-rc.0 with iroh-gossip 0.99. DTT locks iroh 1.0.0 with iroh-gossip 0.101.0, the same gossip line as the tree. Estafette's tree is at iroh 1.3.0.

### Could either replace the D14 member?

- **Partly, for first contact.** Both show that DHT slots can replace the member as a meeting point, subject to the DHT's reach and to the write-then-read delay.
- **No, for the relay.** Both still rely on n0 relays and n0 address services.
- **Against D14's reason.** Both avoid the "stable address" problem. They use a slot address derived from a shared input, not a node key. That is evidence on the reason as written, not a verdict.
- **Against D14's rejected option.** Both are that option, so the decision in D14 is the direct point of tension.

## Not read

- iroh-gossip 0.99 and 0.101.0 source. The gossip join and neighbor logic is inferred from the callers only.
- iroh 1.0.0-rc.0 source. Not in the local registry. The N0 preset in rc.0 was not read.
- Rendezvous: `src/protocol.rs` beyond `initial_join`, `spawn_loops` and vouching, `src/merge.rs`, `src/wire.rs`, `src/dht/memory.rs`, `src/sim_impl.rs`, `PROTOCOL.md`, `ARCHITECTURE.md`, and the fuzz and proof harnesses.
- DTT: `src/gossip/receiver.rs` beyond the struct, `src/gossip/topic/publisher.rs`, `src/gossip/merge/*`, `src/config.rs`, `bootstrap.rs` outside the lines listed, `test-e2e.sh`, `examples/e2e_test.rs`, `ARCHITECTURE.md`, `PROTOCOL.md`.
- mainline 6.1.2 and 7.0.0 beyond the default bootstrap list. The read-side signature verification was not traced.
- The index file at `research/stack/index/index.md` was not consulted.
- No tests were executed in either project. No live DHT or relay runs were made.
