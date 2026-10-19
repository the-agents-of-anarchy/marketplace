# Brief: publish integration/proudhon to main

1. Role: you integrate one session branch into main under the owner's branch model, as a sonnet release agent.
2. Context: repo /Users/ryzhakar/pp/agents-of-anarchy-marketplace, checked out on `integration/proudhon` (the scribe's session branch, records only plus any plugin files it holds). main is fast-forward only behind a GitHub ruleset "main: no rewrite" (no force push, no deletion). Branch model, owner via resident-anarchist, journal /Users/ryzhakar/.local/share/agents-of-anarchy/.. no: repo-local journal of the guest at integration/resident-anarchist history/2026-10-15/events.md lines 16:08 and 16:30: at close or on an explicit trigger: fetch, rebase on origin/main, run the gate, fast-forward main, push; whoever integrates second rebases. The owner's word: "let me close any ambiguity, then publish." and his answer: publish covers records to main. Do not touch the untracked research/stack/ files (the guest's), the guest's worktree/branch, or draft/* branches.
3. Input files: /Users/ryzhakar/pp/agents-of-anarchy-marketplace/CLAUDE.md; any gate definition in the repo (search for "gate" in CLAUDE.md, docs/, scripts/, .github/, Makefile, package.json).
4. Task:
   1. `git fetch origin`; report `git log --oneline origin/main..integration/proudhon | wc -l` and `git log --oneline integration/proudhon..origin/main`.
   2. Find the gate (the check the branch model says to run before main moves). If no gate is defined anywhere, stop and report that; do not invent one.
   3. If the working tree has uncommitted tracked changes, commit them by explicit path (never `git add -A`), subject `docs(records): journal lines`.
   4. `git rebase origin/main` on integration/proudhon; on conflict stop and report, do not resolve by guess.
   5. Run the gate; on failure stop and report its output.
   6. Fast-forward main: `git push origin integration/proudhon:main` (never --force). Then `git push --force-with-lease origin integration/proudhon` only if the rebase rewrote the branch.
   7. Report the new main SHA.
5. Output path: /Users/ryzhakar/pp/agents-of-anarchy-marketplace/docs/orchestration_log/recon/2026-10-16/publish-report.md
6. Report format: sections "Before" (counts), "Gate" (name, command, result), "Rebase" (clean or not), "Main" (old SHA, new SHA, push result), "Problems". Then a 3-sentence summary.
7. Scope: no force push to main; no deletion; no resolving conflicts by guess; no editing of files other than committing existing changes; do not circulate or message peers.
8. Tools: Bash (git), Read, Grep, Write for the report.
9. Prime directive: stop at the first failure and report it; a partial publish is worse than none.
