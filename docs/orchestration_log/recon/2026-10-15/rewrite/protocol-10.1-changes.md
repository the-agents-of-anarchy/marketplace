# Protocol 10.1 changes: the tell and scribe splits, self-set bounded dnd

- **Branch:** `draft/10.1-split` in worktree `/Users/ryzhakar/pp/aoa-skills-101`, from `main` at 1858223. The head is in the report.
- **Untouched:** `main`, the pointer, every card, the commons, and everything under `docs/orchestration_log/` except this file and `traceability.md`.
- **Rules:** memento:skill-creation 0.5.1 with the same writing stack and the same guards as protocol 10 (`test_terms.py` terms and other-sense tests, the no-copy test, the plugin-reference test). The plan is `ten-one-instructions.md` with `split-design.md`; owner rulings at Ev:326–342 bind, and the owner's names are final: `tell`, `post`, `gather`, `ship`.
- **Tests:** `just test` gives 201 passed, exit 0 (199 after commit A, 201 after B and C).
- **Versions:** peers plugin 0.8.0 (`peers/.claude-plugin/plugin.json`, `.claude-plugin/marketplace.json`); protocol 10.1 in card's `Carry `protocol: 10.1`` and its test pin.
- **Skills:** 27. New: `post`, `gather`. Renamed: `scribe` → `ship`. Line counts: post 32, gather 32, ship 36 (scribe was 60), tell 68 (was 86).
- **Commits:** A `6aa8c78` tell split; B `d098d6c` scribe split and hand-on dissolution; C `65661e7` dnd. `just test` was run after each.

## Moves, sentence by sentence (item numbers are the plan's)

| item | sentence (10, main) | from → to | how |
|---|---|---|---|
| 1 | tell:63–79, the nine delivery sentences (level 1 at once; hold level 2 for busy, dormant, dnd; release; retry; the five inbox rules) | tell → post:13–31 | byte-identical, in two tags `<deliver-or-hold>` and `<append-to-an-inbox>`, except tell:69 drops "set by the skill `heartbeat`" (post → none) and tell:65 gains the dnd end time (item 8) |
| 1 | tell:27 | tell:27 | "…never hold it past that turn unless the skill `post` keeps it back." |
| 1 | new in tell | tell:61, tag `<hand-it-on>` | "Get each message to its receivers by the skill `post`; never deliver it by this skill alone." Placed before `<await-the-other-end>` so the body keeps the procedure's order (compose, hand on, await); the plan called it the closing sentence. |
| 1 | tell:4 description | tell:4 | "…and hand it on for delivery." |
| 2 | tell:37 | tell → vouch:19 | "Send the origin of a claim that failed your check a `[notice]` by the skill `tell`; never withhold it." vouch → tell; vouch is no longer a leaf. |
| 3 | heartbeat:45 | heartbeat:45 | "Retry held messages at each wake by the skill `post`; never let a wake pass with one unretried." |
| 3 | gossip:53 | dropped | gossip sends by tell (gossip:37) and tell by post; the hold rule lives once, in post. |
| 4 | scribe:15, 19–23, 39–45, 49 | scribe → ship | byte-identical. scribe:37's enacted outcome merges into the notice: ship:33 "Send `[notice] protocol v<N>`, carrying the change lines and the path to the change, to every live peer and every member the draft reached, by the skill `tell`; never let the pointer carry a change alone." ship's description says "as the scribe". |
| 5 | scribe:27, 29, 31, 33 | scribe → gather | byte-identical except gather:21 (scribe:29) gains "by the skill `tell`" so the edge gather → tell is a named reference. |
| 5 | scribe:37, narrowed | scribe → gather:27 | "Report a deferred or separated outcome to every member the draft reached, with the path to the change; never leave such an outcome unreported." |
| 5 | scribe:53's residue | gather:31 | "Name each pending request with its path in your leave notice when you leave keeping the stewardship `protocol`; never leave with one unnamed." |
| 6 | scribe:13 | dropped | steward:21 covers taking up an open stewardship. |
| 6 | scribe:53 | split | release = steward:17; leave notice = leave:21; pending requests → gather:31. |
| 6 | scribe:55 | scribe → protocol-change:43 | "Follow the last shipped version while the stewardship `protocol` is an open stewardship; never edit the protocol text meanwhile." |
| 6 | scribe:57 | dropped | propose:19 and propose:23 cover it. |
| 6 | scribe:59 | scribe → propose:27 | "Re-send each open request to a new scribe once its `[notice]` taking up the stewardship `protocol` arrives; never drop one." A new proposer duty; see below. |
| 7 | steward:41 | steward:41 | "Serve the stewardship `protocol` by the skills `gather` and `ship`; never serve it by this skill alone." |
| 7 | leave:15 | leave:15 | "Name your pending protocol requests by the skill `gather` when you keep the stewardship `protocol`; never leave with them unnamed." |
| 7 | new in receive | receive:53 | "Take a protocol request sent to you as the scribe by the skill `gather`; never take one in another way." |
| 8 | card:87 | card:87 | "Set `state: dnd` for yourself with a reason and an end time; never set it without both." |
| 8 | card:89 | card:89 | "Remove `state: dnd` at its end time or on your return, whichever comes first; never leave it past either." |
| 8 | card:71 | card:71 | "…a dnd line reading `state: dnd until <stamp>: <reason>`…" (no new field) |
| 8 | ontology:103 | ontology:103 | "Call a member dnd while its card carries `state: dnd until <stamp>: <reason>` and that stamp is still ahead; never call a member dnd past that stamp." |
| 8 | post:15 (from tell:65) | post:15 | holds "until that state clears, a dnd member's end time passes, or its reply time passes". ontology:207 is unchanged: level 1 still reaches dnd. `dormant` stays owner-set. |
| 9 | ontology | — | `delivery` stays the harness hand-off; the terms test demanded no sentence about `post`, so none was added, and no definition appears twice. |
| 10 | plugin, hooks | — | peers 0.8.0, protocol 10.1. hooks.json's description ("the send stamp the skill peers:tell relies on") stays true, so hooks are unchanged. |

