# Human-readable names over keys

Date: 2026-10-16. Clones in /tmp/ra-state (shallow, `--depth 50`; history beyond 50 commits not seen).

| repo | commit read | dir |
|---|---|---|
| dstotijn/alink | b97d274 (2026-10-08) | alink |
| counterpunchtech/mcpmesh | 555dc1d (2026-09-14) | mcpmesh-m2 |
| agent-habilis/agent-gossip | 2c5e132 (2026-10-15) | agent-gossip |
| agent-habilis/habilis-network (engine under agent-gossip) | 8722df5 (2026-10-15); agent-gossip pins 795c4f88 (2026-10-14) | habilis-network |

Binding: cargo-cult-science, stop-yapping. Limits are in the last section.

Mechanism families found:

| | key | name owner | clash rule | stored |
|---|---|---|---|---|
| alink | endpoint id | receiver (local petname) | silent suffix `-2`, `-3` | SQLite, survives restart |
| mcpmesh | endpoint id | receiver (local petname), sender only suggests | refuse, invite survives, retry under alias | redb, survives restart |
| agent-gossip | none; the name is the roster key | sender (self-asserted) | not handled; issue #28 open | memory only, per session |

## Per project

### alink (local petnames, suffixing)

- **Source of a name.** Each node has `config.name`, default `{USER}-{hostname}` run through `sanitize_name` (`src/main.rs:339-349`). The name travels in the peer card (`src/proto.rs:197-203`, `PeerCard{v,id,name,handlers}`) and in the invite ticket (`ticket.name`). It is a suggestion only.
- **Sanitize.** `src/store.rs:673-691`: trim, every char outside `[A-Za-z0-9-_.]` becomes `-`, trim `-`, lowercase, empty becomes `peer`. Non-ASCII collapses to dashes.
- **Who picks the stored name.**
  - Inviter side: `accept_join` uses the name set on the invite when present, else the joiner's `card.name` (`src/node.rs:234`). The inviter can therefore name the invitee at invite time.
  - Joiner side: `join` uses `--alias` if given, else the inviter's `card.name` (`src/node.rs:513-545`).
- **Clash rule.** `upsert_peer` (`src/store.rs:148-179`): if the endpoint id already has a row, keep the old name and only refresh the card. Else take the sanitized base, and while `peer_by_name` finds a hit, try `base-2`, `base-3`, and so on. The column is `name TEXT NOT NULL UNIQUE` (`src/store.rs:20`), so the database also enforces it. Suffix order is first-come at this node. Nothing is told to the remote.
- **Stability.** Name lives in SQLite `peers` table. It survives restart. The key is the primary key (`id TEXT PRIMARY KEY`, `src/store.rs:19`). Name is the second column and unique.
- **Remote renames itself.** `fetch_card` calls `update_peer_card` (`src/store.rs:181`), which changes only the stored card. The local name is untouched. `peers show` prints `calls itself: <card.name>` next to the local name (`src/main.rs:626-642`).
- **Local rename.** `rename_peer` (`src/store.rs:234-245`): sanitize, then refuse with `a peer named "x" already exists` on clash. No auto-suffix here. Note the asymmetry: auto-suffix on insert, refusal on rename.
- **Addressing.** `resolve_peer` (`src/store.rs:212-229`): exact name first, then unique endpoint-id prefix. 1 hit works, 0 hits `unknown peer`, more than 1 `ambiguous`. A name wins over an id prefix, so a name made of hex characters shadows an id prefix.
- **Handler allow lists** accept names or ids (`src/config.rs:179-206`). A rename silently changes who matches a name entry; ids are stable. mcpmesh hit this class of bug and moved off names (see below).
- **Display aid.** `fingerprint(id)` prints `3F2A-91C0-7D4E-B812` (`src/main.rs:1391`) for human comparison of keys at join (`src/main.rs:567,576`).
- **Join authenticity.** `accept_join` refuses when `card.id != remote` (`src/node.rs:226`): the card id must equal the QUIC-authenticated peer id. So the name is attached to a verified key at insert.
- **Why, by their account.** Doc comment `src/store.rs:147`: "Adds or updates a peer, choosing a unique local name based on `preferred_name`." `sanitize_name` doc: "Peer names are used on the command line, so keep them shell-friendly." README line 117 and 244: peers name a handler, never the command. Git log has 7 commits, none about names. No issues read.
- **Tests.**
  - `src/store.rs:737` `peer_names_are_unique`: "Alice Claude" becomes `alice-claude`; a second peer `alice-claude` becomes `alice-claude-2`; `resolve_peer("b")` finds it by id prefix. **Ran it:** `cargo test peer_names_are_unique` passed (1 passed, 0 failed), log `/tmp/ra-state/m2-alink-test.log`.
  - `tests/e2e.sh:9-35`: two nodes `init --name alice-claude` / `david-codex`, join by ticket, `peers --json` shows names. Not run (needs binaries and network).
  - No test covers rename collision, remote self-rename, or hex-looking names.

