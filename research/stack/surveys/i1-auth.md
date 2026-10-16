# Authentication layers: iroh-auth and rcan

Date: 2026-10-16. Scope: how each proves a peer belongs, at which layer, which crypto, and whether either could replace spec D13/D17 membership and the per-message MAC (3.4, 3.6 validation).

## Sources read

- Spec: `spec/blueprint.md` D13 (line 195), D17 (line 219), 3.4 (lines 469-498), 3.6 (lines 516-591), network secret format (line 412), D14 (line 23), D16 (line 35).
- iroh-auth, `/tmp/ra-src/iroh-auth`, commit `282e45b` (2026-06-15): `src/lib.rs`, `src/auth.rs` (all 691 lines), `src/protocol.rs` (hook ranges 92-120, 191-215, 282-300; grep for the rest), `src/secret.rs`, `README.md`, `Cargo.toml`, `Cargo.lock` (version lines), `src/tests.rs` (test names).
- rcan, `/tmp/ra-src/rcan`, commit `fb158f5` (2026-08-27): `src/lib.rs` (ranges 45-56, 192-300, 354-400, 405-508, 617-666; grep for the rest), `src/tests.rs` (test names; bodies at 158-192, 275-300), `Cargo.toml`, `Cargo.lock` (version lines).
- iroh 1.3.0 hook API, `/tmp/ra-src/iroh`, commit `0072d7d`: `iroh/src/endpoint/hooks.rs` (grep and lines 1-40).
- GitHub API metadata for `rustonbsd/iroh-auth` and `n0-computer/rcan`.

## iroh-auth (github.com/rustonbsd/iroh-auth, commit 282e45b, crate 0.2.0)

- What it does for this scope: gates whole iroh connections behind a pre-shared secret. Each side runs a SPAKE2 handshake on a side ALPN before the application connection is admitted. It has no per-message or per-request check.
- Layer: connection. The gate is `EndpointHooks::after_handshake` (`src/protocol.rs:92-215`) and `before_connect` (`src/protocol.rs:282-300`). A remote that is not authenticated gets `Reject` with code 401 when it has no cache entry (`src/protocol.rs:211-216`), and 403 when blocked (`src/protocol.rs:198-203`).
- How, in code:
  - Handshake: SPAKE2 over `Ed25519Group`, password is the secret, identities are both endpoint ids (`src/auth.rs:317-321` acceptor, `src/auth.rs:414-418` opener). The handshake is bound to the two node ids, not to a card.
  - Confirmation: HKDF-SHA512 expands the SPAKE2 output into two 64-byte keys with contexts `iroh-auth-accept` and `iroh-auth-open` (`src/auth.rs:125-126`, `344-356`, `441-453`). Each side proves knowledge by returning the other's key. Comparison is constant-time via `subtle` (`src/auth.rs:373`, `465`).
  - Key use: the SPAKE2 shared secret is expanded only into those two confirmation keys. Nothing exports a session or message key. `grep shared_secret` finds only the `finish` and `Hkdf::new` calls (`src/auth.rs:338-344`, `435-441`). So iroh-auth produces no key that could serve as a per-message MAC key.
  - State: per remote EndpointId, in an LRU of 10,000 entries (`src/lib.rs:15`, `src/auth.rs:132-134`). Once `Authenticated`, every later connection from that id passes the gate without a new handshake (`src/protocol.rs:103`, `293`). The check is per connection, keyed by node id.
  - Failure: an invalid SPAKE2 value or a key mismatch sets `Blocked` for that id (`src/auth.rs:340-341`, `375-378`, `437`, `474-477`). Blocked ids are rejected (`src/protocol.rs:198-203`). The block lives in the same LRU and is lost on eviction (`src/protocol.rs:424`, `552`).
  - Timers: `AUTH_TIMEOUT` 30 s, `TRANSMISSION_TIMEOUT` 5 s (`src/lib.rs:13-14`).
  - Secret: any byte string (`src/secret.rs:4-48`). No length or entropy check.
