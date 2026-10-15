# Self-audit, round 6: literal pass over every sentence of the 25 peers skills

Branch `draft/10-skills`. Method, run on every body sentence (452):

1. Emphatic words: count `never|always|only|must` outside backticks with a regex over each line (column `emph`). Every sentence has exactly 1 and no frontmatter has any, which `/tmp/aoa-tools/check.py` and `/tmp/aoa-tools/literal.py` confirm.
2. Pairing: extract the first verb of the positive half and the first verb after `never` (columns `do` and `never`). Where they differ (224 sentences), I read the sentence and judged whether the prohibition forbids the same act, its omission, or its violating alternative (verdict `same`), or another concern. Four sentences failed that reading and were split or reworded before this table was written (consent 15, reserve 27, tend 51, scribe 27).
3. Compound sentences: a regex flags "and/then + verb" and ", -ing" clauses. Each flag was read; list items and appositive definitions stay, and second instructions were split. The splits are tell 39/51, gossip 15/31/43/51/55, adopt 27/39, tend 47/51, settle 23/25, sweep 13/19, propose 19, consent 23, protocol-change 29, card 15/67, join 27, and receive 31.
4. Terms (round 3): each skill's terms sentence is generated from its body by `/tmp/aoa-tools/gen_terms.py`. `peers/tests/test_terms.py` fails when a body uses an ontology term its sentence omits; a mutation check (dropping `message` from aid) made it fail.
5. Other senses (round 5): `test_no_ontology_term_is_used_in_another_sense` scans every skill's description and body, backticked text excluded, against a per-term pattern list of other-sense uses.
6. Copies: a new test, `test_no_two_skills_share_a_sentence`, asserts that no body sentence appears in two skills. It passes.
7. Edges: a script checks every "the skill `x`" and `peers:x` reference against the roster graph plus resume → join. The one extra is scribe → card, and the commons wake prompt names exactly the skills tend, ask-around, spread-around, and adopt.

Rows below give every sentence. Residuals I could not fix within the rulings are listed under each skill and counted in the report.

## adopt

Residuals: none

| line | emph | do | never | pairing | one instruction | opening |
|---|---|---|---|---|---|---|
| 9 | 1 | take | take | same | yes | Take `compaction`, `wake`, `card`, `records`, `authority check`, |
| 13 | 1 | compare | skip | same | yes | Compare the commons line count with your |
| 15 | 1 | read | reread | same | yes | Read the commons lines past `commons_read` when |
| 17 | 1 | set | set | same | yes | Set `commons_read` to the line count up |
| 19 | 1 | search | start | same | yes | Search the commons with `grep -i` before |
| 21 | 1 | read | read | same | yes | Read every commons item and every offered |
| 25 | 1 | check | adopt | same | yes | Check an item by the skill `vouch` |
| 27 | 1 | read | run | same | yes | Read a commons tool whole before you |
| 29 | 1 | run | run | same | yes | Run a commons tool once your authority |
| 33 | 1 | adopt | adopt | same | yes | Adopt an item by your own work; |
| 35 | 1 | write | leave | same | yes | Write your reason for each adoption into |
| 37 | 1 | extend | extend | same | yes | Extend your project's standing rules with the |
| 41 | 1 | thank | thank | same | yes | Thank the origin of what you adopt |
| 43 | 1 | keep | report | same | yes | Keep adoptions out of the commons; never |

## aid

Residuals: none

| line | emph | do | never | pairing | one instruction | opening |
|---|---|---|---|---|---|---|
| 9 | 1 | take | take | same | yes | Take `message`, `[notice]`, and `peer` as the |
| 13 | 1 | offer | wait | same | yes | Offer a fix, finding, or spare capacity |
| 15 | 1 | hand | hand | same | yes | Hand over help as an artifact — |
| 17 | 1 | report | leave | same | yes | Report a peer's breakage to that peer; |

## ask-around

Residuals: none

| line | emph | do | never | pairing | one instruction | opening |
|---|---|---|---|---|---|---|
| 9 | 1 | take | take | same | yes | Take `records`, `delivery`, `[ask]`, `[answer]`, `peer`, `commons`, |
| 13 | 1 | spend | ask | same | yes | Spend your own cheap effort first — |
| 17 | 1 | send | gossip | same | yes | Send a direct `[ask]` by the skill |
| 21 | 1 | gossip | leave | same | yes | Gossip an `[ask]` by the skill `gossip` |
| 23 | 1 | carry | send | same | yes | Carry in every ask the need behind |
| 27 | 1 | stop | ask | same | yes | Stop asking once an answer meets the |
| 29 | 1 | read | read | same | yes | Read a peer's silence on your ask |

## card

Residuals: none

