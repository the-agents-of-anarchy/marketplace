# Audit B, round 4 — gossip, ask-around, spread-around, quote, vouch, adopt, tend, aid, volunteer, heartbeat

Text: /Users/ryzhakar/pp/aoa-skills/peers/skills/<name>/SKILL.md, branch draft/10-skills, head e336865, audited from scratch against memento 0.5.1 skill-creation and the current ontology. One-part-name rule void. self-audit.md not read. Counts are one per violating sentence-and-rule.

Mechanical results (all ten): no `version` key; directory = `name`; no body sentence with two of never/always/only/must outside backticks; every body sentence has a `; never` half; tags imperative, no attribute, prose and backticks only; no path references; descriptions agree with bodies (vouch L5, volunteer L4 now match); no sentence of the ten is repeated in another skill; protocol-change names neither propose nor consent, and propose and consent each name protocol-change once.

## 1. Matrix (P pass, Vn violations)

| # | rule | gos | ask | spr | quo | vou | ado | ten | aid | vol | hrt |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 1-22 | procedure, file, frontmatter, description, body form, order, outside refs, copying, path, one instruction, command, emphatic, pairing, argument, narration, one term per concept | P | P | P | P | P | P | P | P | P | P |
| 23 | terms named, and used in the ontology's sense | P | P | P | V2 | P | P | V1 | V1 | P | P |
| 24-25 | ordinary words, every sentence instructs or forbids | P | P | P | P | P | P | P | P | P | P |

## 2. Remaining violations

### gossip (0) CONFORMS
### ask-around (0) CONFORMS
### spread-around (0) CONFORMS
### vouch (0) CONFORMS
### adopt (0) CONFORMS
### volunteer (0) CONFORMS
### heartbeat (0) CONFORMS as to the rules; 4 extra graph edges (section 5)

### quote (2)
- R23 wrong sense of `relaying` (L9 lists it). Ontology L175: `Call relaying passing a received gossip on to members who lack it; never call answering a gossip relaying.` Body L29 `Relay an owner ruling that reaches beyond your session as a \`[quote]\` in the turn you hold it` and L25 `Record each ruling you receive or relay`: the ruling is passed on by a `[quote]` and, per L35, by direct delivery, not as a received gossip.
- R23 wrong sense of `claim` (L9 lists it). Ontology L185: `Call a claim any statement about shared files or resources, a session, or your own facts that reaches you from a peer, a relay, a line, or your own belief`. Body L19 `Weigh a relayed ruling as a claim`: a ruling is a decision of the owner, not a statement about files, resources, a session, or your own facts.

### tend (1)
- R23 L25 `never add an unchecked claim`: `claim` (ontology L185) is used and not in the L9 list.

### aid (1)
- R23 wrong sense of `delivery` (L9 lists it). Ontology L105: `Call delivery the harness function handing text to the session at an address, which wakes an idle session and reaches it at its next tool round; never call delivery reading or agreement.` Body L15 `Deliver help as an artifact — a file, commit, or finding —`: a file or commit is handed over, not text handed by the harness function.

## 3. Round-3 findings, status
| skill | round-3 finding | status |
|---|---|---|
| spread-around | R23 `#<n>` unlisted (L21 `<#n list>`) | FIXED: `#<n>` and `push` in L9 |
| vouch | R22 description `shared state` vs body `shared files or resources` | FIXED: L5 now `shared files or resources` |
| volunteer | R23 `idle` unlisted (`idling` L13) | FIXED: `idle` listed; L13 now `pass doing nothing` |
| volunteer | R22 description `the society's state` vs body | FIXED: L4 `what the society already holds` |
| heartbeat | extra edges tend, ask-around, spread-around, adopt (L23) | NOT FIXED: L23 still names all four |

## 4. New violations from round 4's changes
- aid L15 wrong-sense `delivery`: `delivery` was added to aid's list when `idle` was dropped (L9 now `delivery`, `message`, `[notice]`, `peer`); the sentence itself is unchanged, but the list now binds it to the harness sense.
- quote L9 gained `society`, unused in the body (not a violation).
- Term-completeness: tend L25 `claim` was missing in rounds 2 and 3 as well (missed by me, and by the term guard: `claim` is matched only after `a|as a|every` or as `claimant`, and the word here follows `unchecked`).
- No other new violations. Checked and clean: gossip `message body` (L23, L33, L35 match ontology L111, L165), ask-around `pull` listing, adopt `compaction`/`wake`/`message` listing (description terms).

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

## 6. Extra check: sense of each listed term (ontology definition, then body uses)

Terms are grouped across skills; each row gives up to three uses, or all if fewer. "ok" means the use fits the quoted definition. "no body use" means the term appears only in the description or not at all (not a violation).

