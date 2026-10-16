# A2: mcpmesh, scope: mesh model, presence, calls, identity, membership, absent peers

Date: 2026-10-16. Binding: cargo-cult-science, stop-yapping (read in full).

## Sources read

- Repo: https://github.com/counterpunchtech/mcpmesh, commit `555dc1d6a6a5d429729898d508f5068cdc0e2794`, clone at `/tmp/ra-src/mcpmesh`. Shallow clone, one commit, no tags. Release count not measurable here.
- Manifests: `Cargo.toml` (workspace), `Cargo.lock`, `node/Cargo.toml`, `net/Cargo.toml`.
- Design: `docs/specs/mcpmesh-design.md` lines 54, 70, 214, 227, 250, 297, 301, 310, 314, 361, 465-480, 512-521, 640.
- Docs: `docs/embedding.md` (host contract, root directory, sign_app sections), `docs/local-protocol.md` lines 16-32, 160-200 (method table, partial), 174, 608-618, 941-944, 1021, 1780.
- Code: `node/src/node.rs` lines 121-150, 185, 300-372, 440-470, 505-512; `node/src/lib.rs` 1-80; `node/src/roster/presence.rs` lines 1-30, 150-180, 235-320, 312-315; `node/src/roster/transport.rs` 18-30, 72-90; `node/src/daemon/boot.rs` 1258-1276; `node/src/daemon/accept.rs` 16-70 (partial); `node/src/daemon.rs` 946-958; `node/src/daemon/dial.rs` 811; `node/src/daemon/reach.rs` 84; `net/src/endpoint.rs` 29-42; `net/src/service.rs` 246, 388; `node/src/backends/mod.rs` 337, 588; `codec/src/lib.rs` 1-3, 113-117; `cli/src/proxy.rs` 58-97; `trust/src/app.rs` 1-10, 58; `cli/tests/` listing (partial).
- Estafette spec: `spec/blueprint.md` lines 1-63 (Part 1) and 107-117 (section 2.3, invariants I1-I7).
- Survey brief: `research/stack/surveys/brief.md`.

## Not read

- `docs/local-protocol.md` in full (2052 lines), only the method table part and the cited lines.
- Most of `node/src` (about 53k lines in the crate set). Handlers, pairing ceremony, blob provider, audit, relay config, and the daemon's dial race were read by grep and by the cited lines only.
- Spec sections 2.4 to 2.12 and Part 3. Outside this scope.
- Nothing was built or run. Test counts are `#[test]` and `#[tokio::test]` line counts, not executed results.

## mcpmesh (counterpunchtech/mcpmesh, 555dc1d, iroh exact-pinned `=1.2.0`, rmcp `=3.1.0`)

### What it does for this scope

Shares stdio MCP servers, called services, between people who have paired. A caller opens a session to a peer's named service over iroh QUIC. The owner's daemon spawns the MCP server per session and proxies its byte stream. It is not an agent-to-agent message system. The method table has no send, no message, and no inbox verb.

### The seven questions

**1. What it meshes.** MCP servers only. Each service carries an `allow` list of principals: `b64u:<user_id>`, `eid:<device>`, or a roster group. Evidence: `docs/local-protocol.md:164` (`register_service`), `docs/local-protocol.md:24-27` ("mcpmesh spawns it per session. It never speaks mcpmesh-local/1"). Agents are not a primitive. Any agent is a client of an MCP service.

**2. Architecture.** Two shapes over one set of handlers.

| Shape | Form | Evidence |
|---|---|---|
| Daemon | `mcpmesh` binary, per-user singleton, owns the iroh endpoint and a local control socket | `docs/embedding.md`, "never touches the per-user daemon's state, socket, or singleton lock" |
| Library | `mcpmesh-node`, one node per root directory, in-process, no daemon | `node/src/lib.rs:1-30`; `docs/embedding.md`, "One node per root" (`StartError::DataDirInUse`, redb exclusive lock) |

The library's `Node::control()` returns the daemon's `ControlClient` over an in-memory duplex, and runs the daemon's own handlers (`node/Cargo.toml`, `service` feature comment; `docs/embedding.md`, "Full parity is structural"). The supported surface is `NodeBuilder`, `Node`, `Config`, and the control protocol. Every other module is `#[doc(hidden)]` with no stability promise (`node/src/lib.rs`, module attributes).

