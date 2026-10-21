# Spec review: uncommitted S1-S27 apply to spec/blueprint.md

Reviewed 2026-10-21 by claude-opus-5-5 at the team-lead's request. Base HEAD 20e9efe; `git diff -- spec/blueprint.md` (344+/177-). Sources: research/stack/staged-revisions.md, ledger.md, parameters.md, spec-apply-report.md, experiments e2 and e5, owner rulings in docs/orchestration_log/history/2026-10-15/events.md. Spec not edited. Line numbers are those of the working copy.

Count: 4 high, 10 medium, 10 low.

## High

**H1. A lone host with members rebinds every 20 s in a quiet, healthy network.** 3.8 deaf row (l.778), 3.14 (l.969), D46 (l.233).
Evidence: the deaf condition is "knows at least one other node (another host among the known hosts, *or an Online peer*), has received no gossip payload of any kind from anyone for the deaf timeout". 3.14: the host "applies the deaf row and the rebind of 3.8 as a member does". A host does not hear its own broadcasts (spec-apply-report, decision 6). Members send no Presence on a timer (3.16, D18). So a one-host network with members, which is exactly what the order in 3.13 (steps 1-6) builds, gives the host Online peers, no payload within 15 s, and a rebind, which drops every member connection (D46), every 20 s. The Follow-up (a) claim "a lone host no longer rebinds" holds only for a host with no members. Test 24 runs with hosts alive, so it does not catch this.
Fix: for a bootstrap node, count only other hosts as "other nodes" (a host with no other host never rebinds on silence).

**H2. Lock release at the start of Stopping lets two live endpoints share one key for 5 s.** 3.8 stop row (l.781), D2, D19, 3.9.
Evidence: "Hand the Departure broadcast to a task. Release the sidecar lock. Wait the departure wait. Exit." The endpoint has to stay up to deliver the Departure, so a restart on the same card within 5 s builds a second endpoint with the same key. D6: "Two live holders starve each other silently (measured)". e5 "Overlap (both alive)": direct dials go to whichever address the dialer holds, and the gossip of the peers moves to the newer instance. No rule says what a process in Stopping does with an incoming Message. It acks it into an inbox that dies within 5 s, while the sender reads `delivered: true`.
Fix: in Stopping, answer every Message `refused` and drop held direct connections; keep only the gossip broadcast alive until exit.

**H3. Cardless nodes (bootstrap nodes, observers) have no rows, and members insert them as peers.** 3.6 Introduce/IntroduceAck (l.621-659), 3.8 rows "gossip reports a neighbor up" and "Introduce or IntroduceAck received" (l.764, 767), 3.14.
Evidence: a member sends Introduce to every new gossip neighbor, and the host is always its first. The host "answers Introduce with `handle: None`". The member then applies "Same as Presence received and accepted ... card unknown: Insert the peer as Online ... Apply handle assignment" to a node that has no card and no handle. The host then counts as an "Online peer" in the deaf row, shows in `peers`, and draws neighbor-down probes and network-wide Unreachable reports when it goes. `Introduce.handle` is a plain `String`, so neither a host nor an observer can send an Introduce at all. An observer (fresh key on every run, D40) that answers IntroduceAck lands in every neighbor's table. When it exits, its neighbor-down probe fails and it is marked Unreachable and broadcast, and Unreachable entries are never removed.
Fix: add a row: an IntroduceAck with `handle: None`, or any contact from a node that holds no card, updates the lookup only and never enters the peer table; make `Introduce.handle` an `Option`.

**H4. Test 18 cannot pass with held-connection reuse.** 3.10 send step 4 (l.846), 3.6 (l.599), test 18 (l.1022).
Evidence: step 4 says "Use the held connection to the peer, or dial". Test 18: "B is killed and restarted with the same card. Within one second A's send to B is delivered." e5 measured that "held-connection requests hang with no answer until the connection dies at 10 s"; only fresh dials resolve within about 1.0 s. A's first sends after B's restart reuse the dead connection and return `timeout` after 10 s. No rule drops the held connection when B's new Presence arrives.
Fix: on an accepted Presence whose `addr` differs from the lookup entry, or on any Presence of a new session, drop the held connection to that card.

## Medium

