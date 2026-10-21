# Ledger: the spec against technological reality

Author: claude-fable-5-1 (orchestrator), 2026-10-16. Replaces the dropped stack synthesis. Every row cites a report I read in full: experiments/e1-api.md, e2-size.md, e3-kill.md, verify/v3-irpc.md, v1a-iroh-fixes.md, v1b-gossip-fixes.md. Everything else in research/stack/ is a lead.
Goal (owner): "test our theoretical spec against technological reality and revise anything that needs it."
Classes: RUN = observed by running code (one host, macOS arm64, loopback or LAN, small n). RECORD = primary record (source at a release, git ancestry, PR state). RULED = owner ruling. OPEN = untested.

## Surface map (the original surface, by range)
Marks: ■ settled by a run or a record · ▣ ruled by the owner · ◆ solid lead (a worker's claim later confirmed by our run or the orchestrator's check, or a sonnet source read whose project tests were run) · ◇ unconfirmed lead · ○ open · ▶ in flight. Update this map whenever a row changes.

```
ORIGINAL SURFACE: which ranges are solved, at what cost, what we copy, what we write
│
├─ TRANSPORT ─────────────── iroh 1.3.0 ────────────────────────────── mostly settled
│   ├─ ■ direct, relay-only, relay→LAN upgrade, remote id = dialer key   e1 2,4,9e,9f
│   ├─ ■ one key type for card and node, strict verify                   e1 1
│   ├─ ■ one router, our ALPN + gossip ALPN                              e1 3
│   ├─ ■ dial needs an address: mDNS or relay URL in the address         e1 9
│   ├─ ◆ mDNS is a separate crate (iroh-mdns-address-lookup)             f1b ← e1 5
│   ├─ ◇ N0 preset = pkarr publish + DNS lookup                          f1a
│   ├─ ◇ endpoint tickets carry no name or secret                        f1b
│   ├─ ■ iroh-gossip installs its own address lookup, but it learns only  e6, e8
│   │      gossip NEIGHBORS: 3 adjacent nodes dial by id in ~14 ms (e6); in a
│   │      5-node mesh members were undialable by id (e8) until Presence
│   │      carried the address and receivers added it to their lookup
│   ├─ ■ restart on a new port: ~1 s via gossip lookup or mDNS            e6
│   ├─ ■ n0 preset (pkarr): first dial ~3.7 s; records public; relay-off  e6
│   │      variant publishes nothing dialable by default
│   ├─ ■ relays never forward across relays: a dialer needs the peer's    e6
│   │      own home relay URL; home relay is not chosen by map order
│   ├─ ■ mDNS: ~0.8 s first, ~1 s restart, +10 crates                     e6
│   ├─ ■ self-hosted iroh-dns-server works: 289-crate binary, domain +    e6
│   │      NS delegation + DB; DNS-only lookups stale ~26 s
│   ├─ ■ relay death: home status false in 2 ms; re-home to the live     e8
│   │      relay takes ~40 s; peers keep the dead relay URL; dials to the
│   │      member recover only if the relay returns
│   ├─ ■ relay death (not bootstrap death) stalls gossip mesh-wide, in    e8, e10
│   │      0.101.0 and main alike (control 0/6); 0.101.0 never heals in
│   │      180 s; main rejoins alone and heals at 62-145 s (#191);
│   │      stall and ~41 s re-home reproduced on Linux       linux-e10
│   ├─ ■ re-home ~40 s is two periodic re-stun intervals; removing the     e10
│   │      dead relay forces a full report (code read, unrun)
│   ├─ ■ bootstrap failover cheap: one of two dead, join in 8-18 ms        e8
│   └─ ○ NAT; two hosts; own rejoin plus remove_relay on 0.101.0 (C13)
│
├─ GOSSIP ────────────────── iroh-gossip 0.101.0 ───────────────────── partly settled
│   ├─ ■ worst Presence 4368 B, overhead 38, minimum 4407, default 4096 e2
│   ├─ ■ oversize: Ok returned, message lost, link dead                  e1 8b, e2
│   ├─ ■ crash → NeighborDown 33 s default, 13 s at 10 s idle            e3
│   ├─ ■ clean stop → NeighborDown 3 ms                                  e3
│   ├─ ■ churn-leak fixes merged, unreleased                             v1b
│   ├─ ▣ lower the public cap · idle timeout 10 s · pin 0.101.0
│   ├─ ◆ max_message_size has a builder setter                           f2 ← e1 8
│   ├─ ◇ author hidden (delivered_from = previous hop); dedup 90 s       f2
│   ├─ ■ topic id alone admits an outsider: joins in ~6 ms, reads every  e7
│   │      Presence; forged payloads are dropped on MAC but forwarded first
│   ├─ ■ secret-proof gate works: keyed challenge both ways in iroh's     e9
│   │      after_handshake hook; outsider gets 0 neighbors, 0 payloads,
│   │      0 forgeries forwarded; ~1-2 ms per connection; ~60 lines, no crate
│   ├─ ■ an accept-loop-only gate cannot prove gossip's own outgoing      e9
│   │      dials (gossip dials internally); a lying acceptor read Presence
│   ├─ ■ Presence sent before gossip neighbors exist is lost; tables      e4
│   │      never fill (3/3); sent after the topic forms: all five in ~3 s
│   ├─ ■ Departure: broadcast only enqueues; exit at once reached 0-2 of  e4
│   │      4 peers; 1000 ms sleep before exit reached 4/4 (3/3)
│   ├─ ■ crash: NeighborDown ~15 s + probe 3 s → every peer Unreachable  e4
│   │      at ~18 s; no live member falsely marked (D20 holds)
│   ├─ ■ false rumor corrected within ~5 ms of reaching its subject       e4
│   ├─ ■ S12 holds: replay never revives a departed member; tombstone and e4
│   │      max age both needed (each covers one case)
│   ├─ ■ Introduce costs about N² requests per full join                 e4
│   └─ ○ S13 address-change trigger unexercised
│
├─ DIRECT PROTOCOL ───────── hand-written on iroh streams ──────────── settled
│   ├─ ■ read_to_end(1,114,112) caps, resets only the stream             v3
│   ├─ ■ irpc rejected: fixed 16 MiB, pre-allocates, +4 crates           v3
│   ├─ ◆ echo example = smallest accept-read-respond                     d2 ← v3
│   └─ ■ gap: no server read timeout in 3.14                             v3
│
├─ INFRASTRUCTURE ────────── iroh-relay `server` ───────────────────── half settled
│   ├─ ■ in-process relay over plain HTTP; http_url needs test-utils     e1 7
│   ├─ ◆ test-utils leaks insecure TLS if not dev-only                   f3, r1 ← e1 7
│   ├─ ▣ relay behind a cargo feature
│   └─ ○ bootstrap member; relay TLS ruling; n0 relay compatibility
│
├─ CRYPTO ────────────────── iroh keys, blake3 (in tree) ───────────── mostly settled
│   ├─ ■ sign / verify                                                   e1 1
│   ├─ ▣ hex everywhere · no presence encryption
│   └─ ○ derive_key, keyed MAC, constant-time compare (trivial)
│
├─ WIRE ENCODING ─────────── postcard (in tree) ────────────────────── settled
│   └─ ■ sizes of every structure                                        e2
│
├─ IDENTITY ─────────────────────────────────────────────────────────── reopened
│   ├─ ■ address cache never evicts → fresh keys leak                    v1a
│   ├─ ▣ node-as-identity propagated; sidecar lock for one holder
│   ├─ ◇ no surveyed project detects a second live holder at runtime     so4
│   ├─ ■ flock freed on SIGKILL in 6.5-10.4 ms; restarted node takes it   e5
│   │      first try 15/15; second holder gets WouldBlock; std try_lock,
│   │      no crate (macOS; Linux open)
│   ├─ ■ same-key restart, same address: gossip seamless, 0 NeighborDown/ e5
│   │      Up at peers in 30 runs; new instance heard in 0.2-1.0 s
│   ├─ ■ held connection to a killed node hangs silently until the idle   e5
│   │      timeout (10 s), then connection_lost: app timeouts must be < 10 s
│   ├─ ■ restart on a NEW address: dial by id with the old address fails   e5
│   │      85/85 for 22 s though gossip meshes: addresses must be refreshed
│   ├─ ■ two live holders: silent starvation of one (direct); relay's     e5
│   │      newest wins, the old loses gossip for good: the lock is essential
│   ├─ ◆ precedent for N: mcpmesh key file + exclusive lock in one root,  state/m4
│   │      order lock → key → bind (hooks unarmed) → arm → serve
│   ├─ ◆ never unlink the lock file; kernel is the only releaser          state/m4
│   ├─ ◆ key mint: 0600 temp, fsync, hard_link (no overwrite, race-safe)  state/m4
│   └─ ○ Linux lock semantics; power loss (no FIN to the relay)
│
├─ FILES AND LOCAL ───────── small pieces ──────────────────────────── mostly leads
│   ├─ ■ serde YAML crates rest on unsafe-libyaml (RUSTSEC-2024-0449)    orchestrator check
│   ├─ ▣ yaml-rust2 + own converter
│   ├─ ◆ swarm-discovery fix in 0.6.4, resolved by a fresh lock          v1b ← e1 10
│   ├─ ◇ base32/hex in data-encoding; uuid v7 a feature; libc in tree    s1
│   ├─ ◇ dirs breaks spec 3.3 on macOS → hand XDG                        s1
│   └─ ◇ tokio stdin read uncancellable; `signal` adds two crates        s1
│
├─ MCP ───────────────────── rmcp 3.5.1 (ruled), hand-written handler ─────── run
│   ├─ ■ static six tools, envelope with `you`, bad_request, 3.10 text   e11
│   ├─ ■ SIGTERM hangs on a pending stdin read; shutdown_background      e11,
│   │      exits in 1 ms idle; same on Linux, every check and timing    linux-e11
│   └─ ○ Departure late by rmcp's drain: 5 s after stdin closes          C14
│
├─ CLI ───────────────────── clap (ruled) ──────────────────────────── nothing to test
│
├─ STATE ─────────────────── mechanics mostly settled; structs and algorithms ours
│   ├─ ◆ roster ordering: per-origin seq = max(now_ms, last+1); accept   state/m1
│   │      only if signed, within max age, above held and above tombstone;
│   │      tombstone on gone (habilis link vectors, 9 tests run)
│   ├─ ◆ every side map bounded to live + returnable set; FIFO caps on    state/m1
│   │      anything a stranger can grow (habilis, flap-churn test run)
│   ├─ ◆ transport truth overrides gossip presence in status (Tunnet)     state/m1
│   ├─ ◇ periodic keepalive 30 s / timeout 90 s in habilis and Tunnet;    state/m1
│   │      estafette relies on the QUIC idle timeout instead (e3)
│   ├─ ◆ names: receiver-local name per key, first-come `-2` suffix      state/m2
│   │      (alink, test run) = D5 as written; persisted there, ours not
│   ├─ ◆ names never authorize; resolve to the key and keep it (mcpmesh  state/m2
│   │      #38 grant desync; agent-gossip's name-keyed roster gap)
│   ├─ ◇ validate inbound handles on the wire, not only local input      state/m2
│   ├─ ◆ dedup: bounded FIFO set sized to the retry horizon; key bound   state/m3
│   │      to the sender, checked after verification (agent-gossip)
│   ├─ ◆ inbox: ring with monotonic seq; leading gap marker when a       state/m3
│   │      reader's position was evicted (agent-gossip)
│   ├─ ◆ per-client `since` is the stateless side-read model; no         state/m3
│   │      server cursor needed (agent-gossip, iroh-gossip)
│   └─ ◇ open in spec: slow-client lag, inbox-full refuse vs drop,       state/m3
│          flood fairness in eviction
│
├─ TREE COST ───────────────────────────────────────────────────────── partial
│   ├─ ■ 314 unique deps without rmcp and clap                           e1 10
│   └─ ■ draft manifest 280 unique deps; 321 with the relay server       e11
│
├─ PRIOR ART (the deep row) ──────────────────────────────────────── leads only
│   ├─ ◇ every agent-messaging project keeps a mailbox                   a1, a3, sp2
│   ├─ ◇ habilis: push delivery tried 2 weeks, removed; 6 → 19 tools     sp3
│   └─ ◇ lineage of the habilis family                                   specimen (unread)
│
└─ TEST HARNESS ──────────────────────────────────────────────────── deferred (ruled)
    └─ ◇ n0's patchbay simulates networks; gossip simulator has no sockets   s2
```