- Crates and versions (from `Cargo.lock` at this commit): iroh 1.0.0, spake2 0.4.0, hkdf 0.13.0 (manifest; the lock also holds 0.12.4 through another dependency), sha2 0.11.0 (lock also holds 0.10.9), subtle 2.6.1, secrecy 0.10.3, rand 0.10.1 (used only for a dummy reply at `src/auth.rs:471`), lru 0.18.0, n0-watcher 1.0.0, tokio 1.52.3.
- Hook API in estafette's iroh 1.3.0: `EndpointHooks` exists with `before_connect` and `after_handshake`, and `AfterHandshakeOutcome` has `Accept` and `Reject` (`iroh/src/endpoint/hooks.rs:11-28`, `68`, `79`, `102`). iroh-auth's lock pins iroh 1.0.0, so the crate has not been built against 1.3.0 here. Not verified by build.
- Maturity: last push 2026-06-15. GitHub reports 13 stars and 0 releases. The clone is shallow, one commit visible, so history is unknown. Tests in `src/tests.rs`: success, failure with a wrong secret, parallel attempts, asymmetric retry, late failure does not clear an authenticated state (test names at lines 53, 61, 81, 90, 366). These tests cover connection gating only.
- What estafette could take: a pattern (mutual SPAKE2 key confirmation with both node ids bound into the transcript) and, if a connection gate is wanted, the crates spake2 and hkdf. Not a message MAC.
- Against the spec:
  - 3.6, first paragraph: "Accept a connection from any node id. Authorization is per request, by claim and mac, not per connection." iroh-auth does the opposite: it authorizes per connection, by node id, and caches the result (`src/protocol.rs:103`, `293`). Direct conflict with this sentence.
  - 3.6 step 2: the MAC check closes the stream without response. Under iroh-auth, a new node id must complete a handshake before its first request is admitted. That adds a round trip per new ephemeral node id (D14: transport keys are ephemeral, so each restarted process is a new id). Cost measured nowhere here; the handshake count is from `src/protocol.rs:282-300` and `src/auth.rs:498-686`.
  - D16: "The binary applies no allowlist and no blocklist." iroh-auth blocks a node id automatically after one failed handshake (`src/auth.rs:340`, `437`). It applies to connections, not to speech, but it is a blocklist in the transport.
  - D14 reason ("transport keys are ephemeral"): a `Blocked` entry is keyed by node id, so a restarted process with a new key escapes the block. Evidence for the block being weak under this spec's own key model.
  - D17 requirement that verification not depend on gossip state: iroh-auth does not use gossip. No conflict found.
  - Counter-evidence for the PAKE choice: the spec's network secret is 32 random bytes (spec line 412), so offline guessing of the secret is not a practical attack. SPAKE2's main benefit does not apply to this secret. iroh-auth accepts any string (`src/secret.rs`), which is weaker than the spec's secret format.

## rcan (github.com/n0-computer/rcan, commit fb158f5, crate 0.5.0)

- What it does for this scope: signed capability grants. A `Delegation` is an Ed25519-signed record of issuer, audience, capability bytes, origin, and expiry. A chain from a principal key to an invoker key authorizes an invocation. It has no shared secret, no transport, and no network concept. The crate has no iroh dependency (grep for "iroh" in `Cargo.toml` and `src/` finds nothing).
- Layer: none fixed. The caller checks one invocation at a time with `Authorizer::check_invocation_from_at` (`src/lib.rs:467-506`). The caller supplies the invoker key. The crate does not authenticate the invoker: "Make sure the invoker signed and authenticated the message carrying `capability`; this method only checks the capability chain itself" (`src/lib.rs:419-422`).
- How, in code:
  - Signed bytes: `DST` tag `rcan-2-delegation` followed by the canonical body (`src/lib.rs:617-619`, `226-250`, `625-644`). The body covers issuer, audience, origin, expiry, and the capability bytes with their length.
  - Verification happens in `decode` (`src/lib.rs:267-277`, `646-666`) with `verify_strict` (`src/lib.rs:665`). A `Delegation` is built only by `issue`, `delegate`, or a verified decode, so the authorizer does not re-verify signatures. The invariant holds by construction.
  - Chain rule (`src/lib.rs:474-504`): the first link's issuer equals the principal. Each link's issuer equals the previous audience. Each link is unexpired (`src/lib.rs:387-396`: `Expires::At(t)` is valid while `t >= now`, inclusive). The capability owner equals the principal (`src/lib.rs:489`). Each link `permits` the requested capability (`src/lib.rs:494`). The last audience equals the invoker (`src/lib.rs:499`).
  - No revocation, nonce, or replay protection. A search of `src/` and `README.md` for "revok", "nonce", "replay", "blacklist", and "denylist" found nothing. A valid, unexpired chain stays valid until its expiry.
  - Canonical encoding: postcard varints, non-minimal encodings rejected (`src/lib.rs:731-742`, test at `src/tests.rs:192`).
