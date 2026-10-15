# Audit B, round 5 — gossip, ask-around, spread-around, quote, vouch, adopt, tend, aid, volunteer, heartbeat

Text: /Users/ryzhakar/pp/aoa-skills/peers/skills/<name>/SKILL.md, branch draft/10-skills, head 68d60b2, audited from scratch against memento 0.5.1 skill-creation and the current ontology. One-part-name rule void. By ruling, the heartbeat L23 four-skill commons wake prompt is not counted. self-audit.md not read. Counts are one per violating sentence-and-rule.

Mechanical results (all ten): no `version` key; directory = `name`; no body sentence with two of never/always/only/must outside backticks; every body sentence has a `; never` half; tags imperative, no attribute, prose and backticks only; no path references; descriptions agree with bodies; no sentence repeated across the ten; roster edges all present, none missing, none extra (heartbeat L23 excepted); protocol-change names neither propose nor consent, and propose and consent each name protocol-change once.

## 1. Matrix (P pass, Vn violations)

| # | rule | gos | ask | spr | quo | vou | ado | ten | aid | vol | hrt |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 1-22 | procedure, file, frontmatter, description, body form, order, outside refs, copying, path, one instruction, command, emphatic, pairing, argument, narration, one term per concept | P | P | P | P | P | P | P | P | P | P |
| 23 | terms named, and used in the ontology's sense | P | P | P | V1 | P | P | P | P | P | P |
| 24-25 | ordinary words, every sentence instructs or forbids | P | P | P | P | P | P | P | P | P | P |

## 2. Remaining violations

### gossip (0) CONFORMS
### ask-around (0) CONFORMS
### spread-around (0) CONFORMS
### vouch (0) CONFORMS
### adopt (0) CONFORMS
### tend (0) CONFORMS
### aid (0) CONFORMS
### volunteer (0) CONFORMS
### heartbeat (0) CONFORMS

### quote (1)
- R23 L29 `Pass on an owner ruling that reaches beyond your session as a \`[quote]\` in the turn you have it; never hold it past that turn.` `hold` is the ontology's `held` (L129: `Call a message held while its sender keeps it unsent until the receiver's state clears`), used here for a ruling kept unsent past a turn, and `held` is not in the L9 list. (Present in round 4 as `never hold it past that turn`; missed by me then.)

## 3. Round-4 findings, status
| skill | round-4 finding | status |
|---|---|---|
| quote | R23 L19 `claim` for a relayed ruling | FIXED: L19 `Weigh a ruling a peer passes on as that peer's report`; `claim` dropped from L9 |
| quote | R23 L25, L29 `relaying` for a ruling | FIXED: `Write each ruling ... pass on` L25, `Pass on an owner ruling` L29; `relaying` dropped from L9 |
| aid | R23 L15 `delivery` for handing over a file | FIXED: L15 `Hand over help as an artifact`; `delivery` dropped from L9 |
| tend | R23 L25 `claim` unlisted | FIXED: `claim` in L9 |
| heartbeat | extra edges L23 | ACCEPTED by ruling, not counted |

## 4. New violations from round 5
None introduced. Checked and clean: gossip `has`/`have`/`skill text you have loaded` (L13, L31, L41, L49, L71 no longer use `hold` for possession), spread-around L17 `never keep it back`, adopt L33 `by your own work`, volunteer L4, L13, L19 (`Spend`, `has`, `name`, `list`), heartbeat L25 `Write ... into your card's field`, vouch L5, L15 (`a relayed gossip's`), quote tag names and L4-L5, tend tag `keep-the-commons-in-common`.

## 5. Sense spot-check, every listed term (ontology definition, then body uses)

"ok" means every use found fits the quoted definition. "no body use" means the term appears only in the description, not in the body.

