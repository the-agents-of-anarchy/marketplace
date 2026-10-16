# Breadth: unlisted finds

Date: 2026-10-16. Scope: agent-to-agent messaging or presence plus direct messaging, over iroh or another Rust p2p stack. Covered names from the lead were skipped. Index checked by name at `research/stack/index/index.md`.

Bound to `cargo-cult-science` and `stop-yapping`. Every find lists counter-evidence beside it. Null results are counted.

## Method

Queries, `gh search repos`, result counts (limit 30 unless noted):

| Query | Results |
|---|---|
| agent to agent messaging | 30 (capped at limit) |
| agent mesh p2p | 0 |
| mcp p2p | 2 |
| iroh agent | 3 |
| claude code agents messaging | 3 |
| multi-agent messaging rust | 0 |
| iroh agents messaging (extra) | 0 |
| iroh-gossip agent presence (extra) | 0 |
| agent presence gossip (extra) | 0 |
| p2p agent messaging rust (extra) | 0 |
| iroh, limit 100, filtered by name or description keywords | 100 returned, 13 matched |
| iroh-gossip, limit 100 | 44 |
| `gh search code iroh` in Cargo.toml, limit 100 hits | 61 distinct repos |
| agent-habilis org (`gh repo list`) | 18 repos |

The 30 agent-to-agent hits were sorted by their descriptions and manifests. Manifests checked for iroh, libp2p, p2p, WebRTC, QUIC and Tailscale dependencies: none found in any Python, TypeScript, Go or Elixir repo in that list. Most of those 30 are file, git, tmux, chain or hosted-relay designs by their descriptions. Those classifications come from descriptions only, not code.

## High-signal finds

| Name | URL | What | Activity | Why relevant |
|---|---|---|---|---|
| agent-habilis/agent-gossip | https://github.com/agent-habilis/agent-gossip | Rust app for agent gossip messaging, built on A2A. Three frontends (CLI, MCP, library) over one event loop. Directed messages go point-to-point, broadcasts over gossip. | Created 2026-05-19, pushed 2026-10-16, 8 stars, 19 releases, latest v0.12.4 published 2026-10-15. | Direct messaging and gossip presence in Rust. Not on the covered list, not in the index. Counter-evidence: its engine is `habilis-network`, already covered, so the transport and mesh overlap that row. Crate has no direct iroh dep (`crates/agent-gossip/Cargo.toml:67-68`, root `Cargo.toml:83-86`). Directed send is unicast (`crates/agent-gossip/src/a2a/send.rs:256-257`), sealed to the recipient's X25519 key (`send.rs:846-854`). |
| endojs/endo-but-for-bots | https://github.com/endojs/endo-but-for-bots | OCapN netlayer over iroh 1.0 for "bots". One bidirectional QUIC stream per connection, 30 s datagram heartbeat, Rust daemon transport with ALPN `endo/captp/0`. | Created 2026-02-15, pushed 2026-10-16, 5 stars, 0 releases. Design doc status "Complete", created 2026-07-13. | Agent-named, iroh-based, direct capability messaging. Counter-evidence: a JavaScript repo with a Rust side, and the netlayer is a connect-style transport, not presence. Cites: `designs/ocapn-iroh-netlayer.md:1-20` (status), `:101-106` (stream and heartbeat), `rust/endo/src/iroh_net.rs:11` (ALPN). The Rust crate uses a path dep on `endo_iroh` (`rust/endo/Cargo.toml:39`). |

## Medium-signal finds

