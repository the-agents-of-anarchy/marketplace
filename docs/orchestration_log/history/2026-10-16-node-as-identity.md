# Node as identity: propagation through the spec

Author: claude-fable-5-1 (resident-anarchist), 2026-10-16, on the owner's word: "let this node-as-identity assumption propagate and reopen decisions upstream of it." Analysis of spec/blueprint.md (sha1 721acc4b…); no spec edit made. Evidence references are to research/stack/.

## The assumption
N: the card's Ed25519 secret key (the sidecar, D2) is the iroh endpoint key. A member's node id is its card public key, for every session it runs.

## What N rests on (checked)
- iroh's SecretKey and PublicKey are Ed25519 with sign and verify (surveys/f1a-iroh-endpoint.md); the spec's card key is Ed25519 (3.1). One key type serves both.
- A connection's remote id comes from TLS (f1a; experiments/e1-api.md check 4). With N, the remote id *is* the sender's card.

## The key move N enables
Cards are local to one machine (D8). Under N, a second live holder of a card can only be another process on the same machine. A kernel advisory lock (flock) on the card's existing sidecar file, held for the life of the process, settles D6 locally, released by the kernel on any exit, crash included. No protocol, no probe, no tie-break. 3.16's "no lock file" is not broken: the lock sits on a file that already exists.

## Decisions, one by one
| Decision | Under N | Status |
|---|---|---|
| D1 card is identity | holds, strengthened: the network identity is the card | holds |
| D2 key pair, sidecar 0600 | holds; the sidecar also keys the endpoint; agents still never read it | holds |
| D3 fresh transport key per session | replaced by N | reopened: retired |
| D4 claim binds card to transport key | purpose gone; TLS binds node to card. Gossip payloads still need an author signature (gossip hides the author: surveys/f2-gossip.md), so a signature over each gossip payload by the card key replaces the Claim struct | reopened: Claim struct retired, payload signature kept |
| D5 handles | unchanged | holds |
| D6 one live holder, tie-break, probe-gated replacement | settled by the sidecar lock; a restart after a crash simply takes the lock again | reopened: simplified to a lock |
| D7 no lock | reversed by the reasoning above | reopened: reversed |
| D8 cards local | unchanged; it is what makes the lock sufficient | holds, now load-bearing |
| D9 description at claim | unchanged | holds |
| D10 card chosen in session | holds, but the endpoint cannot exist before the card is chosen: the process starts without a node | reopened: start order (below) |
| D11-D13, D15, D16 | unchanged | holds |
| D14 bootstrap member | unchanged (it already has a stable key) | holds |
| D17 every message proves itself | the sender is the TLS remote id; the MAC stays; the claim in the Message goes | reopened: simplified |
| D18-D20 introduction, departure, probe | unchanged in kind; Introduce over a direct stream needs no signature (TLS authenticates it) | holds |
| D21-D31 delivery and surface | unchanged | holds |
| D30, 3.9 state machine | Displaced cannot occur: no one takes a held card mid-session. States: Unclaimed, Claimed, Stopping | reopened: simplified |
| D32 one process per session, agent equals node | holds; the node is born at init, not at process start | reopened: start order |
| D33, D34 inbox socket by pid | unchanged; the inbox listener still starts with the process | holds |
| D40 observer node without card | unchanged: observers keep an ephemeral key | holds |
| D41 operator test send | takes the operator card's lock | holds |

## Spec text that changes
- 3.4: Claim struct and the tie-break and probe paragraphs go. A signed-payload rule replaces them: each gossip payload carries `sig` by the card key over its postcard bytes with `sig` zeroed; the author is `card`, which must verify.
- 3.6: Message drops `from: Claim`; validation steps 3 and 4 vanish (the remote id is the card). Introduce drops its claim. ProbeAck and IntroduceAck drop `claim`.
- 3.7: Presence, Departure, Unreachable carry `card` and `sig` instead of a Claim. Presence shrinks by the Claim's 172 bytes (experiments/e2-size.md), not enough to fit the 4096 default by itself.
- 3.8: the rows "card known, another node" and "your own card from another node" go. A Presence for a known card with a later `ts` updates the entry; an earlier `ts` is ignored (test 20 holds by `ts` alone).
- 3.9: Displaced goes. Start order: inbox listener at process start; endpoint, router, gossip at init. `list_cards`' `held` comes from the local lock, not from the peer table, so the observer wait before the first `list_cards` goes too.
- 3.10: `card_held` means the lock is taken. `init` takes the lock, then builds the endpoint.
- 3.15: test 6 becomes "two processes on one machine claim one card: exactly one gets Claimed, the other `card_held`"; test 18 (restart after SIGKILL) and test 20 (replay) restated without claims.
- 3.16: "Do not replace a held claim without a probe" goes; add "Do not hold a card without its sidecar lock".

## What N fixes from the research
- iroh 1.3.0's address cache grows once per remote ever seen (verify/v1a-iroh-fixes.md): bounded by the number of cards, not sessions.
- Fewer new ids churning through gossip (verify/v1b-gossip-fixes.md): reconnects reuse ids.
- Smaller wire structures: no Claim in Message, Introduce, or the acks.

## What N costs
- A relay sees the same node id every session, so a relay operator can link a card's sessions over time. With a self-hosted relay this is the owner; with n0's relays it is n0. Under D3 they could link sessions only by traffic timing.
- A copied sidecar on a second machine (outside D8) yields two holders the lock cannot see; peers would see one node id from two places. Out of scope by D8, as before.

## Unknowns to test before ruling
1. A process killed while holding the flock: the kernel releases it (expected on macOS and Linux); confirm on both.
2. A peer still holding a stale connection to a crashed node id (up to the 10 s idle timeout) receives a new connection from the restarted process with the same id: does iroh replace the old connection at once, and does gossip see NeighborDown then NeighborUp, or nothing?
3. A dial to that id during the window: which instance answers.

## Update 2026-10-16 15:31 (state/m4-lifecycle.md, sonnet source read, read in full by me)
- Unknown 1: flock freed at once on SIGKILL on macOS (worker's script run); Linux untested; a plain fork inheriting the fd would keep the lock (general knowledge, noted by the worker).
- Unknown 2: iroh-gossip 0.101.0 swaps the send path to a new same-id connection at once (net.rs:773-802); no NeighborDown or NeighborUp if the new one lands first (inferred from hyparview.rs); the same-key reconnect test passed but may not leave a stale accepted connection. iroh-gossip#10 was this stall, closed by #43.
- Unknown 3: relay side: newest same-id registration wins; direct path not found.
- Precedent: mcpmesh binds identity to an exclusive lock in the same root as the key and starts lock, key, bind with gates unarmed, arm, serve.
- Still an experiment: SIGKILL on another process with a live accepted connection at the peer, then same-key restart, watching gossip events and a dial.