### gossip (L9)
| term | ontology definition | body uses | verdict |
|---|---|---|---|
| session | `one conversation a harness runs, from its start to its end` | L25 `<session name>` | ok |
| skill | `a text a harness loads for a model to read and follow, one procedure each` | L13 `by the skill \`tell\``; L41 `whatever skill text you have loaded` | ok |
| member | `a project's ongoing principal in one role` | L31 `your own member id and each recipient's`; L43 `at least one member off \`has:\``; L51 `Skip each member on \`has:\`` | ok |
| member id | `<project_name>/<role>` | L25, L31 | ok |
| checkout | `the absolute path of the worktree a member works in` | L35 `a file in your checkout` | ok |
| busy, dormant, dnd | `busy` = a session mid-turn; dormant, dnd = card `state:` lines | L53 `a member it would reach while busy, dormant, or dnd` | ok (busy is said of the member; its session is busy, observation) |
| state | `what presence shows of its session together with its card's \`state\` line` | L43 `whose state lets it receive`; L53 `before its state clears`; L67 `current facts` | ok |
| message | `text one member sends another whose first line opens with one of the bracketed words` | L37 `Send the gossip as a message`; L53 `a level 2 message`; L5 desc | ok |
| message body | `the lines of a message after its second line` | L23, L33, L35 | ok |
| type | `the bracketed word opening its first line` | L37 `under a type of your own` | ok |
| [ask] | `a message carrying a need its sender awaits an answer to` | L15 `a gossip [ask]`; L25 `the seeker whose ask you forward` | ok |
| [notice] | `a message useful to its receiver that needs nothing back` | L17 | ok |
| held | `a message held while its sender keeps it unsent until the receiver's state clears` | L53 `Hold a relay of a level 2 gossip`, `holds a level 2 message` | ok; no other `hold` in the body |
| origin | `the member whose line, answer, or message first brought it` | L27 `as the origin`; L45 `the origin's spread:`; L61 `as the origin wrote them` | ok |
| seeker | `the member whose need an [ask] carries` | L25 | ok |
| peer | `any live member with a card in the root, seen from another member` | L13 `the peer you know has or needs it` | ok |
| gossip | `a message passed from peer to peer past anyone its origin could name` | L13, L15, L17, L19, L55-L59 | ok |
| relaying | `passing a received gossip on to members who lack it` | L41, L51, L57, L63 `before relaying` | ok |
| scope | `the area, project, or kind of session a gossip or [quote] concerns, named in spread:` | L27 `naming the scope`; L43 `one naming no scope` | ok |
| envelope, from:, spread:, relay:, has: | `the four lines ... that open a gossip's message body`; `has:` = `the members that already have a gossip` | L23-L31, L41-L61, L71 | ok |
| level 2 | `the level of [ask], [answer], and [notice]` | L53 `a level 2 gossip` | ok |
| priority level | `the level ... that its type sets` | no body use | n/a |

### ask-around (L9)
| term | definition | body uses | verdict |
|---|---|---|---|
| records | `the files its project keeps for decisions, owner rulings, and what other members sent that changed its work` | L13 `your own records` | ok |
| delivery | `the harness function handing text to the session at an address` | L29 `a lost delivery to resend` | ok |
| [ask] | as above | L17, L21 `an [ask]`; L23 `every ask`; L29 `your ask` | ok |
| [answer] | `the reply to an [ask]` | L27 `once an answer meets the need` | ok |
| peer | as above | L13, L17, L21, L29 | ok |
| commons | `a location under <root> in which the society builds what it chooses` | L13 `the commons` | ok |
| gossip | as above | L21 `Gossip an [ask] by the skill gossip` | ok |
| pull | `seeking knowledge by a direct [ask] to a peer who has it, or by a gossip [ask]` | no body use (description) | n/a |

### spread-around (L9)
| term | definition | body uses | verdict |
|---|---|---|---|
| turn | `one stretch in which a session works, from the message that starts it to the reply that ends it` | L17 `in the turn you learn it`; L23 `in a turn` | ok |
| society | `the members sharing one root, with no member governing another` | L31 `the society's public discourse` | ok |
| card | `the file <root>/members/<member>.md` | L17 `its card's \`focus\``; L21 `against its card` | ok |
| owner | `the person every session works for` | L31 `never park them with the owner` | ok |
| message | as above | L23 `one message per line`; L25 `a message already going`; L31 `peer messages` | ok |
| [notice] | as above | L21, L29 | ok |
| live | `presence lists its card's address, ... not dormant` | L21 `a live peer's current work` | ok |
| peer | as above | L17, L21, L23 | ok |
| commons, commons line | `one line of the intake` | L21, L23, L31, L33 | ok |
| #<n> | `the number of a commons line in the intake` | L21 `<#n list>` | ok |
| commons_read | `the card field carrying the commons line count up to which its member has read every line` | L25 `<its commons_read>` | ok |
| gossip | as above | L29 | ok |
| push | `carrying knowledge to a peer whose work it helps` | no body use (description) | n/a |