Every 10 sentence lands in exactly one 10.1 skill or is dropped with a ground: `traceability.md` now opens with the 10 → 10.1 table (468 rows, 4 new sentences, 0 unmapped); the 9.3 → 10 table follows it unchanged.

## The new proposer duty (item 6, decided in the 10.1 round)

propose:27 puts on each proposer what scribe:59 put on the departing scribe: "Re-send each open request to a new scribe once its `[notice]` taking up the stewardship `protocol` arrives; never drop one." Protocol 10 made the old scribe re-send; 10.1 makes the proposer re-send, since the proposer holds the request as a file (propose:19, propose:23) and the scribe has left. The round that enacts 10.1 enacts this duty.

## Graph after the split (named references, `ontology` omitted)

- adopt → card, tell, vouch
- aid → tell
- ask-around → gossip, tell
- card → leave, tell
- consent → protocol-change, tell
- gather → propose, protocol-change, tell
- gossip → ask-around, spread-around, tell
- heartbeat → adopt, ask-around, card, post, receive, spread-around, tend, volunteer
- join → card, heartbeat, receive
- leave → card, gather, heartbeat, steward, sweep, tell
- post → —
- propose → protocol-change, tell
- protocol-change → —
- quote → gossip, vouch
- receive → adopt, consent, gather, gossip, quote, sweep, tell, vouch
- reserve → tell
- resume → join
- settle → steward, tell
- ship → card, tell
- spread-around → gossip, tell, vouch
- steward → gather, reserve, settle, ship
- sweep → card
- tell → post, receive, vouch
- tend → spread-around, vouch
- volunteer → adopt, aid, ask-around, heartbeat, spread-around, steward, tend
- vouch → tell

This matches item 12: tell → vouch, post, receive; post → none; gather → protocol-change, propose, tell; ship → card, tell; vouch → tell; steward → gather, ship; leave → gather; receive → gather; heartbeat → post. A party to a round loads its own skill plus protocol-change: gather, propose, and consent name none of each other.

Reachability over these edges:

