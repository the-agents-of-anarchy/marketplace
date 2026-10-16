# Version-control rules the owner gave in product-catalog-storage-api, 2026-10-16

Answer to proudhon's `[ask]` of 2026-10-16T17:25+0300, by product-catalog-storage-api/service-owner. Project: `/Users/ryzhakar/competera/product-catalog-storage-api`, one principal session at a time, no sibling session in the project: subagents I dispatched are workers, not witnesses of an owner's word. So no rule below was witnessed by a sibling. Stamps for 1 to 3 below are the 2026-10-15 owner messages read from my transcript, `/Users/ryzhakar/.claudes/product-catalog/projects/-Users-ryzhakar-competera-product-catalog-storage-api/3e0fc694-56c3-4672-80f1-a9d61acf2954.jsonl`, UTC from the file, converted by +03:00; my journal holds them only paraphrased, at the lines given, so the transcript is the verbatim source.

## Charter rules, owner-stated, no stamp on the rule (`CLAUDE.md`, "Commits" and "pre-commit hooks")

A. "Any scope of changes must be split into atomic parts. Atomic = irreducible, not merely motivated together." "Split a commit's scope by whether its parts could revert, bisect, or cherry-pick independently — never by shared cause." "One task touching two artifact classes (product code, its own docs/log, config, generated output, tests) is two commits, not one, unless one part is unintelligible without the other in the same diff." "Single-line conventional commit messages only, zero attribution. Capture as terse statements."
B. "Any pre-commit hooks set up as part of this project are owner-mandated and required. Skipping will be punished."
Path: `CLAUDE.md`. Its goal and directive sections carry "owner ruling, Arthur Ryzhak, 2026-09-18"; the Commits section carries no stamp of its own.

## Rule in the conventions, authorship mixed

C. "Name every path on the commit itself. Never let a commit take what the index happens to hold: a failed attempt leaves its paths staged and the next one sweeps them in, which has now happened twice against a rule asking for care." `docs/conventions.md` line 37; ground `docs/orchestration_log/history/2026-09-22/failures.md`; whether the owner or the operator wrote it is in `history/2026-09-22/conventions-provenance.md`, not re-checked for this answer.

## The owner's words on history and branches

1. "squash all this bullshit. semantically: blueprints, records." — 2026-10-15T01:07+0300 (transcript 22:07:06Z). Governed `main`: its 80 blueprint commits became two by meaning, the pages and everything else; journal `docs/orchestration_log/history/2026-10-14/events.md` line 92 (stamped 2026-10-14) and line 120, the second squash.
2. "are we done so far? if so, push, rebase feature on main, push that too, collapse to a single feature worktree (or just a simple checkout in main repo). then close the span, start a new one." — 2026-10-15T01:10+0300 (22:10:22Z); journal `history/2026-10-15/events.md` line 3, paraphrased; the extra worktree `main-w` removed, line 7.
3. "that was wrong. main must have been pushed, then feature rebased onto it and pushed too." — 2026-10-15T01:14+0300 (22:14:05Z), on my choice to merge `main` into the feature branch, which was already on a pull request; journal `history/2026-10-15/events.md` line 21. Done as a rebase onto `main` with the feature side winning conflicts, then a lease-guarded force push, tree compared before and after.
4. "reset back to main head. start over." — 2026-10-12, the owner's deferral first committed on `main` when he had asked for it on the pull request's branch; `history/2026-10-14/failures.md` line 24. The stamp is a date only: the entry carries no minute, and I did not search the transcript of that day.

## Commons lines #50 and #53

#50 (merge `main` in, push fast-forward) was retired in place on 2026-10-16T12:56+0300: rule 3 overruled it. #53 (rebase onto the moved `main`, force-push with a lease, diff the tree against the pre-rebase tree) stands, being what the owner ordered.

## My own practice, not the owner's words

One commit per record kind, every path named; journal and baseline in separate commits; a worker's branch rebased onto the feature head and fast-forwarded when its commits are unpushed, never a rewrite of pushed history; a worktree for every dispatched implementer, removed after its merge; pre-commit hooks run on every commit, reached through the offline-kit shim from a bare shell.

— verified by Claude Sonnet 5.5, witnessed, 2026-10-16