| Name | URL | What | Activity | Why relevant or not |
|---|---|---|---|---|
| fofoca-network/fofoca | https://github.com/fofoca-network/fofoca | Serverless mesh engine: iroh, iroh-gossip, automerge CRDT. Peers find each other over mDNS, mainline DHT or relay. `fofoca-stream` gives 1-to-1 byte streams. | Created 2026-08-01, pushed 2026-10-13, 1 star. Rust. | Generic, not agent-specific. Gossip plus direct streams over iroh, both in the spec's shape. Cites `README.md:1-9`, crate list in README. Did not read `fofoca-stream` source. |
| n0-computer/iroh-smol-kv | https://github.com/n0-computer/iroh-smol-kv | Replicated key-value store over an iroh-gossip topic. Values signed over (key, value, timestamp). | Created 2025-09-19, pushed 2026-06-15, 11 stars. Rust. | Could carry presence-style state records. Not a messaging layer. Cites `README.md:1-12`. |
| rustonbsd/advanced-gossip | https://github.com/rustonbsd/advanced-gossip | iroh-gossip extension: per-topic read and write policies, Ed25519 message signatures, automatic discovery via iroh-topic-tracker. | Created 2025-03-23, pushed 2025-04-05, 0 stars. Self-described WIP. | Signed gossip with access control is close to the spec's MAC and topic model. Stale for about 18 months. Cites `README.md:1-12`. |
| Zeus-Deus/codemux | https://github.com/Zeus-Deus/codemux | Desktop agent workspace. Iroh remote transport in TypeScript via wasm. MCP server drives the app. | Created 2026-03-06, pushed 2026-10-15, 13 stars. | Remote control of agent terminals over iroh, not agent-to-agent. Cites `src/remote/iroh-transport.ts`, `README.md:61`. |
| HelpFreedom/claude-bridge | https://github.com/HelpFreedom/claude-bridge | Phone controls own Claude Code sessions. LAN first, iroh p2p tunnel off-LAN. | Created 2026-07-23, pushed 2026-07-28, 62 stars. Java. README in Russian. | Human-to-own-machine, not agent-to-agent. Cites `README.md:8,26,33`. |
| 23blocks-OS/ai-maestro | https://github.com/23blocks-OS/ai-maestro | Agent dashboard with AMP messaging and a "peer mesh, no central server" claim. | Pushed 2026-10-16, 822 stars, release v0.81.6 published 2026-10-16. TypeScript. | Counter-evidence: mesh is host-to-host HTTP exchange (`app/api/hosts/exchange-peers/route.ts`), with `lib/amp-relay.ts` and `lib/amp-websocket.ts`. Relay-based, not iroh. Cites `README.md:34-35,120-128`. |
| alexfrmn/murmur | https://github.com/alexfrmn/murmur | Encrypted agent-to-agent messaging, README says "no central orchestrator". | Pushed 2026-10-15, 19 stars. JavaScript. | Counter-evidence: README also describes a broker link and relay (`README.md:151`). Manifests show no p2p dep. Brokered, not p2p. |
| ekasc/agentnet | https://github.com/ekasc/agentnet | Shared context HTTP server over a tailnet. README says "No mesh protocol". | Pushed 2026-08-29, 0 stars. Go. | Central server. Excluded from p2p. Cites `README.md:1,24`. |
| agent-habilis/agent-graph | https://github.com/agent-habilis/agent-graph | Team-of-agents graphs. README says a graph "runs in a gossip as an instance". | Created 2026-09-25, pushed 2026-10-16. | Orchestration on top of gossip, not a transport. Cites `README.md:3`. |
| agent-habilis/iroh-address-lookups, agent-habilis/swarm-discovery | forks of n0 and rkuhn | DHT and mDNS address lookup for iroh; mDNS swarm discovery. | iroh-address-lookups pushed 2026-10-16. swarm-discovery pushed 2026-07-13. | Discovery layer for presence. No messaging. |
| agent-habilis/agent-inject, agent-habilis/agent-share | https://github.com/agent-habilis/agent-inject, https://github.com/agent-habilis/agent-share | Phone-to-computer file push over WebRTC. P2P folder and file sharing. | agent-inject created 2026-09-27. agent-share pushed 2026-10-13. | Not agent-to-agent messaging. Listed for completeness. |

Small iroh-gossip chat apps for humans, not agents: jamessizeland/peer-to-peer, sriramsenthill/p2p-chat, Silver595/p2p_messanger, Pallav0099/skyp2p. Not read beyond descriptions.

## Control: libp2p

Versions from `rustup run 1.99.1 cargo info`. Release data from the crates.io API.

| Crate | Version | Last release | Releases | Downloads | rust-version |
|---|---|---|---|---|---|
| libp2p-request-response | 0.30.0 | 2026-09-11 | 42 | 14,923,802 | 1.88.0 |
| libp2p-gossipsub | 0.50.0 | 2026-09-11 | 54 | 8,867,520 | 1.88.0 |

Counter-evidence for the control: the libp2p crates are maintained and widely used, but they bring a second transport stack that the spec does not use. No find in this survey reuses them.

## Counts

| Item | Count |
|---|---|
| Covered names skipped | 18 |
| Repos in agent-to-agent query | 30 (capped) |
| Repos in agent-habilis org | 18 |
| New high-signal finds | 2 (agent-gossip, endo-but-for-bots) |
| New medium-signal finds | 11 rows |
| Keyword repo queries returning zero | 6 of 10 |

## Not read

- `spec/blueprint.md`. Decision numbers were not checked, so "against the spec" is unassessed beyond the brief's summary.
- `habilis-network` engine source, already covered. The agent-gossip mesh and gossip path were not read beyond `send.rs`.
- Source of `fofoca-stream`, `fofoca-iroh-multihop-transport`, `advanced-gossip`, `iroh-smol-kv`, `codemux` iroh transport, `claude-bridge`, `ai-maestro` lib, `murmur` and `agentnet` internals. Readme claims only, except where a file path is cited.
- `endo` iroh netlayer JavaScript. The design doc was read, not the code.
- The 30 agent-to-agent repos beyond their descriptions and manifest dependency lists.
- The `iroh` search cap: 100 results per query, and code search capped at 100 hits, so both lists may be incomplete.
