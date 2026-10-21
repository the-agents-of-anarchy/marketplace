# Spec review 2: spec/blueprint.md working copy after the review fixes

Reviewed 2026-10-21 by claude-opus-5-5 for team-lead. `git diff -- spec/blueprint.md`: 369+/181-. Read whole: the current spec/blueprint.md, research/stack/spec-review.md, research/stack/spec-apply-report.md. Spec not edited. Line numbers are those of the working copy.

Counts. First review: 20 fixed, 4 partly fixed, 0 not fixed. Findings below: 1 high, 8 medium, 9 low (18; 4 of them are residues of partly fixed items, 14 new).

## Findings, by severity

### High

**1. A host that knows a dead host rebinds every 20 s for good, and drags its members along (residue of H1).** l.781, l.786, l.753, l.990, D46 l.233, test 23 l.1048.
Evidence: a bootstrap node counts "another host among the known hosts" as an other node. Known hosts are "the hosts of the network configuration, plus every host learned ... for the life of the process" (l.753); configured hosts are never removed (l.547). So after one of two hosts dies, the survivor still "knows" one, hears no record from it, and, in a quiet network (members send nothing on a timer, 3.16), reaches the 15 s deaf timeout and rebinds. Its rejoin goes "through the other known hosts" (l.990), which is only the dead one, so "a join that gains no neighbor within the join timeout ends in another rebind" (l.786) every 20 s, with no end. Each rebind closes the endpoint the members are joined to; iroh-gossip 0.101.0 "never re-dials a peer whose dial failed" (D46 Reason), so members lose the host, go deaf 15 s later, and rebind in turn. Test 23 kills exactly one of two hosts and requires "no member rebinds twice" within 60 s; by the text it fails. Test 24 keeps all hosts alive and cannot catch it. The same loop starts when a host restarts with a configured host that is down.
Fix direction: a bootstrap node never rebinds on silence (the alternative recorded under H1), or it counts only hosts heard within some window.

### Medium

**2. Nothing seeds the address lookup with the configured hosts, so by the letter no first join can dial anyone.** l.597, l.751, l.753, l.682, 3.13 l.956-960.
Evidence: "No address lookup service: no pkarr, no DNS, no local network discovery; addresses come from presence" (l.597). The lookup is fed "on every accepted Presence, and on every Introduce or IntroduceAck" (l.751) and by the Infrastructure row (l.780). A fresh member holds only `HostAddr { id, relay }` from the invitation; the relay goes into the relay map (l.753), but no rule puts `{relays: [relay]}` into the lookup entry of that id. Subscribing "with the node ids of the known hosts" (l.682) then dials ids with no address. The same holds for a later host joining through the configured hosts (l.984, l.990). The guess is obvious, but it is a guess.
Fix direction: "At start, and at every rebind, each known host's lookup entry is `Addr { relays: [relay], direct: [] }` until a record or IntroduceAck replaces it."

**3. Whether a host applies the Infrastructure rows is unstated, and the relay-map sentence contradicts them.** l.990 against l.780.
Evidence: 3.14 says "The endpoint's relay map holds its own relay only" and also that the host "joins again through the other known hosts", which presumes hosts learn hosts from records. If a host applies the l.780 row, "If its relay is absent from the relay map, add it (iroh `insert_relay`)" breaks "own relay only"; it also saves to the configuration ("save the known hosts"), which 3.3 assigns to "a member" (l.547). If a host does not apply the row, the first host (configuration empty, l.977) never knows another host, and the bootstrap-node clause of the deaf row never applies to it. An implementer must pick.

**4. Test 18 still cannot pass as worded (residue of H4).** l.751, l.762, test 18 l.1043.
Evidence: the held connection is dropped "on every accepted Presence". A restarted B sends Presence only after "the topic reports joined, wait the observer wait" (l.762), at least 3000 ms after its join. Until then A's send reuses the connection to the killed B, which e5 measured hangs to the 10 s timeout. An Introduce from B, which may arrive earlier, replaces the lookup but does not drop the held connection. Test 18 says "Within one second A's send to B is delivered" with no anchor; anchored at B's restart it is impossible. State the anchor (B's Presence reaching A), or also drop the held connection on Introduce and IntroduceAck.

