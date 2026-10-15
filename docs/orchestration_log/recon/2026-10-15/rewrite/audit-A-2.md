# Audit A, round 2: ontology, join, resume, card, tell, receive, leave

Branch `draft/10-skills`, head 52cc0ac, `/Users/ryzhakar/pp/aoa-skills/peers/skills/<name>/SKILL.md`. Same rules as round 1 (one-part-name rule void). Done from scratch; `self-audit.md` not read.

Mechanical checks, all seven skills: R3 PASS (one `SKILL.md` per directory); R4 PASS (no `version`); R6 PASS; R7 PASS (line 4 one sentence, line 5 phrases); R9-R13 PASS (every tag `<verb-phrase>`, no attribute, grep clean); R17 PASS; R20/R21 PASS (grep `only|always|must`: none; every body sentence has exactly one `never`, none has two); R3-R17 other than listed below PASS. R16 on `<take-the-terms>`: the frame `Take ... as the skill `ontology` defines them; never take them in another sense.` is shared, the term lists differ per skill; counted PASS.

## Remaining violations per skill

### ontology (238 lines): 6
| rule | line: text |
|---|---|
| R18 | 73: "Call bringing a matter to the owner writing it ..., a question through the harness's question tool, the function prompting the owner with a question, in a turn answering the owner's word counting as part of that answer" (defines bringing and the question tool in one sentence; 233 defines the question tool again) |
| R25 | 19, 21 "harness-ref" vs 219, 221, 223 "ref" for the same identifier |
| R26 | 69: "memento records where the memento plugin runs" (memento undefined) |
| R26 | forward use before definition: 63 "brought" (73), 97 "protocol" (205), 117 "relayer" (161) |
| R27 | 187: "the level below that its type sets" (not a readable sentence; the levels are 189-193) |
| R27 | 195: "any act it calls for, recognizing that it changes nothing you do included" |
Verdict: **6 violations**.

### join (72 lines): 4
| rule | line: text |
|---|---|
| R26 | 33, 41, 47: `<root>` used; `root` not in the list at 9 (ontology 47) |
| R26 | 27, 57: `[notice]` used; not in the list at 9 (ontology 109) |
| R26 | 15: "subagent" used; not in the list (ontology 33) |
| R26 | 63: "reload" used; not in the list (ontology 235) |
Verdict: **4 violations**.

### resume (22 lines): 2
| rule | line: text |
|---|---|
| R22 | 21: "Set your wake again from your card's `wake` field; never assume it survived." (prohibition of another concern) |
| R26 | 19: "each society skill" (`society` not in the list at 9; ontology 49) |
Verdict: **2 violations**.

### card (90 lines): 4
| rule | line: text |
|---|---|
| R26 | 23: "host" not in the list at 9 (ontology 17) |
| R26 | 61: "which peers stay off" (`peer` not listed; ontology 127) |
| R26 | 79: "Send a `[notice]`" (`[notice]` not listed; ontology 109) |
| R26 | 55: "applying change lines" (`change line` not listed; ontology 203) |
Verdict: **4 violations**.

### tell (78 lines): 7
| rule | line: text |
|---|---|
| R18 | 57: "Put longer content in a file in your checkout, the body carrying its path" (two instructions) |
| R27 | 39: "Send each peer a failure of your own reached a `[notice]` correcting it" (not a readable command) |
| R26 | 49: "reply line" undefined in the file and in ontology (ontology 113 defines only "reply time") |
| R26 | 75: `[answer]` not in the list at 9 (ontology 107) |
| R26 | 65: "whose card carries `reads`" (`card` not listed; ontology 53) |
| R26 | 71: `<root>/inbox/<member>.md` (`root`, `member` not listed; ontology 47, 43) counted as 2 (`root`, `member`) |
Verdict: **7 violations**.

### receive (52 lines): 3
| rule | line: text |
|---|---|
| R25/R26 | 31: "never send a bare pointer" uses "pointer", which ontology 201 defines as `<root>/PROTOCOL.md` |
| R26 | 13: "your card's `reads`" (`card` not listed at 9; ontology 53) |
| R26 | 45: "Relay a message" (`relaying` not listed; ontology 161) |
Verdict: **3 violations**.

### leave (30 lines): 3
| rule | line: text |
|---|---|
| R26 | 27: `<root>/departed/` (`root` not listed at 9; ontology 47) |
| R26 | 29: "other members' cards" (`member` not listed; ontology 43) |
| R26 | 21: "the asks you withdraw" (`[ask]` not listed; ontology 105) |
Verdict: **3 violations**.

