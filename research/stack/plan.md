# Stack research plan

Owner: ryzhakar. Adopted 2026-10-16 ("we follow it"). Orchestrator: resident-anarchist (claude-fable-5-1, now Opus 5.5).

## Question
For estafette (spec: agents-of-anarchy-marketplace `spec/blueprint.md`; repo github.com/the-agents-of-anarchy/estafette), which ranges of functionality do iroh, its ecosystem, and the wider crate world solve; what each costs in our dependency tree; what we copy; what we write.

## Fixed by the owner
- MCP: take the official Rust crate. Not a decision; only version, features, and tree cost are measured.
- Test harness: shallow now, researched later.
- What iroh projects chose: deep.
- Claude Code and pi bridges: out of scope.
- Models, as in the plan the owner adopted: haiku for mechanical work (fetch, parse, measure, index, shallow rows), now in the mix because it is more capable and cheap, always with small context batches (one narrow scope, at most three projects or one crate family per agent); sonnet for the deep source-level rows; opus for the synthesis. Corrected 2026-10-16 on the owner's word: "that's not what i said."

## Round 1 (parallel)
| Agent | Output |
|---|---|
| capabilities: every capability Part 3 of the spec needs, by section, tagged by range | ground/capabilities.md |
| tree: scratch crate outside the repo with iroh 1.x, iroh-gossip, the official MCP crate (stdio server), clap derive; resolved tree, enabled features, small crates already present, MSRVs vs 1.99.1 | ground/tree.md |
| index: awesome-iroh, n0-computer repos and examples, crates.io reverse deps of iroh and iroh-gossip with activity, iroh site project list | index/index.md |

## Round 2 (after round 1; surveys by decision, not by index category)
| Survey | Depth |
|---|---|
| foundation: endpoint, ALPN protocol routing, embeddable relay server, local discovery, tickets; iroh-gossip version, events, stability | deep, source; split across agents by crate |
| projects: presence over gossip | deep, source; batches of at most three projects |
| projects: direct protocol (framing, encoding, any n0 RPC layer) | deep, source; batches |
| projects: identity and membership (signed claims, private networks, tickets as invitations) | deep, source; batches |
| projects: infrastructure (self-hosted relay, bootstrap nodes) | deep, source; batches |
| small pieces: YAML, TOML, JSON lines, UUIDv7, base32, XDG paths, signals; each in-tree, copy, or pull | shallow |
| test harness: what iroh offers for tests | shallow |
| breadth: libraries that already do presence plus direct messaging over iroh | shallow |
Projects agents read source, not READMEs. Outputs: surveys/<slug>.md.

## Round 3
Verify only what round 2 promotes: any library that would take over a whole range of the spec. One agent per candidate, source-level. Contradictions get a resolver. Outputs: verify/<slug>.md.

## Round 4
One opus agent reads every report; writes synthesis/stack.md: per range, the crate that solves it (in tree or new pull), what we copy, what we write; a draft manifest with features. Where a project's practice argues against a spec decision, it lists the point for the owner to deliberate; it never edits the spec. Promoted to estafette docs/reference/ like the bootstrap standard.

## Rules for every agent
Bind cargo-cult-science and stop-yapping. Primary sources: manifests, registry API, source. README claims are hypotheses. Evidence, not recommendations, except the synthesis.

## Progress
| Round | Agent | Status | Output |
|---|---|---|---|
| 1 | r1-capabilities (haiku) | done 2026-10-16 01:01 | ground/capabilities.md: 174 capabilities, 12 ranges, 28 ambiguities |
| 1 | r1-tree (haiku) | done 01:00; file saved by the orchestrator | ground/tree.md: iroh 1.3.0, iroh-gossip 0.101.0, rmcp 3.5.1, clap 4.6.7; 276 crates |
| 1 | r1-index (haiku) | done 01:04 | index/index.md: ~290 entries; prior art found: walkie, alink, agent-swarm, mcpmesh |
| 2 | 13 sonnet + 3 haiku, dispatched 01:10 | running | surveys/: f1-iroh, f2-gossip, f3-relay, p1-presence-n0, p2-presence-trackers, p3-presence-apps, a1-agent-messaging, a2-mcpmesh-buzz, d1-irpc, d2-direct-apps, i1-auth, i2-admission, r1-infra, s1-small-pieces, s2-tests, s3-breadth; shared brief surveys/brief.md |
| 3-4 | | not started | |

## Facts round 1 hands to round 2
- Already in the tree, free to use: tokio, serde, serde_json, postcard, ed25519-dalek, blake3, rand, data-encoding, uuid, tracing, thiserror, bytes, futures, irpc (via iroh-gossip).
- Absent: any YAML crate, toml, any XDG crate, base32.
- irpc is n0's RPC layer and a candidate for the direct protocol of spec 3.6: the direct-protocol survey must read it.
- iroh-gossip is pre-1.0 (0.101.0) while iroh is 1.3.0.

## Ambiguity notes from round 1 (orchestrator's reading)
- Single-claim race: settled by spec D6/D7, tie-break plus probe, no lock.
- Node id text form: iroh's own; the foundation survey confirms which.
- `public` bytes: carried and verified verbatim; no canonical JSON needed.
- The other 25 in ground/capabilities.md go to the synthesis.

## Lessons for dispatch
- Some workers refuse to write report files under their harness's rule against unrequested docs. Every prompt states that the file at the named path is the requested deliverable.
- Haiku workers get one narrow scope and at most three projects or one crate family each.
