# Audit C, round 4: steward, reserve, settle, sweep, scribe, propose, consent, protocol-change

Auditor: audit-C. Text: `/Users/ryzhakar/pp/aoa-skills/peers/skills/<name>/SKILL.md`, branch draft/10-skills, head e336865. Rules: skill-creation 0.5.1; one-part-name rule void. Standards as before. Checked on all eight: frontmatter only `name`, `description`; directory = name; every body line inside a tag; imperative tag names; no attributes; no path to another skill; one `never` per sentence, no only/must/always (grep zero); every listed term has an ontology definition; every term the body uses sits in the terms sentence (round-3 gaps closed).

## Per-skill result

| skill | violations | remaining |
|---|---|---|
| steward | 1 | L9 `held` wrong-sense binding |
| reserve | 1 | L9 `held` wrong-sense binding |
| settle | 0 | none |
| sweep | 0 | none |
| scribe | 0 | none |
| propose | 0 | none |
| consent | 0 | none |
| protocol-change | 0 | none |

### steward (1)
- steward L9 lists `held` and binds it with "never take them in another sense". Ontology L127: "Call a message held while its sender keeps it unsent until the receiver's state clears; never call a dropped message held." Body uses are the possession sense, not the message sense: L13 "Name each stewardship you hold in your card's `stewards`", L19 "Hold at most one machine-wide stewardship", L29 "a branch you hold", L39 "Hold an exclusive resource by the skill `reserve`". Wrong sense; the listing contradicts the body. NEW to this audit (the list entry existed in round 3 and I did not catch it).

### reserve (1)
- reserve L9 lists `held`. Body uses: L31 "or its resource tests held", L33 "whose resource still tests held", L19 "Hold an exclusive resource by its own line". A resource that tests held is in use; ontology L127 defines `held` for a message. Wrong sense. NEW to this audit, same cause.

## Round-3 findings

| round-3 finding | status |
|---|---|
| scribe L13 `departs` vs `gone` | fixed: L13 "once the scribe is gone"; `gone` listed in L9 |
| scribe L53 `[notice] leaving` unlisted | fixed: L53 "one leave notice"; `leave notice` listed |
| scribe L55, L57 "stands open" unlisted | fixed: "is an open stewardship"; `open stewardship` listed |

## Sense spot-check (the rewriter's named gap)

Method: for each listed term, three body uses where the body has three; definition quoted for the terms where a doubt arose, otherwise the ontology line cited. Wrong-sense uses found: `held` in steward and reserve only. Everything else is in sense.

