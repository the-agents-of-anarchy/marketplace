# Liveness: how projects solve it

Scope: the survey, specimen, verify, and experiment reports under `research/stack/`, grepped for liveness terms and read only at matching sections. No source trees were opened, so every `file:line` below is the report's citation, not a check against code.

Labels on latency: **measured** means a run in e3-kill. **Derived** means arithmetic on stated constants, not run. **Stated** means a report's reading of code, not run.

| Mechanism | Projects using it (report) | Parameters (intervals, timeouts) | Detection latency (measured or stated) | Traffic cost | Evidence |
|---|---|---|---|---|---|
| QUIC connection idle timeout | iroh stack under estafette (f2-gossip, e3-kill); Tunnet pool (p3a-presence-apps); p2panda discovery (p3b-p2panda) | noq default 30 s, not overridden by iroh; tuned to 10 s in e3; p2panda discovery uses a shorter idle value (not stated) | **Measured:** SIGKILL to connection close 30.00 s default, 10.00 s tuned | Timer only, no packets of its own | e3-kill L15, L34-42; f2-gossip L16; p3b-p2panda L45 |
| Transport keep-alive pings | iroh overrides (e3-kill); habilis fork (sp4-habilis-network-internals); iroh-gossip #162 "close idle or stale connections" closed unmerged (verify/v1b-gossip-fixes); habilis override added then reverted in `69ca1c2` (sp5-agent-swarm-beyond-mcp) | noq default none; iroh default 5 s connection and path keep-alive; habilis: one PING per idle path every 5 s | **Measured:** the 5 s keep-alive changed nothing in e3, because iroh already sends it by default. Keep-alive prevents idle close; it is not a detector by itself. | **Stated:** one PING per 5 s per idle path per custom address (sp4 L202) | e3-kill L16-18, L60-62; sp4 L202; sp5 L144, L170; v1b L9 |
| Gossip neighbour event on connection close | iroh-gossip `NeighborDown` (f2-gossip); n0 presence example ignores it (p1-presence-n0); Peersey chat example removes the peer at once (p3a); Tunnet logs it and does not act on it (p3a); p2panda updates its neighbour set (p3b) | No parameter of its own; rides the transport timer. iroh-gossip has no heartbeat or keepalive (f2 L16). Neighbour request timeout 500 ms (e3-kill L26). | **Measured:** NeighborDown 32.99 s median after SIGKILL, default; 13.00 s tuned. About 3.0 s after close, source not found. | None of its own | e3-kill L26, L34, L42; f2-gossip L11-16; p1 L15, L27; p3a L55, L106; p3b L69-71 |
| Clean-stop farewell (gossip Disconnect) | iroh-gossip shutdown sends Disconnect (f2-gossip L16; p3b L69); Tunnet clean stop (p3a L25); habilis `Left` presence (sp1 L65), not traced to peers (sp1 L48) | `Disconnect` with `alive: false` on stop (p3a L25) | **Measured:** NeighborDown 3 ms median on SIGTERM, range 2 to 4 ms, n=5. Fresh connect refused in 3 to 5 ms in 4 of 5 runs. | One message per active neighbour, once, at exit | e3-kill L38-41, L48; p3a L25; f2-gossip L16 |
| Periodic presence beacon with TTL or sweep | habilis `Alive` every 30 s, evicted after 90 s unheard, swept every 10 s (sp1 L67-69; a3 L34); Tunnet signed beacon every 30 s with 90 s expiry (p3a L61, L68); mcpmesh roster heartbeat every 60 s (a2 L104); endo-but-for-bots 30 s datagram heartbeat (s3-breadth L35). smol-kv republish every 300 s is a refresh, not liveness (p1 L17). | habilis: 30 s, 90 s, 10 s sweep. Tunnet: 30 s, 90 s. mcpmesh: 60 s. | **Derived:** habilis evicts 90 to 100 s after last heard. Tunnet shows a crashed peer online for 60 to 90 s (p3a L74). **Not measured in any report.** | **Stated:** habilis and Tunnet send one message per member every 30 s to the whole topic. Receivers track every member. No report measures the cost (sp1 L156). | sp1 L65-69, L156; a3 L34; p3a L61-74; a2 L104; s3 L35; p1 L17 |
| Probe before declaring dead | mcpmesh reach probe and ping ALPN (a2-mcpmesh L43, L147); Tunnet online verdict combines a live connection with an unexpired beacon (p3a L69-70, L97) | mcpmesh reach probe: 3 s constant (a2 L89; `reach.rs:84`). Tunnet pool idle close 120 s, sweeper 10 s (p3a L70). | **Stated:** 3 s probe. Not measured. Tunnet's open-connection check is called "not a probe" (p3a L70) and "closer to a probe" (p3a L97). | One probe per check (not stated) | a2 L43, L89, L147; p3a L69-70, L97 |
| Pull with deadline | habilis reader liveness pulled from each live peer with one shared 500 ms deadline (sp1 L77); habilis task beat, task cancelled after 2 minutes with no beat (sp1 L76) | 500 ms shared reader deadline; 2 minute task cancel | **Stated:** a peer missing the 500 ms deadline shows as unknown, not absent (sp1 L155). | One request per live peer per query | sp1 L76-77, L155; sp3-agent-gossip-frontends L37 |
| Last-seen timestamp only | walkie `last_seen_at` (a1-walkie-alink L85); alink same (a1 L85, L123); p2panda local staleness from a failed connection attempt (p3b L72-74) | None for walkie or alink. p2panda: stale on the first failed attempt, except when the local node is not reachable (p3b L74). | Not a detector. walkie and alink record only when a peer was last seen. | None | a1 L85, L123; p3b L72-74 |
| Caller-side timeouts | irpc has none, so callers wrap every call (d1-irpc L34; verify/v3-irpc L18); d2-direct-apps has no timeouts in any example (L66, L94, L117-118). Spec 3.14 values: connect 5 s, ack 10 s, probe 3 s, observer 3 s, departure 1 s (d1 L34). | Spec values only, not implemented in any source read | Not measured. A stalled server read holds its task or connection until close (verify/v3-irpc L75). | None | d1-irpc L34; d2-direct-apps L66, L117-118; v3-irpc L18, L75 |