**M1. A rebind caused by the join timeout is unbounded, and init never returns.** 3.8 init row (l.760), Rebind paragraph (l.783), 3.14 rebind interval (l.993), 3.10 init (l.835).
Evidence: "A join that gains no neighbor within the join timeout ends in another rebind." The 20 s interval binds only "two rebinds caused by deafness". With no reachable host, a member closes its endpoint, TCP-probes every relay, and rebinds about every 5 s, forever, dropping any working direct connection each time. Init "return[s] when the effective handle is assigned", which needs "joined", so the MCP call hangs. spec-apply-report contradiction 1 says such a member "rebinds every 20 s"; by the spec text it is every 5 s. Whether the join timeout applies to a lone host's first subscribe (step 4 of 3.13) is unstated; if it does, that host loops as well.
Fix: apply the rebind interval to every rebind; bound init by a timeout returning a new error code, or return before the join with a warning.

**M2. A rejected Presence still overwrites the address lookup.** 3.8 address lookup (l.749).
Evidence: "On every Presence, Introduce, or IntroduceAck, the node replaces that card's entry". The seq check rejects a replayed old Presence (valid signature, lower seq), but by this wording its stale `addr` still replaces the live one. Test 20 checks only "A's table".
Fix: "On every accepted Presence, and on every Introduce or IntroduceAck".

**M3. Unreachable has no replay rule.** 3.7 Unreachable, 3.8 row "Unreachable received, about a peer" (l.769).
Evidence: the replay rules cover Presence and Departure (seq, max age, tombstone) and Infrastructure (ts per host). For Unreachable the only check is "unless a direct contact with that peer is more recent than `ts`". A peer known only through gossip has no direct contact, so any old signed Unreachable, replayed at any later time, marks it Unreachable. Each replay also makes the target re-broadcast Presence ("about yourself: Send Presence"). No max age applies, and nothing compares `ts` with the peer's held seq.
Fix: drop an Unreachable older than the announcement max age, or with `ts` below the seq held for that card.

**M4. The Infrastructure `ts` has no generator and no bound, and it is persisted.** 3.7 (l.719), 3.3 (l.545), D44.
Evidence: "ts: u64 newer than the last accepted for this host"; the spec never says how a host produces it. Members persist the newest `ts` per host in the configuration. A host restarted with a clock behind its last `ts`, or one record carrying a far-future `ts`, makes every member drop that host's records until the host's clock passes it, across member restarts too. Since D46's floor rests on those records, members of that host go deaf.
Fix: the host sends `ts = max(now_ms, last_ts + 1)` with `last_ts` kept in its infra directory; receivers drop a `ts` further in the future than the announcement max age.

**M5. Concurrent rewrites of the configuration lose updates.** 3.3 (l.545).
Evidence: "rewrites the file whole ... Each rewrite updates `ts` of every host and `heard` of the learned hosts from what this process holds". With several sessions on one machine (spec-apply-report call 21), the last writer wins. A host that another process learned is dropped, and `ts` can go backward in the file, which reopens the replay window that decision (c) closes. Atomic rename prevents torn files, not lost updates.
Fix: re-read the file just before each rewrite and merge: the union of hosts, the max `ts`, the max `heard`.

**M6. The init description bypasses the 3072-byte cap.** 3.10 init (l.835), 3.5 (l.589).
Evidence: the cap is checked "at claim" on the card ("A larger mapping gives `card_invalid`"), and then "The description, if given, is put under `public.description`". It has no length limit. A long description pushes Presence past the frame; S9 then refuses every broadcast, and the member is silent with no error at init.
Fix: apply the 3072-byte cap after inserting the description; over the cap, init returns `bad_request`.

**M7. "Host address" means two things, the host address line has no defined structure, and one Infrastructure check is unimplementable.** 2.2 (l.89), 3.7 (l.718, 726), 3.13 (l.950-952).
Evidence: the glossary says "its node id and its relay URL"; Infrastructure's `addr: Addr` holds relays and direct addresses and no id; the line is "the postcard encoding of the host's address" (parameters #22: "the host's endpoint address"); the invitation fields are named but not typed. 3.7 asks to "Drop an Infrastructure payload ... whose `addr` does not belong to `host`", but Addr carries no id to compare.
Fix: define `HostAddr { v: 1, id: [u8; 32], relay: String }` for the invitation, the line, and the configuration, and state the check (for example, every `addr.relays` entry equals `relay`) or delete it.

