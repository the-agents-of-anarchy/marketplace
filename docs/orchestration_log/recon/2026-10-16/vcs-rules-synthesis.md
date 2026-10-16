# VCS rules synthesis, 2026-10-16

Synthesis of the five input files. No recommendations, no new rules. All entries are peer claims, unverified.

## Keys

Source aliases (bases):
- ANS = `/Users/ryzhakar/pp/agents-of-anarchy-marketplace/docs/orchestration_log/recon/2026-10-16/vcs-rules-answers.md`
- BM = `.../recon/2026-10-16/branch-model.md` (same directory)
- PC = `/Users/ryzhakar/competera/product-catalog-storage-api/docs/orchestration_log/history/2026-10-16/vcs-rules-answer.md`
- ME = `/Users/ryzhakar/pp/memento/docs/orchestration_log/recon/2026-10-16/vcs-rules-answer.md`
- MT = `/Users/ryzhakar/competera/embedding_finetuning_for_ecommerce/docs/orchestration_log/recon/2026-10-16/peers/vcs-rules-answer.md`

Rule IDs: BM1-8 branch-model rules; PC1-4 owner words, PC-A/B/C charter and conventions, PC-P practice; MT1-8; ME1-8; GY gym; MD manifesto-discovery; MS machine-setup; RA resident-anarchist.

Grade (owner-word):
- G1 = verbatim with journal path and stamp
- G2 = verbatim from transcript
- G3 = paraphrase or distilled rule
- G4 = project's own practice

Sibling witness: no rule has a living sibling witness. Two weak exceptions: GY (departed gym manager session, unverifiable) and MT1-3 (d7 shared the conventions file; no record that d7 heard the owner). Witness precedence therefore settles nothing; ranking falls to grade, then to date.

Reach marks (marked, not decided): THIS = this repo only; ONE = one project; ANY = plausibly everywhere.

## 1. Branches