## Each mechanism in two or three sentences

**QUIC connection idle timeout.** The transport closes a silent connection after its idle timer, and that close is the only signal the gossip layer gets for a crashed peer. iroh leaves noq's 30 s default in place. The e3 run confirms the close lands at the configured value.

**Transport keep-alive pings.** A keep-alive sends traffic on an idle connection so the idle timer does not fire on a healthy peer. iroh already sends a 5 s keep-alive by default, and habilis adds a 5 s PING per idle path. Aggressive overrides were tried and reverted in at least one project (sp5), and an iroh-gossip fix for idle connections went unmerged (v1b).

**Gossip neighbour event on connection close.** The gossip layer emits NeighborDown when a connection closes, when a Disconnect arrives, or when a random peer is evicted from a full active view. A silent peer is reported only when its connection closes, so the event inherits the idle timer's latency. Applications differ: the n0 example ignores the event, the Peersey example removes the peer at once, and Tunnet logs it without acting.

**Clean-stop farewell.** On an orderly stop, iroh-gossip sends a Disconnect to each neighbour, and the neighbours see NeighborDown within milliseconds. No report shows a farewell after a crash, which cannot send one. Habilis defines a Left presence message, but no report traces whether it reaches peers.

**Periodic presence beacon with TTL or sweep.** A node broadcasts a presence record on a fixed interval, and receivers drop entries not refreshed within a timeout. Habilis, Tunnet, and mcpmesh use this with 30, 30, and 60 second intervals. The brief says "no heartbeats", and three reports contradict it: habilis (a3 L61), mcpmesh (a2 L104), and Tunnet (p3a L104).

**Probe before declaring dead.** A node checks the peer directly before marking it gone. mcpmesh probes with a 3 s constant and keeps a ping protocol, and Tunnet checks for an open connection. The n0 example, p2panda, and the Tunnet presence path do not probe after a neighbour loss.

**Pull with deadline.** A node asks peers for their state and marks the ones that miss a short deadline as unknown. Habilis uses 500 ms for reader state and a 2 minute cancel for stuck tasks. A missed deadline is recorded as unknown rather than gone.

**Last-seen timestamp only.** A node records when it last heard from a peer and makes no active check. walkie and alink store this value and do not announce arrival or departure. p2panda marks a node stale on a failed connection attempt, which is a local observation and not a liveness signal.

**Caller-side timeouts.** Libraries give no timeout, so the application must bound each call. irpc and the d1 and d2 sources set none. The spec's 3.14 values have no implementation in any source read, and a stalled read holds its task until the connection closes.

## What the measurement says (e3-kill)

- **Crash detection in the default iroh stack:** a SIGKILL shows as a connection close at 30.0 s and NeighborDown at 33.0 s, n=5, spread under 25 ms.
- **Clean stop:** NeighborDown arrives in 3 ms, so a graceful exit is far faster than a crash.
- **Keep-alive tuning:** setting 5 s keep-alive changed nothing, because iroh already uses 5 s by default.
- **Idle tuning:** setting max idle to 10 s moved NeighborDown to 13.0 s, n=3. Behaviour below 10 s is unmeasured.
- **Limits:** loopback only, relays disabled, direct addresses only, a debug build, and 13 processes on one machine. A relay path with its 30 s idle could change the timings. This was not tested.
- **Unexplained:** the 15 s path idle timeout did not close the connection before 30 s, and the ~3 s gap before NeighborDown has no source found. The close event was measured on a separate probe connection, so the gossip connection's own close is inferred.

## Not found in the reports

- **Heartbeat in iroh-gossip:** none. A grep of the source found no keep-alive or heartbeat (f2-gossip L16).
- **Probe after NeighborDown:** absent in the n0 example (p1 L72, L78), in p2panda (p3b L71, L78, L91), and in the Tunnet presence path (p3a L55, L106).
- **Rumour or unreachable announcement:** none in any surveyed project (p3b L78, L91).
- **Measured latency for any application-level beacon:** none. Habilis, Tunnet, mcpmesh, and smol-kv are stated or derived only (Tunnet crash latency is marked "not measured" at p3a L74).
- **Measured traffic cost for any heartbeat:** none. habilis' `benches/idle_cost.rs` was not read (sp1 L156).
- **Whether the Lagged event drops a NeighborDown:** possible per f2-gossip L18, not measured.
- **Whether iroh-gossip reconnects on its own after NeighborDown:** not traced (p3b L71).
- **Tunnet sync heartbeat (15 s) and edge ping (20 s):** not presence, not read (p3a L81, L119).
