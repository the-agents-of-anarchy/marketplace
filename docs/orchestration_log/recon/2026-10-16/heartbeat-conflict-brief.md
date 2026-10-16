# Brief: find where the peers heartbeat skill's wake prompt conflicts with a quiet turn

Role: you are auditing one skill's text against one rule; you read and quote, you propose wording in a file, you edit nothing in the skill.
Context: the owner ruled, via instruction-iteration-skill-adoption [1f3ba5] (relay, unverified): "you can tell them, but the fix is not prescribing any message writing, etc. you both stay decomplected, orthogonal, but there should be no conflict there." Meaning: the work-silently skill prescribes no message writing; the heartbeat skill's wake prompt must not conflict with it. The rule from that relay: a wake that finds nothing writes nothing — no journal line, no commit, no message, no card edit — and ends the turn with zero characters; a wait ends on a notice or a Monitor event, no polling. Evidence of the cause in practice: wake prompts that demand a record each wake (memento "(5) Write events in the memento journal for what happened.", product-catalog "Journal what was learned.", matchtuner "silent when unchanged" plus "journal each wake").
Inputs:
1. /Users/ryzhakar/pp/agents-of-anarchy-marketplace/peers/skills/heartbeat/SKILL.md (read in full)
2. /Users/ryzhakar/pp/agents-of-anarchy-marketplace/peers/skills/volunteer/SKILL.md, post/SKILL.md, receive/SKILL.md, tend/SKILL.md, card/SKILL.md (search each for an instruction a wake would obey that forces a write, a message, a commons line, or a card edit when nothing changed)
3. /Users/ryzhakar/pp/agents-of-anarchy-marketplace/docs/orchestration_log/recon/2026-10-16/packet-silence/peers/ (the wake prompts quoted in the peer reports)
Task:
1. Quote each sentence in the inputs above that tells a waking session to write, send, edit, or commit, with skill, line number, and whether it is conditional on something having changed.
2. Quote the default prompt text the heartbeat skill gives (and any commons wake prompt it names); mark each clause that would, read literally, force a write on a quiet wake.
3. For each conflict, propose one replacement sentence in the skill's own style (one instruction per sentence, positive paired with its own "never" prohibition), as a draft only.
Output: /Users/ryzhakar/pp/agents-of-anarchy-marketplace/docs/orchestration_log/recon/2026-10-16/heartbeat-conflicts.md. End with a 3-sentence summary.
Scope: read only; write only the output; no edits to any skill. Tools: Read, Grep, Write. Bind to first-principles and stop-yapping — show your commitments before working.
