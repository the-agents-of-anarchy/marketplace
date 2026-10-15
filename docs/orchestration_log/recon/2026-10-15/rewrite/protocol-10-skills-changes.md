# Protocol 10 skills: the skill-creation rewrite

- **Branch:** `draft/10-skills` in worktree `/Users/ryzhakar/pp/aoa-skills`, branched from `draft/9.4-participation` at ec3d72f. The head is given in the report.
- **Untouched:** `main`, the pointer, every card, and the commons. The plugin stays at version 0.7.0.
- **Rules applied:** skill-creation 0.5.1, with the part-count clause void (Ev:149). The writing stack, the rewrite instructions, design-amendments (DM), gap-rulings (GR), and the owner's rulings at Ev:227-231 also bind; later documents win.
- **Tests:** `just test` gives 145 passed, exit 0.
- **Records written beside this file:** `traceability.md` (379 rows) and `self-audit.md` (25 tables).

## Skills and line counts

The table has 25 skills, 1184 lines in all. The draft had 670 lines in 4 skills.

| skill | lines | description words |
|---|---|---|
| adopt | 44 | 66 |
| aid | 20 | 43 |
| ask-around | 30 | 52 |
| card | 90 | 54 |
| consent | 24 | 35 |
| gossip | 62 | 54 |
| heartbeat | 44 | 70 |
| join | 70 | 64 |
| leave | 30 | 45 |
| ontology | 170 | 52 |
| propose | 30 | 54 |
| protocol-change | 46 | 67 |
| quote | 38 | 55 |
| receive | 58 | 57 |
| reserve | 32 | 49 |
| resume | 20 | 42 |
| scribe | 58 | 62 |
| settle | 30 | 46 |
| spread-around | 32 | 67 |
| steward | 42 | 69 |
| sweep | 24 | 44 |
| tell | 74 | 67 |
| tend | 54 | 74 |
| volunteer | 40 | 55 |
| vouch | 22 | 61 |

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
- **ontology**: J9:11, 31-33, 41-55, 63-93, 105-121, 299, 369, 513; DJ:39-43, 125, 307, 321, 405; DG:9, 85
- **propose**: J9:431-441
- **protocol-change**: J9:443, 449-459, 473-485
- **quote**: J9:37, 51, 411-415; DJ:37
- **receive**: J9:237-245, 263, 279, 355-357, 419-421; G9:39-49; DJ:235, 337; DG:91, 97-99
- **reserve**: J9:375-387
- **resume**: new. Its source is the owner's ruling "resume as thin wrapper around join" (Ev:227) and DM:37.
- **scribe**: J9:425-429, 461-471, 481, 489-501; DA:13, 53
- **settle**: J9:35-39, 401-407
- **spread-around**: J9:349-353, 359; G9:53-57; DG:37-41
- **steward**: J9:295, 363-373, 389-397, 515
- **sweep**: J9:509-511; DJ:415
- **tell**: J9:13-15, 23, 61, 233-239, 247-285, 347; G9:35; DJ:241-245, 257
- **tend**: J9:301-323, 329, 335; G9:33; DG:31; DT:13, 23, 29, 37-41
- **volunteer**: J9:47; DJ:291-299
- **vouch**: J9:19-21, 283; DJ:21

Some sentences hold a definition and an instruction together. Their definitions went to ontology as single `Call <x> …; never …` sentences, and their instructions stayed with the skill that does the act. Each one is marked `split` in the table.

New instructions, each from an accepted design amendment:

| skill | what was added | source |
|---|---|---|
| card | field `wake` | DM:8, F3 |
| card | read self-facts afresh at each edit | DM:11 |
| card | keep the wake while parked | DM:9 |
| join | search for the existing card first | DM:7 |
| tell | forward a ruling to running subagents | DM:14 |
| tell | escalation as a sender rule | RO:45 |
| receive | read side of the inbox | DM:17 |
| receive | the three memento record skills | DM:19, DM:20, GR:2 |
| receive | park a level 2 message while dormant or dnd, by `card` | DM:10 |
| quote | owner away; reach by what the sender knows; record before relaying | GR:1; Ev:227; DM:22 |
| aid | check by `vouch` | DM:23 |
| adopt | correct by `tend` | DM:24 |
| vouch | route a failed check to its origin | DM:27 |
| consent | check by `vouch` | DM:28 |
| propose and consent | send by `tell` | DM:16 |
| sweep | ping before moving | DM:36 |
| sweep | notice by `tell` | DM:16 |
| heartbeat | both wake forms with their prompts, the card field, practice by harness | DM:31-34; the owner's wake amendment |
| volunteer | the one act: find, pick in order, do by its skill | DM:35 |
| ontology | live, act, no-op acting, the level 2 bound, delivery waking an idle session, the `peers:` exceptions, hazards spread by gossip | DM:1-6 |

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
| `peers/hooks/templates/peer-compact.txt` | Names `peers:join` alone: "Context compacted: load the skill peers:join and rejoin the peer society at <root> as the member your card in <root>/members/ names." |
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

The edges in use are the table in (f) plus the additions from DM:9, 10, 16, 18, 23, 24, 27, 28, 32, the owner's wake amendment, and RO:77 (leave hub). Every skill but ontology names `ontology` once, at its first step (GR:5). These go past it:
- **scribe → card.** The ship step names card's `protocol` instruction (GR:7). No table lists it. It is open item 10.
- **resume → join and resume → heartbeat.** resume is new (Ev:227), and these follow the owner's "thin wrapper around join".
- **memento:record-writing, memento:event-capture, memento:record-promotion** are named from receive, quote, and adopt (DM:19-22, DM:25, GR:2).

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
