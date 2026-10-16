# F3: embedded iroh relay server

Date: 2026-10-16.

## Sources read

- iroh repo at /tmp/ra-src/iroh, commit 0072d7d84b233f9e7185eb676f049beaf557ac03. iroh-relay and iroh are both 1.3.0.
- iroh-relay/Cargo.toml:129-177 (features, `[[bin]]` required-features).
- iroh-relay/src/server.rs:36-71, 100-172, 425-615, 617-700, 691-905 (config types, Server, spawn, shutdown/join).
- iroh-relay/src/server/testing.rs (whole file, 87 lines).
- iroh-relay/src/quic.rs:9-11, 97-112, 207-245.
- iroh-relay/src/relay_map.rs:163-215, 232-310.
- iroh-relay/src/client.rs:272-275; client/tls.rs:96-104.
- iroh-relay/src/main.rs:375-377, 566-612, 760-800.
- iroh/src/endpoint.rs:568, 720-735, 1993-2050.
- iroh/src/test_utils.rs:45-85; iroh/src/net_report.rs:962-985; iroh/tests/patchbay/util.rs:495-530; iroh/Cargo.toml:36, 124, 153.
- noq-proto 1.3.0 (cargo registry): src/transport_parameters.rs:404, 522, 727; src/frame.rs:195.
- spec/blueprint.md: D14 (lines 201-206), D15, D43 (387-391), 3.14 (825-843), 3.15 (845-870, test list only).

## 1. Server feature and crate delta

Feature name: `server` on the `iroh-relay` crate (iroh-relay/Cargo.toml:133). The `iroh` crate does not forward it. Its `test-utils` feature turns on `iroh-relay/server` (iroh/Cargo.toml:153), so pulling in the server through `iroh` is only possible with the test helper set.

Measured in /tmp/ra-src/relay-probe-f3, a path dependency on the local iroh-relay, toolchain 1.99.1, `cargo tree --prefix none -e normal`:

| Build | Lead's command (`sort -u \| wc -l`) | Distinct name and version |
|---|---|---|
| default features | 257 | 199 |
| `server` | 344 | 270 |
| `server` + `test-utils` | not counted raw | 270 |

The lead's command overcounts. Repeated subtrees carry a `(*)` marker, which makes duplicate lines that `sort -u` keeps. The honest delta is 71 distinct crates. The raw delta is 87. Both counts include the probe root and resolve only; nothing was compiled.

Notable crates the server feature adds: clap, toml, serde_json, tracing-subscriber, dashmap, rcgen, time, x509-parser, tokio-rustls-acme, tokio-websockets, sha1, simdutf8, reloadable-state, rustls-platform-verifier, rustls-cert-reloadable-resolver, and iroh-metrics/service. The `server` feature also sets `noq/platform-verifier`.

The probe crate is `/tmp/ra-src/relay-probe-f3`, a new directory. The existing `/tmp/ra-src/relay-probe` has no Cargo.toml and holds other probe files, so it was left alone.

## 2. Server API

- Entry: `iroh_relay::server::Server::spawn(ServerConfig) -> Result<Server, SpawnError>` (server.rs:691). `shutdown(self)` at server.rs:878, `join(&mut self)` at server.rs:900.
- `ServerConfig { relay: Option<RelayConfig>, quic: Option<QuicConfig>, metrics_addr: Option<SocketAddr> }` (server.rs:111). Both `relay` and `quic` are optional, so a QUIC-only or relay-only server is possible.
- `RelayConfig::new(http_bind_addr)` (server.rs:155). Fields: `tls: Option<TlsConfig>`, `limits`, `key_cache_capacity`, `access: Arc<dyn DynAccessControl>` (default `AllowAll`).
- Bind address, plain HTTP: with `tls: None`, all relay HTTP services serve on `http_bind_addr` (server.rs:127-137). Plain HTTP is allowed for the relay.
- TLS: `TlsConfig::new(https_bind_addr, CertConfig)` (server.rs:477). `CertConfig::Manual { server_config: rustls::ServerConfig }` or `CertConfig::LetsEncrypt { acme_config, server_config_builder }` (server.rs:527-546).
- ACME: `AcmeConfig::new(directory_url)`, `::letsencrypt(production)`, `.domains(..)`, `.contact(..)`, `.cache_path(..)` (server.rs:548-605). ACME needs real domains and a reachable directory. It is not a test option.
- QUIC: `QuicConfig::new(bind_addr)` (server.rs:449) with `server_config: Option<rustls::ServerConfig>`. If unset, it falls back to the relay TLS config (server.rs:846-848). If neither exists, spawn fails with `TlsNotConfigured` (quic.rs:42).
- QUIC address discovery (QAD): ALPN `/iroh-qad/0` (quic.rs:10, 102). The server sends observed-address reports with `send_observed_address_reports(true)` (quic.rs:111). The handler only accepts the connection and waits for the client to close it (quic.rs:207-245). The observed address is a QUIC-layer frame (noq-proto `ObservedAddr`, frame.rs:195), not a payload the relay writes itself.
- QAD requires TLS. QUIC cannot run without a certificate, so plain-HTTP relay plus QAD needs a TLS config on `QuicConfig.server_config`. A plain-HTTP relay with no QUIC gives no QAD.
- Test helpers: `iroh_relay::server::testing` (server.rs:70-71). Gated by `test-utils`, not `server`. `self_signed_tls_certs_and_config()`, `tls_config()`, `relay_config()`, `quic_config()`, `server_config()` (testing.rs:80-86). All bind to 127.0.0.1 or 0.0.0.0 on port 0. Self-signed for localhost, 127.0.0.1, ::1.

