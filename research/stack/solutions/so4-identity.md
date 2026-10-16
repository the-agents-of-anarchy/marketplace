# Identity: how projects solve it

Scope: how a long-lived name or identity binds to a network key, how names collide, and how a second live holder is handled. Sources are the surveys, specimen, verify reports, and experiments/e1-api.md. Each row cites the report and its section or line. Claims are as the reports state them; nothing was re-read from source except where a report's own citation is quoted.

| Mechanism | Projects (report) | Key lifetime | Name → key binding | Collision handling | Second live holder | Evidence |
|---|---|---|---|---|---|---|
| A. Ephemeral key, free nickname | agent-gossip / habilis (sp1, sp2, sp4, a1b, a3); p1 workshop chat default; p3a Tunnet room peer id; p3b p2panda default | One process or one join. A restart mints a new key under the same nickname. | Nickname is a display label. Receivers do not pin it to a key. Endpoint table, seal-key lookup, and addressee test all compare the nickname. | None found. Roster is a set of nicknames, so two keys with one nickname share one entry. Open issue #28: a join with a live peer's nickname does not fail. | Not detected. Dedup keys on the key-bound hash, not the name. Anti-entropy answers go only to the endpoint the key proved. | sp2 "Keys and where they live", "How names map to keys"; sp4 "Nicknames"; sp1 open issues #28, #29; a1b "Identity binding"; p3a lines 28, 52 |
| B. Persistent node key in a file | mcpmesh device key (a2 §5); p3a Tunnet agent identity; walkie/alink node key (a1); chio transport seed (i2); yah/mshr identity file (r1) | Until explicit rotation or file removal. Tunnet rotates only by explicit command. | Peers pin the key at pairing (mcpmesh). Name is a label. | Collision avoided by dialing the endpoint id, not the name (a2 test at cli/tests/presence.rs:308). | Mcpmesh: one node per root, redb lock, DataDirInUse (a2 §1). Walkie/alink: one daemon owns the endpoint, other CLI calls go over its socket (a1). | a2 §5; p3a identity.rs:4-7, connect.rs:297-306; a1 node.rs:608-640; i2 iroh_mount.rs:91, 227-239; r1 keypair.rs:4, 98-101 |
| C. Two keys: device and person | mcpmesh (a2 §5) | Device key stable per node. User key stable per person. | User key is separate from device key. Roster links them (G). | Not stated. | Not stated. | a2 §5; node.rs:121, 130 |
| D. Address by key, not name | mcpmesh dial-by-id (a2 §1.3); walkie/alink frames by endpoint id (a1); Buzz by endpoint identity (a2b); iroh-rings by EndpointId (i2) | Follows the key chosen in B or A. | Name never routes. Key routes. Name still needs a source of keys, supplied by pairing or a card. | Sidesteps collision: two nicknames cannot route to one key. | Two nodes with one key: not stated. Transport decides; iroh not read. | a2 §1.3 table; a1 "Keys underneath"; a2b "Addressing"; i2 "iroh-rings" |
| E. Signed record binding an id to a key | chio issuer-signed directory (i2); mcpmesh endorsements and presence beacons (a2 §5, §6); p3a Tunnet coordinator-signed member record (grants.rs:257-265); p1 smol-kv writer-signed values; p2 tracker records signed by node key (record.rs:486-511) | Signer key, long-lived. p2 DHT slot keys derive from a passphrase. | Binds operator id, node id, or endpoint id to a key. Chio binds kernel_id to EndpointId. No surveyed code binds a free handle to a key. | Chio rejects duplicate kernel_id and duplicate EndpointId at bundle load (identity.rs:652-660, 750-762). | Not detected at runtime (i2). | i2 chio "Identity binding"; a2 §5-6; p3a "Identity", "Claim"; p1 "Sign"; p2 lines 24, 46 |
| F. Versioned record against replay | chio version floor and predecessor hash chain (i2, identity.rs:605); mcpmesh roster serial, strictly increasing (a2 §6); agent-gossip per-author seq and prev hash (sp2, send.rs:369-388) | Per record. | Not applicable. | Old version rejected by the floor (chio). Fork resolution not described by any report. | Not stated. | i2 chio; a2 §6; sp2 "Broadcasts" |
| G. Org root key and roster | mcpmesh roster mode (a2 §6) | Root kept offline (P5). | Root signs roster of users, devices, groups. Maps user to devices. | Not stated. | Roster revocation severs live sessions across all ALPNs (a2 §6). | a2 §6; docs/specs/mcpmesh-design.md:297, 301, 314 |
| H. Pairing by invite and check code | mcpmesh pairing mode (a2 §6) | Per pair. | Each node writes its own allowlist row in state.redb, built from one-time invite secrets. | Not stated. | Local peer_revoke marks a device dead on this node only. | a2 §6; node/src/pairing/sas.rs |
| I. Introduction by signed endorsement | mcpmesh peer_introduce (a2 §6) | Per introduction. | Installs identity, not authorization. | Not stated. | Not stated. | a2 §6; docs/local-protocol.md method table |
| J. Connection gate by shared secret | iroh-auth (i1) | Secret is any byte string (i1 secret.rs). No session key exported. | Node id cached per connection, LRU of 10,000 entries. | Not stated. | Failed handshake blocks the id. Block lost on LRU eviction. A restarted process with a new key escapes it (i1). | i1 "iroh-auth" |
| K. Allowlist by key after a token | iroh auth-hook example (d2, auth-hook.rs:342-347) | Per connection. | remote_id used as allowlist key after a token check. | Not stated. | Not stated. | d2 "Identity" |
| L. Per-request permission by EndpointId | iroh-rings (i2) | Caller owns the key. Examples call SecretKey::generate(). | Explicit add of an EndpointId to a ring, with optional expiry (registry.rs:120, 201). | Not stated. | Not detected. Open ring grants read to every peer by design. | i2 "iroh-rings" |
| M. Signed capability chain | rcan (i1) | Issuer keys, no revocation. | Chain from principal key to invoker key. | Not applicable. | Not applicable. No revocation, no replay protection. | i1 "rcan" |
| N. Single holder by OS lock or single owner | agent-gossip bell, <nickname>.bell (sp5, cli/bell.rs:23-44); mcpmesh per-root redb lock (a2 §1); walkie/alink one daemon (a1) | Lock lives with the process. | Lock is per nickname. | Not applicable. | Exclusive try_lock with 500 ms retry. sp3 says one daemon per mesh and nickname, but no refusal path is reported. | sp5 "bell"; a2 §1; a1 line 74; sp3 "Identity binding" |
| O. Local suffix on name collision | walkie/alink (a1 §1.3, store.rs:161-167) | Name lives in local table. | Suffix -2, -3, ... at insert. | Local table only. Nothing presence-aware. | Not stated. | a1 §1.3 |
| P. Random word-word default names | agent-gossip default nickname (sp2, name.rs:127-129, wordlist.rs:116-122) | Per session. | Random pair from a 1024-word list. | Chance only. No check reported. | Not stated. | sp2 "How names map to keys"; sp4 "Nicknames" |
| Q. Membership by shared secret | agent-gossip mesh from SHA256 of join string (sp1, "Joining a mesh"); p2panda 32-byte topic (p3b); iroh-auth password (i1) | Secret per mesh. | Not a name binding. Possession of the secret gates the network. | Not applicable. | iroh-gossip admits any peer that knows the topic id, no other check (v2 Q1). | sp1; p3b "Membership"; v2 Q1 |

