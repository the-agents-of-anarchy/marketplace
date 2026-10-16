# Test harness, shallow

Date: 2026-10-16. Scope: iroh 1.3.0 and iroh-gossip 0.101.0 test facilities. One pass, no evaluation.

Sources read:
- iroh clone `/tmp/ra-src/iroh`, commit `0072d7d84b233f9e7185eb676f049beaf557ac03`: `iroh/Cargo.toml`, `iroh/src/lib.rs`, `iroh/src/test_utils.rs`, `iroh/src/test_utils/test_transport.rs`, `iroh/src/test_utils/qlog.rs` (head), `iroh/src/endpoint.rs` (builder methods, `RelayMode`, tests at 2600-2640, 3465-3475), `iroh/src/endpoint/presets.rs`, `iroh/src/endpoint/connection.rs` (1596-1612), `iroh/src/address_lookup/pkarr.rs` (170-180, 520-530), `iroh/tests/integration.rs`, `iroh/tests/patchbay.rs` (head), `iroh/tests/patchbay/util.rs` (head).
- iroh-gossip clone `/tmp/ra-src/f2-gossip`, commit `2ce78afe09d89d41d123f28eac19bdc831609cc8`: `Cargo.toml`, `src/proto.rs`, `src/proto/sim.rs` (head and API signatures), `src/bin/sim.rs` (CLI), `src/net.rs` (test helper and test names), `tests/sim.rs`, `simulations/all.toml` (head).
- `gh repo list n0-computer` filtered by name, and `gh repo list` filtered for network-lab names.
- Relay internals are not repeated here. See `research/stack/surveys/f3-relay.md`.

## Facilities