**5. The member-join row is a new unbounded loop, and its target set excludes the peers the outage marked Unreachable.** l.782.
Evidence: "join the cards of the Online entries, and again every member join interval, until one of them is a neighbor." No bound: a member whose Online entries are all dead (a stale table, or the last member alive) retries every 3000 ms until the next rebind, or forever. And during the relay block that causes the rebind, neighbor-down probes fail ("On failure, set Unreachable and send Unreachable", l.774), so live peers enter the rebind as Unreachable and are not joined. Fix direction: target Online and Unreachable entries; stop after a fixed count or at the next rebind.

**6. The "`addr.relays` is exactly [`relay`]" check rests on an unstated URL form, and on the host's endpoint having homed before its first record.** l.728, l.951, l.990, config example l.542.
Evidence: (a) Whether "exactly" compares strings or parsed URLs is unstated. iroh-base 1.3.0 `RelayUrl::from_str` wraps `url::Url` (relay_url.rs:38-44); the url crate serializes `https://relay.example` as `https://relay.example/` (WHATWG rule; known behaviour, not run here). A host filling `addr` from its endpoint and `relay` from its configured text fails a string comparison at every member, silently. (b) The host broadcasts "when the topic reports joined" (l.990); if its endpoint has not reported its home relay yet, `addr.relays` is empty and every member drops the record. (c) run infrastructure takes a domain name (l.951), but no sentence derives the relay URL from it (scheme, port, trailing slash). Fix direction: the host sets `addr.relays = [relay]` itself; compare parsed `RelayUrl`s; define `relay` as `https://<domain>/`.

**7. Test 25 promises what the text cannot deliver: a new member learns non-neighbors only after its own Presence, which follows the observer wait.** l.762, l.763, l.767, l.770, test 25 l.1050 (test 19 l.1044 shares it).
Evidence: during the observer wait the new member has sent no Presence, so only its gossip neighbors send it Introduce (l.770). A host neighbor answers with `handle: None`, and that row "updates the lookup only" (l.767), so the host introduces nobody. Every other member replies (l.763) only to the Presence sent after the wait. "its `peers` shows every present member within the observer wait" holds only for neighbors. Own-handle assignment against "the table after the observer wait" (l.790) has the same blind spot (pre-existing at HEAD l.673; test 25 is new). The 105-216 ms measured (apply report, call 24) came from a harness, not from this text. State the anchor (from the Presence) or change the order.

**8. The init description cap has no place in the init order (residue of M6).** l.838, l.762, l.803.
Evidence: "the 3072-byte cap ... applies to `public` after the insertion, and over it init returns `bad_request`." Init's order is "Take the sidecar lock ... build the endpoint, and subscribe" (l.838). Whether the check runs before the lock, or after the lock and the endpoint (then: is the lock released, does the endpoint close, does the state stay Unclaimed so a retry is allowed), is unstated. "A process claims one card for its life" (l.803) makes the answer matter.

**9. The mac bytes of the direct structures are still ambiguous (sibling of M8, which fixed gossip only).** l.574, l.601, l.604, l.637.
Evidence: "For a gossip payload the structure is the `Payload` value, variant index included." For Message, Probe, Introduce and the three responses nothing says whether the mac covers the bare struct or the `Request`/`Response` value with its variant index, nor whether the stream carries the enum tag at all ("The client writes one request structure"). Two implementations can disagree and reject each other.

### Low

**10. Units and the table.** 3.3 l.542-543 writes `ts = <timestamp>`; "timestamp" is milliseconds by 3.1 l.468, but the Infrastructure `ts` is seconds (l.721, l.990). The "more than 300 seconds ahead" bound (l.779, D44) is a limit missing from the 3.14 table; it equals the announcement max age by value only.