Wire framing is NDJSON, one frame per newline, 16 MiB cap (`codec/src/lib.rs:2`). Not postcard.

Five ALPNs exist: `mcpmesh/mcp/1` (`net/src/endpoint.rs:29`), `mcpmesh/pair/1` (`:35`), `mcpmesh/ping/1` (`:42`), `mcpmesh/blob/1` (`node/src/blobs/mod.rs:16`), and iroh-gossip plus the roster blob ALPN, which exist only in roster mode (`node/src/daemon/boot.rs:1262-1276`). Embedders may register `app/...` ALPNs (`node/src/node.rs:348`, `accept_protocol`; `node/src/daemon.rs:946-958`, reserved names refused).

Harness coupling: the library has none. The CLI binary has Claude Desktop and Claude Code install text and config paths (`cli/src/proxy.rs:58-97`). The strings "Claude Code" appear in `net/src/service.rs:388` and `node/src/backends/mod.rs:588`, both inside `#[cfg(test)]` modules (`net/src/service.rs:246`, `node/src/backends/mod.rs:337`). They are test fixtures for stripping a caller's client-info field.

**3. Presence.** Roster mode only. Pairing mode has no gossip: "Pairing mode has no gossip at all — reachability is discovered by dialing" (`docs/specs/mcpmesh-design.md:476`; the sentence uses a dash in the source, the meaning is that pairing mode is dial-only).

- Topic: `blake3("mcpmesh/presence/" + org_id)`, `node/src/roster/transport.rs:25-27`. Keyed by the org id, not by a secret.
- Beat: signed by the device key over domain `mcpmesh/presence/1` (`node/src/roster/presence.rs:20`). Fields `endpoint_id`, `user_id`, `ts`, `roster_serial`, optional `meta`. Endpoint id is the device's ed25519 public key (`presence.rs:245`).
- Timing: period 60 s, jitter ±15 s (`presence.rs:312,315`). Skew ±120 s (`presence.rs:26`). TTL 180 s, enforced as a filter on read (`presence.rs:176-179`).
- Departure: no departure payload. Absence is inferred when the TTL lapses (`presence.rs`, no match for depart, goodbye, leave, or tombstone in the presence or transport files).
- Advisory: "no security decision derives from presence" (`docs/specs/mcpmesh-design.md:476`).
- Gate: the gossip ALPN is admitted only after the trust gate resolves the remote. An unresolved peer is refused (`node/src/daemon/accept.rs:33-40`).
- Exposure: the beat carries `endpoint_id` and `user_id` in clear to every admitted topic member.

**4. Direct calls.** One primitive for the mesh: `open_session {peer, service}` returns a live MCP byte pipe (`docs/local-protocol.md`, method table). The receiving side gets the authenticated identity as `_meta["mcpmesh/peer"]` (`docs/embedding.md`, identity section). For arbitrary app protocols, the library offers `connect_protocol(peer, alpn)` and `accept_protocol(alpn, handler)` (`node/src/node.rs:348, 455`). Both sit behind the same gate. "Your handler runs behind the same gate as every built-in protocol. An unauthorized or revoked peer is closed before accept is called" (`node/src/node.rs`, `accept_protocol` doc). `connect_protocol` "does not authorize anything" and "a peer that is simply offline is a dial failure" (`node/src/node.rs:441-452`).

Payload attribution: `sign_app` and `verify_app` sign with the device key under a caller-chosen domain (`node/src/node.rs:505-562`, `trust/src/app.rs:58`). The doc names store-and-forward as the use case, and says the embedder owns the mailbox.

**5. Identity.** Persistent, not ephemeral.

- Device key: `<root>/config/device.key`, minted on first start if absent (`node/src/node.rs:121`, `node/src/paths.rs:32`). Endpoint id equals this key.
- Stability requirement: "The key must stay STABLE across restarts of the same node — passing a fresh one each boot mints a new identity every time" (`node/src/node.rs:136-142`). Peers pin the identity at pairing (same doc: "the identity every peer pinned at pairing").
- User key: `<root>/config/user.key`, a second persistent key for the person (`node/src/node.rs:130`, `node/src/paths.rs:33`). Exportable as a 33-word recovery phrase, which "IS the private key" (`docs/local-protocol.md`, `user_key_export`).
- Storage: both keys are files in the config directory, mode 0600 (`docs/embedding.md`, root directory section).

