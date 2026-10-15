# Audit B, round 2 — gossip, ask-around, spread-around, quote, vouch, adopt, tend, aid, volunteer, heartbeat

Text audited: /Users/ryzhakar/pp/aoa-skills/peers/skills/<name>/SKILL.md at branch draft/10-skills, head 52cc0ac, from scratch. Rules: memento 0.5.1 skill-creation. One-part-name rule void. self-audit.md not read before writing. Counts are one per violating sentence-and-rule.

Mechanical results (all ten): `version` key count 0; directory = `name`; no body sentence with two of never/always/only/must outside backticks; every body sentence carries a `; never` half; no tag attribute, list, table, or code block in a tag; all tag names imperative verb phrases; no path references.

## 1. Matrix (P pass, Vn violations)

| # | rule | gos | ask | spr | quo | vou | ado | ten | aid | vol | hrt |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | one procedure, named | P | P | P | P | P | P | P | P | P | P |
| 2-5 | SKILL.md, frontmatter, dir=name, description shape | P | P | P | P | P | P | P | P | P | P |
| 6 | no trigger in body | P | P | P | P | P | P | P | P | P | P |
| 7-13 | XML, tag names, tag content, order, outside only by skill name | P | P | P | P | P | P | P | P | P | P |
| 14 | shared content not copied | P | P | P | P | P | P | P | P | P | P |
| 15 | skill by name, not path | P | P | P | P | P | P | P | P | P | P |
| 16 | one instruction per sentence | P | P | P | P | P | P | P | P | P | V1 |
| 17 | command | P | P | P | P | P | P | P | P | P | P |
| 18 | one emphatic word | P | P | P | P | P | P | P | P | P | P |
| 19 | pairing with the same instruction | P | P | P | P | P | P | P | P | P | P |
| 20-21 | no argument, no failure narration | P | P | P | P | P | P | P | P | P | P |
| 22 | one term per concept | P | P | P | P | P | P | P | P | P | V1 |
| 23 | terms defined or named for ontology | V1 | V1 | V1 | P | P | V1 | V1 | V1 | V1 | V1 |
| 24 | ordinary words | P | P | P | P | P | P | P | P | P | P |
| 25 | every sentence instructs or forbids | P | P | P | P | P | P | P | P | P | P |

## 2. Remaining violations

### gossip (1)
- R23 (term in use, not in the `take-the-terms` list at L9; ontology defines each): `[ask]` L15, `[notice]` L17, `message` and `type` L37 (`under a type of your own`), `state` L43 and L53 (`whose state lets it receive`, `before its state clears`), and the ontology sense of `held` L53 (`Hold a relay of a level 2 gossip`).

### ask-around (1)
- R23 L29 `a lost delivery to resend`: `delivery` is an ontology term (L95) absent from the L9 list.

### spread-around (1)
- R23 `message` L23 `one message per line`, L25 `a message already going to a peer`; `society` L31 `the society's public discourse`: ontology terms absent from the L9 list.

### quote (0) CONFORMS

### vouch (0) CONFORMS

### adopt (1)
- R23 `card` L13 `your card's \`commons_read\``, `peer` L33 `on the peer's word`: ontology terms absent from the L9 list.

### tend (1)
- R23 L23 `beside the intake`: `intake` is not defined as a term in ontology (L133 uses it only inside the `commons line` definition) and not in the skill.

### aid (1)
- R23 L15 `as a long message`: `message` is an ontology term absent from the L9 list (`peer`, `[notice]` only).

### volunteer (1)
- R23 L19 `a live peer's work`, `peers state in cards and messages`: `peer` and `message` are ontology terms absent from the L9 list.

### heartbeat (3)
- R16 L23 `load peers:tend, peers:ask-around, peers:spread-around, and peers:adopt, then use each on the commons.` load and use are two instructions in one sentence (inside backticks; the rule has no backtick exemption).
- R22 L23 `peers:tend`, `peers:ask-around`, `peers:spread-around`, `peers:adopt` vs L39 `by the skill \`volunteer\``: two forms for naming a skill inside one skill.
- R23 L43 `a departed member`: ontology defines `departed card` (L55) and `gone` member (L125), not a departed member; `member` is absent from the L9 list.

