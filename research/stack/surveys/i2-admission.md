# Private networks and long-lived identity over iroh keys

Date: 2026-10-16.

## Sources read

- chio, commit `5b8bec41d32f3838b880576fe6123c983ecebf8d` (last commit 2026-09-02, 0 tags). Adapter crate `crates/trust/chio-federation-transport-iroh`: `ARCHITECTURE.md`, `README.md`, `Cargo.toml`, `src/lib.rs`, `src/admission.rs` (full), `src/identity.rs` (lines 60-100, 110-140, 236-290, 380-440, 540-690, 740-765), `src/lanes/limits.rs` (255-340), `src/lanes/fanout.rs` (160-180). chio-cli `crates/products/chio-cli/src/cli/chio/dispatch/pheromone/iroh_mount.rs` (84-100, 215-245, 355-410, 1138-1162), `io.rs` (55-60).
- iroh-rings, commit `8aab11d70cfb06683709bd2c20c666a9bba98b7b` (v0.8.2, last commit 2026-09-25, 1 tag). `src/lib.rs`, `src/ring.rs` (8), `src/protocol/gate.rs` (full), `src/registry.rs` (1-350 by grep and docs, 115-210, 283-305), `Cargo.toml`, `README.md` and `examples/read.rs` by grep.
- Spec `spec/blueprint.md`: D2-D7 (lines 119-180), D13 (195-199), section 3.4 (469-498).

## chio: crates/trust/chio-federation-transport-iroh (iroh 1.0.1 in Cargo.lock; Cargo.toml requires `1.0`)

- **What it does for this scope.** Admits or rejects an iroh connection by its authenticated `EndpointId`, using an issuer-signed directory that maps each operator's `kernel_id` to a transport key. The gate runs before any lane handler.
- **Identity binding, in code.** The long-term operator passport key signs a length-prefixed preimage of (domain tag, `kernel_id`, transport `EndpointId`) (`identity.rs:70-100`). `verify_bundle` checks that signature per entry (`identity.rs:683`). The whole directory is then signed by a pinned external issuer over the bundle body (`identity.rs:236`, `250`, step 5 of `verify_bundle_inner`). Replay is handled by a version floor and predecessor hash chain (`identity.rs:605`), not by a per-claim timestamp.
- **Transport key lifetime.** The transport key is a persistent ed25519 seed read from a file, `{"seedHex": ...}` (`iroh_mount.rs:91`, `227-239`). The CLI requires `--iroh-transport-key` and checks that its public half matches the endorsed `EndpointId` (`iroh_mount.rs:371`, `392`). The file's own comment calls it "rotatable" (`iroh_mount.rs:85-89`).
- **Accept-time admission.** `DirectoryGate::after_handshake` calls `decide(&conn.remote_id())` (`admission.rs:143-145`). `decide` accepts only if `authorize` finds a non-removed entry (`admission.rs:111-137`, `identity.rs:416`). Otherwise it returns Reject 403 (`admission.rs:31-34`). The gate is installed with `.hooks(gate)` (`iroh_mount.rs:1158`).
- **Where a secret lives.** Nowhere in the adapter. The grep for secret, psk, hmac, and keyed terms in `src/` finds no network secret and no MAC. Trust roots are public keys: pinned issuer public keys (`identity.rs:250-262`) and the passport public key in each entry (`identity.rs:124`). The only private material is the per-node transport seed and the passport key (`io.rs:55`, loaded by `load_relay_signing_key`).
- **Second live holder.** Not detected. The bundle load rejects duplicate `kernel_id` (`identity.rs:652-660`) and duplicate `EndpointId` (`identity.rs:750-762`), but only at load time. At runtime `decide` checks each connection alone (`admission.rs:111-137`). `AcceptLimiter` caps in-flight handlers per `EndpointId` (`limits.rs:270`, `327`). That is a fairness cap, not holder detection. Nothing in the adapter stops two nodes started with the same seed from both presenting the same `EndpointId`. Whether iroh routes to one or both is in iroh, which was not read.
- **Probe, tie-break, timestamp.** None found. No `probe` or tie-break code in the adapter.
- **Maturity.** Last commit to the crate path 2026-09-02. Tests present: `identity.rs` test module from line 839 (rotation, eviction, duplicate tests at 1081-1720), `admission.rs` test module (148-372), `lanes/limits.rs` (`per_peer_cap_bounds_single_peer_below_lane_cap`, around 515).
- **What estafette could take.** Pattern: the issuer-signed, body-hash-pinned directory with a version floor and predecessor chain as a model for replay control. Pattern: the three-step fail-closed `verify_bundle` ordering. Crate: nothing, because the crate depends on chio-internal crates.
- **Against the spec.**
  - D3 (fresh transport key per session): contradicted. The adapter needs a stable key, persisted in a file and endorsed by the directory (`iroh_mount.rs:227`, `371`, `392`). The stated reason is that the directory names an `EndpointId`.
  - D4 (self-signed claim, no center): contradicted in shape. Chio binds the identity through a pinned external issuer, which maps `kernel_id` to `EndpointId`. The spec rejects "a trusted registry that maps handles to nodes" as a center (D4 Rejected). The passport endorsement is closest to D4. It lacks `ts` and `handle`, and it is wrapped by the issuer signature.
  - D6 (one live holder, probe): not implemented. Duplicates are caught only at load time.
  - D2 (secret in a sidecar, 0600): the transport seed loader does not check file mode (`iroh_mount.rs:227-239`). The `read_utf8_json_file` helper was not read, so a mode check there is not ruled out.
  - D13 (network secret): no network secret. Membership is issuer-signed directory membership and per-treaty party sets (`identity.rs` party-set index near 768-830). The fan-out topic is `blake3(label || 0x00 || treaty_id)` (`lanes/fanout.rs:172-177`), a public value a non-party can compute. The adapter gates join and receive on party membership (`ARCHITECTURE.md`, Invariants). Its own docs record a residual: the gossip join is not gated at protocol level.
  - 3.4 (topic id and mac key derived from the secret): not implemented. No keyed derivation and no MAC in `src/`.