| skill | from join | from resume | shortest path from join |
|---|---|---|---|
| adopt | yes | yes | join → heartbeat → adopt |
| aid | yes | yes | join → heartbeat → volunteer → aid |
| ask-around | yes | yes | join → heartbeat → ask-around |
| card | yes | yes | join → card |
| consent | yes | yes | join → receive → consent |
| gather | yes | yes | join → receive → gather |
| gossip | yes | yes | join → receive → gossip |
| heartbeat | yes | yes | join → heartbeat |
| join | yes | yes | join |
| leave | yes | yes | join → card → leave |
| ontology | yes | yes | every skill's terms sentence |
| post | yes | yes | join → heartbeat → post |
| propose | yes | yes | join → receive → gather → propose |
| protocol-change | yes | yes | join → receive → consent → protocol-change |
| quote | yes | yes | join → receive → quote |
| receive | yes | yes | join → receive |
| reserve | yes | yes | join → card → leave → steward → reserve |
| resume | no | yes | a SessionStart skill |
| settle | yes | yes | join → card → leave → steward → settle |
| ship | yes | yes | join → card → leave → steward → ship |
| spread-around | yes | yes | join → heartbeat → spread-around |
| steward | yes | yes | join → card → leave → steward |
| sweep | yes | yes | join → receive → sweep |
| tell | yes | yes | join → card → tell |
| tend | yes | yes | join → heartbeat → tend |
| volunteer | yes | yes | join → heartbeat → volunteer |
| vouch | yes | yes | join → receive → vouch |

Every skill is reachable from join, and every skill but join itself from resume, which reaches join.

## Tests and README (item 11)

| test or file | change |
|---|---|
| `test_skills.py` ROSTER | 25 → 27: `scribe` removed, `gather`, `post`, `ship` added, sorted. |
| `test_skill_set_is_the_protocol_10_roster` | renamed `test_skill_set_is_the_protocol_10_1_roster`. |
| `test_card_states_protocol_10` | renamed `test_card_states_protocol_10_1`, pins `Carry `protocol: 10.1``. |
| `test_terms.py` OTHER_SENSES `held` | the gossip pair ("Hold a relay of a level 2 gossip", "holds a level 2 message") dropped; "held message" added (post's description and heartbeat:45 say "held messages"); tell's tag and description phrases stay allowed and now sit in post. |
| `test_terms.py` `scanned_body` | strips "the skills `a` and `b`" (steward:41) as well as "the skill `a`". |
| terms sentences | regenerated for all 27 skills from their bodies by the terms test's patterns. |
| the no-copy test | green: no body sentence appears in two skills. |
| `test_every_plugin_skill_reference_resolves` | green over the skills, hooks, and README. |
| `peers/README.md` | the `## Skills` section regenerated from the 27 frontmatters: ship, post, and gather entries added, scribe removed, and the propose and tell entries (stale since protocol 10) refreshed. |
| hooks | unchanged: send-stamp names no skill; hooks.json's description still names peers:tell truly. |

## The instruction-eval separation (item 13)

| separated rule (10, main) | in 10.1 |
|---|---|
| tell:63 "Deliver a level 1 message at once, whatever …" | post:13, byte-identical ("Deliver a level 1 message at once, whatever the receiver's state; never hold one."). The separation now points at `post`. |
| ontology:207 (level 1) | ontology:207, unchanged text. |
| ontology:209 (level 2) | ontology:209, unchanged text. |
| ontology:139 "Call a member live while presence lists its …" | ontology:139, unchanged text. |
| card:87 "Set `state: dnd` when the owner orders you left …" | card:87, new text: "Set `state: dnd` for yourself with a reason and an end time; never set it without both." The owner's self-set bounded dnd replaces the owner-only rule; the separation's reference now points at this sentence. |
| volunteer:13 "Spend every stretch free of your own work …" | volunteer:13, unchanged text. |

## Owner-open items left unchanged

- Commons edit visibility (adopt:15 vs tend:43), open item 25 of protocol 10.
- Level 1 cost: kept, no cap (owner, Ev:326).
- Hook off switches: as shipped in protocol 10; the owner asked to hear more.
- The instruction-eval separation: its rules map as above; none was changed except card:87, which the owner's dnd ruling changed.

## Not in scope

Federation, society-qualified names, and flattened card file names: the owner says not now, on the roadmap (Ev:333).

## Residual violations by skill, by my read

- scribe → card from protocol 10 is now **ship → card** (ship:29 raises the card's `protocol` instruction): 1 edge beyond the roster graph, kept by gap ruling 7 and item 12.
- heartbeat's commons wake prompt names four skills, by the owner's ruling, not counted.
- Every other skill: 0. The literal pass over 469 body sentences finds one emphatic word per sentence and a same-concern prohibition on each; the mechanical rule check and the three guards are green.
- Two independent audit rounds are expected; nothing beyond the thirteen items was started.
