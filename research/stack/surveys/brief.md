# Round 2 brief, shared by every survey agent

Your prompt names your scope and your output file. That file is the deliverable the owner and orchestrator explicitly requested; write it with the Write tool or a heredoc. No other files.

## Project
estafette: a Rust binary that lets AI agent sessions message each other across machines. Spec: /Users/ryzhakar/pp/agents-of-anarchy-marketplace/spec/blueprint.md. Read only the sections your prompt names. In short: each session runs one process = one iroh node with an ephemeral key; a member is a card (Ed25519 key in a local file) bound to the node by a signed claim; presence travels over iroh-gossip (one topic per network, derived from a shared secret; Presence, Departure, Unreachable payloads; no heartbeats; introductions to new neighbors; probe before declaring a peer dead); messages travel over direct QUIC streams, one request and one response per stream, postcard-encoded, with a MAC keyed from the network secret; an embedded relay plus a cardless bootstrap node in one infrastructure process; an MCP server over stdio with six static tools; an inbox on a Unix socket. No mailbox, no store-and-forward, no center.

## Facts from round 1 (measured)
- Toolchain 1.99.1. iroh 1.3.0 (defaults: metrics, fast-apple-datapath, portmapper, tls-ring), iroh-gossip 0.101.0 (net, metrics), rmcp 3.5.1, clap 4.6.7.
- Already in the tree: tokio, serde, serde_json, postcard, ed25519-dalek 3.0.0, blake3, rand 0.10, data-encoding, uuid, tracing, thiserror 2, bytes, futures, irpc 0.17.0 (via iroh-gossip).
- Absent: any YAML crate, toml, any XDG crate, base32.
- Ecosystem index: /Users/ryzhakar/pp/agents-of-anarchy-marketplace/research/stack/index/index.md (grep it for your projects; do not read it whole).

## Rules
1. Primary sources only: the crate source (clone shallowly to /tmp/ra-src/<name>, or read files via `gh api` / raw URLs), Cargo.toml, docs.rs pages for the exact version, the registry API. A README is a hypothesis.
2. Cite every claim: repo path and line (`src/foo.rs:120`) or URL.
3. Report evidence. No adopt/reject verdicts; that belongs to the synthesis. You may say what a project does that estafette could take: a crate to depend on, a pattern to copy, or nothing.
4. Where a project's design argues against a spec decision, name the decision (D-number or section) and the evidence. Do not argue for or against; record it.
5. Keep your context small: read the files that answer your scope, not whole repos. Note what you did not read.
6. Clean up /tmp/ra-src/<name> when done.

## Report format (projects and foundation surveys)
# {Scope}
Date. Sources read (repos with commit SHA, files).
## Per project or crate
### {name} ({repo}, commit, iroh version it uses)
- What it does for this scope: 2-3 sentences.
- How, in code: the mechanism, with file:line citations.
- Crates it uses for this: names and versions from its Cargo.toml.
- Maturity: last commit, release count, tests present for this mechanism (yes/no, where).
- What estafette could take: crate / pattern / nothing, one line each.
- Against the spec: decision and evidence, or "none found".
## Cross-project observations
[patterns seen in 2+ projects, with citations]
## Not read