## iroh-rings (iroh 1.2.0 in Cargo.lock; Cargo.toml requires `1.2.0`)

- **What it does for this scope.** Access control over iroh protocols. A ring is a named group of peers. Resources bind to rings with permissions (Read, Write, Delete). The gate checks each request against the caller's `EndpointId`.
- **Identity binding, in code.** None beyond the transport. The peer's identity is its `EndpointId`, which iroh authenticates at the QUIC/TLS handshake (`src/protocol/gate.rs:12-17`). No card, no claim, no signature by a second key. The caller owns key generation. The examples call `SecretKey::generate()` (`examples/read.rs:84`, `examples/delete.rs:83`). Persistence is the caller's choice, and the library does not say how to keep the key.
- **Admission.** Per request. `handle_request` checks `has_permission(&peer, ...)` or `Transfer::can_access`, and denies otherwise (`gate.rs:158-169`). Membership is an operator's explicit add by `EndpointId` (`registry.rs:201`). Memberships can expire, and an expired one counts as absent (`lib.rs:22-25`, `registry.rs:120`).
- **Where a secret lives.** Nowhere. No token, invite, or shared key in `src/` or the README. The `OPEN_RING_NAME` ring (`ring.rs:8`, `lib.rs:19-20`) grants Read to any peer regardless of membership, by design.
- **Second live holder.** Not detected. Nothing compares live connections that present the same `EndpointId`. The per-connection loop (`gate.rs:113-120`) serves every stream the peer opens.
- **Maturity.** Last commit 2026-09-25, 1 tag. Tests present: unit tests in `registry.rs` (around 680-860, including expiry) and `tests/gate_integration.rs`.
- **What estafette could take.** Pattern: the per-request `has_permission` check plus the `Transfer` extension point, as a shape for an accept-time gate that is separate from the handler. Crate: nothing, because the crate is a resource-access library and does not model identity.
- **Against the spec.**
  - D1 and D2: no card and no sidecar. Identity is only the `EndpointId`. The spec's card and key pair split is absent.
  - D6: no holder check, and no live-presence notion.
  - D13: the open ring is public-read by design (`ring.rs:8`, `lib.rs:19-20`). This is the "open network" that D13 rejects, applied to a resource rather than to membership.

## Cross-project observations

- **Both bind identity to the `EndpointId` that iroh authenticates.** Neither uses a separate persistent transport key tied to a card through a claim with `ts` and `handle`. chio keeps the transport key stable by design. iroh-rings leaves it to the caller.
- **Neither has a network secret or a keyed MAC.** Trust roots are public keys or explicit per-endpoint lists. Both gates are fail-closed per connection.
- **Neither detects a second live holder.** chio checks duplicates only at bundle load. iroh-rings does not check at all. Both rely on the transport to prevent two endpoints from sharing one `EndpointId`, and the spec's D6 probe is absent in both.
- **Both put admission before the handler.** chio uses `after_handshake` with `EndpointHooks`, and iroh-rings checks inside `accept`. The D6 probe rule has no counterpart in either.

## Not read

- iroh source (1.0.1 and 1.2.0): how two endpoints with one secret key share an `EndpointId`, and what iroh does at a duplicate.
- chio: `lanes/fanout.rs`, `lanes/pheromone.rs`, `lanes/revocation.rs`, `lanes/bilateral.rs`, `catchup.rs`, `metrics.rs`, and most of `identity.rs` test bodies. The chio-core-types `Keypair` type, and the file-mode behaviour of `read_utf8_json_file`.
- chio: `ARCHITECTURE.md` cites an ADAPTER-SPEC; that document is not in the clone and was not located.
- iroh-rings: `src/backends/redb` and `src/transfers/fs.rs` beyond grep.
- Spec sections other than D2-D7, D13, and 3.4.