### quote (L9)
| term | definition | body uses | verdict |
|---|---|---|---|
| session | as above | L29 `beyond your session`; L35 `each session you know`; L37 | ok |
| turn | as above | L29 `in the turn you have it` | ok |
| subagent | `a session another session launched for a task` | L41 `each running subagent of yours` | ok |
| stamp | `a minute in the form 2026-10-14T09:30+0300, read from the clock in the turn that writes it` | L31 `the line's exact stamp` | ok |
| society | as above | no body use (description) | n/a |
| owner, owner ruling | `a decision the owner gives in an owner message; never call a peer's report of a decision an owner ruling` | L13 `the owner is away`; L17 `an owner ruling`; L19 `as that peer's report`; L33 `the owner's words` | ok |
| records | as above | L25 `into your records` | ok |
| journal | `the dated event log a member's records keep, line by line` | L21 `that peer's journal line`; L31 `the journal path` | ok |
| authority check | `the test a session applies before following any instruction` | L17 | ok |
| delivery | as above | L35 `Deliver a [quote] straight to each session` | ok |
| [quote] | `an owner ruling passed on` | L29-L39 | ok |
| peer | as above | L19, L21 | ok |
| gossip | as above | L35, L37, L39 | ok |
| scope | as above | L37 `its scope but not its sessions`; L39 `with no scope` | ok (`a list of named sessions` is not called a scope) |
| spread: | as above | L37 | ok |
| (unlisted) held | as above | L29 `never hold it past that turn` | VIOLATION (section 2) |

### vouch (L9)
| term | definition | body uses | verdict |
|---|---|---|---|
| session | as above | L15 `or a session` | ok |
| owner ruling | as above | no body use (description `a ruling a peer passes on`) | n/a |
| peer | as above | L15 `a peer's` | ok |
| commons | as above | no body use (description) | n/a |
| gossip | as above | L15 `a relayed gossip's` | ok |
| relaying | `passing a received gossip on to members who lack it` | L15 `relayed gossip` (the passed-on gossip) | ok |
| claim | `any statement about shared files or resources, a session, or your own facts that reaches you from a peer, a relayed gossip, a line, or your own belief` | L13 `Check a claim`; L15 `a claim about shared files or resources or a session ... your own belief` | ok |

