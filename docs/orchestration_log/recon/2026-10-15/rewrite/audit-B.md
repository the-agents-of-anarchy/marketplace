# Audit B — gossip, ask-around, spread-around, quote, vouch, adopt, tend, aid, volunteer, heartbeat

Rules: memento 0.5.1 skill-creation SKILL.md. Skills: /Users/ryzhakar/pp/aoa-skills/peers/skills/<name>/SKILL.md. Line numbers are file lines. Name-part rule void per owner; one-part names not flagged. Counts are one per violating sentence-and-rule. Rule 14 includes the identical `read-the-terms` sentence (see cross-skill).

## 1. Matrix (P = pass, Vn = n violations; detail in section 2)

| # | rule | gos | ask | spr | quo | vou | ado | ten | aid | vol | hrt |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | one procedure, named; no second | P | P | P | P | V1 | P | P | P | V1 | P |
| 2 | file named SKILL.md | P | P | P | P | P | P | P | P | P | P |
| 3 | frontmatter name+description, no version | P | P | P | P | P | P | P | P | P | P |
| 4 | directory = name | P | P | P | P | P | P | P | P | P | P |
| 5 | description: one sentence, then phrases | P | P | P | P | P | P | P | P | P | P |
| 6 | no trigger in body | P | P | P | P | P | V1 | P | P | P | P |
| 7 | body in XML tags | P | P | P | P | P | P | P | P | P | P |
| 8 | tag names imperative verb phrases | P | P | P | P | P | P | P | P | P | P |
| 9 | every instruction inside a tag | P | P | P | P | P | P | P | P | P | P |
| 10 | no tag attribute | P | P | P | P | P | P | P | P | P | P |
| 11 | tag holds prose + inline backticks only | P | P | P | P | P | P | P | P | P | P |
| 12 | body order = procedure order | P | P | P | P | P | P | P | P | P | P |
| 13 | outside only by skill name | P | P | P | P | P | P | P | P | P | P |
| 14 | shared content not copied | V1 | V1 | V1 | V1 | V1 | V1 | V2 | V1 | V1 | V4 |
| 15 | skill by name, never path | P | P | P | P | P | P | P | P | P | P |
| 16 | one instruction per sentence | V5 | P | P | P | P | V1 | V1 | P | P | V2 |
| 17 | command, not suggestion | V1 | P | P | P | P | P | P | P | P | P |
| 18 | at most one emphatic word | P | P | P | P | P | P | P | P | P | P |
| 19 | positive paired with prohibition of same instruction | V1 | V1 | P | V1 | P | V1 | P | P | V1 | V1 |
| 20 | no argument (bodies) | P | P | P | P | P | P | P | P | P | P |
| 21 | no failure narration | P | P | P | P | P | P | P | P | P | P |
| 22 | one term per concept | V1 | P | P | P | P | P | P | P | P | V2 |
| 23 | non-ordinary terms defined or via ontology | P | P | V1 | V2 | P | V2 | V3 | P | P | P |
| 24 | ordinary words | P | P | P | P | P | V1 | V1 | P | P | P |
| 25 | every sentence instructs or forbids | P | P | P | P | P | P | P | P | P | P |

Rule 18 checked mechanically: no body sentence holds two of never/always/only/must; no frontmatter holds one. Rule 3: no `version` key in any of the ten.

## 2. Violations (file:line, quoted)

### gossip (9)
- R14 L9 `Read every society term here as the skill \`ontology\` defines it; never read one in another sense.` identical sentence and tag in 24 skills.
- R16 L15 `Originate a gossip [ask] by the skill ask-around and a gossip [notice] by the skill spread-around` two originations.
- R16 L31 `Count the envelope within the ten-line body, moving content that does not fit to a file in your own tree named by its path` count and move.
- R16 L43 `Add yourself to has: before you pass a gossip on, and each recipient as you send` two adds, two times.
- R16 L51 `Relay and answer a gossip once, however many copies reach you` relay and answer.
- R16 L55 `Correct a checkable error in the content before relaying, marking it` correct and mark.
- R17 L41 `Pick the recipients by any means, your own judgment of fit included or left out` permission, not command.
- R19 L41 same sentence: prohibition `never add a constraint of your own to the origin's` contradicts positive `your own judgment of fit included`.
- R22 L39 `not barred by status` vs L47 `while busy, dormant, or dnd ... before the state clears` and ontology `state`; two terms for one concept.

(R16 counted 5 above: L15, L31, L43, L51, L55; R17 1; R19 1; R22 1; R14 1 = 9.)

### ask-around (2)
- R14 L9 read-the-terms sentence.
- R19 L29 `Read a peer's silence on your ask as "doesn't know"; never chase it.` prohibition concerns chasing, not the reading.

