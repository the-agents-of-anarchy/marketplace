# Audit C, round 2: steward, reserve, settle, sweep, scribe, propose, consent, protocol-change

Auditor: audit-C. Text: `/Users/ryzhakar/pp/aoa-skills/peers/skills/<name>/SKILL.md` at branch draft/10-skills, head 52cc0ac. Rules: skill-creation 0.5.1; one-part-name rule void. Same standards as round 1 (pairing = prohibition names the same act; terms = ontology definition, or defined in the first sentence). Checked on all eight: frontmatter has only `name` and `description`; directory = name; every body line sits inside a tag; tag names are imperative (`take-the-terms` etc.); no attributes; no path to another skill; no sentence carries two emphatic words (grep only/must/always: zero hits); every term listed in each `<take-the-terms>` has an ontology definition (checked by script against ontology lines 13-237, including `reply time` L113, `gone` L125, `live` L123, `address` L21, `open stewardship` L179, `round` L209, `draft` L207, `separating` L211, `shipping` L213, `journal` L71, `turn` L23, `checkout` L59). Skill-name edges follow the roster.

## Per-skill result

| skill | violations | remaining |
|---|---|---|
| steward | 0 | none |
| reserve | 0 | none |
| settle | 0 | none (L15 note below) |
| sweep | 0 | none |
| scribe | 2 | L29, L31 |
| propose | 1 | L25 |
| consent | 1 | L15 |
| protocol-change | 1 | L29 |