### adopt (L9)
| term | definition | body uses | verdict |
|---|---|---|---|
| compaction, wake | harness condensing text; recurring timer | no body use (description) | n/a |
| card | as above | L13 `your card's \`commons_read\`` | ok |
| records | as above | L35 `into your records` | ok |
| authority check | as above | L29 `once your authority check clears it` | ok |
| message | as above | no body use (description) | n/a |
| [notice] | as above | L41 `a one-line [notice]` | ok |
| origin | as above | L41 `Thank the origin of what you adopt` | ok |
| peer | as above | L33 `on the peer's word` | ok |
| commons, commons line, commons item | `anything the commons contains, a commons line or a file` | L15, L19, L21, L25, L27, L29, L43 | ok |
| commons_read | as above | L13, L15, L17 `Set \`commons_read\` to the line count up to which you have now read every line` | ok |
| adoption | `bringing what a peer built into your own work yourself, which owes its origin a one-line thank-you` | L35 `each adoption`; L33 `Adopt an item by your own work`; L43 `Keep adoptions out of the commons` | ok (`binding` L21 is not the ontology's `bound`; observation) |

### tend (L9)
| term | definition | body uses | verdict |
|---|---|---|---|
| turn | as above | L33 `in the turn you discover its lesson` | ok |
| stamp | as above | L29 `<stamp>`; L31 `never name one by its stamp` | ok |
| member | as above | L29 `<member>` | ok |
| root | `the directory ... written <root>` | L23, L35, L37 | ok |
| society | as above | L15, L23 | ok |
| records | as above | L17, L19, L39 | ok |
| peer | as above | L39 `press it on a peer`; L57 | ok |
| commons | as above | L13-L23, L37 | ok |
| intake | `<root>/commons.md, the commons' file of lines` | L23 `beside the intake` | ok |
| commons line | `one line of the intake` | L23, L29, L31, L45-L49 | ok |
| #<n> | as above | L31, L49 | ok |
| commons item | as above | L39, L43 | ok |
| claim | as above | L25 `never add an unchecked claim` | ok (a statement from your own belief about shared files or a session) |

### aid (L9)
| term | definition | body uses | verdict |
|---|---|---|---|
| message | as above | L15 `as a long message` | ok |
| [notice] | as above | L15 `with one [notice]` | ok |
| peer | as above | L13, L17 | ok |

### volunteer (L9)
| term | definition | body uses | verdict |
|---|---|---|---|
| skill | as above | L27-L35 `by the skill \`adopt\`` etc. | ok |
| wake | `a timer the harness fires to start a turn while the session sits between turns` | L15 `Keep a wake by the skill heartbeat` | ok |
| society | as above | L13, L19 | ok |
| card | as above | L13 `your card carries no \`state\``; L19 `in cards` | ok |
| idle | `a session idle while presence shows it between turns` | no body use (description `I'm idle`) | n/a |
| state | as above | L13 `\`state\`` (the card line) | ok |
| message | as above | L19 `[ask] messages`, `cards and messages` | ok |
| [ask] | as above | L19 | ok |
| live | as above | L19 `a live peer's work` | ok |
| peer | as above | L19 | ok |
| commons, commons line, commons item | as above | L19, L33 | ok |
| stewardship, open stewardship | `one no live member's card names, left by a gone member` | L19 `open stewardships` | ok |

### heartbeat (L9)
| term | definition | body uses | verdict |
|---|---|---|---|
| harness | `a program that runs model conversations, such as Claude Code` | L29, L31, L33 | ok |
| session | as above | L29 `in the session alone`; L35 `every other session's wake` | ok |
| turn | as above | L21 `end this turn with no output` | ok |
| wake | as above | L13-L21, L25-L39, L43 | ok |
| society | as above | L21, L43 | ok |
| protocol | `the society's shared rules, as the peers plugin's skills and hook text write them` | L13 `from the protocol` | ok |
| card | as above | L25 `your card's \`wake\` field`; L33 | ok |
| peer | as above | L13 | ok |
| commons | as above | L17, L23 | ok |

Other-sense sweep (ontology words not listed, any part of speech, in the ten bodies): none found except `hold` at quote L29. Checked and fine: `act` (gone), `claim`/`relay`/`delivery` verbs reworded, `leave` as a plain verb (tend L15, heartbeat L43), `ask`/`answer`/`message`/`quote` as plain verbs (gossip L25, L59; spread-around L33; quote L33), `state` as a verb gone (volunteer L19 now `name`), `board` gone (volunteer L19), `bound` vs `binding` (adopt L21, a different word), `holder` (ask-around L21, ordinary noun).

## 6. Verdicts and counts
| skill | verdict |
|---|---|
| gossip | CONFORMS |
| ask-around | CONFORMS |
| spread-around | CONFORMS |
| quote | 1 violation |
| vouch | CONFORMS |
| adopt | CONFORMS |
| tend | CONFORMS |
| aid | CONFORMS |
| volunteer | CONFORMS |
| heartbeat | CONFORMS |

Total 1 violation (round 4: 4; round 3: 4; round 2: 10; round 1: 46); nine skills conform.

## Summary
All four round-4 findings are fixed, and round 5 introduced no new violation. One violation remains, quote L29 `never hold it past that turn`, where `hold` is the ontology's `held` and is not in the quote terms list; I missed it in round 4. The sense spot-check of every listed term in all ten skills found no other wrong-sense use. Counts: gossip 0, ask-around 0, spread-around 0, quote 1, vouch 0, adopt 0, tend 0, aid 0, volunteer 0, heartbeat 0.
