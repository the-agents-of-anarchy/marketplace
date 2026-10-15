# Audit A: ontology, join, resume, card, tell, receive, leave

Skills at `/Users/ryzhakar/pp/aoa-skills/peers/skills/<name>/SKILL.md`. Line numbers are that file's. Rules: memento:skill-creation 0.5.1. Name rule void (owner), not checked. Method: every sentence read against every rule; greps for copies, edges, emphatics, versions, attributes, paths.

## Rule key
R1 procedure named. R2 one procedure only. R3 file `SKILL.md`. R4 frontmatter, `name`+`description`, no version. R6 directory = name. R7 description = one sentence + phrases. R8 no request phrase/condition in body. R9 body in XML tags. R10 tag = imperative verb phrase. R11 every instruction in a tag. R12 no attribute. R13 prose + inline backticks only. R14 body order = procedure order. R15 nothing outside except skill name. R16 no shared content copied. R17 skills by name, never path. R18 one instruction per sentence. R19 command, not suggestion. R20 at most one emphatic word. R21 emphatic counted outside backticks. R22 each positive paired with prohibition of the SAME instruction. R23 no argument. R24 no failure narration. R25 one term per concept. R26 non-ordinary terms defined in first-use sentence unless ontology named. R27 ordinary words. R28 every sentence instructs or forbids.

Checks that returned clean for all seven skills: R3 (each dir holds only `SKILL.md`), R4 (no `version`; both fields present), R6, R7 (line 4 one sentence, line 5 phrases), R9, R10 (all tags imperative verb phrases), R11, R12 (grep for attributes: none), R13, R17 (grep for `skills/`, `.md` paths: none to skills), R20/R21 (grep `only|always|must` outside quotes: none; every body sentence carries exactly one `never`), R23, R24. R1 PASS: each skill's procedure is inferable in one sentence (stated in section 3).

## 1. Tables (only violations listed; every rule not listed is PASS)

### ontology (170 lines)
| rule | result | line: offending text |
|---|---|---|
| R15/edges | VIOLATION | 147: "the exceptions being `ontology`, `protocol-change`, `ask-around`, and `spread-around`" names three skills; roster says ontology is a leaf |
| R16 | VIOLATION | 95, 97: message shape, `[<type>] <one self-contained sentence>`, `reply: none \| by <time> \| when convenient · sent <stamp>`, "ten lines at most", "`[hazard]` for what can corrupt or kill a peer's work now" restated in tell 31, 43, 45, 49; 43-45: `state: dormant`, `state: dnd` restated in card 67 |
| R18 | VIOLATION | 13: three definitions (harness, host, harness-ref) in one sentence |
| R18 | VIOLATION | 73: "Call `<root>/commons.md` the commons' intake, ... and `#<n>` a line's number there" defines two terms |
| R18 | VIOLATION | 95: defines message, type line, reply line, body in one sentence |
| R18 | VIOLATION | 97: defines five types in one sentence |
| R22 | VIOLATION | 15: "Call a session's address `<harness>://<host>/<harness-ref>`; never call an address carried across a restart current" (prohibition on currency, not on the form) |
| R22 | VIOLATION | 55: society defined; "never call a decision one member makes for another the society's" (other concern) |
| R22 | VIOLATION | 67: authority check defined; "never call a peer's word the owner's" (other concern) |
| R22 | VIOLATION | 159: join prompt defined; "never call its absence proof that no society exists" (other concern) |
| R23 | VIOLATION | 55: "working as more than the sum of their parts through collaboration, ambitious advances, and network effects" argues, does not instruct |
| R25 | VIOLATION | 73, 75 "intake line" vs 111 "commons lines" for one concept (a line in `commons.md`) |
| R26 | VIOLATION | 13: "session" never defined anywhere in the file |
| R26 | VIOLATION | 17: "owner" used; defined at 59. 33: "society" used; defined at 55. 35: "cards", "commons", "resource board", "pointer", "inboxes" used; defined at 37, 71, 79, 81, 87. 47: "`[notice]`" used; defined at 97. 107: "gossip", "`spread:`" used; defined at 121, 123 (five separate first-use failures) |
| R26 | VIOLATION | 39: "worktree" (git term) undefined |
| R26 | VIOLATION | 23: "turn" (narrow sense) undefined |
| R26 | VIOLATION | 91, 109: "tool round" undefined |
| R26 | VIOLATION | 157, 159: "hook" undefined |
| R26/R27 | VIOLATION | 121: "unknown unknowns and unknown knowns" |
Violations counted: R15 1, R16 1, R18 4, R22 4, R23 1, R25 1, R26 5 first-use clusters at 17-107 + session + worktree + turn + tool round + hook + unknown = counted as 11, total 23.
Verdict: **23 violations**.

