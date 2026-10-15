# Audit B, round 3 — gossip, ask-around, spread-around, quote, vouch, adopt, tend, aid, volunteer, heartbeat

Text: /Users/ryzhakar/pp/aoa-skills/peers/skills/<name>/SKILL.md, branch draft/10-skills, head abf83b9, audited from scratch against memento 0.5.1 skill-creation and the current ontology. One-part-name rule void. self-audit.md not read. Counts are one per violating sentence-and-rule.

Mechanical results (all ten): no `version` key; directory = `name`; no body sentence with two of never/always/only/must outside backticks; every body sentence has a `; never` half; tags imperative, no attribute, prose and backticks only; no path references; protocol-change names neither propose nor consent (its L25 uses the verb `Enact`), and propose and consent each name protocol-change once.

## 1. Matrix (P pass, Vn violations)

| # | rule | gos | ask | spr | quo | vou | ado | ten | aid | vol | hrt |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | one procedure, named | P | P | P | P | P | P | P | P | P | P |
| 2-6 | file, frontmatter, dir, description, no trigger in body | P | P | P | P | P | P | P | P | P | P |
| 7-13 | XML, tag names, tag content, order, outside by skill name | P | P | P | P | P | P | P | P | P | P |
| 14 | shared content not copied | P | P | P | P | P | P | P | P | P | P |
| 15-21 | path, one instruction, command, emphatic, pairing, argument, narration | P | P | P | P | P | P | P | P | P | P |
| 22 | one term per concept | P | P | P | P | V1 | P | P | P | V1 | P |
| 23 | terms named or defined | P | P | V1 | P | P | P | P | P | V1 | P |
| 24-25 | ordinary words, every sentence instructs or forbids | P | P | P | P | P | P | P | P | P | P |

## 2. Remaining violations

### gossip (0) CONFORMS
### ask-around (0) CONFORMS
### quote (0) CONFORMS
### adopt (0) CONFORMS
### tend (0) CONFORMS
### aid (0) CONFORMS
### heartbeat (0) CONFORMS as to the rules; 4 extra graph edges (section 5)

### spread-around (1)
- R23 L21 `as a \`[notice] commons: <#n list>\``: the placeholder is the ontology's `#<n>` (commons-line number, ontology L145), which the L9 list omits.