**11. L9 residue.** 3.1 l.465 still defines an effective handle as "a handle, or a handle followed by `-` and a decimal integer", while a 74-character local name is an announced `h-n` (not a handle: at most 32) plus a second suffix. No rule says a receiver drops an announced handle over 53, or how long `to` may be.

**12. Stopping's order is split.** 3.3 l.547 rewrites the configuration "on entering Stopping"; the stop row (l.784) and the 3.9 diagram (l.796) omit the step, so its place relative to the Departure and the lock is unstated. The stop row also says "keep only the gossip broadcast alive" while requiring every Message to be answered `refused`, which needs the direct listener alive; whether Probe and Introduce are answered in Stopping is unstated.

**13. Two "wire structure" mismatches.** 3.1 l.470: "Every wire structure starts with a version field `v`"; Addr (l.632) has none. 3.13 l.953 says HostAddr is the form of "the `hosts` of the configuration", but the TOML (l.541-544) holds hex `id`, `relay`, `ts`, `heard` and no `v`.

**14. Unreachable about yourself has no replay rule (M3 fixed only the peer row).** l.773: "Send Presence", with no age or seq check, so each replay of an old signed Unreachable, at any time, makes the target broadcast. Only a secret holder can replay (mac, gate).

**15. The observer's direct behaviour is unstated.** H3's row covers what members do with a cardless node, but no sentence says the observer of show peers, tail and doctor answers Introduce with IntroduceAck `handle: None`, or sends Introduce to its neighbors. show peers waits "for Presence and Introduce" (l.947), so it depends on members' Introduce reaching it.

**16. run infrastructure's bind address against fixed ports.** l.951 takes a bind address; l.990 says "The host opens TCP 80 and 443 and UDP 7842". Whether the bind address carries a port, and which service binds it, is unstated.

**17. During a clean restart, sends to the card return `refused` for at least the observer wait.** l.784, l.751. The old process answers `refused` until A's lookup is replaced by the new Presence (join plus 3000 ms). True to I7, but `refused` reads "The member refused the message" (l.869) for a member that is coming back.

**18. D44 overstates persistence.** D44 l.221: "the newest seen for that host, which the configuration keeps across restarts". The file is written only when a host is learned and on Stopping (l.547, l.780); after a crash the saved `ts` lags. The apply report states this (follow-up c); the spec does not.

## First-review items