### join (70 lines)
| rule | result | line: offending text |
|---|---|---|
| R8 | VIOLATION | 13: "Join whenever you learn of the society — at session start, from a hook, a peer's message, or the owner's word, mid-task included" (conditions already in description line 5) |
| R14 | VIOLATION | 45 "Stop before any write when you start inside a live peer's checkout" sits after 35-37 (card moved/written); 23 "before you write any card" also precedes it |
| R16 | VIOLATION | 9: sentence copied verbatim into 24 skills |
| R18 | VIOLATION | 27: "Bring the owner the choice when several cards match, holding meanwhile the one with the latest `updated`" (two instructions) |
| R22 | VIOLATION | 27: "holding meanwhile the one with the latest `updated`; never pick one by guess" (hold is a pick; prohibition covers another act) |
| R22 | VIOLATION | 35: "Move your card back from `<root>/departed/` ...; never write a second card for one member" |
| R22 | VIOLATION | 37: "Make your card present and true by the skill `card`; never work joined without one" |
| R22 | VIOLATION | 41: "Read presence and the cards ... to know who is live ...; never act on a card whose address presence lacks" |
| R25 | VIOLATION | 47 "worktree" vs 23, 43, 49 "checkout" for one concept |
| R26 | VIOLATION | 47: "worktree" undefined |
| R26 | VIOLATION | 23: `project` card field; 27: `updated` card field. Defined only in card (39, 71), not in ontology, not in the sentence |
Verdict: **12 violations**.

### resume (20 lines)
| rule | result | line: offending text |
|---|---|---|
| R16 | VIOLATION | 9: boilerplate sentence |
| R18 | VIOLATION | 15: "Re-read your card and each society skill you were using" (two things re-read) |
| R22 | VIOLATION | 13: "Rejoin by the skill `join`, which finds your existing card; never write a new card for a resumed body" (prohibition of another act) |
| R22 | VIOLATION | 19: "Restore your recurring wake ... by the skill `heartbeat`; never trust it survived" |
| R26 | VIOLATION | 15: "compaction" undefined (ontology and the sentence lack it) |
Verdict: **5 violations**.

### card (90 lines)
| rule | result | line: offending text |
|---|---|---|
| R16 | VIOLATION | 9: boilerplate. 67: "Carry `state: dormant` while the owner parks you, `state: dnd` while the owner orders you left undisturbed" near-copies ontology 43, 45 |
| R18 | VIOLATION | 15: "Keep your card true and current, as flat YAML with one `key: value` per line and lists as YAML lists" (truth + format) |
| R18 | VIOLATION | 67: three instructions (dormant, dnd, no `state`); also repeats 81-87 |
| R19 | VIOLATION | 63: "Carry `knows`, at your choice"; 65: "Carry `reads`, at your choice"; 69: "Carry `wake`, at your choice" (option, not command) |
| R22 | VIOLATION | 15: format half has no prohibition |
| R22 | VIOLATION | 23: "Use the peers plugin's `peers-facts` script as one such means: ...; never run it on a directory other than your working checkout" |
| R22 | VIOLATION | 25: "Use the peers plugin's `peers-card` script ...; never count a line it leaves as checked" |
| R26 | VIOLATION | 17: "session plumbing" |
| R26 | VIOLATION | 39: "git common directory", "worktree" undefined |
| R26 | VIOLATION | 63: "commons tag words" undefined |
Counted: R16 2, R18 2, R19 3, R22 3, R26 3 = 13.
Verdict: **13 violations**.

