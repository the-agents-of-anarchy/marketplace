# Skill audit: protocol-10 skills vs memento:skill-creation

Tree: `/Users/ryzhakar/pp/aoa-participation`, branch `draft/9.4-participation`, HEAD 25395cf (reverts ddc1802). Fourth skill dir is `peers/skills/tend-commons/`, not `tend`. Cites are line numbers in each skill's `SKILL.md`. Rules: `memento/0.5.1/skills/skill-creation/SKILL.md`. Judgment calls (pairing, one-instruction, undefined terms) are mine and literal; line lists let each be checked.

Method: emphatic words counted by `grep -w` outside backticks. Tag attributes, bullets, tables, code fences: grep found none. Skill paths in bodies: grep found none.

## 1. Verdicts by rule

Cell = PASS, or VIOLATION with lines. NA = not checkable from the artifact.

| Rule (quoted) | join | gossip | amend | tend-commons |
|---|---|---|---|---|
| settle: "Name the one procedure ... before writing a line" | NA | NA | NA | NA |
| settle: "Cover one procedure per skill; never cover a second." | VIOLATION 1-428 (see 3) | VIOLATION 22-34, 80-92 vs 8-20, 36-78 | VIOLATION 12-74 vs 76-90 (desc :4 names both) | VIOLATION 20-34, 36-42, 44-52 (desc :4 three verbs); borderline |
| settle: "Write a skill where reading it does the work" | PASS | PASS | PASS | PASS |
| name-the-file: "Name ... `SKILL.md`" | PASS | PASS | PASS | PASS |
| open: frontmatter with `name`, `description` | PASS | PASS | PASS | PASS |
| open: "Never carry a version field" | PASS | PASS | PASS | PASS |
| open: "two or three lowercase parts, hyphen-joined, naming what it does; never carry a fourth part" | VIOLATION :2 (1 part) | VIOLATION :2 (1 part) | VIOLATION :2 (1 part) | PASS :2 (2 parts) |
| open: "Set the directory name to `name`" | PASS | PASS | PASS | PASS |
| open: description "one sentence ... followed by the phrases and conditions" | PASS :4-5 | PASS :4-5 | PASS :4-5 | PASS :4-5 |
| open: "never put one in the body" | VIOLATION :131 | VIOLATION :59 | PASS | PASS |
| body: "Structure the body in XML tags" | PASS | PASS | PASS | PASS |
| body: "imperative verb phrase" tag names | PASS (16 tags) | PASS (6) | PASS (3) | PASS (5) |
| body: "never carry one outside a tag" | PASS | PASS | PASS | PASS |
| body: "never give a tag an attribute" | PASS | PASS | PASS | PASS |
| body: "prose and inline backticks" only | PASS | PASS | PASS | PASS |
| body: "Order the body as the procedure runs" | NA | NA | NA | NA |
| body: "never point outside it to fetch, except by naming another skill" | VIOLATION :159, :163 | PASS | VIOLATION :63 | PASS |
| body: "never copy shared content into two skills" | VIOLATION :233, :237, :239, :267, :405 | VIOLATION :33, :37, :55, :91 | VIOLATION :13, :23, :87 | PASS |
| body: "Reference another skill by name; never by its path" | PASS | PASS | PASS | PASS |
| write: "one instruction per sentence; never spread one across two" | VIOLATION 14: :21 :111 :137 :243 :245 :303 :315 :339 :385 :387 :407; spread :239 :247 :361 | VIOLATION 3: :65 :69; spread :85-87 | VIOLATION 2: :23 :47 | PASS |
| write: "every instruction as a command; never as a suggestion" | VIOLATION :209, :211 ("at your choice") | PASS | PASS | PASS |
| write: "at most one emphatic word" (counted outside backticks) | VIOLATION :125 (`never` + `only`) | VIOLATION :25 (`never` + `only`) | PASS | PASS |
| write: "pair every positive instruction with the prohibition of that same instruction" | VIOLATION 31: :19 :31 :53 :73 :81 :85 :91 :93 :101 :103 :111 :113 :115 :125 :135 :143 :163 :237 :243 :245 :293 :303 :319 :337 :365 :381 :385 :391 :399 :413 :415 | VIOLATION 7: :17 :19 :47 :61 :63 :65 :85 | VIOLATION 10: :13 :21 :41 :47 :53 :55 :61 :63 :69 :81 | VIOLATION 1: :21 |
| write: "State the instruction; never argue for it." | VIOLATION :11, :33, :35 | PASS | PASS | PASS |
| write: "never narrate a failure to meet it" | PASS | PASS | PASS | PASS |
| write: "one term per concept" | VIOLATION 2 groups: item/line/lesson :313 :317 :337; body/session :65 :73 :179 | VIOLATION 2 groups: origin/originator :47 :49 :63 :67; receiver/recipient :61 :63 :65 | VIOLATION 1 group: request/ask :21 :25 :83 :89 | VIOLATION 1 group: item/line :41 vs :21 |
| write: "Define every term ... in the sentence that first uses it" | VIOLATION 6: :13 :65 :155 :249 :331 :369-377 | VIOLATION 6: :13 :23 :47 :49 :73 :77 | VIOLATION 6: :9 :23 :27 :33 :37 :45 | VIOLATION 5: :9 :15 :17 :21 :45 |
| write: "ordinary words" | PASS | PASS | PASS | PASS |
| write: "Keep every sentence that instructs or forbids; never keep another." | VIOLATION :9 | PASS | PASS | PASS |
| verify: "never deliver a skill that breaks one" | VIOLATION (follows from rows above) | VIOLATION | VIOLATION | VIOLATION |

