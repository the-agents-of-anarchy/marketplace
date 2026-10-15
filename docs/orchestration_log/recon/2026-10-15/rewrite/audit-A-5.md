# Audit A, round 5: ontology, join, resume, card, tell, receive, leave

Branch `draft/10-skills`, head 68d60b2, `/Users/ryzhakar/pp/aoa-skills/peers/skills/<name>/SKILL.md`. Same rules (one-part-name rule void; scribe-to-card edge and the heartbeat wake prompt not counted, as ruled). Done from scratch on the current text; `self-audit.md` not read.

Mechanical checks, all seven skills: R3, R4 (no `version`), R6, R7, R9-R13, R17 PASS. R20/R21 PASS: grep `only|always|must` empty; a script found exactly one `never` outside backticks in every body sentence. R16 PASS (no sentence copied between skills). Edges PASS, unchanged: join names card, receive, heartbeat; card names tell; tell names receive; receive names adopt, vouch, tell, gossip, quote, consent; leave names tell, card, steward, scribe, heartbeat, sweep; resume names join; ontology names none; no extra edge. Terms test (pytest stubbed): used-not-listed `[]` and listed-not-used `[]` for join, resume, card, tell, receive, leave.

## Sense spot-check on every listed term
Method: for each term in each terms sentence, read every body and description line matching the test's pattern, and then swept the group for ordinary verb forms of ontology words by grep (hold, act, state, turn, record, relay, claim, deliver, wake, log, message, ask, answer, notice, stamp, park, live, host, type, name, point, bound, ship, open, send). A use is wrong-sense when the word is an ontology term and the line uses another sense. Result by skill:
- join: harness, session, address, hook, subagent, stamp, wake, member, body, root, society, protocol, member id, card, departed card, worktree, checkout, owner, records, bringing a matter to the owner, main session, presence, message, `[ask]`, `[notice]`, live, peer, commons, commons line, `commons_read`, stewardship, pointer, change line, reloaded: all in the ontology's sense except `claim`-derived words below. Sample pairs: `records` ("the files its project keeps for decisions, owner rulings ...") / join 35 "your project's records naming the role you have"; `bringing a matter to the owner` / join 37 "Bring the owner the choice when several cards match"; `live` ("while presence lists its card's address ...") / join 35 "a member id whose card's address presence lists live"; `pointer` ("`<root>/PROTOCOL.md`") / join 61 "Read the pointer's version".
- resume: session, skill, compaction, wake, member, body, society, card, stewardship: OK. Pairs: `compaction` ("the harness condensing a session's earlier text") / resume 17 "after a compaction"; `body` ("the session that currently runs it") / resume 13 "an earlier body had".
- card: harness, session, host, address, turn, skill, plugin, login, stamp, wake, member, body, protocol, member id, card, worktree, checkout, owner, records, journal, presence, dormant, dnd, state, `[notice]`, peer, commons, commons line, `commons_read`, inbox, stewardship, steward, change line: OK. Pairs: `state` / card 71 "Carry `state` while you are parked"; `turn` ("one stretch in which a session works") / card 73 "in that edit's turn"; `records` / card 19 "never make it part of your project's records"; card 51 "your harness logs for your latest reply" no longer uses "records" as a verb.
- tell: session, turn, hook, subagent, stamp, member, root, card, checkout, main session, presence, busy, idle, waiting, dormant, dnd, state, delivery, message, message body, type, `[hazard]`, `[answer]`, `[notice]`, reply time, held, origin, live, peer, inbox, claim, level 1, level 2, escalation, priority level: OK. Pairs: `held` ("a message held while its sender keeps it unsent until the receiver's state clears") / tell 65 "never drop a held message", 27 "call for a hold"; `delivery` ("handing text to the session at an address") / tell 63 "Deliver a level 1 message at once"; `origin` / tell 37 "Send the origin of a claim that failed your check"; `message body` ("the lines of a message after its second line") / tell 53-59.
- receive: session, skill, member, card, message, `[hazard]`, `[ask]`, `[answer]`, `[notice]`, `[quote]`, seeker, peer, commons, commons line, inbox, gossip, relaying, `from:`, `spread:`, `relay:`, `has:`, claim, level 1, priority level, draft: OK. Pairs: `seeker` / receive 29, 35, 37; `relaying` ("passing a received gossip on to members who lack it") / receive 45 "Relay a message carrying a `relay:` line"; `claim` / receive 21 "Check every claim a message carries".
- leave: session, wake, member, root, society, protocol, card, departed card, owner, `[ask]`, leave notice, peer, stewardship: OK. Pairs: `leave notice` / leave 21; `protocol` (scribe: "`stewards` lists `protocol`") / leave 15 "the stewardship `protocol`".
Wrong-sense uses found:
| line | ontology definition | use |
|---|---|---|
| join 55, 57 | `claim`: "any statement about shared files or resources, a session, or your own facts" | "never leave any of it unclaimed", "Reclaim each earlier body's stewardship", "never reclaim one silently" (verb, take back) |
| ontology 185 | `bringing a matter to the owner`: "writing it into your own records and into your next answer to the owner's word" | "adoption bringing what a peer built into your own work" |
| ontology 23 | `message`: "text one member sends another whose first line opens with one of the bracketed words" | "from the message that starts it to the reply that ends it" (a turn may start from an owner message or any text) |

## Remaining violations per skill

### ontology: 3
| rule | line: text |
|---|---|
| R26 (wrong sense) | 185: "Call adoption bringing what a peer built into your own work yourself" |
| R26 (wrong sense) | 23: "from the message that starts it to the reply that ends it" |
| R26 (forward use) | 9: "wherever a skill of the society uses it" uses "skill" before 29 defines it |
Verdict: **3 violations**.

### join: 1
| rule | line: text |
|---|---|
| R26 (wrong sense) | 55: "never leave any of it unclaimed"; 57: "Reclaim each earlier body's stewardship by `[notice]`; never reclaim one silently" |
Verdict: **1 violation**.

### resume: 0 / card: 0 / tell: 0 / receive: 0 / leave: 0
Verdict for each: **CONFORMS**.

## Round-4 findings
All FIXED: ontology "skill" (defined at 29) and "scope" (defined, line 179); tell 43 ("Say the reason"); tell 5 ("pass on what my subagent found"); card 19 ("never make it part of your project's records"); card 51 ("your harness logs"); join 67 ("Handle the messages"); resume 17, 19 ("never work from a condensed memory"); receive 17, 19, 21 ("Handle", "before you use it"). The verb "act" no longer occurs in the group; `act` left every terms sentence.

## New violations from round 5
- None introduced by the round-5 edits themselves (hold, held, keep, name, have, handle, use rewrites are all in the right sense; `hold` survives only in tell as `held`, which matches ontology 129).
- Found by the wider verb sweep, present before: join 55, 57 (claim), ontology 23 and 185, ontology 9 (skill used before defined; the definition arrived in round 5).

## Summary
Round 5 fixed every round-4 finding, and resume, card, tell, receive and leave now conform. The sweep for ontology words in another sense, ordinary verbs included, found join 55 and 57 (claim as "unclaimed" and "reclaim") and ontology 23 (message), 185 (bringing), plus ontology 9, which uses "skill" before its definition at 29. Counts: ontology 3, join 1, resume 0, card 0, tell 0, receive 0, leave 0.