## 3. Round-1 findings, status

| skill | round-1 finding | status |
|---|---|---|
| all ten | R14 identical `read-the-terms` sentence (L9) | FIXED: each skill now carries its own term list (L9). The frame `Take ... as the skill \`ontology\` defines them; never take them in another sense.` is shared boilerplate across 24 skills; counted as a naming instruction, not shared content |
| gossip | R16 L15 two originations | FIXED: L15, L17 |
| gossip | R16 L31 count and move | FIXED: L33, L35 |
| gossip | R16 L43 two adds | FIXED: L47, L49 |
| gossip | R16 L51 relay and answer | FIXED: L57, L59 |
| gossip | R16 L55 correct and mark | FIXED: L63, L65 |
| gossip | R17 and R19 L41 | FIXED: L45 `within the origin's \`spread:\`; never narrow them` |
| gossip | R22 status vs state | FIXED: L43 uses `state` |
| ask-around | R19 L29 chase | FIXED: L29 `never read it as a lost delivery to resend` |
| spread-around | R23 `focus`, `knows` | FIXED: defined inline L17 |
| quote | R19 L17 | FIXED: L17 `never weigh it outside that check`, L19 claim pair |
| quote | R23 `journal` | FIXED: listed L9, ontology L71 |
| quote | R23 `memento` | FIXED: skill name removed (L25) |
| quote | extra edges vouch, memento:event-capture | FIXED: only `gossip` named (L37, L39) |
| vouch | R1 L21 own-failure correction; extra edge tell | FIXED: tag removed; no `tell` |
| adopt | R6 L13 trigger conditions | FIXED: moved to description L5 |
| adopt | R16 L27 | FIXED: L27, L29 |
| adopt | R19 L39 | FIXED: L41, L43 |
| adopt | R23 `memento`, `conventions`; R24 `ground` | FIXED: L35 `Write your reason`, L37 `standing rules` |
| adopt | extra edges tend, memento:record-writing | FIXED: none named |
| tend | R14 L49 near-copy of adopt L43 | FIXED: adopt no longer carries a correct step; tend L51 stands alone |
| tend | R16 L47 three instructions | FIXED: L45, L47, L49 |
| tend | R23 `areas`, `collective and personal wisdom`, `committed path` | FIXED: L15 plain wording, wisdom removed, L37 `a path committed to git` |
| tend | R24 `failed honestly` | FIXED: L51 `failed in your work` |
| tend | observation: L17 contradicted L19, L21 | FIXED: L15 leaves areas and tending to the society |
| aid | extra edge vouch | FIXED |
| aid | observation: `[answer]` for unasked help | FIXED: `[notice]` L15 and description |
| volunteer | R1 L21 route ideas | FIXED: moved to spread-around L31 |
| volunteer | R19 L25 | FIXED: L23 `never pick out of that order` |
| heartbeat | R14 L31 seven days | FIXED: L31 `as Claude Code does` |
| heartbeat | R14 L39 idling near-copy | FIXED: L39 `never spend it another way` |
| heartbeat | R14 L21 count comparison | FIXED: L21 prompt rewritten |
| heartbeat | R16 L21 | FIXED: single instruction |
| heartbeat | R16 L23 | NOT FIXED (two instructions remain, above) |
| heartbeat | R19 L21 | FIXED: L21 `never set a default wake with another prompt` |
| heartbeat | R22 default form vs default wake | FIXED: L17 `default wake`, `commons wake` |
| heartbeat | R22 `peers:x` vs `the skill x` | NOT FIXED: L21 lost its `peers:` names; L23 keeps four |
| heartbeat | extra edges card, receive, adopt (L21), tend, ask-around, spread-around | PARTLY FIXED: card and receive gone; four remain in L23 |