**6. Membership.** Two modes, one trust gate.

- Pairing mode: a local allowlist in `state.redb`, built from one-time invite secrets (`docs/specs/mcpmesh-design.md:54`). Each node writes its own row for each pair. Pairing needs a two-human short-authentication-code ceremony (`docs/specs/mcpmesh-design.md`, P3; `node/src/pairing/sas.rs`).
- Introduction: `peer_introduce` installs a peer from a signed endorsement by someone already paired. It "installs IDENTITY, not authorization" (`docs/local-protocol.md`, method table). The doc says this turns O(N²) ceremonies into O(N).
- Roster mode: an org root key signs a roster of users, devices, and groups, with a strictly increasing serial. Distribution by gossip, blob, and HTTPS poll (`docs/specs/mcpmesh-design.md:297, 301`). The root is kept offline (`docs/specs/mcpmesh-design.md`, P5).
- Revocation: local `peer_revoke` marks a device dead on this node. Roster revocation severs live sessions across all ALPNs (`docs/specs/mcpmesh-design.md:227, 314`).

**7. Absent peers.** No store. Evidence:

- No outbox, mailbox, retry queue, or offline queue in `node`, `net`, `cli`, `local-api`, or `trust`. Matches are comments or docs about what embedders might build (`node/src/node.rs:505-512`, `trust/src/app.rs:5-6`).
- Dial to an offline peer fails with `-32055 peer unreachable` (`docs/local-protocol.md:1021, 1780`).
- Replay is explicitly absent: "transparent session resumption and replay of missed subscribe events" are "Not implemented" (`docs/local-protocol.md:943-944`).
- What persists for absent members: the roster document, through re-seeding by every accepting node (`docs/specs/mcpmesh-design.md:640`), and `org_rotate` "rides every later roster" so offline members re-anchor (`docs/local-protocol.md:174`). Pending invites persist in `data/invites.json` (`docs/embedding.md`). None of these is a message.

### Maturity

- Last commit 2026-09-14. Version 0.58.0. Licence MIT OR Apache-2.0. `RELEASING.md` present. Release count not measured.
- Test functions by crate (`#[test]` plus `#[tokio::test]` lines, not executed): codec 7, net 50, trust 62, node 564, cli 289, local-api 85.
- Presence tests: unit tests in `node/src/roster/presence.rs` (sign and verify, skew, forgery, metadata cap, identity binding) and `cli/tests/presence.rs`.
- Embedding tests: `cli/tests/embed_parity.rs`, `cli/tests/embedded_loopback.rs`.
- Stale text found in the tree: `node/Cargo.toml` comment says iroh `=1.0.1`, workspace pins `=1.2.0`. `docs/embedding.md` says rmcp `=3.0.0-beta.3`, workspace pins `=3.1.0`.
- Mismatch, design text against code: `docs/specs/mcpmesh-design.md:476` says pairing-mode dial has a 3 s timeout. `node/src/daemon/dial.rs:811` sets `DIAL_TIMEOUT` to 20 s. The 3 s constant is the reach probe, `node/src/daemon/reach.rs:84`.

### Estafette fit: dependency shapes

- A. Whole range from `mcpmesh-node`: presence, direct protocol, identity, membership.
- B. Transport only: `accept_protocol` and `connect_protocol` on an `app/` ALPN. Estafette keeps its own presence, identity, and membership.
- C. Patterns only, no dependency.

What shape A imposes, from the code:

