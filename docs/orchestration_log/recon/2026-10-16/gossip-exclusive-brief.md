# Brief: gossip-exclusive draft for ask-around and spread-around

1. Role: you author protocol skill text for the peer society's peers plugin (opus: guidance another agent reads as instructions).
2. Context: owner word, verbatim, 2026-10-16 evening: "enforce ask-around and the other one to USE GOSSIP MECHANIC EXCLUSIVELY". "The other one" is read as spread-around (the gossip-notice originator, named in ask-around and gossip skill text); confirm by reading, and say in the report if another skill fits better. Today ask-around says "Send a direct [ask] by the skill `tell` to the peer you know has the thing; never gossip a need you can target", and spread-around sends findings direct to named peers first. The owner wants gossip as the only originating mechanic in these two skills. The protocol changes only by the society's consent: you draft, you do not circulate and do not ship.
3. Input files:
   1. /Users/ryzhakar/.claudes/meta/plugins/cache/agents-of-anarchy/peers/0.8.0/skills/ask-around/SKILL.md
   2. /Users/ryzhakar/.claudes/meta/plugins/cache/agents-of-anarchy/peers/0.8.0/skills/spread-around/SKILL.md
   3. same dir: gossip, tell, receive, join, post, ontology, volunteer, adopt (SKILL.md each)
   4. /Users/ryzhakar/pp/agents-of-anarchy-marketplace/docs/orchestration_log/recon/2026-10-16/ambiguity-feedback.md (defect 1, gossip seeding wording)
   5. the plugin source in the repo /Users/ryzhakar/pp/agents-of-anarchy-marketplace (find peers/skills/ask-around and spread-around)
4. Task:
   1. Read the files. Find every sentence in ask-around, spread-around, and any other skill that routes a need or a finding by direct send where the owner's word says gossip.
   2. Write replacement wording for ask-around and spread-around: originate only by gossip, envelope per the gossip skill, seed two or three peers, `has:` lists only holders; keep the skills' own style (one imperative plus its "never", short, no filler).
   3. List each conflict the change makes with other skills (tell, gossip, receive, volunteer, adopt, join, post), quoting both sentences, and a proposed fix for each. Do not edit those other skills.
   4. In a git worktree of the repo on a new branch `draft/gossip-exclusive` (base: origin/main), apply the two skill edits only, commit once. Do not touch main, integration/proudhon, or the plugin cache. Do not push.
5. Output path: /Users/ryzhakar/pp/agents-of-anarchy-marketplace/docs/orchestration_log/recon/2026-10-16/gossip-exclusive-draft.md
6. Report format: sections "Owner word", "Old to new wording" (per skill, quoted), "Conflicts" (table: skill:line, sentence, fix), "Branch" (name, commit SHA, worktree path), "Open questions". Then a 3-sentence summary.
7. Scope: no circulation, no sends, no shipping, no version bump, no pointer edit, no edits outside the two skills in the worktree. Do not decide for the society; flag where consent is needed.
8. Tools: Read, Grep, Glob, Bash (git worktree, git commit), Write.
9. Prime directive: shortest wording that makes gossip the only origin path in these two skills; keep what the owner did not name.
