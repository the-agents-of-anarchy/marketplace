# iroh 1.3.0: endpoint, router, keys, remote id

Date: 2026-10-16.

Version read: iroh tag v1.3.0, commit 0072d7d84b233f9e7185eb676f049beaf557ac03, clone at /tmp/ra-src/iroh. iroh and iroh-base are both 1.3.0 (iroh/Cargo.toml:3, iroh-base/Cargo.toml:3).

Sources read: spec sections 3.1, 3.4, 3.6 of /Users/ryzhakar/pp/agents-of-anarchy-marketplace/spec/blueprint.md; iroh-base/src/key.rs, iroh-base/src/lib.rs, iroh-base/Cargo.toml; iroh/src/endpoint.rs, iroh/src/endpoint/presets.rs, iroh/src/endpoint/connection.rs, iroh/src/protocol.rs, iroh/src/lib.rs. Nothing was compiled or run. Every answer is from reading source.

## Answers

**1. Endpoint builder.**

- **Secret key:** `Builder::secret_key(SecretKey)` at iroh/src/endpoint.rs:531. If unset, a random key is generated. Its public half is the endpoint id.
- **Relay modes:** `Builder::relay_mode(RelayMode)` at iroh/src/endpoint.rs:568. `RelayMode` (endpoint.rs:1993) has `Disabled`, `Default`, `Staging`, and `Custom(RelayMap)`. Build a custom list with `RelayMode::custom(urls)` at endpoint.rs:2031.
- **Disabled:** `From<RelayMode>` at endpoint.rs:155-172 maps `Disabled` to no relay transport.
- **Relay-only:** `Builder::clear_ip_transports()` at endpoint.rs:510 removes the IP transports and leaves relay. Pair it with `relay_mode(RelayMode::custom(...))`. Read from code only, not run.
- **ALPN:** `Builder::alpns(Vec<Vec<u8>>)` at endpoint.rs:546. The runtime form is `Endpoint::set_alpns` at endpoint.rs:984. The first matching ALPN wins. `Router::spawn` overwrites this list (protocol.rs:522), so do not set both.
- **Starting preset:** `Builder::empty()` (endpoint.rs:193) starts with relay disabled and IP transports on. `presets::Minimal` (presets.rs:62-77) sets only the crypto provider. `presets::N0` (presets.rs:116-137) adds n0 DNS discovery and n0 relays. `presets::Empty` fails at bind without a crypto provider (presets.rs:27-30).

**2. Router and handler.**

- **Several ALPNs:** call `RouterBuilder::accept(alpn, handler)` once per ALPN (protocol.rs:495). Create the builder with `Router::builder(endpoint)` (protocol.rs:412). Dispatch picks the handler by the connection's ALPN (protocol.rs:653).
- **Registration order:** `spawn()` (protocol.rs:512) sets the endpoint ALPN list from the registered ALPNs in call order (protocol.rs:522). Register the preferred protocol first.
- **Duplicate ALPN:** `ProtocolMap::insert` (protocol.rs:391-394) appends the ALPN to the list again and overwrites the handler. No error is raised. The last registration wins.
- **Smallest handler:** a type implementing `ProtocolHandler` with one required method, `fn accept(&self, connection: Connection) -> impl Future<Output = Result<(), AcceptError>> + Send` (protocol.rs:273-276). The trait requires `Send + Sync + Debug + 'static` (protocol.rs:228). `on_accepting` (protocol.rs:248-256) and `shutdown` (protocol.rs:284-286) have defaults. The blanket conversion at protocol.rs:317 lets `accept(alpn, MyHandler)` take the type directly.

**3. Keys.**

