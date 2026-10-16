# Buzz (Block) agent workspaces on iroh

Date: 2026-10-16.

## Sources read

- https://iroh.computer/blog/buzz-agent-workspaces, fetched with `curl -sL` (HTTP 200, 75963 bytes). Saved to /tmp/ra-src/buzz-page/buzz.html. Text extracted locally with /tmp/ra-scripts/extract_text.py under `python3 -I`. Dated September 22, 2026, byline Rae McKelvey, hosted on the iroh site. The text does not state the author's affiliation.
- https://github.com/block/buzz: top-level listing only, via `gh api repos/block/buzz/contents`, plus repo metadata. Public, default branch `main`, last push 2026-10-16. No file read. Commit SHA not recorded.
- spec/blueprint.md lines 1-63 (Part 1, sections 1.1-1.9).

## Per project or crate

### Buzz and MeshLLM (github.com/block/buzz, commit not recorded, iroh version not stated)

- **What it does for this scope:** Buzz is a community workspace for people and agents. MeshLLM, which the post says is built into Buzz, shares members' spare compute for inference over iroh. The post says sharing is opt-in: "Sharing is entirely opt-in."
- **How, in the post:** The post is the only source. No code was read.
  - Discovery: "The desktop runtime publishes a signed, replaceable discovery note containing the member's MeshLLM owner identity and current iroh endpoint. Other members resolve available serving targets from the relay, validate the endpoint and relay policy locally, and then connect through MeshLLM."
  - Selection gate: a target "becomes selectable only when its endpoint binding is valid, its invite token decodes to a bounded iroh endpoint, and every advertised relay URL matches the machine's locally configured iroh relay policy."
  - Local interface: an OpenAI-compatible endpoint at `127.0.0.1:9337/v1`. The model name or `auto` maps to MeshLLM's virtual mesh model.
  - Inter-relay mesh: "one iroh endpoint per relay runtime. Each runtime gets a unique iroh keypair. Peers exchange attested readiness records, gossip membership, and move fenced tunnel traffic over QUIC streams and datagrams." The crate name is not given. The repo's `crates/` directory exists and was not opened.
  - Wire contract, as tabled in the post: ALPN `buzz/mesh/1`; QUIC bidirectional streams for "Reliable tunnel traffic and control"; QUIC datagrams for "Real-time media, including huddle audio"; `FencedHeader{session_id, generation, owner_runtime_id}` on session-bearing frames; "Redis CAS lease" as the ownership arbiter. The post says "mesh membership is only a routing hint."
- **Iroh pieces the post names:** QUIC connections, QUIC bidirectional streams, QUIC datagrams, endpoint identity by public key, and "global endpoint address lookup," linked to docs.iroh.computer/concepts/address-lookup. The post names no gossip crate. Its phrase "gossip membership" does not say which gossip stack carries it. The post also uses "iroh relay policy" for relay URLs, which is a separate thing from "Buzz relay."
- **Addressing:** "Every iroh endpoint is already identified by a public key. The address is not 'this IP and port'; it is 'this endpoint.'" A member is reached by endpoint identity. The endpoint is found through the signed discovery note fetched from the Buzz relay, plus address lookup.
- **Presence:** The post defines no presence protocol. It names these mechanisms: the signed, replaceable discovery note; "signed status" held by the Buzz relay; attested readiness records and gossip membership between relay runtimes. It does not describe how departure or unreachability is detected.
- **Storage:** The post's table gives the Buzz relay "Membership, signed status, discovery, and workspace history." Where message content is stored is not stated. The post says inference traffic "does not run through the Buzz relay." Session ownership sits in a Redis CAS lease.
- **Maturity:** Public repo, pushed 2026-10-16. Release count, commit count, and tests for the mesh code were not checked. No Cargo.toml was read, so no crate versions are known.
- **What estafette could take:** Nothing is taken from the post directly. Two patterns are worth checking in code: a signed, replaceable discovery record that a receiver validates before selecting a peer, and a generation number in a session header to reject stale ownership. Both are described in the post only.
- **Against the spec:**
  - Spec 1.7 says "No center of authority or memory." The post says the Buzz relay holds "workspace history" and "discovery," and that ownership is arbitrated by a Redis lease. For Buzz, this is a central holder of state. Recorded, not weighed.
  - Spec 1.8 says "Coordination lives in the behavior of members, not in the pipe." The post places session ownership in a relay-side lease, outside member behavior.
  - Spec 1.4 and 1.5 say there is no mailbox and delivery is "now or not at all." The post's "workspace history" held by the relay does not say whether messages are included. Unresolved.
  - Spec 1.9 says "A network has one owner." The post describes a community of many admitted members, admitted by Buzz membership. Recorded.
  - Spec 1.6 requires every message to prove its sender. The post's discovery notes are "member-signed, endpoint-bound, size-bounded, and policy-checked." The shape is similar. The post does not say whether message traffic carries the same proof.

## Cross-project observations

Only one project was surveyed. No cross-project pattern.

## Limits of this evidence

- The source is a vendor post on the iroh site about a partner's product. The post's own claims are unmeasured. It gives no throughput, latency, or failure figures. It says sharing "can reduce inference costs" without numbers.
- The post says "Iroh ... is already running in production on hundreds of thousands of devices." This is unverified.
- The post says the inference path avoids "a central server," and it also places discovery, membership, workspace history, and session ownership on the Buzz relay. Both statements are in the post. Neither is resolved here.
- The post argues against libp2p in one sentence. The linked comparison was not read.

## Not read

- Spec beyond line 63.
- Linked pages: /blog/mesh-llm, /blog/comparing-iroh-and-libp2p, docs.iroh.computer/concepts/address-lookup.
- Goose `roam`, which the post names as the next step. It is not confirmed as shipped.
- Buzz repo files, including `VISION_MESH.md`, `crates/`, `docs/`, `NOSTR.md`, and the `Cargo.toml` files. The repo was not cloned.