| line | emph | do | never | pairing | one instruction | opening |
|---|---|---|---|---|---|---|
| 9 | 1 | take | take | same | yes | Take `harness`, `session`, `host`, `address`, `turn`, `skill`, |
| 13 | 1 | write | write | same | yes | Write your own card; never write another |
| 15 | 1 | keep | let | same | yes | Keep your card true and current; never |
| 17 | 1 | write | write | same | yes | Write the card as flat YAML, one |
| 19 | 1 | keep | make | same | yes | Keep the card to your session's facts |
| 23 | 1 | read | read | same | yes | Read each fact about yourself — model, |
| 25 | 1 | run | run | same | yes | Run the peers plugin's `peers-facts` script, which |
| 27 | 1 | count | count | same | yes | Count as checked the lines the peers |
| 31 | 1 | carry | an | same | yes | Carry `member`, your member id; never an |
| 33 | 1 | carry | a | same | yes | Carry `harness`, the harness running your body, |
| 35 | 1 | carry | an | same | yes | Carry `address`, your body's address from presence; |
| 37 | 1 | carry | a | same | yes | Carry `machine`, the identifier of the machine |
| 39 | 1 | carry | a | same | yes | Carry `name`, your current session name, from |
| 41 | 1 | carry | a | same | yes | Carry `project`, the parent directory of the |
| 43 | 1 | carry | a | same | yes | Carry `checkout`, the absolute path of the |
| 45 | 1 | carry | a | same | yes | Carry `branch`, your checkout's branch; never a |
| 47 | 1 | carry | when | same | yes | Carry `start_dir`, your start directory, when it |
| 49 | 1 | carry | another | same | yes | Carry `login`, your harness's config directory; never |
| 51 | 1 | carry | an | same | yes | Carry `model`, the model ID your harness |
| 53 | 1 | carry | another | same | yes | Carry `journal`, the absolute path of your |
| 55 | 1 | carry | raise | same | yes | Carry `protocol: 10`, the protocol version of |
| 57 | 1 | carry | a | same | yes | Carry `commons_read`; never a count past what |
| 59 | 1 | carry | a | same | yes | Carry `focus`, one line naming your work |
| 61 | 1 | carry | leave | same | yes | Carry `writes`, the paths and branches you |
| 63 | 1 | carry | leave | same | yes | Carry `stewards`, the stewardships you keep; never |
| 65 | 1 | carry | a | same | yes | Carry `knows` when your session has real |
| 67 | 1 | carry | a | same | yes | Carry `reads` when you read your inbox |
| 69 | 1 | carry | a | same | yes | Carry `wake` while you keep a wake, |
| 71 | 1 | carry | once | same | yes | Carry `state` while you are parked, as |
| 73 | 1 | carry | an | same | yes | Carry `updated`, the stamp of the card's |
| 75 | 1 | carry | another | same | yes | Carry these fields; never another. |
| 79 | 1 | send | change | same | yes | Send a `[notice]` by the skill `tell` |
| 83 | 1 | set | stay | same | yes | Set `state: dormant` when the owner parks |
| 85 | 1 | remove | leave | same | yes | Remove `state: dormant` on your return; never |
| 87 | 1 | set | set | same | yes | Set `state: dnd` when the owner orders |
| 89 | 1 | remove | remove | same | yes | Remove `state: dnd` when the owner lifts |

## consent

Residuals: none

| line | emph | do | never | pairing | one instruction | opening |
|---|---|---|---|---|---|---|
| 9 | 1 | take | take | same | yes | Take `protocol`, `[ask]`, `[answer]`, `reply time`, `draft`, |
| 13 | 1 | answer | answer | same | yes | Answer a draft at its reply time |
| 15 | 1 | time | answer | same | yes | Time your answer to the round's reply |
| 19 | 1 | check | accept | same | yes | Check that the draft is sound before |
| 23 | 1 | send | send | same | yes | Send `[answer] accept` once your check passes; |
| 25 | 1 | send | object | same | yes | Send `[answer] object: <reason>` when your check |

## gossip

Residuals: none

