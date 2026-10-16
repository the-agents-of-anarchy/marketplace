# Late join: how projects solve it

Scope: the survey, specimen, and verify reports under `research/stack/`. Two questions: who a late joiner learns is present, and what it missed. Presence and backfill sit in separate tables. One mechanism can serve both, and merging them hides cost.

## Presence catch-up

| Mechanism | Projects (report) | What the joiner learns | Cost (traffic, state kept) | Evidence |
|---|---|---|---|---|
| Republish whole state on NeighborUp | iroh-smol-kv (p1) | Every entry in the replicated map, including entries of other members | Whole state sent to all neighbors on each NeighborUp, not only the new one. Full republish every 300 s. No digest. | surveys/p1-presence-n0.md:43-44, 77; synthesis/stack.md:111 |
| Announce on each new neighbor | Peersey (p3a) | Names and ids of existing members. Payload is unsigned. | One room broadcast per neighbor event. Name map only. | surveys/p3a-presence-apps.md:17, 20-22, 47, 51 |
| Periodic signed beacon | mcpmesh roster mode (a2); Tunnet (p3a) | Current members within one beat: 60 s (mcpmesh), 30 s (Tunnet). Absence by TTL. | One signed message per member per beat. Entries kept until TTL. | surveys/a2-mcpmesh.md:50, 104, 122-123; surveys/p3a-presence-apps.md:61, 68, 73 |
| Periodic alive keepalive | habilis (a3, sp4) | Which members are alive | Alive every 30 s, timeout 90 s. Alive is not logged, so a joiner sees a member only at its next Alive. | surveys/a3-habilis.md:34; specimen/sp4-habilis-network-internals.md:71 |
| Signed roster with serial | mcpmesh roster mode (a2) | Full org membership. Higher serial supersedes lower. | Roster kept by every node. Re-seeded by accepting nodes. Offline members poll over HTTPS. | surveys/a2-mcpmesh.md:72, 80 |
| Signed records in public DHT slots | iroh-gossip-rendezvous and distributed-topic-tracker (p2) | Node ids publishing on the topic now. Not names, not membership. | One signed record per node per minute. Needs the public Mainline DHT. | surveys/p2-presence-trackers.md:19, 28, 42, 63 |
| Introduction by an already-paired peer | mcpmesh `peer_introduce` (a2) | Identity of the introduced device. Doc says it "installs IDENTITY, not authorization." | One signed endorsement per introduction. Pairwise state. | surveys/a2-mcpmesh.md:71, 158 |
| Invite carries host address | walkie, alink (a1) | Only the host. No network-wide list. | Invite single use, consumed on join. Each side keeps its own peer table. | surveys/a1-walkie-alink.md:31, 83-84, 121 |
| No catch-up beyond direct neighbors | p2panda (p3b); iroh-gossip workshop gossip1 (p1) | Direct neighbors from gossip events. Nothing about absent members. | No state kept. gossip1 broadcasts "welcome" once to the first subscriber. | surveys/p3b-p2panda.md:59, 65; surveys/p1-presence-n0.md:46-49, 62 |

## Each mechanism in two or three sentences

**Republish on NeighborUp.** smol-kv pushes its whole replicated map to every neighbor on each neighbor-up, spread over 10 seconds. It needs no request or digest, so the code stays short. The cost scales with state times neighbors per event, and the report did not measure it.

**Announce on each new neighbor.** Peersey's chat broadcasts its own presence to the room when a new neighbor appears, so existing members announce themselves to the joiner. The receiver trusts the peer and name fields, so any member can announce any id.

**Periodic signed beacon.** mcpmesh and Tunnet sign presence on a timer and expire entries by TTL. A joiner needs no handshake and learns current members at the next beat. The report notes that periodic traffic breaks the spec's no-heartbeat rule, and the report measures no mcpmesh beat cost.

**Alive keepalive.** habilis sends Alive every 30 seconds and treats 90 seconds of silence as gone. Alive is not logged, so a joiner sees members only at their next keepalive.

**Signed roster with serial.** mcpmesh has an offline org root sign a roster with a strictly increasing serial. Nodes distribute it by gossip, blob, and HTTPS poll. A later roster supersedes an earlier one, so a node that missed updates catches up from any newer copy.

**Signed records in DHT slots.** The rendezvous and distributed-topic-tracker projects write signed records to public DHT slots. A newcomer reads them and joins the node ids it finds, and a node that starts alone publishes itself and waits. This answers first contact only, and it depends on a public DHT.

