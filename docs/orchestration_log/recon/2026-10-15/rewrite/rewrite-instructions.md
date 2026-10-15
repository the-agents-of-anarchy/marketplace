# Instructions: rewrite the peers skills for protocol 10

Reader: the single fable agent the owner ruled does this rewrite (Ev:195). Bind first, by `writing-stack.md` in this directory; never edit a file before your binding report is out.

Keys:
- `J9:<n>` is a line of 9.3 join: `git -C /Users/ryzhakar/pp/agents-of-anarchy-marketplace show main:peers/skills/join/SKILL.md`.
- `G9:<n>` is a line of 9.3 gossip: `… show main:peers/skills/gossip/SKILL.md`.
- `DJ`, `DG`, `DA`, `DT` are lines of the draft at commit ec3d72f: `peers/skills/{join,gossip,amend,tend-commons}/SKILL.md`. Read them in your worktree before your first edit.
- `CH:<n>` is a line of `/Users/ryzhakar/pp/agents-of-anarchy-marketplace/docs/orchestration_log/recon/2026-10-15/protocol-10-changes.md`.
- `Ev`, `RO`, and `SC` are as defined in `writing-stack.md`.

Records directory (written `<rec>` below): `/Users/ryzhakar/pp/agents-of-anarchy-marketplace/docs/orchestration_log/recon/2026-10-15/rewrite/`.

## (a) Outcome and where the work lives

Outcome: the peers plugin carries the 24 skills of `RO:5-30`. Every skill passes every rule of section (d), and `just test` exits 0. Every 9.3 instruction sentence and every A–H change is traced to one new skill, or dropped with its reason.

1. Create the worktree with `git -C /Users/ryzhakar/pp/agents-of-anarchy-marketplace worktree add -b draft/10-skills /Users/ryzhakar/pp/aoa-skills draft/9.4-participation`; never branch from `main`.
2. Do every edit inside `/Users/ryzhakar/pp/aoa-skills`; never edit `/Users/ryzhakar/pp/aoa-participation`.
3. Commit on `draft/10-skills` and push it to `origin draft/10-skills`; never commit to, check out, or push any other branch.
4. Leave `main` as it is; never touch it.
5. Leave the pointer `<root>/PROTOCOL.md`, every card in `<root>/members/` and `<root>/departed/`, and the commons under `<root>` as they are; never write under `<root>`.
6. Leave the plugin version `0.7.0` in `peers/.claude-plugin/plugin.json` and `.claude-plugin/marketplace.json` as it is (CH:3); never change a version.
7. Write your three records into `<rec>`: `traceability.md`, `self-audit.md`, and `protocol-10-skills-changes.md`. Never write another file there.

## (b) The 24 procedures and their sources

Each skill opens from the one-sentence procedure below (SC:10). Take its instructions from the source lines listed. "Edges" are the skills it names; see (f).

A source line marked `→ prov.` sits in `ontology` provisionally: no roster skill holds it. List each one as an open item; never give it a home of your own.

1. **ontology**
   - Procedure: Read every term the society's skills use as this skill defines it.
   - Sources:
     - J9:31, J9:59, J9:63-93, J9:105-123, J9:233 (the tag set), J9:299 (rewritten per Ev:183), J9:363 (steward), J9:373 (go-between), J9:375 (exclusive resource, resource board), J9:425 (pointer), J9:483 (culture);
     - DJ:125 (recurring wake), DJ:213 (`dnd`), DJ:307, DJ:321, DJ:405 (scribe);
     - DG:9 (gossip), DG:85 (spread);
     - RO:36-45; Ev:47, Ev:48, Ev:183, Ev:195.
   - Provisional sources:
     - the purpose lines J9:11-17 and J9:21-27, with DJ:21 (change D);
     - the owner stance J9:33-55, with DJ:37, DJ:39, DJ:43 (change A);
     - continuity J9:419-421 (RO:32 places it "in ontology or join"; join is narrowed by Ev:149).
   - Edges: none (RO:50, a leaf).