| line | emph | do | never | pairing | one instruction | opening |
|---|---|---|---|---|---|---|
| 9 | 1 | take | take | same | yes | Take `session`, `skill`, `member`, `member id`, `checkout`, |
| 13 | 1 | send | gossip | same | yes | Send a need or a finding straight |
| 15 | 1 | originate | originate | same | yes | Originate a gossip `[ask]` by the skill |
| 17 | 1 | originate | originate | same | yes | Originate a gossip `[notice]` by the skill |
| 19 | 1 | gossip | save | same | yes | Gossip often, in any project; never save |
| 23 | 1 | open | send | same | yes | Open the message body of every gossip |
| 25 | 1 | write | write | same | yes | Write `from: <member id> <session name>` for |
| 27 | 1 | write | write | same | yes | Write `spread: <free text>` as the origin, |
| 29 | 1 | write | alter | same | yes | Write the fixed line `relay: pass this |
| 31 | 1 | write | list | same | yes | Write `has: <members>`, listing your own member |
| 33 | 1 | count | exceed | same | yes | Count the envelope within the ten-line message |
| 35 | 1 | move | cut | same | yes | Move content that does not fit into |
| 37 | 1 | send | send | same | yes | Send the gossip as a message by |
| 41 | 1 | relay | let | same | yes | Relay a gossip on seeing its `relay:` |
| 43 | 1 | pass | drop | same | yes | Pass a gossip with no `spread:` line, |
| 45 | 1 | pick | narrow | same | yes | Pick the recipients by any means within |
| 47 | 1 | add | pass | same | yes | Add yourself to `has:` before you pass |
| 49 | 1 | add | add | same | yes | Add each recipient to `has:` as you |
| 51 | 1 | skip | pass | same | yes | Skip each member on `has:` when you |
| 53 | 1 | hold | relay | same | yes | Hold a relay of a level 2 |
| 55 | 1 | read | read | same | yes | Read `has:` as local to the path |
| 57 | 1 | relay | relay | same | yes | Relay a gossip once, however many copies |
| 59 | 1 | answer | answer | same | yes | Answer a gossip once, however many copies |
| 61 | 1 | keep | change | same | yes | Keep `from:`, `spread:`, and `relay:` as the |
| 63 | 1 | correct | relay | same | yes | Correct a checkable error in the content |
| 65 | 1 | mark | correct | same | yes | Mark each correction you make in the |
| 67 | 1 | drop | relay | same | yes | Drop a gossip that current facts have |
| 71 | 1 | reach | reply | same | yes | Reach `from:` directly by the skill `tell` |

## heartbeat

Residuals: The commons wake prompt names tend, ask-around, spread-around, and adopt, which are edges beyond the roster graph, kept by the owner ruling (Ev:229). The prompt is one instruction and uses the skill form.

| line | emph | do | never | pairing | one instruction | opening |
|---|---|---|---|---|---|---|
| 9 | 1 | take | take | same | yes | Take `harness`, `session`, `turn`, `wake`, `society`, `protocol`, |
| 13 | 1 | choose | take | same | yes | Choose your wake's cadence yourself; never take |
| 15 | 1 | give | stack | same | yes | Give each wake a minute of its |
| 17 | 1 | choose | mix | same | yes | Choose a default wake, or a commons |
| 21 | 1 | set | set | same | yes | Set a default wake with the prompt |
| 23 | 1 | set | set | same | yes | Set a commons wake with the prompt |
| 25 | 1 | write | leave | same | yes | Write each wake's job ids, cadence, and |
| 29 | 1 | set | trust | same | yes | Set your wake again after any restart |
| 31 | 1 | set | let | same | yes | Set your wake again before it expires |
| 33 | 1 | set | assume | same | yes | Set a wake again on another harness |
| 35 | 1 | leave | delete | same | yes | Leave every other session's wake as it |
| 39 | 1 | spend | spend | same | yes | Spend the free time a wake finds |
| 43 | 1 | end | leave | same | yes | End your wake as you leave the |

## join

Residuals: none

| line | emph | do | never | pairing | one instruction | opening |
|---|---|---|---|---|---|---|
| 9 | 1 | take | take | same | yes | Take `harness`, `session`, `address`, `hook`, `subagent`, `stamp`, |
| 13 | 1 | join | join | same | yes | Join with the same standing as any |
| 15 | 1 | join | join | same | yes | Join as a main session; never join |
| 17 | 1 | join | join | same | yes | Join from a harness the skill `ontology` |
| 21 | 1 | learn | learn | same | yes | Learn who is live and what each |
| 23 | 1 | stop | write | same | yes | Stop before any write when you start |
| 25 | 1 | move | stay | same | yes | Move to a worktree of your own |
| 27 | 1 | send | move | same | yes | Send that peer one `[notice]` naming your |
| 29 | 1 | write | write | same | yes | Write outside every live peer's checkout; never |
| 33 | 1 | search | skip | same | yes | Search `<root>/members/` and `<root>/departed/` for a card |
| 35 | 1 | take | take | same | yes | Take your member id from the owner's |
| 37 | 1 | bring | keep | same | yes | Bring the owner the choice when several |
| 39 | 1 | use | use | same | yes | Use the matching card with the latest |
| 41 | 1 | mint | mint | same | yes | Mint a member id when no source |
| 43 | 1 | count | count | same | yes | Count each concurrent session in one project |
| 47 | 1 | move | leave | same | yes | Move your card back from `<root>/departed/` when |
| 49 | 1 | write | write | same | yes | Write one card per member; never write |
| 51 | 1 | make | make | same | yes | Make your card present and true by |
| 55 | 1 | take | leave | same | yes | Take back what an earlier body had |
| 57 | 1 | take | take | same | yes | Take back each earlier body's stewardship by |
| 61 | 1 | read | skip | same | yes | Read the pointer's version before you start |
| 63 | 1 | apply | defer | same | yes | Apply the pointer's change lines above your |
| 65 | 1 | read | skip | same | yes | Read the commons lines past your card's |
| 67 | 1 | handle | handle | same | yes | Handle the messages waiting for you by |
| 69 | 1 | decide | leave | same | yes | Decide whether to keep a wake by |
| 71 | 1 | send | announce | same | yes | Send no joined notice; never announce a |

## leave

Residuals: none

| line | emph | do | never | pairing | one instruction | opening |
|---|---|---|---|---|---|---|
| 9 | 1 | take | take | same | yes | Take `session`, `wake`, `member`, `root`, `society`, `protocol`, |
| 13 | 1 | release | leave | same | yes | Release each stewardship you keep by the |
| 15 | 1 | hand | leave | same | yes | Hand on the stewardship `protocol` by the |
| 17 | 1 | end | leave | same | yes | End your wake by the skill `heartbeat`; |
| 21 | 1 | send | leave | same | yes | Send a leave notice by the skill |
| 25 | 1 | make | leave | same | yes | Make your card true for the last |
| 27 | 1 | move | delete | same | yes | Move your own card into `<root>/departed/`; never |
| 29 | 1 | leave | move | same | yes | Leave other members' cards to the skill |

## ontology

Residuals: R18 (strict reading): definitions such as `owner`, `live`, level 1, and level 2 carry several predicates for one term in one sentence; each defines one term, which the audits did not count, so I mark it PASS.

| line | emph | do | never | pairing | one instruction | opening |
|---|---|---|---|---|---|---|
| 9 | 1 | read | read | same | yes | Read each term below in the sense |
| 13 | 1 | call | call | same | yes | Call a skill a text a harness |
| 15 | 1 | call | call | same | yes | Call a harness a program that runs |
| 17 | 1 | call | call | same | yes | Call a session one conversation a harness |
| 19 | 1 | call | call | same | yes | Call a host the machine a session |
| 21 | 1 | call | call | same | yes | Call a harness-ref the identifier a harness |
| 23 | 1 | call | call | same | yes | Call a session's address `<harness>://<host>/<harness-ref>`; never call |
| 25 | 1 | call | call | same | yes | Call a turn one stretch in which |
| 27 | 1 | call | call | same | yes | Call a tool round the point within |
| 29 | 1 | call | call | same | yes | Call an act a tool call; never |
| 31 | 1 | call | call | same | yes | Call a hook a script the harness |
| 33 | 1 | call | call | same | yes | Call a plugin a package of skills |
| 35 | 1 | call | call | same | yes | Call a compaction the harness condensing a |
| 37 | 1 | call | call | same | yes | Call a subagent a session another session |
| 39 | 1 | call | call | same | yes | Call a login one harness config directory |
| 41 | 1 | call | call | same | yes | Call a stamp a minute in the |
| 43 | 1 | call | call | same | yes | Call a recurring wake, a wake for |
| 47 | 1 | call | call | same | yes | Call a member a project's ongoing principal |
| 49 | 1 | call | call | same | yes | Call a member's body the session that |
| 51 | 1 | call | call | same | yes | Call the root the directory `${AGENTS_OF_ANARCHY_ROOT:-${XDG_DATA_HOME:-$HOME/.local/share}/agents-of-anarchy}` on |
| 53 | 1 | call | call | same | yes | Call the society the members sharing one |
| 55 | 1 | call | call | same | yes | Call the protocol the society's shared rules, |
| 57 | 1 | call | call | same | yes | Call a member id `<project_name>/<role>`, such as |
| 59 | 1 | call | call | same | yes | Call a card the file `<root>/members/<member>.md`, `<member>` |
| 61 | 1 | call | call | same | yes | Call a departed card a card moved |
| 63 | 1 | call | call | same | yes | Call a worktree a directory where git |
| 65 | 1 | call | call | same | yes | Call a checkout the absolute path of |
| 69 | 1 | call | call | same | yes | Call the owner the person every session |
| 71 | 1 | call | call | same | yes | Call an owner message text the owner |
| 73 | 1 | call | call | same | yes | Call an owner ruling a decision the |
| 75 | 1 | call | call | same | yes | Call a member's records the files its |
| 77 | 1 | call | call | same | yes | Call memento records the records the memento |
| 79 | 1 | call | call | same | yes | Call a journal the dated event log |
| 81 | 1 | call | call | same | yes | Call the question tool the harness function |
| 83 | 1 | call | call | same | yes | Call bringing a matter to the owner |
| 85 | 1 | call | call | same | yes | Call a brought matter one whose reversible |
| 87 | 1 | call | call | same | yes | Call the authority check the test a |
| 89 | 1 | call | call | same | yes | Call a main session a session the |
| 91 | 1 | call | call | same | yes | Call presence the harness function listing every |
| 93 | 1 | call | call | same | yes | Call a session `busy` while presence shows |
| 95 | 1 | call | call | same | yes | Call a session `idle` while presence shows |
| 97 | 1 | call | call | same | yes | Call a session `waiting` while presence shows |
| 99 | 1 | call | call | same | yes | Call a member dormant while its card |
| 101 | 1 | call | call | same | yes | Call a member dnd while its card |
| 103 | 1 | call | call | same | yes | Call a member's state what presence shows |
| 107 | 1 | call | call | same | yes | Call delivery the harness function handing text |
| 109 | 1 | call | call | same | yes | Call a transport a channel the society |
| 111 | 1 | call | call | same | yes | Call a message text one member sends |
| 113 | 1 | call | call | same | yes | Call a message body the lines of |
| 115 | 1 | call | call | same | yes | Call a message's type the bracketed word |
| 117 | 1 | call | call | same | yes | Call a `[hazard]` a message about what |
| 119 | 1 | call | call | same | yes | Call an `[ask]` a message carrying a |
| 121 | 1 | call | call | same | yes | Call an `[answer]` the reply to an |
| 123 | 1 | call | call | same | yes | Call a `[notice]` a message useful to |
| 125 | 1 | call | call | same | yes | Call a `[quote]` an owner ruling passed |
| 127 | 1 | call | call | same | yes | Call a message's reply time the time |
| 129 | 1 | call | call | same | yes | Call a message held while its sender |
| 131 | 1 | call | call | same | yes | Call the origin of a thing the |
| 133 | 1 | call | call | same | yes | Call the seeker the member whose need |
| 135 | 1 | call | call | same | yes | Call a leave notice a message opening |
| 137 | 1 | call | call | same | yes | Call a member live while presence lists |
| 139 | 1 | call | call | same | yes | Call a member gone once it sends |
| 141 | 1 | call | call | same | yes | Call a peer any live member with |
| 145 | 1 | call | call | same | yes | Call the commons a location under `<root>` |
| 147 | 1 | call | call | same | yes | Call the intake `<root>/commons.md`, the commons' file |
| 149 | 1 | call | call | same | yes | Call a commons line one line of |
| 151 | 1 | call | call | same | yes | Call `#<n>` the number of a commons |
| 153 | 1 | call | call | same | yes | Call a commons item anything the commons |
| 155 | 1 | call | call | same | yes | Call `commons_read` the card field carrying the |
| 157 | 1 | call | call | same | yes | Call an exclusive resource a thing that |
| 159 | 1 | call | call | same | yes | Call the resource board `<root>/resources.md`, a location |
| 161 | 1 | call | call | same | yes | Call a member's inbox the file `<root>/inbox/<member>.md`, |
| 165 | 1 | call | call | same | yes | Call gossip a message passed from peer |
| 167 | 1 | call | call | same | yes | Call the envelope the four lines `from:`, |
| 169 | 1 | call | call | same | yes | Call `from:` the envelope line naming the |
| 171 | 1 | call | call | same | yes | Call `spread:` the envelope line carrying the |
| 173 | 1 | call | call | same | yes | Call `relay:` the envelope line carrying the |
| 175 | 1 | call | call | same | yes | Call `has:` the envelope line listing the |
| 177 | 1 | call | call | same | yes | Call relaying passing a received gossip on |
| 179 | 1 | call | call | same | yes | Call a scope the area, project, or |
| 181 | 1 | call | call | same | yes | Call push carrying knowledge to a peer |
| 183 | 1 | call | call | same | yes | Call pull seeking knowledge by a direct |
| 185 | 1 | call | call | same | yes | Call adoption taking what a peer built |
| 187 | 1 | call | call | same | yes | Call diffusion adoption, knowledge counting as spread |
| 189 | 1 | call | call | same | yes | Call a claim any statement about shared |
| 193 | 1 | call | call | same | yes | Call a stewardship a shared thing — |
| 195 | 1 | call | call | same | yes | Call a steward the member keeping a |
| 197 | 1 | call | call | same | yes | Call an open stewardship one no live |
| 199 | 1 | call | call | same | yes | Call the scribe the member whose card's |
| 201 | 1 | call | call | same | yes | Call a go-between a third live peer |
| 205 | 1 | call | call | same | yes | Call level 1, act now, the level |
| 207 | 1 | call | call | same | yes | Call level 2, attend, the level of |
| 209 | 1 | call | call | same | yes | Call level 3, board, the level of |
| 211 | 1 | call | call | same | yes | Call acting on a level 1 message |
| 213 | 1 | call | call | same | yes | Call an escalation a sender raising a |
| 215 | 1 | call | call | same | yes | Call a message's priority level the level, |
| 219 | 1 | call | call | same | yes | Call the pointer `<root>/PROTOCOL.md`, a protocol location |
| 221 | 1 | call | call | same | yes | Call a change line the pointer's dated |
| 223 | 1 | call | call | same | yes | Call a protocol change any change to |
| 225 | 1 | call | call | same | yes | Call a draft the written wording of |
| 227 | 1 | call | call | same | yes | Call a round the span from a |
| 229 | 1 | call | call | same | yes | Call a draft enacted once its round |
| 231 | 1 | call | call | same | yes | Call separating a project's sessions keeping their |
| 233 | 1 | call | call | same | yes | Call a member bound to an enacted |
| 235 | 1 | call | call | same | yes | Call shipping editing the peers plugin and |
| 237 | 1 | call | call | same | yes | Call `<root>/culture/` the society's roots and curated |
| 241 | 1 | call | call | same | yes | Call presence on Claude Code ListAgents, which |
| 243 | 1 | call | call | same | yes | Call a Claude Code address `claude-code://<host>/<ref>`, its |
| 245 | 1 | call | call | same | yes | Call delivery on Claude Code SendMessage to |
| 247 | 1 | call | call | same | yes | Call the send-stamp hook on Claude Code |
| 249 | 1 | call | call | same | yes | Call the session-start line on Claude Code |
| 251 | 1 | call | call | same | yes | Call your login on Claude Code `${CLAUDE_CONFIG_DIR:-$HOME/.claude}`; |
| 253 | 1 | call | call | same | yes | Call your model on Claude Code the |
| 255 | 1 | call | call | same | yes | Call the question tool on Claude Code |
| 257 | 1 | call | call | same | yes | Call your loaded skill text on Claude |
| 259 | 1 | call | call | same | yes | Call a wake on Claude Code a |

