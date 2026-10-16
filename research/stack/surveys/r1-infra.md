# R1 infrastructure: self-hosted relays and bootstrap nodes (rayfish, mshr)

Date: 2026-10-16.

## Binding

Bound to cargo-cult-science and stop-yapping, read in full from `.claude/manifesto-repo/LLM_MANIFESTOS/manifestos/`.
I must report what the code does, with citations, and I will not present a README as evidence.
I must give the disconfirming facts too, and I will record what contradicts a spec decision as well as what agrees.
I must answer tersely, and I will cut filler from every section.

## Sources read

- Brief: `research/stack/surveys/brief.md`.
- Spec: `spec/blueprint.md` D14 (201-206), D15 (207-208), D43 (387-391), 3.3 network configuration file (437-466), 3.14 (825-843).
- Relay foundation report, not repeated: `research/stack/surveys/f3-relay.md`.
- rayfish clone `/tmp/ra-src/rayfish`, commit be3e39e8336d46dcbf95b0e8d63f5918c263e97a (2026-10-15).
- mshr clone `/tmp/ra-src/mshr`, commit c00b4b0be417c40117d57c95f53a9f1221d296a5 (2026-10-10).

## rayfish (`/tmp/ra-src/rayfish`, be3e39e, iroh 1.3.0 via git fork)

### Summary

- No relay server in this repo. No `server` feature on `iroh-relay`, no `iroh_relay::server` use, no relay deploy script.
- Default relays: n0's public set. `RelayMode::Default` (`/tmp/ra-src/iroh/iroh/src/endpoint.rs:2012`) when the user has set nothing.
- Optional preset: `relay = rayfish`, which resolves to `http://relay.iroh.rayfish.xyz:3340` (`src/config.rs:346`). The host is operated outside this repo.
- Bootstrap: an invite code carries the coordinator's EndpointId. A pkarr DNS record carries a seed peer list. No config-file bootstrap list.
- Deployment: one daemon process (`ray daemon`) under systemd. No docker image for the relay or the coordinator.
- TLS for relays: none configured by rayfish. The preset is plain HTTP.

### Relay: own or n0's (`src/config.rs:325-385`, `src/transport.rs:520-537`)

- `AppConfig::default()` sets `relay: ServerOverride::default()` (`src/config.rs:716`). An unset relay keeps iroh's N0 preset.
- `build_relay_mode` returns `None` when unset (`src/transport.rs:524-527`). The endpoint then gets the N0 default.
- Setting `relay` replaces the N0 set only in `replace` mode. Otherwise n0's URLs are appended (`src/transport.rs:532-535`).
- The keyword `rayfish` expands to `RELAY_PRESET_RAYFISH` (`src/config.rs:346, 363-366`). Any other entry must be an `http` or `https` URL (`src/config.rs:333-340`).
- Set through `ray config set relay ...`, key `relay` (`ray-proto/src/settings.rs:80`). Stored in `settings.toml` (`src/config.rs:803`).
- The relay is applied at endpoint bind (`src/transport.rs:338-340`). A change needs a daemon restart (`src/main.rs:1951`).

### Relay: embedded or separate (`src/transport.rs`)

- Separate. The daemon only dials relays. It never serves one.
- Rayfish's `tests/e2e/README.md:92-96` says the containers reach "pkarr and the relays" over the host's NAT. The e2e rig uses the public internet, not a private relay.

### Bootstrap peers (`src/invite.rs:1-16, 128-139`; `src/dht.rs:1-16, 70-95`; `src/daemon/network_registry.rs:1218-1234`)

- Invite code: `bs58(network_pubkey || coordinator || secret || checksum)`. The joiner dials the coordinator's EndpointId directly.
- The coordinator is the only node that burns invites. Invites are single-use with expiry (`src/invite.rs:1-16`).
- Member restart and reconcile: the pkarr record `_rayfish` under the network key. It holds the group blob hash and a seed peer list (`src/dht.rs:70-95`, `:216-247`).
- Seed list contents: connected peers of the network, plus the publishing node's own id, sorted and de-duplicated (`src/daemon/network_registry.rs:1225-1233`).
- Publishing: only the coordinator holds the network secret key and publishes (`src/dht.rs:1-4`).
- Restore: the comment at `src/daemon/network_registry.rs:217` says a member network restore needs the pkarr lookup. The call site was not traced.
- Discovery server: `DISCOVERY_PRESET_RAYFISH = http://dns.iroh.rayfish.xyz:8080` (`src/config.rs:347`). Default when unset is `https://dns.iroh.link/pkarr` (`src/dht.rs:17`).
- Local discovery: mDNS, on by default (`src/config.rs:717`).

### Deployment shape