- Crates and versions (from `Cargo.lock`): ed25519-dalek 3.0.0 (manifest `>=3.0.0-rc.0, <4.0.0`), postcard 1.1.3 (manifest 1.1.1), serde 1.0.229, data-encoding 2.11.1, n0-error 1.0.0, smallvec 1.15.2, derive_more 2.1.1, hex 0.4.3. Dev only: minicbor-serde, ron, serde_json, assert_matches.
- Maturity: last push 2026-10-05. GitHub reports 26 stars, 2 releases (v0.4.0, v0.3.1), 6 tags. The manifest at this commit says 0.5.0, and no release tag matches it. Tests in `src/tests.rs`: wire and string snapshots (lines 81, 109), serde delegation (126), tamper rejection covering forged signature, widened capability, padding, version byte, and empty input (158-190), non-canonical varint (192), v1 rejection (210), wrong capability type (235), two-link chain (275), chain must start at the authorizer (341), subject must be the authorizer (356), owner needs no chain (377), expiry error (317).
- What estafette could take: a pattern (domain-separated Ed25519 signing with `verify_strict`, and verification at decode so no invalid value can exist). A crate (rcan itself) only if a signed-grant layer is ever wanted. ed25519-dalek is already in the tree at 3.0.0.
- Against the spec:
  - D13 rejected "Invitations signed by members: more machinery and a social process." rcan is signed-grant machinery of that kind, with chains (`src/lib.rs:194-224`). Recorded, not argued.
  - D16 rejected "Allowlists". rcan's authorizer is a grant check: an invocation passes only with a chain (`src/lib.rs:405-508`).
  - 3.4 claim signature: the spec signs the postcard bytes with `sig` zeroed and no domain tag. rcan prefixes a tag (`src/lib.rs:243`, `661`). The spec does not name a verify routine. rcan uses `verify_strict` (`src/lib.rs:665`).
  - 3.6 Message: the body is authenticated by a MAC keyed from the network secret. The card key signs only the claim, not the message. Any holder of the network secret can therefore emit a Message carrying any `from` claim it has seen. rcan's doc assumes the invoker signed the message (`src/lib.rs:419-422`). This is acceptable only if the one-owner rule of D13 is the trust boundary. Recorded as a fact about the spec.
  - 3.4 claims have a timestamp but no expiry and no revocation. rcan has both an expiry field and a verifier for it. No spec text addresses this difference.

## Answers to the scope questions

- **How each proves a peer belongs.** iroh-auth: possession of the shared secret, shown by a SPAKE2 exchange that binds both node ids. rcan: a signature chain from a principal key. It does not prove membership in a group. The spec: possession of the network secret (MAC over the message) plus a card signature over the claim.
- **Layer.** iroh-auth: connection, per remote node id, cached (`src/protocol.rs:92-300`). rcan: per invocation, supplied by the caller. Spec 3.6: per request, by claim and MAC.
- **Crypto and versions.** iroh-auth: spake2 0.4.0, hkdf 0.13.0, sha2 0.11.0 (SHA-512), subtle 2.6.1, secrecy 0.10.3, lru 0.18.0, iroh 1.0.0 (its lock; estafette tree is 1.3.0). rcan: ed25519-dalek 3.0.0 with `verify_strict`, postcard 1.1.3. Spec: BLAKE3 `derive_key` for the MAC key and topic id (spec 3.4), Ed25519 for the card claim.
- **Could either replace the per-message MAC and the signed claim.** No, for either. iroh-auth authenticates connections, not messages. It could replace the membership role of the MAC only if the spec accepted per-connection authorization, which 3.6 rules out. rcan has no shared-secret membership. Using it would replace D13 with an owner-signed grant, which D13 rejected, and it would add a card signature over each Message, which 3.6 does not have.

## Cross-project observations

- **Binding to transport identity.** iroh-auth binds the SPAKE2 transcript to both endpoint ids (`src/auth.rs:317-321`, `414-418`). The spec's 3.6 step 4 checks `from.node` against the remote node id. Both tie an authorization to the transport key. Seen in two sources, one of them the spec.
- **Verification at the boundary, not later.** iroh-auth refuses at the hook (`src/protocol.rs:92-215`). rcan verifies at decode so an invalid value cannot exist (`src/lib.rs:646-666`). The spec validates in order and closes or refuses at each step (3.6 steps 1-8). Consistent in intent; the spec's per-message check is stronger on which field fails.
- **Domain separation.** rcan tags its signed bytes (`src/lib.rs:619`). iroh-auth uses HKDF context labels (`src/auth.rs:125-126`). The spec's MAC keys use labels ("messaging mac v1", spec 3.4), but the claim signature has no tag (spec 3.4).

## Not read

- iroh-auth `src/protocol.rs` lines 300-366 and 420-560 (the `register_in_flight` and `release_in_flight` bodies), `examples/`, and the bodies of its tests.
- rcan `src/lib.rs` lines 300-354 and 660-756 (serde impls, decode body, varint helpers), its README, and most test bodies.
- crates.io metadata: the sandbox returns 403 for crates.io, so release counts and download numbers are not verified. GitHub data only.
- No build or test run of either crate. All behavior is from reading the code.
