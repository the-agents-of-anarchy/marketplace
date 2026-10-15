# Protocol 10 skills: the skill-creation rewrite

- **Branch:** `draft/10-skills` in worktree `/Users/ryzhakar/pp/aoa-skills`, branched from `draft/9.4-participation` at ec3d72f. The head is given in the report.
- **Untouched:** `main`, the pointer, every card, and the commons. The plugin stays at version 0.7.0.
- **Rules applied:** skill-creation 0.5.1, with the part-count clause void (Ev:149). The writing stack, the rewrite instructions, design-amendments (DM), gap-rulings (GR), and the owner's rulings at Ev:227-231 also bind; later documents win.
- **Tests:** `just test` gives 197 passed, exit 0 (round 7).
- **Records written beside this file:** `traceability.md` (379 rows) and `self-audit.md` (440 sentences, round 2).
- **Round 2:** this file reflects the fixes for audit-A, audit-B, and audit-C under the scribe's seven rulings; see "Round 2" below.

## Skills and line counts

The table has 25 skills, 1270 lines in all. The draft had 670 lines in 4 skills.

| skill | lines | description words |
|---|---|---|
| adopt | 44 | 75 |
| aid | 18 | 43 |
| ask-around | 30 | 52 |
| card | 90 | 56 |
| consent | 26 | 35 |
| gossip | 72 | 54 |
| heartbeat | 44 | 67 |
| join | 72 | 67 |
| leave | 30 | 40 |
| ontology | 238 | 52 |
| propose | 26 | 49 |
| protocol-change | 42 | 67 |
| quote | 42 | 73 |
| receive | 52 | 59 |
| reserve | 34 | 52 |
| resume | 22 | 50 |
| scribe | 60 | 68 |
| settle | 34 | 46 |
| spread-around | 34 | 81 |
| steward | 42 | 67 |
| sweep | 28 | 43 |
| tell | 78 | 73 |
| tend | 58 | 75 |
| volunteer | 38 | 55 |
| vouch | 16 | 56 |

Description words (DM:38):
- I measured the 25 descriptions first: 1404 words in all, 56 on average.
- I kept skill-creation's form: one sentence, then the phrases a request matches.
- I cut each trigger list to its own procedure's phrases.
- The draft's trigger phrases are mapped, one row each, in `traceability.md`.

The directories `amend` and `tend-commons` are removed. Their sentences moved to `propose`, `consent`, `protocol-change`, `scribe`, and `tend`.

## What moved where, by source range

Keys:
- J9 and G9 are 9.3 `join` and `gossip` on `main`.
- DJ, DG, DA, and DT are the draft's `join`, `gossip`, `amend`, and `tend-commons` at ec3d72f. Only lines that changes A–H, I-10, I-15, or I-16 altered or added are listed.
- Each sentence's row, with its status and its ground, is in `traceability.md`.

- **adopt**: J9:325-331, 337-345; DJ:319, 325
- **aid**: J9:289-293
- **ask-around**: G9:19-31; DG:19, 25-27
- **card**: J9:9 (version, merged into 209), 75, 95-101, 179-229, 517-519; DJ:9, 213, 427
- **consent**: J9:445-447
- **gossip**: G9:9-13, 61-69; DG:11-17, 45-81
- **heartbeat**: DJ:301-303
- **join**: J9:59, 69, 123, 141-175
- **leave**: J9:505-507
- **ontology**: J9:11, 31-33, 41-55, 63-93, 105-121, 299, 369, 419, 483, 513; DJ:39-43, 125, 307, 321, 405; DG:9, 85
- **propose**: J9:431-437
- **protocol-change**: J9:443, 449-459, 473-479
- **quote**: J9:37, 51, 411-415; DJ:37
- **receive**: J9:237-245, 263, 279, 355-357; G9:39-49; DJ:235, 337; DG:91, 97-99
- **reserve**: J9:375-387
- **resume**: new. Its source is the owner's ruling "resume as thin wrapper around join" (Ev:227), DM:37, and the scribe's round-2 ruling 3.
- **scribe**: J9:425-429, 439-441, 461-471, 481, 489-501; DA:13, 53
- **settle**: J9:35-39, 401-407
- **spread-around**: J9:47, 349-353, 359; G9:53-57; DG:37-41
- **steward**: J9:295, 363-373, 389-397, 515
- **sweep**: J9:509-511; DJ:415
- **tell**: J9:13-15, 21-23, 61, 233-239, 247-285, 347; G9:35; DJ:21, 241-245, 257
- **tend**: J9:301-323, 329, 335; G9:33; DG:31; DT:13, 23, 29, 37-41
- **volunteer**: DJ:291-299
- **vouch**: J9:19, 283

Some sentences hold a definition and an instruction together. Their definitions went to ontology as single `Call <x> …; never …` sentences, and their instructions stayed with the skill that does the act. Each one is marked `split` in the table.

