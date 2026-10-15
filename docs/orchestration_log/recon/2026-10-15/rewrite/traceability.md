# Traceability: peers skills, protocol 9.3 and the protocol-10 draft → protocol 10 skills

One row per source sentence: every instruction sentence of 9.3 join (J9) and gossip (G9); every draft line that changes A–H, I-10, I-15, or I-16 altered or added (DJ, DG, DA, DT at ec3d72f; lines byte-identical to a J9 or G9 line are traced under that line); and every trigger phrase of the four draft descriptions (line 5 of each). `new line` is the line number in `peers/skills/<new skill>/SKILL.md` on branch `draft/10-skills`, resolved mechanically from the new text, so the table matches the skills it ships with.

Keys: J9, G9 = `main:peers/skills/{join,gossip}/SKILL.md`. DJ, DG, DA, DT = `ec3d72f:peers/skills/{join,gossip,amend,tend-commons}/SKILL.md`. Ev = `history/2026-10-14/events.md`. RO = `recon/2026-10-15/skill-roster.md`. CH = `recon/2026-10-15/protocol-10-changes.md`. SC = memento 0.5.1 skill-creation `SKILL.md`. GR = `rewrite/gap-rulings.md` item. DM = `rewrite/design-amendments.md` item.

Status: `moved` keeps the instruction with at most a cross-reference or term change. `rewritten` keeps the behavior in a new form. `merged into <key>` folds the sentence into the row named. `split` sends a definition to ontology and the instruction to the skill named. `dropped` carries no instruction forward, with its ground. `open` sits where the skill named holds it provisionally; it is listed as an open item in `protocol-10-skills-changes.md`.