Quoted offending text, by cite:
- join:9 "This skill is peer protocol 10." (statement, and a version carried in the body).
- join:125 "... keeps it in the session only and ends it after seven days; never count one as lasting past either."
- gossip:25 "... never treat the commons as the only source."
- join:131 "Join whenever you learn of the society — at session start, from a hook, a peer's message, or the owner's word" duplicates join:5 triggers.
- gossip:59 "Relay a gossip on seeing its `relay:` line" duplicates gossip:5 "a gossip message arriving with a `relay:` line".
- join:159 "Know the protocol version in force, from the pointer's `version`"; join:163 "Apply the pointer's change lines above this skill's version when the pointer is newer". amend:63 same. Instructions fetched from `<root>/PROTOCOL.md`, outside the skill.
- join:239 "except as the next three instructions require", join:247 "except as the next instructions require", join:361 "except as the next instruction allows". Each spreads one instruction across sentences.
- join:243 "Send a session presence shows `busy` nothing but `[hazard]` messages, holding every other message until ..." (send, and hold).
- join:407 "Propose, answer, adopt, and ship protocol changes, and pass on the scribe role, by the skill `amend`" (five instructions).
- join:209 "Carry `knows`, at your choice"; join:211 "Carry `reads`, at your choice" (optional, so not a command).
- join:33 "the trust base between peers"; join:35 "as the society's scarcest resource"; join:11 "through collaboration, proactive and ambitious advances, and network effects" (reasons given for the instruction).
- Copies: join:233 = gossip:91 (silent on an ask you cannot place); join:237 = gossip:33 (bad answer stands); join:239 = gossip:37 (send in the turn you learn it); join:267 = gossip:55 = amend:23 (ten-line body); join:405 = amend:13 (definition of the scribe); join:353, :387 = amend:87 (escalate a dispute to the owner only when both sides ask).
- amend:9, tend-commons:9 "Act under the skill `join`, which defines the society, member, peer, card, root ..." leave every listed term undefined in the skill. tend-commons:9 also lists "authority check"; the word appears nowhere else in tend-commons.

## 2. Counts by rule and ten most serious, per skill

Count = lines cited in section 1 (groups counted once). Rule keys: SK one procedure, NM name, DS description, OU outside pointer, CP copied content, I1 one instruction, EM emphatic, PR pairing, CM command, AR argument, TM one term, UD undefined term, NI non-instruction, VF verify.

### join: 71 violations

SK 1, NM 1, DS 1, OU 2, CP 5, I1 14, EM 1, PR 31, CM 2, AR 3, TM 2, UD 6, NI 1, VF 1.

1. join:1-428: carries ten procedures; see 3. Rule: "Cover one procedure per skill; never cover a second."
2. join:9: "This skill is peer protocol 10." instructs nothing. Rule: "Keep every sentence that instructs or forbids; never keep another."
3. join:2: `name: join` has one part. Rule: "two or three lowercase parts".
4. join:163: change lines are fetched from the pointer, outside the skill. Rule: "never point outside it to fetch".
5. join:125: `never` and `only` in one sentence. Rule: "Cap each sentence at one emphatic word".
6. join:239, :247, :361: "except as the next ... instruction(s) require" spreads one instruction across sentences. Rule: "never spread one across two".
7. join:243: send-only-hazards and hold-the-rest are two instructions in one sentence. Rule: "Write one instruction per sentence".
8. join:407: five instructions in one sentence. Same rule.
9. join:405 (scribe), :233, :237, :239, :267: content also carried in amend and gossip. Rule: "never copy shared content into two skills".
10. join:131: trigger conditions in the body. Rule: "Put every phrase and condition a request matches in the description; never put one in the body".

Next by weight: join:13, :155 (term used before its definition at :83, :343); join:31, :53, :73, :85 (`never` clause names another concern).

### gossip: 27 violations

SK 1, NM 1, DS 1, CP 4, I1 3, EM 1, PR 7, TM 2, UD 6, VF 1.