### spread-around (2)
- R14 L9 read-the-terms sentence.
- R23 L17 `its card's \`focus\` and \`knows\`` card fields defined nowhere in ontology or in the skill.

### quote (4)
- R14 L9 read-the-terms sentence.
- R19 L17 `Weigh the owner's own word under your own authority check; never let a peer speak with the owner's authority.` positive concerns the owner's word, prohibition concerns peers.
- R23 L19 `the relayer's journal line` (also L27 `the journal path`): `journal` undefined here and in ontology.
- R23 L23 `where memento runs` `memento` undefined in the skill and in ontology (`records` L23 likewise unglossed).

### vouch (2)
- R1 L21 `Correct each failure of your own that reached a peer, by a [notice] ...` self-correction is a second procedure; the description names only "route a failed check back to its origin".
- R14 L9 read-the-terms sentence.

### adopt (7)
- R6 L13 `whenever a join, compaction, resume, wake, or peer message already holds your attention` request-matching conditions in body; description names none of them.
- R14 L9 read-the-terms sentence.
- R16 L27 `Read a commons tool whole and run it once your authority check clears it` read, then run.
- R19 L39 `Thank the origin ... by a one-line [notice] ...; never report an adoption in the commons.` prohibition concerns where to report, not how to thank.
- R23 L33 `where memento runs` undefined. R23 L35 `your own conventions` `convention` is defined only in tend L41, not here or in ontology.
- R24 L33 `Write a fresh ground for each adoption` `ground` in the sense of reason is not an ordinary word.

### tend (7)
- R14 L9 read-the-terms sentence.
- R14 L49 `Correct an item that failed honestly in your work, in place, naming the failure; never let a failure go uncorrected.` near-copy of adopt L43 `Correct an item that fails in your work, or proves wrong, by the skill tend; never leave it standing uncorrected.`
- R16 L47 `Keep every line's number through an edit, a retired line reading ... and a merged one ...` three instructions.
- R23 L15 `commons areas`; R23 L17 `collective and personal wisdom`; R23 L39 `a committed path`: three undefined terms.
- R24 L49 `failed honestly` not ordinary usage.

### aid (1)
- R14 L9 read-the-terms sentence.

### volunteer (3)
- R1 L21 `Carry deferred matters and new ideas to the society's public discourse ...; never park them with the owner.` routing ideas is not finding, picking, or doing work.
- R14 L9 read-the-terms sentence.
- R19 L25 `Pick one piece of work in this order: learning, then teaching and asking, then tending and aid; never teach before you learn.` prohibition covers one pair of the order.

