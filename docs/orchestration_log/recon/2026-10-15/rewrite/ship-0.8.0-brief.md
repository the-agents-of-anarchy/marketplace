# Brief: ship peers 0.8.0 (adopted by consent)

Role: release mechanic for /Users/ryzhakar/pp/agents-of-anarchy-marketplace (git, `just`, plugin `peers`).

Context: the 0.8.0 draft (branch `draft/10.1-split`, worktree /Users/ryzhakar/pp/aoa-skills-101, head 383554a5171d9a2d31e9a39a095fff3ee50b17da) was adopted by consent: accepts from memento/steward, product-catalog-storage-api/service-owner, dotfiles/machine-setup, LLM_MANIFESTOS/manifesto-discovery, embedding_finetuning_for_ecommerce/maximalist-review, claude-skills/instruction-eval; no objection stands; claude-skills/instruction-eval keeps its loaded text for four lines until the owner rules. Root pointer: /Users/ryzhakar/.local/share/agents-of-anarchy/PROTOCOL.md (version 10 now, append-only change lines).

Do NOT touch: docs/orchestration_log/ (the scribe's records), CLAUDE.md, .manifestos.yaml, anything under docs/orchestration_log/history/2026-10-15/ (a guest's span), spec/, any file you did not create. Add and commit by explicit path only; never `git add -A`; the working tree is shared. Read a clock with `date` at the moment you write any date or stamp; never type one from memory.

Steps (stop and report at the first failure; improvise nothing):
1. `git -C /Users/ryzhakar/pp/aoa-skills-101 fetch -q; git -C /Users/ryzhakar/pp/aoa-skills-101 rev-parse HEAD origin/draft/10.1-split` — both must equal 383554a5171d9a2d31e9a39a095fff3ee50b17da; if either differs, stop and report both shas. Run `just test` there; record exit code and pass count (expect 202).
2. In /Users/ryzhakar/pp/agents-of-anarchy-marketplace on branch main: `git status --short` (record it); `git merge --no-ff draft/10.1-split -m "feat(peers): peers 0.8.0 — one version, post, gather, ship, self-set dnd"`. On a conflict stop and report the files; do not resolve. Run `just test` there; record exit code and count.
3. Check peers/.claude-plugin/plugin.json and the peers entry of .claude-plugin/marketplace.json both read 0.8.0; report both. Fix nothing.
4. `git push origin main`; report the HEAD sha.
5. `git worktree remove /Users/ryzhakar/pp/aoa-skills-101` (keep the branch locally and on origin).
6. Pointer: read /Users/ryzhakar/.local/share/agents-of-anarchy/PROTOCOL.md; set its `version:` line to `0.8.0` (keep the file's shape); then append exactly two lines, each by one `printf '%s\n' '<line>' >> <file>` (never delete or reword older lines), with D = the output of `date +%Y-%m-%d` read now and SHA = the merge sha from step 4:
Line 1: `- 0.8.0 (D): from this version the protocol's version is the version of the peers plugin; a card reading a pre-plugin number (9.x, 10) counts as below every plugin version. Skills: tell splits (tell composes, post delivers by level and receiver state), scribe splits (ship writes and announces the enacted text, gather turns requests into a draft, puts it to every live member, closes the round), hand-on dissolves into steward, leave, propose and protocol-change (a proposer re-sends open requests to a new scribe), vouch tells the peer a failed claim came from, dnd is self-set and bounded (state: dnd until <stamp>: <reason>). 27 skills. Adopted by consent — accepts memento/steward, product-catalog-storage-api/service-owner, dotfiles/machine-setup, LLM_MANIFESTOS/manifesto-discovery, embedding_finetuning_for_ecommerce/maximalist-review, claude-skills/instruction-eval. Separated: claude-skills/instruction-eval keeps its loaded text for post:13 (was tell:63), ontology:207, ontology:209, ontology:139 until the owner rules. peers 0.8.0, SHA.`
Line 2: `- mapping (D): protocol 9.3 was peers 0.5.0; protocol 10 was peers 0.7.0; from 0.8.0 the protocol version is the peers plugin's version.`
Do NOT edit any member's card, including the scribe's.

Output: a report at /Users/ryzhakar/pp/agents-of-anarchy-marketplace/docs/orchestration_log/recon/2026-10-15/rewrite/ship-0.8.0-report.md: each step's command, exit code, counts, shas, the two lines appended exactly, the version values. End your reply with a 3-sentence summary.
Tools: Bash (git, just, date), Read, Write (the report only). Scope: only these steps; no recommendations.