## Each mechanism in two or three sentences

**A. Ephemeral key, free nickname.** Agent-gossip mints an Ed25519 key per daemon process, and a restart mints a new key under the same nickname. Routing still keys on the nickname: the endpoint table, seal-key lookup, and addressee test compare names, and the receiver deliberately does not pin a nickname to a key. Open issue #28 says a join with a live peer's nickname does not fail.

**B. Persistent node key in a file.** Mcpmesh mints a device key on first start and says peers pin it at pairing. Walkie, chio, and yah keep a node key in a file as well, and Tunnet changes its identity only by explicit command. Because the key outlives restarts, the name can change without changing the identity.

**C. Two keys: device and person.** Mcpmesh keeps a second persistent key for the user, exportable as a 33-word phrase that its doc calls the private key. The roster (G) is what ties that key to its devices. No other surveyed project has a person-level key.

**D. Address by key.** Several projects route dials and frames by key, so two holders of one nickname cannot be confused on the wire. Mcpmesh's dial-by-id test is the explicit case. The name still has to resolve to a key somewhere, and pairing or a card supplies that.

**E. Signed record binding an id to a key.** Chio, mcpmesh, Tunnet, smol-kv, and one tracker sign records with a long-lived key. These bind operator, node, or endpoint ids, never a free handle, so the spec's handle-bearing claim has no counterpart in code. Chio alone rejects duplicate ids when its bundle loads.

**F. Versioned record against replay.** Chio uses a version floor and predecessor hash chain, mcpmesh a strictly increasing roster serial, and agent-gossip per-author sequence numbers with a prev hash. Each stops an older record from replacing a newer one. No report says how two valid, diverging chains are resolved.

**G. Org root key and roster.** Mcpmesh's roster mode has an offline org root sign users, devices, and groups under a serial that only increases. Revoking through the roster severs live sessions across all protocols. This is the only roster-based revocation that reaches live connections in the reports.