| term | ontology definition (line) | body uses checked | verdict |
|---|---|---|---|
| held (steward, reserve) | L127 "a message held while its sender keeps it unsent until the receiver's state clears" | steward L13, L19, L39; reserve L19, L31, L33 | WRONG SENSE (possession / in use) |
| stewardship | L189 "a shared thing ... named in its card's `stewards`, as a service any peer may question" | steward L13 "Name each stewardship ... in your card's `stewards`"; L37 "Take a questioned stewardship to a go-between"; L39 "never hold one as a stewardship" | in sense |
| open stewardship | L193 "one no live member's card names, left by a gone member" | steward L21 "Take up an open stewardship you can serve"; scribe L55, L57 "is an open stewardship" | in sense |
| go-between | L197 "a third live peer that mediates a contested matter" | steward L37; settle L15 "Ask a go-between to mediate", L17 "a go-between's proposal" | in sense |
| exclusive resource | L155 "a thing that exists once and cannot be forked" | steward L39; reserve L13, L19; settle L25 | in sense |
| resource board | L157 "`<root>/resources.md` ... one line per held exclusive resource" | reserve L13 "Read the board `<root>/resources.md`"; L19; L27 | in sense |
| stamp | L39 "a minute in the form `2026-10-14T09:30+0300`, read from the clock" | reserve L23 "the earlier `sent` stamp"; propose L19 "the exact stamp" | in sense |
| departed card | L59 "a card moved into `<root>/departed/`" | reserve L33 (two uses: "card is departed", "citing the departed card"); sweep L21 "into `<root>/departed/`" | in sense |
| member id | L55 `<project_name>/<role>` | reserve L19 `<member id>` | in sense |
| owner | L67 "the person every session works for ... never call the owner a member" | settle L13 "the owner's attention", L25, L27; scribe L49 | in sense |
| bringing a matter to the owner | L81 "writing it into your own records and into your next answer to the owner's word" | settle L25 "Bring a failed mediation ... to the owner", L27; scribe L49 | in sense |
| brought matter | L83 "reversible choice goes ahead and irreversible choice waits for the owner's word" | settle L29 "a brought dispute ... while it waits" | in sense |
| presence | L89 "the harness function listing every session it can see" | sweep L13 "Look in presence", L17 "your presence covers", L21 "presence lacks its address" | in sense |
| address | L21 `<harness>://<host>/<harness-ref>` | sweep L13 "under a new address", L21 "lacks its address" | in sense |
| harness | L13 "a program that runs model conversations" | sweep L17 "`harness` your presence covers"; protocol-change L35 "your harness reloads it" | in sense |
| gone | L137 "once it sends a leave notice, or once presence drops its address" | sweep L13 "seems gone"; scribe L13 "once the scribe is gone" | in sense |
| leave notice | L133 "a message opening `[notice] leaving`" | sweep L21 "once a leave notice named it"; scribe L53; protocol-change L21 "a member that sent a leave notice" | in sense |
| live | L135 "presence lists its card's address, it has sent no leave notice, it is not dormant ..." | sweep L27; scribe L13, L29, L47 | in sense |
| peer | L139 "any live member with a card in the root, seen from another member" | settle L13; scribe L23; protocol-change L25 "a peer besides the proposer" | in sense |
| [hazard] | L115 "what can corrupt or kill a peer's work now" | steward L27, L31 | in sense |
| [notice] | L121 "useful to its receiver that needs nothing back" | steward L15, L17, L33; sweep L27; scribe L47 | in sense |
| [ask] | L117 "a need its sender awaits an answer to" | scribe L29 "one `[ask] protocol draft: <path>`"; propose L17 | in sense |
| [answer] | L119 "the reply to an `[ask]`" | consent L23, L25; protocol-change L19 "Weigh answers" | in sense |
| turn | L23 "one stretch in which a session works" | scribe L27 "the turn each receiver spends reading a draft" | in sense |
| hook, plugin | L29 "a script the harness runs at a fixed event"; L31 "a package of skills and hooks a harness loads" | scribe L19 "the peers plugin's skills, its hook text"; L39; L43 "the plugin's version" | in sense |
| protocol | L53 "the society's shared rules, as the peers plugin's skills and hook text write them" | scribe L19 "canonical protocol text", L23, L55; propose L13 "the protocol text"; protocol-change L41 "your card's `protocol`" | in sense |
| checkout | L63 "the absolute path of the worktree a member works in" | scribe L57; propose L19 "a file in your checkout" | in sense |
| journal | L77 "the dated event log a member's records keep" | propose L19 "its evidence as a journal path" | in sense |
| type | L113 "the bracketed word opening its first line" | propose L17 "under a type of your own" | in sense |
| scribe | L195 "the member whose card's `stewards` lists `protocol`" | scribe L13, L31; propose L13, L17, L23 | in sense |
| pointer | L215 "`<root>/PROTOCOL.md`" | scribe L21, L45, L49; protocol-change L29, L37 | in sense |
| change line | L217 "the pointer's dated line stating what one version changed" | scribe L45, L47; protocol-change L35, L37, L39 | in sense |
| protocol change | L219 "any change to the peers plugin's skills or hook text" | propose L4, L17 "propose a change"; protocol-change L4 | in sense |
| draft | L221 "the written wording of a protocol change put to the society" | scribe L29, L33, L37; consent L13, L19; protocol-change L13, L25 | in sense |
| round | L223 "the span from a draft's circulation to its outcome" | scribe L27 "open a round", L31 "Close each round"; propose L25; consent L15 | in sense |
| enacted | L225 "once its round closes with the society's consent" | scribe L37, L39; protocol-change L25, L29 | in sense |
| separating | L227 "a project's sessions keeping their loaded protocol version while the society enacts a change they object to" | scribe L37, L45; protocol-change L31 "separating its project", L39 | in sense |
| bound | L229 "bound to an enacted change once that change applies to it" | protocol-change L29 | in sense |
| shipping | L231 "editing the peers plugin and the pointer to carry an enacted change" | scribe L39, L43, L55; protocol-change L35 header | in sense |
| reloaded | L253 "your loaded skill text ... reloaded once the owner runs `/reload-plugins` or relaunches you" | protocol-change L35 "until your harness reloads it" | in sense |
| reply time | L125 "the time its second line names for an answer" | scribe L31; consent L13, L15; protocol-change L13, L25 | in sense (note: consent L15 "the round's reply time" and protocol-change L13 "a draft's reply time" attach it to a round and a draft, where the definition says a message; not counted) |
| session, member, card, society | L15, L45, L57, L51 | steward L25, L29; settle; sweep L25; scribe | in sense |

## Cross-skill and content

Edges: steward -> reserve L39, settle L37, scribe L41; reserve -> tell L21; settle -> tell L15, steward L33; sweep -> card L25; scribe -> propose L33, protocol-change L31 (extra card L41); propose -> protocol-change L25; consent -> protocol-change L15. protocol-change names neither propose nor consent; propose and consent each name protocol-change. No near-copied sentence across the eight. Each skill's procedure matches its roster row, as in round 3. propose L25 "Expect your request's outcome ..." remains an expectation, not an act (note, not counted).

## Verdicts

steward 1; reserve 1; settle CONFORMS (0); sweep CONFORMS (0); scribe CONFORMS (0); propose CONFORMS (0); consent CONFORMS (0); protocol-change CONFORMS (0). Total 2 (round 3: 3).

Summary: All three round-3 findings on scribe are fixed, and scribe now conforms. The sense spot-check found one wrong-sense term: `held`, bound in steward L9 and reserve L9 to ontology L127's message sense while the bodies use hold and "tests held" for stewardships and resources; every other listed term is used in its ontology sense. Per-skill counts: steward 1, reserve 1, settle 0, sweep 0, scribe 0, propose 0, consent 0, protocol-change 0.
