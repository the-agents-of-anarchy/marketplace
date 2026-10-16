# Specimen brief: the agent-habilis family

The owner wants "a deeper look into them. as a specimen, not an example to follow necessarily. and surely not as direct future reference."

So: study the agent-habilis projects the way a naturalist studies a specimen. Describe what they built, how it works, what their own docs and history say about why, and where it fails or strains. Do NOT recommend adopting, copying, or following anything. Do NOT judge them against estafette's spec except where your prompt asks. The RFC repo is empty; skip it.

Your prompt names your scope and your output file. That file is the deliverable the owner explicitly requested; write it with Bash (`cat > path <<'EOF'`), incrementally, so a cut-off run still leaves a usable file.

## Sources
- github.com/agent-habilis/agent-gossip, github.com/agent-habilis/agent-swarm, github.com/agent-habilis/habilis-network.
- Clone into /tmp/ra-spec/<repo> with `git clone --filter=blob:none` (history without all blobs) when absent; reuse when present; never delete anything under /tmp/ra-spec.
- History is evidence: `git log --oneline`, `git log --stat -- <path>`, commit messages, CHANGELOG, release notes (`gh release list -R agent-habilis/<repo>`), issues (`gh issue list -R agent-habilis/<repo> --state all --limit 50`).
- Earlier surveys exist; grep them, do not repeat them: /Users/ryzhakar/pp/agents-of-anarchy-marketplace/research/stack/surveys/a3-habilis.md, a1b-agent-swarm-mcp.md, s3-breadth.md.

## Rules
1. Cite every claim: path:line at a named commit, a commit SHA, a release, or an issue number.
2. Distinguish what the code does from what the docs say; report mismatches.
3. Small context: grep first, read files in parts, read only what answers your scope. List what you did not read.

## Report format
# {Scope}
Date. Repos and commits read.
## What it is (3-5 sentences)
## How it works (mechanisms with citations)
## Why, by their own account (docs, commit messages, issues; quoted)
## How it evolved (history: designs added, removed, reverted; dated)
## Where it strains (bugs, open issues, doc/code mismatches, self-flagged weaknesses)
## Observations for the owner (descriptive, no prescriptions)
## Not read