1. gossip:22-34 and :80-92: asking and answering direct asks (:25, :83, :89) is the targeted send that :11 hands to join. Rule: "Cover one procedure per skill".
2. gossip:2: one-part name.
3. gossip:25: `never` and `only`.
4. gossip:59: relay trigger in the body.
5. gossip:33, :37, :55, :91: copies of join:237, :239, :267, :233.
6. gossip:65: "Add yourself to `has:` before you pass a gossip on, and each recipient as you send" is two instructions.
7. gossip:69: "Correct a checkable error ... before relaying, marking it" is two instructions.
8. gossip:85-87: telling the seeker and naming what serves are one instruction over two sentences.
9. gossip:13, :23, :73: `[ask]`, `[notice]`, `[answer]`, "the commons" used with no definition here.
10. gossip:47 vs :49: "origin" and "originator" for one concept. Also gossip:17, :19, :47, :61, :63, :65, :85: `never` clause names another concern.

### amend: 26 violations

SK 1, NM 1, OU 1, CP 3, I1 2, PR 10, TM 1, UD 6, VF 1.

1. amend:12-74 and :76-90: consent round and scribe succession; description :4 names both. Rule: "Cover one procedure per skill".
2. amend:2: one-part name.
3. amend:9: twelve terms left to join. Rule: "Define every term ... in the sentence that first uses it".
4. amend:63: "Apply the change lines above your loaded version on that notice or a newer pointer". Rule: "never point outside it to fetch".
5. amend:13: scribe definition also at join:405.
6. amend:23: ten-line body also at join:267 and gossip:55.
7. amend:47: "Bind a silent member ..., open to a late objection" is two instructions.
8. amend:23: "in a file in your own tree, inline at ten lines or fewer" gives two placements for one instruction.
9. amend:21, :25, :83, :89: "ask" and "request" for one concept.
10. amend:13, :21, :41, :47, :53, :55, :61, :63, :69, :81: `never` clause names another concern. Also amend:27, :33, :37, :45: "round", "heavy work", "separate", "loaded version" undefined.

### tend-commons: 9 violations

SK 1, PR 1, TM 1, UD 5, VF 1.

1. tend-commons:20-52: writing, tending, and carrying are three runnable procedures; description :4 lists three verbs. Rule: "Cover one procedure per skill". Borderline.
2. tend-commons:9: nine terms left to join, and "authority check" listed though unused.
3. tend-commons:15: "commons areas" undefined.
4. tend-commons:17: "collective and personal wisdom" undefined.
5. tend-commons:21: "stamp", "member", "[<tags>]" undefined here.
6. tend-commons:45: "card" and "live peer" undefined here.
7. tend-commons:21: "Use `<root>/commons.md` as the library's intake ...; never write a line without its evidence path" pairs use with a prohibition on writing.
8. tend-commons:41 "item" vs :21 "line".
9. Verify rule, by the rows above.

## 3. join: one procedure after the split?

No. join carries more than one procedure. The 9.3 split removed amend (consent round, scribe) and the commons write/tend text; 428 lines remain (protocol-10-changes.md:18).

Procedures in join, each runnable alone:
1. Join the society: 130-166.
2. Keep your card true: 168-220.
3. Send messages (tags, reply line, inbox, busy and dormant holds): 222-278.
4. Give mutual aid: 280-288.
5. Participate when not busy: 290-304.
6. Use the commons (read-side core): 306-340.
7. Steward shared things and exclusive resources: 342-378.
8. Settle disputes through a go-between: 380-388.
9. Relay owner rulings: 390-396.
10. Keep continuity in your own records: 398-402.
11. Leave, park, or end: 410-428.

Not procedures, but present: purpose 8-28, owner stance 30-58, checked-facts vocabulary 60-104, Claude Code mapping 106-128, protocol-change pointer 404-408.

## 4. Rule for the names

Quoted, open-the-skill: "Take `name` from the procedure named above — two or three lowercase parts, hyphen-joined, naming what it does; never carry a fourth part." and "Set the directory name to `name`; never let the two differ."

Read literally, "two or three" excludes one part, and "never carry a fourth part" excludes four or more. protocol-10-changes.md:241 reads it the same way.

| Skill | name line | Parts | Verdict | Directory = name |
|---|---|---|---|---|
| `join` | join/SKILL.md:2 | 1 | VIOLATION: fewer than two parts; names the first of eleven procedures (see 3), not what the skill does | yes |
| `gossip` | gossip/SKILL.md:2 | 1 | VIOLATION: fewer than two parts | yes |
| `amend` | amend/SKILL.md:2 | 1 | VIOLATION: fewer than two parts | yes |
| `tend-commons` | tend-commons/SKILL.md:2 | 2 | PASS: two parts, verb and object, lowercase, hyphen-joined | yes |

The owner accepted `join` and `gossip` (brief); that ruling is not a rule in the rules file, so the table stands as written.

## Summary

All four skills break the rules: join 71 violations, gossip 27, amend 26, tend-commons 9, counted by the lines cited above. join still carries eleven procedures after the split, and amend and gossip each carry two. By the rule, `join`, `gossip`, and `amend` fail the two-or-three-part name rule and `tend-commons` passes it.
