# iroh 1.3: local discovery, tickets, events

Author: worker w1-f1b-iroh (haiku), 2026-10-16. Saved by the orchestrator from the worker's message; the worker declined to write files. Peer content, unverified. Nothing compiled or run.

## 1. Local network discovery (mDNS)
- Not in iroh 1.3: `iroh/src/address_lookup.rs:46-50` says mDNS and Mainline DHT lookup "live in separate crates". No `mdns` feature in `iroh/Cargo.toml:150`. `iroh/examples/transfer.rs:593-596` errors on `--mdns`.
- Crate: `iroh-mdns-address-lookup` 0.6.0, repo n0-computer/iroh-address-lookups at 0d480bc; no `[features]`.
- Enable: `MdnsAddressLookupBuilder` implements `AddressLookupBuilder` (`iroh-mdns-address-lookup/src/lib.rs:254-261`); `Builder::address_lookup` accepts it (`iroh/src/endpoint.rs:616`). Crate doc example (`lib.rs:11-22`) adds it after bind via `endpoint.address_lookup().unwrap().add(mdns.clone())`. Builder-before-bind form not compiled.
- Not in any preset: builder starts empty (`iroh/src/endpoint.rs:206`); the `N0` preset adds only pkarr and DNS (`iroh/src/endpoint/presets.rs:117-133`).
- Pulls in: `swarm-discovery` 0.6.1 (with `acto` 0.8.2, `hickory-proto` 0.26.1, `socket2`, `rand`, `thiserror` 2, `tokio`, `tracing`). New against iroh's lock: `swarm-discovery`, `acto`.
- Privacy: the record name carries the endpoint id (`lib.rs:195-205`); `advertise(false)` turns advertising off (`lib.rs:182`); on by default.

## 2. Tickets
- `iroh-tickets` 1.0.0 at cec7f1e. Type `iroh_tickets::endpoint::EndpointTicket` (`src/endpoint.rs:30`), trait `Ticket` (`src/lib.rs:26`).
- Contents: an `EndpointAddr` = one `EndpointId` plus `TransportAddr`s (relay URL, IP socket address, custom) (`iroh-base/src/endpoint_addr.rs:42-62`). No name, secret, signature, or MAC.
- Text form: prefix `endpoint`, then lowercase base32 without padding of a postcard body with a `Variant1` tag (`src/endpoint.rs:46`, `src/lib.rs:49-56`). Tests at `src/endpoint.rs:163,171,179`.
- Fits spec 2.2 "ticket" for the bootstrap member's id and relay.
- Gap for 3.13 invitation string: name and secret cannot ride in an `EndpointTicket`; the invitation needs a container or its own format.
- iroh-tickets' lock pins iroh-base 1.0.0; iroh 1.3 uses iroh-base 1.3.0. Semver-compatible; clean build not confirmed.
- iroh 1.3 does not depend on iroh-tickets (docs mention only: `iroh/src/address_lookup/memory.rs:4`).

## 3. Network change and relay reconnect events
iroh 1.3 has no single event named "network change" or "relay reconnect"; spec 3.8 assumes one.

| Spec event | Nearest iroh surface | Evidence |
|---|---|---|
| Relay reconnect | `Endpoint::home_relay_status()`: watcher of `Vec<RelayStatus>`; `.updated().await` or `.stream()` | `iroh/src/endpoint.rs:1408`, example `:1973`; `RelayStatus::is_connected()` `:1932`, `last_error()` `:1946` |
| Relay state values | `Connecting`, `Connected`, `Disconnected { last_failure }` | `iroh/src/socket/transports/relay/actor.rs:962-978` |
| Network change | `Endpoint::watch_addr()`: direct IP addresses and home relay URLs | `iroh/src/endpoint.rs:1289`; built from `ip_addrs` and `home_relay` at `:1291-1292` |
| Wait for relay | `Endpoint::online()` | `iroh/src/endpoint.rs:1374`; a wait, not an event |

- Network change is an input, not an output: `Endpoint::network_change()` (`endpoint.rs:1665`) tells iroh the network changed; iroh rebinds, re-probes, notifies QUIC (`iroh/src/socket.rs:1657-1690`). No public stream reports a network change to the program.
- `Endpoint::net_report()` (`endpoint.rs:1457`) exists only with the `unstable-net-report` feature.
- Inference, not run: a reconnect to the same relay URL likely leaves `watch_addr()` unchanged (`socket.rs:488-500`); `home_relay_status()` is the reconnect signal, `watch_addr()` the address-change signal.
- Spec consequence: row 3.8 needs two watchers, or a stated rule for which triggers Presence. A network change that leaves addresses unchanged emits nothing found.

## Not read
iroh-relay internals and the reconnect loop in `relay/actor.rs`; netmon link-change detection; swarm-discovery source (lock entry only); iroh-mainline-address-lookup; n0-watcher; mdns tests beyond names; release counts (depth-1 clones). Last commits: iroh 2026-09-28, iroh-tickets 2026-08-18, iroh-address-lookups 2026-10-15.
