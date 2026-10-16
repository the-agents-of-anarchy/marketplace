# Report: ship peers 0.8.0

All steps passed. No failure, no conflict.

## Step 1
- `git -C /Users/ryzhakar/pp/aoa-skills-101 fetch -q` — exit 0
- `rev-parse HEAD origin/draft/10.1-split` — 383554a5171d9a2d31e9a39a095fff3ee50b17da / 383554a5171d9a2d31e9a39a095fff3ee50b17da (both match)
- `just test` in aoa-skills-101 — exit 0, 202 passed (run twice; both 202)

## Step 2
- branch: main
- `git status --short` — empty
- `git merge --no-ff draft/10.1-split -m "feat(peers): peers 0.8.0 — one version, post, gather, ship, self-set dnd"` — exit 0, ort strategy, no conflict, 23 files changed, 215 insertions, 143 deletions
- `just test` in marketplace — exit 0, 202 passed

## Step 3
- peers/.claude-plugin/plugin.json: `"version": "0.8.0"`
- .claude-plugin/marketplace.json peers entry: `0.8.0`

## Step 4
- `git push origin main` — exit 0, `3b37af5..4237ec4  main -> main`
- HEAD (merge sha): 4237ec43b4a505eaae1b16969b199e2840e39d10

## Step 5
- `git worktree remove /Users/ryzhakar/pp/aoa-skills-101` — exit 0
- branch `draft/10.1-split` local: present; origin: present (383554a5171d9a2d31e9a39a095fff3ee50b17da)

## Step 6
File: /Users/ryzhakar/.local/share/agents-of-anarchy/PROTOCOL.md
- `date +%Y-%m-%d` read: 2026-10-15
- `version:` line: `version: 10` -> `version: 0.8.0` (sed, exit 0)
- Appended by two `printf '%s\n' '<line>' >> file` calls (exit 0 each). Lines as written:

Line 1:
```
- 0.8.0 (2026-10-15): from this version the protocol's version is the version of the peers plugin; a card reading a pre-plugin number (9.x, 10) counts as below every plugin version. Skills: tell splits (tell composes, post delivers by level and receiver state), scribe splits (ship writes and announces the enacted text, gather turns requests into a draft, puts it to every live member, closes the round), hand-on dissolves into steward, leave, propose and protocol-change (a proposer re-sends open requests to a new scribe), vouch tells the peer a failed claim came from, dnd is self-set and bounded (state: dnd until <stamp>: <reason>). 27 skills. Adopted by consent — accepts memento/steward, product-catalog-storage-api/service-owner, dotfiles/machine-setup, LLM_MANIFESTOS/manifesto-discovery, embedding_finetuning_for_ecommerce/maximalist-review, claude-skills/instruction-eval. Separated: claude-skills/instruction-eval keeps its loaded text for post:13 (was tell:63), ontology:207, ontology:209, ontology:139 until the owner rules. peers 0.8.0, 4237ec43b4a505eaae1b16969b199e2840e39d10.
```

Line 2:
```
- mapping (2026-10-15): protocol 9.3 was peers 0.5.0; protocol 10 was peers 0.7.0; from 0.8.0 the protocol version is the peers plugin's version.
```

No member card edited. No file under docs/orchestration_log/ edited other than this report.