| Id | Verdict | Spec text |
|---|---|---|
| H1 | partly fixed | l.781: "for a bootstrap node: another host among the known hosts". Fixes the lone host; a host that knows a dead host loops (finding 1). |
| H2 | fixed | l.784: "Drop every held direct connection, and from here on answer every Message `refused`"; l.672 step 3 "and the process is not Stopping"; l.801. Two endpoints with one key still overlap up to 5 s by design (D19); e5 measured that overlap. |
| H3 | fixed | l.625 `handle: Option<String>`; l.767 "The node never enters the peer table"; l.774 "If the neighbor is not in the peer table, do nothing". Observer side unstated (finding 15). |
| H4 | partly fixed | l.751: "On every accepted Presence the node also drops its held connection". Presence comes after the observer wait; test 18's one second has no anchor (finding 4). |
| M1 | fixed | l.1014 "at least, between any two rebinds"; l.786 "no sooner than the rebind interval after this one"; l.838 "at most the join timeout plus the observer wait". |
| M2 | fixed | l.751: "On every accepted Presence, and on every Introduce or IntroduceAck". |
| M3 | fixed | l.772: "Drop it if its `ts` is older than the announcement max age ..., or below the seq held for that card." Self row untouched (finding 14). |
| M4 | fixed | l.990: "`ts = max(last + 1, now in seconds since the Unix epoch)`, and the host writes `last` ... before it broadcasts"; l.779 "more than 300 seconds ahead ... Drop it. Hold and save nothing from it." |
| M5 | fixed | l.547: "Each rewrite first re-reads the file and merges it ...: the union of the hosts, the larger `ts` and the later `heard`". Residual window stated in the text. |
| M6 | partly fixed | l.838: "the 3072-byte cap of 3.5 applies to `public` after the insertion, and over it init returns `bad_request`". Order against lock and endpoint unstated (finding 8). |
| M7 | fixed | l.956-968 HostAddr and Invitation; l.728 "whose `addr.relays` is not exactly [`relay`]". Gives rise to findings 2, 3, 6. |
| M8 | fixed | l.563 "the `Payload` value, variant index included"; l.574 "a receiver verifies the mac first, then the signature". Direct structures not covered (finding 9). |
| M9 | fixed | l.780: "Replace the host's entry in the lookup with its address. If its relay is absent from the relay map, add it". |
| M10 | fixed | l.801: "after the departure wait, shuts its runtime down in the background". |
| L1 | fixed | l.666 "3951 bytes"; test 17 "521 + 161 (... 1 + 4 × 130 ...)". Recomputed below. |
| L2 | fixed | l.470: "A fixed-size byte array (`[u8; 16]`, `[u8; 32]`, `[u8; 64]`) is encoded as its bytes with no length prefix". |
| L3 | fixed | D4 l.141: "3.4 fixes the signed bytes". |
| L4 | fixed | l.1020 "wire limit (any wire structure)"; l.601 and D50 l.428 say "wire limit". |
| L5 | fixed | D2 l.129 "flock, as std's `File::try_lock`"; l.837 "except for the card this process holds, which is held without a try". |
| L6 | fixed | D40 l.383: "Each run leaves one entry in iroh's address cache of every node it touches (D3); accepted". |
| L7 | fixed | D46 l.234: "they scale with the number of hosts ... each member receives one record per host every 5 s". |
| L8 | fixed | 2.13 l.440: "revocation and expiry of host certificates". |
| L9 | partly fixed | l.465: "so a `from` field holds at most 74 characters". Grammar sentence unchanged (finding 11). |
| L10 | fixed, outside the spec | ledger.md l.339, S27 row: "replay: a member keeps the newest `ts` per host, persisted in the config"; staged-revisions.md ends at the manifest line with no stray text (commit 81da7c5). |

Test 17, recomputed from 3.6 and 3.7 (postcard, worst case): Payload variant 1, `v` 1, `card` 32, `handle` 1 + 53, `public` 2 + 3072 (3072 needs a 2-byte varint), `attached` 1, `seq` 10, `mac` 32, `sig` 64 (no prefix, l.470) = 3269. `addr.relays` 1 + 4 × (2 + 128) = 521; `addr.direct` 1 + 8 × (1 + 16 + 3) = 161. Total 3951 ≤ 4058 = 4096 − 38; 107 bytes spare. Matches l.666 and l.1042. Every Presence field is counted.

Cross-references: every D number cited resolves (D1-D14, D16-D51; D15 unused and cited nowhere); "test 17" (l.666) and "3.15" (D49) resolve; no "ticket", "Displaced", "bootstrap member", or `claim.` remains. Limits table against text: all values agree (200 ms, 500 ms, 1000 ms, 1500, 3000 x3, 5000 x2, 10000 x3, 5 s, 15 s, 20 s, 300 s, 3600 s, 30 days, the sizes); the one missing entry is finding 10. No row of 3.8 overlaps another: the two Infrastructure rows split on `ts`; the two Introduce rows split on `handle`; the bootstrap-node clause sits inside the deaf row.

## Flows

