# Brief: ship protocol 10 (adopted by consent)

Role: release mechanic for /Users/ryzhakar/pp/agents-of-anarchy-marketplace (git, `just`, plugin `peers`).

Context: protocol 10 was adopted by consent: accepts from memento/steward, product-catalog-storage-api/service-owner, embedding_finetuning_for_ecommerce/maximalist-review, dotfiles/machine-setup (on 323571a), LLM_MANIFESTOS/manifesto-discovery and claude-skills/instruction-eval (on ee8fd61); no objection stands; claude-skills/instruction-eval keeps its loaded text for six lines until the owner rules. The branch `draft/10-skills` (worktree /Users/ryzhakar/pp/aoa-skills) carries it. Root pointer: /Users/ryzhakar/.local/share/agents-of-anarchy/PROTOCOL.md (version 9.3, append-only change lines).

Do NOT touch: docs/orchestration_log/ (the scribe's records), CLAUDE.md, .manifestos.yaml, any file under docs/orchestration_log/history/2026-10-15/ (a guest's span), any untracked or modified file you did not create. Add and commit by explicit path only; never `git add -A`. The working tree is shared with other sessions.

Steps (stop and report at the first failure; improvise nothing):
1. `git -C /Users/ryzhakar/pp/aoa-skills fetch -q; git -C /Users/ryzhakar/pp/aoa-skills rev-parse HEAD origin/draft/10-skills` — both must equal ee8fd6124aa0d51b1f5bbb674126e8559f8c3399; if either differs, stop and report both shas. Run `just test` in /Users/ryzhakar/pp/aoa-skills; record exit code and pass count (expect 197).
2. In /Users/ryzhakar/pp/agents-of-anarchy-marketplace on branch main: `git status --short` (record it); `git merge --no-ff draft/10-skills -m "feat(peers): peer protocol 10 — 25 skills, ontology"`. If the merge conflicts, stop and report the files; do not resolve. Run `just test` there; record exit code and count.
3. Check the version files: peers/.claude-plugin/plugin.json and the peers entry in .claude-plugin/marketplace.json must both read 0.7.0; report both. Fix nothing.
4. `git push origin main`; report the HEAD sha.
5. Remove the worktree: `git worktree remove /Users/ryzhakar/pp/aoa-skills` (keep the branch locally and on origin).
6. Pointer: read /Users/ryzhakar/.local/share/agents-of-anarchy/PROTOCOL.md; set its `version:` line to 10 (keep the file's shape); append exactly one change line with a single `printf '%s\n' '<line>' >> <file>` (never delete or reword older lines), with <merge sha> the sha from step 4:
`- 10 (2026-10-16): protocol rewritten as 25 one-procedure skills written to memento:skill-creation, shared terms in ontology (join, resume, card, tell, receive, gossip, ask-around, spread-around, quote, aid, volunteer, heartbeat, adopt, tend, vouch, steward, reserve, settle, leave, sweep, scribe, protocol-change, propose, consent); owner away at all times; any member not busy, dormant or dnd may be contacted; level 1 ([hazard], [quote]) reaches every member endangered or concerned whatever its state; adoption is thanked to the origin in one line; the commons is a communal garden; gossip carries from:, spread:, relay:, has: with has: and status as separate filters. Adopted by consent — accepts memento/steward, product-catalog-storage-api/service-owner, embedding_finetuning_for_ecommerce/maximalist-review, dotfiles/machine-setup, LLM_MANIFESTOS/manifesto-discovery, claude-skills/instruction-eval. Separated: claude-skills/instruction-eval keeps its loaded text for tell:63, ontology:207, ontology:209, ontology:139, card:87, volunteer:13 until the owner rules. peers 0.7.0, <merge sha>.`
Do NOT edit any member's card, including the scribe's.

Output: a report at /Users/ryzhakar/pp/agents-of-anarchy-marketplace/docs/orchestration_log/recon/2026-10-15/rewrite/ship-10-report.md: each step's command, exit code, counts, shas, the exact change line appended, the plugin version values. End your reply with a 3-sentence summary.
Tools: Bash (git, just), Read, Write (the report only). Scope: only these steps; no recommendations.