## Round-1 findings: fixed or not
- ontology: all FIXED. R15 extra edges (no skill name left in ontology; grep clean). R16 (95, 97 shape strings now only in tell; grep). R18 at 13, 73-split, 95, 97 (now one term per sentence; 73 reappears above as a new finding). R22 at 15, 55, 67, 159. R23 at 55. R25 intake/commons lines (grep: one term). R26 session, worktree, turn, tool round, hook, unknown unknowns, and the 17/33/35/47/107 order failures.
- join: all FIXED. R8 (13 no longer lists triggers), R14 (checkout section now precedes card), R16, R18 (27 split into 37, 39), R22 (27, 35, 37, 41), R25/R26 worktree, R26 `project`/`updated` (defined in the sentences).
- resume: FIXED R16, R18 (split to 17, 19), R22 at 13, R26 compaction. NOT FIXED: R22 old 19, now 21 (still "never assume it survived").
- card: all FIXED. R16 (9, 67), R18 (15, 67), R19 (63, 65, 69 now conditional), R22 (15, 23, 25), R26 (plumbing, worktree/git common directory, tag words), extra edge `heartbeat` removed.
- tell: FIXED R2 (17 gone), R16 (31, 43, 45, 49 no longer in ontology), R18 at 21 and 39, R22 at 35. NOT FIXED: R18 old 51, now 57.
- receive: all FIXED. R2 (record keeping gone), R16, R18 (31, 53), R22 (49, 53), R26 (memento terms gone), extra edges `card`, `memento:*` gone.
- leave: all FIXED. R8 (13), R14 (announce now follows the hand-on), R16.

## New violations the fixes introduced
- ontology 73 (R18, bringing + question tool in one sentence), 19 vs 219-223 (R25 `harness-ref`/`ref`), 69 (R26 memento), 187 (R27), 195 unchanged text.
- join 9, card 9, tell 9, receive 9, leave 9, resume 9: the per-skill term lists omit terms their bodies use (the mechanism the fix introduced; each gap listed above).
- tell 39 (R27) came with the added correction sentence.

## Cross-skill checks
Edges, roster graph vs text (all at the step where they apply):
| skill | graph | text | missing | extra |
|---|---|---|---|---|
| ontology | leaf | none | none | none |
| join | card, receive, heartbeat | card 51, receive 67, heartbeat 69 | none | none |
| card | tell | tell 79 | none | none |
| tell | receive | receive 75 | none | none |
| receive | adopt, vouch, tell, gossip, quote, consent | vouch 21, tell 29, gossip 39, 45, quote 47, consent 49, adopt 51 | none | none |
| leave | tell, card, steward, scribe, heartbeat, sweep | steward 13, scribe 15, heartbeat 17, tell 21, card 25, sweep 29 | none | none |
| resume | not in roster | join 13 | n/a | n/a; no skill names `resume` (grep); `heartbeat` no longer named at 21 |
Copies: no sentence of the group appears in another skill (grep `reply: none`, `one self-contained sentence`, `corrupt or kill`, `intake`, `record-writing`). `ten lines` recurs in propose 21, gossip 33, tell 55, receive 31 in different sentences.
Rounds: `protocol-change` names neither `propose` nor `consent` (PASS); `propose` names `protocol-change` at 25 (PASS); `consent` names it at 15 (PASS).
Roster note: continuity should be "a line in ontology or join naming memento:record-writing"; grep finds that skill name nowhere in the group (ontology 69 names "memento records" in prose only).

## Content check
| skill | procedure inferred | roster |
|---|---|---|
| ontology | define the terms and levels the skills use | MATCH |
| join | join the society: id, card, stay out of peers' checkouts, reclaim, catch up | MATCH |
| resume | rejoin by `join` and restore card, skills, wake | no row |
| card | keep the card true, announce, park | MATCH |
| tell | send a tagged message | MATCH |
| receive | act on an arriving message, route by kind | MATCH |
| leave | release, end wake, announce, move the card | MATCH |

## Summary
Round 2 cleared every round-1 finding except resume 21 (R22) and tell 57 (R18), and it added new gaps: the per-skill `<take-the-terms>` lists omit terms the bodies use, ontology gained a long sentence at 73, `harness-ref`/`ref` and the "bare pointer" collision with the pointer term, and two unreadable sentences (ontology 187, tell 39). All roster edges are present at their steps with no extras, no copied sentences remain, and the round rule holds. Counts: ontology 6, join 4, resume 2, card 4, tell 7, receive 3, leave 3; none conforms.
