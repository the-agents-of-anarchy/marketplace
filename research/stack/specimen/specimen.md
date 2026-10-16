# Specimen: the agent-habilis family

> Basis: reports sp1 to sp5, surveys a3, a1b, and the agent-habilis rows of s3-breadth, read whole; 2026-10-16. Descriptive, per the owner's word. Nothing was run, built, or tested by any report.
> Tags: **H** = commit, tag, release, or issue. **C** = code read at a named commit. **D** = doc, README, or comment only. `AG` = agent-gossip. `HN` = habilis-network.

## What it is

The agent-habilis org (18 repos) built `agent-gossip`: a Rust CLI, MCP server, and library that gives AI coding-agent sessions a serverless peer mesh. It offers broadcast chat over gossip, sealed one-to-one messages over unicast, two shared JSON documents (`state`, `meta`), and A2A-shaped tasks. The networking engine lives in a second repo, `habilis-network`, unpublished and pinned by git rev, built on org-owned forks of iroh and iroh-gossip. The surveys' label "agent-swarm" is an early name of the same repo as AG. AG: created 2026-05-18/19, 531 commits, 19 releases, latest v0.12.4 (2026-10-15), 8 stars. HN: repo record created 2026-10-02 (a3), commit history from 2026-07-31, 105 commits, 0 releases, 1 star.

## Lineage and names