**M8. The bytes that are signed and MACed on gossip are ambiguous, and the check order is unstated.** 3.4 (l.561, 572), 3.7 (l.726).
Evidence: "the postcard encoding of the payload with `sig` and `mac` set to zero bytes" does not say whether the Payload enum's variant index is included; two implementations can disagree and reject each other. 3.4 fixes the order of computing ("compute the mac after the signature") but no sentence fixes the order of checking; 3.7 lists two "Drop" sentences.
Fix: "the encoding of the `Payload` value, variant index included"; "verify the mac first, then the signature".

**M9. The Infrastructure row skips known hosts: no lookup refresh, and re-adding a removed relay is unclear.** 3.8 (l.777), D45.
Evidence: "If the host or its relay is not known: add ... add its relay to the relay map ..., also when the relay-loss row removed it, put the host's address in the lookup". A known host that restarts on new direct addresses keeps its stale lookup entry, since the address lookup paragraph covers Presence and Introduce only. Whether a relay removed by the relay-loss row is still "known" (its host is) is unclear, so D45's "adds it back when its host announces again" may never run.
Fix: on every accepted record, replace the host's lookup entry, and `insert_relay` whenever the relay is absent from the relay map.

**M10. SIGTERM shutdown can kill the Departure before the departure wait.** 3.9 (l.798), stop row (l.781), D19.
Evidence: "On SIGTERM the binary hands over the Departure first, then shuts its runtime down in the background", against "Wait the departure wait. Exit." D19 says "the wait is what delivers it". Read literally, the runtime that runs the Departure task shuts down at once.
Fix: "On SIGTERM, after the departure wait, shut the runtime down in the background."

## Low

**L1. Test 17 and the 3.6 Address caps miscount relay URLs.** l.664, l.1021; spec-apply-report decision 2. A 128-byte string has a 2-byte postcard length (the varint holds 127 in one byte): relays come to 1 + 4 × 130 = 521, not 517, so the largest Presence is 3951 bytes, not 3947. It still fits within 4058. Fix: 521 and 3951, or cap URLs at 127 bytes.

**L2. The encoding of `sig: [u8; 64]` and `cert: [u8; 64]` is unstated.** serde implements arrays only up to 32, so an implementer picks a wrapper; a bytes wrapper adds a 1-byte length that test 17 does not count. iroh-base 1.3.0's `Signature` serializes as a 64-tuple with no prefix (key.rs:378-382). Fix: state "64 bytes, no length prefix".

**L3. D4 is stale against 3.4.** D4: "over the postcard encoding with the signature field zeroed". 3.4 adds the domain prefix and zeroes `mac` as well. Fix: D4 refers to 3.4.

**L4. "wire limit" is not a 3.14 term.** 3.6 l.599 and D50 l.428 say "wire limit"; 3.14 names it "wire structure, any". Fix: one name.

**L5. The lock type is not named.** D2 says "exclusive advisory lock". POSIX `fcntl` locks are per process and drop when any descriptor of the file closes, so `list_cards` "trying the lock and releasing it at once" inside the claimed process, or a re-read of the sidecar, would free the process's own lock. e5 used `std::fs::File::try_lock` (flock). Fix: name flock, or std's `File::try_lock`.

**L6. The observer's fresh key contradicts D3's reason.** D40 says "with a fresh key on each run"; D3 says "a fresh key per session leaks an entry on every long-lived node". Every `show peers`, `tail`, and `doctor` run leaks an entry on each node it touches. Fix: give the observer a stable per-machine key, or record the leak as accepted in D40.

**L7. D18 rejects what D46 now relies on.** D18 rejects periodic heartbeats as "constant traffic that grows with the member count"; D46 rests on a 5 s Infrastructure record delivered to every member (hosts × members). Fix: state the cost and why hosts differ, in D46 Reason.

**L8. A certificate has no revocation and no expiry.** D44, 3.4. A retired or compromised host stays certified for good; 2.13 lists revocation of the network secret only. Fix: add "revocation of host certificates" to 2.13 Deferred.

**L9. The 53-character cap on effective handles breaks locally.** 3.1 l.465, handle assignment l.785. A receiver suffixes an announced effective handle of up to 53 characters to `h-n`, giving up to 56 characters in `from`, outside the 3.1 grammar (a base handle is at most 32). Fix: suffix the requested part, or allow 56.

**L10. Source records disagree, and one file is damaged.** The ledger S27 row still says "replay of an old record is unchecked (`ts` carried, not compared)", while the spec compares and persists `ts` (team-lead decisions 3 and c). research/stack/staged-revisions.md ends with stray tool-call text (`</content> </invoke> <invoke name="Bash"> ... git add research/stack/staged-revisions.md`). Fix: update the ledger row; truncate the file.