- **One stable endpoint per root.** Peers pin the device endpoint at pairing. A per-session ephemeral key, as the brief specifies, is a new stranger to every pair each session (`node/src/node.rs:136-142`).
- **Every app ALPN sits behind the mcpmesh gate.** Unpaired peers close before the handler runs (`node/src/node.rs`, `accept_protocol` doc; `node/src/daemon/accept.rs:33-40`). I found no switch that admits unpaired peers. Part 1.6, "everyone may speak to everyone", then needs pairwise pairings, introductions by `peer_introduce`, or roster membership.
- **Presence exists only in roster mode.** Pairing mode has no gossip (`docs/specs/mcpmesh-design.md:476`). A pairing-mode network has no presence at all.
- **Roster mode brings an org root.** The root signs membership and is held offline (`docs/specs/mcpmesh-design.md:297, 513`). A roster URL and blob re-seeding are central-looking infrastructure (`docs/specs/mcpmesh-design.md:301, 640`).
- **Presence topic is keyed by org id, not a secret.** `node/src/roster/transport.rs:25-27`. The brief specifies a topic from the network secret.
- **Heartbeat every 60 s.** `node/src/roster/presence.rs:312`. The brief specifies no heartbeats.
- **Dependency weight is fixed.** `node/Cargo.toml` has one feature, `unstable-relay-only`, and it is test-only. No switch removes roster, blob, gossip, or HTTPS-poll code. `reqwest`, `iroh-blobs`, `iroh-gossip`, `redb`, `toml`, and `figment` come with the crate.
- **Version pins collide with the brief.** Workspace pins `iroh =1.2.0` exact (`Cargo.toml`). The brief lists iroh 1.3.0 for estafette. Workspace also pins `rmcp =3.1.0` exact. The brief lists rmcp 3.5.1. Both cannot unify. Estafette would downgrade both, or hold two copies.
- **Shape A also takes the MCP surface.** `mcpmesh-node` brings `rmcp` through `mcpmesh-net`, so estafette's MCP server runs on mcpmesh's pinned rmcp.

What shape B imposes, the transport-only option:

- The gate still applies. Estafette's shared-secret membership would be a second check on top of mcpmesh's per-pair gate.
- The stable endpoint identity still applies.
- Estafette builds its own presence, delivery acknowledgement, and framing. The app stream is raw bytes. No receipt is returned by mcpmesh.
- The iroh and rmcp pins still apply, because the handler signature names iroh types (`node/src/lib.rs`, iroh re-export note).

### Against Part 1 of the spec, read item by item

| Part 1 item | mcpmesh | Evidence |
|---|---|---|
| 1.2 card with a seal; 1.2 card as persistent self | no card object. Identity is a device key file plus a user key file | `node/src/node.rs:121-146`, `node/src/paths.rs:32-33` |
| 1.3 newcomer's name adjusted on collision | no rename. Collisions avoided by addressing an endpoint id | `cli/tests/presence.rs:308`, name "dial_by_eid_targets_the_exact_endpoint_despite_a_nickname_collision" |
| 1.4 member announces arrival and departure | arrival by periodic beat only. No departure payload. Absence by TTL | `node/src/roster/presence.rs:176-179, 312` |
| 1.4 network forgets who left | forgets by TTL filter on read, not by a departure event | `node/src/roster/presence.rs:176-179` |
| 1.5 delivered means it reached the door | no message primitive. Sessions and protocol streams only | `docs/local-protocol.md` method table |
| 1.5 a shout is many messages | no fan-out verb. The caller dials each peer | `docs/local-protocol.md` method table |
| 1.6 every message proves sender and network membership | sender proven by TLS endpoint key. Network membership is per-pair or per-roster. No network-wide secret | `node/src/node.rs` `accept_protocol` doc; no keyed MAC found by grep |
| 1.7 no mailbox, queue, group, thread, or center | no mailbox, queue, group, or thread. Roster mode has an org root, a roster URL, and blob re-seeding | `docs/specs/mcpmesh-design.md:297, 301, 513, 640` |
| 1.9 transport carries no social meaning | `set_app_metadata` folds up to 256 bytes of app state into each signed roster-mode beat once set | `docs/local-protocol.md` `set_app_metadata` row; `node/src/roster/presence.rs:23-25` |
| 1.9 one owner per network | roster: one org root per network. Pairing: no network, only pairwise trust | `docs/specs/mcpmesh-design.md:297, 513` |

### Against invariants I1-I7 (section 2.3)

