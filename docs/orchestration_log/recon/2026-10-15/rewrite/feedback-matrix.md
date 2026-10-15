# Design feedback matrix, skill roster, 2026-10-15

Analyst output. Peer claims unverified unless the Check column says confirmed. Read-only except this file.

## Keys

Members (6): **M** memento-manager, **MT** matchtuner-maintainer, **PC** product-catalog-maintainer, **MS** machine-setup-manager, **IE** instruction-eval, **MD** manifesto-discovery.

Sources (cite form `member:item`):
- M `/Users/ryzhakar/pp/memento/docs/orchestration_log/recon/2026-10-15/roster-feedback.md` (items E1-E5, L1, etc.)
- MT only in journal receipt, `docs/orchestration_log/history/2026-10-14/events.md` line 198 (no detail file).
- PC `/Users/ryzhakar/competera/product-catalog-storage-api/docs/orchestration_log/history/2026-10-15/skill-roster-feedback.md` (items 1-14)
- MS `/Users/ryzhakar/pp/offline-kit/docs/society/roster-feedback-2026-10-15.md` (items 1-9)
- IE `/Users/ryzhakar/pp/claude-skills.worktrees/instruction-eval/orchestration_log/history/2026-10-12/society-skill-design-feedback.md` (section names; cites `R-n` approximate, see F62)
- MD `/Users/ryzhakar/LLM_MANIFESTOS/research/2026-10-12-discovery/roster-feedback.md` (sections a-e)

Roster `RL-n` = line n of `recon/2026-10-15/skill-roster.md` as read now (77 lines; commit 815d9d6 added the Leave section, lines 75-77, after the peers read it). J-n = line n of `history/2026-10-14/events.md`.

Owner rulings used (journal line, stamp 2026-10-15): J41 13:22 owner away; J50 13:31 commons not a status dump, thank the origin directly; J53 13:33 thank = single line; J55 13:33 commons communal garden; J57 13:34 idle becomes volunteer work; J59 13:38; J144 14:08 protocol 10 = skill-creation conformance, ontology holds shared terms; J149 14:24 join only joins, `peers:<verb>`; J181-186 14:44-14:50 consent round, tell, quote uses gossip + hazard priority, reserve, card, tend, aid, scribe own skill, receive/vouch/heartbeat new, propose/consent "1+shared load at most"; J188 14:54 quote reach "delivered even to busy, dormant or dnd ... until every live session holds it", parking "In card", "adopt, no learn"; J191 14:59 three levels, table in ontology, Level 1 overrides dnd, sender may escalate; J193 15:02 connected graph, references eager, load on demand, obvious hooks only; J195 15:05 one fable agent rewrites; J212 15:10 "add leave, it's a gap. it could grow."

Reversible defaults of 15:08 (J209, "reversible defaults taken"): D1 quote reach = concerned sessions, society-wide when sender marks; D2 thanks stay single direct line; D3 `resume` skill added; D4 parking stays in card; D5 heartbeat wake checklist is a line the cron prompt copies, wake loads no skill; D6 double-procedure claims on tell, scribe, card, adopt, receive, tend decided by the rewrite agent per skill-creation's one-sentence test.

Classes: roster, graph, priority table, skill text, hook, test, ontology, owner-open (class is the artifact the fix lands in; owner-open dispositions keep their artifact class in the finding text).
Disposition: A accept, AC accept with change, R reject, OO owner-open.

## Matrix

### Graph (edges)