## Checked and found fine

- S12: seq generator, acceptance (signature, above held, above tombstone, max age), tombstone kept for the max age, Unreachable keeps `ts`, 300 s, test 20: all match staged S12 and the 19:06 ruling.
- S14: Claim, tie-break, probe replacement, and Displaced are all gone; D2, D3, D6, D7, D10, D17, D30, D32, 3.9, 3.10 `card_held`, and tests 6, 13, 18 (text), 20 match staged S14; the removed validation steps 3-4 became "the sender is the card of the connection's remote id".
- S16: D13 text, the gate paragraph, the derivation `messaging gate v1`, the entropy note, and the 3000 ms timeout match staged S16 and "Hook, both ways".
- S20: addr in Presence, Introduce, and IntroduceAck; replace, never merge; no pkarr, DNS, or local discovery; D15 moved to Deferred as mDNS; the invitation carries id and relay. Faithful.
- S21: D14, D43, known hosts, insert_relay, saved hosts, "an invitation needs one reachable host", and tests 22, 25, 26 match the ledger row.
- S26: rebind, 20 s debounce, relay probe and strip (C2), 5 s join timeout, on_join patch (D49), MJOIN 1.5 s / 3 s (E20 values); trigger per the 15:15 ruling, marked pending.
- S27: owner key in the configuration, one certificate per id, acceptance only when the certificate verifies and the record is signed by the certified id, test 27, 3.16 line.
- S1, S2, S5, S6, S9, S10, S11, S13, S15, S17, S18, S19, S24, S25: present and faithful to staged or ledger text.
- G1-G4 spot-checked: #6, #9, #10-15, #21, #22, and G5 #23-29 present with their values.
- The 3.14 limits table agrees with every number in the text: 1,048,576, 3072, 4096, 1000, 5000, 10000 (x3), 3000 (x3), 300 s, 5000, 3600 s, 500, 200, 30 days, 15 s, 20 s, 5000, 1000, 1500, 3000, 5 s, 1,114,112. A maximal Message (1,048,725 bytes) fits within 1,114,112.
- Test 17's other terms: variant 1, `v` 1, arrays without prefix, `public` 2+3072, handle 1+53, seq 10, SocketAddr 20 (serde's non-human-readable form: tag, 16 octets, port varint), and 4096-38 = 4058 (e2: 38 bytes, derived from source).
- D-record and section references resolve: D8, D10, D14, D16, D19, D44-D51, 2.13, 3.3-3.16, test 17. D15 is unused and referenced nowhere. No leftover "ticket", "transport key", "Displaced", "duplicate set", "bootstrap member", or base32.
- Signer and prefix per gossip payload (3.4 table), the certificate prefix, mac over the signed encoding, the gate binding both ids, and the direct structures authenticated by TLS remote id plus mac.
- The 3.8 event table has no duplicate rows for one event (apart from H3's missing cardless case).
- Invariants I1, I3-I7 hold as written; I2 holds if the owner is not read as a component (spec-apply-report note 11). H2 strains I7 in practice.
- iroh-relay 1.3.0's `server` feature pulls `tokio-rustls-acme` with a LetsEncrypt CertConfig (server.rs:50, 529), so D51 needs no new crate. iroh-base 1.3.0 `PublicKey` Display is lowercase hex (key.rs:221), as S5 assumes.

## Could not check

- Whether a member that C16 blocks keeps hearing a live host's 5 s records, and so never goes deaf. If its receive path survives (for example over a direct UDP path, while QUIC ACKs on the relay path cannot leave), the new trigger never fires. Nothing measured: E15-E21 used 1 s application heartbeats and a 3 s trigger. E24 should include this case.
- Heal times and test 23's 60 s bound at the 15 s trigger (unmeasured; the report says so too).
- Whether neighbor-down probes and sends in the first 15 s after a relay death feed the C16 queue faster than the harness's probers did (E17: "real-member rate unknown").
- ACME effort for D51 (pending its two-machine check).
- -32601 for non-object `arguments` (JSON-RPC's "method not found"; parameters #28 cites e11; not rerun).
- The 280 / 320 crate counts (not rerun); the 38-byte gossip overhead beyond e2's source reading.
- G1-G4 values outside the spot-check; iroh `insert_relay` / `remove_relay` behaviour; flock semantics on Linux (e5 ran macOS only).