| Invariant | What shape A imposes | Evidence |
|---|---|---|
| I1 binary knows no harness | Library: none. The CLI binary carries Claude Desktop and Claude Code text. Depending on the library, not the CLI, keeps I1 | `cli/src/proxy.rs:58-97`; harness names appear only in test code (`net/src/service.rs:246, 388`, `node/src/backends/mod.rs:337, 588`) |
| I2 no component has authority over members | Roster mode installs an org root whose signature decides membership. Pairing mode puts the decision in each node's own gate. I2 holds only in pairing mode, and only if each pair is its own authority | `docs/specs/mcpmesh-design.md:297, 513`; `docs/local-protocol.md` `org_approve`, `org_revoke` |
| I3 inbox carries messages only | The library has no inbox. Its control API has more than 60 verbs, including `user_key_export`, `org_create`, and `org_revoke`. Reusing the control client as an inbox would break I3 | `docs/local-protocol.md` method table |
| I4 MCP tool list static | Not enforced by mcpmesh. Services register and unregister at runtime. Grep found no list-changed handling in `net`, `node`, or `cli`. Imposes nothing unless estafette exposes mcpmesh services | `docs/local-protocol.md` `register_service`, `unregister_service`; grep |
| I5 card holds no secret | Keys live as files in the config directory. The user key exports as 33 words that are the private key. A card that is a config directory holds secrets | `node/src/paths.rs:32-33`; `docs/local-protocol.md` `user_key_export`. Tension inside the spec: Part 1.2 says the card carries a seal, I5 says a card holds no secret |
| I6 network keeps no message for absent member | No message store. Roster and invite state persist, not messages. Roster re-seeding and `org_rotate` deliver state to offline members | `docs/specs/mcpmesh-design.md:640`; `docs/local-protocol.md:174`; `docs/embedding.md` (`data/invites.json`) |
| I7 send tells the truth | Dial failure is reported as `-32055`. An accepted app stream gives no application-level receipt, so the sender cannot tell that a handler stood at the door | `docs/local-protocol.md:1021, 1780`; `node/src/node.rs` `connect_protocol` doc |

### Brief items checked against the code

- No heartbeats. Mismatch: 60 s beats (`node/src/roster/presence.rs:312`).
- Departure payload. Absent: no departure in presence or transport.
- Probe before declaring dead. Present: `node/src/daemon/reach.rs:84` (3 s probe), ping ALPN `net/src/endpoint.rs:42`. Probe results are advisory.
- Topic from shared network secret. Mismatch: topic from org id (`node/src/roster/transport.rs:25-27`).
- Ephemeral key per session. Mismatch: stable key, required by design (`node/src/node.rs:136-142`).
- Postcard framing with a MAC keyed from the network secret. Absent: NDJSON (`codec/src/lib.rs:2`), no keyed MAC, no postcard by grep.

### What estafette could take, one line each

- Crate: `mcpmesh-node` as transport only (shape B), and only if estafette accepts stable endpoint identity, the per-pair gate, and iroh `=1.2.0`.
- Pattern: signed presence beat with domain, skew window, and TTL (`node/src/roster/presence.rs:45-120, 176-179`).
- Pattern: accept-time gate on every ALPN, resolved before the handler runs (`node/src/daemon/accept.rs:33-40`).
- Pattern: payload signing with the device key under a caller-chosen domain (`trust/src/app.rs:58`, `node/src/node.rs:505-562`).
- Pattern: signed introduction by an already-paired peer, installing identity without authorization (`docs/local-protocol.md`, `peer_introduce`).
- Pattern: two-human short-authentication-code ceremony (`node/src/pairing/sas.rs`), if any pairing step remains in estafette.

### Cross-project observations

Only one project in this scope, so none.

## Not read

- The local-protocol method table beyond the lines cited, the subscribe event stream, and the audit API.
- Pairing ceremony code in `node/src/pairing/` beyond the SAS file name.
- The blob provider and roster-blob code in `node/src/blobs/` and `cli/src/roster/`.
- The rendezvous code, `node/src/pairing/rendezvous.rs`, 2907 lines.
- Spec sections 2.4 to 2.12 and Part 3. Read only Part 1 and 2.3, as scoped.
- No test run, no build, no network access to the upstream repo. Clone is at the commit named above.