- One process: `ray daemon` (`src/main.rs:310`). Runs the TUN device, IPC socket, endpoint, and coordinator logic together.
- systemd unit: `contrib/rayfish.service:1-15`. `ExecStart=/usr/local/bin/ray daemon`, `Restart=on-failure`.
- Other init systems: `contrib/rayfish.init` and `rayfish.openrc`. macOS: `contrib/com.rayfish.vpn.plist`.
- Docker only in `tests/docker/Dockerfile` for the e2e fleet (systemd as PID 1, sshd). Not a deploy artifact.

### TLS

- Relay: no custom trust. `ca_tls_config`, `insecure_skip_verify`, and root stores do not appear in `src/` or `ray-proto/`. The preset is `http://`, so no TLS is used on the relay path (`f3-relay.md` §3: `http` scheme gives plain `ws`).
- pkarr: `ep.tls_config()` is reused for the pkarr client (`src/dht.rs:51-60`). The default URL is `https`.
- Name resolution for the relay: fixed public resolvers `1.1.1.1` and `8.8.8.8` appended to the control-plane nameserver list (`src/transport.rs:124-130, 296-311`).

### Maturity

- Last commit: 2026-10-15 (be3e39e, "docs: update changelog for 0.5.9 release"). Version 0.5.9.
- Tests for the mechanism: `src/config.rs:2658-2698` (relay URL expansion), `src/transport.rs:840-866` (augment vs replace), `src/dht.rs:349-365, 369-530` (record encode, decode, version, wrong key). None cover a running relay.

### What estafette could take

- Pattern: the pkarr record for a seed list. It is a DNS-carried bootstrap source. Against D14 (below).
- Pattern: the augment-or-replace relay override (`build_relay_mode`). Keeps n0 as fallback by default. Estafette's D14 has no equivalent.
- Pattern: resolving the relay's own name against a fixed public resolver list, not the host's resolv.conf (`src/transport.rs:296-311`). Relevant to a relay behind a dead host DNS.
- Nothing: relay server code. Rayfish has none to copy.

### Against the spec

- **D14, rejected alternative.** D14 rejects "membership lookup in a public DHT" as "a third-party dependency with a network reach requirement." Rayfish uses a pkarr record on `dns.iroh.link` by default, and on its own host when configured, and, on restore of a member network, through the pkarr lookup named at `src/daemon/network_registry.rs:217` (call site not traced; `src/dht.rs:17, 216-247`). The evidence bears on the rejection's stated cost: rayfish takes that dependency, and its own docs call the record the seed list. Recorded, not argued.
- **D14, bootstrap source.** D14 puts the bootstrap in the network configuration file as a node id list (3.3 `bootstrap = [...]`). Rayfish puts the coordinator in the invite code and the seed list in DNS. No config-file bootstrap list. Recorded.
- **D43, one operator command.** Rayfish has no single infrastructure command. The coordinator is a `ray` daemon on a machine that holds the network key (`ray invite`, `src/main.rs:377`). The relay is not run by the project from this repo. Recorded.
- **3.3 relay URL.** The spec example is `relay = "https://relay.example"`. Rayfish's preset is `http://` (`src/config.rs:346`), so the example has no rayfish counterpart. Recorded.
- **D15, local discovery.** D15 says nodes find each other on the LAN. Rayfish turns mDNS on by default (`src/config.rs:717`). Agrees.
- **3.14, relay in process.** Rayfish runs no relay in process. Against the 3.14 embedded relay plus endpoint design: no evidence either way from rayfish, which takes the relay from elsewhere.

## mshr (`/tmp/ra-src/mshr`, c00b4b0, iroh 1.3, crate 0.8.46)

### Summary

- Library only. No binary, no Dockerfile, no systemd unit. The consuming daemon (yubaba) is not in this repo.
- Embeddable relay: `mshr::relay::Server`, built on iroh-relay's `server` feature (`crates/mshr/Cargo.toml:21`).
- Default relays: n0's, through `Seeds::defaults()`. A bare `Endpoint` gets no relay at all.
- Bootstrap: pinned seeds in `mshr://<node-id>?addr=...&relay=...` form, from the caller or env (`YAH_XLB_SEED`). No config file.
- TLS: mandatory on the relay. Three modes: self-signed, Let's Encrypt via ACME, or a caller-supplied rustls config.

### Relay: own or n0's (`crates/mshr/src/seeds.rs:244-330, 497-505`; `crates/mshr/src/endpoint.rs:419-430`)

