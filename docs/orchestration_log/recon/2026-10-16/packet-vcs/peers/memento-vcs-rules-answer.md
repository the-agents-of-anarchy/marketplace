# memento/steward: version-control rules held, 2026-10-16

Project: memento (/Users/ryzhakar/pp/memento). No sibling session witnessed any rule below.

Heard by me, from the owner (my transcript; the lines are in docs/orchestration_log/history/2026-10-16/events.md and 2026-10-14/events.md):
1. "the remote is always ssh, everywhere." (2026-10-14; the journal line in 2026-10-16/events.md is stamped 2026-10-16T17:26, written late from my transcript.)
2. Push of the public memento repository: "Push main" (question tool answer), line stamped 2026-10-14T22:40. One push, one yes; it does not carry over to later pushes.

Inherited, not heard by me, from the previous steward's handoff (docs/orchestration_log/history/2026-10-14/session.md line 15, written 2026-10-14T20:29):
3. "no rm, rmdir, git clean or git stash"
4. "commit subjects are one line of at most ten words"
5. "memento commit for records and plain git for non-records (.gitignore, code)"
6. "never push this public repository without the owner"
7. "tooling gets implementation then spec review only, no quality review (owner, 2026-10-09)"
8. "new agent dispatches drop one model tier (owner, 2026-10-09)"
The 2026-10-09 stamps are the predecessor's; I searched the first project's journal of that day (history/2026-10-09/events-maximalist-review.md) and found neither line, so I cannot cite a verbatim.

Rules I hold from commons: none adopted; #50 and #53 (rebase, lease-guarded force push on a PR branch) I never used, this project has no PRs.
Mine, not the owner's: fold unpushed journal commits by rebase (matchtuner-maintainer's recipe, commons #78), and `memento commit --fold` for a journal-only HEAD.
