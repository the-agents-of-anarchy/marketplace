# State mechanics brief

Owner (2026-10-16): "specific structs and algorithms of state we will need to design. but mechanics of that state i expect iroh-based projects did settle. especially, similarly focused ones."

Your job: find how similarly focused iroh-based projects settled ONE mechanic of in-memory state (your prompt names it), from their source. Report how it works, why (their docs, commits, issues), and how it is tested. Describe solutions; do not list what projects lack.

estafette context (spec: /Users/ryzhakar/pp/agents-of-anarchy-marketplace/spec/blueprint.md, read only the sections your prompt names): one process per agent session; a member is a card with a persistent Ed25519 key (being reconsidered as the node key itself); presence over iroh-gossip, messages over direct QUIC streams; a peer table keyed by card; handles as labels with first-seen suffixing; a duplicate set of message ids; an inbox buffer of the last 1000 frames replayed by sequence number to a local bridge; no mailbox for absent members, no center.

Sources: clone with `git clone --depth 50` into /tmp/ra-state/<repo> (reuse if present; never delete anything there). Read source and tests; cite path:line at the commit you read. Use `git log` for history when it explains why. A README is a hypothesis.

Write your report with Bash heredoc (or Write) to the path your prompt gives; the owner explicitly requested it. Write incrementally.

Report format:
# {Mechanic}
Date; repos with commit SHAs.
## Per project
### {project}
- Mechanism (data structure, update rule, expiry/eviction, ordering), with path:line
- Why, by their account (quote docs, commits, issues)
- Tests that exercise it (path:line), and whether you ran them (`cargo test <name>` if cheap)
## Options this gives estafette (each: what it is, cost, which project proves it)
## What could make this wrong