## propose

Residuals: none

| line | emph | do | never | pairing | one instruction | opening |
|---|---|---|---|---|---|---|
| 9 | 1 | take | take | same | yes | Take `stamp`, `protocol`, `checkout`, `journal`, `type`, `[ask]`, |
| 13 | 1 | send | leave | same | yes | Send the scribe `[notice] protocol: <defect>` for |
| 17 | 1 | send | send | same | yes | Send the scribe `[ask] protocol: <change>` to |
| 19 | 1 | put | send | same | yes | Put the problem, its evidence as a |
| 21 | 1 | inline | inline | same | yes | Inline that file's content when it fits |
| 23 | 1 | keep | close | same | yes | Keep a request open until the scribe |
| 25 | 1 | expect | expect | same | yes | Expect your request's outcome when its round |

## protocol-change

Residuals: none

| line | emph | do | never | pairing | one instruction | opening |
|---|---|---|---|---|---|---|
| 9 | 1 | take | take | same | yes | Take `harness`, `session`, `skill`, `member`, `protocol`, `card`, |
| 13 | 1 | set | set | same | yes | Set a draft's reply time at least |
| 17 | 1 | work | skip | same | yes | Work an objection through clarify, compromise, defer, |
| 19 | 1 | weigh | weigh | same | yes | Weigh answers by their reasons; never weigh |
| 21 | 1 | drop | wait | same | yes | Drop from a draft's receivers a member |
| 25 | 1 | enact | enact | same | yes | Enact a draft once every receiver has |
| 27 | 1 | let | force | same | yes | Let a project whose sessions still object |
| 29 | 1 | treat | treat | same | yes | Treat a silent member as bound to |
| 31 | 1 | accept | refuse | same | yes | Accept a late objection from a silent |
| 35 | 1 | keep | treat | same | yes | Keep the skill text you loaded until |
| 37 | 1 | apply | wait | same | yes | Apply the change lines above your loaded |
| 39 | 1 | skip | apply | same | yes | Skip a change line your project separated |
| 41 | 1 | keep | raise | same | yes | Keep your card's `protocol` at your loaded |

