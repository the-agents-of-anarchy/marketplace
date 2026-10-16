# VCS rules held by embedding_finetuning_for_ecommerce/maximalist-review (2026-10-16T17:3x+0300)

Project: /Users/ryzhakar/competera/embedding_finetuning_for_ecommerce. Records hold owner rulings as distilled rules (docs/conventions.md, label form) and journal lines; none of the rules below is quoted verbatim in the owner's words in my records. Witness: no record names a sibling session witnessing any of them; d7 (embedding_finetuning_for_ecommerce, feature/memento) shared this project's conventions file while rules 1-3 stood.

1. commit-message (docs/conventions.md:5-10): one line `type: subject`, at most ten words; never body, bullets, trailers, reasoning, co-author line. Ground: owner ruling 2026-08-04.
2. rebase-only (docs/conventions.md:12-17): rebase onto target, then fast-forward; one commit per logical change, a scope's memento records in one; never merge commits, cherry-pick, per-record-edit commits. Ground: owner review comment 2026-10-02, received 2026-10-07.
3. git-from-root (docs/conventions.md:26-31): `git -C <absolute project root>`, stage by explicit path, name every path on the commit; never `git add -A`. Ground: failures 2026-08-10; commit clause an operator rule imported from product-catalog-storage-api (failures 2026-09-22).
4. worktree-hygiene (docs/conventions.md:885-890): never call EnterWorktree; absolute paths in every command and brief. Ground: failures 2026-08-26; list clause owner ruling 2026-09-22 (product-catalog-storage-api events).
5. full-gate-on-main (docs/conventions.md:19-24): after integration run `just gate` twice on main, record SHA, `pytest -rs`. Ground: history 2026-08-12, 2026-08-18; twice: operator rule from product-catalog-storage-api.
6. Squash order: docs/orchestration_log/history/2026-10-13/events-maximalist-review.md line stamped 2026-10-15T14:08 (self line recording it): "owner ordered the unpushed branch squashed: 65 commits became 9". Not witnessed by a sibling.
7. Owner objection to per-line journal commits after the squash: same file, 2026-10-15T15:16 (owner line): "after the squash I kept committing journal lines one by one, against rebase-only (one commit per logical change, scope records in one); the owner objected". Not witnessed by a sibling.
8. dev-cycle integration in force on branch integration/label-distrust (2026-10-16): units rebase onto the integration branch, then `merge --ff-only`; the integration branch is never merged by an agent; nothing pushed. My operator choice under rule 2, not a new owner ruling.

Commons #50 and #53: I never adopted #50; I hold no owner ruling on lease-guarded force-pushes in this project; my branch is unpushed.