| # | Facility | Crate, feature | Where | What it does |
|---|---|---|---|---|
| 1 | `test-utils` feature | iroh, `test-utils` | `iroh/Cargo.toml:153`; `iroh/src/lib.rs:305-306` | Gates the `iroh::test_utils` module. Enables `iroh-relay/test-utils`, `iroh-relay/server`, and optional deps `axum`, `simple-dns`. |
| 2 | `run_relay_server`, `run_relay_server_with`, `run_relay_server_with_access` | iroh, `test-utils` | `iroh/src/test_utils.rs:34`, `:44`, `:51` | Starts an in-process relay on a random loopback port with self-signed TLS and QUIC on by default. Returns `(RelayMap, RelayUrl, Server)`. Dropping the `Server` stops it. The access variant takes a custom `DynAccessControl`. |
| 3 | `DnsPkarrServer` | iroh, `test-utils` | `iroh/src/test_utils.rs:83` (module), `:105` (struct), `:140` (`preset`) | In-process DNS server and Pkarr relay for address-lookup tests. `preset()` returns a `Preset` that installs DNS lookup and Pkarr publisher on an endpoint. `dns_resolver()` returns a resolver pointed at the server. |
| 4 | `TestNetwork`, `TestTransport`, `TestNetwork::create_transport` | iroh, `test-utils` plus `unstable-custom-transports` | `iroh/src/test_utils.rs:17-18` (gate); `iroh/src/test_utils/test_transport.rs:43` (transport), `:86` (network), `:106` (`create_transport`) | In-memory custom transport. Endpoints in one process exchange packets over channels keyed by `EndpointId`. `address_lookup()` returns a lookup for the same network. `create_transport` errors if the id already exists. |
| 5 | `TestTransport` as a `Preset` | iroh, same as row 4 | `iroh/src/test_utils/test_transport.rs:49-70` (impl), `:379-400` (test builder, calls `clear_ip_transports` at `:400`) | Applies the transport and the network's address lookup to an endpoint builder in one step. |
| 6 | `QlogFileGroup` | iroh, `test-utils`; output needs `qlog` | `iroh/src/test_utils.rs:14` (re-export); `iroh/src/test_utils/qlog.rs:36` (`from_env`), `:45` (`new`), `:67` (`create`); `iroh/Cargo.toml:156` (`qlog`) | Writes one QUIC qlog file per named endpoint into a directory, or from an env var. Without the `qlog` feature the code path is a no-op (`qlog.rs:46`, `:68`). |
| 7 | Several endpoints in one process | iroh, no feature beyond dev | `iroh/src/endpoint.rs:2600-2640` (`endpoint_two_relay_only_no_ip`); `iroh/src/endpoint/connection.rs:1601`, `:1609` | Each endpoint is `Endpoint::builder(preset)`, with a secret key from a seeded `ChaCha8Rng`, `RelayMode::Custom(relay_map)`, `ca_tls_config(CaTlsConfig::insecure_skip_verify())`, then `.bind()`. The address passes between tasks over a `oneshot` channel. |
| 8 | Relay-only path | iroh, none | `iroh/src/endpoint.rs:510` (`clear_ip_transports`), `:517` (`clear_relay_transports`); tests at `:2618`, `:2662`, `:3471`, `:3580`, `:3660` | Removes IP transports from the builder, so the connection can only use the relay. `endpoint_two_relay_only_no_ip` panics if any reported path is IP (`:2600-2640`). |
| 9 | Address lookup disabled | iroh, none | `iroh/src/endpoint.rs:596` (`clear_address_lookup`), `:616` (`address_lookup`) | `clear_address_lookup` removes every lookup service. `address_lookup` adds one. A dial then needs the address supplied directly. No test call site of `clear_address_lookup` found in iroh `src` or `tests`. |
| 10 | Empty and minimal presets | iroh, needs `tls-ring` or `tls-aws-lc-rs` | `iroh/src/endpoint/presets.rs:37` (`Empty`), `:59-77` (`Minimal`) | `Minimal` sets only the rustls crypto provider. It adds no relay and no address lookup. `Empty` adds nothing. |
| 11 | n0 preset | iroh, default crypto feature | `iroh/src/endpoint/presets.rs:113-140` (`N0`), `:175-181` (`N0DisableRelay`) | `N0` adds Pkarr publisher, Pkarr resolver, DNS lookup (outside browsers), and the default relays. `N0DisableRelay` is `N0` with `RelayMode::Disabled`. |
| 12 | `RelayMode` | iroh, none | `iroh/src/endpoint.rs:1993-2005` | `Disabled` turns off relay listen and dial. `Default` and `Staging` use n0 infrastructure. `Custom(RelayMap)` pins a relay set. |
| 13 | Loopback, ephemeral bind | iroh, none | `iroh/src/endpoint.rs:370` (`bind_addr`), `:450` (`bind_addr_with_opts`); test at about `:3465-3475` (`test_bind_addr_clear`) | Binds `(Ipv4Addr::LOCALHOST, 0)` after `clear_ip_transports`. Port 0 gives an OS-chosen port. |
| 14 | Linux netns lab (patchbay) | iroh, dev-dependency `patchbay = 0.7` with `iroh-metrics`, Linux only | `iroh/Cargo.toml:140-144`; `iroh/tests/patchbay.rs:27` (cfg `target_os = "linux"` and not `skip_patchbay`), `:58-59` (`ctor` user-namespace setup); `iroh/tests/patchbay/util.rs:12` (`Lab`, `Device`, `IpSupport`, `TestGuard`) | Builds a Linux network-namespace lab with devices, NAT, DNS, and uplinks. Tests then set up routes. |
| 15 | Patchbay test cases | iroh, row 14 | `iroh/tests/patchbay.rs:70` (`holepunch_simple`), `:99` (`run_add_faster_link`), `:193` (`run_link_outage_recovery`), `:249` (`run_hard_nat_to_holepunchable`), `:337` (`run_holepunch_many_addrs`); `iroh/tests/patchbay/relay.rs:43` (`run_relay_connect`), `:122` (`run_relay_udp_blocked`) | Holepunch under NAT, faster-link switch, outage and recovery, hard NAT, many addresses, relay connect over IPv4 and IPv6, relay with UDP blocked. Other files in `tests/patchbay/` exist: `degrade.rs`, `nat.rs`, `switch-uplink.rs`. |
| 16 | Live n0 integration test | iroh, none | `iroh/tests/integration.rs:36-45` | Uses `presets::N0` with `RelayMode::Staging` on the real network. Not hermetic. |
| 17 | Gossip endpoint helper | iroh-gossip, dev-dep `iroh` with `test-utils` | `iroh-gossip Cargo.toml` `[dev-dependencies]` iroh block (line 101); `src/net.rs:1207-1227` (`create_endpoint`) | `Minimal` preset, `RelayMode::Custom(relay_map)`, random secret key, `insecure_skip_verify`. Adds an optional `MemoryLookup` to the address lookup. Awaits `online()`. |
| 18 | Gossip net tests | iroh-gossip, same dev-dep | `src/net.rs:1263` (`gossip_net_smoke`), `:1402` (`subscription_cleanup`), `:1545` (`can_reconnect`), `:1646` (`can_die_and_reconnect`), `:1795` (`gossip_change_alpn`), `:1828` (`gossip_rely_on_gossip_address_lookup`) | Each test calls `iroh::test_utils::run_relay_server()` (`:1265`, `:1405`, `:1548`, `:1700`), builds endpoints with `create_endpoint`, and drives gossip over the in-process relay. |
| 19 | Gossip protocol simulator | iroh-gossip, `test-utils` (gate `src/proto.rs:59`) | `src/proto.rs:59-60`; `src/proto/sim.rs:24` (`NetworkConfig`), `:109` (`Network`), `:124` (`new`), `:166` (`insert_and_join`), `:243` (`run_trips`), `:249` (`run_duration`), `:261` (`run_while`), `:420` (`report`), `:535` (`SimulatorConfig`), `:565` (`from_env`) | Deterministic in-memory simulation of the topic state machines. Message latency comes from `LatencyConfig` (static or random per message, `sim.rs:61-90`). RNG is seeded ChaCha12. No sockets, no QUIC. |
| 20 | Simulator tests | iroh-gossip, `test-utils` | `tests/sim.rs:10` (`big_hyparview`), `:29` (`big_multiple_sender`), `:61` (`big_single_sender`), `:92` (`big_burst`), `:127` (`read_var`) | Four tests. Parameters come from env vars `PEERS` (default 100), `SEED`, `GOSSIP_ROUND_TIMEOUT` (`src/proto/sim.rs:565-572`). |
| 21 | `sim` CLI and scenario files | iroh-gossip, `simulator` | `Cargo.toml` `[features]` (`simulator` list), `:146-151` (bin `required-features`); `src/bin/sim.rs:65-93` (`Cli`, `Command::Run`, `Command::Compare`); `src/bin/sim.rs:232-234` (`GossipSingle`, `GossipMulti`, `GossipAll`); `simulations/all.toml` | `sim run --config-path` runs TOML scenarios. Flags: `--out-dir`, `--baseline`, `--single-threaded`, `--filter`. `sim compare` diffs two output dirs. `all.toml` lists seeds and scenarios with node counts and a latency range. |
| 22 | `n0-tracing-test` | n0-computer crate, dev-dep in gossip | `iroh-gossip Cargo.toml` `[dev-dependencies]`, `n0-tracing-test = "0.3"` | Captures and reads tracing logs in async and sync tests. Gossip net tests use `#[traced_test]`. |
| 23 | `patchbay` | n0-computer repo `n0-computer/patchbay` | `gh repo list n0-computer`, description: "Rust library for realistic network simulation via Linux namespaces" | Same library as row 14. Not cloned. Crate source not read. |
| 24 | `test-plans` | n0-computer repo `n0-computer/test-plans` | `gh repo list n0-computer` | Name matched the test filter. Empty description. Last push 2023-01-19. Contents not read. |