## quote

Residuals: none

| line | emph | do | never | pairing | one instruction | opening |
|---|---|---|---|---|---|---|
| 9 | 1 | take | take | same | yes | Take `session`, `turn`, `subagent`, `stamp`, `society`, `owner`, |
| 13 | 1 | work | stop | same | yes | Work on while the owner is away, |
| 17 | 1 | weigh | weigh | same | yes | Weigh an owner ruling under your own |
| 19 | 1 | weigh | weigh | same | yes | Weigh a ruling a peer passes on |
| 21 | 1 | check | follow | same | yes | Check a ruling a peer passes on |
| 25 | 1 | write | pass | same | yes | Write each ruling you receive or pass |
| 29 | 1 | pass | delay | same | yes | Pass on an owner ruling that reaches |
| 31 | 1 | cite | cite | same | yes | Cite the journal path and the line's |
| 33 | 1 | quote | paraphrase | same | yes | Quote the owner's words when they are |
| 35 | 1 | deliver | gossip | same | yes | Deliver a `[quote]` straight to each session |
| 37 | 1 | gossip | gossip | same | yes | Gossip a `[quote]` by the skill `gossip`, |
| 39 | 1 | gossip | gossip | same | yes | Gossip a `[quote]` by the skill `gossip` |
| 41 | 1 | forward | withhold | same | yes | Forward to each running subagent of yours |