2. **join**
   - Procedure: Become a member of the society on learning of it.
   - Sources: J9:141-175; DJ:131-165.
   - Edges: card, receive, heartbeat.
3. **card**
   - Procedure: Keep your own card true and current.
   - Sources: J9:9 (version, per writing-stack tension 6), J9:95-101, J9:179-229, J9:517-519; DJ:97-103, DJ:169-219, DJ:423-427 (`dnd`); Ev:188 (parking lives in the card).
   - Edges: tell.
4. **tell**
   - Procedure: Send a peer a tagged message.
   - Sources:
     - J9:61, J9:233, J9:235, J9:239, J9:247-261, J9:265, J9:267, J9:271-277, J9:281;
     - J9:347 (merged into J9:267);
     - DJ:63, DJ:223-229, DJ:237-259, DJ:263-273, DJ:333 (merged);
     - Ev:181.
   - Edges: receive.
5. **receive**
   - Procedure: Act on a message that arrives.
   - Sources: J9:237, J9:241-245, J9:263, J9:279, J9:285, J9:355-357; G9:39-49; DJ:227, DJ:231-235, DJ:255, DJ:271, DJ:277, DJ:335-337; DG:89-99.
   - Edges: adopt, vouch, tell, gossip, quote, consent.
6. **gossip**
   - Procedure: Pass a message from peer to peer past anyone its origin could name, inside the envelope.
   - Sources: G9:9, G9:13, G9:61, G9:65-69; DG:9, DG:11, DG:15, DG:17, DG:45-55, DG:59-83; Ev:78, Ev:93, Ev:165.
   - Edges: ask-around, spread-around, tell.
7. **ask-around**
   - Procedure: Seek what you need from peers you cannot name, by gossip.
   - Sources: G9:19, G9:23, G9:27, G9:31-35; DG:13 (the `[ask]` half), DG:19, DG:23-33; Ev:47, Ev:183.
   - Edges: gossip, tell.
8. **spread-around**
   - Procedure: Offer what you learned to the peers it may help, by gossip where you cannot name them.
   - Sources: G9:53-57; DG:13 (the `[notice]` half), DG:37-41; J9:349-353, J9:359; DT:45-51; Ev:183, Ev:186.
   - Edges: gossip, vouch, tell.
9. **quote**
   - Procedure: Relay an owner ruling until every live session holds it.
   - Sources: J9:411-415; DJ:391-395; Ev:181, Ev:188; RO:37, RO:41.
   - Edges: gossip.
10. **aid**
    - Procedure: Offer a peer a fix, finding, or capacity it lacks, unasked.
    - Sources: J9:289-293; DJ:281-285; Ev:183.
    - Edges: tell.
11. **volunteer**
    - Procedure: Turn time free of your own work into work for the society.
    - Sources: DJ:291-297; Ev:49, Ev:54, Ev:57.
    - Edges: ask-around, spread-around, adopt, tend, aid, heartbeat.
12. **heartbeat**
    - Procedure: Keep a recurring wake set across restarts.
    - Sources: DJ:299-303; Ev:49; RO:18, RO:48. The Claude Code means stays in ontology's mapping tag (DJ:125).
    - Edges: volunteer.
13. **adopt**
    - Procedure: Bring what a peer built into your own work by your own act, thanking its origin.
    - Sources:
      - J9:325, J9:327, J9:331, J9:337-345;
      - J9:333 (replaced by DJ:319, change F);
      - DJ:313-319, DJ:323-331;
      - Ev:48, Ev:50, Ev:53, Ev:190.
    - Edges: vouch, tell.
14. **tend**
    - Procedure: Build, correct, merge, and retire what the commons holds.
    - Sources: J9:301-323, J9:329, J9:335; DJ:309-311; DT:13-41; Ev:55, Ev:183.
    - Edges: vouch, spread-around.
15. **vouch**
    - Procedure: Check a claim before you believe it, act on it, or pass it on.
    - Sources: J9:19, J9:283; DJ:19, DJ:275; Ev:160, Ev:186.
    - Edges: none beyond ontology.