**Peer introduction.** mcpmesh's `peer_introduce` installs a device's identity from a signed endorsement by a peer already paired with it. The doc claims this turns O(N²) pairings into O(N). The report did not test that claim, and authorization still needs its own step.

**Invite-carried address.** walkie and alink put the host's endpoint address in the invite. The joiner dials it, and the host stores the joiner. Each side keeps its own peer list, so a joiner learns only the host.

**No catch-up.** p2panda announces nothing on join, and a new node learns neighbors through its walker and the gossip join. gossip1 greets the first subscriber once, and later joiners get nothing. Both leave late joiners blind to members who are not direct neighbors.

**Caveat on the pinned gossip version.** The verify report quotes a PR body saying a 0.101.0 node may lose joins from new nodes. The fixes, iroh-gossip #178 and #189, are merged on main and unreleased (verify/v1b-gossip-fixes.md:10-11, 19).

## Presence catch-up vs content backfill (kept apart)

Presence answers who is here now. Backfill answers what was said or changed while the joiner was away. One mechanism can do both. smol-kv's republish carries application entries, so it is also backfill (surveys/p1-presence-n0.md:43-44). The table below lists backfill only.

| Mechanism | Projects (report) | What the joiner gets | Cost (traffic, state kept) | Evidence |
|---|---|---|---|---|
| Chat digest and resend by answerers | habilis (sp4, sp2, a3) | Chat missed while away, bounded by each answerer's 1000-entry log | Digest every 10 s per member. Up to 3 answerers, each resends up to 64 per digest. Directed messages go only to the addressee. | specimen/sp4-habilis-network-internals.md:75-79, 94, 200; specimen/sp2-agent-gossip-messaging.md:82 |
| State heads and change set | habilis (sp4) | Automerge changes since the asker's heads | Rounds of at most 8 answers of 64 frames per asker per 5 s. Bounded by document size. | specimen/sp4-habilis-network-internals.md:81, 94 |
| Event ring replay with cursor | agent-swarm MCP (a1b) | Events past the cursor from the local event ring. Cursor 0 returns about 200. | Ring bounded by size. Cursor kept per session. `missed_before` flags an aged-out cursor. | surveys/a1b-agent-swarm-mcp.md:76-81 |
| Append-only log catch-up | p2panda sync feature (p3b) | Messages missed while offline | Needs a log store. Not wired into presence. | surveys/p3b-p2panda.md:92, 99 |
| Central workspace history | Buzz (a2b) | Unresolved. The relay holds "workspace history," and the post does not say whether it includes messages. | A central holder of state. | surveys/a2b-buzz.md:25, 29, 31 |

**Digest and resend.** Each habilis member broadcasts a chat digest every 10 seconds. Up to three members answer, and each member picks answerers from its own roster view, so two members may disagree. The log keeps 1000 entries per member with no time bound, so a long absence can outlast every holder's log and the gap is lost.

**State backfill.** The state digest carries automerge heads, and the answer is the change set since the asker's heads. The answer ends with the answerer's own heads, so a node still behind asks again.

**Event ring replay.** agent-swarm's MCP cursor starts at 0 and returns the local event ring. The report describes this as a local replay, not a fetch from peers. Its cursor is independent of the daemon's cursor.

**Limits of backfill.** A directed message is backfilled only while the recipient's endpoint is known; otherwise the resend is dropped (sp2:82). A group above 16 shards is never logged, so it is not backfilled (sp2:84, 142). The habilis backfill tests were read from their headers, not run (surveys/a3-habilis.md:51).

## Not found in the reports

- **Introduce-only presence on join.** The synthesis says no project implements it (synthesis/stack.md:130).
- **Measured cost of any republish, digest, or beacon round.** Each report names its cost as unmeasured (surveys/p1-presence-n0.md:53; specimen/sp4-habilis-network-internals.md:94, 200).
- **Running proof of late-join order.** NeighborUp order on reconnect was not verified by running (surveys/p1-presence-n0.md:84).
- **Late-join latency measurement.** The beacon rows give bounds from beat intervals, not measurements.
- **How habilis fills a joiner's roster.** The roster is a nickname set (specimen/sp4-habilis-network-internals.md:104), and the fill path from logged join events was not traced.
- **Tunnet membership sync.** Membership is an iroh-docs document (surveys/p3a-presence-apps.md:61), and its membership and sync code were not read.
- **Chio catch-up file.** `catchup.rs` appears in the unread list of surveys/i2-admission.md.
- **Indexed sync projects.** iroh-docs, subduction, and gantz_collab_sync are indexed (index/index.md:158, 280, 295), but no survey reads them for late join.