Discrepancy: testing.rs:78 says "QUIC addr discovery is disabled" for `server_config()`. Line 83 sets `quic: Some(quic_config())`, so QAD is enabled. The code is the evidence; the doc comment is wrong.

## 3. Pointing an endpoint at a custom relay

- `RelayMode` (iroh/src/endpoint.rs:1993-2005): `Disabled`, `Default`, `Staging`, `Custom(RelayMap)`.
- `RelayMode::custom(urls)` (endpoint.rs:2031) builds the map from `RelayUrl`s. `RelayMode::Custom(map)` takes a full map.
- The endpoint builder takes it via `.relay_mode(RelayMode)` (endpoint.rs:568).
- `RelayMap::from(RelayConfig)`, and `RelayConfig::new(url, Option<RelayQuicConfig>)` (relay_map.rs:250). `RelayQuicConfig::new(port)` (relay_map.rs:299). The `From<RelayUrl>` default sets QUIC to `RelayQuicConfig::default()`, which is port 7842 (relay_map.rs:282-307, defaults.rs:7).
- Scheme: the client uses plain `ws` when the URL scheme is `http` or `ws` (client.rs:272-275, client/tls.rs:100-102). So `http://` relay URLs work with no TLS.
- Trust for a self-signed relay: the client uses `ca_tls_config(CaTlsConfig)` (endpoint.rs:731). `CaTlsConfig::insecure_skip_verify()` is gated behind `cfg(test)` or `test-utils` (iroh-relay/src/tls.rs:92-96). Iroh tests use it (iroh/src/endpoint/connection.rs:1601, 1609). Production trust needs custom roots or a real certificate.

## 4. The iroh-relay binary and embedding

- `main.rs:566-612`: `#[tokio::main]`, install ring provider, `Cli::parse()`, `Config::load`, check that QAD requires TLS (main.rs:585), `--dev` switches to plain HTTP (main.rs:588-595), `build_relay_config(cfg).await` (main.rs:602), `relay::Server::spawn(relay_config).await` (main.rs:603), then `tokio::select!` on ctrl-c or `relay.join()`, and `relay.shutdown().await`.
- `build_relay_config` (main.rs:760-790) fills `ServerConfig` from the file. It sets `relay` via `RelayConfig::new`, `quic`, and metrics.
- Binary defaults: QAD off (`enable_quic_addr_discovery` returns false, main.rs:375-377). Relay on. The binary is compiled only with `server` (Cargo.toml:173-176).
- Embedding example: iroh/src/test_utils.rs:45-85 builds `ServerConfig` with a `Manual` self-signed cert, `QuicConfig::new((LOCALHOST, 0))`, spawns, reads `https_addr()` and `quic_addr()`, and returns a `RelayMap` built with `RelayConfig::new(url, RelayQuicConfig::new(port))`. iroh/tests/patchbay/util.rs:495-530 does the same with fixed ports and the relay URL `https://relay.test`.
- Spec mapping: D43 and 3.14 need one process that runs the relay and the bootstrap endpoint and prints the ticket. The binary's `main` does not host an endpoint. Embedding means reproducing the `main` flow in estafette with `Server::spawn` and an iroh endpoint.

## Cross-project observations

- The spec and the repo both give relay and QAD separate configs. QAD needs TLS in every reading. Plain HTTP relay plus QAD therefore needs a certificate. The spec does not say which relay URLs or certificates D14 uses. Not decided here.
- The relay's `server` feature pulls in TLS, ACME, and metrics code with no per-part switches. The only subset switch is `metrics`.

## Not read

- iroh-relay/src/server/http_server.rs, clients.rs, client.rs, streams.rs, resolver.rs, metrics.rs (behavior of the relay protocol, access checks, and rate limits).
- main.rs Config parsing and TOML schema (main.rs:92-365) and build_relay_config TLS and limit branches (main.rs:620-760), except the parts above. The CLI flags in main.rs:47-64 were not read in detail.
- Server ACME runtime path (server.rs:700-790) beyond the config types.
- The full client-side QUIC path (quic.rs:262-380) beyond the observed-address call.
- Compile check. The probe resolves dependencies only; it does not build the crates.
- The spec sections D15 and the other 3.15 scenarios beyond the lines needed for D14, D43, and 3.14.
