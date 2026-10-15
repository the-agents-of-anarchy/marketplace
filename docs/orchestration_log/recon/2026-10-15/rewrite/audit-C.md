# Audit C: steward, reserve, settle, sweep, scribe, propose, consent, protocol-change

Auditor: audit-C. Rules: skill-creation 0.5.1. Files: `/Users/ryzhakar/pp/aoa-skills/peers/skills/<name>/SKILL.md`. Line numbers are file lines. Standard for pairing: the prohibition must name the same act the instruction commands, not a neighbouring concern. Standard for terms: ontology's definitions count; anything else non-ordinary must be defined in its first sentence. Checked on every file: frontmatter carries only `name` and `description` (no version); directory = `name`; file is `SKILL.md`; no attribute on any tag; no instruction outside a tag; tag names are imperative; no path to another skill; no sentence carries two emphatic words (grep for only/must/always: zero hits; one `never` per sentence); no argument or failure narration found. Rows below list only what differs.

## steward (6 violations)

| rule | result |
|---|---|
| one procedure; description one sentence + phrases; no trigger in body | PASS |
| tags, order, pointers by skill name (reserve L39, settle L37, scribe L41, ontology L9) | PASS |
| one instruction per sentence; command; emphatic cap | PASS |
| pairing | VIOLATION L37 "Take a questioned stewardship to a go-between by the skill `settle`; never settle it by who claimed first." (prohibition names another concern: the settling criterion, not the taking-to) |
| one term per concept | VIOLATION L21 "a departed or gone member" (ontology term is `gone`; `departed` names a directory, ontology L35) ; VIOLATION L29 "that branch's owner" (`owner` is the ontology's human, ontology L59) |
| terms defined | VIOLATION L21 "an open stewardship" (undefined; ontology lacks it); VIOLATION L25 "canonical copy" (undefined, non-ordinary; first use L25; also L31 "force-moving a shared branch" undefined) |
| other rows | PASS |

Verdict: 6 violations (L37; L21 `departed or gone`; L29; L21 `open stewardship`; L25 `canonical copy`; L31 `force-moving`).

## reserve (1 violation)

| rule | result |
|---|---|
| shared content not copied | VIOLATION L23 "Let the claim with the earlier `sent` stamp hold an exclusive resource while its mediation runs; never seize it meanwhile." (same rule as settle L23 "the claim with the earlier `sent` stamp holding it meanwhile") |
| all other rows (L13, L15, L19, L21, L27, L29, L31 pairings, terms via ontology, tell by name L21) | PASS |

Verdict: 1 violation.

## settle (5 violations)

| rule | result |
|---|---|
| pairing | VIOLATION L15 "Ask a go-between to mediate a contested matter, by the skill `tell`; never treat its proposal as binding." (prohibition of another concern) ; VIOLATION L23 "...; never fork it." (prohibits separating, a different instruction from bringing to the owner) |
| one instruction per sentence | VIOLATION L23 "Bring a failed mediation over an exclusive resource to the owner, the claim with the earlier `sent` stamp holding it meanwhile" (two: bring, and who holds) ; VIOLATION L25 "Bring any other dispute to the owner when both sides ask, both versions standing separate meanwhile" (two: bring, and keep both versions) |
| shared content not copied | VIOLATION L23 (see reserve L23) |
| one procedure (ask go-between, separate, bring owner, record) | PASS |
| edges, tags, terms, other pairings (L13, L19, L29) | PASS |

Verdict: 5 violations.

## sweep (3 violations)

| rule | result |
|---|---|
| one instruction per sentence | VIOLATION L13 "Look in presence for a member that seems gone under a new address, by its card's `name`, and ask it by the skill `tell` before you move its card" (look, and ask) |
| one term per concept; defined | VIOLATION L15 "Sweep a card whose `harness` your presence covers; never move a card your presence cannot see." (`sweep` is undefined in the body and shares a concept with `move` in the same sentence and L19) |
| pairing | VIOLATION L19 "Move another member's card into `<root>/departed/` once a leave notice named it, or once presence lacks its address and its `updated` is over 24 hours old; never delete a card." (prohibition names deleting, not moving outside the conditions) |
| edges: card L21 present; tell L13, L23 present (extra) | see cross-skill |
| other rows | PASS |

Verdict: 3 violations.

## scribe (10 violations)

| rule | result |
|---|---|
| one term per concept | VIOLATION L17 "Hold the scribe role as a stewardship like any other" vs L13/L21/L51 "the stewardship `protocol`" and L53/L55 "the role" (one concept, two names) ; VIOLATION L55 "files in your own tree" (ontology term is `checkout`, ontology L39) |
| one instruction per sentence | VIOLATION L25 "Write and propagate what the peers consent to; never decide a change alone." (two verbs, two acts) |
| pairing | VIOLATION L35 "Report each outcome ... ; never leave a draft unresolved." (prohibition names resolving, not reporting) |
| shared content not copied | VIOLATION L15 "Take a contested scribe claim to a go-between; never take it to the owner unless both sides ask." (restates settle L25 rule for one case) ; VIOLATION L31 "Hold each round to the skill `protocol-change`; never run one from memory." (near-copy of propose L29) |
| terms defined | VIOLATION L31 "round" (undefined; first use tag L28); VIOLATION L35 "adopted, deferred, or separated" (and L43 "separated project", L47) undefined; VIOLATION L34/L37 "ship" undefined; VIOLATION L41 "patch ... minor ... major" (version-number senses undefined) |
| one procedure (take role, keep text, run rounds, ship, hand on) | PASS |
| edges propose L29, protocol-change L31, ontology L9 present | PASS |

Verdict: 10 violations.

## propose (7 violations)

| rule | result |
|---|---|
| one procedure | VIOLATION L4 "report a defect or propose a change to the scribe, and, as the scribe, circulate the draft as one round" (a sender's procedure and the scribe's procedure in one skill; roster row names only "the author's part") |
| one instruction per sentence | VIOLATION L19 "Put the problem, its evidence ... and the wording in a file in your own tree, inline at ten lines or fewer" (file, or inline: two instructions) |
| one term per concept | VIOLATION L19 "your own tree" (ontology: `checkout`) |
| terms defined | VIOLATION L19 "a journal path" (`journal` undefined here and in ontology) ; VIOLATION L25 "each receiver's turn over its whole context as the round's cost" (`turn`, `context` narrow senses undefined; `round` undefined) |
| shared content not copied | VIOLATION L29 "Run the round by the skill `protocol-change`; never run it from memory." (near-copy of scribe L31) |
| pairing L13, L17, L21, L27; tags; edge protocol-change L29 | PASS |

Verdict: 7 violations.

## consent (4 violations)

| rule | result |
|---|---|
| terms defined | VIOLATION L13 "heavy work" (undefined; ontology's term is `busy`) ; VIOLATION L15 "the round" (undefined) |
| pairing | VIOLATION L19 "Check that the draft holds by the skill `vouch`; never accept to be agreeable." (prohibition names a motive, not the unchecked acceptance) |
| one instruction per sentence | VIOLATION L23 "Answer by the skill `tell` with `[answer] accept` once your check holds, or with `[answer] object: <reason>`" (two answers) |
| one procedure; edges; tags; other rows | PASS |

Verdict: 4 violations.

## protocol-change (6 violations)

| rule | result |
|---|---|
| one procedure | VIOLATION L42-46 `<keep-the-culture>`: "Read `<root>/culture/` as history; never as rules." and "Add a deliberation to `<root>/culture/` for a choice that changes what the society values" (a second procedure; absent from the description L4-5 and from the roster row) |
| shared content not copied | VIOLATION L43 (copies ontology L85 "never call its content rules") |
| terms defined | VIOLATION L12 "round" (undefined; tag name first use) ; VIOLATION L17 "defer, then separate" (and L25, L29, L37 "separates its project", "separated from") undefined ; VIOLATION L29 "Bind a silent member" (`bind` undefined) |
| pairing | VIOLATION L29 "Bind a silent member from its next read of the pointer, open to a late objection that separates its project; never refuse a late objection." (prohibition names another concern, and the sentence carries two: bind, and stay open) |
| leaf: names neither `propose` nor `consent` (grep: skill names present = ontology, protocol-change only) | PASS |
| other rows (L13, L19, L21, L25, L27, L33, L35, L37, L39, L45) | PASS |

Verdict: 6 violations.

## Cross-skill checks

Edges (roster graph vs text):

| skill | roster edges | found at | missing | extra |
|---|---|---|---|---|
| steward | reserve, settle, scribe | L39, L37, L41 | none | none |
| reserve | tell | L21 | none | none |
| settle | tell, steward | L15, L29 | none | none |
| sweep | card | L21 | none | tell (L13, L23) |
| scribe | propose, protocol-change | L29, L31 | none | card (L39) |
| propose | protocol-change | L29 | none | tell (L13, L17) |
| consent | protocol-change | L15 | none | vouch (L19), tell (L23) |
| protocol-change | none (leaf) | none | none | none |

Every skill names `ontology` at L9 (roster: every other skill names ontology). protocol-change names neither propose nor consent: PASS. propose names protocol-change (L29): PASS. consent names protocol-change (L15): PASS.

Near-copies found by grep across `/Users/ryzhakar/pp/aoa-skills/peers/skills`:
- reserve L23 / settle L23: "the claim with the earlier `sent` stamp" (same rule twice).
- scribe L31 / propose L29: "never run one/it from memory" with `protocol-change`.
- scribe L15 / settle L25: "to the owner ... both sides ask".
- protocol-change L43 / ontology L85: "never as rules" / "never call its content rules".
- steward L15, L17, L21 / scribe L13: "by card edit and `[notice]`" (same form for a claim; scribe's is the `protocol` case; not counted).
- sweep L23 / steward L33: "never move one unannounced" (same words, different subject; not counted).
- "your own tree" in propose L19, scribe L55 also in gossip L31, tell L51: one phrase, ontology term is `checkout`.

## Content check

| skill | inferred procedure (one sentence) | roster row | match |
|---|---|---|---|
| steward | Claim, hold, release, and guard a shared thing by your card and branch, handing questions, resources, and the protocol to other skills. | look after a shared thing for every session | yes |
| reserve | Hold an exclusive resource by a board line and keep the board true. | claim an exclusive resource on the board | yes |
| settle | Take a dispute to a go-between, separate if it fails, bring the owner the rest, record the outcome. | take a dispute to a go-between | yes; the record step (L29) returns to steward |
| sweep | Move a gone member's card to departed after checking it answers nowhere. | move a gone member's card to departed | yes |
| scribe | Take, keep, ship, and hand on the protocol role. | hold the scribe role; ship by consent; hand it on | yes |
| propose | Report a defect or propose a change to the scribe; the scribe circulates the draft. | the author's part of a round | exceeds: scribe circulation (L24-30) is a second role's procedure |
| consent | Check a protocol draft and answer accept or object. | each receiver's part of a round | yes |
| protocol-change | Time the round, weigh answers, close it, apply a shipped change. | shared context of a round | exceeds: `<keep-the-culture>` L42-46 is a second procedure |

## Verdicts

| skill | verdict |
|---|---|
| steward | 6 violations |
| reserve | 1 violation |
| settle | 5 violations |
| sweep | 3 violations |
| scribe | 10 violations |
| propose | 7 violations |
| consent | 4 violations |
| protocol-change | 6 violations |

Comparison with self-audit.md (read after): self-audit.md holds no VIOLATION entry (grep: zero hits) and marks the rules it lists for these skills PASS; none of the violations above appear in it.

Summary: None of the eight skills conforms; counts are scribe 10, propose 7, steward 6, protocol-change 6, settle 5, consent 4, sweep 3, reserve 1, for 42 in all. The recurring faults are two instructions in one sentence (settle L23, L25; sweep L13; scribe L25; propose L19; consent L23; protocol-change L29), narrow terms left undefined (`round`, `separate`, `open stewardship`, `ship`, `heavy work`, `journal`), and `your own tree` used where ontology says `checkout`. Cross-skill, all outgoing roster edges are present and protocol-change stays a leaf, but sweep, scribe, propose, and consent add edges the roster lacks, and four sentences are copied or near-copied across skills (reserve/settle, scribe/propose, scribe/settle, protocol-change/ontology).