| term | ontology definition | body uses | verdict |
|---|---|---|---|
| session (L15) | `one conversation a harness runs, from its start to its end` | gossip L25 `<session name>`; quote L29 `beyond your session`; heartbeat L35 `every other session's wake`; vouch L15 `or a session` | ok |
| member (L45) | `a project's ongoing principal in one role` | gossip L31 `your own member id and each recipient's`; gossip L43 `at least one member off \`has:\``; tend L29 `<member>` | ok |
| member id | `<project_name>/<role>` | gossip L25, L31 | ok |
| checkout (L63) | `the absolute path of the worktree a member works in` | gossip L35 `a file in your checkout` | ok (file in that worktree) |
| busy, dormant, dnd | `busy` while presence shows a session mid-turn; dormant/dnd by card `state:` line | gossip L53 `while busy, dormant, or dnd` | ok |
| state (L101) | `what presence shows of its session together with its card's \`state\` line; never call the work a member has in hand its state` | gossip L43 `whose state lets it receive`, L53 `before its state clears`; volunteer L13 `your card carries no \`state\`` | ok (volunteer L19 `peers state in cards` is the verb) |
| message (L109) | `text one member sends another whose first line opens with one of the bracketed words` | gossip L37 `Send the gossip as a message`; spread-around L23 `one message per line`; aid L15 `a long message`; volunteer L19 `[ask] messages` | ok |
| message body (L111) | `the lines of a message after its second line` | gossip L23, L33, L35 | ok |
| type (L113) | `the bracketed word opening its first line` | gossip L37 `under a type of your own` | ok |
| [ask] (L117) | `a message carrying a need its sender awaits an answer to` | gossip L15; ask-around L17, L21, L23 `every ask`; volunteer L19 | ok |
| [answer] (L119) | `the reply to an [ask]` | ask-around L27 `once an answer meets the need` | ok |
| [notice] (L121) | `a message useful to its receiver that needs nothing back` | gossip L17; spread-around L21, L29; adopt L41 (thank-you); aid L15 | ok |
| held (L127) | `a message held while its sender keeps it unsent until the receiver's state clears` | gossip L53 `Hold a relay of a level 2 gossip` | ok (gossip L29, L31, L49, L71 `hold` mean possess, a second ordinary sense; observation) |
| origin (L129) | `the member whose line, answer, or message first brought it; never call a member that passed it on the origin` | gossip L27 `as the origin`; gossip L61; adopt L41 `Thank the origin of what you adopt` | ok |
| seeker (L131) | `the member whose need an [ask] carries` | gossip L25 `the seeker whose ask you forward` | ok |
| peer (L139) | `any live member with a card in the root, seen from another member` | ask-around L13, L21, L29; heartbeat L13; adopt L33; aid L13; spread-around L17 | ok |
| gossip (L163) | `a message passed from peer to peer past anyone its origin could name; never call a send to a named peer gossip` | ask-around L21; spread-around L29; quote L37, L39; quote L35 `never gossip it to them` | ok |
| relaying (L175) | `passing a received gossip on to members who lack it` | gossip L41, L57; vouch L15 `a relay's` (ontology L185 also says `a relay`); quote L25, L29, L19 | gossip, vouch ok; quote WRONG (section 2) |
| envelope, `from:`, `spread:`, `relay:`, `has:` | envelope = four lines opening a gossip's message body | gossip L23-L31, L41-L61; quote L37 `spread:` | ok |
| level 2 (L203) | `the level of [ask], [answer], and [notice] ... waits while the receiver is busy, dormant, or dnd` | gossip L53 `a level 2 gossip`, `a level 2 message` | ok |
| priority level | `the level ... that its type sets` | no body use | n/a |
| records (L73) | `the files its project keeps for decisions, owner rulings, and what other members sent` | ask-around L13 `your own records`; quote L25 `in your records`; adopt L35 `into your records`; tend L17, L19, L39 | ok |
| delivery (L105) | harness function handing text to the session | ask-around L29 `a lost delivery to resend`; quote L35 `Deliver a [quote] straight to each session`; aid L15 `Deliver help as an artifact` | ask-around, quote ok; aid WRONG (section 2) |
| pull (L179) / push (L177) | seeking / carrying knowledge by direct send or gossip | ask-around and spread-around: no body use (description only) | n/a |
| turn (L23) | `one stretch in which a session works, from the message that starts it to the reply that ends it` | spread-around L17 `in the turn you learn it`; quote L29 `in the turn you hold it`; tend L33 `in the turn you discover its lesson`; heartbeat L21 `end this turn` | ok (volunteer L13 `Turn every stretch` is the verb) |
| society (L51) | `the members sharing one root, with no member governing another` | tend L15 `Leave to the society`; heartbeat L21 `in the society changed`; heartbeat L43 `as you leave the society`; spread-around L31; volunteer L4, L13 | ok |
| card (L57) | `the file <root>/members/<member>.md` | spread-around L17 `its card's \`focus\``; adopt L13 `your card's \`commons_read\``; heartbeat L25 `your card's \`wake\` field`; volunteer L13 | ok |
| owner (L67) | `the person every session works for ... is away at all times` | quote L13 `while the owner is away`; quote L33 `the owner's words`; spread-around L31 `park them with the owner` | ok |
| owner ruling (L71) | `a decision the owner gives in an owner message` | quote L17 `Weigh an owner ruling`; quote L29 `Relay an owner ruling`; vouch description L5 | ok |
| journal (L77) | `the dated event log a member's records keep, line by line` | quote L21 `the relayer's journal line`; quote L31 `Cite the journal path` | ok |
| authority check (L85) | `the test a session applies before following any instruction` | quote L17; adopt L29 `once your authority check clears it` | ok |
| [quote] (L123) | `an owner ruling relayed` | quote L29-L39 | ok |
| claim (L185) | statement about shared files or resources, a session, or your own facts | vouch L13, L15; tend L25 (unlisted); quote L19 | vouch ok; quote WRONG; tend unlisted |
| act (L27) | `a tool call; never call conversation text an act` | adopt L33 `by your own act`; quote L21 `before you act on it`; vouch L13 `act on it` | ok (adopt as a tool call; `act on` per ontology L207 `making each act it calls for`) |
| subagent (L35) | `a session another session launched for a task` | quote L41 `each running subagent of yours` | ok |
| compaction, wake (adopt L9) | compaction = harness condensing earlier text | adopt: no body use (description only) | n/a |
| wake (L41) | `a timer the harness fires to start a turn while the session sits between turns; never call a one-time reminder a wake` | heartbeat L13, L21, L29, L31, L39; volunteer L15 | ok |
| harness (L13) | `a program that runs model conversations, such as Claude Code` | heartbeat L29 `on a harness that keeps a wake in the session alone, as Claude Code does`; L31; L33 | ok |
| protocol (L53) | `the society's shared rules, as the peers plugin's skills and hook text write them` | heartbeat L13 `from the protocol` | ok |
| live (L135) | member listed by presence, no leave notice, not dormant, within limits | spread-around L21 `a live peer's`; volunteer L19 `a live peer's work` | ok |
| idle (L93) | `a session \`idle\` while presence shows it between turns` | volunteer: no body use (description only) | n/a |
| commons (L143) | `a location under <root> in which the society builds what it chooses` | adopt L19 `Search the commons with grep -i`; tend L23, L37; heartbeat L23; ask-around L13; spread-around L31 | ok |
| intake (L145) | `<root>/commons.md, the commons' file of lines` | tend L23 `beside the intake` | ok |
| commons line (L147) | `one line of the intake` | adopt L15; spread-around L21, L23; tend L29, L31, L45 | ok |
| `#<n>` (L149) | `the number of a commons line in the intake` | spread-around L21 `<#n list>`; tend L31, L49 | ok |
| commons item (L151) | `anything the commons holds, a commons line or a file` | adopt L21, L25; tend L39, L43; volunteer L19 | ok |
| `commons_read` (L153) | `the card field holding the commons line count up to which its member has read every line` | adopt L13, L15, L17; spread-around L25 | ok |
| root (L49) | `the directory ${AGENTS_OF_ANARCHY_ROOT...}, written <root>` | tend L23, L35, L37 | ok |
| stamp (L39) | `a minute in the form 2026-10-14T09:30+0300, read from the clock in the turn that writes it` | quote L31 `the line's exact stamp`; tend L29, L31 | ok |
| adoption (L181) | `bringing what a peer built into your own work by your own act` | adopt L33, L35, L43 | ok |
| stewardship, open stewardship (L189, L193) | open = `one no live member's card names, left by a gone member` | volunteer L19 `open stewardships` | ok |