- **Algorithm:** Ed25519. `PublicKey` wraps `CompressedEdwardsY` (iroh-base/src/key.rs:30). `SecretKey` wraps the ed25519-dalek `SigningKey` (key.rs:261). `EndpointId` is a type alias for `PublicKey` (key.rs:70). iroh-base pins `ed25519-dalek >=3.0.0-rc.0,<4.0.0` (iroh-base/Cargo.toml:21). The tree already has 3.0.0 (brief), so no new signature crate is needed.
- **Sign:** `SecretKey::sign(&self, msg: &[u8]) -> Signature` (key.rs:323).
- **Signature bytes:** `Signature::to_bytes(&self) -> [u8; 64]` (key.rs:460). `Signature::from_bytes(&[u8; 64])` (key.rs:465). `TryFrom<&[u8]>` (key.rs:445) is the fallible form.
- **Verify:** `PublicKey::verify(&self, message: &[u8], signature: &Signature) -> Result<(), SignatureError>` (key.rs:134). It calls `verify_strict` (key.rs:136). Strict verification rejects some signatures and keys that plain verification accepts. Check this against the spec's word "verifies".
- **Seed:** `SecretKey::from_bytes(&[u8; 32])` (key.rs:337) takes the Ed25519 seed. `SecretKey::to_bytes` (key.rs:332) returns it.
- **Public from secret:** `SecretKey::public` (key.rs:299). `PublicKey::from_bytes(&[u8; 32])` (key.rs:122) rejects bytes that are not a curve point.
- **Text forms emitted:**
  - `Display` for `PublicKey` writes 64 lowercase hex characters (key.rs:221-223). `Debug` writes `PublicKey(<hex>)` (key.rs:211-218).
  - `to_z32` writes z-base-32 (key.rs:164). Its alphabet is at key.rs:21, `ybndrfg8ejkmcpqxot1uwisza345h769`. This is not RFC 4648 base32.
  - `SecretKey` has no `Display`. `Debug` writes `SecretKey(..)` (key.rs:263-267).
- **Text forms parsed:** `PublicKey::from_str` (key.rs:249) and `SecretKey::from_str` (key.rs:269) both call `decode_base32_hex` (key.rs:475-498). It accepts 64 hex characters, or unpadded RFC 4648 base32 in either case. It does not accept z-base-32. For z-base-32 use `PublicKey::from_z32` (key.rs:169).
- **Postcard:** when the format is not human-readable, `PublicKey` serializes as its raw 32 bytes (key.rs:78-87). `Signature` serializes as a 64-element tuple (key.rs:378-392). Both are raw with no length prefix. A postcard round-trip test for `Signature` exists at key.rs:557-564. These match the `[u8; 32]` and `[u8; 64]` fields of spec 3.4.
- **Fit with spec 3.1:**
  - Ed25519 keys, 32-byte public key, 32-byte seed, and 64-byte signature all match the types above.
  - The spec's card public key text is lowercase base32, unpadded, 52 characters. iroh's `Display` emits hex (64 characters) instead. `from_str` parses unpadded RFC base32, but iroh never emits it. Encoding must be written by hand with the data-encoding crate's `BASE32_NOPAD`, lowercased. Data-encoding is already in the tree (brief).
  - The `to_z32` output is a different alphabet from RFC base32. Do not use it for the spec's text form.
  - The sidecar secret is 64 hex characters plus a newline. `SecretKey::from_str` does not trim. By the length check at key.rs:484-485, a 65-character input fails. Trim first, or decode the hex and call `from_bytes`. Read from code only, not run.
  - Serde under a human-readable format writes `PublicKey` as the `Display` hex (key.rs:78-87). A JSON encoding built with serde will therefore carry hex, not base32. Spec 3.1 says JSON is the local encoding.
- **Answer to "could these serve as the card key with no separate signature crate":** the types cover the Ed25519 keys, signing, verification, and fixed-size encodings the spec names. Three things need writing by hand: the base32 text form, the sidecar hex parse, and any JSON form of the card key. Verification uses `verify_strict`. Depending on iroh-base is already implied by depending on iroh.

**4. Accepted connection: remote endpoint id.**

- **Type:** the handler's `accept` receives a `Connection` (protocol.rs:273-276). `Connection<HandshakeCompleted>` is the default state.
- **Method:** `Connection::remote_id(&self) -> EndpointId` at iroh/src/endpoint/connection.rs:1167. It sits in `impl Connection<HandshakeCompleted>` (connection.rs:1153). It is infallible.
- **Source of the value:** the id is set during the handshake by `static_info_from_conn` (connection.rs:370). That calls `remote_id_from_noq_conn` (connection.rs:383-410), which reads the single TLS peer certificate and converts it to an endpoint id. The value does not come from client bytes.
- **Spec 3.6 step 4:** compare `connection.remote_id().as_bytes()` (key.rs:111, returns `&[u8; 32]`) with `from.node`.
- **Not this path:** `remote_id` at connection.rs:1269 and 1311 returns `Result`. Those belong to the 0-RTT states, not to the accept path.

## Not read

- Local network discovery, which spec 3.6 requires. Not checked.
- Relay-only behavior at runtime. Read from code only.
- The raw `Endpoint::accept` path that bypasses the Router. Not read.
- `IncomingFilter` (protocol.rs:214). Not checked against the spec.
- iroh-relay internals, net report, and portmapper. Out of scope.
- Spec 3.4 Probe and Introduce fields beyond the Claim. Out of scope.
- No compile, no test run.