- Default: `RelayChoice::Default`, which resolves to `RelayMode::Default` (n0's relay map). `seeds.rs:309-311`.
- Override: `RelayChoice::Custom(urls)` replaces the default. It does not extend it (`seeds.rs:249-253`). Test `seeds_round_trip.rs:252-270` checks that no n0 URL survives.
- Off: `RelayChoice::Disabled` (spelled `none`), giving no relay map (`seeds.rs:250, 497-505`).
- Bare endpoint: `endpoint.rs:421-423` maps a missing relay map to `RelayMode::Disabled`. An endpoint built without `Seeds::apply` has no relay transport. The README quickstart (`crates/mshr/README.md:44-56`) builds exactly that: no `.relay_map(...)` call. The quickstart call does not match the code's API. It calls `Endpoint::builder(keypair, &["myapp/v1"])`. The real entry is `Endpoint::builder()` with `.keypair()` and `.alpns()` (`endpoint.rs:506-508, 393, 400`).
- Setting the lane through `Seeds::apply` or `YAH_XLB_RELAY` takes effect at bind. The flag `--xlb-relay` appears only in a test comment (`seeds_round_trip.rs:252-256`); mshr defines no CLI.

### Relay: embedded or separate (`crates/mshr/src/relay.rs:1-30, 255-329`)

- Embedded as a type. `relay::Server::builder().start()` spawns `iroh_relay::server::Server` in the calling process (`relay.rs:325-327`).
- The builder is a library call, not a binary. No mshr command starts a relay. The consumer decides where it runs.
- One process hosts HTTPS (relay WebSocket), QUIC address discovery, and an HTTP probe listener. The HTTP listener defaults to `127.0.0.1:0` (`relay.rs:206-212`). The doc says production should pin port 80.
- The relay shares one cert across HTTPS and QUIC. QUIC takes the relay's TLS config when none is given (see f3 §2).

### Bootstrap peers (`crates/mshr/src/seeds.rs:1-50, 112-200, 325-420`; `crates/mshr/src/discovery.rs:101-118, 194-222`)

- Three lanes, each its own knob (`seeds.rs:1-30`): pkarr (resolve a bare NodeId), relays (NAT-traversal relay), pinned (direct addresses).
- Pinned seeds: `YAH_XLB_SEED`, repeatable (`seeds.rs:72-74`). URL form `mshr://<node-id>?addr=<ip:port>&relay=<url>` (`seeds.rs:158-200`).
- A bare NodeId is a legal seed but needs the pkarr lane to resolve (`seeds.rs:91-100, 144`).
- Config file: none. The identity file lives at `ProjectDirs::from("dev","yah","yah").data_local_dir()` (`keypair.rs:4, 98-101`). Seeds come from the caller and env only.
- Precedence: explicit argument, then environment, then default (`seeds.rs:43-47`). Each knob resolves on its own.
- Replacement rule: a URL override replaces the default (`seeds.rs:49-52`). Pinned seeds are additive (`seeds.rs:52`).
- Pkarr: `default_relays()` returns n0's pkarr relay (`discovery.rs:108-111`). `Discovery::with_relays` sets the pkarr URL list, not the transport relay (`discovery.rs:194-208`).

### Deployment shape

- None in the repo. `find` for Dockerfile, `*.service`, compose files, and container manifests returned nothing.
- CI: `.github/workflows/release.yml` is named in the workspace notes (`Cargo.toml:15-20`) but is not in this clone. The ACME test is `#[ignore]` and needs `PEBBLE_BIN` and `PEBBLE_CA_CERT`. CI wiring is marked "follow-up" (`tests/relay_acme_pebble.rs:10-17`).

### TLS (`crates/mshr/src/relay.rs:106-175, 231-305`; `crates/mshr/src/endpoint.rs:324-330, 427-430`)

- Self-signed: `tls_self_signed()` uses iroh-relay's `testing` helper (`relay.rs:272-281`). Clients need `insecure_skip_tls_verify(true)`.
- ACME: `tls_letsencrypt(AcmeConfig)` with `production()`, `staging()`, or `custom(url)`. Domain and contact required. `cache_dir` optional (`relay.rs:106-175`). Challenges run on the HTTPS port (`relay.rs:236-238`).
- Manual: `tls_manual(rustls::ServerConfig)`. Caller owns certs and reload (`relay.rs:245-249`).
- `start()` errors when no TLS mode is set (`relay.rs:257-260`). A plain-HTTP relay is not offered. Compare f3 §2, where iroh allows `tls: None`.
- Client insecure mode: `insecure_skip_tls_verify` calls `CaTlsConfig::insecure_skip_verify()` (`endpoint.rs:428-430`). That constructor is compiled only with `cfg(any(test, feature = "test-utils"))` in iroh-relay (`iroh-relay/src/tls.rs:92-96`).
- Leak: mshr enables iroh-relay's `test-utils` unconditionally (`crates/mshr/Cargo.toml:21`). So the constructor is compiled into every mshr build. The endpoint call at `endpoint.rs:428` is outside any test `cfg` (only `endpoint.rs:814` is). The README (`README.md:193-195`) says the self-signed constructor "may move behind a `test-utils` feature flag" so production builds skip the fixtures. Today it does not.

### Maturity

- Last commit in the clone: 2026-10-10, "export: mshr snapshot" (c00b4b0). Crate 0.8.46.
- Tests on this mechanism: `tests/relay_round_trip.rs` (self-signed relay, no `#[ignore]`); `tests/seeds_round_trip.rs:252-285` (custom relay replaces default, runs by default); `tests/seeds_round_trip.rs:199` (`#[ignore]`, needs public internet); `tests/relay_acme_pebble.rs:93` (`#[ignore]`, needs Pebble).
- No test covers the ACME path under CI.

### What estafette could take

- Pattern: the three-lane split (pkarr, relay, pinned), with each knob resolved on its own. Estafette's D14 has one ticket. Splitting it would match mshr's stated reason.
- Pattern: `RelayChoice` with `Default`, `Disabled`, `Custom`. "Custom replaces, never extends" is a rule D14 does not state.
- Pattern: the `mshr://<node-id>?addr=...&relay=...` string. It survives a command line, an env var, and a systemd `Environment=` line without escaping. D14 names a ticket and 3.3 lists bare node ids, so the ticket string form is unspecified.
- Pattern: `relay::Server` as a builder with three TLS modes (self-signed, ACME, manual) and `https_url()` / `relay_map()` getters. Compare 3.14.
- Crate: `iroh-relay` with `server` and `tls-ring`, pulled in by mshr at `crates/mshr/Cargo.toml:21`. Do not copy the `test-utils` flag. It leaks into builds, as shown above.
- Nothing: deployment. mshr has no deploy artifact.

### Against the spec

- **D14, bootstrap node.** mshr has no stable infrastructure node. Bootstrap is a list of pinned seeds the operator supplies. D14 requires "a node with a stable key that joins the topic and announces nothing." mshr's pinned seeds carry node ids but no node runs for them. Recorded.
- **D14, rejected alternative.** D14 rejects "Membership lookup in a public DHT." mshr's default pkarr lane does exactly that: n0's pkarr relay for bare NodeIds (`discovery.rs:108-111`, `seeds.rs:315-318`). Recorded.
- **D15, local discovery.** D15 says nodes find each other on the LAN with no configuration. mshr's README enables the LAN lane explicitly (`crates/mshr/README.md:49-50`, `with_lan()`). Recorded.
- **D43, one operator command.** mshr provides no command. The consumer must build the relay. Recorded.
- **3.14, relay in process.** Consistent. mshr's `relay::Server` runs in-process, as 3.14 specifies, but as a library call. Recorded.

## Cross-project observations

- **No project runs a relay from its own binary.** Rayfish runs none. mshr exposes one as a library type. Neither ships a relay binary or deploy file. Evidence: rayfish `Cargo.toml` (no `server` feature); mshr `crates/mshr/src/relay.rs`.
- **Both use n0's relays by default.** Rayfish: `src/transport.rs:524-527`. mshr: `crates/mshr/src/seeds.rs:309-311`. Both fall back to n0 for NAT traversal and pkarr. D14 says nothing about n0.
- **Both override by replacement, with an augment option only in rayfish.** Rayfish `replace` flag (`src/transport.rs:532-535`). mshr replaces always (`seeds.rs:249-253`).
- **Both use a pkarr record or lane for NodeId resolution.** Rayfish: `_rayfish` record with seed list (`src/dht.rs:70-95`). mshr: pkarr lane (`discovery.rs:194-208`). Both use a third-party DHT service by default. D14 rejects this.
- **Plain HTTP differs.** Rayfish preset is `http://` (`src/config.rs:346`). mshr's server builder refuses to start without TLS (`relay.rs:257-260`), so mshr never serves plain HTTP.
- **Bootstrap ticket shapes differ.** Rayfish: `bs58` invite code carrying the coordinator id (`src/invite.rs:128-139`). mshr: `mshr://` URL carrying a node id and optional addresses (`seeds.rs:158-200`). Neither reads a config file for seeds.

## Not read

- rayfish: `src/daemon/mesh/runtime.rs` and `src/daemon/mesh/reconverge.rs` beyond the publish call. The full pkarr resolve path (`src/dht.rs:216-260`) was seen only through grep.
- rayfish: `src/cli/` command bodies. `ray invite`, `ray join`, and `ray up` were located by enum, not traced.
- rayfish: `ray-mobile`, `ray-apple`, `ray-windows` deploy paths.
- mshr: `src/lan/` (mDNS and DNS-SD lanes), `src/discovery.rs:119-411` beyond the public API, `src/endpoint.rs` beyond the relay and TLS builder.
- mshr: the release workflow. `.github/workflows/` is absent from the clone. The workspace notes name it.
- Neither: iroh-relay's own `main.rs` config loader. f3 covers the server API.
- Downstream consumers (yubaba, noisetable) are not in either clone and were not read.
