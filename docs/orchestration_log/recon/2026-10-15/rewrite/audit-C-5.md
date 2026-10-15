# Audit C, round 5: steward, reserve, settle, sweep, scribe, propose, consent, protocol-change

Auditor: audit-C. Text: `/Users/ryzhakar/pp/aoa-skills/peers/skills/<name>/SKILL.md`, branch draft/10-skills, head 68d60b2. Rules: skill-creation 0.5.1; one-part-name rule void; scribe -> card edge and the heartbeat wake prompt not counted (ruling). Checked on all eight: frontmatter only `name`, `description`; directory = name; every body line inside a tag; imperative tag names (`check-before-reserving`, `reserve-by-a-line`, `note-the-outcome`, `take-the-terms` ...); no attributes; no path to another skill; one `never` per sentence, no only/must/always (grep zero); every listed term has an ontology definition; descriptions read for ontology words in other senses.

## Per-skill result

| skill | violations | remaining |
|---|---|---|
| steward | 0 | none |
| reserve | 3 | L5, L19, L21 |
| settle | 1 | L15 |
| sweep | 1 | L25 |
| scribe | 0 | none |
| propose | 1 | L25 |
| consent | 1 | L15 |
| protocol-change | 0 | none |

### reserve (3)
- L5 "or a board line whose holder departed": `departed` is the ontology's word for a card moved into `<root>/departed/` ("Call a departed card a card moved into `<root>/departed/`"); here it describes a member, whose ontology term is `gone`. Also `holder` is a second word for the body's "member" (L21, L27, L31, L33). NEW (the description kept the word the body dropped).
- L19 "Reserve an exclusive resource by its own line on the board, ...; never use one off the board." The prohibition names using, not reserving: another act than the one commanded. NEW from round 5's rewording (round 4 read "never hold one off the board").
- L21 "Ask the member a line names for its resource by the skill `tell`": the body uses "the skill", an ontology term (`skill`: "a text a harness loads for a model to read and follow, one procedure each"), absent from reserve L9. NEW: `skill` entered the ontology in round 5.

### settle (1)
- L15 "Ask a go-between to mediate a contested matter, by the skill `tell`": `skill` used (also L33 "by the skill `steward`") and absent from L9. NEW.

### sweep (1)
- L25 "Leave the moved card's lines as its member last kept them by the skill `card`": `skill` used and absent from L9. NEW.

### propose (1)
- L25 "Expect your request's outcome when its round closes by the skill `protocol-change`": `skill` used and absent from L9. NEW.

### consent (1)
- L15 "Time your answer to the round's reply time by the skill `protocol-change`": `skill` used and absent from L9. NEW.

steward L9, scribe L9, protocol-change L9 list `skill`; the five above do not.

## Round-4 findings

| round-4 finding | status |
|---|---|
| steward L9 `held` wrong sense | fixed: `held` removed; body now "keep" (L13, L19), "your own branch" (L29), "Reserve an exclusive resource" (L39) |
| reserve L9 `held` wrong sense | fixed: `held` removed; body now "reserve" and "tests in use" (L31, L33) |

## Sense spot-check, every listed term (definition quoted in short; body uses by line)

Wrong-sense uses found: `departed` for a member (reserve L5, counted above). All else in sense; ordinary verbs checked in all eight bodies and descriptions: hold, claim, act, state, record, relay, scope, body, line, board, answer, check, bring, keep, name, run, sent, turn, round: none carries an ontology sense other than its own, apart from the one finding.