## 4. New violations introduced by the fixes
- R23 (all eight skills in section 2 except heartbeat's L43 item): the per-skill term list at L9 names some ontology terms the skill uses and omits others. The round-1 blanket sentence covered every term; the narrowed list leaves the omitted terms unnamed. Instances: gossip 1, ask-around 1, spread-around 1, adopt 1, aid 1, volunteer 1 (and tend `intake`, heartbeat `member`, which are partly older).
- No other new violations. Checked and clean: spread-around L31 (ideas moved in; description L4, L5 now covers it), quote L41 (subagent forwarding; description L5 covers it), vouch description after the tag removals, adopt description L4-L5 after condition move.

## 5. Cross-skill checks

Edges (roster vs text; each skill names `ontology`):

| skill | roster | found | missing | extra |
|---|---|---|---|---|
| gossip | ask-around, spread-around, tell | L13, L15, L17, L37, L53, L71 | none | none |
| ask-around | gossip, tell | L17, L21 | none | none |
| spread-around | gossip, vouch, tell | L13, L17, L29 | none | none |
| quote | gossip | L37, L39 | none | none |
| aid | tell | L15 | none | none |
| volunteer | ask-around, spread-around, adopt, tend, aid, heartbeat | L15, L27-L35 | none | none |
| heartbeat | volunteer | L39 | none | peers:tend, peers:ask-around, peers:spread-around, peers:adopt (L23, inside the commons prompt) |
| adopt | vouch, tell | L25, L41 | none | none |
| tend | vouch, spread-around | L25, L57 | none | none |
| vouch | leaf | none | none | none |

Missing edges 0; extra edges 4 (heartbeat only), down from 12.

Copies: greps across all 25 skill dirs find no sentence of the ten repeated in another skill. Frames only, not counted: the `take-the-terms` instruction (24 skills); `Append each ... with its own \`printf\`` at tend L35 and tell L71 (different object).

protocol-change: no group-B skill names protocol-change, propose, or consent; protocol-change names neither propose nor consent as skills (its L25 `proposer` is a role word); propose and consent each name protocol-change once.

## 6. Content check (inferred procedure vs roster)
- gossip: wrap a message in the four-line envelope and relay it once by `spread:` and `has:` until the origin is reached. Matches roster; no second procedure.
- ask-around: seek by gossip `[ask]` after own effort and a direct ask. Matches.
- spread-around: offer findings, commons lines, and ideas to the peers and discourse they serve, after vouching. Matches roster "gossip applied to offering" plus the idea-routing sentence L31 the description now names; counted as one offering procedure, not flagged.
- quote: check, record, and relay an owner ruling by scope. Matches; L13 restates the owner's absence from ontology L63 as a command, not a copied sentence.
- vouch: check a claim against the thing itself. Matches the roster row; the route-a-failed-check step is gone.
- adopt: read, check, adopt by own act, thank the origin, record the reason. Matches.
- tend: build, correct, merge, retire commons items, then carry them to peers. Matches; L43 and L51 overlap (L51 is a case of L43), no rule broken.
- aid: offer a fix, finding, or capacity unasked as an artifact with one notice; L17 reporting breakage stays within it.
- volunteer: find society work, pick one piece in order, do it by its skill. Matches.
- heartbeat: choose, set, record, restore, spend, end a wake. Matches.

## 7. Verdicts and counts
| skill | verdict |
|---|---|
| gossip | 1 violation |
| ask-around | 1 violation |
| spread-around | 1 violation |
| quote | CONFORMS |
| vouch | CONFORMS |
| adopt | 1 violation |
| tend | 1 violation |
| aid | 1 violation |
| volunteer | 1 violation |
| heartbeat | 3 violations (+4 extra edges) |

Total 10 violations (round 1: 46). Two skills conform.

## Summary
Round 2 fixed 36 of the 39 distinct round-1 findings; quote and vouch now conform, and the missing-or-extra edge count fell from 12 to 4. Two round-1 heartbeat findings remain (L23 packs load and use into one sentence; L23's `peers:` names vs L39's `the skill` form), plus its four extra edges inside that prompt. The fix that narrowed each `take-the-terms` list to per-skill terms introduced the only new finding class: eight skills still use ontology terms the list does not name (and tend's `intake` is defined nowhere). Counts: gossip 1, ask-around 1, spread-around 1, quote 0, vouch 0, adopt 1, tend 1, aid 1, volunteer 1, heartbeat 3.
