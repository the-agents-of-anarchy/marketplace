# Session 2026-10-15 — resident-anarchist (guest)

Span: resident-anarchist [6a43c8], a guest session of the agents-of-anarchy society, the preparer of the estafette spec and stack. Works only in its worktree /Users/ryzhakar/pp/aoa-marketplace-resident-anarchist on branch integration/resident-anarchist; commit by path, never -A; push continuously. The scribe (proudhon [abf96a]) keeps its own records.

## Standing orders (owner), in force after any compaction
- Guest: do not join the society; no card, no commons duties; relay to the scribe only on the owner's word.
- Bound: stop-yapping, first-principles, cargo-cult-science, only-what-it-needs, lines-spent, build-for-today, Anarchy 101 (conduct). Subagents bind cargo-cult-science, first-principles, stop-yapping (command form in the brief).
- No explicitly Russian sources, ever.
- Office hours: a round opens only on the owner's typed "i'm present"; questions in the owner's terms, every term explained; one question per call unless the owner asks for rapid fire.
- Agents: redirect only by TaskStop then SendMessage. Read every report in full; check load-bearing claims at source; never relay a worker's claim unchecked.
- Records: run `date` before every stamp; one journal line per event.
- Prose for the owner follows agent-conduct:write-well.

## The estafette work: closed on the owner's word (2026-10-21)
- Owner: "the current spec setup should be good enough then ... this is as far as i'm willing to go in spec itself." No further spec work without a new word.
- Spec applied: spec/blueprint.md (S1-S27, relay HTTPS D51, hosts never rebind on silence per E24), commits ce767d9 and 2c34b10; reports research/stack/spec-apply-report.md, spec-review.md, spec-review-2.md.
- Entry point: research/stack/README.md (index of E1-E25, reports, Linux reruns, code branches, ledger items, known limitations). Owner's view: research/stack/showcase.md. Item status: research/stack/ledger.md.
- Accepted limitations (relay-only paths): a host blocked by the relay bug has no recovery (E25: 10/21 runs, 62-87 s); the deaf rule misses a member that hears host records but not its peers (one run, 71 s); a real strict network never met; QUIC address discovery in the embedded relay unconfirmed.
- Owner's own actions open: post the iroh bug report (research/stack/experiments/e14-bug-report/ and .tar.gz; ISSUE.md is the issue text); optionally ask GitHub to purge the old commits of integration/resident-anarchist (history rewritten 2026-10-21 to remove the home address; old tip 3c5627d).
- Propagated 2026-10-21: notice to proudhon (spec, index, bug report, link skill, history rewrite); lab-sibling told the lab work is finished.

## Lab
- Server estafette-lab (cx23, nbg1) via the project skill run-hetzner-lab and `just remote::*`. Deadline 2026-10-22 18:00Z; the backstop (~/.local/share/estafette-lab/lab-control.py, hourly launchd) keeps a server whose type is sold out in its location, and its IPs, firewall and key with it (owner ruling 2026-10-21). Throwaway servers estafette-e23 and estafette-e24 were created and deleted.
- lab-sibling: the owner's Claude Code session there; idle, told the work is finished. Message link: background `just remote::forward`; it drops on every network change of this Mac and must be reopened. Interim link procedure: .claude/skills/link-remote-peer; generic notes research/stack/lab/remote-peer-link.md.
- Never start or configure the sibling session.
