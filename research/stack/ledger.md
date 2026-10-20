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
│   ├─ ■ relay + bootstrap death stalled gossip mesh-wide in 0.101.0:    e8
│   │      heartbeats never resumed in 88 s, also between members on the
│   │      live relay (3/3 with probers, 1/3 without); cause untested
│   ├─ ■ bootstrap failover cheap: one of two dead, join in 8-18 ms        e8
│   └─ ○ NAT; two hosts; the e8 stall against unreleased iroh-gossip main
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
├─ MCP ───────────────────── rmcp 3.5.1 (ruled) ────────────────────── unverified
│   └─ ○ static six tools over stdio; stdin close; shutdown
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
│   └─ ■ 314 unique deps without rmcp and clap                           e1 10
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
| 28 | — | Tree cost | RUN: e1's package (iroh, iroh-gossip, iroh-relay server, mDNS, tokio) 314 unique dependencies; rmcp and clap not included | e1 10 |

## OPEN, ordered by how much of the spec rests on it
1. Node as identity: sidecar lock released on crash (macOS, Linux); a restarted node reusing its id while peers hold a stale connection; which instance answers a dial in that window. Gates D2-D7, D10, D30, 3.4, 3.6, 3.8, 3.9.
2. Address lookup: dial by id with n0's preset (pkarr), with a self-hosted lookup, and with addresses carried in Presence; several relays in one map and how a peer homed elsewhere is reached. Gates 3.3 config, 3.10 step 3, D14, relay TLS.
3. Presence flow: join, Introduce to a late joiner, Departure delivery within 1000 ms, probe after NeighborDown, Unreachable rumor and self-correction (D18-D20, 3.8, tests 4, 5, 8, 19, 20).
4. Gossip admission: does an outsider holding only the topic id and a bootstrap address receive Presence (lead: verify/v2-gossip-gate.md, a source trace).
5. rmcp: a static six-tool server over stdio; stdin close detection; shutdown with a pending stdin read (D28, 3.9, 3.10).
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
| C7 | D14 | relay TLS and n0 relay compatibility | e1 7 | plain HTTP; ACME; manual cert; list including n0 relays |
| C8 | D3-D7 | RULED → S14 | | |
| C9 | 3.8 init row, D18 | RULED → S15 | | |
| C10 | D19, 3.8 stop row | RULED → S17 | | |
| C11 | 3.10, 3.14 | RULED → S19 | | |
| C12 | D13, D17, 3.7 | RULED → S16 (mechanism measured in e9; confirmation pending) | | |
| C13 | D11, D14, S7 | a relay and bootstrap host dying stalled gossip mesh-wide for 88 s in iroh-gossip 0.101.0, members on the live relay included | e8 | rerun e8 scenario 1 against iroh-gossip main (unreleased connection-lifecycle fixes) before ruling; then keep the release pin, pin main by revision, or wait |

## Staged revisions (ruled, not applied)
| # | Ruling | Spec sections | Kind |
|---|---|---|---|
| S1 | lower the `public` cap so the default gossip frame carries the largest Presence; exact cap after C5 and C8 | 3.5, 3.7, 3.14 | spec edit |
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
| S16 | every gossip connection, incoming and outgoing, passes a keyed challenge in both directions inside iroh's after_handshake hook before the gossip layer sees it (owner confirmed: hook, both ways); gate key derived from the secret; 3 s timeout | D13, D17, 3.4, 3.6, 3.7, 3.14 | spec edit |