Wrong-sense uses: quote L19 (`claim`), quote L25 and L29 (`relaying`), aid L15 (`delivery`). Unlisted: tend L25 (`claim`).

Observations (not counted): gossip uses `hold` as possess (L29, L31, L49, L71) and as keep-unsent (L53, ontology `held`); `volunteer` L9 lists `idle`, `adopt` L9 lists `compaction` and `wake`, `spread-around` and `ask-around` list `push` and `pull`, each used only in the description.

## 7. Verdicts and counts
| skill | verdict |
|---|---|
| gossip | CONFORMS |
| ask-around | CONFORMS |
| spread-around | CONFORMS |
| quote | 2 violations |
| vouch | CONFORMS |
| adopt | CONFORMS |
| tend | 1 violation |
| aid | 1 violation |
| volunteer | CONFORMS |
| heartbeat | CONFORMS (+4 extra edges) |

Total 4 violations (round 3: 4; round 2: 10; round 1: 46); seven skills conform.

## Summary
All three round-3 skill findings are fixed, leaving seven skills conforming; heartbeat's four extra edges in its L23 prompt are the one carry-over. The sense check you asked for found three wrong-sense uses of listed terms (quote L19 `claim` for a relayed ruling, quote L25 and L29 `relaying` for a ruling that is not a received gossip, aid L15 `delivery` for handing over a file) plus one unlisted term missed in earlier rounds (tend L25 `claim`). Counts: gossip 0, ask-around 0, spread-around 0, quote 2, vouch 0, adopt 0, tend 1, aid 1, volunteer 0, heartbeat 0.
