# Spec apply report: S1-S27 into spec/blueprint.md

Applied 2026-10-21 by spec-apply (claude-opus-5-5) on the owner's word "apply current changes, carefully" (journal 2026-10-21 14:35). Not committed. Sources read whole: spec/blueprint.md, research/stack/staged-revisions.md, research/stack/ledger.md, research/stack/parameters.md, experiments e12, e13, e15, e17, e18, e19, e20, e21; owner rulings from docs/orchestration_log/history/2026-10-15/events.md lines 196-333. C17's E16 patch not applied (ruled not carried).

## Per S id

| S | Spec sections changed | Source |
|---|---|---|
| S1 | 3.5 (cap 3072, compact JSON), 3.7 (3072), 3.14 (public 3072, gossip frame 4096), test 17 (size test) | staged S1/S9; owner 2026-10-20 19:20 |
| S2 | 3.14 QUIC idle timeout 10000 ms; 3.6 transport line | staged S2 |
| S3 | D47 (new, 2.12); 3.2 manifest (iroh-relay optional under `relay`); 3.14 | staged "Stack D-records"; e11 tree counts (rerun: 280 / 320 unique, e11 says 321) |
| S4 | D48 (new); 3.5 converter rules; 3.2 manifest | staged; ledger row 24 |
| S5 | 3.1 hex for card public key, secret, network secret, fingerprint; node id = card key in iroh's form; 3.3, 3.13 hex forms | staged S5 |
| S6 | D13 (presence authenticated, not encrypted) | staged S6 ("1.6 or D13": D13 chosen) |
| S7 | D49 (new) with the C18 patch; 3.2 manifest | staged; owner 2026-10-21 12:30 (C18) |
| S8 | D50 (new) | staged; owner 2026-10-21 14:20 "Keep the decision"; v3 via ledger |
| S9 | 3.7 size check before broadcast, error on refusal; 3.16 line | staged; owner 2026-10-21 14:24 |
| S10 | 3.6 connection reuse, server read timeout, stream reset; 3.10 send step 4; 3.14 server read timeout | staged S10/S19 |
| S11 | D25 replaced by "No duplicate suppression"; 3.6 step 7 removed; 3.14 duplicate set removed; test 17 removed | staged S11 |
| S12 | 3.1 seq term; 3.7 seq on Presence and Departure, ts kept on Unreachable; 3.8 announcement ordering paragraph, tombstone, seq generator; 3.14 max age 300 s; test 20 | staged S12; owner 2026-10-20 19:06 |
| S13 | 3.8 row "home relay status changes, or own address set changes" | staged S13 |
| S14 | 2.2 (claim, transport key removed; member, node, presence redefined); D2, D3, D4, D5 (word), D6, D7, D10, D17, D30, D32; 3.1; 3.4 (Claim, tie-break, probe-replacement removed; payload signature added); 3.6 (Message, Introduce, ProbeAck, IntroduceAck without claim; validation); 3.7; 3.8 (tie-break rows removed); 3.9 (Displaced removed); 3.10 (`held`, `card_held`, `displaced` status, init); tests 6, 9, 10, 13, 18; 3.16 | staged S14 |
| S15 | 3.8 init row (Presence after joined); D18 sentence | staged S15 |
| S16 | D13; 3.1 gate key; 3.4 derivation and entropy note; 3.6 gate paragraph; 3.14 gate timeout; test 21 | staged S16; owner 2026-10-20 19:06 "Hook, both ways" |
| S17 | D19; 3.8 stop row; 3.9; 3.14 departure wait 5000 ms; D2 (lock release, see contradiction 3) | staged S17 |
| S18 | D22 ("never that it was read"); 3.11 paragraph | staged S18 |
| S19 | 3.10 send algorithm (drop held connection, no retry); 3.16 line | staged S10/S19 |
| S20 | 3.6 Addr, Introduce and IntroduceAck carry addr; 3.7 Presence addr; 3.8 address lookup (replace, never merge); 3.10 send step 4; 3.3 hosts; 3.13 invitation host addresses; D15 removed, mDNS added to 2.13 Deferred; 3.6 "no pkarr, no DNS, no local discovery" | staged S20; owner 2026-10-20 19:06, 19:24 "No n0 at all" |
| S21 | 1.7 ("the fixed places"); 2.2 host, host address, infrastructure record; D14, D42, D43; 3.3 config `hosts`, atomic rewrite; 3.6 relay map from known hosts; 3.7 Infrastructure payload; 3.8 known hosts, Infrastructure row; 3.13 join network, show invitation, run infrastructure; 3.14 infrastructure process, record interval; tests 22, 25, 26 | ledger S21; e21; owner 2026-10-20 19:10 |
| S22 | G1-G4 (22 values) and the six implementer's calls: Part 3 intro (calls), 3.1 (#1, #2, #9, #12), 3.3 (#10, #11, #13, #15), 3.5 (#3, #4, #14), 3.6 (#5, #6, #7), 3.7 (#8), 3.8 (#19), 3.9 (#16), 3.10 step 3 (#6), 3.11 (#17, #18), D40 and 3.13 (#20), 3.13 (#21, #22) | parameters.md; owner 2026-10-20 19:32 |
| S23 | G5 (#23-29): 3.10 (result form, error order, `since` schema, unknown tool, non-object arguments, rmcp build, server name), 3.1 key order, D30 sentence, 3.2 manifest | parameters.md G5; owner 2026-10-20 21:40 |
| S24 | D45 (new); 3.8 relay-loss row; Infrastructure row re-adds a removed relay; 3.14 relay-loss wait 500 ms; test 28. Rejoin lever not applied (replaced by S26) | ledger S24; e12 L1 |
| S25 | D19 sentence; 3.9 (own stdin reader, SIGTERM order, background shutdown); 3.10 transport line; test 4 | ledger S25; e13 |
| S26 | D46 (new; trigger per owner ruling 2026-10-21, relayed by team-lead); 3.8 deaf row, member-join row, Rebind paragraph, join timeout in init row; 3.14 deaf timeout (15 s, pending), rebind interval, join timeout, relay probe timeout, member join wait and interval; tests 23, 24 | ledger S26; e15, e17, e18, e19, e20; owner 2026-10-21 12:30 "Full fix" |
| S27 | D44 (new); D16 sentence; 2.2 owner key; 3.1 owner key; 3.3 `owner`, owner key file, infra cert file; 3.4 host certificate; 3.7 Infrastructure checks; 3.13 certify host, invitation carries owner key; 3.14 certificate requirement; 3.16 line; test 27 | ledger S27, C19; e21 H4; owner 2026-10-21 12:34 |
| Relay TLS | D51 (new, marked pending a two-machine check); 3.14 HTTPS by ACME; 3.13 run infrastructure takes a domain name | owner 2026-10-21 14:35 |
| C18 | D49 and 3.2 manifest: `[patch.crates-io]` copy with PR #161's on_join line | owner 2026-10-21 12:30 |

All 27 S ids applied; none skipped as not applicable.

## Judgement calls

1. D7: staged gave only the title and a parenthetical; Reason and Rejected are mine.
2. D5 "If you change this": "a claim can be refused" became "a card can be refused".
3. D2 "If you change this": "claims cannot be verified" became "a node cannot prove its card".
4. D25 kept as a record ("No duplicate suppression") instead of deleted, so the reason staged under "Reason to record" has a home and the D numbers stay stable. D15 deleted outright (its number left unused).
5. New D-records numbered D44-D51; D44-D46 sit in 2.5 Network, D47-D51 in a new 2.12 Stack; Deferred renumbered 2.13.
6. Message carries a new `handle` field. With `from: Claim` gone, an unknown sender has no handle for the peer table or the inbox `from`, which D17 and test 8 require. Alternative not taken: the receiver sends Introduce and waits for the answer before enqueuing.
7. Addr wire shape (`relays: Vec<String>`, `direct: Vec<String>`) is mine; S20 names the content, not the encoding.
8. Introduce carries `addr` as well as IntroduceAck: staged S20 names IntroduceAck, the ruling (2026-10-20 19:06) says "every Presence and Introduce".
9. Signature and mac order: sign with `sig` and `mac` zeroed, then mac; verify mac first. Not stated anywhere.
10. Host certificate signs the raw 32-byte host id; E21 prefixed a domain string ("e21-cert"). No domain separation added.
11. Row "Presence or Departure received for your own card: ignore". Staged removed the old own-card row and gave nothing in its place; without a row a replay of your own old Presence inserts you as a peer.
12. Introduce and IntroduceAck skip the seq check (they are direct, TLS-bound contacts and carry no seq).
13. Init order: lock, endpoint, subscribe, joined, observer wait, own handle, Presence, return. list_cards has no observer wait (staged), so the observer wait moved after the join.
14. Join timeout (5 s, rebind on failure) applies to the first join at init too, as in E18's harness.
15. Rebind interval (20 s) binds only silence-caused rebinds; a join timeout rebinds at once (E15/E18 harness: JOIN_FAIL rebinds without the debounce).
16. Rebind keeps the peer table, lookup, known hosts, seq, inbox, socket, lock. No source states it; it follows from "binds a fresh one with the same key".
17. Member join targets "the cards of the Online entries" (E20 used the harness's fixed member list; E20 notes "needs a member list in the product").
18. Relay probe: TCP connect with 1000 ms timeout, as E17's C2. Relay-loss wait 500 ms, as E12's L1 debounce (E12 calls it "a guess", untuned).
19. Infrastructure record broadcast "when joined and every 5 s", from E21's host design; the ledger row does not state the interval. Without it a later joiner never learns hosts it did not meet.
20. Infrastructure host joins through the other configured hosts and keeps its own relay only in its relay map (E21).
21. Learned hosts saved by atomic rewrite of the config file (several sessions on one machine write it).
22. Operator functions added: `show invitation`, `certify host`; `join network` also takes a host address line (G4 #22 "accepted by join"); `run infrastructure` takes a domain name (ACME); infra cert file `<data>/infra/<network>.cert`; owner secret key file `<config>/networks/<network>.owner.key`; without a valid certificate run infrastructure prints its host line and exits.
23. Invitation carries the owner public key (G4 #21 predates S27).
24. Tests: 9 lost its claim half; 10 replaced by a payload-signature test; 13 lost "after displacement"; 17 slot reused for the size test (numbers kept stable for ledger references); 21-28 new. Bounds I chose: test 22 1000 ms (measured 24-163 ms), test 23 60 s (measured 14-35 s), test 28 2000 ms (measured 0.7 s), test 25 "within the observer wait" (measured 105-216 ms), test 18 "one second" (staged).
25. Gate test 21 added though staged lists no test for S16.
26. 3.16: "Do not accept a Message whose claim node differs" became "Do not take the sender of a Message from anything but the connection's remote id"; added "Do not accept an Infrastructure payload whose certificate the owner key does not verify".
27. D16 gains a sentence naming infrastructure records as the exception (ledger S27 lists D16).
28. D19 carries the S25 reason (S25's rows name 3.8, 3.9, 3.14, S17; D19 is S17's record).
29. D13 Rejected gains "Encrypted presence: the gate already keeps outsiders out", from staged S6's parenthetical.
30. D44 Rejected causes: E21 lists the two alternatives as "not tried"; the causes given are mine.
31. D51 Reason and Rejected are mine; the ruling gives only the condition ("if low-effort high-benefit"). No ACME evidence exists in the research; the record says pending.
32. Manifest table: versions in parentheses are the e11 draft lockfile's resolution, not rulings; toml and yaml-rust2 stay `*` as drafted; postcard `=1.1.3` is the draft's pin, not a ruling.
33. 1.7 "the one fixed place ... holds" became "the fixed places ... hold" (S21: several hosts). Part 1 is not in any S row's section list.
34. D-record evidence lines cite measured numbers from the ledger and reports (D3, D6, D13, D14, D19, D45, D46, D47, D49).

## Contradictions

1. RESOLVED by owner ruling (relayed by team-lead, 2026-10-21). S26's trigger "no Presence from any peer for 3 s" contradicted D18 and 3.16 "Do not send a Presence on a timer": it was measured with 1 s application heartbeats (E15-E21 harness), and in a quiet product network it would rebind every idle member every 20 s. Ruling: a member is deaf when it has heard no gossip message from anyone for 15 s, and then it rebinds; this replaces "no Presence for 3 s"; the 20 s debounce and the rest of S26 stay as staged; the 15 s value is pending a measurement (team-lead dispatching it). It works because each bootstrap node rebroadcasts its signed infrastructure record every 5 s (S21). Applied: D46 Decision (deaf rule, the D14 dependency, pending mark), 3.8 row (any gossip payload, deaf timeout, the dependency), 3.14 (deaf timeout 15 s pending, must stay above the 5 s record interval; rebind interval wording). The 2.13 Deferred entry added earlier is removed. Remaining notes: D46's evidence was measured at a 3 s trigger, so heal times at 15 s are unmeasured (test 23's 60 s bound may need revisiting after the measurement); with every host dead a member hears nothing and rebinds every 20 s, which is expected, since its joins fail anyway.
2. RESOLVED. Staged S20 says IntroduceAck carries `addr`; the ruling says every Presence and Introduce. Both Introduce and IntroduceAck carry it.
3. RESOLVED. Staged D2 "holds it for the life of the process" against S17 "release the sidecar lock" at stop. D2 now says the lock is held until Stopping releases it.
4. OPEN. list_cards learns `held` by trying the lock and releasing it at once (staged); an init on another process during that instant gets `card_held` falsely. Not in any staged text.
5. OPEN. Address size is unbounded: `public` is capped at 3072 bytes, but an address with many direct addresses can push a Presence past the 4096-byte frame; S9 then refuses it and the member goes silent. Staged S1 asks for a size test at application (test 17); no cap on the address is ruled.
6. OPEN. Replay of an old Infrastructure record is unchecked (ruled). With D45, a replay of a dead host's record re-adds its relay, and traffic toward a dead relay is what triggers the C16 block.
7. OPEN. Known hosts only grow: no rule removes a dead host from the configuration.
8. OPEN, pre-existing. The invitation must hold one or more host addresses (G4 #21), but create network runs before any host exists. `show invitation` prints a later one; the first host's own bootstrap is not specified.
9. NOTE. Hosts run no rebind (E21: "Hosts run no W1; a real host that joined through A would be exposed to C16"). Not ruled either way; the spec gives hosts none.
10. NOTE. D45 (S24's remove_relay) stays as ruled, though E14 shows removal does not clear the C16 block and E15 could not separate L1's effect on W1 (A3 vs A2). Its measured benefit is the 0.7 s re-home only.
11. NOTE. I2 "No component has authority over members": the owner key is an authority over hosts' records, not over members; consistent as read.
12. NOTE. Tree count: rerun of `cargo tree -e normal` on the e11 lockfile gives 280 unique crates without `relay` and 320 with it; e11 reports 321.

## git diff --stat

```
 .../orchestration_log/history/2026-10-15/events.md |   1 +
 spec/blueprint.md                                  | 499 +++++++++++++--------
 2 files changed, 321 insertions(+), 179 deletions(-)
```

The events.md line was modified before this work began (present in the starting git status); not mine. spec/blueprint.md at first delivery: 320 insertions, 179 deletions. After the deaf-trigger ruling and the team-lead decisions: 377 insertions, 185 deletions (git diff --numstat), final, after option (i), follow-ups a-c, both reviews, E22, E23, and the host deaf window. This report file is new and untracked.

## Accounting

S1 applied, S2 applied, S3 applied, S4 applied, S5 applied, S6 applied, S7 applied, S8 applied, S9 applied, S10 applied, S11 applied, S12 applied, S13 applied, S14 applied, S15 applied, S16 applied, S17 applied, S18 applied, S19 applied, S20 applied, S21 applied, S22 applied (22 values, 6 calls), S23 applied (7 values), S24 applied (removal part only; rejoin lever replaced by S26), S25 applied, S26 applied (trigger per owner ruling: deaf after 15 s, pending measurement), S27 applied. Relay TLS applied as pending. C18 applied. C17 patch not applied, as ruled.

## Decided by team-lead 2026-10-21, reversible

Each with its single closest alternative. These supersede contradictions 4-9 and judgement calls 7 and 10 above.

1. list_cards probe race (contradiction 4). Init retries the lock for up to 200 ms before `card_held`. Spec: D6, 3.10 init row and `card_held` row, 3.14 "lock retry window 200 milliseconds". Alternative: list_cards reads a pid written in the sidecar instead of probing.
2. Address size (contradiction 5). Decided (team-lead, option (i)): direct addresses are binary socket addresses (postcard's encoding of `SocketAddr`), at most 8; relay URLs at most 4, each at most 128 bytes. A node carries the first ones its endpoint reports up to the caps; a receiver drops a structure whose Addr exceeds a cap. Spec: 3.6 Addr struct and "Address caps" paragraph, test 17. Alternative: (ii) text addresses with relays 2 x 128 and direct 8 x 47 (3913 bytes).
   Arithmetic (postcard, worst case; frame 4096, gossip overhead 38 bytes per E2, so a payload may use 4058):
   - outside Addr: variant 1 + `v` 1 + `card` 32 + `handle` 1+53 + `public` 2+3072 + `attached` 1 + `seq` 10 (u64 varint max) + `mac` 32 + `sig` 64 = 3269
   - relays: 1 + 4 x (1 + 128) = 517
   - direct: 1 + 8 x 20 = 161 (per address: variant tag 1 + IPv6 octets 16 + port varint at most 3)
   - Presence = 3269 + 517 + 161 = 3947 <= 4058; 111 bytes of headroom.
   - the first caps proposed (direct as text, 8 x 128) gave 4819, 761 over; not applied.
   Note: std's serde form of a V6 socket address carries no flowinfo and no scope id, so a link-local IPv6 address loses its scope. Read from std's serde behaviour, not measured. Resolved by team-lead 2026-10-21: a node leaves link-local IPv6 addresses (fe80::/10) out of Addr (3.6 Address caps), so the lost scope id cannot matter. Alternative: carry the scope id in a field of its own.
3. Record replay (contradiction 6). A member holds the newest `ts` per host id and drops a record whose `ts` is not newer. Held in memory only: a restarted member accepts one replay of a record older than what it saw before. Spec: D44, 3.7 field comment, 3.8 two Infrastructure rows, test 27. Alternative: accept replays.
4. Hosts only grow (contradiction 7). A learned host not heard for 30 days leaves the configuration at the next rewrite; hosts from the invitation or join network carry no `heard` key and are never removed. Spec: D44, 3.3 config example and rewrite rule, 3.14 "infrastructure record expiry 30 days". Alternative: never remove.
5. First host (contradiction 8). Spec 3.13 gains an explicit order: create network, run infrastructure on the first host (first run prints its line and exits for want of a certificate), certify host, run infrastructure again (alone, its own bootstrap), join network with its line on the owner's machine, show invitation; 3.14 states that a host with no other host subscribes alone. My additions to the given order: the certificate steps 3-4 (needed by S27), step 5, and "copy the configuration file to the first host, never the owner key file". Alternative (closest, mine; none given): the invitation may name zero hosts for infrastructure machines.
6. Hosts and rebind (note 9). Hosts apply the deaf rule and rebind as members do. Spec: D46, 3.14. Consequence: a lone host with no member hears nothing (gossip does not deliver its own broadcasts) and rebinds every 20 s until a member joins. Alternative: hosts never rebind.
7. Signature domains (judgement call 10). The certificate signs `"estafette-host-cert-v1" || host id`; the Infrastructure signature covers `"estafette-infra-v1" || encoding`. Reason: a signature over a raw id can be reused in another context. Spec: 3.4. Presence, Departure, and Unreachable signatures carry no prefix; not covered by the decision. Alternative: raw id and raw encoding, as before.

### Follow-ups, team-lead 2026-10-21, reversible

a. Deaf rule needs a known other node. Silence counts only while the node knows at least one other node: another host among its known hosts, or an Online peer. A node that knows none never rebinds on silence, so a lone host no longer rebinds every 20 s (supersedes the consequence noted under decision 6). Spec: D46, 3.8 deaf row. Alternative: a host that knows no other host never rebinds.
b. Every gossip signature domain-separated. Presence `estafette-presence-v1`, Departure `estafette-departure-v1`, Unreachable `estafette-unreachable-v1`, Infrastructure `estafette-infra-v1`; the certificate keeps `estafette-host-cert-v1`. Spec: 3.4 table of signer and prefix. Alternative (mine; none given): prefixes on the certificate and the Infrastructure payload only, as in decision 7.
c. Replay state persisted. Each host in the config may carry `ts`, the newest accepted record `ts`; a process loads these at start. Spec: D44, 3.3 example and rewrite rule. Alternative: in memory only.
   My addition: the file is rewritten only when a host is learned, so the saved `ts` can lag what the process held. To narrow that, a process also rewrites the file on entering Stopping if it holds a newer `ts`. A crash (no Stopping) still loses the newer values, and between the last rewrite and a crash a restarted member accepts each host's records newer than the saved `ts` but older than what it last saw: at most the records of that window, all genuine and signed. Not closed, because persisting every 5 s record would rewrite the config every 5 s.

## Review fixes

Source: research/stack/spec-review.md (4 high, 10 medium, 10 low), read whole. Reviewer's fix taken unless noted. 23 fixed in the spec, 1 left open (L10).

| Id | What changed | Alternative |
|---|---|---|
| H1 | A bootstrap node counts only other hosts as other nodes in the deaf rule (team-lead note); members keep "another host or an Online peer". D46, 3.8 deaf row, 3.14. | A host never rebinds. |
| H2 | In Stopping: drop every held direct connection and answer every Message `refused`; only the gossip broadcast stays alive. 3.8 stop row, 3.6 Message step 3, 3.9. | Keep the lock until exit (reverses S17's "release the lock at once"). |
| H3 | `Introduce.handle` is `Option<String>`. New row: an Introduce or IntroduceAck with `handle: None`, or any contact from a cardless node, updates the lookup only and never enters the peer table. Neighbor-down probes only peers in the table. 3.6, 3.8. | Mark cardless entries with a flag and hide them from `peers`. |
| H4 | On every accepted Presence the node drops its held connection to that card, so the next request dials afresh. 3.8 address lookup. Taken in place of the reviewer's "addr differs, or a new session": a same-address restart leaves addr unchanged, and the node cannot tell a new session. Presence is rare, so the extra dials cost little. | Drop only when `addr` differs from the lookup entry. |
| M1 | The rebind interval binds every rebind, the join timeout included. 3.8 Rebind paragraph, 3.14. Init returns within the join timeout plus the observer wait: on a failed join it assigns the handle against the table as it stands and returns, and Presence follows a later successful join. 3.8 init row, 3.10 init. A host with no other host applies no join timeout. 3.14. Taken in place of a new error code, because the error list is closed. | Init fails with a new error code. |
| M2 | Only an accepted Presence replaces the lookup entry; Introduce and IntroduceAck always do. 3.8. | none closer |
| M3 | An Unreachable is dropped if its `ts` is older than the announcement max age, or below the seq held for that card. 3.8. | Unreachable also carries a seq. |
| M4 | Per team-lead: the host's record `ts` is a strictly increasing counter, `max(last + 1, now in seconds)`, with `last` persisted in `<data>/infra/<network>.ts` and starting from 0 if lost. A member drops a record more than 300 s ahead of its own clock and holds or saves nothing from it. 3.3 files, 3.7 field, 3.8 row, 3.14, D44. The unit is now seconds, unlike the other timestamps of 3.1. | `ts = max(now_ms, last_ts + 1)` in milliseconds (reviewer). |
| M5 | Each rewrite re-reads the configuration first and merges it: the union of hosts, the larger `ts`, the later `heard`. 3.3. A write landing between the re-read and the rename can still be lost; closing that needs a lock on the config file, which D7 rules out. | Last writer wins. |
| M6 | The 3072-byte cap applies to `public` after the description is inserted; over it, init returns `bad_request`. 3.10. | Truncate the description. |
| M7 | `HostAddr { v, id, relay }` and `Invitation { v, network, secret, owner, hosts }` defined in 3.13, used by the invitation, the host address line, and the configuration. The unimplementable "addr does not belong to host" check is replaced by "`addr.relays` is exactly [`relay`]" (3.7); a host's relay map holds its own relay only (3.14). | Delete the check. |
| M8 | Signed and MACed bytes are the encoding of the `Payload` value, variant index included; a receiver verifies the mac first, then the signature. 3.4. | none closer |
| M9 | On every accepted record: replace the host's lookup entry, and `insert_relay` whenever the relay is absent from the relay map (this is what re-adds a relay removed under D45); save only when the host is new. 3.8. | Refresh only on new hosts. |
| M10 | On SIGTERM, the runtime shuts down in the background only after the departure wait. 3.9. | none closer |
| L1 | Relay URLs take 1 + 4 × 130 = 521 bytes (a 128-byte string has a 2-byte length), so the largest Presence is 3269 + 521 + 161 = 3951 <= 4058. 3.6 Address caps, test 17. Supersedes the 517 / 3947 in decision 2 above. | Cap URLs at 127 bytes. |
| L2 | Fixed-size byte arrays, `[u8; 64]` included, encode with no length prefix, as iroh's `Signature`. 3.1 wire encoding. | A bytes wrapper with a length prefix (+1 byte each; test 17 would need it). |
| L3 | D4 now points to 3.4 for the signed bytes. | none closer |
| L4 | The 3.14 row is renamed "wire limit (any wire structure)", the term 3.6 and D50 use. | Rename the uses to "wire structure, any". |
| L5 | D2 names flock (std's `File::try_lock`), not `fcntl`. list_cards reports the card this process holds as held without trying its lock. D2, 3.10. | Name `fcntl` and forbid other descriptors. |
| L6 | D40 records the address-cache leak of the observer's fresh key as accepted (G2 #20 ruled a fresh key). | A stable per-machine observer key (reverses G2 #20). |
| L7 | D46 Reason gives the cost of the 5 s records (one per host per member every 5 s), and why they differ from the heartbeats D18 rejects: they scale with hosts, not members. | none closer |
| L8 | 2.13 Deferred gains "revocation and expiry of host certificates". | Add a revocation list now. |
| L9 | 3.1: 53 characters is the announced length; a node's local name for a peer may add one suffix, so `from` holds at most 74 characters (53 + `-` + 20 digits). | Suffix only the requested part (needs the requested handle on the wire). |
| L10 | OPEN. The ledger S27 row and the stray text at the end of staged-revisions.md are outside spec/blueprint.md, which is the only file this task edits; both are records with their own owners. | Fix them here. |

Not changed, per team-lead: the reviewer's "could not check" risk that a C16-blocked member keeps hearing the hosts' 5 s records and never goes deaf goes to the measurement.

## Relay HTTPS settled by E22 (team-lead, 2026-10-21)

Source: research/stack/experiments/e22-two-machines.md, Answer section, plus its notes on the certificate cache (line 125) and the LetsEncrypt mode (line 39). The owner's condition (2026-10-21 14:35, "if low-effort high-benefit, we commit to https") is met: Let's Encrypt via iroh-relay's `LetsEncrypt` certificate mode gave a trusted certificate 9.15 s after first start from a 10-line configuration, with only TCP 80 and 443 open; a cached restart takes 2 ms; HTTPS adds 87 ms to coming online.

| Change | Spec |
|---|---|
| D51 no longer pending: HTTPS only, plain HTTP not served; Reason gains the E22 numbers | D51 |
| QUIC address discovery enabled on infrastructure relays (`enable_quic_addr_discovery`, UDP 7842): a member with direct paths comes online in 0.49 s, against 3.1 s without | D51, 3.14 |
| Certificate cache directory `<data>/infra/<network>.certs/` at mode 0700, since iroh-relay writes the cached key file 0644 | D51, 3.3 files, 3.14 |
| Host ports: TCP 80 and 443, UDP 7842 | 3.14 |

Judgement calls:
- The cache path `<data>/infra/<network>.certs/` is my choice; E22 used `certs/` beside the relay.
- E22 ran the iroh-relay binary from a TOML file; the spec embeds the relay. Certificate path confirmed at source by team-lead (2026-10-21): the library takes Let's Encrypt as `CertConfig::LetsEncrypt { acme_config }` (iroh-relay-1.3.0 src/server.rs:529-531, `AcmeConfig` at 548-557). QUIC address discovery in the library remains unconfirmed, assumed equivalent to the binary's `enable_quic_addr_discovery = true`.

Resolved: no contact email input. tokio-rustls-acme 0.9.1's contact list defaults to empty (src/config.rs:79); only the binary's main.rs:644-647 demands an email (team-lead, at source). run infrastructure keeps its inputs.

## Review 2 fixes

Source: research/stack/spec-review-2.md (1 high, 8 medium, 9 low), read whole. All 18 fixed in the spec; one residue stated under finding 1.

| # | What changed | Alternative |
|---|---|---|
| 1 (high) | Per team-lead: a rebind's join goes through every known host and every Online peer whose address the node holds, so a host that knows a dead host rejoins through its members. 3.8 known hosts and Rebind, D46, 3.14. Residue closed by team-lead (2026-10-21): a host counts as other nodes only the hosts whose record it heard within the last 60 s (new limit "host deaf window 60 seconds"; D46, 3.8 deaf row, 3.14). A host whose fellow host died rebinds at most a few times in the first minute, which also covers a host blocked by the relay bug, then stops. Alternative: a host never rebinds on silence. The missing-sidecar reading under E23 is confirmed by team-lead. | A bootstrap node never rebinds on silence. |
| 2 | At start and at every rebind, a known host with no lookup entry gets `Addr { relays: [relay], direct: [] }` from its HostAddr until a record or IntroduceAck replaces it. 3.8. | Put HostAddr's relay into the dial call directly. |
| 3 | A host applies the Infrastructure rows to learn and save hosts, but never adds a relay to its relay map (a relay URL in an address suffices to dial, E21 source reading). 3.14, 3.8 row ("members only"), 3.3 ("a node that learns a host"). | Hosts learn no hosts. |
| 4 | Introduce and IntroduceAck also drop the held connection to that card, except the one they came on; test 18 is anchored at B's new Presence reaching A. 3.8, test 18. | Anchor only. |
| 5 | Member join targets Online and Unreachable entries, at most 10 tries (new limit "member join tries"), never past the next rebind. 3.8, 3.14. | Stop only at the next rebind. |
| 6 | The host's relay URL is `https://<domain name>/`; the host sets `relay` and `addr.relays = [relay]` itself; members compare parsed relay URLs. 3.14, 3.7, 3.3 example. | Compare strings after normalising. |
| 7 | Tests 19 and 25 are anchored at the relevant Presence. The own-handle blind spot during the observer wait is pre-existing (HEAD) and unchanged. | Send Presence before the observer wait. |
| 8 | Init validates the card, inserts the description, and checks the cap before the lock; a failure leaves the state Unclaimed. 3.10. | Check after the lock and release it on failure. |
| 9 | The mac of a direct structure covers the `Request` or `Response` value, variant index included, which is also what the stream carries. 3.4. | Mac over the bare structure. |
| 10 | Config `ts` is the host's record counter in seconds; new limit "infrastructure record future bound 300 seconds"; the row cites it. 3.3, 3.8, 3.14. | Make the counter milliseconds. |
| 11 | Effective handle split into the announced form (at most 53, receivers drop non-matching) and the local form (announced plus one suffix, at most 74); `to` over 74 is `bad_request`. 3.1. | none closer |
| 12 | The stop row now holds the config rewrite (after the lock release) and says the direct listener stays up to answer Message `refused` and closes Probe and Introduce streams unanswered, so probes of a stopping node fail. 3.8, 3.9 diagram. | Answer Probe in Stopping (would mark a departing node Online again). |
| 13 | `v` starts every top-level wire structure; nested Addr has none. HostAddr's fields appear in TOML text form in the configuration. 3.1, 3.13. | Give Addr a `v`. |
| 14 | Unreachable about yourself: dropped if older than the max age or below your last Presence's seq. 3.8. | none closer |
| 15 | The observer passes the gate, sends Introduce with `handle: None`, answers Introduce with `handle: None`, sends no payload. 3.13 show peers. | none closer |
| 16 | run infrastructure takes a bind IP address; the relay takes TCP 443, TCP 80, UDP 7842 on it; the endpoint any free port. 3.13, 3.14. | A port per service as input. |
| 17 | `refused` row names "while the recipient is stopping, for example during a restart on the same card". 3.10. | A new error code (the list is closed). |
| 18 | D44 says the configuration keeps the newest `ts` as of its last rewrite, and that after a crash it can lag. | none closer |

## E23 rules (team-lead, 2026-10-21)

Source: research/stack/experiments/e23-lock.md, Answer section.
- D6 Reason gains the Linux numbers: lock free 154-232 us after SIGKILL, free after every hard reset (20/20); unsynced sidecar lost 5/5 when cut 1-2 s after writing, intact 5/5 with fsync on file and directory.
- D6 and 3.5: a sidecar is written and synced (`sync_all` on the file and its directory) before any lock is taken on it; create card does this before writing the card.
- "Treat a missing sidecar as a new identity only when no lock file exists": the lock file is the sidecar itself (D2), so the two conditions coincide. Applied as: init never mints a key; a missing sidecar gives `sidecar_invalid`; only create card mints one, and never over an existing card or sidecar. Contradiction noted for team-lead: if a separate lock file was meant, that reverses D7.
- S13 debounce: re-announce only when the announced address set changed since the last Presence, at most once per 2 s (new limit "re-announce interval 2000 milliseconds"); a change inside the interval is announced when it ends if it still differs. 3.8, 3.14. E23 measured S13 as written at about 20 announcements in 12 s while a relay was down, all with the same address.