16. **steward**
    - Procedure: Look after a shared thing for every session, in the open.
    - Sources: J9:295, J9:363-373, J9:389-397, J9:515; DJ:287, DJ:343-353, DJ:369-377, DJ:421.
    - Edges: reserve, settle, scribe.
17. **reserve**
    - Procedure: Hold an exclusive resource by its own line on the resource board.
    - Sources: J9:375-387; DJ:355-367; Ev:181.
    - Edges: tell.
18. **settle**
    - Procedure: Take a contested matter to a go-between.
    - Sources: J9:401-407; DJ:381-387.
    - Edges: tell, steward.
19. **leave**
    - Procedure: Leave the society when the owner ends your session.
    - Sources: J9:505-507; DJ:411-413.
    - Edges: card, steward, scribe, sweep.
20. **sweep**
    - Procedure: Move a gone member's card into `<root>/departed/`.
    - Sources: J9:509-513 (the protocol-8 clause is dropped, CH:209); DJ:415-419.
    - Edges: card.
21. **scribe**
    - Procedure: Serve as the scribe, from taking the role to handing it on.
    - Sources:
      - J9:425-429, J9:461-471, J9:481, J9:489-501;
      - DA:13-17, DA:49-59, DA:69, DA:77-89;
      - DJ:405;
      - Ev:113-114, which void the major-bump approval in J9:467 before 1.0.0.
    - Edges: propose, protocol-change.
22. **protocol-change**
    - Procedure: Know the round every party to a protocol change shares.
    - Sources: J9:443, J9:449-459, J9:473-479, J9:483-485; DA:31, DA:37-47, DA:61-67, DA:71-73; Ev:186, Ev:188; RO:33.
    - Edges: none. It names neither `propose` nor `consent` (RO:73).
23. **propose**
    - Procedure: Bring a protocol change to the society as a draft.
    - Sources: J9:431-441; DA:19-29.
    - Edges: protocol-change.
24. **consent**
    - Procedure: Answer a protocol draft with your acceptance or your objection.
    - Sources: J9:445-447; DA:33-35.
    - Edges: protocol-change.

Dropped with reason. Carry each into the traceability table.
- J9:126-138 and the protocol-8 clause of J9:509: I-10 trim, case on record (CH:205-209).
- J9:269 and DJ:261: replaced by the edges receive → gossip and volunteer → ask-around and spread-around, and by gossip's description (RO:54, RO:60).
- G9:11, G9:15, G9:17, G9:25, G9:29, G9:59, G9:71: removed by change H (CH:130-133). The removals are fan-out and stop rules, the gain gate, and the `asked:` list.
- DJ:339, DJ:407, DA:9, DT:9: pointers replaced by the reference graph and by ontology (RO:47-73; Ev:144).
- The bare version statement J9:9 and DJ:9: writing-stack tension 6.

Procedure:
1. Settle each skill's procedure sentence above before you write a line of it (SC:10); never write a skill from another sentence.
2. Write each skill as `peers/skills/<name>/SKILL.md`, with the directory equal to `name` (SC:18, SC:28); never keep a draft skill directory that the roster lacks.
3. Remove the directories `amend` and `tend-commons` once their sentences are traced (RO:5-30); never leave a stale skill.
4. Merge two source sentences that state one instruction into one, recording `merged into` in the table; never carry both.
5. Split a source sentence that holds a definition and an instruction, sending the definition to ontology and the instruction to the skill whose act it is; never keep the two together.
6. Map each trigger phrase of the draft descriptions to the one new description whose procedure it matches. The sources are DJ:4-5, DG:4-5, DA:4-5, and DT:4-5. Never drop a trigger phrase silently.
7. Keep `join`'s description naming "agents that share a project, a machine, or neither, on any harness", as `peers/tests/test_skills.py:105-111` pins; never remove that phrase.

## (c) Traceability table

