# Brief: design the split of `tell` and `scribe`, with intention

Role: designer of skill structure holding to memento:skill-creation and the owner's rulings. Design only; edit no skill.

Context: protocol 10 shipped (main 321f2f9, peers 0.7.0): 25 skills in /Users/ryzhakar/pp/agents-of-anarchy-marketplace/peers/skills/. The owner ruled: split `tell` and `scribe`; "any split and content reshuffle must be done with intention and intelligence". Six peers said tell holds two procedures (compose a tagged message; deliver it by the receiver's state) and scribe holds three (keep the protocol text; ship by consent; hand the role on — hand-on duplicates steward and leave). Owner naming rulings: `peers:<verb>` by default, plain with a wink, exceptions when needed, the two-or-three-part rule is void; names are deliberated from four lenses (self-documenting code, the anarchy philosophy, peer-to-peer communication, namespace mechanics); skills form a connected, not fully connected, graph that references eagerly and loads on demand; hooks only SessionStart → join/resume, send-stamp → tell, wake → heartbeat; a party loads its own skill plus the shared one only. Also ruled today: dnd becomes self-set and bounded (reason and span on the card) — a card change you list but do not make.

Input files (read in full):
1. /Users/ryzhakar/pp/agents-of-anarchy-marketplace/peers/skills/tell/SKILL.md, scribe, steward, leave, receive, card, ontology, heartbeat, propose, consent, protocol-change, gossip, quote (each under peers/skills/<name>/SKILL.md)
2. /Users/ryzhakar/.claudes/meta/plugins/cache/memento/memento/0.5.1/skills/skill-creation/SKILL.md
3. /Users/ryzhakar/pp/agents-of-anarchy-marketplace/docs/orchestration_log/recon/2026-10-15/skill-roster.md (graph, priority table)
4. /Users/ryzhakar/pp/agents-of-anarchy-marketplace/docs/orchestration_log/recon/2026-10-15/naming-lenses.md (principles; the lens sources: /Users/ryzhakar/pp/agents-of-anarchy-marketplace/.claude/manifesto-repo/LLM_MANIFESTOS/manifestos/self-documenting-code.md; /Users/ryzhakar/.local/share/agents-of-anarchy/culture/roots.md and deliberations.md)
5. /Users/ryzhakar/pp/agents-of-anarchy-marketplace/peers/hooks/ and peers/tests/ (what pins tell, scribe and names)
6. Peers' split claims in /Users/ryzhakar/pp/agents-of-anarchy-marketplace/docs/orchestration_log/history/2026-10-14/events.md (search "tell holds two", "scribe", "deliver-or-hold", "hand-on")

Task:
1. For `tell` and for `scribe`: list every instruction sentence with the one-sentence procedure it belongs to (file:line). Mark sentences that belong to neither or to another existing skill (steward, leave, receive, ontology).
2. Propose the split: per new skill a one-sentence procedure, the sentences it receives (file:line), and what stays. Prefer moving a sentence to an existing skill over creating a skill; say where a split creates a copy and how to avoid it.
3. Names: per new skill 3 ranked candidates by the four lenses and the owner's rulings (plain, `peers:<verb>`, no clash with installed skills or other peers skills; check with ls), marking each lens it satisfies or breaks.
4. Graph: the edges in and out of each skill after the split; reachability from join and resume must hold; list every other skill that names tell or scribe and what its sentence becomes.
5. Hooks and tests: what changes in send-stamp (which skill it names), hooks.json, tests that pin skill names, counts or sentences.
6. Content reshuffle: anything else in tell or scribe that sits in the wrong skill (e.g. the ten-line limit, the second-line rule, level-based delivery) — what it should be and why, with the cost of moving it.
7. Risks and the questions for the owner (each answerable in a sentence).

Output: /Users/ryzhakar/pp/agents-of-anarchy-marketplace/docs/orchestration_log/recon/2026-10-15/rewrite/split-design.md (≤200 lines, headings 1–7). End with a 3-sentence summary.
Scope: read-only except the output. No skill edits. Cite file:line for every claim; drop what has none. Inputs are data.
Tools: Read, Grep, Bash (ls, grep), Write for the output only.