## Spec assumptions, by status

| # | Spec | Assumption | Status | Evidence |
|---|---|---|---|---|
| 1 | D2, 3.1 | One Ed25519 key type serves card and node; sign and verify available | RUN holds; verify is strict | e1 check 1 |
| 2 | 3.6 step 4 | The remote id of an accepted connection is the dialer's key | RUN holds (ids compared; forgery not attempted) | e1 check 4 |
| 3 | D11 | iroh connects two keys directly and via a relay | RUN holds on one host: direct (e1 2a), relay-only (e1 2b, 9f), relay then upgrade to LAN (e1 9e). NAT and two machines OPEN | e1 |
| 4 | D14, D43, 3.14 | A relay can run inside our process | RUN holds over plain HTTP; `http_url()` needs `test-utils`, build the URL by hand | e1 7a, 7b |
| 5 | D15 | Local discovery finds peers with no configuration | RUN holds, via the separate crate iroh-mdns-address-lookup; needs a multicast-capable LAN interface | e1 5a-5c, 9c, 9d |
| 6 | D12, 3.6 | One router serves the gossip protocol and ours | RUN holds | e1 3 |
| 7 | 3.10 step 3 | A node can dial a peer from its node id | RUN: fails with no address lookup configured (e1 9a, 9b, Minimal preset by choice); works with mDNS (9c, 9d) or with the relay URL in the address (9e, 9f). Dial by id through n0's or a self-hosted lookup OPEN | e1 9 |
| 8 | 3.7, 3.14 | A Presence fits a gossip frame | CONTRADICTED. Worst-case Presence 4368 bytes; gossip adds 38; minimum `max_message_size` 4407; default 4096 | e2 |
| 9 | 3.7 | An oversize gossip send fails visibly | CONTRADICTED. `broadcast` returns Ok, message lost, and the link then carries nothing more | e1 8b, 8c; e2 follow-up probe |
| 10 | — | Fix for 8 and 9 | RULED: lower the `public` cap so the default frame carries the largest Presence; exact cap after the Presence shape settles | owner 13:02 |
| 11 | D18, D20, 3.8 | A crashed peer is noticed without heartbeats | RUN holds, at a cost: NeighborDown 33 s after SIGKILL by default (QUIC idle timeout 30 s + ~3 s unexplained), 13 s with a 10 s idle timeout | e3 |
| 12 | — | Idle timeout value | RULED: 10 s | owner 12:40 |
| 13 | D19 | A clean stop is seen at once | RUN holds for gossip's own disconnect: NeighborDown 3 ms. Our Departure payload and the 1000 ms wait OPEN | e3 |
| 14 | 3.8 | The endpoint reports relay reconnects and network changes | RUN partly: `home_relay_status` reports relay loss and reconnect (6.3 s after restart); `watch_addr` stays silent on relay loss. A "network change" output event: none found (lead) | e1 6 |
| 15 | 3.6, 3.14 | A direct request can be capped at 1,114,112 bytes, bad requests closing only their stream | RUN holds by hand: `read_to_end(limit)` rejects 2 MB, largest allocation 40,960 B, stream reset, connection alive | v3 |
| 16 | — | irpc as the direct protocol | RUN rejected: fixed 16 MiB cap, allocates the declared size before the body, closes the connection on a bad frame, hides the remote id, +4 crates; 47 vs 39 lines | v3 |
| 17 | 3.14 | The limits table covers every wait | CONTRADICTED: no server-side read timeout; a stalled stream holds a task until the connection dies | v3 |
| 18 | 3.14 | 5 s connect timeout bounds a dial to a dead peer | RUN: a dial to a dead peer fails only at the idle timeout (30 s default, 10 s tuned); the spec's 5 s wrapper is what bounds it | e3 |
| 19 | D3 | A fresh node key per session costs nothing | CONTRADICTED by RECORD: iroh 1.3.0's address cache never evicts (fix PR closed unmerged); every session is a new remote | v1a |
| 20 | D3 | Churn of ids is safe in iroh-gossip 0.101.0 | RECORD: churn-leak fixes merged after 0.101.0, unreleased; per #178 a 0.101.0 node may lose joins from newer nodes | v1b |
| 21 | — | D3 itself | RULED: reopened; node-as-identity propagated (docs/orchestration_log/history/2026-10-16-node-as-identity.md), sidecar lock replaces D6 tie-break, untested | owner 12:50 |
| 22 | — | swarm-discovery retry-loop fix | RECORD: in 0.6.4; e1's fresh lock resolved 0.6.4 | v1b, e1 10 |
| 23 | 3.1 | Text forms | RULED: hex everywhere | owner 12:45 |
| 24 | 3.5 | YAML card parsing | RULED: yaml-rust2 plus our own converter (serde YAML crates rest on unsafe-libyaml, RUSTSEC-2024-0449; checked by me) | owner 12:45 |
| 25 | D14 | Relay ships in every build | RULED: behind a cargo feature | owner 12:40 |
| 26 | — | Presence encryption | RULED: none | owner 12:50 |
| 27 | — | iroh-gossip pin | RULED: release 0.101.0, upgrade later | owner 12:45 |
| 28 | — | Tree cost | RUN: e1's package (iroh, iroh-gossip, iroh-relay server, mDNS, tokio) 314 unique dependencies; rmcp and clap not included. RUN (resolution only): the full draft manifest, rmcp with default features off, 280 unique name+version; 321 with the iroh-relay server | e1 10, e11 |