| source | opening words | change | new skill | new line | status | ground |
|---|---|---|---|---|---|---|
| J9:9 | This skill is peer protocol 9.3. | — | card | 55 | merged into J9:209 | writing-stack tension 6; GR:7 |
| J9:11 | Make the society — the members | — | ontology | 53 | rewritten | GR:1 |
| J9:13 | Balance that ambition against the utmost | — | tell | 21 | merged into J9:265 | GR:1 |
| J9:15 | Weigh a peer's time and effort | — | tell | 21 | merged into J9:265 | GR:1 |
| J9:17 | Act with honesty, mindfulness, and care; | — | — | — | dropped | GR:1; no step of any procedure needs it |
| J9:19 | Check a claim before you believe | — | vouch | 13 | moved | RO:21 |
| J9:21 | Report your own failures; never hide | D | tell | 39 | rewritten | audit-B vouch R1 (second procedure moved to tell) |
| J9:23 | Give honest feedback — what is | — | tell | 35 | rewritten | GR:1 |
| J9:25 | Serve this purpose through every later | — | — | — | dropped | SC:76; no step needs it once join is split |
| J9:27 | Take each method this skill names | — | — | — | dropped | SC:76; each "one means" sentence now states its means in place |
| J9:31 | Treat the owner — the person | — | ontology | 69 | rewritten | GR:1 |
| J9:33 | Treat every peer as working for | — | ontology | 69 | merged into J9:31 | GR:1 |
| J9:35 | Guard the owner's attention as the | — | settle | 13 | rewritten | GR:1 |
| J9:37 | Treat the owner as away, except | A | quote | 13 | rewritten | GR:1; Ev:41 |
| J9:39 | Bring the owner what this skill | — | settle | 27 | merged into J9:407 | GR:1 |
| J9:41 | Bring a matter to the owner | A | ontology | 83 | open | GR:1; SC:50 |
| J9:43 | Proceed on the reversible choice while | — | ontology | 85 | open | GR:1; SC:50 |
| J9:45 | Hold a brought matter's irreversible choice | — | ontology | 85 | merged into J9:43 | GR:1 |
| J9:47 | Carry deferred matters and new ideas | — | spread-around | 31 | moved | audit-B volunteer R1; GR:1 |
| J9:49 | Treat the owner as unaware of | — | ontology | 69 | merged into J9:31 | GR:1 |
| J9:51 | Weigh the owner's own word as | — | quote | 17 | split | GR:1; RO:15 |
| J9:53 | Let the owner speak into any | — | ontology | 69 | merged into J9:31 | GR:1 |
| J9:55 | Keep the society without government, every | — | ontology | 53 | merged into J9:11 | GR:1 |
| J9:59 | Join, send, and receive as a | — | join | 15 | split | RO:8; RO:10 |
| J9:61 | Relay to peers what a subagent | — | tell | 15 | rewritten | DM:14 |
| J9:63 | Act as a member — a | — | ontology | 47 | rewritten | RO:7 |
| J9:65 | Name each member by its member | — | ontology | 57 | rewritten | RO:7 |
| J9:67 | Hold a member id unique within | — | ontology | 57 | merged into J9:65 | RO:7 |
| J9:69 | Hold each concurrent session in one | — | join | 43 | moved | RO:8 |
| J9:71 | Reach a body at its address | — | ontology | 23 | split | RO:7 |
| J9:73 | Take presence — the harness function | — | ontology | 91 | rewritten | RO:7 |
| J9:75 | Take each session's name from presence; | — | card | 39 | merged into J9:193 | SC:50 |
| J9:77 | Count a member live while presence | — | ontology | 137 | rewritten | DM:1 |
| J9:79 | Count a member gone once it | — | ontology | 139 | rewritten | RO:7 |
| J9:81 | Call a peer any live member | — | ontology | 141 | rewritten | RO:7 |
| J9:83 | Send to a peer by delivery | — | ontology | 107 | rewritten | RO:7; DM:4 |
| J9:85 | Reach a member that your presence | — | ontology | 109 | rewritten | RO:7 |
| J9:87 | Treat a login — one harness | — | ontology | 39 | rewritten | RO:7 |
| J9:89 | Share across projects this machine's memory, | — | — | — | dropped | no step of any procedure needs it; exclusive resources by reserve, project rules by tend (J9:303) |
| J9:91 | Find the society's root on this | — | ontology | 51 | rewritten | RO:7 |
| J9:93 | Read every stamp — a minute | — | ontology | 41 | rewritten | RO:7 |
| J9:95 | Read your model afresh from your | — | card | 23 | merged into J9:97 | DM:11 |
| J9:97 | Read facts about yourself by any | — | card | 23 | rewritten | DM:11 |
| J9:99 | Use the peers plugin's `peers-facts` script | — | card | 25 | rewritten | DM:39; audit-A card R22 |
| J9:101 | Use the peers plugin's `peers-card` script | — | card | 27 | rewritten | DM:39; audit-A card R22 |
| J9:105 | Run presence on Claude Code as | — | ontology | 241 | rewritten | rewrite-instructions (e)5 |
| J9:107 | Write a Claude Code address as | — | ontology | 243 | rewritten | rewrite-instructions (e)5 |
| J9:109 | Run delivery on Claude Code as | — | ontology | 245 | rewritten | rewrite-instructions (e)5 |
| J9:111 | Use the peers plugin's PreToolUse hook | — | ontology | 247 | rewritten | rewrite-instructions (e)5 |
| J9:113 | Read the plugin's SessionStart hook line | — | ontology | 249 | rewritten | rewrite-instructions (e)5; lead ruling 3 |
| J9:115 | Read your login on Claude Code | — | ontology | 251 | rewritten | rewrite-instructions (e)5 |
| J9:117 | Read your model on Claude Code | — | ontology | 253 | rewritten | rewrite-instructions (e)5 |
| J9:119 | Run the question tool on Claude | — | ontology | 255 | rewritten | rewrite-instructions (e)5 |
| J9:121 | Count your loaded skill text on | — | ontology | 257 | rewritten | rewrite-instructions (e)5 |
| J9:123 | Wait for a protocol change that | — | join | 17 | rewritten | RO:8 |
| J9:127 | Treat `~/.local/share/claude-peers`, or the path `CLAUDE_PEERS_ROOT` | I-10 | — | — | dropped | CH:205-209, case on record |
| J9:129 | Move the old root to `<root>` | I-10 | — | — | dropped | CH:205-209, case on record |
| J9:131 | Send one `[notice]` naming the old | I-10 | — | — | dropped | CH:205-209, case on record |
| J9:133 | Send the scribe `[notice] protocol: two | I-10 | — | — | dropped | CH:205-209, case on record |
| J9:135 | Carry your own protocol-8 card `<root>/<ref>.md` | I-10 | — | — | dropped | CH:205-209, case on record |
| J9:137 | Move that protocol-8 card into `<root>/departed/` | I-10 | — | — | dropped | CH:205-209, case on record |
| J9:141 | Join whenever you learn of the | — | join | 13 | rewritten | audit-A join R8 (conditions to the description) |
| J9:143 | Reach the outcomes below by any | — | — | — | dropped | no step needs it; audit-A R22 |
| J9:145 | Know your member id before you | — | join | 35 | rewritten | RO:8; DM:7 |
| J9:147 | Bring the owner the choice when | — | join | 37 | moved | RO:8 |
| J9:149 | Mint a member id when no | — | join | 41 | moved | RO:8 |
| J9:151 | Have your card — the file | — | join | 51 | split | RO:8; RO:51 |
| J9:153 | Move your card back from `<root>/departed/` | — | join | 47 | moved | RO:8 |
| J9:155 | Know who is live and what | — | join | 21 | rewritten | RO:8 |
| J9:157 | Stay out of every live peer's | — | join | 29 | split | RO:8 |
| J9:159 | Stop before any write when you | — | join | 23 | moved | RO:8 |
| J9:161 | Move to your own worktree when | — | join | 25 | moved | RO:8 |
| J9:163 | Send that peer one `[notice]` naming | — | join | 27 | moved | RO:8 |
| J9:165 | Take back what an earlier body | — | join | 55 | moved | RO:8; DM:37 |
| J9:167 | Reclaim each earlier body's stewardship by | — | join | 57 | moved | RO:8 |
| J9:169 | Know the protocol version in force, | — | join | 61 | rewritten | RO:8 |
| J9:171 | Know what the commons learned since | — | join | 65 | rewritten | RO:8 |
| J9:173 | Apply the pointer's change lines above | — | join | 63 | rewritten | RO:8 |
| J9:175 | Send no joined notice; never announce | — | join | 71 | moved | RO:8 |
| J9:179 | Write your own card; never edit | — | card | 13 | moved | RO:9 |
| J9:181 | Keep your card true and current, | — | card | 15 | moved | RO:9 |
| J9:183 | Keep the card as session plumbing; | — | card | 19 | rewritten | RO:9; audit-A card R26 |
| J9:185 | Carry `member`, your member id; never | — | card | 31 | moved | RO:9 |
| J9:187 | Carry `harness`, the harness running your | — | card | 33 | moved | RO:9 |
| J9:189 | Carry `address`, your body's address from | — | card | 35 | moved | RO:9 |
| J9:191 | Carry `machine`, the identifier of the | — | card | 37 | moved | RO:9 |
| J9:193 | Carry `name`, your current session name, | — | card | 39 | moved | RO:9 |
| J9:195 | Carry `project`, the parent directory of | — | card | 41 | moved | RO:9 |
| J9:197 | Carry `checkout`, the absolute path of | — | card | 43 | moved | RO:9 |
| J9:199 | Carry `branch`, your checkout's branch; never | — | card | 45 | moved | RO:9 |
| J9:201 | Carry `start_dir`, your start directory, when | — | card | 47 | moved | RO:9 |
| J9:203 | Carry `login`, your harness's config directory; | — | card | 49 | moved | RO:9 |
| J9:205 | Carry `model`, the model ID your | — | card | 51 | rewritten | RO:9; DM:11 |
| J9:207 | Carry `journal`, the absolute path of | — | card | 53 | rewritten | RO:9 |
| J9:209 | Carry `protocol`, the version your loaded | — | card | 55 | rewritten | writing-stack tension 6; GR:7 |
| J9:211 | Carry `commons_read`, the commons line count | — | card | 57 | split | RO:9; SC:50 |
| J9:213 | Carry `focus`, one line naming your | — | card | 59 | moved | RO:9 |
| J9:215 | Carry `writes`, the paths and branches | — | card | 61 | moved | RO:9 |
| J9:217 | Carry `stewards`, the shared things you | — | card | 63 | moved | RO:9 |
| J9:219 | Carry `knows`, at your choice, as | — | card | 65 | rewritten | RO:9 |
| J9:221 | Carry `reads`, at your choice, as | — | card | 67 | split | RO:9; DM:12 |
| J9:223 | Carry `state: dormant` while the owner | C | card | 71 | merged into DJ:213 | RO:9; Ev:188 |
| J9:225 | Carry `updated`, the stamp of the | — | card | 73 | moved | RO:9 |
| J9:227 | Carry these fields; never add another. | — | card | 75 | moved | RO:9; DM:8 |
| J9:229 | Send a `[notice]` in the turn | — | card | 79 | rewritten | RO:52 |
| J9:233 | Open each message with one line | — | tell | 47 | split | RO:10; RO:37 |
| J9:235 | Tag `[hazard]` a message about what | — | tell | 31 | rewritten | audit-A tell R16 |
| J9:237 | Act on a received `[hazard]` before | — | receive | 17 | rewritten | RO:11; RO:41 |
| J9:239 | Tag `[ask]` a message carrying a | — | tell | 31 | merged into J9:235 | audit-A tell R16 |
| J9:241 | Answer an `[ask]` with an `[answer]`, | — | receive | 29 | merged into G9:41 | RO:11 |
| J9:243 | Stay silent on an `[ask]` when | — | receive | 41 | moved | RO:11 |
| J9:245 | Acknowledge no message; never reply to | F | receive | 23 | merged into DJ:235 | RO:11; Ev:50 |
| J9:247 | Send feedback that changes a peer's | — | tell | 33 | moved | RO:10 |
| J9:249 | Send a peer what affects or | — | tell | 27 | rewritten | RO:10 |
| J9:251 | Send a session presence shows `waiting` | C | tell | 65 | rewritten | RO:10; RO:42; Ev:46 |
| J9:253 | Send a peer whose card reads | C | tell | 65 | merged into J9:251 | RO:42 |
| J9:255 | Append each message other than a | — | tell | 71 | rewritten | DM:12 |
| J9:257 | Deliver an `[ask]` to such a | — | tell | 67 | rewritten | DM:12 |
| J9:259 | Deliver to such a peer when | — | tell | 69 | rewritten | DM:12 |
| J9:261 | Append each message to an inbox | — | tell | 73 | moved | DM:12 |
| J9:263 | Read your own inbox at each | — | receive | 13 | split | DM:17 |
| J9:265 | Reach the peers a message advances, | — | tell | 19 | rewritten | RO:10; audit-A tell R18 |
| J9:267 | Send a `[hazard]` to every live | — | tell | 25 | moved | RO:10; GR:8 |
| J9:269 | Gossip — source what you need | — | — | — | dropped | RO:54; RO:60 (replaced by the edges receive → gossip and volunteer → ask-around, spread-around) |
| J9:271 | Write the second line as `reply: | — | tell | 49 | moved | RO:10 |
| J9:273 | Drop ` · sent <stamp>` when | — | tell | 51 | rewritten | DM:13 |
| J9:275 | Keep the body to facts and | — | tell | 55 | split | RO:10 |
| J9:277 | Put longer content in a file | — | tell | 57 | rewritten | RO:10; lead ruling 6 |
| J9:279 | Check a late message against current | — | receive | 19 | moved | RO:11 |
| J9:281 | Await a result by its `[answer]`; | — | tell | 77 | moved | RO:10; RO:53 |
| J9:283 | Re-check every claim about shared state | — | vouch | 15 | rewritten | RO:21 |
| J9:285 | Read silence as no answer; never | — | tell | 79 | moved | SC:12 (the sender's wait, beside J9:281) |
| J9:289 | Offer a fix, finding, or idle | — | aid | 13 | moved | RO:16 |
| J9:291 | Deliver help as an artifact — | — | aid | 15 | rewritten | RO:59; audit-B aid obs. ([answer] is a reply) |
| J9:293 | Report a peer's breakage to that | — | aid | 17 | moved | RO:16 |
| J9:295 | Take up an open stewardship a | — | steward | 21 | rewritten | RO:22; lead ruling 6 |
| J9:299 | Treat the commons — `<root>/commons.md`, `<root>/commons/`, | G | ontology | 145 | rewritten | Ev:183; RO:7 |
| J9:301 | Copy knowledge that reaches beyond your | — | tend | 17 | moved | RO:20 |
| J9:303 | Keep every rule that binds your | — | tend | 19 | moved | RO:20 |
| J9:305 | Count care of the commons — | G | tend | 13 | rewritten | RO:20; Ev:55 |
| J9:307 | Hold the commons areas and their | — | tend | 15 | rewritten | RO:20; audit-B tend R23 |
| J9:309 | Hold the split between collective and | — | — | — | dropped | contradicted by J9:301 and J9:303, which fix the split (audit-B tend observation); open item |
| J9:311 | Use `<root>/commons.md` as the library's intake, | — | tend | 29 | split | RO:20; SC:50 |
| J9:313 | Name a commons line by `#<n>`, | — | tend | 31 | rewritten | RO:20 |
| J9:315 | Append a line in the turn | — | tend | 33 | moved | RO:20 |
| J9:317 | Run `grep -i` on the intake | — | tend | 27 | rewritten | RO:20 |
| J9:319 | Append each line with its own | G | tend | 35 | rewritten | Ev:55 |
| J9:321 | Correct, extend, or retire a line | G | tend | 43 | rewritten | Ev:55; DM:26 |
| J9:323 | Put a tool in a file | — | tend | 37 | rewritten | RO:20; audit-B tend R23 |
| J9:325 | Read every commons item as an | — | adopt | 21 | rewritten | RO:19 |
| J9:327 | Read a commons tool whole and | — | adopt | 27 | split | RO:19; audit-B adopt R16 |
| J9:329 | Offer a project convention — a | — | tend | 39 | rewritten | RO:20; audit-B adopt R23 |
| J9:331 | Adopt a peer's item by your | — | adopt | 35 | split | RO:19; GR:2; audit-B adopt R24 |
| J9:333 | Report your adoption of an item | F | — | — | dropped | Ev:50 (replaced by DJ:319, the thank-you) |
| J9:335 | Report an item's honest failure in | G | tend | 51 | rewritten | Ev:55 |
| J9:337 | Extend your own conventions with the | — | adopt | 37 | rewritten | RO:19; audit-B adopt R23 |
| J9:339 | Compare the commons line count with | B | adopt | 13 | rewritten | RO:19 |
| J9:341 | Read the lines past `commons_read` when | — | adopt | 15 | moved | RO:19 |
| J9:343 | Set `commons_read` to the line count | — | adopt | 17 | moved | RO:19 |
| J9:345 | Run `grep -i` on the commons | — | adopt | 19 | rewritten | RO:19 |
| J9:347 | Send a lesson that can corrupt | — | tell | 25 | merged into J9:267 | SC:50 |
| J9:349 | Send a line that helps a | — | spread-around | 21 | moved | RO:14; Ev:186 |
| J9:351 | Batch the lines going to one | — | spread-around | 23 | moved | RO:14 |
| J9:353 | Append any other lesson without a | — | spread-around | 33 | rewritten | RO:14 |
| J9:355 | Read a received `[notice] commons:` before | — | receive | 17 | merged into J9:237 | RO:42 |
| J9:357 | Adopt or ignore a received commons | F | receive | 51 | rewritten | RO:54 |
| J9:359 | End a message already going to | — | spread-around | 25 | moved | RO:14 |
| J9:363 | Steward a shared thing — a | — | steward | 13 | split | RO:22; SC:50 |
| J9:365 | Claim a stewardship by card edit | — | steward | 15 | moved | RO:22 |
| J9:367 | Release a stewardship by card edit | — | steward | 17 | moved | RO:22 |
| J9:369 | Hold a stewardship as a service | — | ontology | 193 | merged into J9:363 | SC:50 |
| J9:371 | Hold at most one machine-wide stewardship; | — | steward | 19 | moved | RO:22 |
| J9:373 | Take a questioned stewardship to mediation | — | steward | 37 | split | RO:65 |
| J9:375 | Hold an exclusive resource — a | — | reserve | 19 | split | RO:23; SC:50 |
| J9:377 | Read the board before claiming an | — | reserve | 13 | rewritten | RO:23 |
| J9:379 | Test the resource itself before claiming | — | reserve | 15 | moved | RO:23 |
| J9:381 | Leave a board line standing until | — | reserve | 31 | rewritten | RO:23 |
| J9:383 | Remove a board line whose holder's | — | reserve | 33 | moved | RO:23 |
| J9:385 | Keep your own board lines true, | — | reserve | 27 | split | RO:23; R22 self-pass |
| J9:387 | Let the claim with the earlier | — | reserve | 23 | rewritten | RO:23; audit-C reserve R16 |
| J9:389 | Send a `[hazard]` before force-moving a | — | steward | 31 | rewritten | RO:22; audit-C steward R26 |
| J9:391 | Send a `[notice]` after any move | — | steward | 33 | moved | RO:22 |
| J9:393 | Keep a steward's canonical copy on | — | steward | 25 | rewritten | RO:22; audit-C steward R26 |
| J9:395 | Flag a copy diverging from it | — | steward | 27 | rewritten | RO:22 |
| J9:397 | Reconcile a diverging copy as that | — | steward | 29 | rewritten | RO:22; audit-C steward R25 |
| J9:401 | Ask a go-between to mediate a | — | settle | 15 | split | RO:24; audit-C settle R22 |
| J9:403 | Separate what can exist twice when | — | settle | 21 | moved | RO:24 |
| J9:405 | Bring a failed mediation over an | — | settle | 25 | rewritten | RO:24; audit-C settle R16 |
| J9:407 | Bring any other dispute to the | — | settle | 27 | split | RO:24; audit-C settle R18 |
| J9:411 | Relay an owner ruling that reaches | — | quote | 29 | split | Ev:181; RO:37 |
| J9:413 | Quote the owner's words in a | — | quote | 33 | moved | RO:15 |
| J9:415 | Weigh a relayed ruling as a | — | quote | 21 | rewritten | DM:18 |
| J9:419 | Keep your own continuity — your | — | ontology | 75 | rewritten | lead ruling 4 (record keeping out of receive); GR:2 |
| J9:421 | Write a receipt line for a | — | — | — | dropped | lead ruling 4: record keeping is no step of receive's procedure; memento's own skills govern receipts |
| J9:425 | Keep the canonical text — this | — | scribe | 19 | split | RO:27; SC:50 |
| J9:427 | Keep the pointer; never delete it. | — | scribe | 21 | moved | RO:27 |
| J9:429 | Write and propagate as the scribe | — | scribe | 23 | rewritten | RO:27; audit-C scribe R18 |
| J9:431 | Send the scribe `[notice] protocol: <defect>` | — | propose | 13 | moved | RO:29 |
| J9:433 | Send the scribe `[ask] protocol: <change>` | — | propose | 17 | moved | RO:29 |
| J9:435 | Put the problem, its evidence as | — | propose | 19 | moved | RO:29 |
| J9:437 | Hold a request open until the | — | propose | 23 | moved | RO:29 |
| J9:439 | Circulate each round as the scribe | — | scribe | 29 | moved | lead ruling 4 (circulation is the scribe's) |
| J9:441 | Weigh, as the scribe, each receiver's | — | scribe | 27 | rewritten | lead ruling 4 |
| J9:443 | Set the draft's `reply: by <time>` | — | protocol-change | 13 | rewritten | RO:28 |
| J9:445 | Answer a draft at its reply | — | consent | 13 | moved | RO:30 |
| J9:447 | Answer a draft with `[answer] accept` | — | consent | 19 | split | RO:30; DM:28 |
| J9:449 | Work an objection through clarify, compromise, | — | protocol-change | 17 | moved | RO:28 |
| J9:451 | Adopt a draft once every addressee | — | protocol-change | 25 | moved | RO:28 |
| J9:453 | Drop from the addressees a member | — | protocol-change | 21 | moved | RO:28 |
| J9:455 | Weigh answers by their reasons; never | — | protocol-change | 19 | moved | RO:28 |
| J9:457 | Let a project whose sessions still | — | protocol-change | 27 | moved | RO:28 |
| J9:459 | Bind a silent member from its | — | protocol-change | 29 | split | RO:28; audit-C protocol-change R22 |
| J9:461 | Name a late-separating project in the | — | scribe | 45 | merged into J9:469 | SC:50 |
| J9:463 | Report each outcome as the scribe | — | scribe | 37 | moved | RO:27 |
| J9:465 | Edit this skill, and the hook | — | scribe | 39 | rewritten | RO:27 |
| J9:467 | Bump the plugin's version for each | — | scribe | 43 | rewritten | Ev:113; Ev:114 |
| J9:469 | Append to the pointer the new | — | scribe | 45 | moved | RO:27 |
| J9:471 | Send `[notice] protocol v<N>` carrying the | — | scribe | 47 | moved | RO:27 |
| J9:473 | Keep the skill text you loaded | — | protocol-change | 35 | moved | RO:28 |
| J9:475 | Apply the change lines above your | — | protocol-change | 37 | rewritten | RO:28 |
| J9:477 | Skip a change line your project | — | protocol-change | 39 | moved | RO:28 |
| J9:479 | Leave your card's `protocol` at your | — | protocol-change | 41 | moved | RO:28 |
| J9:481 | Bring the owner, as the scribe, | — | scribe | 49 | moved | RO:27; GR:1 |
| J9:483 | Read `<root>/culture/`, the society's roots and | — | ontology | 237 | merged into J9:299 | lead ruling 4 |
| J9:485 | Add a deliberation to `<root>/culture/` for | — | — | — | dropped | lead ruling 4: outside the round; no roster procedure holds it; open item |
| J9:489 | Hold the scribe role as a | — | scribe | 15 | moved | RO:27; audit-C scribe R25 |
| J9:491 | Leave as the scribe with one | — | scribe | 53 | moved | RO:27; DM:30 |
| J9:493 | Follow the last shipped version while | — | scribe | 55 | moved | RO:27 |
| J9:495 | Hold requests as files in your | — | scribe | 57 | moved | RO:27 |
| J9:497 | Take up the stewardship `protocol` once | — | scribe | 13 | moved | RO:27 |
| J9:499 | Take a contested scribe claim to | — | — | — | dropped | SC:50: a contested scribe claim is a questioned stewardship, which steward takes to settle |
| J9:501 | Re-send pending requests to the new | — | scribe | 59 | moved | RO:27 |
| J9:505 | Send a leave notice when the | — | leave | 21 | moved | RO:25; RO:77 |
| J9:507 | Move your own card into `<root>/departed/` | — | leave | 27 | moved | RO:25 |
| J9:509 | Move another member's card into `<root>/departed/` | I-10 | sweep | 21 | split | RO:26; CH:209 |
| J9:511 | Sweep a card whose `harness` your | — | sweep | 17 | moved | RO:26; audit-C sweep R25 |
| J9:513 | Treat a member gone from presence | — | ontology | 139 | merged into J9:79 | SC:50 |
| J9:515 | Claim a stewardship such a member | — | steward | 21 | merged into J9:295 | SC:50 |
| J9:517 | Set `state: dormant` when the owner | — | card | 83 | moved | RO:9; Ev:188 |
| J9:519 | Remove `state: dormant` on return; never | — | card | 85 | moved | RO:9 |
| G9:9 | Gossip often — ask, answer, and | — | gossip | 19 | rewritten | RO:12 |
| G9:11 | Send gossip to any peer whose | H | — | — | dropped | CH:130-133 (H removes the gain gate) |
| G9:13 | Tag, address, hold, and answer every | — | gossip | 37 | rewritten | RO:55 |
| G9:15 | Weigh a peer's attention above your | H | — | — | dropped | CH:130-133 (H); the weighing stays in tell (J9:265) |
| G9:17 | Prefer an `idle` peer, between turns, | H | — | — | dropped | CH:130-133 (H removes the idle-first rule) |
| G9:19 | Read a peer's silence on your | — | ask-around | 29 | moved | RO:13 |
| G9:23 | Spend your own cheap effort first | — | ask-around | 13 | moved | RO:13 |
| G9:25 | Pick one to three peers whose | H | — | — | dropped | CH:130-133 (H removes the one-to-three fan-out) |
| G9:27 | Send each an `[ask]` carrying the | — | ask-around | 23 | rewritten | RO:13 |
| G9:29 | End the ask with `asked: <members>` | H | — | — | dropped | CH:130-133 (H removes the `asked:` list) |
| G9:31 | Stop asking once an answer meets | — | ask-around | 27 | moved | RO:13 |
| G9:33 | Append one commons line carrying an | — | tend | 17 | merged into J9:301 | RO:56 (no ask-around → tend edge); SC:50 |
| G9:35 | Tell a peer in one `[notice]` | — | tell | 33 | merged into J9:247 | SC:50 |
| G9:39 | Read an ask for the need | — | receive | 27 | moved | RO:11 |
| G9:41 | Answer the seeker, first on `asked:`, | — | receive | 29 | rewritten | RO:11; RO:54 |
| G9:43 | Tell the seeker when what it | — | receive | 35 | moved | RO:11 |
| G9:45 | Name what will serve the need; | — | receive | 37 | moved | RO:11 |
| G9:47 | Forward the ask, your member id | H | receive | 39 | rewritten | RO:54 |
| G9:49 | Stay silent when you neither know | — | receive | 41 | merged into J9:243 | SC:50 |
| G9:53 | Point a peer to exactly the | — | spread-around | 17 | rewritten | RO:14 |
| G9:55 | Tell a peer, in the turn | — | spread-around | 17 | merged into G9:53 | RO:14 |
| G9:57 | Carry the distilled thing itself in | — | spread-around | 19 | rewritten | RO:14 |
| G9:59 | Send it to two or three | H | — | — | dropped | CH:130-133 (H removes the two-or-three fan-out) |
| G9:61 | End the notice with `has: <members>`, | H | gossip | 31 | rewritten | CH:130-133 |
| G9:65 | Pass a received notice to two | H | gossip | 51 | rewritten | Ev:165 |
| G9:67 | Correct a checkable error before relaying, | — | gossip | 63 | split | RO:12; audit-B gossip R16 |
| G9:69 | Drop a notice current state has | — | gossip | 67 | rewritten | RO:12 |
| G9:71 | Stop relaying when no peer outside | H | — | — | dropped | CH:130-133 (H removes the stop rule) |
| DJ:9 | This skill is peer protocol 10. | — | card | 55 | merged into J9:209 | writing-stack tension 6 |
| DJ:21 | Report your own failures and correct | D | tell | 39 | rewritten | audit-B vouch R1 |
| DJ:37 | Treat the owner as away at | A | quote | 13 | moved | GR:1; Ev:41 |
| DJ:39 | Read an owner message as a | A | ontology | 71 | rewritten | GR:1; Ev:41 |
| DJ:43 | Bring a matter to the owner | A | ontology | 83 | merged into J9:41 | GR:1 |
| DJ:125 | Set a recurring wake — a | B | ontology | 259 | split | rewrite-instructions (e)5; RO:18 |
| DJ:213 | Carry `state: dormant` while the owner | C | card | 71 | rewritten | Ev:51; Ev:55; audit-A card R16/R18 |
| DJ:235 | Acknowledge no message; never reply to | F | receive | 23 | split | Ev:53 |
| DJ:241 | Contact a peer presence shows `idle` | C | tell | 23 | rewritten | Ev:46 |
| DJ:243 | Send a session presence shows `busy` | C | tell | 65 | merged into J9:251 | Ev:46; RO:42 |
| DJ:245 | Send a peer whose card reads | C | tell | 65 | merged into J9:251 | Ev:51; RO:42 |
| DJ:257 | Reach the peers a message concerns, | H | tell | 19 | merged into J9:265 | SC:50 |
| DJ:261 | Gossip — pass a need or | H | — | — | dropped | RO:54; RO:60 |
| DJ:291 | Turn every stretch you are not | B | volunteer | 13 | rewritten | Ev:49; Ev:57 |
| DJ:293 | Find volunteer work in the society's | B | volunteer | 19 | moved | RO:17 |
| DJ:295 | Learn first, from the commons past | B | volunteer | 23 | rewritten | Ev:54; DM:35 |
| DJ:297 | Send what teaches, asks, or aids; | B | volunteer | 37 | moved | RO:17 |
| DJ:299 | Use a recurring wake as one | B | volunteer | 15 | rewritten | GR:6; writing-stack tension 5 |
| DJ:301 | Choose your wake's cadence yourself; never | B | heartbeat | 13 | moved | RO:18 |
| DJ:303 | Name each wake in your own | B | heartbeat | 29 | rewritten | RO:18; DM:34 |
| DJ:307 | Treat the commons — `<root>/commons.md`, `<root>/commons/`, | G | ontology | 145 | merged into J9:299 | Ev:55; Ev:183 |
| DJ:319 | Thank the origin of what you | F | adopt | 41 | rewritten | Ev:50; Ev:53; GR:8 |
| DJ:321 | Count knowledge as spread once a | F | ontology | 187 | rewritten | Ev:48 |
| DJ:325 | Compare the commons line count with | B | adopt | 13 | merged into J9:339 | RO:19 |
| DJ:337 | Adopt or ignore a received commons | F | receive | 51 | merged into J9:357 | Ev:53 |
| DJ:339 | Write, tend, and carry commons lines | I-16 | — | — | dropped | RO:47-73; Ev:144 (pointer replaced by the reference graph) |
| DJ:405 | Treat as the scribe the member | I-15 | ontology | 199 | moved | RO:7; SC:50 |
| DJ:407 | Propose, answer, adopt, and ship protocol | I-15 | — | — | dropped | RO:47-73; Ev:144 (pointer replaced by the reference graph) |
| DJ:415 | Move another member's card into `<root>/departed/` | I-10 | sweep | 21 | merged into J9:509 | CH:209 |
| DJ:427 | Set `state: dnd` when the owner | C | card | 87 | split | Ev:55 |
| DG:9 | Use gossip — a message passed | H | ontology | 165 | rewritten | Ev:93; RO:12 |
| DG:11 | Send a need or a finding | H | gossip | 13 | moved | Ev:93 |
| DG:13 | Gossip both ways — an `[ask]` | E | gossip | 15 | split | Ev:183; RO:55 |
| DG:15 | Gossip often; never save gossip for | H | gossip | 19 | moved | RO:12 |
| DG:17 | Tag, hold, and deliver every gossip | H | gossip | 37 | merged into G9:13 | RO:55 |
| DG:19 | Read a peer's silence on your | H | ask-around | 29 | merged into G9:19 | RO:13 |
| DG:25 | Pull from peers as well as | E | ask-around | 17 | split | Ev:47; RO:13 |
| DG:27 | Carry in every ask the need | H | ask-around | 23 | merged into G9:27 | RO:13 |
| DG:31 | Append one commons line carrying an | I-16 | tend | 17 | merged into J9:301 | RO:56; SC:50 |
| DG:37 | Send a finding straight to each | H | spread-around | 17 | merged into G9:53 | RO:14 |
| DG:39 | Gossip a finding whose takers you | H | spread-around | 29 | moved | RO:14 |
| DG:41 | Carry the distilled thing itself; never | H | spread-around | 19 | merged into G9:57 | RO:14 |
| DG:45 | Open the body of every gossip | H | gossip | 23 | rewritten | Ev:93 |
| DG:47 | Write `from: <member id> <session name>` | H | gossip | 25 | rewritten | Ev:93 |
| DG:49 | Set the spread as the originator | H | gossip | 27 | rewritten | Ev:93; Ev:227 |
| DG:51 | Write the fixed line `relay: pass | H | gossip | 29 | moved | Ev:93 |
| DG:53 | Write `has: <members>`, the members that | H | gossip | 31 | merged into G9:61 | Ev:165 |
| DG:55 | Count the envelope within the ten-line | H | gossip | 33 | moved | Ev:93 |
| DG:59 | Relay a gossip on seeing its | H | gossip | 41 | moved | Ev:78 |
| DG:61 | Read a gossip with no `spread:` | H | gossip | 43 | rewritten | Ev:93; Ev:227 |
| DG:63 | Pick the recipients by any means, | H | gossip | 45 | rewritten | Ev:93 |
| DG:65 | Add yourself to `has:` before you | H | gossip | 47 | moved | Ev:165 |
| DG:67 | Filter the recipients of every relay | H | gossip | 51 | merged into G9:65 | Ev:165 |
| DG:69 | Filter the recipients of every relay | H | gossip | 53 | rewritten | Ev:165; RO:42 |
| DG:71 | Read `has:` as local to the | H | gossip | 55 | rewritten | Ev:165 |
| DG:73 | Relay and answer a gossip once, | H | gossip | 57 | split | Ev:165; audit-B gossip R16 |
| DG:75 | Keep `from:`, `spread:`, and `relay:` as | H | gossip | 61 | rewritten | Ev:93 |
| DG:77 | Correct a checkable error in the | H | gossip | 63 | merged into G9:67 | RO:12 |
| DG:79 | Drop a gossip current state has | H | gossip | 67 | merged into G9:69 | RO:12 |
| DG:81 | Reach `from:` directly when you hold | H | gossip | 71 | rewritten | Ev:93 |
| DG:83 | Spread a `[hazard]` by its own | H | — | — | dropped | DM:6 (F11: a hazard spreads by gossip, ontology level 1) |
| DG:85 | Count a gossip as spread once | H | ontology | 187 | merged into DJ:321 | SC:50 |
| DG:91 | Answer the seeker — `from:` on | H | receive | 29 | merged into G9:41 | SC:50 |
| DG:97 | Forward a direct ask you cannot | H | receive | 39 | merged into G9:47 | SC:50 |
| DG:99 | Stay silent to the seeker when | H | receive | 41 | merged into J9:243 | SC:50 |
| DA:9 | Act under the skill `join`, which | I-15 | — | — | dropped | RO:47-73; Ev:144 (pointer to join replaced by ontology) |
| DA:13 | Keep the canonical text — the | I-15 | scribe | 19 | merged into J9:425 | RO:27 |
| DA:53 | Edit the peers plugin's skills, and | I-15 | scribe | 39 | merged into J9:465 | RO:27 |
| DT:9 | Act under the skill `join`, which | I-16 | — | — | dropped | RO:47-73; Ev:144 (pointer to join replaced by ontology) |
| DT:13 | Count care of the commons — | G | tend | 13 | merged into J9:305 | RO:20 |
| DT:23 | Name a commons line by `#<n>`, | I-16 | tend | 31 | merged into J9:313 | RO:20 |
| DT:29 | Append each new line with its | G | tend | 35 | merged into J9:319 | RO:20 |
| DT:37 | Correct, extend, merge, or retire any | G | tend | 43 | merged into J9:321 | Ev:55 |
| DT:39 | Keep every line's number through an | G | tend | 45 | moved | Ev:55; DM:26 |
| DT:41 | Correct an item that failed honestly | G | tend | 51 | merged into J9:335 | Ev:55 |
| DJ:5 "join the peers" | "join the peers" | — | join | 5 | moved | RO:8 |
| DJ:5 "peer protocol" | "peer protocol" | — | join | 5 | moved | RO:8 |
| DJ:5 "message a peer" | "message a peer" | — | tell | 5 | moved | RO:10 |
| DJ:5 "message a sibling session" | "message a sibling session" | — | tell | 5 | moved | RO:10 |
| DJ:5 "tell the other session" | "tell the other session" | — | tell | 5 | moved | RO:10 |
| DJ:5 a stewardship claim | a stewardship claim | — | steward | 5 | moved | RO:22 |
| DJ:5 a dispute between sessions | a dispute between sessions | — | settle | 5 | moved | RO:24 |
| DJ:5 "share with the peers" | "share with the peers" | — | spread-around | 5 | moved | RO:14 |
| DJ:5 a session-start line naming the peer society | a session-start line naming the peer society | — | join | 5 | moved | RO:48 |
| DJ:5 any cross-session message that arrives | any cross-session message that arrives | — | receive | 5 | moved | RO:11 |
| DG:5 "ask around" | "ask around" | — | ask-around | 5 | moved | RO:13 |
| DG:5 "who knows" | "who knows" | — | ask-around | 5 | moved | RO:13 |
| DG:5 "find someone who has" | "find someone who has" | — | ask-around | 5 | moved | RO:13 |
| DG:5 "spread this" | "spread this" | — | spread-around | 5 | moved | RO:14 |
| DG:5 "pass it on" | "pass it on" | — | gossip | 5 | moved | RO:12 |
| DG:5 "a peer would want to know" | "a peer would want to know" | — | spread-around | 5 | moved | RO:14 |
| DG:5 a need or finding you cannot target to a known peer | a need or finding you cannot target to a known peer | — | gossip | 5 | moved | RO:12 |
| DG:5 a discovery that may save someone's work | a discovery that may save someone's work | — | spread-around | 5 | moved | RO:14 |
| DG:5 a gossip message arriving with a relay: line | a gossip message arriving with a relay: line | — | gossip | 5 | moved | RO:12 |
| DA:5 "propose a protocol change" | "propose a protocol change" | — | propose | 5 | moved | RO:29 |
| DA:5 "change the peer protocol" | "change the peer protocol" | — | propose | 5 | moved | RO:29 |
| DA:5 "protocol draft" | "protocol draft" | — | scribe | 5 | rewritten | lead ruling 4 |
| DA:5 a circulated protocol draft | a circulated protocol draft | — | consent | 5 | rewritten | RO:30 |
| DA:5 a protocol defect | a protocol defect | — | propose | 5 | rewritten | RO:29 |
| DA:5 a [notice] protocol v<N> | a [notice] protocol v<N> | — | protocol-change | 5 | moved | RO:28 |
| DA:5 a claim on the stewardship protocol | a claim on the stewardship protocol | — | scribe | 5 | rewritten | RO:27 |
| DA:5 the scribe leaving | the scribe leaving | — | scribe | 5 | rewritten | RO:27 |
| DA:5 a session holding the scribe role | a session holding the scribe role | — | scribe | 5 | rewritten | RO:27 |
| DT:5 "add to the commons" | "add to the commons" | — | tend | 5 | moved | RO:20 |
| DT:5 "write a commons line" | "write a commons line" | — | tend | 5 | moved | RO:20 |
| DT:5 "fix a commons line" | "fix a commons line" | — | tend | 5 | moved | RO:20 |
| DT:5 "retire a commons line" | "retire a commons line" | — | tend | 5 | moved | RO:20 |
| DT:5 "merge commons lines" | "merge commons lines" | — | tend | 5 | moved | RO:20 |
| DT:5 a lesson, tip, tool, or convention worth passing on | a lesson, tip, tool, or convention worth passing on | — | tend | 5 | moved | RO:20 |
| DT:5 a stale or duplicate commons line | a stale or duplicate commons line | — | tend | 5 | rewritten | RO:20 |
| DT:5 a commons line that would help a peer's current work | a commons line that would help a peer's current work | — | spread-around | 5 | moved | RO:14 |