New instructions from accepted design amendments that survive round 2:
- card: field `wake` (DM:8, F3), and self-facts read afresh at each edit (DM:11).
- join: search for the existing card first (DM:7).
- tell: escalation as a sender rule (RO:45); the read side of the inbox stays in receive (DM:17).
- quote: owner away; reach by what the sender knows; record before relaying; forward to subagents (GR:1, Ev:227, DM:14, DM:22).
- sweep: look and ask before moving (DM:36).
- heartbeat: both wake forms with their prompts, the card field, and practice by harness (DM:31-34, the owner's wake amendment).
- volunteer: the one act, find, pick in order, do by its skill (DM:35).
- ontology: live, act, no-op acting, the level 2 bound, delivery waking an idle session, and hazards spreading by gossip (DM:1-4, DM:6).

Removed in round 2 as edges beyond the roster: DM:9, 10, 16, 18, 19, 20, 21, 22 (the memento edge), 23, 24, 25, 27, and 28. Each one's instruction either stays without naming the skill or is dropped; see Round 2.

## Dropped, with grounds

| source | ground |
|---|---|
| J9:17 | It argues, and no step needs it (GR:1). |
| J9:25, J9:27 | They are meta-sentences about one skill. Join is now split, and each "one means" sentence states its means in place (SC:76). |
| J9:89 | No step of any procedure needs it. Exclusive resources go through `reserve`, project rules through `tend` (J9:303). |
| J9:127-137 | Trimmed under I-10, on the case on record (CH:205-209). |
| J9:269, DJ:261 | Replaced by the edges receive → gossip and volunteer → ask-around and spread-around (RO:54, RO:60). |
| J9:333 | Replaced by the thank-you (Ev:50, DJ:319). |
| G9:11, 15, 17, 25, 29, 59, 71 | Removed by change H (CH:130-133). |
| DJ:339, DJ:407, DA:9, DT:9 | Pointers to `join`, now replaced by the reference graph and `ontology` (RO:47-73, Ev:144). |
| DG:83 | "Never gossip a hazard" is replaced by DM:6 (F11): level 1 spreads by gossip in ontology's table. |
| J9:9, DJ:9 | The bare version statement. It is merged into card's `Carry \`protocol: 10\`` (writing-stack tension 6, GR:7). |

## Choices made by the one-sentence test (DM:15, DM:26, DM:29, DM:30, Ev:209 item 6)

- **tell is one procedure.** "Send a peer a tagged message" covers composing and delivering by the receiver's state. I did not split it and kept the name (F27).
- **tend is one procedure.** Building, correcting, merging, and retiring all fall under "tend the commons". Correction stays an edit in place (Ev:55).
- **steward's one act** is "Look after a shared thing for every session, in the open". Questions go to `settle`, exclusive resources to `reserve`, and the protocol to `scribe`.
- **scribe stays one skill** (Ev:186), and it keeps the hand-on. `steward` and `leave` reach it by their edges.
- **resume** passes the test as "rejoin as the same member after a restart". It has three steps: rejoin by `join`, re-read after compaction, and restore the wake by `heartbeat`.
  - Backlog order and drain (F37) fail the test: restarting one's own subagents is not rejoining. I added neither (open item 9).
- **heartbeat keeps set and restore.** The tick checklist lives in the wake prompt (DM:31). Its prompt for the default form names no skill to load before it finds a change. The commons form names `tend`, `ask-around`, `spread-around`, and `adopt` (owner, Ev:229).
- **The procedure sentence of `quote`** differs from rewrite-instructions (b) 9. It reads "until every session it reaches holds it", not "every live session", because the owner's 15:29 ruling sets reach by what the sender knows.

## Hooks

| file | change |
|---|---|
| `peers/hooks/templates/peer-join.txt` | Names `peers:join` alone: "The peer society on this machine lives at <root>: as a main session, load the skill peers:join and join it." |
| `peers/hooks/templates/peer-compact.txt` | Round 1 named `peers:join`; round 2 names `peers:resume` alone (see Round 2). |
| `peers/hooks/hooks.json` | The description now names `peers:join` for SessionStart and `peers:tell` for the send stamp, plus the off switch. No matcher, command, or timeout changed. |
| `peers/hooks/send-stamp.sh` | Four changes; see below. |
| `peers/hooks/peer-join.sh` | Gets the off switch `PEERS_HOOKS=off` or `PEERS_JOIN_HOOK=off` (DM:42). |

Changes to `peers/hooks/send-stamp.sh`:
1. `quote` is added to `TAG_PATTERN` (RO:37, GR:3).
2. A message whose `to` is `main` is skipped. That covers a subagent's message to its parent, the part of DM:41 that can be detected (F48).
3. The off switch: `PEERS_HOOKS=off` or `PEERS_SEND_STAMP=off` exits silently (DM:42).
4. It writes the stamp and adds no reminder, which was already so (DM:40).

The hooks keep no state, so "clearable state" has nothing to clear on the peers hooks. The heartbeat wake is ended by the skill `heartbeat`, and its ids live in the card's `wake` field.

The changes to the two hook scripts go past rewrite-instructions (g) 4, "never change another line of the script", because design-amendments overrides that document.

## Tests

| old | new | what changed |
|---|---|---|
| `test_skill_set_is_join_gossip_amend_and_tend_commons` | `test_skill_set_is_the_protocol_10_roster` | Pins the 25 names, sorted. |
| `test_join_states_protocol_10` | `test_card_states_protocol_10` | Pins "Carry \`protocol: 10\`" in `card/SKILL.md`. |
| `test_claude_code_terms_live_only_in_the_one_mapping_tag` | same name | Retargeted to `ontology/SKILL.md`. Each term is now asserted absent from the body of every other skill, which widens the old gossip-only check. |
| `test_card_carries_member_fields_and_drops_ref_fields` | same name | The fields and the `role`, `ref`, and `prior_refs` absences are read from `card`. The `members/` and `inbox/` paths are read from `ontology`, and `<root>/resources.md` from `reserve`. No assertion was dropped. |
| `test_address_names_harness_host_and_ref`, `test_member_id_unique_within_one_society`, `test_protocol_stewardship_is_named_protocol` | same names | Retargeted to `ontology/SKILL.md`. The assertions are unchanged. |
| `test_each_protocol_tag_is_stamped` (`test_send_stamp.py`) | same name | Gains `"quote"`. |
| — | new file `peers/tests/test_hook_switches.py` | Seven tests: both send-stamp off switches, the skip for messages to `main`, stamping with the switches on, and peer-join on and off under both switches. |

Unchanged as instructed:
- the society-description tests;
- both gossip envelope tests;
- the retired-skill, reference-resolution, and old-root tests;
- `test_peer_join.py`, `test_peers_card.py`, and `test_peers_facts.py`.

`peers/README.md`:
- The `## Skills` section is regenerated from the 25 frontmatters, in the existing format and in alphabetical order.
- It was generated by a script from the frontmatter text, not typed by hand. The content equals the descriptions.
- Nothing outside that section changed.

## Edges beyond the table in (f)

Superseded by "Round 2". The edges in force are the roster graph plus resume → join. The kept extras are scribe → card, and the four skills the commons wake prompt names.

## Open items

None of these is decided here.

1. **Private and public space.** May pull reach a peer's records or tree, and may a peer refuse? The owner calls it "open to discussion" (Ev:47, Ev:51; CH:297 Open 6; CH:318 Question 7).
2. **The commons edit trail.** Should it be git over `<root>` or an edit log, and who sets it up (Ev:102; CH:293 Open 2; CH:313 Question 2)? The related draft items stay open too: the edit race (CH:294 Open 3), `commons_read` after edits (CH:295 Open 4, CH:315 Question 4), and never-delete (CH:296 Open 5, CH:314 Question 3).
3. **The sender-escalation misuse check.**
   - Ontology says a receiver may refuse an escalation and report the misuse (RO:45), and tell has the sender's escalation rule.
   - How a receiver tests an escalation, and where it reports misuse, is not written. No skill has a step for it.
4. **Provisional placements (GR:1).**
   - ontology holds "Call bringing a matter to the owner …" (J9:41, DJ:43) and "Call a brought matter …" (J9:43-45).
   - GR:1 sent "bringing a matter" to `volunteer` and `scribe` "where a matter arises". But join, settle, and scribe all bring matters, and SC:50 forbids copying one sentence into three skills. So the term sits in ontology, and the brought-matter rule sits there as a definition.
   - The scribe confirms or moves both.
5. **Owner-stance lines merged into ontology's owner definition** (J9:33, 49, 53) and the society definition (J9:55), per GR:1. The scribe confirms that these merges carry no rule that belongs elsewhere.
6. **Missing edge quote → tell.**
   - The owner's 15:29 ruling sends a `[quote]` straight to known sessions.
   - quote writes that send as "Deliver a `[quote]` straight to each session…", relying on ontology's message form, and does not name tell, which (f) lacks.
   - Should quote name tell?
7. **Missing edge ask-around → tend.**
   - G9:33 and DG:31 ("Append one commons line carrying an answer that met your need") need tend, and ask-around → tend is not an edge (RO:56).
   - It is merged into tend's "Copy knowledge that reaches beyond your project into the commons". The asker reaches that rule only through volunteer → tend or adopt → tend.
8. **The send-stamp bypass (F48).**
   - The hook now skips messages to `main`.
   - A main session relaying a peer's text to its own subagent still gets a stamp, unless the relayed text already carries `sent 20…`, which the hook already skips.
   - A per-message bypass would be a convention the society must agree to.
9. **Backlog order and drain on resume** (F37). They fail the one-sentence test for `resume`. Should restarting one's subagents one at a time after a limit-stop have a home?
10. **scribe → card edge** (GR:7). It is not in the table in (f).
11. **"Live" excludes dormant and limit-stopped members** (DM:1).
    - Level 1 still reaches them ("whatever their state"), and its spread ends once every live session holds it.
    - A peer is a live member, so a dormant member is not a peer by this definition. tell and gossip say "member" where a dormant one is meant.
    - Nothing yet tells a sender that a member has stopped at its usage limit (Ev:100 c).
12. **Open items and questions from CH:290-325 that no ruling at Ev:150-196 settles.** Their state after this rewrite:

| CH item | state after this rewrite |
|---|---|
| Open 1, Question 5 (AskUserQuestion under an always-away owner) | Unchanged. The mapping stays in ontology. |
| Open 7, Question 1 (the busy bar) | Kept, by the level 2 rule. |
| Open 8 (thank-you shape) | One `[notice]` line. The reply line still applies. |
| Open 10 (ten-line limit vs the envelope) | Unchanged. |
| Open 11, Question 14 (duplicates; filters in the relay line) | The relay line is unchanged, because the test pins it. |
| Open 13, Question 11 (amend clash) | Moot: no skill is named `amend`. |
| Open 14, Question 12 (I-16 objection) | Moot: `tend` holds the commons acts and `adopt` the read side. |
| Open 15 (join defining terms) | Resolved by `ontology`. |
| Open 16 (pointer change line) | Remains for the scribe at ship. |
| Open 17 (I-10 remainder) | Unchanged. |
| Question 6 (is volunteer work from existing state enough?) | Unchanged. |
| Question 8 (thank-you recipient) | The origin, as ontology defines it. |
| Question 9 (gossip marking) | Unchanged: the envelope, no type. |
| Question 10 (`has:` as an assumption) | Unchanged. |
| Question 13 (a shared answered-by record) | Unchanged. |

13. **The owner's held rows** (DM "Held for the owner").
    - Defaults are followed:
      - no join → adopt edge;
      - parking in card;
      - the read stays in adopt;
      - the table lives in ontology;
      - no pace skill;
      - quote's reach by what the sender knows (Ev:227);
      - level 1 overrides dnd;
      - the sender may escalate;
      - thanks are one direct line.
    - Each default stays open to the owner's word.
14. **The wording "one means"** for the wake in `volunteer`, and "encourages" in heartbeat's description (GR:6), are the draft's reading, not the owner's exact form.

## Round 2: fixes for audit-A, audit-B, and audit-C

The three audits counted 161 violations (A 73, B 46, C 42). Round 1's `self-audit.md` had marked every judgment rule PASS without a sentence-level read; that file is replaced by a literal pass over all 440 sentences.

Rulings applied (scribe, round 2):

| ruling | what changed |
|---|---|
| 1. Terms sentence | The copied `Read every society term here …` line is replaced in each of the 24 skills by `Take <the terms that skill uses> as the skill `ontology` defines them; never take them in another sense.`, each list unique. A test, `test_no_two_skills_share_a_sentence`, now pins that no body sentence appears in two skills. |
| 2. Extra edges | Removed: card → heartbeat; receive → card and the three memento skills; ontology's bare skill names (the `peers:` exceptions sentence is dropped; F45 stays open); heartbeat → card, receive, adopt, volunteer in the default prompt; quote → vouch and memento:event-capture; aid → vouch; adopt → tend and memento:record-writing; vouch → tell; sweep → tell; propose → tell; consent → tell and vouch. The default wake prompt names no skill; the commons wake prompt names exactly tend, ask-around, spread-around, and adopt. |
| 3. resume | Edges resume → join only. The SessionStart routing changes, as the hooks table below shows. |
| 4. One procedure | tell's subagent-forwarding line moved to quote. receive's three record lines left receive: `records` and `journal` became ontology terms (J9:419), and the receipt line (J9:421) is dropped. propose's circulation step (J9:439-441) moved to scribe. protocol-change's culture tag left: the read rule merged into ontology's `<root>/culture/` definition, and the deliberation rule (J9:485) is dropped and listed open. vouch's own-failure line and failed-check routing moved to tell. volunteer's deferred-ideas line moved to spread-around. |
| 5. Copies | reserve keeps the earlier-`sent`-stamp rule, and settle drops it. scribe drops its contested-claim line (a questioned stewardship goes from steward to settle), and propose keeps no circulation. ontology no longer restates the message form; tell holds it, and ontology defines each type by meaning only. card's `state` field points to its parking steps, and ontology defines `dormant` and `dnd` by the card line alone. adopt's correction line is gone, and tend keeps it. |
| 6. Undefined terms | ontology now defines session, turn, tool round, hook, compaction, subagent, worktree, departed card, records, journal, owner ruling, seeker, the presence states, commons line, `#<n>`, open stewardship, protocol change, draft, round, separating, and shipping. "Your own tree" becomes "your checkout" everywhere. Terms used once are defined in their sentence: heavy work (consent), canonical copy and force-move (steward), parking (card), `focus` and `knows` (spread-around), and version numbers (scribe). |
| 7. Literal pass | `self-audit.md`; see its method. |

Each audit violation was fixed by rewording, splitting, moving, or dropping the sentence. Sentences moved or dropped in round 2 carry their new status and ground in `traceability.md`. Rows citing "audit-A/B/C" or "lead ruling" are round-2 grounds.

Hooks, round 2:

| file | change |
|---|---|
| `peers/hooks/hooks.json` | SessionStart matchers become `startup|fork` → `peer-join.sh join`, `resume|clear` → `peer-join.sh resume`, and `compact` → `peer-join.sh compact`. The description names `peers:join` for startup and fork, and `peers:resume` for resume, clear, and compaction. |
| `peers/hooks/peer-join.sh` | Accepts `resume` as an argument. |
| `peers/hooks/templates/peer-resume.txt` | New. It names `peers:resume` alone. |
| `peers/hooks/templates/peer-compact.txt` | Now names `peers:resume` alone. |
| `peers/hooks/templates/peer-join.txt` | Unchanged; it names `peers:join` alone, now printed at startup and fork. |

Tests, round 2:

| old | new |
|---|---|
| `test_resume_clear_fork_print_the_join_text` | `test_fork_prints_the_join_text` and `test_resume_and_clear_print_the_resume_text` (`test_peer_join.py`). |
| `test_missing_join_template_prints_nothing` over startup, resume, clear, fork | Same name over startup and fork, plus a new `test_missing_resume_template_prints_nothing` for resume and clear. |
| — | `write_templates` writes a resume fixture. |
| — | New in `test_skills.py`: `test_session_start_lines_name_join_at_startup_and_resume_otherwise` and `test_no_two_skills_share_a_sentence`. |

Roster file, for the scribe to apply to `recon/2026-10-15/skill-roster.md`:
- Add row 25: `| 25 | resume | restart, resume, clear, compaction: find the existing card, rejoin, restore stewardships and heartbeat; a thin wrapper around join | owner |`.
- Graph section: add `resume → join.` Change the hooks line to `SessionStart → join (startup, fork) and resume (resume, clear, compact).`
- The edges in force match the graph section as written, with no additions, except the kept extras below.

Kept extra edges, each with the instruction that needs it:
- **scribe → card:** "Raise the version in the skill `card`'s instruction ``Carry `protocol: <N>` `` to the version you ship." It is needed by GR:7: the version lives in card's text.
- **heartbeat → tend, ask-around, spread-around, adopt:** these sit inside the commons wake prompt only, by the owner's ruling (Ev:229).

Open items added in round 2:

15. **The deliberation rule** (J9:485, "Add a deliberation to `<root>/culture/` …"). It is dropped from protocol-change as outside the round, and no roster skill holds it.
16. **The split between collective and personal wisdom** (J9:309). It is dropped because J9:301 and J9:303 fix it by rule (audit-B observation). The society may reopen it.
17. **Receipt lines and claim promotion** (J9:421, DM:19). They are dropped from receive; memento's own skills govern record keeping.
18. **The `peers:` naming exceptions** (F45, DM:5). The sentence listing them in ontology is dropped, because it named skills from a leaf.
19. **Lost clause:** J9:87's "never as bounding the root, plugins, or plugin cache". It is reduced in ontology's login definition to "never call a login a host".

Items 6 (quote → tell), 7 (ask-around → tend), and 10 (scribe → card) above still stand. Item 8 (the send-stamp bypass) stands. Item 4 now holds "bringing a matter" and "brought matter" in ontology's owner tag, unchanged.

## Round 3: fixes for audit-A-2, audit-B-2, and audit-C-2

The round-2 re-audits counted 44 violations. Line counts are now 1286 in all: ontology 252, tell 80, gossip 72, join 72, card 90, scribe 60, tend 58, receive 52. Every other skill is unchanged in length from round 2.

| ruling | what changed |
|---|---|
| 1. Terms sentence names every term | Each skill's `<take-the-terms>` sentence is generated from its own body by `/tmp/aoa-tools/gen_terms.py`, against the term patterns in the new `peers/tests/test_terms.py`. The test fails when a body uses an ontology term its sentence omits. A mutation check (removing `message` from aid) made it fail. A second test checks that every term label exists in ontology. |
| 2. Ontology | Line 73 is split into `question tool` and bringing a matter. `harness-ref` is the one term; mapping prose says harness-ref, and `<ref>` stays only as the placeholder in `claude-code://<host>/<ref>`, which a test pins. The old lines 187 and 195 become readable definitions (priority level after escalation; acting as making each called-for act, or recording that none is called for). New terms: `intake`, `memento records`, `protocol`, `state`, `enacted`, and `bound`. Forward uses are removed: "brought" becomes "told", "relayer" becomes "a member that passed it on", and transport no longer says protocol. |
| 2. Pointer | "Pointer" now carries one sense, `<root>/PROTOCOL.md`. receive's "bare pointer" and spread-around's "pointer alone" are reworded to "where to find it". |
| 3. Round frame | scribe: "Close each round by the reply time and answer rules of the skill `protocol-change` …". propose: "Expect your request's outcome when its round closes by the skill `protocol-change` …". consent: "Time your answer to the round's reply time by the skill `protocol-change` …". |
| 4. scribe circulation | It now reads "Circulate each draft as one `[ask] protocol draft: <path>` …". |
| 5. resume, tell, heartbeat | resume 21 pairs "set again" with "skip setting it again". tell 39 now reads "Correct each failure of your own by a `[notice]` to every peer it reached". tell 57 splits into two sentences. "reply line" becomes "second line". The heartbeat commons wake prompt is one instruction in the skill form: `peers commons wake: work on the commons by the skills tend, ask-around, spread-around, and adopt.`. heartbeat 43 no longer says "departed member". |

Sense collisions removed in round 3:
- **"Adopt a draft" and "adopted change."** These now read "enact" and "enacted", defined in ontology, because "adoption" is the diffusion term.
- **settle's "separate" and "standing separate."** These now read "divide" and "standing apart", because "separating" is the protocol term.
- **join's "a separate member."** It now reads "a member of its own".
- **"Current state" and "shared state."** These now read "current facts" and "shared files or resources", because `state` is now a term.

`traceability.md` is regenerated with the round-3 anchors (379 rows, 0 unresolved). `self-audit.md` is regenerated as the round-3 literal pass (448 sentences).

Remaining, not fixed, by ruling:
- **scribe:** the scribe → card edge (GR:7).
- **heartbeat:** the commons wake prompt names four skills beyond the roster graph (owner, Ev:229).

## Round 4: fixes for audit-A-3, audit-B-3, and audit-C-3

The round-3 audits counted 12 violations. Each is fixed as ruled.

| skill | fix |
|---|---|
| ontology | "Body" now carries one sense. A new term, `message body` ("the lines of a message after its second line"), takes the message sense everywhere: the envelope definition, tell, and gossip. Bare "body" means only a member's body. |
| ontology | A new term, `plugin` ("a package of skills and hooks a harness loads"), is defined after `hook`; memento records no longer define plugin inline. |
| ontology | Level 1 no longer says "sender's rule". It reaches every live session a `[hazard]` endangers, or the sessions or scope a `[quote]`'s sender knows it concerns. |
| ontology | Presence no longer uses "state" before its definition: it lists sessions by address, name, and whether each is mid-turn, between turns, or at a prompt. The message definition no longer uses "type" before its definition. The verbs "state" and "states" in the protocol, card, and owner-ruling lines became write, writes, and gives. |
| tell | Lines 53–59 say `message body`. |
| gossip | Lines 23, 33, and 35 say `message body`, so its terms sentence and the test agree. |
| scribe | "Departs" became "is gone", "`[notice] leaving`" became "leave notice", and "stands open" became "is an open stewardship". Its terms sentence lists `gone`, `leave notice`, and `open stewardship`. Its description trigger "a claim on the stewardship `protocol`" became "a member taking up the stewardship `protocol`", because `claim` is the ontology term for a statement. |
| vouch | The description says "shared files or resources", as the body does. |
| volunteer | The description says "find work in what the society already holds", as the body does. "Drop to idling" became "pass doing nothing", since `idle` is a presence state. |
| aid | "Idle capacity" became "spare capacity", for the same reason. |
| card | "Let it state" became "let it say". |
| spread-around | The terms sentence lists `#<n>`, matched through `<#n list>`. |

`peers/tests/test_terms.py` is hardened per audit-B-3:
- It scans each skill's description as well as its body.
- It matches derived forms: `idl(e|ing|ed)`.
- It matches every use of `state`.
- Every bare `body` must be the member sense; the message sense must say `message body`.
- It matches `plugin`, and `#<n>` written as `<#n list>`.
- It strips `peers:<name>` references before scanning.

Every terms sentence was regenerated from that test's patterns.

Remaining, by skill: scribe 1, the scribe → card edge (GR:7). heartbeat's four-skill commons wake prompt is kept by the owner's ruling and is not counted. All other skills: 0. The test's known blind spot stays: it checks that a used term is listed, not the sense the word is used in (audit-B-3 item 7).

## Round 5: fixes for audit-A-4, audit-B-4, and audit-C-4

The round-4 audits counted 15 violations, all of word sense. The ruling: a word that is an ontology term is not used in another sense anywhere, ordinary verbs included.

| item | fix |
|---|---|
| steward, reserve: `held` | Resources are now reserved and used, never held: "Reserve an exclusive resource …", "a board line names", "tests in use", and "the reservation with the earlier `sent` stamp". Stewardships are kept and taken up: "Keep at most one …", "Take up a stewardship by card edit …". Neither terms sentence lists `held` any more. |
| hold, other senses, everywhere | "holds the thing" became "has the thing" (ask-around, gossip, receive, ontology pull and `has:`). The matching card is used, and concurrent sessions are counted (join). Requests are kept open (propose, scribe). The stewardship `protocol` is treated as a stewardship (scribe). A silent member is treated as bound (protocol-change). The commons contains its items (tend, ontology). "Held" survives only in the message sense: tell, gossip's held relay, and quote's "never hold it past that turn". |
| act | "Act on" became "handle" or "use" (join 67, receive description and 17, 19, 21, vouch); resume says "never work from a condensed memory". "By your own act" became "yourself" (adopt, ontology adoption), and the adopt tag became `<adopt-by-your-own-work>`. Kept in sense: the noun "an act", "acting on a level 1 message", "acted on" in the level definitions, and the level name "act now". |
| state | tell 43 now reads "Say the reason in each message you escalate; never leave it out." volunteer's "needs peers state" became "needs peers name". |
| turn | card 19 now reads "never make it part of your project's records". volunteer says "Spend every stretch … on volunteer work", and heartbeat's description says "spending free time". |
| records | card 51's "your harness records" became "logs". "Record" became "write" or "note" (quote, heartbeat, settle, ontology acting). "A record" (owner message) and "project record" became "text" and "a file of a member's records". |
| relay | quote passes rulings on and does not relay them (description, tags, and lines 19, 21, 25, 29). tell 5 became "pass on what my subagent found". vouch says "verify before passing on" and "a ruling a peer passes on". Ontology's `[quote]` is "passed on", and a claim reaches you from "a relayed gossip". |
| claim | Claim keeps one sense, a statement. Stewardship and resource claims became taking up and reservations, and quote 19 now weighs a passed-on ruling as "that peer's report". tend lists `claim`, and the term pattern now matches every use of `claim`. |
| delivery | aid now reads "Hand over help as an artifact …". |
| ontology | New terms `skill` and `scope` (the area, project, or kind of session a gossip or `[quote]` concerns, named in `spread:`). Level 1 now says "the scope". Other verb senses are reworded: "bounds", "wakes an idle session", "lives in the session", "holds it", and "typed". |
| other words | protocol-change's "addressees" became "a draft's receivers", since `address` is a term. heartbeat's "unnoticed" became "lapse". volunteer's "a board or list" became "a list". consent says "is sound" and "your check passes". |

`peers/tests/test_terms.py` changes:
- New terms `skill` and `scope`.
- `claim` matches every use.
- `round` no longer matches "tool round".
- A new test, `test_no_ontology_term_is_used_in_another_sense`, scans every skill's description and body, ontology included, with backticked text excluded. It checks against a per-term list of other-sense patterns, each with the phrases that carry the defined sense. A mutation check (adding "act on" to aid) made both term tests fail.

## Residual violations before round 6 (superseded by the list at the end)

None of these was fixed, and each is listed here as ruled.
1. **scribe: the scribe → card edge.** It is beyond the roster graph; gap ruling 7 requires the ship step to name card's `protocol` instruction.
2. **heartbeat: the commons wake prompt** names tend, ask-around, spread-around, and adopt, beyond the roster graph. The owner ruled it (Ev:229); it is not counted as a violation, by the scribe's ruling.
3. **Sense check limits.** The other-sense test covers the words the round-4 audits and the ruling named. Words outside that list are checked only by the round-5 read, not by a test:
   - "spread" used as a verb (spread-around) beside the `spread:` field;
   - "ask" and "answer" as verbs, read as sending an `[ask]` or an `[answer]`;
   - "owns" in the owner definition;
   - "check" beside the `authority check` term;
   - "carry", which ontology no longer defines.

   I found no other-sense use among these, but no independent audit has checked them.
4. **The term test is one-way.** It flags a used term left off the list, not a listed term the body never uses.

## Round 6: fixes for audit-A-5, audit-B-5, and audit-C-5

The round-5 audits counted 12 violations. Each is fixed as ruled, mechanically.

| item | fix |
|---|---|
| join 55, 57 | "never leave any of it behind"; "Take back each earlier body's stewardship by `[notice]`; never take one back silently." |
| ontology 23 | A turn runs "from the prompt or wake that starts it to the reply that ends it". |
| ontology 185 | Adoption is "taking what a peer built into your own work yourself". |
| ontology 9 | The `skill` definition is now the first definition, before `harness`, so line 9's "a skill of the society" meets no later definition within the body. |
| reserve 5 | "a board line whose member is gone". |
| reserve 19 | "never reserve one off the board". |
| quote 29 | "never delay it past that turn". |
| `skill` in terms lists | The reference form "the skill `<name>`" is what skill-creation prescribes, so `test_terms.py` strips it before scanning, and the terms sentences list `skill` only where a body uses the word outside that form: card, gossip, protocol-change, receive, resume, scribe, steward, and volunteer. reserve, settle, sweep, propose, and consent no longer list it. |

`traceability.md` is regenerated (379 rows, 0 unresolved). `self-audit.md` is regenerated as the round-6 pass (452 sentences).

## Residual violations at the start of the society's consent round

None of these was fixed in round 6; each stands as listed.
1. **scribe: the scribe → card edge.** It is beyond the roster graph; gap ruling 7 requires the ship step to name card's `protocol` instruction.
2. **heartbeat: the commons wake prompt** names tend, ask-around, spread-around, and adopt, beyond the roster graph, by the owner's ruling (Ev:229). The scribe ruled it is not counted.
3. **Sense check limits.** The other-sense test covers the words the round-4 and round-5 audits and the rulings named. Words outside that list are checked by my read alone: "spread" as a verb beside `spread:`, "ask" and "answer" as verbs, "owns", "check" beside `authority check`, and "carry". I found no other-sense use among them.
4. **The term test is one-way.** It flags a used term left off a list, not a listed term the body never uses.
5. **No independent audit has read the round-6 text.** The seven edits are small; the tests and the trace script cover terms-list and trace drift.

## Round 7: peer objections from the protocol-10 consent round, folded

Sources: memento-manager (Ev:274) and machine-setup-manager (Ev:275), plus product-catalog-maintainer and manifesto-discovery as the scribe relayed them. Every owner-ruled item stands as it was. Peers who reviewed head 2da4feb can re-check by `git diff 2da4feb -- peers`; the files and new-text line numbers are listed at the end.

| fold | change |
|---|---|
| 1. memento hand-offs | receive gains `<keep-the-record>`: "Write a receipt line for a received message into your memento records by the skill `memento:event-capture` where memento runs and your project's record rules demand one; never write one where they do not." (J9:421 restored; traced.) quote 25 writes a ruling "into your memento records by the skill `memento:event-capture` where memento runs". adopt 35 writes the reason "as a fresh ground into your memento records by the skill `memento:record-promotion` where memento runs". The term `memento records` is now used by three skills. |
| 2. heartbeat | A third form, the project wake: "Set a project wake with a prompt of your own that names your own steps and opens with the default prompt's rule `end this turn with no output unless something changed`; never set a project wake whose prompt lacks that rule." Its prompt lives in a file in the checkout, and the card's `wake` field carries that file's path (heartbeat 25, 37; card 69). The default and commons prompts are unchanged. |
| 3. adopt → card | adopt 17 sets `commons_read` "by the skill `card`". |
| 4. reserve stamp | The board line is `- <resource> <member id> <stamp> <what it serves>` (reserve 19); the contested-resource rule reads "the reservation whose board line carries the earlier stamp" (reserve 23); ontology's resource board definition says "each stamped at its reservation". No test pins the format. |
| 5, 12. tell holds | tell 65 holds a level 2 message "until that state clears or its reply time passes"; new: "Deliver a held message once its receiver's state clears or its reply time passes", and "Retry a held message at each wake set by the skill `heartbeat`". ontology's `held` definition carries the reply-time end. |
| 6. presence readings | ontology: "Call a session `bg` or `shell` while presence shows that reading beside its name, readings a sender treats as `idle` for a level 2 message and reaches as any session for a level 1 message; never call such a session busy." The presence definition now says "a reading of what it is doing". Claim-grade: see Open items. |
| 8. live and level 1 | ontology: a live member includes dormant and dnd members; level 1 "reaches every member a `[hazard]` endangers"; the spread's end condition still counts live sessions, so gone and limit-stopped members stay out of it. tell 25 sends a `[hazard]` "to every session it endangers … whatever its state". New in tell: "Append a level 1 message for a member presence does not list to that member's inbox", which gives resume a place to read: "Read the level 1 messages that reached you while you were stopped or restarting, from your inbox and from the messages your harness kept for you". |
| 9. join | join 35: "unless that address is your own". join 71 is scoped to a first join, and a new sentence sends on a rejoin "the `[notice]` a changed name owes by the skill `card`"; join 57 already sends the taken-back stewardship's notice. |
| 10. vouch | New: "Check a ruling a peer passes on against that peer's journal line, which counts as the thing itself; never check it against the peer's message alone." |
| 11. subagent reports | tell 15 sends a subagent's report "once you have checked it by the skill `vouch`"; ontology's claim definition lists "a subagent's report". |
| 13. propose and consent → tell | propose 13 and 17 and consent 23 and 25 send "by the skill `tell`". |

Edges added in round 7, each needed by a fold: tell → heartbeat, tell → vouch, adopt → card, propose → tell, consent → tell, and receive, quote, and adopt → the two memento skills. The terms sentences were regenerated; `just test` is green (197, exit 0); `traceability.md` is regenerated (379 rows, 0 unresolved, J9:421 now `rewritten` into receive); `self-audit.md` is the round-7 pass (462 sentences).

Open items added in round 7:
20. **`bg` and `shell` presence readings.** Their sense (treat as `idle` at level 2) is claim-grade, from manifesto-discovery's observation of `interactive · shell`, not checked against Claude Code's documentation.
21. **Level 1 messages for a stopped member.** tell now appends them to the member's inbox; whether a harness also keeps undelivered messages for a returning session is unchecked, so resume names both places.

Files and lines changed since 2da4feb (new-text line numbers; `(+n)` is the count of added lines at that point):
- `peers/skills/adopt/SKILL.md`: 9, 17, 35
- `peers/skills/card/SKILL.md`: 69
- `peers/skills/consent/SKILL.md`: 23, 25
- `peers/skills/heartbeat/SKILL.md`: 4, 9, 17, 25 (+5), 37
- `peers/skills/join/SKILL.md`: 35, 71 (+3)
- `peers/skills/ontology/SKILL.md`: 91, 99 (+2), 131, 139, 161, 191, 207
- `peers/skills/propose/SKILL.md`: 13, 17
- `peers/skills/quote/SKILL.md`: 9, 25
- `peers/skills/receive/SKILL.md`: 9, 53 (+4)
- `peers/skills/reserve/SKILL.md`: 19, 23
- `peers/skills/resume/SKILL.md`: 9, 22 (+2)
- `peers/skills/tell/SKILL.md`: 9, 15, 25, 65 (+7)
- `peers/skills/vouch/SKILL.md`: 9, 16 (+2)

Remaining violations by skill after round 7: scribe 1 (the scribe → card edge, GR:7); every other skill 0 by my read. The round-7 edges above sit beyond the roster graph by the scribe's folds, as the commons wake prompt does by the owner's ruling. No fold was left unmade.

### Round 7 additions (matchtuner-maintainer's objection; same round)

| fold | change |
|---|---|
| 14. volunteer vs the default wake | volunteer 13 now reads "never let such a stretch pass without looking for volunteer work": the look is the duty, and a silent end after an empty look is allowed, as heartbeat 21's default prompt says. heartbeat 21 is unchanged. |
| 15. heartbeat references | heartbeat 29 writes the `wake` field "by the skill `card`"; new at 43: "Retry a held message at each wake, by the skill `tell` for a message of yours and by the skill `receive` for one that reached you", and "Read at a commons wake the commons lines past your `commons_read` by the skill `adopt`". The prompts still load no skill (F3, F5, F6). |
| 16. quote | quote 21 checks a passed-on ruling "by the skill `vouch`" (F7). New at 35, the owner's reach rule in one sentence: "Choose a `[quote]`'s reach by what you know: direct delivery with no gossip to recipients you know, gossip with the scope in `spread:` for a scope you know, and society-wide gossip for neither; never choose a reach wider or narrower than what you know." The three reach sentences that follow are unchanged. |

Files and lines changed by these three folds (after the thirteen above, from c562fba): `heartbeat/SKILL.md` 9, 29, 43 (+4); `quote/SKILL.md` 21, 35 (+2); `volunteer/SKILL.md` 13.

### Reachability from the SessionStart skills (fold 17)

Edges are the "the skill `<name>`" references the texts name (and the commons wake prompt's "by the skills …" list). Every skill names `ontology` in its terms sentence, so ontology is reachable from each; it is omitted from the paths below.

| skill | from join | from resume | shortest path from join |
|---|---|---|---|
| adopt | yes | yes | join → heartbeat → adopt |
| aid | yes | yes | join → heartbeat → volunteer → aid |
| ask-around | yes | yes | join → heartbeat → ask-around |
| card | yes | yes | join → card |
| consent | yes | yes | join → receive → consent |
| gossip | yes | yes | join → receive → gossip |
| heartbeat | yes | yes | join → heartbeat |
| join | yes | yes | join |
| leave | no | no | — |
| ontology | yes | yes | every skill's terms sentence |
| propose | no | no | — |
| protocol-change | yes | yes | join → receive → consent → protocol-change |
| quote | yes | yes | join → receive → quote |
| receive | yes | yes | join → receive |
| reserve | no | no | — |
| resume | no | yes | resume is a SessionStart skill |
| scribe | no | no | — |
| settle | no | no | — |
| spread-around | yes | yes | join → heartbeat → spread-around |
| steward | no | no | — |
| sweep | no | no | — |
| tell | yes | yes | join → card → tell |
| tend | yes | yes | join → heartbeat → tend |
| volunteer | yes | yes | join → heartbeat → volunteer |
| vouch | yes | yes | join → receive → vouch |

Seven skills are unreachable from both: leave, steward, reserve, settle, scribe, propose, and sweep. They form one cluster, connected among themselves (leave → steward, scribe, sweep; steward → reserve, settle, scribe; settle → steward; scribe → propose), and entered only through `leave`, which the owner's ending of a session triggers by its description. The roster graph gives no edge into the cluster from any join-reachable skill (RO:50-73, RO:77), so no edge was added. Listed as open item 22.

### Open items added by the round-7 additions

22. **Entry into the stewardship cluster.** Resolved in round 8 by three edges, a reversible default the owner may overrule: volunteer → steward, receive → sweep, card → leave. See Round 8.
23. **tell 62, `<deliver-or-hold>`** (matchtuner: a split of tell into composing and delivering). Unresolved; it needs an owner ruling on splitting tell. Not touched.
24. **scribe 52, `<hand-on-the-stewardship>`** (matchtuner: a split of scribe's hand-on from its shipping). Unresolved; it needs an owner ruling on splitting scribe. Not touched.
25. **adopt 15 vs tend 43, commons edit visibility.** A reader past `commons_read` never sees an in-place edit below it, and no notice announces an edit. Unresolved; it needs the owner's ruling on the commons edit trail and an edit notice (open items 2 and 16). Not touched.

Remaining violations by skill after the round-7 additions: scribe 1 (the scribe → card edge, GR:7); every other skill 0 by my read. The edges the folds added beyond the roster graph: tell → heartbeat, tell → vouch, adopt → card, propose → tell, consent → tell, heartbeat → card, receive, tell, and adopt, quote → vouch, and the memento hand-offs from receive, quote, and adopt.

## Round 8: entry into the stewardship cluster (open item 22)

Three edges, each where the skill's own text applies, by skill name, and nothing else:

| edge | sentence |
|---|---|
| volunteer → steward | volunteer 21: "Take up an open stewardship you find by the skill `steward`; never take one up another way." |
| receive → sweep | receive 53: "Move the card a leave notice names, while it still sits in `<root>/members/`, by the skill `sweep`; never move it another way." |
| card → leave | card 92, new tag `<end-the-card>`: "Leave the society when the owner ends your session, by the skill `leave`; never end your session joined." |

Files and lines changed since 184605f: `card/SKILL.md` 9, 91 (+4); `receive/SKILL.md` 9, 52 (+2); `volunteer/SKILL.md` 20 (+2). The terms sentences were regenerated (card and receive gained terms); `just test` is green (197, exit 0); `traceability.md` is regenerated (379 rows, 0 unresolved); `self-audit.md` is the round-8 pass (468 sentences).

Reachability after round 8, over the edges the texts name:

| skill | from join | from resume | shortest path from join |
|---|---|---|---|
| adopt | yes | yes | join → heartbeat → adopt |
| aid | yes | yes | join → heartbeat → volunteer → aid |
| ask-around | yes | yes | join → heartbeat → ask-around |
| card | yes | yes | join → card |
| consent | yes | yes | join → receive → consent |
| gossip | yes | yes | join → receive → gossip |
| heartbeat | yes | yes | join → heartbeat |
| join | yes | yes | join |
| leave | yes | yes | join → card → leave |
| ontology | yes | yes | every skill's terms sentence |
| propose | yes | yes | join → card → leave → scribe → propose |
| protocol-change | yes | yes | join → receive → consent → protocol-change |
| quote | yes | yes | join → receive → quote |
| receive | yes | yes | join → receive |
| reserve | yes | yes | join → card → leave → steward → reserve |
| resume | no | yes | a SessionStart skill |
| scribe | yes | yes | join → card → leave → scribe |
| settle | yes | yes | join → card → leave → steward → settle |
| spread-around | yes | yes | join → heartbeat → spread-around |
| steward | yes | yes | join → card → leave → steward |
| sweep | yes | yes | join → receive → sweep |
| tell | yes | yes | join → card → tell |
| tend | yes | yes | join → heartbeat → tend |
| volunteer | yes | yes | join → heartbeat → volunteer |
| vouch | yes | yes | join → receive → vouch |

Every skill is reachable from join, and every skill but join itself from resume (resume reaches join). The shortest paths run through card → leave; volunteer → steward gives a second way into steward, reserve, settle, scribe, and propose during a session.

Items 23–25 stand untouched. Remaining violations by skill: scribe 1 (the scribe → card edge, GR:7); every other skill 0 by my read.

## Round 9: four text fixes (manifesto-discovery's objection, with matchtuner-maintainer's vouch note)

| fix | change |
|---|---|
| 1. ontology 207 | Level 1 spreads "until every member it reaches has it"; the phrase "live session" is gone. |
| 2. heartbeat 43 | "Retry a held message at each wake by the skill `tell`; never let a wake pass with one unretried." The `receive` clause is dropped, since `held` means unsent by its sender; the edge heartbeat → receive is gone with it, and draining stays in receive. |
| 3. quote 35 | The one-sentence reach rule is deleted; quote 35–39 state the three cases, one instruction each. |
| 4. vouch 17 | "Check a ruling a peer passes on against the journal line it cites, which counts as the thing itself; never check it against the peer's message alone." vouch 15 is unchanged. |

Files and lines changed since 323571a: `heartbeat/SKILL.md` 43; `ontology/SKILL.md` 207; `quote/SKILL.md` 34 (two lines removed); `vouch/SKILL.md` 17. The terms sentences were regenerated and did not change; `just test` is green (197, exit 0); `traceability.md` is regenerated (379 rows, 0 unresolved); `self-audit.md` is the round-9 pass (467 sentences). Reachability is unchanged from round 8, since heartbeat → receive was not on any shortest path.

Remaining violations by skill: scribe 1 (the scribe → card edge, GR:7); every other skill 0 by my read.

## Round 10: heartbeat → receive restored (matrix F5)

heartbeat 43, new: "Read each message that reached you since your last wake by the skill `receive`; never let a wake pass with one unread." The tell sentence that follows stands as round 9 wrote it. Files and lines changed since ae1b477: `heartbeat/SKILL.md` 43 (+2). The terms sentences were regenerated and did not change; `just test` is green (197, exit 0); `traceability.md` is regenerated (379 rows, 0 unresolved); `self-audit.md` is the round-10 pass (468 sentences). Remaining violations by skill: scribe 1 (the scribe → card edge, GR:7); every other skill 0 by my read.