### vouch (1)
- R22 description L5 `a claim about shared state or a session` vs body L15 `a claim about shared files or resources or a session` and ontology L181 `shared files or resources`: two phrasings for one concept, and `state` is an ontology term (a member's state, L99) in another sense.

### volunteer (2)
- R23 L13 `never let such a stretch drop to idling`: `idling` is `idle` (ontology L91), absent from the L9 list.
- R22 description L4 `find work in the society's state` vs body L19 `Find volunteer work in what the society already holds`: two phrasings for one concept; the description keeps `state`, which L9 lists in its ontology sense (a card's `state`).

## 3. Round-2 findings, status

| skill | round-2 finding | status |
|---|---|---|
| gossip | R23 unlisted `[ask]`, `[notice]`, `message`, `type`, `state`, `held` | FIXED: all in L9 list |
| ask-around | R23 `delivery` L29 | FIXED: listed L9 (also `[answer]`) |
| spread-around | R23 `message`, `society` | FIXED: both listed L9 |
| adopt | R23 `card`, `peer` | FIXED: listed L9 |
| tend | R23 `intake` | FIXED: listed L9; ontology L141 now defines the intake |
| aid | R23 `message` | FIXED: listed L9 |
| volunteer | R23 `peer`, `message` | FIXED: listed L9 |
| heartbeat | R16 L23 load and use | FIXED: `work on the commons by the skills tend, ask-around, spread-around, and adopt.` |
| heartbeat | R22 `peers:x` vs `the skill x` | FIXED: L23 now `the skills tend, ...`, no `peers:` form |
| heartbeat | R23 `a departed member` | FIXED: L43 `after you leave` |
| heartbeat | extra edges tend, ask-around, spread-around, adopt (L23) | NOT FIXED: still named in the L23 prompt |
| quote, vouch | (0 in round 2) | stay conforming on rules, except vouch description (new, below) |

## 4. New violations from round 3's changes
- vouch R22 (L5 vs L15): the ontology claim definition changed to `shared files or resources` (L181) and vouch L15 followed; the description kept `shared state`.
- volunteer R22 (L4 vs L19): body L19 changed to `what the society already holds`; the description kept `the society's state`.
- spread-around R23 (L21 `<#n list>`) and volunteer R23 (L13 `idling`): not new text, but they escape the new term guard (section 6).
- No other new violations. Checked: gossip L67 `current facts` (fixed `state` use), spread-around L19 reword, heartbeat L43 reword, tend and adopt term lists complete.

## 5. Edges (roster vs text; each skill names `ontology`)
| skill | roster | found | missing | extra |
|---|---|---|---|---|
| gossip | ask-around, spread-around, tell | L13, L15, L17, L37, L53, L71 | none | none |
| ask-around | gossip, tell | L17, L21 | none | none |
| spread-around | gossip, vouch, tell | L13, L17, L29 | none | none |
| quote | gossip | L37, L39 | none | none |
| aid | tell | L15 | none | none |
| volunteer | ask-around, spread-around, adopt, tend, aid, heartbeat | L15, L27-L35 | none | none |
| heartbeat | volunteer | L39 | none | tend, ask-around, spread-around, adopt (L23) |
| adopt | vouch, tell | L25, L41 | none | none |
| tend | vouch, spread-around | L25, L57 | none | none |
| vouch | leaf | none | none | none |

Missing 0; extra 4 (heartbeat L23). Copies: no sentence of the ten is repeated in another skill; the `take-the-terms` frame is shared boilerplate with per-skill term lists.

## 6. Extra check: does each opening terms sentence list every ontology term its body uses?

I read every body sentence against the ontology (not against the test). Terms used and not listed:
| skill | omitted ontology term | where |
|---|---|---|
| spread-around | `#<n>` | L21 `<#n list>` |
| volunteer | `idle` | L13 `idling` |
| all others (gossip, ask-around, quote, vouch, adopt, tend, aid, heartbeat) | none | complete |

Listed but not used in the body (harmless over-listing, not counted): gossip `priority level`; ask-around none; quote, vouch, adopt, aid list `act` and `delivery` where the body uses the verbs `act on` and `Deliver`.

peers/tests/test_terms.py: pytest is not installed here, so I ran its `used_terms` and `listed_terms` functions directly over the ten skills: it passes (0 failures). It is a one-way guard (terms used must be listed). Cases it misses, each shown by the two omissions above or by pattern reading:
1. Derived forms: `idle` is matched by `\bidle\b` only, so `idling` (volunteer L13) passes unlisted.
2. Placeholders: `#<n>` is matched literally, so `<#n list>` (spread-around L21) passes unlisted.
3. `state` is matched only after `receiver's|peer's|member's|its|that|whose`, or as `` `state` ``; it misses `the state`, `shared state`, `a state`, `society's state`.
4. `held` is matched only by four fixed phrases; any other `Hold ...` or `hold it` is invisible.
5. `body` is matched only as `member's body`/`your body`; gossip's message-body use is invisible, and ontology gives `body` only the member sense (L45) while gossip and the envelope definition (L161) use it for a message.
6. The scan reads the body only; descriptions are never checked (vouch L5, volunteer L4 above).
7. It does not check the sense: a listed term used in an ordinary sense (`act on`, `Deliver`, `Turn every stretch`) passes, and a skill may list a term it never uses.
8. It strips `the skill \`x\`` and one `the skills a, b, and c` pattern; a skill named another way (for example `peers:x`) would trigger term matches, and a new skill-list shape would not be stripped.

## 7. Content check
Each skill covers the procedure its roster row names and no second: gossip (envelope and relay), ask-around (seek by gossip), spread-around (offer, including commons lines and ideas, one offering procedure), quote (check, record, relay a ruling), vouch (check a claim), adopt (read, check, adopt, thank, record why), tend (build, correct, merge, retire, carry), aid (offer unasked), volunteer (find, pick, do), heartbeat (choose, set, record, restore, spend, end a wake).

## 8. Verdicts and counts
| skill | verdict |
|---|---|
| gossip | CONFORMS |
| ask-around | CONFORMS |
| spread-around | 1 violation |
| quote | CONFORMS |
| vouch | 1 violation |
| adopt | CONFORMS |
| tend | CONFORMS |
| aid | CONFORMS |
| volunteer | 2 violations |
| heartbeat | CONFORMS (+4 extra edges) |

Total 4 violations (round 2: 10; round 1: 46); seven skills conform.

## Summary
Round 3 fixed every round-2 term finding and heartbeat's sentence and form findings, leaving seven skills conforming and four violations in three skills (spread-around 1, vouch 1, volunteer 2); the only unfixed round-2 item is heartbeat's four extra edges in its L23 prompt. The new violations are two description-versus-body mismatches (vouch `shared state`, volunteer `the society's state`) caused by body rewrites that left the description behind, plus two unlisted ontology terms (`#<n>` at spread-around L21, `idle` as `idling` at volunteer L13). `test_terms.py` passes but misses exactly those two terms, along with other derived forms, any description, and the sense of a term. Counts: gossip 0, ask-around 0, spread-around 1, quote 0, vouch 1, adopt 0, tend 0, aid 0, volunteer 2, heartbeat 0.