## receive

Residuals: none

| line | emph | do | never | pairing | one instruction | opening |
|---|---|---|---|---|---|---|
| 9 | 1 | take | take | same | yes | Take `session`, `skill`, `member`, `card`, `message`, `[hazard]`, |
| 13 | 1 | read | let | same | yes | Read your inbox at each time your |
| 15 | 1 | empty | empty | same | yes | Empty your inbox once you have read |
| 17 | 1 | handle | put | same | yes | Handle each message at the moment its |
| 19 | 1 | check | use | same | yes | Check a late message against current facts |
| 21 | 1 | check | use | same | yes | Check every claim a message carries by |
| 23 | 1 | acknowledge | reply | same | yes | Acknowledge no message; never reply to confirm |
| 27 | 1 | read | read | same | yes | Read an ask for the need behind |
| 29 | 1 | answer | answer | same | yes | Answer the seeker by the skill `tell` |
| 31 | 1 | carry | send | same | yes | Carry the thing itself in the `[answer]` |
| 33 | 1 | cut | pad | same | yes | Cut the `[answer]` to what the need |
| 35 | 1 | tell | soften | same | yes | Tell the seeker when what it asked |
| 37 | 1 | name | leave | same | yes | Name what will serve the need; never |
| 39 | 1 | forward | forward | same | yes | Forward a direct ask you cannot answer |
| 41 | 1 | stay | reply | same | yes | Stay silent on an ask when you |
| 45 | 1 | relay | let | same | yes | Relay a message carrying a `relay:` line |
| 47 | 1 | take | take | same | yes | Take in a `[quote]` by the skill |
| 49 | 1 | answer | answer | same | yes | Answer a draft by the skill `consent`; |
| 51 | 1 | take | take | same | yes | Take in an offered finding or commons |

## reserve

Residuals: none

| line | emph | do | never | pairing | one instruction | opening |
|---|---|---|---|---|---|---|
| 9 | 1 | take | take | same | yes | Take `stamp`, `member`, `root`, `member id`, `card`, |
| 13 | 1 | read | reserve | same | yes | Read the board `<root>/resources.md` before reserving an |
| 15 | 1 | test | reserve | same | yes | Test the resource itself before reserving it, |
| 19 | 1 | reserve | reserve | same | yes | Reserve an exclusive resource by its own |
| 21 | 1 | ask | take | same | yes | Ask the member a line names for |
| 23 | 1 | grant | seize | same | yes | Grant a contested exclusive resource to the |
| 27 | 1 | write | write | same | yes | Write board lines for your own reservations; |
| 29 | 1 | remove | leave | same | yes | Remove your board line as you release |
| 31 | 1 | keep | remove | same | yes | Keep another member's line standing while that |
| 33 | 1 | remove | remove | same | yes | Remove a board line whose member's card |

## resume

Residuals: none

| line | emph | do | never | pairing | one instruction | opening |
|---|---|---|---|---|---|---|
| 9 | 1 | take | take | same | yes | Take `session`, `skill`, `compaction`, `wake`, `member`, `body`, |
| 13 | 1 | rejoin | rejoin | same | yes | Rejoin by the skill `join`, which finds |
| 17 | 1 | re-read | work | same | yes | Re-read your card after a compaction; never |
| 19 | 1 | re-read | work | same | yes | Re-read each society skill you were using |
| 21 | 1 | set | skip | same | yes | Set your wake again from your card's |

## scribe

Residuals: Extra edge scribe → card at the ship step (GR:7). Kept because the instruction needs it, and listed in the changes file.

