# Audit C, round 3: steward, reserve, settle, sweep, scribe, propose, consent, protocol-change

Auditor: audit-C. Text: `/Users/ryzhakar/pp/aoa-skills/peers/skills/<name>/SKILL.md`, branch draft/10-skills, head abf83b9. Rules: skill-creation 0.5.1; one-part-name rule void. Standards as before (pairing = prohibition names the same act; terms = ontology definition or defined in the first sentence). Checked on all eight: frontmatter has only `name` and `description`; directory = name; every body line is inside a tag; tag names are imperative; no attributes; no path to another skill; one `never` per sentence, no only/must/always (grep: zero hits); every term in each `<take-the-terms>` line has an ontology definition (script against ontology, no miss).

## Per-skill result

| skill | violations | remaining |
|---|---|---|
| steward | 0 | none |
| reserve | 0 | none |
| settle | 0 | none |
| sweep | 0 | none |
| scribe | 3 | L13, L53, L55 |
| propose | 0 | none |
| consent | 0 | none |
| protocol-change | 0 | none |

### scribe (3), all NEW to this audit's terms-sentence check (the words existed in round 2; round 3 made the opening list the test, and the list is short of three body terms)
- L13 "Take up the stewardship `protocol` once the scribe departs": the body says `departs`; the ontology term is `gone` (ontology L133), absent from L9's list. Second term for a defined concept, and unlisted.
- L53 "Leave as the scribe with one `[notice] leaving` to every live peer": this is the ontology's `leave notice` (L129); L9 does not list it.
- L55 "Follow the last shipped version while the stewardship `protocol` stands open": "stands open" is the ontology's `open stewardship` (L179 in round 2 numbering); L9 does not list it (also L57 "while the stewardship `protocol` stands open").

## Round-2 findings

| round-2 finding | status |
|---|---|
| scribe L29 "Circulate each round" | fixed: L29 "Circulate each draft as one `[ask] protocol draft: <path>`" |
| scribe L31 near-copy frame | fixed: L31 "Close each round by the reply time and answer rules of the skill `protocol-change`; never close one by rules of your own." |
| propose L25 near-copy | fixed: L25 "Expect your request's outcome when its round closes by the skill `protocol-change`; never expect it sooner." |
| consent L15 near-copy | fixed: L15 "Time your answer to the round's reply time by the skill `protocol-change`; never answer after it." |
| protocol-change L29 `bind` | fixed: "Hold a silent member bound to an enacted change ...; never hold it bound earlier." (`bound` listed, ontology L225) |

## Round-3 changes checked

- Party frame: scribe L31 (close), propose L25 (expect), consent L15 (time) are each a command with its own same-act prohibition, each worded by party; no two share a frame. PASS.
- Not counted, note: propose L25 commands an expectation, not an act, and overlaps L23 "Hold a request open until the scribe reports its outcome; never close it on silence." Both sentences are well-formed commands.
- settle L21, L29 "Divide", "standing apart": one sense per word; PASS. protocol-change L25 "Enact ... never enact one on silence": PASS with ontology `enacted`.
- `departed` in scribe L13 vs reserve L33 "holder's card is departed": reserve uses ontology `departed card`; PASS.

## Opening terms sentence lists every ontology term the body uses

| skill | complete? | gap |
|---|---|---|
| steward | yes | none |
| reserve | yes | none |
| settle | yes | none |
| sweep | yes | none |
| scribe | NO | `gone` (L13), `leave notice` (L53), `open stewardship` (L55, L57) |
| propose | yes | none |
| consent | yes | none |
| protocol-change | yes | none |

## Cross-skill

| skill | roster edges | found at | missing | extra |
|---|---|---|---|---|
| steward | reserve, settle, scribe | L39, L37, L41 | none | none |
| reserve | tell | L21 | none | none |
| settle | tell, steward | L15, L33 | none | none |
| sweep | card | L25 | none | none |
| scribe | propose, protocol-change | L33, L31 | none | card (L41) |
| propose | protocol-change | L25 | none | none |
| consent | protocol-change | L15 | none | none |
| protocol-change | none | none | none | none |

protocol-change names neither propose nor consent; propose and consent each name protocol-change. No near-copied sentence across the eight (grep of "by the skill `protocol-change`" lines: three distinct sentences).

## Content check

Each skill's inferred procedure matches its roster row, unchanged from round 2: steward looks after a shared thing; reserve holds a resource by a board line; settle takes a dispute to a go-between; sweep moves a gone member's card; scribe takes, keeps, circulates, ships, and hands on the protocol stewardship; propose sends the scribe a defect or change and holds it open; consent checks and answers a draft; protocol-change times, weighs, closes, and applies a round.

## Verdicts

steward CONFORMS (0); reserve CONFORMS (0); settle CONFORMS (0); sweep CONFORMS (0); scribe 3; propose CONFORMS (0); consent CONFORMS (0); protocol-change CONFORMS (0). Total 3 (round 2: 5).

Summary: All five round-2 findings are fixed, and the party-worded round frame (scribe L31, propose L25, consent L15) gives three distinct commands with no near-copy. Seven of eight skills conform; scribe has 3 violations, all because L9's terms sentence omits `gone` (body says "departs", L13), `leave notice` (L53), and `open stewardship` (L55, L57). Per-skill counts: steward 0, reserve 0, settle 0, sweep 0, scribe 3, propose 0, consent 0, protocol-change 0.
