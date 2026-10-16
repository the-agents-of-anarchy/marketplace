# Departure: how projects solve it

Scope: how a node announces a clean stop, how peers learn of it, and how a node's lifecycle binds to its owner. Sources are the reports under `research/stack/` only. No new projects were opened.

Reading note: "report" names the file under `research/stack/`. Line numbers are the report's own citations, not verified against source.

| Mechanism | Projects (report) | What peers see, and when | Failure mode | Evidence |
|---|---|---|---|---|
| Gossip-layer Disconnect on clean shutdown | peersey chat on iroh-gossip 0.99.0 (p3a); p2panda-net (p3b); iroh-gossip source, quit path (f2) | Direct neighbours get a Disconnect with `alive: false`, then `NeighborDown`. Only direct neighbours see it. | Sent only on clean shutdown. Crash or unclean exit sends nothing. The quitting node emits no event of its own (f2). Does not propagate past direct neighbours (p3b). | p3a:25-26; p3b:69; f2:12-16 |
| Application Left or Leave message | agent-gossip, `Left` presence subtype (sp1:65, :70); walkie, `Leave` frame (a1:22, :26); habilis fork, `Disconnect::left` and `LeavePeers` (sp4:184, :203) | Peers receive an explicit departure and mark the member gone at once. Walkie sends Leave only after the peer stored everything. | Drop without leave runs no leave path in agent-gossip (sp1:154). Walkie drops undelivered messages on leave (a1:53). `LeavePeers` is named in a commit message only, semantics not traced (sp4:184). | sp1:70, :154; a1:26, :53; sp4:184, :203 |
| Drain before leave, bounded or not | walkie (a1:26); spec 3.8 wait, which is our blueprint and not a surveyed project (f2:48) | Walkie holds Leave until the peer acknowledges storage. Blueprint waits at most 1000 ms, then exits. | Walkie states no bound on the wait. Blueprint wait is the only delivery guarantee. Broadcast returns when queued, not when sent (f2:48). | a1:26; f2:48 |
| Presence expiry, no departure message | mcpmesh (a2:52, :123); n0 smol-kv (p1:15, :45); tunnet beacon (p3a:73); habilis Alive sweep (sp1:67-68, :154) | Absence is inferred only when an entry or beacon lapses. Tunnet shows a stopped peer online until its beacon expires. Habilis evicts after a 90 s sweep. | Stop and crash look the same (p3a:105). N0 departed entries keep circulating until the 24 h horizon (p1:44). Tunnet's crash-to-offline window is derived, not measured (p3a:74). | a2:52; p1:45; p3a:73-74, :105; sp1:67-68 |
| Neighbour-down as departure proxy | peersey chat (p3a:23, :55); n0 gossip1 joiner exits on NeighborDown (p1:61) | The receiver removes the peer at once, with no probe. The removal is local. | A topology change looks like a departure (p3a:55). A silent peer is found only when its connection closes (f2:16). | p3a:23, :55; p1:61; f2:16 |
| Drop as stop | p2panda-net, dropping the last handle sends Shutdown (p3b:69); peersey Rendezvous drop cancels tasks only (p3a:26); agent-gossip Node drop aborts loop (sp1:48, :154) | In p2panda, peers get Disconnect and see NeighbourDown. In the other two, peers see nothing from the drop. | Whether a drop counts as a clean stop depends on the library's drop code, not the caller. | p3b:69; p3a:26; sp1:154 |
| Owner death triggers the graceful quit | agent-gossip daemon, `watch_owner` (sp5:45) | When the owner process ends, the daemon broadcasts `left` and exits, same path as SIGTERM. | Pid reuse solved by pid plus start time (sp5:44). Whether the Stop hook persists after skill load is untraced (sp5:148). | sp5:44-48 |
| Transport close code and refusal | iroh 1.3.0 and noq, measured in our spike e3, not a project (e3:38-48) | Clean stop, median values: NeighborDown 3 ms, connection closed with code 0 at 3 ms, fresh dial refused at 3 to 5 ms. | One of five clean-stop dials raced shutdown and failed at the 30 s handshake timeout (e3:48). The report does not say which shutdown call the SIGTERM handler made. Loopback only (e3:67). | e3:24, :38-48, :67 |

## Each mechanism in two or three sentences

**Gossip-layer Disconnect.** The gossip stack sends a Disconnect to each active neighbour on clean shutdown. The neighbour then emits NeighborDown, which is the only departure signal that needs no application code. Its reach is one hop.