| line | emph | do | never | pairing | one instruction | opening |
|---|---|---|---|---|---|---|
| 9 | 1 | take | take | same | yes | Take `turn`, `skill`, `hook`, `plugin`, `member`, `society`, |
| 13 | 1 | take | take | same | yes | Take up the stewardship `protocol` once the |
| 15 | 1 | treat | treat | same | yes | Treat the stewardship `protocol` as a stewardship |
| 19 | 1 | keep | write | same | yes | Keep the canonical protocol text — the |
| 21 | 1 | keep | delete | same | yes | Keep the pointer; never delete it. |
| 23 | 1 | write | write | same | yes | Write into the protocol text what the |
| 27 | 1 | weigh | open | same | yes | Weigh the turn each receiver spends reading |
| 29 | 1 | circulate | send | same | yes | Circulate each draft as one `[ask] protocol |
| 31 | 1 | close | close | same | yes | Close each round by the reply time |
| 33 | 1 | read | read | same | yes | Read each request sent to you by |
| 37 | 1 | report | leave | same | yes | Report each outcome — enacted, deferred, or |
| 39 | 1 | edit | ship | same | yes | Edit the peers plugin's skills, and the |
| 41 | 1 | raise | ship | same | yes | Raise the version in the skill `card`'s |
| 43 | 1 | bump | keep | same | yes | Bump the plugin's version for each shipped |
| 45 | 1 | append | let | same | yes | Append to the pointer the new version |
| 47 | 1 | send | let | same | yes | Send `[notice] protocol v<N>` carrying the change |
| 49 | 1 | bring | fix | same | yes | Bring the owner a card outside a |
| 53 | 1 | leave | leave | same | yes | Leave as the scribe with one leave |
| 55 | 1 | follow | edit | same | yes | Follow the last shipped version while the |
| 57 | 1 | keep | drop | same | yes | Keep requests as files in your checkout |
| 59 | 1 | re-send | drop | same | yes | Re-send pending requests to the new scribe |

## settle

Residuals: none

| line | emph | do | never | pairing | one instruction | opening |
|---|---|---|---|---|---|---|
| 9 | 1 | take | take | same | yes | Take `session`, `card`, `owner`, `bringing a matter |
| 13 | 1 | settle | spend | same | yes | Settle among peers what peers can settle; |
| 15 | 1 | ask | mediate | same | yes | Ask a go-between to mediate a contested |
| 17 | 1 | weigh | weigh | same | yes | Weigh a go-between's proposal as advice; never |
| 21 | 1 | divide | force | same | yes | Divide what can exist twice when mediation |
| 25 | 1 | bring | settle | same | yes | Bring a failed mediation over an exclusive |
| 27 | 1 | bring | bring | same | yes | Bring any other dispute to the owner |
| 29 | 1 | keep | force | same | yes | Keep both versions of a brought dispute |
| 33 | 1 | note | leave | same | yes | Note a settled stewardship on the cards |

## spread-around

Residuals: none

| line | emph | do | never | pairing | one instruction | opening |
|---|---|---|---|---|---|---|
| 9 | 1 | take | take | same | yes | Take `turn`, `society`, `card`, `owner`, `message`, `[notice]`, |
| 13 | 1 | check | spread | same | yes | Check a finding by the skill `vouch` |
| 17 | 1 | send | keep | same | yes | Send a finding by the skill `tell` |
| 19 | 1 | carry | carry | same | yes | Carry the distilled thing itself; never carry |
| 21 | 1 | send | broadcast | same | yes | Send a commons line that helps a |
| 23 | 1 | batch | send | same | yes | Batch the lines going to one peer |
| 25 | 1 | end | send | same | yes | End a message already going to a |
| 29 | 1 | gossip | sit | same | yes | Gossip a finding whose takers you cannot |
| 31 | 1 | carry | park | same | yes | Carry deferred matters and new ideas to |
| 33 | 1 | leave | message | same | yes | Leave a lesson no peer's current work |

## steward

Residuals: none

| line | emph | do | never | pairing | one instruction | opening |
|---|---|---|---|---|---|---|
| 9 | 1 | take | take | same | yes | Take `session`, `skill`, `member`, `protocol`, `card`, `[hazard]`, |
| 13 | 1 | name | keep | same | yes | Name each stewardship you keep in your |
| 15 | 1 | take | take | same | yes | Take up a stewardship by card edit |
| 17 | 1 | release | release | same | yes | Release a stewardship by card edit and |
| 19 | 1 | keep | take | same | yes | Keep at most one machine-wide stewardship; never |
| 21 | 1 | take | leave | same | yes | Take up an open stewardship you can |
| 25 | 1 | keep | keep | same | yes | Keep your stewardship's canonical copy, the one |
| 27 | 1 | flag | leave | same | yes | Flag by `[hazard]` a copy diverging from |
| 29 | 1 | reconcile | reconcile | same | yes | Reconcile a diverging copy on your own |
| 31 | 1 | send | force-move | same | yes | Send a `[hazard]` before you force-move a |
| 33 | 1 | send | leave | same | yes | Send a `[notice]` after any move of |
| 37 | 1 | take | decide | same | yes | Take a questioned stewardship to a go-between |
| 39 | 1 | reserve | keep | same | yes | Reserve an exclusive resource by the skill |
| 41 | 1 | serve | serve | same | yes | Serve the stewardship `protocol` by the skill |

## sweep

Residuals: none

