# Design amendments for the rewrite agent, 2026-10-15

Source: `feedback-matrix.md` (rows F1-F62, dispositions A/AC/OO/R) and `skill-roster.md` (RL-n = line n). Each instruction ends with its row id. Edges are references, not loads (RL-49). Cite roster lines by the corrected numbers in F62.

## ontology

1. Define "live" (a member that is not limit-stopped or parked) in the first-use sentence in ontology, so Level 1 spread can end (F53).
2. Define "act" in ontology as tool calls, never conversation text, so Level 1 "before its next step" and Level 2 "at its next tool round" stay distinct (F52).
3. State in ontology that "acts" at Level 1 includes recognising a no-op, so a receiver whose ruling is already on file may skip it while "acted on before the next step" is still met (F51).
4. Set the Level 2 wait bound in the ontology table to the reply time in tell's reply line (RL-10), and say a delivered message wakes an idle session, so the bound covers only dead or limit-stopped members (F55, F61).
5. List the `peers:` naming exceptions (protocol-change, ask-around, spread-around, ontology) once in ontology (F45).
6. Name gossip in the table's spread column, or in tell, so a [hazard] has a route to gossip's spread rule (F11).

## join

7. Make join's text look for the existing card first, so a resumed session after a login change neither duplicates nor orphans it, and leave the SessionStart hook line unchanged (F38).

## card

8. Add a card field holding the wake's cron ids, cadence and 7-day expiry, so a successor reads them there, and make heartbeat name card for it (F3).
9. Add a reference from card to heartbeat, with no load, and leave parking inside card (F4).
10. Add an edge from receive to card, and nothing from receive to heartbeat, for a message arriving while dormant or dnd (F14).
11. Add one line to card: read self-facts (model, host, harness, machine) afresh at each card edit (F42).

## tell

12. Add tell's sender-side inbox rules (reads field, append, stale fallback, one printf per message) (F43).
13. Keep "omit the stamp, never guess" in tell as the fallback when the send-stamp hook fails (F46).
14. Add one line to tell on relaying what a subagent reports, and on forwarding a ruling to running delegates; do not create a skill (F39).
15. Decide with skill-creation's one-sentence test whether tell splits compose from deliver, and do not rename tell (F27, D6).
16. Add an edge to tell from propose, consent and sweep, and keep leave → tell and leave → heartbeat (already adopted, RL-77), where each ends by sending a message or ending a wake (F1, F2, F10, F18).

## receive

17. Add receive's read-side inbox rules, with no split into a separate skill (F43).
18. Add edges from quote and receive to vouch, and keep Level 1 "acted on before the next step" unchanged (F7, C4).
19. Name memento's record skills (event-capture, record-promotion) in receive's text where memento runs, as a reference and not a hard dependency (F21).
20. Place the continuity line naming memento:record-writing in receive and adopt, not in ontology or join (F23).

## quote

21. Make quote name the ontology priority table instead of copying the level rule (F34).
22. Name the memento record skills in quote's text where memento runs, as a reference (F21).

## aid

23. Add an edge from aid to vouch, so findings passed on get a check (F8).

## adopt

24. Add an edge from adopt to tend, so an adopter who finds a commons line wrong can correct it (F16).
25. Name the memento record skills in adopt's text where memento runs, as a reference (F21).

## tend

26. Apply the one-sentence test inside tend to build, correct, merge and retire, add no new skills, and keep correction as an edit (F29, J55).

## vouch

27. Add an edge from vouch to tell, so a failed check routes back to the origin (F17).

## consent

27a. Add a by-name reference from consent to vouch, on demand, and keep consent's load at its own part plus protocol-change (F9, J186).

## steward and scribe

28. Name steward's one act in one sentence (F36).
29. Keep scribe its own skill; apply the one-sentence test and move hand-on to the steward and leave edges (F24, D6).

## heartbeat