1. Write `<rec>traceability.md` as one Markdown table with one row per source sentence; never let a row hold two sentences.
2. Cover every instruction sentence of J9 and G9, every line that changes A–H altered or added (CH:28-163), and every trigger phrase of the draft descriptions; never skip a line.
3. Give each row these columns: `source` (key:line), `opening words` (the first six words), `change` (A–H, I-10, I-15, I-16, or `—`), `new skill`, `new line` (number in the new `SKILL.md`), `status` (`moved`, `rewritten`, `merged into <key:line>`, `split`, `dropped`, or `open`), and `ground` (the Ev, RO, CH, or SC line that sets the status).
4. Map every row to exactly one new skill, or mark it `dropped` or `open`; never map a row to two skills.
5. Ground every `dropped` row in an owner ruling, a skill-creation rule, a case on record, or "no step of any procedure needs it"; never drop a row without a ground.
6. Update the table in the commit that moves its sentences; never let the table lag the skills.

## (d) Writing rules — run on every skill before reporting

Verbatim from SC:10-80. One clause is void by owner ruling, as marked.

- [ ] Name the one procedure the skill performs, in a sentence, before writing a line; never write from an unnamed procedure.
- [ ] Cover one procedure per skill; never cover a second.
- [ ] Write a skill where reading it does the work; never where the work happens without reading.
- [ ] Name the new skill's file `SKILL.md`; never name it otherwise.
- [ ] Open the skill with YAML frontmatter — the block between `---` lines — carrying `name` and `description`; never omit either.
- [ ] Never carry a version field in the frontmatter.
- [ ] Take `name` from the procedure named above — two or three lowercase parts, hyphen-joined, naming what it does; never carry a fourth part. (Part count VOID, Ev:149. Take the name from RO:5-30.)
- [ ] Set the directory name to `name`; never let the two differ.
- [ ] Write `description` as one sentence naming what the skill does, followed by the phrases and conditions a request matches; never merge the two into one sentence.
- [ ] Put every phrase and condition a request matches in the description; never put one in the body — everything below the frontmatter.
- [ ] Structure the body in XML tags; never structure it another way.
- [ ] Name each tag as an imperative verb phrase; never name a tag for its content alone.
- [ ] Carry every instruction — one thing to do or refuse — in tag content; never carry one outside a tag.
- [ ] Carry a tag's whole meaning in its content; never give a tag an attribute.
- [ ] Inside a tag write prose and inline backticks; never write anything else.
- [ ] Order the body as the procedure runs; never depart from that order.
- [ ] Keep everything the skill needs inside it for one read; never point outside it to fetch, except by naming another skill.
- [ ] Move what two skills both need into a third skill; never copy shared content into two skills.
- [ ] Reference another skill by name; never by its path.
- [ ] Write one instruction per sentence; never spread one across two.
- [ ] Write every instruction as a command; never as a suggestion.
- [ ] Cap each sentence at one emphatic word — `never`, `always`, `only`, `must`; never carry two.
- [ ] Count an emphatic word where it commands; never where backticks quote it.
- [ ] Pair every positive instruction with the prohibition of that same instruction; never pair it with the prohibition of another concern.
- [ ] State the instruction; never argue for it.
- [ ] Name what the skill requires; never narrate a failure to meet it.
- [ ] Hold one term per concept from its first use; never introduce a second term for a concept already named.
- [ ] Define every term outside ordinary English, the file system, Markdown, YAML, and XML — and every common word carrying a narrow sense — in the sentence that first uses it; never leave one undefined. (Resolved for shared terms by writing-stack tension 3.)
- [ ] Write anything a person will read in ordinary words; never in words that person would not use.
- [ ] Keep every sentence that instructs or forbids; never keep another.
- [ ] Read the finished skill against every instruction above; never deliver a skill that breaks one.

Checks the audit found most often (`recon/2026-10-15/skill-audit.md:32-39`):
- A `never` half that forbids another concern.
- Two instructions joined by "and" or "then".
- "except as the next instruction" chains.
- Two emphatic words in one sentence.
- One concept under two words. Examples: origin/originator, ask/request, item/line, receiver/recipient.

## (e) The ontology skill

