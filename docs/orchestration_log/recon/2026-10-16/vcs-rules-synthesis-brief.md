# Brief: synthesize the owner's version-control rules across projects

Role: you are synthesizing version-control rules the owner gave to sessions in several projects into one comparison for the scribe; you read, you write one file, you decide nothing.
Context: eight member sessions answered an ask for the owner's branching, merging, committing and pushing rules. Answers are peer claims, unverified. A rule a sibling session witnessed takes precedence over one only a single session heard; where no sibling witnessed anything, say so and rank by owner-word grade (verbatim with journal path and stamp > verbatim from a transcript > paraphrase > a project's own practice). Precedence between two owner statements: the later one governs, both kept.
Inputs (read all, in full):
1. /Users/ryzhakar/pp/agents-of-anarchy-marketplace/docs/orchestration_log/recon/2026-10-16/vcs-rules-answers.md (every answer, one entry per sender)
2. /Users/ryzhakar/pp/agents-of-anarchy-marketplace/docs/orchestration_log/recon/2026-10-16/branch-model.md (this repo's eight rules, newest)
3. /Users/ryzhakar/competera/product-catalog-storage-api/docs/orchestration_log/history/2026-10-16/vcs-rules-answer.md
4. /Users/ryzhakar/pp/memento/docs/orchestration_log/recon/2026-10-16/vcs-rules-answer.md
5. /Users/ryzhakar/competera/embedding_finetuning_for_ecommerce/docs/orchestration_log/recon/2026-10-16/peers/vcs-rules-answer.md
Task:
1. Per topic (branches, worktrees, rebase vs merge, force pushes, commit size and message form, records commits, when to push or integrate, PRs, remotes and ssh, deletions), list every rule: wording, project, owner-word grade, stamp, source path, sibling witness yes or no.
2. Mark each conflict between rules (same topic, different rule) and say which governs by the precedence above; where precedence cannot settle it, write "owner's call".
3. Mark each rule with its likely reach: this repo only, one project, or plausibly everywhere (do not decide; mark).
4. List what is missing: topics no member holds a rule on.
Output: write to /Users/ryzhakar/pp/agents-of-anarchy-marketplace/docs/orchestration_log/recon/2026-10-16/vcs-rules-synthesis.md as one table per topic plus a conflicts list and a missing list. End with a 3-sentence summary for a notification.
Scope: no recommendations, no new rules, no edits to any input file. Tools: Read, Write, Grep. Bind to first-principles and stop-yapping — show your commitments before working.