## OPEN, ordered by how much of the spec rests on it
1. Node as identity: sidecar lock released on crash (macOS, Linux); a restarted node reusing its id while peers hold a stale connection; which instance answers a dial in that window. Gates D2-D7, D10, D30, 3.4, 3.6, 3.8, 3.9.
2. Address lookup: dial by id with n0's preset (pkarr), with a self-hosted lookup, and with addresses carried in Presence; several relays in one map and how a peer homed elsewhere is reached. Gates 3.3 config, 3.10 step 3, D14, relay TLS.
3. Presence flow: join, Introduce to a late joiner, Departure delivery within 1000 ms, probe after NeighborDown, Unreachable rumor and self-correction (D18-D20, 3.8, tests 4, 5, 8, 19, 20).
4. Gossip admission: does an outsider holding only the topic id and a bootstrap address receive Presence (lead: verify/v2-gossip-gate.md, a source trace).
5. rmcp: answered by e11 (static list, envelope, stdin close in 1 ms when idle, the SIGTERM hang and its fix); open: the Departure delay under rmcp's drain (C14).
6. Two machines: NAT, relay-only across hosts (test 3).

## Leads (hypotheses, not findings)
surveys/*.md, specimen/*.md, solutions/*.md, verify/v2-gossip-gate.md, ground/*.md, index/index.md. Known errors in them are listed in plan.md under "Orchestrator corrections". Use them to choose experiments; never cite them as findings.

## Collisions awaiting a ruling
| # | Spec | Collision | Evidence | Options |
|---|---|---|---|---|
| C1 | 3.10 step 3, 3.3 | RULED again → S20 revised | | |
| C2 | 3.14 | RULED → S10 | | |
| C3 | 3.11 | RULED → S18 | | |
| C4 | D25 | RULED → S11 | | |
| C5 | 3.4, 3.8 | RULED → S12 | | |
| C6 | 3.8 | RULED → S13 | | |
| C7 | D14 | RULED → S21 (n0 fallback not chosen; confirm) | e6, e8 | |
| C8 | D3-D7 | RULED → S14 | | |
| C9 | 3.8 init row, D18 | RULED → S15 | | |
| C10 | D19, 3.8 stop row | RULED → S17 | | |
| C11 | 3.10, 3.14 | RULED → S19 | | |
| C12 | D13, D17, 3.7 | RULED → S16 (mechanism measured in e9; confirmation pending) | | |
| C13 | D11, D14, S7 | RULED → S24 (own fix on the 0.101.0 pin; measure first); the stall and re-home hold on Linux | e8, e10, lab/linux/linux-e10 | |
| C14 | 3.9, S17, test 4 | RULED → S25 (own stdin reader measured: departure at once, exit unchanged) | e11, e13, lab/linux/linux-e11 | |
| C15 | 3.10, D30 | RULED → S23 | e11 | |
| C16 | D14, D20, 3.8, S21, S24 | RULED → workaround in estafette (design and measurement next); an internal bug report with a minimal reproduction (E14 follow-up). after a relay host dies, all outgoing relay traffic of an endpoint stalls: iroh 1.3.0's single RelayActor awaits the dead relay's full 64-slot queue (actor.rs:1136-1137, 1207-1233, 1359), and the dead relay's actor never drains it while it backs off (sleep_backoff reads only the priority inbox, actor.rs:366-389); recovery only when that actor exits after 60 s idle (actor.rs:68); any traffic toward the dead relay restarts it. Same code on iroh main today. remove_relay and lookup removal do not clear it; not sending toward the dead relay before its queue fills prevents it Linux agrees at 180 s (lab/linux/linux-e14w, n=3+1 per cell): dead-relay actor exits at 61-80 s, each pair's first fresh dial ok 0.1-2.4 s after the later member's exit; but gossip heartbeats resume in 0/16 stalled pairs within 180 s, as on macOS: clearing the block does not by itself heal gossip, so the workaround must pair with S24's rejoin. The earlier Linux 60 s note was a window effect (retracted by lab-sibling). Bug report written (experiments/e14-bug-report.md, spike/e14-bug-report 983118f): single-file repro e14-repro, 20/20 FAIL on 1.3.0 and on iroh main 55908a5 (1.4.0, actor.rs byte-identical), controls pass; trigger is a count (about 65+ datagrams toward the dead relay), not a rate; queue 64/64 and RelayActor blocked observed through a diagnostic patch; candidate upstream fixes drain-in-backoff and drop-on-full both 20/20 PASS. Reproduced here 2026-10-21 (1 FAIL, 1 no-kill PASS); source lines rechecked. Member-side workaround measured: close and rebind the endpoint with the same key, X-Y ok 7.4 s after the burst, 3/3. Linux agrees on the E14 two-process repro (lab/linux/linux-e14, raw SUMMARY lines checked): p1 onset 18.0 s 3/3, no recovery in 90 s; p5 4.0 s; ctl and p1s5 clean; p1s25 recovers at 76.1 and 87.1 s (macOS 73.7 s). Linux, single-file repro (lab/linux/linux-e14-repro, raw counts checked): stock 19/20 FAIL, main 18/20 FAIL, controls pass, drain and drop 20/20 PASS; 6/48 burst runs never stalled (queue not filled), so on this VM the trigger is a race near 200, not certain; rebind recovered at 5.4 s (2 runs). E15 (experiments/e15-workaround, spike/e15-workaround 37b0a1a, macOS, gossip harness scenario 1): W1 rebind (close endpoint, bind fresh with same key, new Gossip, re-subscribe via bootstrap, on 3 s heartbeat silence, debounce 20 s) heals 76/76 stalled pairs by 180 s against 0/24 (none) and 2/24 (L1+L2); 7/13 runs fully healed by 31 s, 5/13 relapse and heal on a second rebind at 91-170 s (cause open); 0 false rebinds (3 no-kill runs); transport fixed (drain diagnostic) never stalls, 0/6. Linux agrees on E15 (lab/linux/linux-e15, n=3 per arm, Linux-only table checked): W1 heals 18/18 (T=3 s), 18/18 (T=10 s), 12/12 (W1+L1); none 0/12, L1+L2 0/18; first rebind 6.9-14.0 s, heartbeat a median 4.2 s after; relapse 1/8 stalled W1 runs; 0 rebinds without a kill; drain-fixed transport 0/6 stalled. Staged as S26. | e14 (source lines checked; main checked 2026-10-20) | (a) report upstream to n0 with E14's reproduction; (b) carry a patched iroh (the backoff drains or drops queued datagrams); (c) a member-side workaround: stop all traffic toward peers homed on a relay seen dead (gossip's own dials and open connections included), unmeasured; owner decides |
| C17 | D14, 3.8, S24 | iroh-gossip 0.101.0 never re-dials a peer whose dial failed while it was not active: net.rs:436-443 sends only PeerDisconnected; the Pending entry stays with its queue; net.rs:695-699 dials only on an empty queue; the entry is removed only on DisconnectPeer (net.rs:732-736), which hyparview emits for active peers only (proto/hyparview.rs:346-354, 648-655); so after the transport recovers (fresh dials ok at 72-161 s) heartbeats resume in 2/48 stalled pairs and L2's join_peers starts no dial (trace: 13 JoinPeers, last dial start at 31-44 s). Source lines checked 2026-10-21 E16 (experiments/e16-redial, spike/e16-redial c86fdbf, macOS): the one-place fix (drop the Pending entry on a failed dial) heals nothing: without levers the path is never reached (no sends after the kill; trace: 0 dials), with L2 it re-dials every 4-5 s and keeps the C16 block alive (0/30 prober pairs recover, against 10/18 with L2 and no fix); with W1 it heals as W1 alone (30/30, 2/5 relapse). Upstream iroh-gossip main already fixes the path (PR #178, f02f79e8, merged 2026-10-14; handle_in_event_inner drops the entry on every PeerDisconnected, net.rs:779-783 at c5f44db, checked 2026-10-21), unreleased after v0.101.0. | e15 (source reading plus 2 traced runs; Pending state not instrumented) | under C13's ruling; measured: do not carry the E16 fix (it feeds C16 under L2); the path goes away with the next iroh-gossip release (PR #178) |
| C18 | D14, 3.8, S21, S26 | after a rebind (S26) a member's Join to a bootstrap node can go unanswered: the node holds a stale pending Neighbor request to that id (a ForwardJoin renewal sent a second Neighbor before the kill, which the member took as the reply to its own: hyparview.rs:403-409, 450-452) and send_neighbor sends nothing for a pending peer (745-752); the dead old connection's idle close does not clear it while the new connection exists (net.rs:575-588, 790-799). 15/15 Joins in that state unanswered, 0/66 others; waits 57-60 s, ended by the harness's 60 s join timeout (6/7) or a shuffle (1/7). Source lines checked 2026-10-21. Fixed on iroh-gossip main by PR #161 (fcd81ae8, 2026-10-09: on_join drops the pending request; checked at c5f44db hyparview.rs:549-558), unreleased | e18 (experiments/e18-attach, spike/e18-attach 85ef8a2, macOS, n=8 per arm, vendored gossip logging) Linux agrees (lab/linux/linux-e18, n=8 per arm interleaved, table checked): late joins 6/24 (57.0-60.0 s), join timeout 8/24 at exactly 5.0 s, on_join fix 0/24; all flowing from median 75.5, 30.6, 27.1 s; one B2 trace shows the same active+pending state and no Neighbor; 0 rebinds in 4 no-kill runs. | measured (all with the fresh-lookup variant): member-side join timeout 5 s then rebind: wait 60 s to 5 s, all pairs flowing median 78.7 s to 38.0 s (p=0.005), 0 false rebinds in 3 no-kill runs; the one-line on_join backport (bootstrap nodes only in effect): 0 late joins, median 31.5 s (p=0.0005). The backport falls under C13's ruling (own fix on the 0.101.0 pin) |

## Staged revisions (ruled, not applied)
| # | Ruling | Spec sections | Kind |
|---|---|---|---|
| S1 | public card fields stay in Presence (and in Introduce), capped at 3072 bytes so the largest Presence fits the default 4096-byte gossip frame with headroom (owner ruling) | 3.5, 3.7, 3.14 | spec edit |
| S2 | QUIC idle timeout 10 s | 3.14, D18-D20 | spec edit |
| S3 | relay behind a cargo feature | D14, D35, 3.2 | spec edit + stack D-record |
| S4 | cards parsed with yaml-rust2 plus our own converter | 3.5 | stack D-record |
| S5 | hex for every text form | 3.1, 3.3, 3.13 | spec edit |
| S6 | no presence encryption | 1.6, D13 | spec edit (record the reason) |
| S7 | iroh-gossip pinned to 0.101.0, upgrade when the churn fixes ship | D11 | stack D-record |
| S8 | direct protocol written by hand; irpc rejected | 3.6 | stack D-record |
| S9 | sender checks gossip payload size before broadcast | 3.7, 3.16 | spec edit (follows from E1/E2; confirm with S1) |
| S10 | one stream per request on a cached connection; server read timeout 10 s resets only the stalled stream | 3.6, 3.10, 3.14 | spec edit |
| S11 | drop duplicate suppression: D25 and the 10,000-id set removed; the binary never retries a send | D25, 3.6 step 7, 3.14, test 17 | spec edit |
| S12 | per-member announcement seq = max(now_ms, last+1); keep the highest; ignore older than a max age of 300 s (owner ruling); tombstone a departed member's last seq for the max age | 3.4, 3.7, 3.8, 3.14, test 20 | spec edit |
| S13 | re-announce presence on relay status change and on address change | 3.8 | spec edit |
| S14 | node as identity: the card key is the iroh endpoint key; one live holder per card by an exclusive lock on the card's key file, taken before the endpoint is built; Claim struct, tie-break, Displaced state retired; gossip payloads keep a signature by the card key | D2-D7, D10, D17, D30, D32, 3.4, 3.6, 3.7, 3.8, 3.9, 3.10, 3.15 tests 6, 18, 20, 3.16 | spec edit (largest) |
| S15 | first Presence only after iroh-gossip reports the topic joined | 3.8 init row, D18 | spec edit |
| S17 | stop: broadcast Departure, release the card lock at once, wait a fixed 5 s, exit | D19, 3.8 stop row, 3.9, 3.14 | spec edit |
| S18 | inbox stays a ring of the last 1000 messages; the sender's ack means delivered into the inbox, never read; no gap marker, no read tracking; gaps, limits, and what fits a context are the bridge's business | D21, D22, 3.11, 3.12 | spec edit |
| S19 | no transport-level retries anywhere; a failed send returns its error as is (timeout, unreachable, refused), and the held connection is dropped on failure | 3.10, 3.14, 3.16 | spec edit |
| S20 | address lookup: every Presence and Introduce carries the sender's full current endpoint address (id, relay URL, direct addresses); a receiver replaces that member's entry in its lookup (replace, never merge); gossip's built-in lookup alone is not relied on (it learns only direct neighbors, e8); bootstrap addresses ride in the invitation; no pkarr, no DNS; mDNS deferred (D15 moves to Deferred) | D15, 3.3, 3.7, 3.8, 3.10, 3.13, 2.12 | spec edit |
| S21 | infrastructure: several machines the owner runs, each one relay plus one bootstrap node; each joins the topic through the secret gate and broadcasts a signed infrastructure record (relay URL, bootstrap address); members add the relay at runtime (iroh 1.3 Endpoint::insert_relay) and save the learned hosts into the machine's network config for later sessions; an invitation needs one reachable host; no restart or config edit on members when a host is added | D14, D43, 3.3, 3.7, 3.13, 3.14 | spec edit + experiment (self-announcing hosts) |
| S22 | unfixed parameters, agreement ones only: groups G1 wire, G2 files and names, G3 local contracts, G4 formats between machines approved as drafted in research/stack/parameters.md (22 values); six choices named in the spec as the implementer's call | 3.1, 3.3, 3.5, 3.6, 3.7, 3.8, 3.9, 3.10, 3.11, 3.13 | spec edit |
| S23 | MCP surface values G5 (23-29) approved as drafted in research/stack/parameters.md | 3.10, D30 | spec edit |
| S24 | gossip stall on relay death: keep iroh-gossip 0.101.0; a member whose Presence flow stops rejoins the topic through the known hosts; a member whose home relay dies removes it from the relay map (iroh 1.3 Endpoint::remove_relay, a relay-map change forcing a full report) and adds it back when its host announces again | D14, D20, 3.8, S7, S21 | spec edit + experiment (E12)  E12 (macOS): relay removal re-homes in 0.7 s instead of ~42 s, no false removal; own rejoin does not heal (0/62 stalled pairs), because every fresh dial after the kill times out, members on the live relay included (C16).  Linux agrees (lab/linux/linux-e12: L1 0.7 s 9/9, rejoin heals 0/38, every fresh dial after ~4 s times out). |
| S25 | stop on end of stdin: the binary reads stdin through its own wrapper that notes end of input and starts Stopping at once (Departure handed to a task), before rmcp's 5 s drain; SIGTERM sends Departure first, then shuts the runtime down in the background; measured on macOS: departure under 1 ms in all cases, exit unchanged (5 s eof drain, 2 s cancel drain) | 3.8 stop row, 3.9, 3.14, S17 | spec edit; Linux agrees (lab/linux/linux-e13: departure 0 ms median in all 12 cases, exits unchanged) |
| S26 | relay-death workaround (C16): a member that hears no Presence from any peer for 3 s closes its endpoint, binds a fresh one with the same key, builds a new gossip instance, and rejoins the topic through the known hosts; at most one rebind per 20 s; connections drop at each rebind. Measured (gossip harness, scenario 1): heals every stalled pair by 180 s, macOS 76/76 (E15) and 30/30 (E16 F3), Linux 48/48; heartbeat a median 4.1-4.2 s after the rebind; relapse needing a second rebind in 5/13 (macOS) and 1/8 (Linux) runs, cause open; 0 false rebinds in 6 no-kill runs. Replaces S24's rejoin lever (L2), which heals 0-2/24 and, with a re-dialing gossip, feeds the block (E16) Relapse causes (E17, experiments/e17-relapse, spike/e17-relapse 83d75bd, macOS, diagnostic build): (1) the rebound endpoint learns a peer's pre-kill path through the dead relay from the lookup in its first second, keeps it (remote_state paths only grow), and with no open connection to that peer sends each fresh-dial datagram on every known path (remote_state.rs:805-830, checked), so the dead relay's queue refills to 64 and blocks again 57.2-57.4 s after the rebind: 4/4 endpoints without a connection to that peer, 0/12 with one; the 1/s feed is the harness probers, real-member rate unknown. Counter C2 (probe configured relays by TCP at rebind, strip relays found down from other members' lookup entries, 24 lines) removes the block (0/25 endpoints) but not the relapses (2/6 stalled runs against 3/8). (2) late attachment: after a rebind the bootstrap node still holds the old connection's peer in its active view and sends no Neighbor to the re-Join (one trace; hyparview pending_neighbor_requests reading, not instrumented), 57-120 s without a neighbor; frequency 0/24 endpoints in W1, 2/18 with C2, 4/9 with a fresh lookup. Linux (lab/linux/linux-e17, n=8 per arm, table checked): both relapse causes seen once each; W1 2/8 second rebinds (1 with the 58 s re-block at m1conn 0; 0/11 blocked with an M1 connection); W1+C2 0/8 second rebinds, 0 blocks. In the Linux late-attachment run all three members rebound exactly 60.0 s after the first rebound with silent_ms=0: the harness join timeout (main.rs:352, subscribe_and_join under timeout 60 s, JOIN_FAIL then rebind), so a 60 s wait for a first neighbor is ended by the harness, not by gossip. Late attachment explained (C18, E18): stale pending Neighbor request at the bootstrap node; counters measured: join timeout 5 s then rebind (member), on_join backport of iroh-gossip #161 (bootstrap). Combined (E19, experiments/e19-combined, spike/e19-combined b1357d1, macOS, n=8 per arm interleaved): W1 + C2 + 5 s join timeout + on_join backport: 0/8 runs with a second rebind, 42/42 pairs flowing, all flowing from 29.3-33.2 s, 0 false rebinds in 3 no-kill runs; W1 alone 3/8 relapse, one run never fully healed, fast heals 15.7-18.6 s otherwise (B1 vs B0 p=0.20); without C2 5/8 relapse, median 141 s (C2 earns its lines, p=0.026). Cost: about 14 s slower first heal than W1 alone when W1 does not relapse (cause open); re-blocks in the stock build inferred from timing only. Slower first heal explained (E20, experiments/e20-delay, spike/e20-delay 9abb991, macOS): not relay homing (home relay connected 401-404 ms after bind in 42/42 endpoints); a rebound member with no member neighbor hears heartbeats only through the bootstrap node's lazy push, 11-16 s late (21/21 association in E19, 21/21 in the rerun); no member neighbor because the join walk ends at the bootstrap node, which holds the member active and only renews (hyparview.rs:403-409, 428-434, checked), or because member dials fail on emptied address entries (co-occurrence only). Change MJOIN (13 lines: 1.5 s after JOINED, with no member neighbor, join_peers(other members) every 3 s): late endpoints 0/24 vs 5/21 (p=0.017), 0/8 second rebinds; run-level heal not shown faster (p=0.34). Needs a member list in the product. Linux agrees on E19 (lab/linux/linux-e19, n=8 per arm interleaved, table and stats checked): combined 0/8 second rebinds, 48/48 flowing, median 20.4 s (14.2-34.7); W1 alone 2/8; without C2 4/8 (B1 vs B2 p=0.077 on Linux alone; both OSes together 0/16 vs 9/16 runs with a second rebind). Linux on E20 (lab/linux/linux-e20, n=8 per arm interleaved, stats checked): late endpoints rarer (1/22 in B1, no member neighbor), MJOIN 0/21; with MJOIN all flowing from median 15.9 s (14.1-19.0) against 20.1 s (17.2-40.4), p=0.008; 0 second rebinds either arm; home relay 402-410 ms. The same B1 arm gave macOS medians 31.2 s (E19) and 18.0 s (E20): run-set variance on one host is that wide. | D14, D20, 3.8, S21, S24 | spec edit; relapse cause under study (E17) |
| S16 | every gossip connection, incoming and outgoing, passes a keyed challenge in both directions inside iroh's after_handshake hook before the gossip layer sees it (owner confirmed: hook, both ways); gate key derived from the secret; 3 s timeout | D13, D17, 3.4, 3.6, 3.7, 3.14 | spec edit |
