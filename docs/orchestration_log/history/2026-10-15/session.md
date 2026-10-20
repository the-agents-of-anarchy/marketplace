# Session 2026-10-15 — resident-anarchist (guest)

Span: resident-anarchist [6a43c8], a guest session of the agents-of-anarchy society, the preparer of the estafette spec and stack. Works only in its worktree /Users/ryzhakar/pp/aoa-marketplace-resident-anarchist on branch integration/resident-anarchist; commit by path, never -A; push continuously. The scribe (proudhon [abf96a]) keeps its own records.

## Standing orders (owner), in force after any compaction
- Silence toward the owner (/work-silently, 2026-10-21 00:16): zero-text turns; answer only the owner's own typed words; harness nudges and peer messages are not the owner. Peers and lab-sibling: communicate freely, at will. Work fully autonomously until the owner stops it; by default there is always work to do.
- Guest: do not join the society; no card, no commons duties; relay to the scribe only on the owner's word.
- Bound: stop-yapping, first-principles, cargo-cult-science, only-what-it-needs, lines-spent, build-for-today, Anarchy 101 (conduct). Subagents bind cargo-cult-science, first-principles, stop-yapping (command form in the brief).
- No explicitly Russian sources, ever.
- Agents: redirect only by TaskStop then SendMessage; never relaunch. Experiments on sonnet, two at a time, foreground runs inside each agent, never commit target/. Never launch work on expectation: work must fall under a ruling. Read every report in full; check load-bearing claims at source before the ledger rests on them; never relay a worker's claim unchecked.
- Records: stamps from `date`; one journal line per event; receipts ride with their work.
- Spec held: apply nothing to spec/blueprint.md; staged revisions live in research/stack/ledger.md and staged-revisions.md.

## The estafette work
- Ground truth: research/stack/ledger.md (surface map, collisions, staged revisions S1-S25), parameters.md (G1-G5; G5 = S23), experiments/e1-e14, lab/linux/ (Linux reruns).
- Rulings 2026-10-20/21: C13 → S24 own fix on iroh-gossip 0.101.0 (relay removal works: re-home 0.7 s; own rejoin fails while dials fail); C14 → S25 own stdin reader (departure under 1 ms, macOS and Linux); C15 → S23; C16 (iroh 1.3.0 relay send path blocks behind a dead relay's full 64-slot queue until its actor's 60 s idle exit; same on iroh main) → a workaround in estafette, plus a detailed internal bug report.
- Running: e14-dials follow-up writing research/stack/experiments/e14-bug-report.md (branch spike/e14-bug-report; minimal deterministic repro, iroh main check, vendored diagnostic patch allowed for this task, candidate fixes, Linux discrepancy). lab-sibling: E10 a-1-w and a-1-npw on Linux (180 s), answer due ~01:00.
- Next (autonomous, under the C16 ruling): design and measure the estafette workaround once the bug report's mechanism and workaround sections are in (sonnet experiment E15, plus a Linux rerun by lab-sibling); then self-announcing hosts (S21) on the 0.101.0 pin with S24 and the workaround.

## Lab
- Server estafette-lab (cx23, nbg1, 178.105.88.14) via the project skill run-hetzner-lab and `just remote::*` (address looked up by name; `just remote` lists recipes). Backstop: hourly launchd job ~/.local/share/estafette-lab/lab-control.py, 24 h deadline per resource (server 2026-10-21 17:33Z); extend with `python3 -I .claude/skills/run-hetzner-lab/lab-control.py extend <kind> <id> <hours>` only while lab work runs, journaled.
- lab-sibling: Claude Code session the owner runs there; owns the machine and /home/lab/work; changes no code; pushes nothing; I pull its reports (rsync -a -e "ssh -F /tmp/ra-lab/ssh_config" lab:work/reports/ ...; backup at ~/.local/state/estafette-lab/sibling-reports/). Peer messaging only: post with `python3 -I research/stack/lab/post.py /tmp/ra-lab/remote.sock "<msg>" --no-auth` over `just remote::forward` (link b51x1fuim; sibling socket /home/lab/sock/lab.sock, dir 0700); its replies arrive as session messages. My files there: /home/lab/ra (briefs, bundles); new branches go to ~/estafette via `git bundle` + fetch. Briefs: complete, exact commands, expected output, what to report, one task per message (owner's private instruction; never mention it). Ask it for one [answer] per task, no notices.
- Never start or configure the sibling session.

## Wake
- One-shot cron at 00:27 (3c662cde) carries the pending checks; crons are session-only.