1. Hold in ontology every term two or more skills use; never define such a term in another skill (Ev:144; writing-stack tension 3).
2. Open every other skill's first tag with one instruction naming the skill `ontology` as the source of its terms (RO:50); never restate an ontology definition elsewhere.
3. Write each definition as an instruction, `Call <x> <definition>; never call <y> <x>`, after J9:81; never write a bare statement.
4. Carry at least these terms:
   - **commons**: a location under `<root>` in which the society builds what it chooses, of any complexity. `<root>/commons.md` is one thing built there, not the commons itself (Ev:183, Ev:184). It is public space every member tends (Ev:55). It is not a status board (Ev:50).
   - **pointer**: `<root>/PROTOCOL.md`, a protocol location naming the current version and one dated change line per version (J9:425; Ev:195-196).
   - **resource board**: `<root>/resources.md` (J9:375). It is a location beside the commons, the cards, and the pointer.
   - **push**: carrying knowledge to a peer whose work it helps, by a direct send or by gossip (Ev:93, Ev:173).
   - **pull**: seeking knowledge by a direct `[ask]` to a peer who holds it, or by a gossip `[ask]` (Ev:47).
   - **adoption**: bringing what a peer built into your own work by your own act. It owes a one-line thank-you to its origin (Ev:50, Ev:53; DJ:319).
   - **diffusion**: adoption. Knowledge counts as spread once a peer adopts it (Ev:48; DJ:321; DG:85). Never count a send, read, relay, or citation as spread.
   - **owner**: J9:31.
   - **steward**: the member whose card's `stewards` names a shared thing it looks after for every session (J9:363). A stewardship is a service, not property (J9:369).
   - **scribe**: the member whose card's `stewards` lists `protocol`, keeper of the protocol text (DJ:405). The test pins the phrase "`stewards` lists `protocol`" (`test_skills.py:99-102`).
   - **message types**: `[hazard]`, `[ask]`, `[answer]`, `[notice]`, and exactly one new type, `[quote]`, an owner ruling relayed (RO:37). Ask-around and spread-around use `[ask]` and `[notice]` with the gossip envelope, and add no type (RO:37).
   - **the priority table**, as one tag of three prose sentences, one per level (writing-stack tension 4), carrying RO:39-43:
     - Level 1, act now: `[hazard]` and `[quote]`. Reach: every live session. Overrides busy, waiting, dormant, and dnd. The receiver acts before its next step. It spreads until every live session holds it.
     - Level 2, attend: `[ask]`, `[answer]`, `[notice]`. Reach: the peers the sender or `spread:` names. Overrides nothing, and waits while the receiver is busy, dormant, or dnd. The receiver acts at its next tool round. It spreads as `spread:` says.
     - Level 3, board: commons lines and resource lines. Never sent; read in place. The receiver acts at its own wake. It does not spread.
   - **escalation**: a sender may mark a message one level above its type's level, stating the reason. A receiver may refuse and report the misuse. Adding a type or a level is a protocol change (RO:45).
   - Every term J9:59-93 defines: main session, member, member id, body, address, harness, host, harness-ref, presence and its states, live, gone, leave notice, peer, delivery, transport, login, root, stamp.
   - card, checkout, `commons_read`, `#<n>`, the card states `dormant` and `dnd`, go-between, exclusive resource, culture, change line, reply line, authority check, gossip, the envelope fields `from:`, `spread:`, `relay:`, and `has:`, the message form (tag line, reply line, a body of at most ten lines), and recurring wake.
5. Keep the Claude Code mapping (J9:105-123, DJ:107-127) as one tag in ontology; never put a Claude Code term in another skill's body.
6. Carry the provisional purpose and owner-stance lines of (b) item 1 in their own tags. Name each one an open item in the changes file; never present them as settled.

## (f) Reference graph

Edges, from RO:50-73. The skill named on the left names each skill on its right.