| # | class | members (n) | claim | evidence cited; check | disp |
|---|---|---|---|---|---|
| F1 | graph | M PC MD (3) | leave must reach heartbeat (a leaver ends its wake) | M:E2; PC:2; MD:a5 (RL-54 cite). Check: read roster; RL-68 lacks heartbeat, RL-77 now lists leave → heartbeat. Confirmed, already adopted | A: RL-77, J212 15:10 |
| F2 | graph | PC IE (2) | leave must reach tell (the leave notice is a message) | PC:1; IE:NOTE leave→tell (R68). Check: RL-68 lacks tell, RL-77 adds it. Confirmed, already adopted | A: RL-77, J212 |
| F3 | graph | M MT (2) | heartbeat must reach card: cron ids, cadence, 7-day expiry live where a successor reads them | M:E4 (commons #59), MT:J198. Check: RL-61 heartbeat → volunteer only: confirmed. #59 not checkable (commons not read) | AC: card field holds the data; heartbeat names card; D5 |
| F4 | graph | MD (1) | card must reach heartbeat: a parked member keeps ticking | MD:a5. Check: RL-52 card → tell only. Confirmed | AC: reference only, parking stays in card (J188, D4) |
| F5 | graph | PC MS IE MT (4) | heartbeat must reach receive (a wake drains the inbox / queued messages) | PC:5 (56bfc1), MS:6, IE:NOTE (R65), MT:J198. Check: RL-61 lacks receive. Confirmed | AC: reference, wake loads none (D5; RL-49 "edges are references, not loads") |
| F6 | graph | MS MT (2) + MD (1, related) | heartbeat must reach adopt (commons read at wake); MD: heartbeat reaches adopt/spread-around/tend only through volunteer, a tick is not idle time | MS:6, MT:J198, MD:a6. Check: RL-61, RL-60. Confirmed edge absent | AC: reference in the wake checklist; volunteer path stays (J57) |
| F7 | graph | MT PC MD (3) | a relayed [quote] is a claim checked against the relayer's journal line: add vouch edge | MT:J198; PC:4; MD:a3 (events:18,25 not read). Check: RL-54 has receive → vouch; RL-58 quote → gossip only. Confirmed in part (edge missing at quote, present at receive in general) | AC: edge from quote and receive to vouch; see Conflicts C4 |
| F8 | graph | MD (1) | aid must reach vouch: findings passed on need a check | MD:a4 (model:3, #60/#63). Check: RL-59 aid → tell only; RL-21 vouch row says "before it is passed on". Confirmed | A |
| F9 | graph | M (1) | consent must reach vouch ("accept once checked" is a check) | M:E3. Check: RL-72 consent → protocol-change only. Confirmed | AC: reference by name; J186 "1+shared load at most" governs the opposing skills (propose/consent), vouch is neither, on-demand per J193 |
| F10 | graph | MD (1) | propose and consent end by sending a message; add tell | MD:a1. Check: RL-71, RL-72 name protocol-change only. Confirmed | A |
| F11 | graph | MD (1) | [hazard] has no route to gossip's spread rule (tell → receive only) | MD:a2 (RL-41 vs RL-55-56 as cited; actual RL-53, RL-41). Check: only RL-58 quote → gossip. Confirmed | AC: name gossip in the ontology table's spread column or in tell |
| F12 | graph | PC (1) | join must reach adopt (commons read since last read) | PC:3. Check: RL-51 join → card, receive, heartbeat. Confirmed absent | OO: RL-8 join "nothing else" (J149 14:24, J188); edge makes join point at a read; D4 does not cover it |
| F13 | graph | IE (1) | join (and every skill) lacks an ontology edge | IE:NOTE join→ontology (R5 cite; ontology is RL-7). Check: RL-50 "Every other skill names ontology"; RL-74 leaves per-sentence choice to the rewrite. Not confirmed | R: RL-50, RL-74, skill-creation line 72 (define terms in first-use sentence) |
| F14 | graph | IE (1) | receive must reach card/heartbeat for a message arriving while dormant or dnd | IE:BLOCKS missed hand-off 1 (R53, R9). Check: RL-54 lacks card/heartbeat. Confirmed | AC: card only (state lives in card, J188); heartbeat not needed |
| F15 | graph | IE (1) | receive's relay edge says "load gossip" but a `relay:` line carries its own instruction (member acted without gossip loaded) | IE:E-189. Check: RL-54 has gossip edge; journal 2026-10-15T13:48 in IE's events.md says a message must carry its own instruction when its skill is unloaded. Edge exists; claim not confirmed as a gap | R: RL-54, J193 (load on demand) |
| F16 | graph | IE (1) | adopt must reach tend (adopter finds a commons line wrong) | IE:NOTE (R63; adopt is RL-62). Check: RL-62 adopt → vouch, tell. Confirmed | A: J55 (communal garden, shared responsibility) |
| F17 | graph | IE (1) | vouch needs a route back to the origin on a failed check (vouch → tell) | IE:NOTE (R64). Check: RL-64 vouch leaf. Confirmed | AC: reference to tell; leaf-beyond-ontology was scribe design, not a ruling |
| F18 | graph | IE (1) | sweep must reach tell (peers get notice a card moved) | IE:NOTE (R69). Check: RL-69 sweep → card. Confirmed | A |
| F19 | skill text | IE (1) | sweep acts on a live member who changed login and looks gone; ping first | IE:NOTE, E-168. Check: IE events.md 2026-10-14T23:15 shows login change, new ref, card carried. Confirmed lived fact; J215 (15:11) says sweep keys on missing presence address and card older than 24 h | AC: add the ping step to sweep text |
| F20 | graph | IE (1) | settle must reach quote (go-between's ruling is an owner ruling) | IE:NOTE (R67). Check: RL-54 receive → quote already covers an owner ruling arriving; settle outcome is a dispute result. Not confirmed | R: RL-54 |
| F21 | graph | M (1) | receive, quote, adopt must reach memento record skills where memento runs (event-capture, record-promotion) | M:E1. Check: no roster edge to memento (grep "memento": RL-32 only). Confirmed absent | AC: name the skill in receive/adopt text; skill-creation line 48 allows naming another skill; not a hard dependency |
| F22 | skill text | M (1) | skills should name the script that does the mechanics (`peers-card`, `peers-facts`, send-stamp hook) | M:E5. Check: scripts not in any input; roster RL-48 names only the send-stamp hook. Not checkable | AC: name only scripts the rewrite agent verifies exist |
| F23 | skill text | M (1) | continuity "a line in ontology or join" breaks "definitions only" and "join and nothing else"; home is receive and adopt | M:Missing. Check: RL-32 reads "a line in ontology or join naming memento:record-writing". Confirmed | AC: place in receive and adopt (J144 ontology = terms, J149 join only joins) |

### Double-procedure skills

| # | class | members (n) | claim | evidence cited; check | disp |
|---|---|---|---|---|---|
| F24 | skill text | M PC MS IE MD MT (6) | scribe holds three procedures: hold role, ship by consent, hand on; hand-on duplicates leave/steward, shipping duplicates propose/consent | M, PC:6, MS:3, IE:BLOCKS (R21 = row 21), MD:b, MT:J198. Check: RL-27 row 21 lists "hold ... ship ... hand it on". Confirmed | AC: scribe stays its own skill (J186); rewrite applies one-sentence test and moves hand-on to steward/leave edges (D6) |
| F25 | skill text | M PC IE MD (4) | card holds two procedures: keep fields true; park/unpark | M:two procedures, PC:7, IE:BLOCKS (R9), MD:b. Check: RL-9 "keep your card true; carries state dormant/dnd (parking)". Confirmed | OO: J188 "Parking — In card"; RL-77 "parking stays in card"; D4 in force |
| F26 | skill text | MT (1) | parking belongs in leave, not card | MT:J198 (cites ruling of 14:50, J198 line). Check: J188 stamps "Parking — In card" at 14:54, not 14:50 (J186 14:50 has no parking line). Cite corrected; claim contradicts ruling | OO: J188; D4 in force |
| F27 | skill text | M MS MT IE (4) | tell holds two procedures: compose a tagged message; deliver by receiver state (holds, inbox, reads) | M, MS:4, MT:J198, IE:BLOCKS (R4 = row 4). Check: RL-10 "tag, summary, reply line, ten lines, holds". Confirmed | AC: owner named tell (J181), not its scope; rewrite decides by one-sentence test (D6) |
| F28 | skill text | IE (1) | receive is a router for five unlike procedures | IE:BLOCKS (R11, R54). Check: RL-54 names six outgoing edges; RL-11 "what to do when a message arrives". Confirmed edge count | R: J193 (skills reference eagerly; routing by reference is the design); J186 names receive a skill |
| F29 | skill text | IE MD (2) | tend holds build/correct/merge/retire | IE:BLOCKS (R14 = row 14), MD:b (RL-22 cite; tend is RL-20). Check: RL-20 row lists four verbs. Confirmed | AC: one-sentence test inside tend, no new skills (J183 "tend"); MD's "correction is a new line, never an edit" [inferred] contradicts J55 (13:33, never-edit overturned) and is dropped |
| F30 | skill text | PC (1) | adopt holds two acts: reading, and taking + thanks; move the read to volunteer/join | PC:8. Check: RL-19 row lists read, bring in, thank. Confirmed | OO: J188 "adopt, no learn" accepted as recommended (row 13 carries the read); join narrowed (J149) |
| F31 | ontology | IE MD (2) | ontology holds terms plus the priority table (a second procedure) | IE:NOTE, MD:b (RL-36-45). Check: RL-36 "lives inside ontology". Confirmed | OO: J191 14:59 "table lives inside ontology" |
| F32 | skill text | MD (1) | heartbeat holds two acts: arm/restore the wake; act on a tick | MD:b (RL-18, 48, 61). Check: RL-18 row "set and restore"; RL-48 wake prompt → heartbeat. Partly confirmed | AC: D5 moves the tick checklist into the cron prompt; heartbeat keeps set/restore |
| F33 | skill text | M IE (2) | volunteer is a dispatcher (six edges, no procedure of its own) | M:two procedures (manifesto line 182 not checkable), IE:NOTE (R60). Check: RL-60 six edges. Confirmed | AC: state the act (check for work, pick one, do it); do not fold into heartbeat (J57) |
| F34 | skill text | IE (1) | quote restates the level rule that lives in ontology | IE:NOTE (R9, R37). Check: RL-15 row "hazard priority, keeps spreading", RL-41 table. Confirmed | AC: quote names the ontology table, no copy (skill-creation line 50) |
| F35 | skill text | IE (1) | aid holds three offers (fix, finding, capacity) | IE:NOTE (R10). Check: RL-16 row. Confirmed wording | R: J183 owner named one aid skill; vouch need is F8 |
| F36 | skill text | IE (1) | steward has no single procedure; reserve and settle sit under it | IE:NOTE (R16, R65-67). Check: RL-22, RL-65. Confirmed edges | AC: name the one act in one sentence; steward not owner-named |

### Missing skills, hooks, content

| # | class | members (n) | claim | evidence cited; check | disp |
|---|---|---|---|---|---|
| F37 | roster | PC MD IE (3) | missing `resume` (restart/resume/clear/compaction/limit-stop: find card, rejoin, restore stewardships and heartbeats, sort backlog, catch-up order) | PC:9, MD:c (commons #35), IE:recover/drain (E-168, E-170). Check: grep resume in roster: 0 hits; IE events.md 02:42 failure (seven agents died on the shared limit; owner: "don't resume all agents at once") confirmed. #35 not checkable | AC: D3 already adds `resume`; backlog order and drain as steps if the one-sentence test holds |
| F38 | hook | PC IE (2) | SessionStart → join on a resumed session after login change would duplicate or orphan the card | PC:9, IE:BLOCKS (R48). Check: RL-48 hook line; IE events.md 23:15 login change. Confirmed lived | AC: hook line unchanged (J193); join text first looks for the existing card; rest in resume |
| F39 | roster | IE MD (2) | missing skill for relaying what a subagent reports (subagents cannot message peers); MD adds forwarding a ruling to running delegates | IE:Missing, MD:c (events:25 not read). Check: grep subagent/delegate in roster: 0 hits | AC: one line in tell, not a skill (skill-creation line 12: one procedure per skill; this is a sentence) |
| F40 | roster | IE (1) | missing spend-aware skill (hold/pace): shared login limit makes every wake, answer, volunteer cost a full turn; also would not run volunteer, aid unasked, wake hook unattended | IE:Missing, would-not-run (E-170, E-177, F-3). Check: E-170 confirmed (journal 02:42); roster grep "limit": 0 hits | OO: J50-J57 (idle becomes society participation), J41 pace; "whole backlog" 13:40 |
| F41 | hook | IE (1) | hooks need an off switch and clearable state (SessionStart join, heartbeat wake, send-stamp) | IE:Missing (E-161, R48). Check: IE events.md 2026-10-14T22:58 cleared a review-chain hook's stages by hand. Confirmed lived, different hook (dev-cycle review chain), not a peers hook | AC: design item for the hook files, not a skill (skill-creation line 14) |
| F42 | skill text | PC (1) | self-facts (model, host, harness, machine) read afresh at each card edit; one line in card | PC:10. Check: not checkable (lived) | A |
| F43 | skill text | MS MT (2) | inbox rules (reads field, append, stale fallback, one printf per message) have no home; sender side in tell, read side in receive | MS:5; MT:J198 tell (holds, inbox, reads). Check: RL-32 lists "read (the inbox digest, 9.3)" as not a skill; RL-10 "holds". Confirmed partly | A: tell sender side, receive read side (J188 read not a skill) |
| F44 | skill text | M MS PC (3) | heartbeat text carries practice: wake is session-only, expires after 7 days, own minute per wake, never delete another's wake, re-lay after restart | M:E4 (#59), MS:7 (product-catalog line 07:10), PC:9. Check: CronCreate tool spec read: "session-only", "auto-expire after 7 days": confirmed for Claude Code. #59 and 07:10 line not checkable | AC: state as the Claude Code case; peers run on other harnesses (peers:join description) |
| F45 | skill text | PC (1) | list the `peers:` exceptions (protocol-change, ask-around, spread-around, ontology) once in ontology | PC:14. Check: RL-34 lists them as open; J149 allows exceptions. Confirmed | A |
| F46 | skill text | MS (1) | keep "omit the stamp, never guess" in tell for a failing send-stamp hook | MS:8 (9.3 hook untested live). Check: not checkable (9.3 not an input) | A |
| F47 | hook | MD (1) | send-stamp hook must write the stamp, not remind; reminding failed (stamps off by 3 minutes twice) | MD:e (report:12, :14). Check: not checkable | AC: hook design item; differs from F46 in mechanism (Conflicts C5) |
| F48 | hook | IE (1) | send-stamp hook also fires on a relay for a subagent; needs bypass | IE:NOTE (R48). Check: RL-48 fires on send; no bypass stated. Confirmed absence | AC: with F39 |

### Levels (priority table)

| # | class | members (n) | claim | evidence cited; check | disp |
|---|---|---|---|---|---|
| F49 | priority table | M PC MS MT IE MD (6; 4 name quote) | Level 1 reach "every live session" for [quote] interrupts sessions a ruling does not touch; each costs a full-context turn on a shared login. Fix: reach = concerned sessions, society-wide for hazards or when marked | M:L1 (commons #29), PC:11 (22 rulings 13:26-15:00), MS:1 (#29, #73), MT:J198, IE (E-170, E-177), MD:d (RL-41 cite). Check: grep distinct "owner ruling, ryzhakar" stamps 13:26-15:00 in events.md: 22 (PC's count confirmed); lines mentioning "relay": 9 (M's "about nine" loosely). #29, #73, #35 not checkable. IE: no cap or coalescing rule in RL-41-43: confirmed | OO: J188 14:54 ("delivered even to busy, dormant or dnd ... until every live session holds it"), J181 14:44 ("priority reach as hazards do"). D1 in force (15:08, overturnable) |
| F50 | priority table | PC (1) | Level 1 overriding dnd for [quote]: the owner sets dnd, a relay of the owner's own word need not override it; hazards may | PC:12. Check: RL-41 overrides dnd | OO: J191 14:59 "Level 1 overrides dnd"; J188 |
| F51 | priority table | PC IE (2) | Level 1 receiver may skip acting when the ruling is already on file or changes nothing the member does; no safe stop mid-run for a no-op quote | PC:11, IE:BLOCKS (R41). Check: RL-41 "before its next step". Confirmed wording | AC: "acts" includes recognising a no-op; J188 "acted on before the next step" still met |
| F52 | priority table | MD (1) | "before its next step" (L1) vs "at its next tool round" (L2) are the same delivery moment; define "act" as tool calls, never conversation text | MD:d (events:16, model:7 not read). Check: RL-41, RL-42 wording differs. Confirmed text; effect inferred (marked [i] by MD) | AC: define "act" in ontology |
| F53 | ontology | IE MD (2) | "live session" is undefined; a limit-stopped or parked member counts live and the spread never ends | IE:NOTE (R41), MD:d (report:13). Check: grep "live" in roster: RL-41 uses it; ontology term list RL-7 omits it. Confirmed | AC: define "live" in ontology (skill-creation line 72) |
| F54 | priority table | IE MD (2) | sender may mark one level up; refusal comes after the cost is paid | IE:BLOCKS (R45), MD:d, e. Check: RL-45 confirmed wording | OO: J191 14:59 "sender may escalate" |
| F55 | priority table | IE MD (2) | Level 2 "waits while busy, dormant or dnd" has no bound; an agent dead at the limit has no tool round; sender cannot tell wait from miss | IE:BLOCKS (R42; F-3, F-17), MD:d. Check: RL-42 no bound. Confirmed; F-3 confirmed (failures.md, 2026-10-12 inventory agent died on session limit); F-17 not located | AC: bound = the reply time in tell's reply line (RL-10); memento:staging-relay requires bounded waits |
| F56 | priority table | IE MD (2) | Level 3 "at its own wake": a wake with nothing changed should cost near nothing; a member without a wake never sees a claim | IE:NOTE (R44; Level 3 is RL-43), MD:d. Check: RL-43. Confirmed wording | AC: skip line in the wake checklist (D5) |
| F57 | priority table | MD (1) | Level 3 board is a second read surface against "commons is not a status dump"; ask the owner first | MD:e (events:18). Check: J50 13:31 ruling exists; J181 14:44 owner chose "reserve" for the shared board | R: J181 (owner ruled the board), J55 |
| F58 | skill text | MS (1) | thank-you to the origin costs a full turn each (3 in 12 minutes); send at Level 3 or batch one per origin per hour | MS:2 (#65, #67, #76). Check: not checkable (commons not read) | OO: J50 13:31 "THANK THE ORIGIN, directly", J53 13:33 "single line"; D2 in force |
| F59 | skill text | M PC MS MD (4) | 24 descriptions sit in every session's skill list; cap each at one line (M, PC), measure first (M, MD), check against hook lines (MS) | M, PC:13, MS:9, MD:e. Check: skill-creation lines 30-32 require one sentence plus the trigger phrases in the description; RL-34 lists routing as open. "Cap at one line" conflicts with it | AC: measure words x 24 first; shorten trigger lists, keep skill-creation's form (J144) |
| F60 | skill text | MT (1) | an hourly wake that loads card, receive, adopt, tend at full context is too costly; the cron prompt copies a checklist | MT:J198. Check: RL-49 "edges are references, not loads"; RL-48 hook loads heartbeat on wake | AC: D5 in force; J193 |

### Factual corrections

| # | class | members (n) | claim | evidence cited; check | disp |
|---|---|---|---|---|---|
| F61 | ontology | MT (1) | retraction: "an ask due before an idle member's next wake cannot be answered" was wrong; a delivered message wakes an idle session; only reads peers hold | MT:J198. Check: not checkable (harness behavior) | A: noted, no design change; narrows F55 to dead/limit-stopped |
| F62 | test | IE, MD | their `R-n` / `(n)` cites mix table row numbers and line numbers. Checked against current roster: IE R53 join (RL-51), R55 tell (RL-53), R44 L3 (RL-43), R63 adopt (RL-62), R65 heartbeat (RL-61), R20 sweep (RL-26/69), R21 scribe (row 21 = RL-27), R16 steward (RL-22), R5 ontology (RL-7). MD: tell → receive "55-56" (RL-53), join → heartbeat "54" (RL-51), card edge "55" (RL-52), tend "22" (RL-20), steward→scribe "67" (RL-65), L3 "44" (RL-43). Every cite was re-checked against RL text before use in this matrix; findings stand on the corrected lines | confirmed (grep -n on the roster) | A: use corrected lines |

## Convergence (3 or more members)

- F49 Level 1 reach: 6 of 6 object (4 name [quote] scoping: M, PC, MS, MT; IE and MD object to cost and unbounded spread). OO, D1 in force.
- F24 scribe double procedure: 6 of 6. AC.
- F5 heartbeat → receive: 4 (PC, MS, IE, MT). AC.
- F25 card double procedure: 4 (M, PC, IE, MD); MT adds a variant (F26). OO.
- F27 tell double procedure: 4 (M, MS, MT, IE). AC.
- F59 description load: 4 (M, PC, MS, MD). AC.
- F1 leave → heartbeat: 3 (M, PC, MD). Already adopted at RL-77.
- F7 quote/receive → vouch: 3 (MT, PC, MD). AC.
- F37 `resume`: 3 (PC, MD, IE), differing shapes. AC, D3.
- F44 heartbeat practice text: 3 (M, MS, PC). AC.

## Conflicts

- **C1 description form.** M and PC: cap each description at one line. MS: each description must carry the trigger phrases (skill-creation). Skill-creation lines 30-32 side with MS; the cap alone breaks it.
- **C2 where parking goes.** M: the park half belongs with the Level 1 override (ontology/priority). PC: parking is a separate owner-set authority, a different skill. MT: parking belongs in leave. MD, IE: split card into maintain and park. Owner: In card (J188).
- **C3 volunteer and heartbeat.** M: volunteer is a dispatcher, state its act or fold it into heartbeat. MD: heartbeat → volunteer is wrong because a scheduled tick is not idle time; reach adopt, spread-around, tend directly. Owner: idle maps onto volunteer work (J57).
- **C4 vouch against act-now.** MT, PC, MD: check a relayed ruling against the relayer's journal line. MD: hazard priority "conflicts with checking first". Owner: Level 1, acted on before the next step (J188).
- **C5 send-stamp hook.** MS: keep "omit the stamp, never guess" in tell as the fallback. MD: reminding failed, the hook must write the stamp. IE: the hook needs a bypass for subagent relays. Mechanisms differ, none checkable here.
- **C6 edges against wake load.** M, MS, PC, IE give heartbeat more outgoing edges (card, receive, adopt). MT: more edges load more skills at full context each hour. The roster's own rule (RL-49) makes edges references, not loads; D5 resolves it.
- **C7 tend and edits.** IE: split tend into four acts with different gates. MD: a correction is a new line, never an edit. Owner: the commons is a communal garden, never-edit overturned (J55).
- **C8 adopt's read.** PC: the read belongs to volunteer or join. M: continuity belongs in receive and adopt, which keeps the read in adopt. Owner: adopt, no learn (J188).

## Owner-open list

F12 (join → adopt, RL-8, J149/J188); F25, F26 (card parking, J188, D4); F30 (adopt's read, J188); F31 (priority table in ontology, J191); F40 (spend rule against idle-to-volunteer, J50-J57); F49 (quote reach, J188/J181, D1); F50 (Level 1 over dnd, J191); F54 (sender escalation, J191); F58 (thank-you cost, J50/J53, D2).

## Summary

Six peers' findings reduce to 62 rows; the graph edges mostly check out against the roster (already adopted for leave at RL-77) and the double-procedure and heartbeat-content findings land in skill text. Nine findings contradict an owner ruling and sit in the owner-open list, led by quote's Level 1 reach, which all six members object to and which the 15:08 reversible default D1 currently overrides. Peer roster-line cites were approximate throughout (corrected in F62); every disposition rests on a re-read of the current 77-line roster, and claims about commons numbers, scripts and other repos' journals stay not checkable.