| term | ontology sense | body uses |
|---|---|---|
| session | "one conversation a harness runs" | steward L25; protocol-change L27 "a project whose sessions still object" |
| skill | "a text a harness loads for a model to read and follow" | steward L37, L39, L41; scribe L31, L33, L41; protocol-change L35 "the skill text you loaded" |
| member | "a project's ongoing principal in one role" | steward L29 "another member's branch"; reserve L21, L27; sweep L13 |
| protocol | "the society's shared rules" | scribe L19, L23, L55; propose L13; protocol-change L41 "your card's `protocol`" |
| card | "the file `<root>/members/<member>.md`" | steward L13; sweep L21, L25; reserve L31 |
| [hazard] | "what can corrupt or kill a peer's work now" | steward L27, L31 |
| [notice] | "useful to its receiver that needs nothing back" | steward L15, L33; sweep L27; scribe L47, L59 |
| exclusive resource | "exists once and cannot be forked" | steward L39; reserve L13, L19; settle L25 |
| stewardship | "a shared thing ... named in its card's `stewards`" | steward L13, L15, L37; scribe L13, L15 |
| steward | "the member keeping a stewardship" | steward description L5 "a steward's"; scribe description L4 |
| open stewardship | "no live member's card names, left by a gone member" | steward L21; scribe L55, L57 |
| go-between | "a third live peer that mediates a contested matter" | steward L37; settle L15, L17 |
| stamp | "a minute in the form `2026-10-14T09:30+0300`" | reserve L23 "the earlier `sent` stamp"; propose L19 |
| root | "the directory `${AGENTS_OF_ANARCHY_ROOT:-...}`" | reserve L13, L31, L33; sweep L21 |
| member id | `<project_name>/<role>` | reserve L19 `<member id>` |
| departed card | "a card moved into `<root>/departed/`" | reserve L33 (two uses); sweep L21 |
| resource board | "`<root>/resources.md` ... one line per reserved exclusive resource" | reserve L13, L19, L27 |
| owner | "the person every session works for" | settle L13, L25, L27; scribe L49 |
| bringing a matter to the owner | "writing it into your own records and into your next answer to the owner's word" | settle L25, L27; scribe L49 |
| brought matter | "reversible choice goes ahead, irreversible waits" | settle L29 "a brought dispute ... while it waits" |
| [ask] | "a need its sender awaits an answer to" | scribe L29; propose L17; consent description |
| peer | "any live member with a card in the root" | settle L13; scribe L23; protocol-change L25 |
| harness | "a program that runs model conversations" | sweep L17; protocol-change L35 |
| address | `<harness>://<host>/<harness-ref>` | sweep L13, L21 |
| presence | "the harness function listing every session it can see" | sweep L13, L17, L21 |
| [answer] | "the reply to an `[ask]`" | consent L23, L25; protocol-change L19, L21 |
| leave notice | "a message opening `[notice] leaving`" | sweep L21; scribe L53; protocol-change L21 |
| live | "presence lists its card's address, no leave notice, not dormant ..." | sweep L27; scribe L13, L29, L47 |
| gone | "once it sends a leave notice, or once presence drops its address" | sweep L13; scribe L13 |
| turn | "one stretch in which a session works" | scribe L27 |
| hook, plugin | "a script the harness runs at a fixed event"; "a package of skills and hooks" | scribe L19, L39, L43 |
| society | "the members sharing one root" | scribe description L4 |
| checkout | "the absolute path of the worktree a member works in" | scribe L57; propose L19 |
| reply time | "the time its second line names for an answer" | scribe L31; consent L13, L15; protocol-change L13, L25 (L15 and L13 attach it to a round and a draft; not counted) |
| scribe | "the member whose card's `stewards` lists `protocol`" | scribe L13, L31; propose L13, L17, L23 |
| pointer, change line | "`<root>/PROTOCOL.md`"; "the pointer's dated line" | scribe L21, L45, L47; protocol-change L29, L35, L37 |
| draft, protocol change | "written wording of a protocol change"; "any change to the peers plugin's skills or hook text" | scribe L29, L33; consent L13, L19; propose L4, L17; protocol-change L13, L25 |
| round | "the span from a draft's circulation to its outcome" | scribe L27, L31; propose L25; consent L15 |
| enacted | "once its round closes with the society's consent" | scribe L37, L39; protocol-change L25, L29 |
| separating | "a project's sessions keeping their loaded protocol version while the society enacts a change they object to" | scribe L37, L45; protocol-change L31, L39 |
| bound | "bound to an enacted change once that change applies to it" | protocol-change L29 "Treat a silent member as bound" |
| shipping | "editing the peers plugin and the pointer to carry an enacted change" | scribe L39, L43, L55; protocol-change L35 |
| reloaded | "your loaded skill text ... reloaded once the owner runs `/reload-plugins`" | protocol-change L35 |
| journal, type | "the dated event log a member's records keep"; "the bracketed word opening its first line" | propose L19; propose L17 |

## Cross-skill and content

Edges present: steward -> reserve L39, settle L37, scribe L41; reserve -> tell L21; settle -> tell L15, steward L33; sweep -> card L25; scribe -> propose L33, protocol-change L31 (card L41 accepted); propose -> protocol-change L25; consent -> protocol-change L15. No extra edge, no missing edge. protocol-change names neither propose nor consent; propose and consent each name protocol-change. No near-copied sentence. Procedures match the roster rows. Note, not counted: propose L25 commands an expectation.

## Verdicts

steward CONFORMS (0); reserve 3; settle 1; sweep 1; scribe CONFORMS (0); propose 1; consent 1; protocol-change CONFORMS (0). Total 7 (round 4: 2).

Summary: Both round-4 findings are fixed, and steward, scribe, and protocol-change conform. Seven violations remain, five of them one cause: round 5 added `skill` to the ontology and reserve, settle, sweep, propose, and consent use "the skill" in their bodies without listing it, while reserve also carries `departed` said of a member (L5) and a prohibition naming another act (L19). Per-skill counts: steward 0, reserve 3, settle 1, sweep 1, scribe 0, propose 1, consent 1, protocol-change 0.