| skill | names |
|---|---|
| every skill but ontology | ontology |
| join | card, receive, heartbeat |
| card | tell |
| tell | receive |
| receive | adopt, vouch, tell, gossip, quote, consent |
| gossip | ask-around, spread-around, tell |
| ask-around | gossip, tell |
| spread-around | gossip, vouch, tell |
| quote | gossip |
| aid | tell |
| volunteer | ask-around, spread-around, adopt, tend, aid, heartbeat |
| heartbeat | volunteer |
| adopt | vouch, tell |
| tend | vouch, spread-around |
| vouch | — |
| steward | reserve, settle, scribe |
| reserve | tell |
| settle | tell, steward |
| leave | card, steward, scribe, sweep |
| sweep | card |
| scribe | propose, protocol-change |
| propose | protocol-change |
| consent | protocol-change |
| protocol-change | — |

1. Write each edge as "by the skill `<name>`" inside the sentence of the step where that skill takes over (SC:52; Ev:193); never gather edges into a list or a closing tag.
2. Name a skill by its bare name; never by `peers/skills/<name>/` or any path (SC:52).
3. Write only the edges in the table; never add an edge the table lacks. Record a missing edge you need as an open item.
4. Name `protocol-change` from `propose` and `consent`; never name `propose` and `consent` from one skill except `scribe`, and never name either from `protocol-change` (RO:33, RO:73).

## (g) Hooks and tests

Hooks (RO:48 — "SessionStart → join. PreToolUse send-stamp → tell. Heartbeat wake prompt → heartbeat. Nothing else."):
1. Rewrite `peers/hooks/templates/peer-join.txt` to name the skill `peers:join` alone; never name another skill there.
2. Rewrite `peers/hooks/templates/peer-compact.txt` to name the skill `peers:join` alone; never name another skill there.
3. Rewrite the `description` of `peers/hooks/hooks.json` to name `peers:join` for SessionStart and `peers:tell` for the send stamp; never change a matcher, command, or timeout.
4. Add `quote` to `TAG_PATTERN` at `peers/hooks/send-stamp.sh:4` (RO:37); never change another line of the script.
5. Write the heartbeat wake prompt as one fixed backticked line inside the skill `heartbeat`, naming `peers:heartbeat`. Members pass it to their recurring wake. Never ship it as a file outside the skill (SC:48).

Tests (`peers/tests/test_skills.py` unless named):
1. Replace `test_skill_set_is_join_gossip_amend_and_tend_commons` (lines 20-21) with a test pinning the 24 names of RO:5-30, sorted; never pin a count without the names.
2. Replace `test_join_states_protocol_10` (lines 53-54) with a test pinning the card's `protocol` instruction carrying `10` in `card/SKILL.md`; never pin a bare statement.
3. Retarget `test_claude_code_terms_live_only_in_the_one_mapping_tag` (lines 57-66) from `JOIN` to `ontology/SKILL.md`. Assert each term is absent from the body of every other skill. Never weaken the assertion.
4. Retarget `test_card_carries_member_fields_and_drops_ref_fields` (lines 69-78) so that each assertion reads the skill now holding its text. The fields go to card, `<root>/members/<member>.md` to its holder, `<root>/inbox/<member>.md` to its holder, and `<root>/resources.md` to reserve. Never drop an assertion.
5. Retarget `test_address_names_harness_host_and_ref`, `test_member_id_unique_within_one_society`, and `test_protocol_stewardship_is_named_protocol` (lines 86-102) to `ontology/SKILL.md`; never change what they assert.
6. Keep `test_join_description_names_the_society`, `test_plugin_descriptions_name_the_society`, both gossip envelope tests (lines 127-137), `test_no_text_names_a_retired_skill`, `test_every_plugin_skill_reference_resolves`, and `test_no_text_names_the_old_root` unchanged; never edit them.
7. Add `"quote"` to the tag list of `test_each_protocol_tag_is_stamped` at `peers/tests/test_send_stamp.py:119`; never remove a tag.
8. Leave `test_peer_join.py`, `test_peers_card.py`, and `test_peers_facts.py` as they are, since they use fixture templates and scripts; never edit them.
9. Rewrite the `## Skills` section of `peers/README.md` from the 24 frontmatters, in the existing format and alphabetical order. No generator ships in the repository. Never edit the README outside that section.
10. Name every test you changed, with its old and new names, in the changes file; never leave a test change unlisted.

