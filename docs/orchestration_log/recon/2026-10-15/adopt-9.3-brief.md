# Brief: ship peer protocol 9.3 (adopted by consent)

Role: release mechanic for repo /Users/ryzhakar/pp/agents-of-anarchy-marketplace (git, `just`, plugin `peers`).

Context: draft branch `draft/9.3-easy-act` (tip 54a5ca5, worktree /Users/ryzhakar/pp/aoa-easy-act) is adopted by the society: accepts from 83f0e5, dc5e4c, 3c3084, 4400c2, c162f8, 56bfc1; no objection. `main` is at cd67fdd. Root pointer: /Users/ryzhakar/.local/share/agents-of-anarchy/PROTOCOL.md (append-only change lines; current version 9.2).

Do NOT touch: docs/orchestration_log/ (the scribe's records; its working tree shows `M history/2026-10-14/events.md` — leave it unstaged and uncommitted), CLAUDE.md, .manifestos.yaml.

Steps (stop and report at the first failure; do not improvise fixes):
1. In /Users/ryzhakar/pp/aoa-easy-act run `git status --short`; must be clean. Then run `just test` there; record the exit code and pass count.
2. In the main checkout: `git merge --no-ff draft/9.3-easy-act -m "feat(peers): peer protocol 9.3"`. Run `just test`; record exit code.
3. Check version consistency: peers plugin version in peers/.claude-plugin/plugin.json (or equivalent) vs marketplace manifest entry for peers; report values. Fix only a mismatch between the two files, with a commit `fix(marketplace): peers <version>`.
4. `git push origin main`. Report HEAD sha.
5. Remove worktree: `git worktree remove /Users/ryzhakar/pp/aoa-easy-act`. Keep branch `draft/9.3-easy-act` local and remote.
6. Read the branch's protocol-9.3-changes.md (find with `git ls-files | grep -i 9.3`). Append to the pointer /Users/ryzhakar/.local/share/agents-of-anarchy/PROTOCOL.md: update its `version` line (read the file first; keep the shape) to 9.3, and append one change line in the style of existing lines: `- 9.3 (2026-10-15): <terse summary of the revision-2 items from protocol-9.3-changes.md> Adopted by consent — accepts 83f0e5, dc5e4c, 3c3084, 4400c2, c162f8, 56bfc1. peers <plugin version>, <merge sha>.` Append with a single write; never delete or reword older lines.

Output: write a report to /Users/ryzhakar/pp/agents-of-anarchy-marketplace/docs/orchestration_log/recon/2026-10-15/adopt-9.3-report.md with: each step's command, exit code, test counts, shas, the exact change line appended, plugin version. End with a 3-sentence summary suitable for a notification.

Tools: Bash (git, just), Read, Edit. Scope: only the steps above; no recommendations.
