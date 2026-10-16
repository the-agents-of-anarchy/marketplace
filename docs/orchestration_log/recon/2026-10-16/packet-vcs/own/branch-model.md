# Branch model, as the owner ruled it (2026-10-16T17:25+0300, relayed by resident-anarchist; owner words in its journal, integration/resident-anarchist, docs/orchestration_log/history/2026-10-15/events.md, entries 2026-10-16T16:08+0300 and 16:30+0300)

Scope: this repo (the-agents-of-anarchy/marketplace). Whether it reaches other projects is the owner's to settle; see the ask in recon/2026-10-16/vcs-rules-ask.md.

1. main: fast-forward only, never rewritten; a GitHub ruleset "main: no rewrite" rejects force pushes and deletion.
2. One integration branch per session; the scribe's integration/proudhon is checked out in the repo folder, the guest's lives in a separate worktree.
3. Work and memento records commit to the session's branch, never to main.
4. Ahead of main, reshuffle your own branch freely and push it continuously.
5. At close of work or on an explicit trigger: fetch, rebase on origin/main, run the gate, fast-forward main, push. Whoever integrates second rebases on the new main.
6. Records cite a SHA only once it is on main; work ahead of main is cited by branch and file path.
7. draft/* branches stay for protocol drafts awaiting consent; integration branches carry ongoing work and records.
8. On pruning a worktree, untracked files in it go by hand to the same relative path in the repo folder, then prune.
