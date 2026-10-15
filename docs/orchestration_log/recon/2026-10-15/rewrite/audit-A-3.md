# Audit A, round 3: ontology, join, resume, card, tell, receive, leave

Branch `draft/10-skills`, head abf83b9, `/Users/ryzhakar/pp/aoa-skills/peers/skills/<name>/SKILL.md`. Same rules (one-part-name rule void). Done from scratch on the current text; `self-audit.md` not read.

Mechanical checks, all seven skills: R3 PASS; R4 PASS (no `version`); R6 PASS; R7 PASS; R9-R13 PASS (no attribute, all tags imperative verb phrases); R17 PASS; R20/R21 PASS (grep `only|always|must`: none; every body sentence has exactly one `never` outside backticks, checked by script); R16 PASS (shape strings `reply: none`, `one self-contained sentence`, `corrupt or kill` each in one skill; the shared `<take-the-terms>` frame carries per-skill lists).

## Extra check: does each opening terms sentence list every ontology term the body uses
1. Ran `tests/test_terms.py`'s own `used_terms` / `listed_terms` (pytest stubbed; pytest is not installed): join, resume, card, tell, receive, leave each return used-not-listed `[]` and listed-not-used `[]`.
2. Read every body against its list by hand, independent of the test's regexes. Omissions found: none for a term the test knows. One gap lies outside the test's term list: the word "body" in a message sense (tell 53, 55, 57, 59; ontology 161 "gossip body") against ontology 45, where "body" is a member's session. Tell's list does not name `body`, and ontology gives the message sense no definition. Counted below. Second gap outside the test: "plugin" (see ontology).

## Remaining violations per skill

### ontology: 4
| rule | line: text |
|---|---|
| R25/R26 | 45 "Call a member's body the session that currently runs it" vs 161 "that open a gossip body" and tell 53-59 "the body": one word, two senses, the message sense undefined |
| R26 | 87: "each by address, name, and state" uses "state" before 99 defines it; 107: "opens with its type" uses "type" before 109 defines it |
| R26 | 51, 215, 227, 239, 241 "the peers plugin's skills" (and card 25, 27): "plugin" is defined only inside the memento sentence at 73, not as a term |
| R27 | 197: "which reaches the sessions its sender's rule for its type names" (no skill or term names that rule) |
Verdict: **4 violations**.

### join: 0
Verdict: **CONFORMS**.

### resume: 0
Verdict: **CONFORMS**.

### card: 0
Verdict: **CONFORMS**.

### tell: 1
| rule | line: text |
|---|---|
| R26 | 53 "Keep the body to facts and paths on one topic", 55, 57, 59: "body" in the message sense, not in tell's list at 9 and not defined (ontology 45 gives it another sense) |
Verdict: **1 violation**.

### receive: 0
Verdict: **CONFORMS**.

### leave: 0
Verdict: **CONFORMS**.

## Round-2 findings, fixed or not
- ontology: FIXED 73 (R18; question tool now a separate sentence), 19 vs ref (R25; `<ref>` named as the harness-ref, 221-223 use harness-ref), 69 memento (R26; memento records defined inline at 73), forward uses (R26; "brought" now "told", "protocol" defined at 51, "relayer" gone), 187 and 195 (R27; reworded at 138 and 134).
- join: FIXED all four (the list at 9 now names root, `[notice]`, subagent, reloaded).
- resume: FIXED 21 (R22; now "never skip setting it again") and society (R26; listed).
- card: FIXED all four (host, peer, `[notice]`, change line listed).
- tell: FIXED 57 (split into 57, 59), 39 (reworded), reply line (now "second line"), `[answer]`, card, root, member (all listed).
- receive: FIXED pointer collision (31 reworded), card and relaying (listed).
- leave: FIXED root, member, `[ask]` (listed).
All round-2 findings fixed.

## New violations from round 3's changes
- ontology 87 and 107 forward use of "state" and "type": new text (state and type split into their own definitions at 99 and 109 after the sentences that use them).
- ontology 197 "sender's rule", 51 "plugin", and the "body" senses (45/161, tell 53-59) were not caught by the generated terms test; they predate round 3 or arrived with it but were not seen before.
- No violation from the generated terms sentences themselves.

## Cross-skill checks
Edges (graph vs text):
| skill | graph | text | missing | extra |
|---|---|---|---|---|
| ontology | leaf | none | none | none |
| join | card, receive, heartbeat | card 51, receive 67, heartbeat 69 | none | none |
| resume | no row | join 13 | n/a | n/a (no skill names `resume`) |
| card | tell | tell 79 | none | none |
| tell | receive | receive 77 | none | none |
| receive | adopt, vouch, tell, gossip, quote, consent | vouch 21, tell 29, gossip 39, 45, quote 47, consent 49, adopt 51 | none | none |
| leave | tell, card, steward, scribe, heartbeat, sweep | steward 13, scribe 15, heartbeat 17, tell 21, card 25, sweep 29 | none | none |
Round skills: `protocol-change`, `propose`, `consent` each name only `ontology`, and `propose` and `consent` also `protocol-change`; `protocol-change` names neither `propose` nor `consent`: PASS.
Content: procedures match the roster rows for every skill (ontology defines terms; join joins; card keeps the card; tell sends a message; receive acts on arrivals; leave leaves; resume rejoins by `join`). Roster note unchanged: no skill in the group names `memento:record-writing`.

## Summary
Round 3 fixed every round-2 finding, and join, resume, card, receive and leave now conform. The generated terms sentences list every term the test knows each body uses (used-not-listed empty for all six skills), but the test's term list misses the word "body" in the message sense, which leaves tell at 1 violation. Ontology has 4 remaining (body sense, forward use of "state" and "type", undefined "plugin", the unnamed "sender's rule"). Counts: ontology 4, join 0, resume 0, card 0, tell 1, receive 0, leave 0.