### tell (74 lines)
| rule | result | line: offending text |
|---|---|---|
| R2 | VIOLATION | 17: "Forward an owner ruling that bears on a running subagent of yours to that subagent" (not sending a tagged message to a peer) |
| R16 | VIOLATION | 9: boilerplate |
| R16 | VIOLATION | 31 ("what can corrupt or kill the peer's work now"), 43 (`[<type>] <one self-contained sentence>`), 45 (`reply: none \| by <time> \| when convenient · sent <stamp>`), 49 ("ten lines at most") copy ontology 95, 97 |
| R18 | VIOLATION | 21: "Reach the peers a message concerns, weighing their time and effort above your own" |
| R18 | VIOLATION | 39: "Escalate ... when its matter outruns that level, stating the reason in the message" |
| R18 | VIOLATION | 51: "Put longer content in a file in your own tree and send its path" |
| R22 | VIOLATION | 35: "Send feedback ... as a `[notice]`; never let a bad answer stand" |
Counted: R2 1, R16 5 (9, 31, 43, 45, 49), R18 3, R22 1 = 10.
Verdict: **10 violations**.

### receive (58 lines)
| rule | result | line: offending text |
|---|---|---|
| R2 | VIOLATION | 53-57: "Keep your own continuity ...", "Write a receipt line ...", "Raise a received claim ... into a verified record" (record keeping; roster: continuity is "a line in ontology or join", not receive) |
| R16 | VIOLATION | 9: boilerplate |
| R18 | VIOLATION | 31: answer + "cut to what the need uses" + carry the thing (one sentence, 60+ words) |
| R18 | VIOLATION | 53: keep continuity "by the skill `memento:record-writing` where memento runs, and otherwise wherever your project keeps its records" (two routes) |
| R22 | VIOLATION | 49: "Adopt or ignore an offered finding ... by the skill `adopt`; never reply to it beyond the thank-you" |
| R22 | VIOLATION | 53: "never keep a peer log in the root" (other concern) |
| R26 | VIOLATION | 53-57: "memento", "continuity", "verified record" undefined; the named memento skills are not ontology |
Verdict: **7 violations**.

### leave (30 lines)
| rule | result | line: offending text |
|---|---|---|
| R8 | VIOLATION | 13: "when the owner ends your session" (condition already in description lines 4, 5) |
| R14 | VIOLATION | 13 announces "any handoff path" before 19 (hand on the scribe role) produces it |
| R16 | VIOLATION | 9: boilerplate |
Verdict: **3 violations**.

## 2. Cross-skill checks

### Edges (roster graph vs text)
| skill | graph says | text names | missing | extra |
|---|---|---|---|---|
| ontology | leaf | 147: protocol-change, ask-around, spread-around | none | 3 (bare names at 147) |
| join | card, receive, heartbeat | card 37, receive 65, heartbeat 67, ontology 9, 17 | none | none |
| resume | not in roster | join 13, heartbeat 19, ontology 9 | n/a | n/a; no skill names `resume` (grep: only adopt 13 as the word "resume"); join does not name it |
| card | tell | tell 77, heartbeat 89, ontology 9 | none | heartbeat (89) |
| tell | receive | receive 69, ontology 9 | none | none |
| receive | adopt, vouch, tell, gossip, quote, consent | vouch 23, tell 31, gossip 37, 43, quote 45, consent 47, adopt 49, card 19, memento:record-writing 53, memento:event-capture 55, memento:record-promotion 57 | none | card (19), memento ×3 (53, 55, 57) |
| leave | tell, card, steward, scribe, heartbeat, sweep (roster 77) | tell 13, steward 17, scribe 19, heartbeat 21, card 25, sweep 29 | none | none |
Every edge sits at the step where it applies. Every skill names `ontology` at line 9.