| Date | Event | Evidence | Tag |
|---|---|---|---|
| 2026-05-18 | Initial commit. README titled "agent-habilis-swarm". Commit says references point at "renamed repo agent-habilis/swarm". | AG `c4212fc`, `c4f2500` | H |
| 05-19 to 06-27 | CLI binary renamed `ah-s`, `ahs`, `ahsw`. | `01edfc2`, `b254f57`, `6e610cd` | H |
| 07-04 to 07-18 | Repo and noun renamed: agent-gossip (07-04), agent-mesh (07-05), agent-square (07-06), agent-gossip (07-17), room to gossip and participant to peer (07-18). | `8b46635`, `91bb268`, `63d84f9`, `1d75e16`, `9153588`, `78e2a5d` | H |
| 07-05 | Engine moved from AG `src` into crate `agent-habilis-gossip`, same repo. | AG `7da270b` | H |
| 07-30 | AG splits chat into `msg` and broadcast (`6226382`). Commit `f81b052`, cited by HN docs as the divergence point, has the same tree, a different parent, and is unreachable from AG main. | sp4 | H |
| ~07-30 | Mallorca (a graphics app, no public repo) vendors a subset of the AG engine, base `f81b052`. | HN `VENDORED.md` | D |
| 07-31 | Engine extracted "from the mallorca repo" as `fofoca`. HN history starts here. | HN `86bd79d` | H |
| 08-05 | AG drops its own engine copy and consumes `fofoca` by rev. Body: the repo "kept its own copy, so the two drifted." | AG `98f517c` | H |
| 08-04 | `agent-share` vendored-fork changes merged back into the engine. | HN `dc8ba0e` | H |
| 10-02 | Engine renamed `fofoca` to `habilis-network`. Iroh forks move back to agent-habilis. | HN `9b7b65f`, `61daa92` | H |
| 10-13 | AG renames its engine references. Release 0.12.0, breaking: older mesh ids and tickets stop working. | AG `23c3c0c` (#38) | H |
| 10-16 | AG pins `795c4f8`. HN main is `8722df5`. | AG `Cargo.toml:47` | C |

Names, in order: repo `swarm`, `agent-gossip`, `agent-mesh`, `agent-square`, `agent-gossip`. Engine: in-AG crate, `fofoca`, `habilis-network`. Source of "fork": HN `FORKED.md` says the workspace "began as a verbatim vendoring of a subset of `agent-habilis/agent-gossip`" (D). History shows three things: the engine began in AG (7da270b), HN began as an extraction from mallorca (86bd79d), AG consumes HN by rev (98f517c, Cargo.toml). Verdict in the contradictions section.

## Anatomy

| Part | Where it runs | Boundary |
|---|---|---|
| Engine event loop (one `tokio::select!`: IPC, HTTP, gossip, probes, timers, quit) | HN `daemon/event_loop.rs:674` | Same loop code for every frontend. |
| CLI daemon | One detached process per mesh and nickname. `--owner-pid` re-exec with `setsid`. | Unix socket `<runtime>/<nickname>.ipc.sock`, mode 0600, no in-band auth. Runtime base `/tmp/agent-gossip-<uid>`. |
| MCP server | Engine loop inside the MCP server process. Poll-only, no daemon, no state file. | stdio (rmcp). One mesh per server instance. |
| Library `MeshSession` | Engine loop inside the host process. | In-process. Drop aborts the loop. Graceful path is `leave()`. |
| Bell | Background `agent-gossip poll --long`, holds OS lock `<nickname>.bell`. | Ends on an unserved event or at `--max-secs 7000`. |
| Stop hook | `agent-gossip bell-check --session-pid "$PPID" \|\| true`, 15 s, in four skills' front matter. | Prints a block decision when a ready session has no armed bell. |
| Skills | 16 `gossip-*` dirs, rendered to `SKILL.md`, embedded in the binary. `plug` installs them. | Prose carries the protocol. |
| Browser peer | `agent-gossip-wasm-client`, own lockfile, not built in CI. | wasm, WebRTC. |
| A2A faces | `--a2a-serve` local HTTP JSON-RPC with bearer token. `a2a expose` and `connect` tunnel A2A HTTP over the mesh. | Localhost, own ALPN. |
| Engine crates | 16: protocol, util, doc (automerge), chunks, stream, netplay, ffi, wasm, four transports (iroh-gossip, multihop, webrtc, util). | Engine is `publish = false`. Consumers: AG, `agent-share`, mallorca via C ABI. |
| Transports | iroh QUIC direct and relay, WebRTC, multihop (max 8 hops), gossip-as-transport (partly built). | Default set `udp,webrtc,gossip` (0.12.0 changelog). HN doc 9.1 says `udp,webrtc,multihop,gossip`. |
| Discovery | Lookups `mdns`, `dht`, `relay`. Relay ladder rung 0 is `https://relay.agent-habilis.com/`. Rendezvous beacon co-hosted by a member. | Join id carries the seed. |
| Org relatives | `agent-graph` (graphs "in a gossip"), `agent-share`, `agent-inject`, iroh and iroh-gossip forks, `iroh-address-lookups`, `swarm-discovery`. | Not read beyond README and pin comments. |

## Identity and names

| Fact | Evidence | Tag |
|---|---|---|
| Identity key: Ed25519, minted per process by `Identity::generate()` in daemon setup. Memory only. A restart mints a new key. | HN `daemon/setup.rs:692`, `identity.rs:13-16` | C |
| Seal key: X25519 derived from the Ed25519 seed, label `habilis-mesh/x25519-enc/v1`. Public half published in the card's `mesh-seal` extension. | HN `identity.rs:70-92`, AG `card.rs:78-84` | C |
| iroh `EndpointId`: fresh random key per endpoint build. | HN `lookup/mod.rs:891-895` | C |
| Nickname: 1 to 32 chars, forbids control, whitespace, bidi, `< > # / \`. Default random `word-word` from a 1024-word list (1,048,576 names). | HN `ident.rs:26-46`, `name.rs:127-129` | C |
| Nickname is "a non-unique display label ... deliberately not pinned/claimed". | HN `gossip/recv.rs:547-551` | C |
| Nickname keys four lookups: endpoint binding, seal key (`/peers/<nick>/card`), addressee test, card-forgery gate. | HN `state.rs:2053-2074`, AG `card.rs:122-145`, HN `recv.rs:1362-1365`, `-doc/lib.rs:221-243` | C |
| Roster is a nickname-keyed set. Two keys under one nickname count once. No collision handling found. | HN `state.rs:333`, `membership.rs:72` | C |
| Signing key binds to an endpoint through `PeerInfo`. Anti-entropy answers go to the endpoint the key proved. | HN `state.rs:269-272`, `transport/send.rs:161-177` | C |
| Mesh membership: possession of the join id (32-byte seed, "the bearer credential"). Topic meshes seed from `SHA256(domain \|\| string)`: anyone who knows the string joins. Invite tickets default 24 h. | HN `docs/architecture.md` 4.3-4.5, `crypto.rs:55-58` | D, C |
| MCP and CLI address a peer by nickname. No handle or key field in `send_msg`. | AG `mcp/mod.rs:190-197` | C |
| Session-to-daemon ownership: pid ancestry or recorded owner pid, confirmed over IPC. | AG `cli/session.rs:76-83, 204-249` | C |

## Presence

| Layer | Mechanism | Evidence | Tag |
|---|---|---|---|
| Engine | Presence subtypes `Joined`, `Left`, `Alive`. `Alive` sent only after 30 s with no other broadcast. Sweep every 10 s evicts members unheard for 90 s. | HN `lifecycle/heartbeat.rs:16-41`, `tuning.rs:136-157` | C |
| Engine | Presence updated by any received traffic. Eviction event only for members whose arrival was surfaced. | HN `lifecycle/mod.rs:58` | C |
| Engine | Graceful exit sends `Left`. SIGTERM, SIGHUP, SIGQUIT, ctrl-c, and owner-pid change all take the graceful path. | HN `daemon/shutdown.rs:113-238` | C |
| App | Task beats: status `mesh:beat` every 30 s on live tasks. A party cancels after 2 minutes with no leg or beat. | AG `a2a/extensions.rs:8`, changelog 0.11.1, `e883286` | C, H |
| App | Reader liveness is pulled: `mesh/reader.get` to each live peer, one shared 500 ms deadline. A slow peer shows no `reader` key. | AG `a2a/peer_path.rs:103-168` | C |
| App | Receipts: `delivered` when the recipient daemon takes the frame, `read` when its agent polls it. | AG `a2a/receipt.rs:1-60` | C |
| App | Bell armed state is an OS file lock, not daemon memory. | AG `cli/bell.rs:23-44` | C |
| Earlier survey | iroh-gossip itself has no heartbeat. `Alive` is the engine's addition. | `f2-gossip.md:16`, not rechecked by sp1 | D |

Presence cost of idle members is unmeasured. A bench `benches/idle_cost.rs` exists, unread.

## Messaging and delivery semantics

| Aspect | Behavior | Evidence | Tag |
|---|---|---|---|
| Two planes | Broadcast over gossip. Directed `msg` over unicast only, sealed to the recipient. Gossip never carries a directed frame. | HN `transport/send.rs:1-6`, AG commit `6226382` | C, H |
| Sealing | Ephemeral X25519, ECDH, ChaCha20-Poly1305. AEAD associated data is the constant label. Sender bound only by the outer Ed25519 signature over the ciphertext. | HN `seal.rs:62-87` | C |
| Missing seal key | Send errors `cannot seal to '<nick>'`. Never plaintext. | AG `send.rs:854-876` | C |
| Broadcast body | Public gossip: plaintext, signed. Passworded: encrypted with mesh key, plaintext refused. Frames carry per-author `seq`, `prev` hash, DAG parents. | AG `send.rs:357-388` | C |
| Directed ordering | No sequence number. Order within one stream unverified. | AG `send.rs:959-974` | C |
| Size | Wire frame 3840 B. Body input 64 MiB. Sealing inflates about 1.4x. More than 16 shards: not logged. | HN `consts.rs:45-78`, AG `send.rs:688` | C |
| "Sent" | Means the unicast write or handoff succeeded. Cold peers are dialed by a task whose verdict arrives later. | HN `transport/send.rs:24-40` | C |
| Receipts | Sealed, unicast, fire-and-forget. No retry, no ack. Older peers send none. | AG `receipt.rs:24-26`, changelog 0.12.4 | C |
| Retries in product | Card publish (doubling waits), lost shards (from sender cache), frames buffered while unmeshed. None for a directed message. | AG `node.rs:124-127`, `send.rs:1524`, HN `recv.rs:370-454` | C |
| Absent recipient, no endpoint known | Error `undeliverable`. Not stored. | HN `transport/send.rs:74-89` | C |
| Absent recipient, sender unmeshed | Accepted, echoed, buffered (1024 frames, no age limit seen), re-sent on next meshed edge. | HN `tuning.rs:38`, `recv.rs:377-456` | C |
| Absent recipient, sent then went offline | Logged (1000 entries, count-based eviction of the fullest author's oldest message). Digest every 10 s, at most 3 answerers, 64 resends each. Resend works only if the recipient's endpoint is known then. | HN `tuning.rs:16-106`, `antientropy.rs:296-365` | C |
| Retention bound | Count, not time. A long absence can outlast every holder's log. | HN `message_log.rs:110-181` | C |
| Tasks | A2A-shaped. Limits: 64 live per peer, 1024 across peers. Replayed legs no longer surface (0.11.1). | AG `a2a/tuning.rs:93-100` | C |

## Reaching an agent session (per harness)

| Harness or path | Mechanism | Evidence | Tag |
|---|---|---|---|
| Any MCP client | Poll `fetch_messages`, cursor in MCP process memory, `long=true` parks about 60 s. MCP push exists but "no major MCP client surfaces it". No wake. | AG `mcp/mod.rs:27-31, 925-928` | C |
| Claude Code | Daemon plus bell (`poll --long`). Bell exit is the wake, delivered by the harness as a background-task notice. Agent then reads in the foreground and re-arms. Stop hook refuses an end of turn with the bell unarmed. | AG `skills/shared/receive-loop.md`, `cli/session.rs:411-436` | D, C |
| Claude Code, discover | Monitor adapter streams `gossip_found` and `gossip_lost`. Only Monitor path left. | `skills/gossip-discover/adapters/claude-code.md` | D |
| Pi | Daemon and bell run as tasks in the pi-processes `process` tool, `alertOnSuccess: true`. Missing tool: skill prints install block and stops. | `skills/shared/daemon-session.md` | D |
| Codex | No push. Poll in the foreground each turn. | `receive-loop.md:5-9` | D |
| Cursor, opencode | Skill tree installed. No receive mechanism named. Unverified. | `cli/agent.rs:50-61` | C |
| Library host | Engine loop in host process. | AG `api/session.rs:41` | C |
| Browser | wasm `GossipPeer`: create, join, broadcast, `messages(after)`, leave. No card published, so directed sends to it fail (#2). | wasm `lib.rs:57-180` | C, H |
| Non-agent HTTP client | `--a2a-serve` JSON-RPC 2.0 with bearer token, card at the well-known path. | AG `cli/args/shared.rs:30-37` | C |

The bell prints nothing. Daemon stdout goes to `/dev/null`. Skill text: "A notification cannot carry a message." The harness half of every wake is outside the repo and untraced.

## Evolution: what was tried, kept, removed

| Date | Change | Evidence | Fate |
|---|---|---|---|
| 05-18 | 6 MCP tools, HyParView and Plumtree-style gossip over iroh-gossip | `c4212fc` | Grew to 19 tools by 07-30. Stable since `6226382`. |
| 05-26 | Aggressive QUIC keep-alive and idle override | `69ca1c2` | Reverted to iroh defaults. |
| 05-27 | Env-var config | `b83c9fc` | Replaced by constants and hidden flags. |
| 06-27 to 06-30 | Shared `state` and `meta`, first JSON Patch | `a8e5398`, `673311c`, `36a244c` | Kept, now RFC 7386 merge. |
| 06-28 | Per-author rate limiter | `74660e9` | Removed. |
| 07-02 to 07-03 | `pipe`, `mount`, `port`, `sh`, `file` subcommands | `70de613` to `79da240` | Removed. |
| 07-03 | Native A2A v1.0. Added `a2a_call`, `task_artifact`, `task_status`. | `115ac1c` | Kept. `send_task`, `send_notice` removed. |
| 07-10 | Push via harness notification | `d564dc9` | Removed: "can truncate a message body or write it to disk". Poll plus bell. |
| 07-10 | `--spool` frame mirror | `155a9db`, `5b708c9` | Removed as "incomplete". |
| 07-11 | Interactive surface; directed-over-gossip transport | `4dd28ee`, `5dc1507` | Removed. JSON-only output. |
| 07-30 | `send_message` split into `send_msg` and `send_broadcast` | `6226382` | Kept. |
| 08-02 | Backfill re-broadcast directed frames to the whole gossip | `0216a54` | Fixed: addressee only. HN same fix 08-05 `71e99dd`. |
| 08-04 to 08-05 | Multihop crate: out of repo, back in. Blob crate removed, transport half restored behind a flag. | HN FORKED changes 13, 18, 20, 25 | Churn within one week. |
| 08-14 | Browser peer | `165c559` | Kept. Not in CI. |
| 08-30 | Blob crate removed for chunk store | HN `4b6f00b` | Kept. |
| 09-22 | `--lookup` and `--transport` replace old flags. `--public` dropped. | `83d7d38` | Kept. |
| 09-23 | Stop hook ("only the model enforced the one-bell contract") | `d31543a`, 0.10.0 | Kept. |
| 09-25 | Task beats and 2-minute stall cancel | `e883286`, 0.11.1 | Kept. Skills stopped telling workers to re-send `working`. |
| 09-30 | Daemon held as background task "ended every gossip session within 2 h" | `c747529` | Replaced by detached `setsid` daemon plus owner-pid watch. |
| 10-13 | Card published in frame-sized merges. Mesh ids v2. | 0.12.0, #41 closed | Kept. |
| 10-15 | Delivery receipts, reader liveness | `30d8747`, 0.12.4 | Kept. |
| 06-03 to 10-12 | Iroh and iroh-gossip forks: leak fixes (AG, 06-03 to 06-05), patches dropped from AG 07-05 (`42e8523`), re-homed in HN with path-selection and `LeavePeers` patches (09-23 to 10-12). | AG `2157f76`, HN pin comments | In force in HN. |

## Strains

| Strain | Evidence | Tag |
|---|---|---|
| Nickname collisions silent. Rosters keyed by nickname. A `Left` from one holder removes the name for both. | AG #28 open, HN `state.rs:333` | H, C |
| Daemon death plus rejoin: new random nickname, open tasks lost. Same-nickname rejoin refused about 90 s. | AG #29 open | H |
| Every restart changes all keys. | HN `identity.rs:13-16`, self-flagged "documented follow-up" | C |
| Stale seal key after peer restart: frame fails to open, dropped with WARN, no receipt, sender sees success. | sp2 reading of AG `node.rs:322-327` | inferred |
| Directed send to browser peer fails every time, error claims transient. | AG #2 open | H |
| Card of 4840 B against 3840 B frame: every directed send failed 25+ minutes, trace was one WARN. | AG #41, closed 10-13 | H |
| Shard groups over 16 not logged, never backfilled. | AG `send.rs:688-690` | C |
| `Done` returned for a buffered frame while unmeshed. | HN `broadcast.rs:96-100`, `transport/send.rs:23-25` | C |
| Held-frame buffer has no expiry in flush path. | HN `recv.rs:377-456` | C |
| Reader state pulled, commit titled "publish reader liveness". Slow peer reads as unknown. | AG `peer_path.rs:103-168` | C |
| Directory meshes always carry multihop policy. | HN #7 open, `directory.rs:79` | H, C |
| Stream reader cannot attach with mdns or dht in hash. | HN #3 open | H |
| AG copies transport ids and `LookupSet::any` from the engine by hand. | HN #9 open | H |
| Full disk: state-file heartbeat can still abort the engine daemon in about 10 s. | AG changelog 0.11.x | D |
| Tests fail under host load. | AG #42 open | H |
| Other open AG issues: #37 stuck-task check, #40 `gossip-join` drops `--nickname`, #44 stale model field. | `gh issue list` | H |
| Stop hook: scope is four skills. Persistence across turns is harness-dependent. Upgrade refuses first stop once. | AG `cli/agent.rs:381`, changelog 0.11.1 | C, D |
| MCP-only clients cannot be woken. | AG `mcp/mod.rs:925-928` | C |
| Pin drift: AG pins `795c4f8`, HN main `8722df5`. Bump by hand. | `Cargo.toml:47` | C |
| Doc drift, nickname: `identity.rs` and `message/mod.rs:1029` describe trust-on-first-use pinning. Receive path pins nothing. | HN `identity.rs:10-31`, `recv.rs:547-551` | D vs C |
| Doc drift, missing file: `identity.rs` cites `docs/history-integrity.md`. Absent. | HN tree `8722df5` | C |
| Doc drift, `FORKED.md` lists crates `-reassembly`, `-directory`, `-blobs`. None exist. Omits `-chunks`, `-stream`, `-netplay`, `-wasm`. | HN #8, `crates/` | H, C |
| Doc drift, AG `tuning.rs:29-36` says directed requests ride the gossip overlay. Engine says they never do. | AG `tuning.rs`, HN `transport/send.rs:1-6` | C vs C |
| Doc drift, README "verified on receipt" and "backfilling missed messages". Key not checked against nickname. Backfill needs known endpoint. | AG `README.md:22, 66` | D vs C |
| Doc drift, "nothing to host" vs relay rung 0 at `relay.agent-habilis.com`. | AG README, HN `lookup/relay.rs:55-63` | D vs C |
| Doc drift, MCP module doc names `skill/SKILL.md` (absent) and "April 2026" (earliest commit 2026-05-18). | AG `mcp/mod.rs:27-37` | C |
| Naming drift: structs `CreateMeshArgs`, `MeshInfoResult` under tools named `gossip`. | AG `mcp/mod.rs:107-344` | C |
| Unused dependency suspected: `slot-template` has no reference under `src/`. Tests and `build.rs` not checked. | AG `Cargo.toml:52` | C |
| Citations to missing objects: HN `FORKED.md` change 24 cites upstream `0b9f438`, absent. Iroh-gossip PR `#147` not found locally. | sp4 | C |

## Contradictions between reports, and resolution

| # | Claim A | Claim B | Resolution |
|---|---|---|---|
| 1 | a3, sp5: HN is a fork of AG, AG is "the upstream line" (`FORKED.md`). | sp1, sp4: `FORKED.md` is stale. AG consumes HN. HN history starts at a mallorca extraction. | Split. **Origin stands, on mixed evidence.** Engine code began in AG (H: `7da270b`). A copy sat in mallorca (D: `VENDORED.md` base `f81b052`; H: `86bd79d` message "vendored inside mallorca"). HN began as that extraction. **Current relation: consumer and engine** (C: `Cargo.toml:47`; D: `HABILIS_NETWORK_CHANGES.md:3-5`). "Upstream line" does not stand. a3 read only `FORKED.md` lines 1-40 and none of AG. |
| 2 | `FORKED.md` names `f81b0529` as divergence. | HN history lacks that SHA. | Unresolved. SHA exists in AG clone (sp1). Unreachable from AG main, tree equals `6226382`, parent differs (sp4). sp4 infers AG history was rewritten. That is inference. Cannot confirm from HN. |
| 3 | `FORKED.md` skips the mallorca hop (as quoted by sp5). | `VENDORED.md` and `86bd79d` name mallorca. | Commit message outranks the doc. Whether `FORKED.md` mentions mallorca elsewhere: unread past line 60. |
| 4 | a3: 18 MCP tools. | a1b, sp3: 19. | 19. a3 omitted `a2a_call` (`mod.rs:813`). a1b table lists all nineteen with lines. |
| 5 | a1b: nickname bound to key trust-on-first-use. | sp2, sp4: nicknames not pinned. | Code stands (`recv.rs:547-551`). a1b read the doc comment (`identity.rs:11`). No TOFU code found. |
| 6 | a1b, sp3: production key generation site not found. | sp2: found. | Found. HN `daemon/setup.rs:692`. |
| 7 | Estafette brief via a3, and `f2-gossip.md:16`: "no heartbeats". | a3, sp1: `Alive` every 30 s, 90 s timeout. | Both hold at different layers. iroh-gossip has none. The engine adds `Alive`. |
| 8 | sp1, sp3: `agent-habilis/agent-swarm` redirects to AG. | sp5: `agent-swarm` returns 404. `swarm` resolves. | Unresolved. Reports checked on one date. Only README title "agent-habilis-swarm" and commit `c4f2500` name the early repo. "agent-swarm" may never have been a repo name. |
| 9 | sp1: pin `795c4f8` is an ancestor of HN HEAD. | sp4: not in any ref of the HN clone. sp2: AG commit `5faf662` pins `8722df5`. | Unresolved. Clones differ (blobless, shallow). sp5 read `795c4f8` through the GitHub API. `5faf662` ref not stated. |
| 10 | a3: own directed frames are never retained (`recv.rs:1068`). Example app sets `loggable: false`. | sp2: sender logs a directed frame after a successful send (AG `send.rs:1356-1371`). Commit `0216a54`: "both parties retain". | Layers differ: engine example app and AG app. Not traced end to end. Unresolved. |
| 11 | a3: 9 open HN issues. | sp4: 7 open, 7 closed. | Later count stands: #3, #7, #8, #9, #19, #20, #21. |
| 12 | sp5 lists four `plug` roots. | sp3: five, with opencode (`cli/agent.rs:50-61`). | sp3 stands. Names the fifth. Not rechecked. |
| 13 | sp3 observation: "one repo, three names". | sp3, sp5 bodies: five or six names. | Bodies stand. Five repo names, six counting `swarm`. |
| 14 | sp4, `docs/architecture.md` 9.1: default transports include multihop. | AG 0.12.0 changelog: default `udp,webrtc,gossip`. | Both are D. Different repos. Code not read for either. Unresolved. |

## Confidence

| Item | Status |
|---|---|
| Executed anything (tests, builds, benchmarks, mesh) | Nothing, by any report. |
| Rests on history (commits, tags, releases, issues) | Rename sequence, engine extraction and consumption dates, tool-count timeline, removals, push-removal reasons, open and closed issues. Strongest tier. |
| Rests on code read at a commit | Presence timers, sealing, size limits, delivery cases, nickname handling, bell and hook. Bodies of unicast pool, multihop forwarding, and `antientropy.rs` functions unread. |
| Rests on docs or comments only | Gossip-as-transport relay gate, default transport set, `VENDORED.md` base SHA, mallorca's role, harness behavior of every wake path, Cursor and opencode receive. |
| Inferred, not reproduced | Stale seal key after restart. Rewritten AG history. Divergent answerer ranking from differing views. |
| Unread | Mallorca (no repo), `agent-share` past README, `agent-graph`, wasm bodies, npm packages, FFI, formula sha256, issue comments, history before 07-17 (blobless pickaxe timed out), HN branches `fix-multihop-transport` and `fix-loopback-room-split`. |
| Harness side | Claude Code, Pi, Codex, Cursor, opencode code never read. Wake claims are skill text. |
| Dates | All 2026. Snapshot 2026-10-16, AG `2c5e132`, HN `8722df5`. |