**H. Pairing by invite and check code.** Mcpmesh turns a one-time invite secret into an allowlist row on each side, and pairing needs a two-human check code. Each node writes its own row, so one pair is recorded twice. Local revoke then marks a device dead on that node only.

**I. Introduction by signed endorsement.** An already-paired peer can introduce a third peer with a signed endorsement. Mcpmesh's doc says this installs identity, not authorization, and that it turns O(N²) pairings into O(N). Authorization stays a separate step.

**J. Connection gate by shared secret.** Iroh-auth runs a SPAKE2 handshake before admitting a connection, binds both node ids into the transcript, and caches the result per node id. A failed handshake blocks that id, but the block lives in the same cache and disappears on eviction. A restarted process with a new key escapes it, which conflicts with the spec's ephemeral-key model.

**K. Allowlist by key after a token.** Iroh's auth-hook example checks a token on one stream, then uses the remote id as the allowlist key. Nothing in the examples compares the remote id with any payload identity. It is the simplest form of J, without the handshake.

**L. Per-request permission by EndpointId.** Iroh-rings keeps rings of EndpointIds with permissions and expiry, and checks each request against the caller's id. Its open ring grants read to every peer by design. The library does not say how the caller keeps the key.

**M. Signed capability chain.** Rcan verifies a chain of Ed25519 delegations from a principal key to the invoker, with strict verification at decode. It has no revocation and no replay protection, so a valid chain stays valid until expiry. Rcan checks only the chain, so the caller must authenticate the invoker.

**N. Single holder by OS lock or single owner.** Agent-gossip takes an exclusive OS file lock named after each nickname, retrying for 500 ms. Mcpmesh's redb lock refuses a second node on one root. Walkie and alink avoid a second holder by letting one daemon own the endpoint and routing other calls to it.

**O. Local suffix on name collision.** Walkie and alink add -2, -3, and so on when a name clashes with the local table. The check sees only local names, so a remote holder of the same name is invisible to it.

**P. Random word-word default names.** Agent-gossip generates nicknames as a random pair from a 1024-word list, which gives 1,048,576 names. The report describes no check beyond that space, so collision is left to chance.

**Q. Membership by shared secret.** Agent-gossip derives its mesh from a SHA256 of the join string, p2panda uses a 32-byte topic as the join key, and iroh-auth uses a password. In each, holding the secret gates the network, not a name. Iroh-gossip admits any peer that knows the topic id.

## Not found in the reports

- **Second live holder detection at runtime.** Only chio checks duplicates, and only at bundle load (i2). Iroh, the layer that would route two endpoints with one key, was not read by any report (i2 "Not read", f1a).
- **Probe, tie-break, and timestamp rules.** The spec's D6 is not implemented in chio or iroh-rings (i2). Agent-gossip has no identity-status field in responses (a1b, D30).
- **Collision check on nicknames.** None in agent-gossip or habilis (sp4). Issue #28 is the only report-level evidence (sp1).
- **Signed binding of a free handle to a key.** No surveyed code does it. Tunnet has no Claim type (p3a), and p1 says the spec's claim has no precedent.
- **Trust-on-first-use warning or key-change alarm.** No report describes one, except the disputed line below.
- **Rotation with name continuity.** Tunnet rotates by explicit command (p3a), but no report says what peers do on rotation.
- **Revocation of a leaked key.** Mcpmesh has local revoke and roster revocation (a2 §6). Iroh-auth's block list is lost on eviction (i1). Rcan has no revocation (i1).
- **E1 experiment.** Experiments/e1-api.md has no identity content. Its only name is an mDNS service name (line 55), which is discovery, not identity.
- **Protocol id collision.** Iroh's ProtocolMap overwrites a duplicate ALPN with no error (f1a, protocol.rs:391-394). This is protocol registration, not identity, and is noted only for completeness.

**Disputed or unverified:**

- **Nickname trust-on-first-use.** A1b says receivers bind a nickname to a key trust-on-first-use, citing protocol/identity.rs:11-12 and 27-30. Sp2 and sp4 say receivers deliberately do not pin, citing recv.rs:547-551. The reports do not reconcile these, and the recv.rs comment is the more specific source.
- **Production key generation.** A1b found only test call sites and did not locate the production one. Sp2 reports `Identity::generate()` in daemon setup at setup.rs:692, read on main at 8722df5. Sp3 says the engine site was not read at the pin.
- **Pinned version.** A1b, a3, and sp5 say the root pin is 795c4f8, which is not in the clone. Sp2 read main at 8722df5. Key-lifetime claims in row A hold at main and are unverified at the pin.