### mcpmesh (local petnames, reject on clash, ids for authority)

Terms: "nickname" is the name. Docs call a stored name "display-only".

- **Source of a name.**
  - Self-name: `[identity].nickname` in config, else sanitized `hostname -s` (lowercase, `[a-z0-9-]` only, text before first `.`), else short base32 fingerprint of the endpoint id (`node/src/daemon.rs:1788-1817`). Live-changeable via `set_nickname`, persisted to config under a lock (`docs/local-protocol.md:181`).
  - Peer name: set once at pairing. Inviter stores `peer_nickname` alias if the invite carries one, else the redeemer's self-claim (`effective_redeemer_nickname`, `node/src/pairing/rendezvous.rs:356`). Redeemer stores `as_nickname` if given, else the invite's suggestion (`docs/local-protocol.md:170`).
- **Store.** redb table keyed by endpoint id; row is `PeerEntry{endpoint_id, nickname, services, paired_at, last_addr, user_id,...}` (`node/src/allowlist.rs:93-115`). Name is a column, not a key. Name uniqueness is NOT a storage constraint: `PeerStore::add` upserts by endpoint id, and `remove` deletes all rows with that name (`node/src/allowlist.rs:562-570`: "nicknames are NOT unique ... a conscious decision").
- **Clash rule: refuse, at pairing time, before any state change.**
  - Inviter: `nickname_collision` (`node/src/pairing/rendezvous.rs:1635`) scans `store.list()` for a row with the same name and a different endpoint id. Same id re-pair passes. Runs on the name that will actually be stored, via one shared helper `resolve_and_check_collision` (`:309-323`), used both before and after the invite burn so check and write cannot diverge.
  - Redeemer: `nickname_squat` (`:1657`) mirrors it before adopting the invite's suggested name. Fails "before any dial".
  - Order matters: the pre-check runs only after `peek_live_alias` shows the caller holds a live secret (`:777-805`). The comment says checking first "would let a stranger with a garbage secret probe which names exist". Unproven callers get the generic `pairing refused`.
  - Invite survives a collision refusal (#87). The redeemer retries the same invite with a new name (`docs/local-protocol.md:434-445`). A second check after the burn guards a race between two redeemers; there the invite is already spent and the loser must ask for a fresh one (`:1813-1830`).
  - Typed refusals: `-32043 ERR_NICKNAME_TAKEN` (inviter-side, retry same invite with a rename), `-32048 ERR_INVITE_NAME_CONFLICT` (redeemer-side, retry with `as_nickname`). Reason text names the action, not a control verb (#147).
  - Inviter's own alias colliding gives the generic refusal with no code, so the redeemer learns nothing about the inviter's private names (`collision_reply`, `:340-350`).
  - Stated cost in docs: a live-invite holder can enumerate which names exist on the inviter by retrying (`docs/local-protocol.md:441-446`). They bound it with a pair rate limiter and a warn log.
- **Stability.**
  - Peer name stored at pairing does not change when the remote renames itself. Docs: `set_nickname` is "Display-only: peers keep the nickname they stored at pairing time until a re-invite" (`docs/local-protocol.md:181`).
  - Local rename: `peer_rename` renames all of a person's devices (matched by `user_id`) or a provisional contact by nickname, refuses when the new name belongs to another contact, and runs under `reload_lock` (`node/src/daemon/handlers.rs:1180-1250`). No grant is rewritten.
  - Survives restart (redb). Pending invites with aliases also persist (`docs/local-protocol.md:169`).
- **Addressing.** `open_session{peer}` accepts a nickname, a `b64u:<user_id>` (races that person's devices), or `eid:<hex>` (exact endpoint) (`docs/local-protocol.md:190`). Nickname lookup is `entry_for`: `list().find(name == x)` (`node/src/allowlist.rs:517`). `list()` iterates redb in key order, so if two rows ever share a name the winner is the one with the lowest endpoint id, not first-seen. Docs say "first-match by name" (`docs/local-protocol.md:424-430`).
- **The settled rule: names never authorize.** Service `allow` lists hold stable principals only (`b64u:`, `eid:`, roster names); a bare nickname typed there is resolved to the principal at write time (#38; `docs/config.md:444`, `docs/local-protocol.md:164`). The inbound name given to services is `MCPMESH_PEER_NAME`, documented "**display only**; it collides and changes under a rename"; scope per-caller state on `MCPMESH_PEER_EID` (`docs/local-protocol.md:1590-1594`). Reason given in code: `nickname_collision` doc says it is "NOT a privilege defense anymore (#38)". The "0.7.x class of silent grant desync" came from names in allow lists (`docs/local-protocol.md:~425`).
- **Introductions.** `peer_introduce` installs a peer from a signed endorsement with a `nickname` chosen by the receiver, under the same collision guard; installs identity, not authorization (`docs/local-protocol.md:172`).
- **Why, by their account.** Quoted above: "display/routing clarity only"; "your own dials to that name would become ambiguous"; "a duplicate display name would make the inviter's own records ambiguous (status shows two peers as one, and outbound routing by name is first-match)" (`rendezvous.rs:1625-1634`). Issue numbers #37, #38, #87, #147, #159 are cited in code and docs; I did not read the issues themselves, only their citations.
- **Tests.**
  - `cli/tests/pairing_rendezvous.rs`: `collision_guard_allows_a_fresh_unique_nickname:447`, `..._allows_same_peer_re_pair:485`, `..._allows_same_peer_additional_service:517`, `collision_guard_refuses_impersonating_an_existing_peer:668`, `collision_refusal_preserves_the_invite_for_a_retry_under_a_new_name:743`, `redeem_refuses_an_invite_squatting_an_existing_peers_nickname:1010`, `an_inviter_side_alias_collision_says_nothing_to_the_redeemer:1297`, `both_sides_store_their_own_local_alias_after_a_real_pairing:1586`, plus a no-oracle test near `:784-828`.
  - `cli/tests/presence.rs:308` `dial_by_eid_targets_the_exact_endpoint_despite_a_nickname_collision`: two stored peers named "twin"; `eid:` dial reaches the right one.
  - Unit: `node/src/control.rs:1751` `a_nickname_collision_answers_err_nickname_taken`; `node/src/pairing/rendezvous.rs:1686-1850` refusal-wire tests; `node/src/daemon.rs:2140` `sanitize_hostname_makes_a_friendly_nickname`; `node/src/daemon/handlers.rs:7424` rename-all-devices test.
  - **Ran:** `cargo test -p mcpmesh-node --lib nickname` — passed (11), see "Test run log". Integration tests in `cli/tests` need two iroh endpoints; not run.

### agent-gossip (nickname is the roster key; identity is a separate signing key)

Mechanics live in the engine `habilis-network`. agent-gossip pins it at rev 795c4f88 (`Cargo.toml:47`). I read the clone at 8722df5; the roster fields I cite exist unchanged at 795c4f88 (`daemon/state.rs:342` `peer_endpoints: HashMap<Nickname, EndpointAddr>`; `gossip/recv.rs:550` same pin comment). Line numbers below are 8722df5.

- **Source of a name.** Self-chosen at join or create. `--nickname` flag, else `Nickname::random()` = two words from a 1024-word list, `word-word` (`habilis-network-protocol/src/nickname.rs:84`, `wordlist.rs:5,116`; about 1.05 million pairs). Nothing checks the random pair against the live roster. Charset: 1..=32 Unicode scalars, any script and emoji; rejects control chars, whitespace, bidi formatting, `/ \ < > #` (`nickname.rs:1-80`). Validation also runs on deserialize, so a hostile frame cannot inject a name (terminal injection, `<nick>`/`#mesh` display forms).
- **Roster.** `peers: HashSet<Nickname>`, `last_seen: HashMap<Nickname, Instant>`, `peer_endpoints: HashMap<Nickname, EndpointAddr>` (`daemon/state.rs:333-352`). Updated on every authenticated frame: `lifecycle::observe` inserts/refreshes by `message.author` (`lifecycle/mod.rs:58-110`). `Left` removes the name and its endpoint (`lifecycle/mod.rs:~140-175`). Silence beyond `ALIVE_TIMEOUT` evicts to a `quiet` set. `peer_endpoints` is last-writer-wins, "a restart re-advertises a new endpoint under the same name" (`state.rs:344-350`). The signed `PeerInfo` is "the only thing tying a nickname to an endpoint".
- **Two keys, one name.** Engine verifies the signature against the key in the frame, drops self-echo by public key not nickname, and states: "the `author` nickname is a non-unique display label and is deliberately **not** pinned/claimed, so a nickname is never 'burned' by a restart" (`gossip/recv.rs:497-552`). `docs/identity-binding.md:21-35` repeats the motivation: pinning would stop a restarted peer reclaiming its name and "the useful names are consumed by ghosts".
- **Identity key lifetime.** Ed25519 key is in-process and ephemeral, new per create/join (`habilis-network-protocol/src/identity.rs:12-18`). A restart is a new identity under the same nickname. Cards in the shared meta doc at `/peers/<nick>/card` of a crashed peer persist until a later session under that nickname overwrites them (`agent-gossip/src/a2a/node.rs:318-330`).
- **Addressing.** A directed send takes `to: Nickname`. Sender looks up the recipient's x25519 seal key at `/peers/<nick>/card` in the replicated meta doc and refuses to send plaintext if it is missing ("cannot seal to 'x': its encryption key is not known yet (cards still propagating)", `a2a/send.rs:854-875`). Endpoint hint comes from the same card. Task creation fast-fails `unknown peer '<nick>'` when the name is not in `state.peers()`, unless a live task with that name exists (`a2a/send.rs:1618-1641`). Receiver gates directed frames on `to == self_author`.
- **Known clash behavior (documented as a defect).** Issue #28 (open, filed 2026-09-30; read via a web fetch summarizer, see limits) lists: roster keyed by nickname so a second key under a known name fires no `joined`; a `Left` from either holder removes the name for both; the meta gate checks by nickname so both can write and retract `/peers/<nick>/card`; a second daemon on one host with the same nickname takes over `<nick>.ipc.sock`. Two designs parked from PR #27: (1) a `NickTaken` signed broadcast, a claim table, a probe that evicts a dead predecessor after about 3 s, protocol 13.0 (reviewers: probe can evict a slow live holder; wall-clock claim order; slow ready gate for a lone joiner); (2) no new frame: drop frames from a second key while the first is live, joiner refuses itself on seeing the holder's `Joined` in its first digest round, session signing key persists so a rejoin is not a conflict, emit `nickname_conflict` on partition merge and evict nobody.
- **Restart/rejoin.** Issue #29 (open): after a daemon crash the agent rejoins under the same nickname, name kept "in the agent's context ... nothing is written to disk"; the dead key stays in rosters about 90 s, so keeping the session signing key would avoid being refused as a duplicate. Depends on #28. Open tasks resume on a same-name, same-key `peer_return`.
- **Choosing a name.** Issue #40 (open, 2026-10-11): the `gossip-join` skill drops `--nickname`, so users get random names; a nickname "can't be changed after joining"; named roles like `net-lead` help orchestrated meshes. In code, a repeat join on the same mesh succeeds only if the nickname matches the existing one, else error `already in gossip` (`src/mcp/mod.rs:1042-1053`).
- **Security gap, written down.** `docs/identity-binding.md`: every A2A party check, the seal key, and the endpoint hint compare nicknames, but nothing binds `author` to `pubkey`. An attacker rewrites `/peers/alice/card` with their own key and receives all sealed traffic for alice. A per-node first-writer pin is rejected as wrong: it blocks legitimate rejoin with a fresh key and "converges nowhere" (each node pins what it saw first). Their leading direction: keep the nickname as a cheap display label and give authorization paths a separate key-addressed identifier (`docs/identity-binding.md` section "What the real fix looks like"). Note a contradiction inside the engine: `identity.rs:9-10` says the nickname is "bound to it trust-on-first-use by the receiver", while `recv.rs:550` says it is deliberately not pinned. I did not find the TOFU code; the recv.rs comment matches the code I read.
- **Tests.**
  - `crates/agent-gossip/tests/adversarial.rs:795` `gap_nickname_impersonation_is_accepted`: `#[should_panic(expected = "OPEN GAP")]` tripwire; attacker posts under victim's nickname with its own key and the victim surfaces it. Doc says its going red marks the note obsolete.
  - `tests/mcp_stdio.rs:495-520` `join_mesh_idempotent_for_same_mesh`: same nickname returns the same handle, different nickname errors `already in gossip`.
  - `tests/shared_state.rs:618` `meta_entry_returns_after_rejoin`: leave retracts `/peers/<nick>`, rejoin under same nickname with fresh key republishes the card.
  - `tests/mcp_stdio.rs:1140-1161`, `tests/task.rs:174`: unknown-peer task creation fails fast.
  - `habilis-network-protocol/src/nickname.rs:100-` unit tests: valid and invalid charsets, 32-char cap counts characters.
  - No test exercises two live holders of one nickname (consistent with #28 open). Not run: these are multi-node iroh tests with a large dependency build; the engine alone is 436 crates.

## Options this gives estafette

Spec context: D5 (first-seen suffixing, kept for session, announce effective handle), D29 (address = effective handle only), 3.8 handle paragraph (each node assigns from what it saw first; two nodes can name one member differently within a propagation window).

1. **Receiver-local petname with first-come suffix, stored per card key.** What: each node maps `card key to name`, suggestion comes from the peer, clash gets `-2`, `-3`. Cost: lowest. Matches D5 and 3.8 as written. Proof: alink (`src/store.rs:148-179`). Difference to note: alink persists the name on disk and keeps it across restarts. Estafette's table is in memory, so a restarted node can re-assign different suffixes to the same peers. Keying the name to the card key instead of the node key keeps a peer's name when its process restarts with the same card, but only for this node's lifetime.
2. **Refuse on clash, with a retry path.** What: at admission a name already held by another key is rejected and the sender picks another. Cost: needs an admission handshake with a reply channel, which presence over gossip does not have; fits poorly with "no center". Proof: mcpmesh pairing (`rendezvous.rs:309-350`). Estafette's D5 explicitly rejects network-wide refusal because a stranger could block a name; mcpmesh avoids that by refusing only after a secret proves invitation, and by making the name receiver-local anyway.
3. **Sender suggests, receiver owns, authority never keys on names.** What: the name in presence is a suggestion; every trust decision uses the key. Cost: zero extra state. Proof: mcpmesh #38 (names removed from allow lists after "silent grant desync"; `docs/local-protocol.md:1594` "display only"), agent-gossip `docs/identity-binding.md` (authority on nickname is the live gap). Estafette's D29 says "Fingerprints and keys are internal", so the send tool must resolve handle to key at call time and the result should return the key fingerprint it used, so a later reuse of the handle by another member cannot silently retarget a retry.
4. **Dual address: name or exact key.** What: accept the name and also an exact-key form (`eid:<hex>`) in `to`. Cost: reintroduces keys in agent text, which D29 rejects as noise. Proof: mcpmesh `open_session` accepts `eid:` and `b64u:`; its test `presence.rs:308` exists because name dials can be ambiguous. alink accepts a unique id prefix. Option only if D29 is revisited; ambiguity today is handled by `ambiguous_handle` (spec line 724).
5. **Show the sender-chosen name next to the local one.** What: keep both `local handle` and `calls itself X`. Cost: one extra field. Proof: alink `peers show` ("calls itself", `src/main.rs:640`). Helps an agent notice a rename; mcpmesh and alink both leave the local name unchanged when the remote renames.
6. **Name fixed for the session by first seen, announce the effective handle, no negotiation.** What: D5 as written. Proof: no repo implements exactly this. alink and mcpmesh assign locally at pairing (persisted); agent-gossip does not assign at all. The closest point: all three keep a peer's name stable while the peer exists, and none rename an existing entry on a later clash.
7. **Avoid what agent-gossip shows going wrong.** A name-keyed roster collapses two members that pick one name (no `joined`, shared `Left`, shared meta entry). Estafette keys the peer table by card, so this cannot happen at the table level. Keep it that way for any shared structure (inbox, dup set) too.
8. **Name charset.** alink: `[a-z0-9-_.]` after sanitize. mcpmesh self-name: `[a-z0-9-]`. agent-gossip: any Unicode, with explicit bans on bidi, controls, `/ \ < > #`, and validation on deserialize. Estafette's `^[a-z][a-z0-9-]{0,31}$` is inside all three. Wire-side validation of inbound handles, not only local input, is the agent-gossip lesson (terminal-injection note in `nickname.rs`).
9. **Random default names.** agent-gossip's 1024-word pair list gives about 1.05 million names and issue #40 shows users prefer chosen role names. A random default avoids most clashes; it does not remove them (no roster check).

## What could make this wrong

- **Shallow clones.** Depth 50. "Why" from git history is limited to what is in 50 commits (alink has only 7). I saw no commit messages on naming in alink. mcpmesh issue numbers (#37, #38, #87, #147, #159) come from code comments and docs; I did not read the issues. A comment can be stale: mcpmesh docs themselves note an earlier paragraph "was stale".
- **Issues #28, #29, #40 were read via a web fetch tool that summarizes the page with a small model.** Quotes in the issue bullets are the tool's paraphrase, not verified verbatim. All three show no comments in that output. They are open, so the "clash handling" in agent-gossip is a described desire, not shipped behavior. `gh issue view` returned nothing in this sandbox.
- **agent-gossip mechanics come from a different repo.** Roster and keying are in `habilis-network` (a fork, `FORKED.md`, divergence at f81b0529). I read 8722df5; agent-gossip pins 795c4f88. I confirmed the same fields and the same pin comment at 795c4f88 (`state.rs:342`, `recv.rs:550`) and a 4-file diff touching recv/heartbeat/lifecycle between the two. I did not diff the behavior of those files. Line numbers are 8722df5 except where stated.
- **The engine contradicts itself on pinning** (`identity.rs:9-10` TOFU versus `recv.rs:550` not pinned). I read the recv.rs path only.
- **mcpmesh coverage.** I read pairing-mode names (redb, nickname). Roster mode (org rosters with `display_name`, `device_label`, gossip presence) has its own naming and I read only its docs lines, not code. Nobody in these three repos has presence-gossip with receiver-assigned suffixes like estafette's D5, so option 1 and 6 are adaptations, not copies.
- **Persistence differs.** alink and mcpmesh store names on disk, so "stable across restart" there rests on a database. Estafette's peer table is in memory: restart behavior of names has no precedent in these three for receiver-assigned names. agent-gossip is the only in-memory case and its name is sender-chosen.
- **Test claims.** Only the alink unit test was run by me; the mcpmesh run is below. Other tests were read, not executed. The mcpmesh two-node tests could fail or pass for reasons I did not check.
- **hex-shadowing and list-order claims** (alink name vs id prefix; mcpmesh `entry_for` picks lowest endpoint id) come from reading code, not from a test. redb iteration order by key is my reading of the table definition and comments, not run.

## Test run log

- alink: `cargo test peer_names_are_unique` — `test store::tests::peer_names_are_unique ... ok`; `1 passed; 0 failed; 12 filtered out`.
- mcpmesh: `cargo test -p mcpmesh-node --lib nickname` at 555dc1d — `11 passed; 0 failed; 535 filtered out` (log `/tmp/ra-state/m2-mcpmesh-test.log`). These are unit tests only (store, handlers, control, refusal-wire). The two-endpoint pairing and presence tests in `cli/tests` were not run. Names of the 11:

```
test daemon::tests::sanitize_hostname_makes_a_friendly_nickname ... ok
test daemon::handlers::tests::an_alias_is_validated_the_same_way_a_nickname_is ... ok
test control::tests::a_nickname_collision_answers_err_nickname_taken ... ok
test audit::log::tests::a_live_session_is_keyed_on_the_principal_not_the_nickname ... ok
test allowlist::tests::gate_resolves_known_nickname_refuses_unknown ... ok
test daemon::handlers::tests::redeem_validates_as_nickname_before_it_touches_the_invite_line ... ok
test allowlist::tests::remove_deletes_all_entries_sharing_a_nickname ... ok
test daemon::handlers::tests::peer_nickname_is_refused_with_a_multi_use_invite_and_when_blank ... ok
test daemon::handlers::tests::peer_diagnostics_joins_the_live_row_by_id_not_nickname ... ok
test blobs::provider::tests::pairing_mode_eid_grant_admits_and_nickname_grant_stays_denied ... ok
test daemon::handlers::tests::a_peer_nickname_is_stored_but_never_travels_on_the_line ... ok
test result: ok. 11 passed; 0 failed; 0 ignored; 0 measured; 535 filtered out; finished in 5.25s
```
