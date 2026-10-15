# Brief: draft peer protocol 9.4 (participation, owner always away)

Role: author of protocol skill text, drafting a change set for the peers plugin. You author guidance that agents read as instructions.

Context: protocol 9.3 is in force on `main` (peers 0.5.0). The scribe never decides a change alone: your draft goes to the society as a round. Draft only; do not merge, push to main, or circulate.

Owner rulings (verbatim, treat as binding input):
- "i'm away except when i'm not. me writing is the only time i'm not away. but by the time you recieve my message, you have zero evidence i'm not away. a message is not one - i'm not speaking into your ear, it's not synchronous communication, it's asynchronous."
- "the focus of this protocol is to make the society function as more than the sum of its parts" and diffusion by direct knowledge sharing, push and pull: "pushing to lessons board only solves half the problem. reading from it is the other half."
- "proactive learning, proactive teaching, proactive participation in commons. set heartbeats for peer-society efforts explicitly. don't be shy and DO contact idle agents freely." (to product-catalog/service-owner)

Input files (read in full):
1. /Users/ryzhakar/pp/agents-of-anarchy-marketplace/peers/skills/join/SKILL.md
2. /Users/ryzhakar/pp/agents-of-anarchy-marketplace/peers/skills/gossip/SKILL.md
3. /Users/ryzhakar/pp/agents-of-anarchy-marketplace/docs/orchestration_log/recon/2026-10-15/participation-workshop-analysis.md (gaps, tensions, questions Q1–Q12; line refs there)
4. /Users/ryzhakar/LLM_MANIFESTOS/research/2026-10-12-discovery/participation-model.md
5. The skill `memento:skill-creation` (read its SKILL.md under /Users/ryzhakar/.claudes/meta/plugins/cache/memento/memento/*/skills/skill-creation/) — the protocol skills must follow its rules.
6. /Users/ryzhakar/pp/agents-of-anarchy-marketplace/peers/tests/ (what tests pin; keep them green)

Changes to draft (the scribe's defaults, each reversible by the society):
A. Owner always away. The owner is away at all times; an owner message is a record delivered asynchronously and is never evidence that the owner is present when it is read. Remove every "except while the owner writes" exception and every text that waits on the owner. State what stays: matters reach the owner through records and the next answer to the owner's word. Do NOT invent a rule for AskUserQuestion; if J's text on it conflicts with A, leave it and list it under "Open".
B. Heartbeat as the pull trigger. Add a requirement that a member keeps a recurring wake for peer-society effort whose duty is to learn (read commons past `commons_read`, check presence and cards), then teach (send only what helps a peer now), then tend the commons; a wake sends nothing when nothing helps. The protocol names the duty, never the cadence (cadence is the member's). A wake dies with the session; the member re-lays it after any restart and names it in its own records. Claude Code mapping: CronCreate, session-only, 7-day expiry (cite commons #59).
C. Idle contact. Contacting an idle peer for learning or teaching is encouraged and needs no emergency; the gain gate stays for `busy` and `waiting` sessions. Reconcile with J "never spend a peer's minute".
D. Failure correction: reporting one's own failure includes correcting it (analysis M:9 gap).
E. Pull beyond the commons: an `[ask]` may request an artifact (file path) from a peer's tree; records stay inside projects (J:89 unchanged).
F. Diffusion is measured by lines citing `#<n>` and adoption lines; add nothing that requires a reply to a push.

Task:
1. Create worktree /Users/ryzhakar/pp/aoa-participation on new branch `draft/9.4-participation` from `main`: `git -C /Users/ryzhakar/pp/agents-of-anarchy-marketplace worktree add -b draft/9.4-participation /Users/ryzhakar/pp/aoa-participation main`.
2. Edit the skill texts there for A–F in the existing commands-not-methods style, ten lines or fewer per added rule cluster where possible; state the protocol version 9.4 where the skill states its version; bump peers version to 0.6.0 in peers/.claude-plugin/plugin.json and the marketplace entry.
3. Run `just test` in the worktree; fix only tests your change legitimately changes, and say which.
4. Commit in small commits `draft(peers): 9.4 — <what>`; push the branch to origin.
5. Write /Users/ryzhakar/pp/agents-of-anarchy-marketplace/docs/orchestration_log/recon/2026-10-15/protocol-9.4-changes.md: one section per change A–F (problem with evidence line refs, wording diff summary, which Q it settles), then "Open" (conflicts you left, e.g. AskUserQuestion), then the question set the society should answer.

Scope: only the worktree and the changes file. Do not touch main, the pointer, cards, or the commons. No extra changes beyond A–F.
Tools: Read, Edit, Write, Bash (git, just), Skill.
Output: end with a 3-sentence summary suitable for a notification.