**First network setup (3.13 order).**
1. create network: secret, owner key, config with no host. Fine.
2. run infrastructure, first run: creates the key, prints the line, exits. Guess: how `relay` in the line is formed from the domain name (finding 6c); whether the relay and ACME start before the exit.
3. certify host: fine; the copy of the certificate to the host is manual, and the text says so.
4. run infrastructure again: "subscribes alone, is its own bootstrap, and applies no join timeout". It knows no other host, so it never goes deaf. Its first record waits for "the topic reports joined", which a lone subscriber reaches only when the first member arrives; harmless, unstated.
5-6. join network with the line, show invitation. Guess: whether show invitation includes learned hosts or only configured ones.

**A member joining by invitation.** join network writes secret, owner, hosts (no `ts`, no `heard`); create card; list_cards; init. Guesses: seeding the lookup for the host id (finding 2); when the description cap is checked (finding 8). After joined and the observer wait the member assigns its handle against a table that holds only gossip neighbors (finding 7); the host answers IntroduceAck `handle: None` and enters only the lookup. Other members learn the newcomer from its Presence and reply with Introduce. On a join that fails within 5 s, init returns with a handle assigned against an empty table, which can differ from the name other nodes give it: allowed by l.788, but test 7 ("at every node, its own included") then fails.

**A clean stop and restart on the same card.** Stop row: Departure handed to a task, lock released, held connections dropped, Messages refused, 5000 ms wait, exit. Guesses: where the config rewrite of 3.3 falls (finding 12); whether Probe and Introduce are still answered. The new process takes the lock at once, builds a second endpoint with the same key, joins, waits 3000 ms, and sends Presence with seq = now_ms, which beats the Departure's seq and its tombstone. Until A accepts that Presence, A's sends reach the old process and get `refused`, or `unreachable` after it exits; the latter broadcasts an Unreachable that the new process answers with Presence (finding 17). A clock stepped back between the two sessions puts the new seq under the tombstone, and the new Presence is refused for up to 300 s (pre-existing S12 behaviour; the text does not name the risk).

**A relay host dying while members are idle.** Members homed on it: the relay-loss row removes the relay after 500 ms, the home moves, the address change sends Presence (which the C16 block may hold). Neighbor-down for the dead host: not in the peer table, nothing. Members hear the surviving host's records every 5 s unless blocked; blocked ones go deaf at 15 s and rebind: close, TCP-probe each known relay with a 1000 ms timeout (sequential or parallel: unstated), strip dead relays from other members' lookup entries, build a new endpoint "with the relay map" (whether a dead relay that was not the home relay leaves the new map: unstated), join through the known hosts, send Presence, member join after 1500 ms. Faults: the surviving host enters finding 1's loop at about 15 s; the member-join target set misses peers marked Unreachable during the block, and the loop has no bound (finding 5). The first review's open question (a blocked member that still hears records never goes deaf) remains open.

**A new host announcing itself.** Steps 2-4 with a configuration naming a live host. The new host joins through it (finding 2 applies to it too) and broadcasts on joined and every 5 s with `ts` from its counter file. Members check certificate, signature, `addr.relays` against [`relay`] (finding 6), and `ts`; then hold, replace the lookup, insert_relay, add, save with re-read and merge. Test 22's 1000 ms agrees with the rows. Guesses: whether existing hosts learn the new host (finding 3); from then on every host that knows it is exposed to finding 1 if it dies; how the new host reaches the old host's relay when its own relay map holds only its own relay (E21 shows it works; the text does not say how).

## Could not check

- iroh's dialing of a relay URL absent from the endpoint's relay map (finding 3, new-host flow): not read at source; E21's result taken as reported.
- The url crate's trailing-slash serialization (finding 6a): known WHATWG behaviour, not run here.
- The 38-byte gossip overhead (e2), the 280/320 crate counts, and every measured figure the D-records cite: not rerun.
- Whether a C16-blocked member keeps hearing records and never goes deaf; heal times at the 15 s trigger: unmeasured, as the first review said.
- Whether iroh-gossip 0.101.0 reports `joined` for a lone subscriber only on its first incoming neighbor (flow 1, step 4): inferred from the joined semantics the spec uses, not read at source.