## Notes

- The only public route to iroh's helpers is the `test-utils` feature. The custom-transport helpers also need `unstable-custom-transports` (`iroh/src/test_utils.rs:17`), and that feature is named unstable.
- Gossip's `net.rs` tests already depend on `iroh::test_utils`. The gossip simulator (row 19) sits one layer below the endpoint. It does not exercise the QUIC or the relay.
- Doc and code disagree on the N0 preset's staging choice. `presets.rs:104-105` says tests or `test-utils` select staging infra. The code selects staging only when the env var `IROH_FORCE_STAGING_RELAYS` is non-empty (`src/address_lookup/pkarr.rs:177`, `:527`; `src/endpoint.rs:2041-2042`). No cfg switch found.
- The comment on `endpoint_two_relay_only_no_ip` says "without Address Lookup" (`endpoint.rs:2601`). The builder there uses `presets::N0` (`:2613`), and `N0` installs Pkarr and DNS lookup (row 11).
- Patchbay tests run only on Linux and need user namespaces (row 14, `tests/patchbay.rs:27`, `:58`).
- Spec: none checked. Scope was listing only.

## Not read

- iroh `iroh-relay` test helpers: covered by `f3-relay.md`, not repeated.
- iroh `tests/patchbay/nat.rs`, `degrade.rs`, `switch-uplink.rs`, and the remainder of `patchbay.rs` and `patchbay/util.rs` beyond the head.
- iroh `src/test_utils.rs` lines 140-560 (DNS and Pkarr server bodies) and `test_transport.rs` bodies beyond the signatures.
- iroh `src/endpoint.rs` test bodies beyond the cited ranges, and the remaining `src/address_lookup/*` tests.
- iroh-gossip `src/proto/sim.rs` bodies (report formatting, round stats), `src/bin/sim.rs` body, `examples/chat.rs`, `examples/setup.rs`, and the `src/proto/*` unit tests (`hyparview.rs`, `plumtree.rs`, `state.rs`, `topic.rs`).
- `simulations/all.toml` beyond the first 20 lines.
- The `patchbay` crate source and docs.rs for version 0.7. Not cloned.
- The `n0-tracing-test` crate source.
- `n0-computer/test-plans` contents. `net-tools` was matched by a broader filter and not read.
- Shallow clone CHANGELOGs and the `iroh` workspace's CI config.