| ID | Rule | Project | Grade | Stamp | Source | Witness | Reach |
|---|---|---|---|---|---|---|---|
| BM1 | main fast-forward only, never rewritten; GitHub ruleset "main: no rewrite" rejects force push and deletion | this repo | G3 (words in RA journal, not in inputs) | 2026-10-16T16:08, 16:30 | BM; journal integration/resident-anarchist `docs/orchestration_log/history/2026-10-15/events.md` | no | THIS (BM scope line: reach is owner's to settle) |
| BM2 | One integration branch per session; scribe's integration/proudhon in repo folder, guest's in separate worktree | this repo | G3 | same | BM | no | THIS |
| BM3 | Work and memento records commit to the session's branch, never to main | this repo | G3 | same | BM | no | THIS |
| BM4 | Ahead of main, reshuffle own branch freely, push it continuously | this repo | G3 | same | BM | no | THIS |
| BM7 | `draft/*` for protocol drafts awaiting consent; integration branches for ongoing work and records | this repo | G3 | same | BM | no | THIS |
| PC4 | "reset back to main head. start over." Deferral committed on main when owner asked for it on the PR branch | product-catalog | G1 (date-only stamp) | 2026-10-12 | PC; `history/2026-10-14/failures.md` line 24 | no | ONE |
| PC2 | "...push, rebase feature on main, push that too, collapse to a single feature worktree (or just a simple checkout in main repo)..." | product-catalog | G2 | 2026-10-15T01:10+0300 | PC; transcript `/Users/ryzhakar/.claudes/product-catalog/projects/-Users-ryzhakar-competera-product-catalog-storage-api/3e0fc694-56c3-4672-80f1-a9d61acf2954.jsonl` | no | ONE |
| MT8 | Integration branch integration/label-distrust; units rebase onto it, `merge --ff-only`; integration branch never merged by an agent | embedding_finetuning | G4 (operator choice under MT2) | 2026-10-16 | MT | no | ONE |
| MS-P | Commits directly on main in three repos; no branches | dotfiles et al. | G4 | none | ANS (machine-setup-manager) | no | ONE |
| GY | No rule on branches | gym | none | none | ANS | n/a | n/a |

## 2. Worktrees

| ID | Rule | Project | Grade | Stamp | Source | Witness | Reach |
|---|---|---|---|---|---|---|---|
| BM2 | Guest's integration branch lives in a separate worktree | this repo | G3 | 2026-10-16 | BM | no | THIS |
| BM8 | On pruning a worktree, untracked files go by hand to the same relative path in the repo folder, then prune | this repo | G3 | 2026-10-16 | BM | no | THIS |
| MD-wt | Worktree per sibling (petro-iteration), "on the owner's ruling"; second-hand, the sibling's rule | LLM_MANIFESTOS | G3 | 2026-10-13 | ANS; `/Users/ryzhakar/LLM_MANIFESTOS/orchestration_log/history/2026-10-12/events-llm-manifestos-0d.md` line 71 | second-hand via sibling | ONE |
| PC2 | Collapse to a single feature worktree or a simple checkout in the main repo (extra worktree `main-w` removed) | product-catalog | G2 | 2026-10-15T01:10 | PC | no | ONE |
| MT4 | Never call EnterWorktree; absolute paths in every command and brief. Ground: failures 2026-08-26; list clause owner ruling 2026-09-22 | embedding_finetuning | G3 | 2026-08-26, 2026-09-22 | MT; `docs/conventions.md:885-890` | no | ONE |
| PC-P | Worktree per dispatched implementer, removed after its merge | product-catalog | G4 | none | PC | no | ONE |
| MS-P | No worktrees | dotfiles et al. | G4 | none | ANS | no | ONE |

## 3. Rebase vs merge

| ID | Rule | Project | Grade | Stamp | Source | Witness | Reach |
|---|---|---|---|---|---|---|---|
| PC3 | "that was wrong. main must have been pushed, then feature rebased onto it and pushed too." Context: owner rejected merging main into a feature branch already on a PR | product-catalog | G2 | 2026-10-15T01:14+0300 | PC; journal `history/2026-10-15/events.md` line 21 | no | ONE; ANY (rebase-over-merge recurs in BM5, MT2) |
| PC2 | Rebase feature on main (see section 1) | product-catalog | G2 | 2026-10-15T01:10 | PC | no | ONE |
| MT2 | Rebase onto target, then fast-forward; one commit per logical change; never merge commits, cherry-pick, per-record-edit commits | embedding_finetuning | G3 (distilled, not verbatim) | owner review comment 2026-10-02, received 2026-10-07 | MT; `docs/conventions.md:12-17` | no | ONE; ANY (as above) |
| BM5 | At close or explicit trigger: fetch, rebase on origin/main, run the gate, fast-forward main, push; second integrator rebases on the new main | this repo | G3 | 2026-10-16 | BM | no | THIS |
| #53 | Rebase onto the moved main, lease-guarded force push, diff tree against pre-rebase tree; stands | commons (product-catalog origin) | G3 | stands per PC | PC; ANS | no | ANY (commons line) |
| #50 | Merge main in, push fast-forward; retired. ANS: owner retired it at 2026-10-15T01:14; PC: retired in place 2026-10-16T12:56 by overruling via PC3 (same fact, two stamps: owner word 15th, commons edit 16th) | commons | G2 for the word (= PC3) | see left | ANS; PC | no | ANY (commons line) |
| ME-P | Fold unpushed journal commits by rebase (commons #78 recipe); `memento commit --fold` for journal-only HEAD | memento | G4 | none | ME | no | ONE |
| PC-P | Worker branch rebased onto feature head and fast-forwarded when unpushed | product-catalog | G4 | none | PC | no | ONE |
| adopted neither #50 nor #53 | machine-setup-manager (no PRs/pushes); memento (no PRs); resident-anarchist holds neither; matchtuner never adopted #50 | various | n/a | n/a | ANS; ME; MT | n/a | n/a |

## 4. Force pushes

| ID | Rule | Project | Grade | Stamp | Source | Witness | Reach |
|---|---|---|---|---|---|---|---|
| BM1 | GitHub ruleset rejects force push to main | this repo | G3 | 2026-10-16 | BM | no | THIS |
| BM4 | Reshuffle own ahead-of-main branch freely and push continuously (force push not named; rewrite of pushed own branch implied) | this repo | G3 | 2026-10-16 | BM | no | THIS |
| PC3 / #53 | Lease-guarded force push of the rebased feature branch (performed as ordered) | product-catalog | G2 | 2026-10-15T01:14 | PC | no | ONE |
| MT | No force-push ruling | embedding_finetuning | none | n/a | MT; ANS | n/a | n/a |
| PC-P | Never rewrite pushed history of a worker branch | product-catalog | G4 | none | PC | no | ONE |
| GY, ME, MS, MD, RA | No force-push rule stated | n/a | none | n/a | inputs | n/a | n/a |

## 5. Commit size and message form

| ID | Rule | Project | Grade | Stamp | Source | Witness | Reach |
|---|---|---|---|---|---|---|---|
| MT1 | One line `type: subject`, at most ten words; no body, bullets, trailers, reasoning, co-author line | embedding_finetuning | G3 | owner ruling 2026-08-04 | MT; `docs/conventions.md:5-10` | weak (d7 shared file) | ONE |
| ME4 | Commit subjects one line of at most ten words (inherited from predecessor handoff) | memento | G3 (second-hand) | handoff written 2026-10-14T20:29 | ME; `docs/orchestration_log/history/2026-10-14/session.md` line 15 | no | ONE |
| GY-form | One-line `type(scope): subject`; no body, trailer, attribution, co-author line. One logical change per commit | gym | G3 (conventions, journal unchecked) | owner ruling 2026-09-26 | ANS; `/Users/ryzhakar/pp/gym/docs/conventions.md` § Commit | departed gym manager | ONE |
| PC-A | "Any scope of changes must be split into atomic parts. Atomic = irreducible, not merely motivated together." Split by whether parts could revert, bisect or cherry-pick independently, never by shared cause. Two artifact classes (code, docs/log, config, generated output, tests) = two commits unless one is unintelligible without the other. "Single-line conventional commit messages only, zero attribution." | product-catalog | G3 (verbatim in charter; section carries no stamp; goal/directive sections stamped 2026-09-18) | none on rule | PC; `CLAUDE.md` "Commits" | no | ONE |
| MT2 | One commit per logical change | embedding_finetuning | G3 | 2026-10-02 | MT | no | ONE |
| MS-P | One commit per logical change | dotfiles et al. | G4 | none | ANS | no | ONE |
| MS-own | "you own this. you cannot just stand with some changes and not take ownership over them. this is all yours to deal with." Governed leaving changes uncommitted | dotfiles | G2 | about 2026-10-15T13:00+0300 | ANS; transcript `/Users/ryzhakar/.claudes/meta/projects/-Users-ryzhakar-dotfiles/2399b19a-1f85-42ef-b808-4122a6ef884f.jsonl` | no | ONE; ANY (generic ownership of changes) |
| attribution | No attribution lines in commits and PRs. MS: harness reminder, not typed owner words; memento/steward journal records owner's yes to `"attribution": false` in shared settings. MD: harness. Also in MT1, GY-form, PC-A | several | G3 | n/a | ANS; MT; PC | no | ANY |
| explicit paths | Name every path on the commit; never take what the index holds: PC-C (authorship owner-or-operator unchecked; `docs/conventions.md` line 37; ground `history/2026-09-22/failures.md`; provenance in `history/2026-09-22/conventions-provenance.md`); MT3 (`git -C <abs root>`, stage by explicit path, never `git add -A`; commit clause operator rule imported from product-catalog, ground failures 2026-08-10, 2026-09-22); MD (practice after shared index nearly mixed files) | product-catalog, embedding_finetuning, LLM_MANIFESTOS | G3 / G4 (not shown to be owner words) | 2026-08-10, 2026-09-22 | PC; MT; ANS | no | ONE; ANY (three projects) |
| hooks/gates | PC-B: "Any pre-commit hooks set up as part of this project are owner-mandated and required. Skipping will be punished." (`CLAUDE.md`, G3, no stamp). GY: commit only on 0 FAIL after `gym records check` passes (2026-09-26). MT5: after integration run `just gate` twice on main, record SHA, `pytest -rs` (history 2026-08-12, 2026-08-18; "twice" is an operator rule from product-catalog). BM5: run the gate before fast-forwarding main | per project | G3 | as stated | PC; ANS; MT; BM | no | ONE each |

## 6. Records commits

| ID | Rule | Project | Grade | Stamp | Source | Witness | Reach |
|---|---|---|---|---|---|---|---|
| BM3 | Records commit to the session's branch, never main | this repo | G3 | 2026-10-16 | BM | no | THIS |
| BM6 | Records cite a SHA only once it is on main; work ahead of main is cited by branch and file path | this repo | G3 | 2026-10-16 | BM | no | THIS |
| RA-squash | "the research work and the memento records work must be squashed to their minimum possible linear commits." Scope: everything after the 0.8.0 commit; shape: one per kind per day; old history: keep a backup ref | this repo | G1 | 2026-10-16T15:55+0300 | ANS; journal integration/resident-anarchist `docs/orchestration_log/history/2026-10-15/events.md` | no | THIS |
| ME5 | `memento commit` for records, plain git for non-records (.gitignore, code) | memento | G3 (second-hand) | handoff 2026-10-14T20:29 | ME | no | ONE |
| GY-rec | Memento changes: one `chore(memento): <kind>` commit per batch | gym | G3 | owner ruling 2026-09-26 | ANS | departed gym manager | ONE |
| MT2 | A scope's memento records in one commit; never per-record-edit commits | embedding_finetuning | G3 | 2026-10-02 | MT | no | ONE |
| MT6 | Owner ordered the unpushed branch squashed: 65 commits became 9 (self line) | embedding_finetuning | G3 | 2026-10-15T14:08 | MT; `docs/orchestration_log/history/2026-10-13/events-maximalist-review.md` | no | ONE |
| MT7 | Owner objected to per-line journal commits after the squash (owner line, same file) | embedding_finetuning | G3 | 2026-10-15T15:16 | MT | no | ONE |
| PC1 | "squash all this bullshit. semantically: blueprints, records." Main's 80 blueprint commits became two by meaning (pages; everything else) | product-catalog | G2 | 2026-10-15T01:07+0300 | PC; transcript (22:07:06Z); journal `history/2026-10-14/events.md` lines 92, 120 | no | ONE; ANY (squash-by-meaning recurs in RA, MT6) |
| PC-P | One commit per record kind, every path named; journal and baseline in separate commits | product-catalog | G4 | none | PC | no | ONE |

## 7. When to push or integrate

| ID | Rule | Project | Grade | Stamp | Source | Witness | Reach |
|---|---|---|---|---|---|---|---|
| BM4 | Push own branch continuously | this repo | G3 | 2026-10-16 | BM | no | THIS |
| BM5 | Integrate at close of work or explicit trigger | this repo | G3 | 2026-10-16 | BM | no | THIS |
| RA-push | "push repo" | this repo (estafette) | G1 | 2026-10-16T00:46+0300 | ANS; RA journal | no | THIS |
| RA-claim | "ask them to claim repo under this name for us." | this repo (estafette) | G1 | 2026-10-15T23:52+0300 | ANS; RA journal | no | THIS |
| MD-push1 | "push and notify them it's live". Governed pushing main with a new manifesto | LLM_MANIFESTOS | G1 (not re-read by sender; stamp "about") | about 2026-10-15T22:26+0300 | ANS; `/Users/ryzhakar/LLM_MANIFESTOS/orchestration_log/history/2026-10-14/events-participation.md` line 40 (repeated 43) | no | ONE |
| MD-push2 | "i push as i see fit. i did." (journal records the fact, not the quote) | LLM_MANIFESTOS | G2 | about 2026-10-12 20:00 local | ANS; transcript; `.../history/2026-10-12/events-llm-manifestos-0d.md` line 20 | no | ONE |
| PC2 | "...if so, push, rebase feature on main, push that too..." | product-catalog | G2 | 2026-10-15T01:10 | PC | no | ONE |
| PC3 | Main pushed first, then feature rebased onto it and pushed | product-catalog | G2 | 2026-10-15T01:14 | PC | no | ONE |
| GY-push | Commit a finished unit at once after `gym records check` passes; never push without the owner's word | gym | G3 | owner ruling 2026-09-26 | ANS | departed gym manager | ONE |
| ME1-push | "Push main" (question-tool answer): one push, one yes, does not carry over | memento | G1 | 2026-10-14T22:40 | ME; ANS | no | ONE |
| ME6 | Never push this public repository without the owner | memento | G3 (second-hand) | handoff 2026-10-14T20:29 | ME | no | ONE |
| MT-P / MS-P | Nothing pushed (unpushed branch; no pushes) | embedding_finetuning, dotfiles | G4 | 2026-10-16 | MT; ANS | no | ONE |

## 8. PRs

| ID | Rule | Project | Grade | Stamp | Source | Witness | Reach |
|---|---|---|---|---|---|---|---|
| PC3 | No merge of main into a branch on a PR; rebase onto pushed main, push the feature too | product-catalog | G2 | 2026-10-15T01:14 | PC | no | ONE |
| PC4 | Owner's deferral belongs on the PR's branch, not on main | product-catalog | G1 (date-only stamp) | 2026-10-12 | PC; `history/2026-10-14/failures.md` line 24 | no | ONE |
| #53 | Lease-guarded force push after rebase of a PR branch | commons | G3 | stands | PC | no | ANY |
| attribution | No attribution in PR descriptions (MS: harness reminder) | dotfiles | G3 | n/a | ANS | no | ANY |
| ME / MT | No PRs in these projects (ME); branch unpushed (MT) | n/a | none | n/a | ME; MT | n/a | n/a |

## 9. Remotes and ssh

| ID | Rule | Project | Grade | Stamp | Source | Witness | Reach |
|---|---|---|---|---|---|---|---|
| ME1 | "the remote is always ssh, everywhere." Journal line in `history/2026-10-16/events.md` stamped 2026-10-16T17:26, written late from transcript | memento (owner wording says everywhere) | G2 | 2026-10-14 (date only) | ME; ANS | no | ANY (stated) |
| BM1 | GitHub ruleset on main (remote-side enforcement) | this repo | G3 | 2026-10-16 | BM | no | THIS |
| RA-claim | Claim repo under this name (ownership on remote) | this repo | G1 | 2026-10-15T23:52 | ANS | no | THIS |

## 10. Deletions

| ID | Rule | Project | Grade | Stamp | Source | Witness | Reach |
|---|---|---|---|---|---|---|---|
| ME3 | "no rm, rmdir, git clean or git stash" (inherited) | memento | G3 (second-hand) | handoff 2026-10-14T20:29 | ME; `history/2026-10-14/session.md` line 15 | no | ONE |
| BM1 | Ruleset rejects deletion of main | this repo | G3 | 2026-10-16 | BM | no | THIS |
| BM8 | Prune worktree only after moving untracked files by hand | this repo | G3 | 2026-10-16 | BM | no | THIS |
| RA-squash | Squash old history: keep a backup ref | this repo | G1 | 2026-10-16T15:55 | ANS | no | THIS |
| PC-P | Worktree removed after its merge | product-catalog | G4 | none | PC | no | ONE |
| PC4 | "reset back to main head. start over." (discard and restart) | product-catalog | G1 (date-only) | 2026-10-12 | PC | no | ONE |

Excluded as not VCS: ME7 (tooling gets implementation then spec review only, owner 2026-10-09) and ME8 (agent dispatches drop one model tier, owner 2026-10-09). ME notes it could not verify either stamp.

## Conflicts

Precedence: sibling witness (none) > owner-word grade > later owner statement governs, both kept.

1. Commit subject form. MT1 `type: subject`, at most ten words (2026-08-04) and ME4 ten-word cap vs GY-form `type(scope): subject` (2026-09-26) vs PC-A "conventional" single line (unstamped). GY-form is later than MT1 but all are per-project; no owner statement spans projects. Owner's call.
2. Who may push, and when. GY-push and ME6 "never push without owner" (2026-09-26; handoff 2026-10-14) vs BM4 "push continuously" (2026-10-16) vs RA-push, MD-push1, PC2 explicit push orders vs MD-push2 "i push as i see fit". In this repo BM4 governs (later; explicit pushes of RA agree). In gym and memento the local never-push rule stands. Whether BM4 reaches them: owner's call. MD-push2 reads as the owner's own push; it neither grants nor denies the sessions.
3. Rewriting main. PC1 (main's commits squashed, 2026-10-15; state before push per PC2 order) vs BM1 "main never rewritten" (2026-10-16). BM1 governs in this repo (later). Reach to product-catalog, and whether PC1 applies only before the first push: owner's call.
4. Rewriting pushed history. PC-P "never rewrite pushed history" (G4) vs BM4 and PC3/#53 (rewrite of pushed own or feature branch, owner words). Owner word outranks practice: rewrite of non-main branches stands, main excluded (BM1). MT: no ruling.
5. Commits straight to main. MS-P (G4, no branches) vs BM3 and PC4 (never main). MS-P is practice; owner has no stated rule for dotfiles. BM3 governs this repo; its reach to dotfiles: owner's call.
6. Worktrees. MD-wt (worktree per sibling, 2026-10-13, second-hand) vs PC2 (collapse to single worktree, 2026-10-15) vs MT4 (never EnterWorktree) vs BM2 (guest in separate worktree, 2026-10-16). BM2 governs this repo (latest). PC2 concerned one feature's extra worktree, not sibling sessions. MT4 bans the tool, not worktrees. Cross-project reach: owner's call.
7. Granularity of records commits. MT2/MT7 (one per scope, no per-edit commits) vs GY-rec (one per batch) vs PC-P (one per record kind) vs RA-squash (one per kind per day) vs ME-P (fold into HEAD). Same direction (batch, do not commit per edit), different unit. Latest owner word: RA-squash (2026-10-16T15:55), this repo only. Cross-project unit: owner's call.
8. Records and work in one commit. PC-A (two artifact classes = two commits unless unintelligible apart) vs MT2 "a scope's memento records in one" (does not say whether work joins them). Unresolved by the inputs. Owner's call.
9. `rm`-class ban vs worktree pruning. ME3 (no rm, rmdir, git clean, git stash; memento only) vs BM8 and PC-P (prune or remove worktrees). Different mechanisms, different projects; whether pruning counts as removal under ME3: owner's call.
10. Discrepancy, not a rule conflict: #50 retirement stamp (ANS: owner word 2026-10-15T01:14; PC: commons edit 2026-10-16T12:56). Owner word is PC3 at 01:14; the 12:56 stamp is the commons edit. Both kept.

No conflict found on rebase over merge: PC3, PC2, MT2, BM5, MT8 agree. Cherry-pick ban stands only in MT2.

## Missing

No member holds a rule on:
- tags, releases, version bumps (0.8.0 is named in RA-squash only as a boundary)
- branch naming (only `draft/*` and `integration/*` appear, in BM)
- branch deletion after merge
- PR creation, review, merge method, who merges
- amend, revert, reset beyond PC4
- `--no-verify` outside PC-B
- signing
- conflict-resolution policy (PC3 "feature side winning" appears once as an act, not a rule)
- multiple remotes, forks, remote naming, repo visibility and creation
- stash (only ME3 bans it)
- cherry-pick outside MT2
- large files, submodules, .gitignore beyond ME5
- CI
- which member may push or integrate main
- whether any rule spans projects, beyond ME1 ("everywhere") and the BM scope line

## Summary

Eight sessions yielded about 70 rules; none has a living sibling witness, so ranking falls to grade and date, and only RA, MD, ME1-push, PC4 and the BM journal citations reach G1. Rebase-then-fast-forward, no attribution, and squash-by-meaning recur across three or more projects; the unsettled points are commit subject form, who may push, rewriting main, worktrees, and records-commit granularity, each marked "owner's call" for cross-project reach. Missing: tags, branch naming and deletion, PR merge method, amend and revert, and any cross-project scope beyond ME1 "ssh everywhere".