30. Keep heartbeat to setting and restoring the wake, and put the tick checklist in the cron prompt, which wakes load no skill (F32, D5).
31. Add references from heartbeat to receive and adopt in the wake checklist, with no load, and keep the volunteer path (F5, F6, F60, D5).
32. Add a skip line to the wake checklist so a wake with nothing changed costs near nothing (F56, D5).
33. State heartbeat's practice (wake is session-only, expires after 7 days, own minute per wake, never delete another's wake, re-lay after restart) as the Claude Code case, with other harnesses named as differing (F44).

## volunteer

34. State volunteer's one act (check for work, pick one, do it), and do not fold it into heartbeat (F33).

## sweep

35. Add a ping step to sweep before acting on a member whose login changed and looks gone (F19).

## resume (added by D3)

36. Write `resume` for restart, clear, compaction and limit-stop: find the card, rejoin, restore stewardships and heartbeats; add backlog order and drain as steps only if the one-sentence test holds (F37, D3).

## All skills

37. Measure description words across the 24 skills first, then shorten trigger lists while keeping skill-creation's one sentence plus trigger phrases (F59).
38. Name only scripts (`peers-card`, `peers-facts`, send-stamp) that you have verified exist (F22).

## Hooks

39. Write the send-stamp hook so it writes the stamp and does not remind (F47).
40. Give the send-stamp hook a bypass for a relay made for a subagent (F48).
41. Give each hook (SessionStart join, heartbeat wake, send-stamp) an off switch and clearable state (F41).

## Tests

42. Check every roster line cited in the rewrite against the current roster text, using the corrected lines in F62 (F62).

## Held for the owner

- F12 (join → adopt): matrix names no D, notes "D4 does not cover it"; follow RL-8 "nothing else" and J149/J188, add no join → adopt edge.
- F25, F26 (parking in card, or in leave): D4 "parking stays in card"; keep parking in card and add none to leave (RL-77).
- F30 (adopt's read): "adopt, no learn" (J188), "accepted as recommended"; keep the read in adopt as RL-19 states, and narrow join (J149).
- F31 (priority table inside ontology): matrix names no D; follow J191 "table lives inside ontology", keep it there.
- F40 (spend-aware skill): matrix names no D; add no hold or pace skill and keep idle mapped to volunteer (J50-J57).
- F49 (Level 1 quote reach): D1 "quote reach = concerned sessions, society-wide when sender marks"; write it so in quote and the table, as a default the owner may overturn.
- F50 (Level 1 overrides dnd for [quote]): matrix names no D; follow J191 "Level 1 overrides dnd", change nothing.
- F54 (sender escalation): matrix names no D; follow J191 "sender may escalate", change nothing.
- F58 (thank-you cost): D2 "thanks stay single direct line"; keep thanks to one direct line to the origin (J50, J53).

## Not applied

- F13 (every skill lacks an ontology edge): R; RL-50 and RL-74 leave the per-sentence choice to the rewrite, and skill-creation line 72 governs.
- F15 (receive's relay edge): R; the edge exists and load is on demand (RL-54, J193).
- F20 (settle → quote): R; RL-54 already covers an owner ruling arriving.
- F28 (receive is a router): R; routing by reference is the design (J193), and J186 names receive a skill.
- F35 (aid holds three offers): R; the owner named one aid skill (J183), and the vouch need is F8.
- F57 (Level 3 board as a second read surface): R; the owner ruled the board (J181, J55).
- Rows dispositioned "not checkable": none; the unverifiable cites inside accepted rows (F22, F46) are handled in items 38 and 13.

## Summary

46 accepted rows (12 A, 34 AC), grouped by skill plus hook and test items, become 43 instructions, each tied to its matrix row. Nine OO rows (ten ids, F25 and F26 sharing one line) are held with their defaults: D1, D2 and D4 are quoted where the matrix names them, and the other rows follow the quoted owner ruling unchanged. Six R rows are listed under "Not applied", and the matrix has no rows with a "not checkable" disposition.