### heartbeat (9)
- R14 L9 read-the-terms sentence.
- R14 L31 `seven days on Claude Code` restates ontology L169 `ends after seven days`.
- R14 L39 `never let a wake drop to idling` near-copy of volunteer L13 `never let such a stretch drop to idling`.
- R14 L21 default prompt `compare presence, your card, your inbox, and the commons line count with what you last saw` duplicates adopt L13 count comparison.
- R16 L21 and L23: each quoted prompt packs several instructions (compare; end turn; act on message / commons / free time; load four skills; tend; pull; push; adopt).
- R19 L21 positive sets a fixed prompt; prohibition `never make a default wake load a skill before it finds a change` concerns what the wake does, not the prompt choice (L23's pair is the right shape).
- R22 L17 `default form` / `commons form` vs L21 `default wake` / L23 `commons wake`.
- R22 L21, L23 `peers:receive`, `peers:adopt`, `peers:tend` etc. vs L25 `the skill \`card\``, L39 `the skill \`volunteer\``; two forms for naming a skill.

## 3. Cross-skill checks

### Edges (roster graph vs text). Every skill also names `ontology` (required).
| skill | roster edges | found | missing | extra |
|---|---|---|---|---|
| gossip | ask-around, spread-around, tell | all three (L13, L15, L33, L47, L61) | none | none |
| ask-around | gossip, tell | both (L17, L21) | none | none |
| spread-around | gossip, vouch, tell | all three (L13, L17, L29) | none | none |
| quote | gossip | gossip (L33, L35) | none | vouch (L19), memento:event-capture (L23) |
| aid | tell | tell (L17) | none | vouch (L15) |
| volunteer | ask-around, spread-around, adopt, tend, aid, heartbeat | all six (L15, L29-L37) | none | none |
| heartbeat | volunteer | volunteer (L21, L39) | none | card (L25), receive, adopt, tend, ask-around, spread-around (inside L21, L23 prompts) |
| adopt | vouch, tell | both (L25, L39) | none | tend (L43), memento:record-writing (L33) |
| tend | vouch, spread-around | both (L27, L53) | none | none |
| vouch | leaf beyond ontology | none required | none | tell (L19, L21) |

Missing edges: none. Extra edges: 12 (quote 2, aid 1, heartbeat 6, adopt 2, vouch 1). Roster ruling is "only these"; each extra is a graph departure, not counted in section 2.

### Copies (grep over all 25 skill dirs)
- `Read every society term here as the skill \`ontology\` defines it; never read one in another sense.` is byte-identical in 24 skills (every skill but ontology), and so is the `<read-the-terms>` tag. Shared content copied into every skill.
- adopt L43 vs tend L49 near-copy (above). adopt L13 vs heartbeat L21 near-copy of the count comparison. volunteer L13 vs heartbeat L39 near-copy of the idling clause.
- Overlap without sentence copy, not counted: gossip L21 four envelope lines and L31 ten lines restate ontology L123, L95; tend L31 line form and spread-around L17 card fields have no second home.
- Other distinctive phrases (`fresh ground`, `unasked`, `Correct each failure`, `peers wake`, `Treat the owner as away`) appear in one skill only.

### protocol-change
- No skill in group B names protocol-change, propose, or consent (grep: zero hits). protocol-change names neither propose nor consent as skills (L25 says "proposer", a role word); propose and consent each name protocol-change once (grep count 1 each). Pass; outside group B.

## 4. Content check (procedure inferred, then compared with the roster row)

| skill | inferred one sentence | roster row | match |
|---|---|---|---|
| gossip | Wrap a message in the four-line envelope and relay it once, honoring `spread:` and `has:`, until the origin is reached | the mechanic: envelope, two filters (has, status), relay once | yes |
| ask-around | Seek what you need by a gossip `[ask]` after own effort and a direct ask | gossip applied to seeking | yes |
| spread-around | Offer a finding, directly or by gossip, after vouching | gossip applied to offering | yes; commons-line push (L21-L25) overlaps tend L53 |
| quote | Relay a recorded owner ruling as a `[quote]` by scope | relay an owner ruling: gossip underneath, hazard priority, keeps spreading | yes; L13 (owner away) restates ontology L59 |
| vouch | Check a claim and route a failed check to its origin | check a claim before it enters the commons or is passed on | yes, except L21 own-failure correction (second procedure) |
| adopt | Read what peers built, check, adopt by own act, thank the origin | read others' work, bring into your work, thank the origin | yes; L43 pointer to tend is a second step (correct) |
| tend | Build, correct, merge, retire commons items, then carry them to peers | build, correct, merge, retire in the commons | yes; L13-L21 are standing stances, L17 contradicts L19/L21 (below) |
| aid | Offer a peer a fix, finding, or capacity, unasked, as an artifact with one message | offer a peer a fix, finding or capacity unasked | yes; L19 report-breakage is a fourth object |
| volunteer | Find society work in its state, pick one piece in order, do it by its skill | turn not-busy time into society work | yes, except L21 (route ideas) |
| heartbeat | Choose, set, record, restore, end a recurring wake | set and restore the recurring wake | yes |

## 5. Observations not counted as violations
- tend L17 `never fix it by your own rule` is contradicted by L19 `Copy knowledge that reaches beyond your project into the commons` and L21 `Keep every rule that binds your project in your project's records; never move one out`, which fix that split by rule.
- aid L17 sends help as `[answer]`; ontology L97 defines `[answer]` as the reply to an ask, and aid's help is unasked.
- Descriptions of volunteer L4 and heartbeat L4 carry `so that` (argument) but the rule governs instructions; left uncounted.
- self-audit.md read after this audit, first 120 lines only (adopt, aid, ask-around tables): it marks rows for terms, ordinary words, pairing, one-instruction and trigger-in-body PASS on adopt, which sections 1-2 contradict at adopt L13, L27, L33, L35, L39.

## 6. Verdicts
| skill | verdict |
|---|---|
| gossip | 9 violations |
| ask-around | 2 violations |
| spread-around | 2 violations |
| quote | 4 violations (+2 extra edges) |
| vouch | 2 violations (+1 extra edge) |
| adopt | 7 violations (+2 extra edges) |
| tend | 7 violations |
| aid | 1 violation (+1 extra edge) |
| volunteer | 3 violations |
| heartbeat | 9 violations (+6 extra edges) |

Total: 46 violations, none CONFORMS; 12 extra edges, 0 missing.

## Summary
No skill in group B conforms: 46 violations across ten skills, the most in gossip and heartbeat (nine each). One shared cause, the identical `read-the-terms` sentence in 24 skills, breaks the no-copied-content rule in every skill; the rest are compound sentences, mismatched prohibitions, undefined terms, and two near-copied clauses. Every roster edge is present, but 12 extra edges exist, led by heartbeat's six and quote's `vouch` and `memento:event-capture`.