### scribe (2)
- Ontology sense, one term per concept: L29 "Circulate each round as one `[ask] protocol draft: <path>`" (ontology L209: a round is the span from a draft's circulation to its outcome; a span cannot be circulated; the draft is circulated). NEW: introduced by the fix that moved circulation here.
- Near-copy across skills: L31 "Run each round by the skill `protocol-change`; never run one another way." (same frame as consent L15 and propose L25; see cross-skill). NEW form of round-1 finding.

### propose (1)
- Near-copy: L25 "Follow your request's round by the skill `protocol-change`; never follow it another way." (consent L15 "Follow the round by the skill `protocol-change`; never follow it another way." differs only by "your request's"). NEW form of round-1 finding.

### consent (1)
- Near-copy: L15 "Follow the round by the skill `protocol-change`; never follow it another way." (see propose L25).

### protocol-change (1)
- Term: L29 "Bind a silent member to an adopted change from its next read of the pointer; never bind it earlier." (`bind` carries a narrow sense, being held to a change; not in `<take-the-terms>` and not defined in the sentence). Carried from round 1; not new.

Note, not counted: settle L15 "Ask a go-between to mediate a contested matter, by the skill `tell`; never mediate a matter you are party to." prohibits an adjacent act (mediating), not asking; judged same concern, as with sweep L15. protocol-change L25 and scribe L37 use `adopt` for a society's act, while ontology's adoption (a peer taking a peer's work into its own) is another sense; not counted.

## Round-1 findings: fixed or not

| id | finding | status |
|---|---|---|
| steward L37 | pairing (settling criterion) | fixed: "never decide the question alone" |
| steward L21 | `departed or gone` | fixed: "an open stewardship you can serve" |
| steward L29 | `that branch's owner` | fixed: "a branch you hold" |
| steward L21 | `open stewardship` undefined | fixed: in `<take-the-terms>`, ontology L179 |
| steward L25 | `canonical copy` | fixed: defined in the sentence |
| steward L31 | `force-moving` | fixed: "rewriting its history" |
| reserve L23 | copy of settle L23 | fixed: settle no longer carries the rule |
| settle L15 | pairing | fixed (split into L15, L17) |
| settle L23 | two instructions; pairing; copy | fixed (L25, L29 split; copy gone) |
| settle L25 | two instructions | fixed (L27, L29) |
| sweep L13 | two instructions | fixed (L13, L15) |
| sweep L15 | `sweep`/`move` | fixed: "Move a card" L17 |
| sweep L19 | pairing (delete) | fixed: "never move one before either" L21; delete moved to L23 |
| scribe L17 | role vs stewardship | fixed (L15, L55-57 use the stewardship) |
| scribe L15 | copy of settle L25 | fixed: removed |
| scribe L25 | two verbs | fixed: "Write into the protocol text what the peers consented to" |
| scribe L31 | copy of propose L29 | NOT fixed: re-worded, copy cluster remains |
| scribe L31/L35/L34/L41 | `round`, `adopted/deferred/separated`, `ship`, semver | fixed (ontology; "its last number", "its middle number") |
| scribe L35 | pairing | fixed: "never leave an outcome unreported" |
| scribe L55 | `own tree` | fixed: `checkout` |
| propose L4 | two procedures | fixed: circulation moved to scribe L26-34 |
| propose L19 | two instructions | fixed (L19, L21) |
| propose L19 | `own tree`, `journal` | fixed |
| propose L25 | `turn over its whole context` | fixed: removed |
| propose L29 | copy of scribe L31 | NOT fixed (see above) |
| consent L13, L15 | `heavy work`, `round` | fixed (defined in sentence; ontology) |
| consent L19 | pairing (motive) | fixed: "never accept an unchecked draft" |
| consent L23 | two answers | fixed (L23, L25) |
| protocol-change L42-46 | second procedure (culture) | fixed: removed |
| protocol-change L43 | copy of ontology L85 | fixed: removed (ontology L215 holds it) |
| protocol-change L12, L17 | `round`, `defer/separate` | fixed (ontology `round`, `separating`) |
| protocol-change L29 | `bind`; pairing; two acts | pairing and split fixed (L29, L31); `bind` NOT fixed |

## Cross-skill checks

| skill | roster edges | found at | missing | extra |
|---|---|---|---|---|
| steward | reserve, settle, scribe | L39, L37, L41 | none | none |
| reserve | tell | L21 | none | none |
| settle | tell, steward | L15, L33 | none | none |
| sweep | card | L25 | none | none (tell removed) |
| scribe | propose, protocol-change | L33, L31 | none | card (L41) |
| propose | protocol-change | L25 | none | none |
| consent | protocol-change | L15 | none | none |
| protocol-change | none | none | none | none |

protocol-change names neither propose nor consent: PASS. propose and consent each name protocol-change: PASS. Each skill takes ontology terms at L9 via `<take-the-terms>`.

Near-copies (grep across the skills directory): consent L15 / propose L25 / scribe L31 share the frame "<verb> the round by the skill `protocol-change`; never <verb> it another way". Cleared: "earlier `sent` stamp" (reserve L23 only), "both sides ask" (settle L27 only), "never as rules" (gone from protocol-change), "own tree" (gone from these eight).

## Content check

| skill | inferred procedure | roster row | match |
|---|---|---|---|
| steward | Claim, hold, release, and guard a shared thing on your card and branch; hand questions, resources, the protocol to other skills. | look after a shared thing | yes |
| reserve | Hold an exclusive resource by a board line and keep the board true. | claim an exclusive resource | yes |
| settle | Take a dispute to a go-between, separate if it fails, bring the owner the rest, record the outcome. | take a dispute to a go-between | yes |
| sweep | Move a gone member's card to departed after checking it answers nowhere. | move a gone member's card | yes |
| scribe | Take, keep, circulate, ship, and hand on the protocol stewardship. | hold the role; ship by consent; hand on | yes |
| propose | Send the scribe a defect or change as a file and hold the request open through its round. | author's part of a round | yes |
| consent | Check a protocol draft and answer accept or object. | each receiver's part | yes |
| protocol-change | Time the round, weigh answers, close it, apply a shipped change. | shared context of a round | yes |

## Verdicts

steward CONFORMS (0); reserve CONFORMS (0); settle CONFORMS (0); sweep CONFORMS (0); scribe 2; propose 1; consent 1; protocol-change 1. Total 5 (round 1: 42).

Summary: Thirty-seven of the 42 round-1 findings are fixed; steward, reserve, settle, and sweep now conform. Five violations remain: the "by the skill `protocol-change`; never ... another way" frame repeats in scribe L31, propose L25, and consent L15; scribe L29 circulates a "round" where ontology says a draft is circulated; protocol-change L29 uses `bind` undefined. Per-skill counts: steward 0, reserve 0, settle 0, sweep 0, scribe 2, propose 1, consent 1, protocol-change 1.