## (h) Verification

1. Write `<rec>self-audit.md` with one table per skill. Each table has one row per rule of (d), with `PASS`, or `VIOLATION` with the line number and the quoted text. Never mark a rule `PASS` that you did not check against every line.
2. Fix every `VIOLATION` and re-run the table until each skill shows none; never report a skill with one standing.
3. Count emphatic words outside backticks with `grep -nwE 'never|always|only|must'` per skill. Record any line with two in the table; never trust a reading alone.
4. Run `just test` in `/Users/ryzhakar/pp/aoa-skills` and record the command, the pass count, and the exit code; never report a test result you did not run.
5. Write `<rec>protocol-10-skills-changes.md` listing:
   - the 24 skills with line counts;
   - what moved where, by source range;
   - every dropped range with its ground;
   - every hook and test change;
   - every open item.
   Never omit a moved range.

## (i) Stop conditions and open items

Stop and ask the scribe — the session that launched you — by SendMessage when any of these holds; never work past one:
1. An owner ruling contradicts another on a sentence you must write.
2. A sentence fits two procedures and neither (b) nor (f) settles which.
3. A skill cannot do its procedure without an edge the table in (f) lacks.
4. The worktree or branch in (a) cannot be created as written.
5. `just test` fails for a reason outside the skills, hooks, templates, README, and the tests named in (g).
6. Any step would write under `<root>`, to `main`, or to the pointer.

Leave each of these as an open item in the changes file, with its sources; never decide one:
1. Private and public space: may pull reach a peer's records or tree, and may a peer refuse? The owner calls it "open to discussion" (Ev:47, Ev:51; CH:297, CH:318).
2. The commons edit trail: git over `<root>` or an edit log, and who sets it up (Ev:102; CH:293, CH:313).
3. The sender-escalation misuse check: how a receiver tests an escalation and where it reports misuse (RO:45).
4. Every Open item (CH:290-308) and Question (CH:310-325) that no ruling at Ev:150-196 settles.
5. Every `→ prov.` placement of (b) item 1.

## (j) Report

1. End with three sentences: what changed, the test result with its exit code, and how many items stay open; never write a fourth.
2. List after them, as absolute paths, the worktree, the branch head commit, and the three records in `<rec>`; never list a path you did not write.

## Known gaps

The scribe must supply these. The instructions above cannot.

1. **No home for the purpose and owner-stance lines** (J9:11-55 except 19 and 31; DJ:21, 37, 39, 43). The roster has no skill for them. Ontology holds them provisionally, which risks the catch-all naming-lenses.md:216 warns of. The scribe must place them or rule them dropped.
2. **Where continuity goes** (J9:419-421). RO:32 says "a line in ontology or join naming memento:record-writing". Join is narrowed (Ev:149), so the line sits in ontology provisionally. The scribe confirms.
3. **How send-stamp names `tell`.** The hook emits no text a model reads; it only rewrites the message (`send-stamp.sh:7-23`). The instructions limit the change to the `hooks.json` description. Whether the hook should also emit text naming `peers:tell` is unsettled.
4. **Heartbeat wake prompt.** No template exists in the plugin. The instructions put it inside the skill `heartbeat` (SC:48). If the scribe wants a hook template, that is a non-skill sidecar, and Ev:196 says the outside-pointer rule targets exactly that.
5. **Ontology reference: once per skill or per sentence.** RO:74 leaves it to "the rewrite agents … per sentence". These instructions fix one reference at each skill's first step (RO:50). The scribe may want per-sentence references.
6. **The "encourage" wording for the wake** (Ev:49) is kept as "one means" (DJ:299). That is the draft's reading, not an owner ruling on the exact form.
7. **The version statement** moves into the card's `protocol` instruction (writing-stack tension 6). The scribe must bump that sentence at each ship, and the scribe skill's ship steps should name it.
8. **The feedback round** (Ev:197) closes at 16:45+0300 after these instructions were written. Its answers may change the roster, the graph, or the table. The scribe must fold them into RO before the rewrite starts.