### Copies
- Boilerplate `Read every society term here as the skill `ontology` defines it; never read one in another sense.` is line 9 of 24 skills, including all six non-ontology skills here (grep). Literal R16 hit; counted once per skill.
- ontology 95/97 vs tell 31, 43, 45, 49: same strings (grep `reply: none | by <time>`, `one self-contained sentence`, `ten lines at most`, `corrupt or kill`).
- ontology 43, 45 vs card 67, 81-87: same `state:` definitions.
- join 67 / resume 19 / leave 21 / card 89 / volunteer 15 each carry a wake sentence by `heartbeat`; wording differs, not copies.
- No other sentence copied (grep of distinctive phrases `departed/`, `commons_read`, `leave notice`, `the thing itself`).

### Round skills
- protocol-change names neither propose nor consent: PASS (only `protocol-change` 5 and `ontology` 9 as skill names; "proposer" at 25 is a word).
- propose names protocol-change: PASS (propose 29). consent names protocol-change: PASS (consent 15).

## 3. Content check (inferred procedure vs roster row)
| skill | inferred one-sentence procedure | roster row | match |
|---|---|---|---|
| ontology | Define the terms and levels the other skills use. | define the terms ... (priority table inside) | MATCH; seams map and priority levels in scope |
| join | Join the society: find a member id, make the card, avoid peers' checkouts, reclaim what an earlier body held, catch up. | join the society (nothing else) | MATCH with overlap: 35 and 53-55 are rejoin content, which resume names |
| resume | Rejoin as the same member after a restart and restore the wake. | no row | NO ROW; overlaps join 35, 53-55, 67 |
| card | Keep your card true: fields, facts, parking, notice of change. | keep your card true; dormant/dnd | MATCH |
| tell | Send a tagged message to a peer by the receiver's state. | send a tagged message (tag, summary, reply line, ten lines, holds) | MISMATCH at 17 (subagent forwarding) |
| receive | Act on an arriving message and route each kind. | what to do when a message arrives | MISMATCH at 53-57 (record keeping) |
| leave | Leave the society: announce, release, end wake, move card. | leave the society | MATCH |

## 4. Verdicts
| skill | verdict |
|---|---|
| ontology | 23 violations |
| join | 12 violations |
| resume | 5 violations |
| card | 13 violations |
| tell | 10 violations |
| receive | 7 violations |
| leave | 3 violations |
Boilerplate R16 (line 9) accounts for 6 of these (join, resume, card, tell, receive, leave); discount if the owner rules the by-name ontology sentence exempt.

## Comparison with self-audit (read after)
`self-audit.md` marks every rule PASS for all seven skills (0 occurrences of VIOLATION or FAIL; rows 10, 16, 20, 24 read "PASS — ..." identically on every skill). This audit disagrees on R2 (tell 17, receive 53-57), R8 (join 13, leave 13), R14 (join 45, leave 13), R16, R18, R19 (card 63, 65, 69), R22, R25, R26.

## Summary
Seven skills were audited sentence by sentence: none conforms (ontology 23, card 13, join 12, tell 10, receive 7, resume 5, leave 3 violations). The recurring failures are multi-instruction sentences, prohibitions that pair with a different concern than the positive half, undefined git/Claude terms (worktree, session, hook, compaction), copied ontology text in tell and card, and skills carrying a second procedure (tell 17, receive 53-57). All roster edges for the group are present at their steps, with extra edges at card 89, receive 19, 53, 55, 57 and ontology 147, and protocol-change, propose and consent satisfy the round rule.