**Application Left or Leave.** Agent-gossip, walkie, and the habilis fork each define an explicit departure message. Walkie gates its Leave on the peer's acknowledgement that storage finished. Only the message's presence is confirmed in the reports. Delivery of a Left to all members is not traced in agent-gossip.

**Drain before leave.** Walkie holds the leave until undelivered messages reach the peer, and drops what remains. The blueprint in our own spec uses a 1000 ms bounded wait instead. That wait is untested, and it is the only delivery guarantee the blueprint offers.

**Presence expiry.** Five systems infer absence from a timer. Mcpmesh and n0 use TTLs that lapse. Tunnet and habilis use beacons or Alive pings with a sweep. The cost is latency equal to the TTL, and stop and crash are indistinguishable.

**Neighbour-down as departure.** Two chat applications treat a gossip neighbour loss as a member leaving. This is cheap but wrong whenever the overlay rearranges its links. The reports call this out as a known conflation.

**Drop as stop.** Libraries differ on whether dropping a handle or object runs the shutdown path. P2panda sends Disconnect on drop. Peersey and agent-gossip do not. A caller cannot tell from the call site which applies.

**Owner-death quit.** The agent-gossip daemon treats its owner's death as a SIGTERM. It then broadcasts `left` and exits. This is the only surveyed project that ties a peer's departure to its owner process.

**Transport close code.** At the transport layer, a clean stop closes with a distinct code and refuses new dials. That gives peers a few milliseconds of notice instead of the idle timeout. The only evidence is one spike on loopback, with five default-config runs and no tuned SIGTERM run.

## Lifecycle binding (node dies with its owner)

- **Detached re-exec.** Agent-gossip re-runs itself detached with `setsid` when given `--owner-pid`, then exits 0 (sp5:39, sp1:44). The report quotes the reason: process groups are not enough because Claude Code walks processes by session id.
- **Owner identity.** The owner is pid plus start time, because a reused pid would otherwise look like the same owner (sp5:44).
- **Owner watch.** The daemon polls the owner's start time. A change triggers the graceful quit (sp5:45).
- **Orphan watch.** A daemon with no owner watches its parent pid, and skips the watch when the parent is pid 1 (sp5:46).
- **Signals.** Ctrl-c, SIGTERM, SIGHUP, and SIGQUIT all route through the same graceful path (sp5:47).
- **Session state file.** Written to a temp file and renamed, mode 0600, with pid and owner pid. Peers read it to discover sessions (sp5:53-54).
- **Stale socket.** Removed when no process with the recorded pid exists. The check is existence only, not identity (s1:70).
- **Stop hook.** Four skills run a bell check on turn end. The hook is model-enforced and its persistence is untraced (sp3:49, sp5:148-149). It keeps the session from going deaf. It does not announce departure.
- **Library and MCP sessions.** The loop lives in the host process. Host exit is a silent departure (sp1:48).
- **Walkie daemon.** One daemon per room. The README claims survival of a killed daemon, but the code keeps the outbox and inbox in memory only (a1:60-61). No test kills the daemon (a1:62).
- **Shutdown draining.** Habilis drains relay tasks with `join_next`, so a cancelled task cannot panic shutdown (sp4:166).
- **Relay server.** Iroh-relay exposes `shutdown` and `join`. The report does not say what peers see (f3:40).
- **Stdin trigger.** Our spec wants stdin close to stop the node. Tokio's stdin read cannot be cancelled, so shutdown can hang (s1:58). This is a spec issue, not a project solution.

## Not found in the reports

- **Tombstones.** No surveyed project writes a tombstone for a departed member (a2:52, p1:45).
- **Goodbye in four projects.** Mcpmesh, n0, tunnet, and p2panda send no application-level farewell (a2:52, p1:78, p3a:105, p3b:59).
- **Peer acknowledgement of departure.** No report describes a peer acknowledging a departure message. Walkie's ack covers stored messages, not the leave itself.
- **Clean-stop measurement in a live project.** Only the e3 spike measured clean stop. No live project was timed.
- **Tuned clean stop.** The e3 tuned run covered SIGKILL only (e3:75).
- **Relay or Linux behaviour.** Not measured. The e3 runs were loopback on macOS, without relays (e3:66-68).
- **Walkie kill test.** Not run (a1:63).
- **Buzz departure.** The buzz post describes no departure detection (a2b:24).
- **LeavePeers semantics.** Named in a habilis commit message only. Not traced (sp4:184).