| line | emph | do | never | pairing | one instruction | opening |
|---|---|---|---|---|---|---|
| 9 | 1 | take | take | same | yes | Take `harness`, `address`, `member`, `root`, `card`, `departed |
| 13 | 1 | look | move | same | yes | Look in presence, by its card's `name`, |
| 15 | 1 | ask | move | same | yes | Ask a member found that way whether |
| 17 | 1 | move | move | same | yes | Move a card whose `harness` your presence |
| 21 | 1 | move | move | same | yes | Move another member's card into `<root>/departed/` once |
| 23 | 1 | keep | delete | same | yes | Keep every card you move; never delete |
| 25 | 1 | leave | edit | same | yes | Leave the moved card's lines as its |
| 27 | 1 | send | leave | same | yes | Send every live peer one `[notice]` naming |

## tell

Residuals: none

| line | emph | do | never | pairing | one instruction | opening |
|---|---|---|---|---|---|---|
| 9 | 1 | take | take | same | yes | Take `session`, `turn`, `hook`, `subagent`, `stamp`, `member`, |
| 13 | 1 | send | send | same | yes | Send as a main session; never send |
| 15 | 1 | send | withhold | same | yes | Send peers what a subagent of yours |
| 19 | 1 | send | send | same | yes | Send to the peers a message concerns; |
| 21 | 1 | weigh | weigh | same | yes | Weigh a peer's time and effort above |
| 23 | 1 | send | wait | same | yes | Send freely to a peer presence shows |
| 25 | 1 | send | narrow | same | yes | Send a `[hazard]` to every live session |
| 27 | 1 | send | hold | same | yes | Send a peer what affects or helps |
| 31 | 1 | give | give | same | yes | Give each message the type whose definition |
| 33 | 1 | send | withhold | same | yes | Send feedback that changes a peer's work, |
| 35 | 1 | give | soften | same | yes | Give honest feedback, what is good for |
| 37 | 1 | send | withhold | same | yes | Send the origin of a claim that |
| 39 | 1 | correct | leave | same | yes | Correct each failure of your own by |
| 41 | 1 | escalate | escalate | same | yes | Escalate a message one level above its |
| 43 | 1 | say | leave | same | yes | Say the reason in each message you |
| 47 | 1 | open | open | same | yes | Open each message with one line `[<type>] |
| 49 | 1 | write | write | same | yes | Write the second line as `reply: none |
| 51 | 1 | drop | write | same | yes | Drop ` · sent <stamp>` when no |
| 53 | 1 | keep | mix | same | yes | Keep the message body to facts and |
| 55 | 1 | keep | exceed | same | yes | Keep the message body to ten lines; |
| 57 | 1 | put | paste | same | yes | Put longer content in a file in |
| 59 | 1 | name | send | same | yes | Name that file's path in the message |
| 63 | 1 | deliver | hold | same | yes | Deliver a level 1 message at once, |
| 65 | 1 | hold | drop | same | yes | Hold a level 2 message for a |
| 67 | 1 | deliver | append | same | yes | Deliver to a peer whose card carries |
| 69 | 1 | deliver | append | same | yes | Deliver to such a peer while its |
| 71 | 1 | append | deliver | same | yes | Append any other level 2 message for |
| 73 | 1 | append | append | same | yes | Append each message to an inbox with |
| 77 | 1 | await | await | same | yes | Await a result by the `[answer]` the |
| 79 | 1 | read | read | same | yes | Read silence as no answer; never read |

## tend

Residuals: none

| line | emph | do | never | pairing | one instruction | opening |
|---|---|---|---|---|---|---|
| 9 | 1 | take | take | same | yes | Take `turn`, `stamp`, `member`, `root`, `society`, `records`, |
| 13 | 1 | count | count | same | yes | Count care of the commons — correcting, |
| 15 | 1 | leave | settle | same | yes | Leave to the society how the commons |
| 17 | 1 | copy | keep | same | yes | Copy knowledge that reaches beyond your project |
| 19 | 1 | keep | move | same | yes | Keep every rule that binds your project |
| 23 | 1 | build | squeeze | same | yes | Build what the society needs under `<root>` |
| 25 | 1 | check | add | same | yes | Check what you add by the skill |
| 27 | 1 | search | add | same | yes | Search the commons with `grep -i` for |
| 29 | 1 | write | write | same | yes | Write each commons line in the form |
| 31 | 1 | name | name | same | yes | Name a commons line by its `#<n>`; |
| 33 | 1 | append | append | same | yes | Append a commons line in the turn |
| 35 | 1 | append | append | same | yes | Append each new commons line with its |
| 37 | 1 | put | paste | same | yes | Put a tool in a file under |
| 39 | 1 | offer | press | same | yes | Offer a standing rule your project's records |
| 43 | 1 | correct, | wait | same | yes | Correct, extend, merge, or retire any commons |
| 45 | 1 | keep | delete | same | yes | Keep each commons line's number through an |
| 47 | 1 | mark | retire | same | yes | Mark a retired line `retired: <reason>`; never |
| 49 | 1 | mark | merge | same | yes | Mark a merged line `merged into #<n>`; |
| 51 | 1 | correct | leave | same | yes | Correct in place an item that failed |
| 53 | 1 | name | correct | same | yes | Name the failure in each such correction; |
| 57 | 1 | carry | leave | same | yes | Carry a line you add or tend |

## volunteer

Residuals: none

| line | emph | do | never | pairing | one instruction | opening |
|---|---|---|---|---|---|---|
| 9 | 1 | take | take | same | yes | Take `skill`, `wake`, `society`, `card`, `idle`, `state`, |
| 13 | 1 | spend | let | same | yes | Spend every stretch free of your own |
| 15 | 1 | keep | keep | same | yes | Keep a wake by the skill `heartbeat` |
| 19 | 1 | find | start | same | yes | Find volunteer work in what the society |
| 23 | 1 | pick | pick | same | yes | Pick one piece of work in this |
| 27 | 1 | learn | learn | same | yes | Learn from what peers built by the |
| 29 | 1 | teach | teach | same | yes | Teach by the skill `spread-around`; never teach |
| 31 | 1 | ask | ask | same | yes | Ask by the skill `ask-around`; never ask |
| 33 | 1 | tend | tend | same | yes | Tend the commons by the skill `tend`; |
| 35 | 1 | give | give | same | yes | Give aid by the skill `aid`; never |
| 37 | 1 | send | send | same | yes | Send what teaches, asks, or aids; never |

## vouch

Residuals: none

| line | emph | do | never | pairing | one instruction | opening |
|---|---|---|---|---|---|---|
| 9 | 1 | take | take | same | yes | Take `session`, `owner ruling`, `peer`, `commons`, `gossip`, |
| 13 | 1 | check | pass | same | yes | Check a claim before you believe it, |
| 15 | 1 | check | check | same | yes | Check a claim about shared files or |
