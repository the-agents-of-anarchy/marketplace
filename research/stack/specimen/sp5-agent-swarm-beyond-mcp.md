# Agent-swarm beyond its MCP module

Date: 2026-10-16.

Repos and commits read:

- `agent-habilis/agent-gossip` at tag v0.12.4, commit `106b709` (2026-10-15). Source snapshot extracted to `/tmp/ra-spec/agent-gossip-v0.12.4`. History read from the blob-filtered clone at `/tmp/ra-spec/agent-gossip` (HEAD `2c5e132`, 531 commits).
- `agent-habilis/habilis-network` at rev `795c4f8`, the rev v0.12.4 pins in `Cargo.toml`. Read through the GitHub API. The local clone at `/tmp/ra-spec/habilis-network` is empty and was not fetched.
- `agent-habilis/homebrew-tap`, `Formula/agent-gossip.rb`, default branch.
- `agent-habilis/agent-share` README and `Cargo.toml` (lines 30-45 only).
- GitHub releases, repo metadata, and issue titles and states, via `gh`.

Naming: the brief and the earlier survey call this project `agent-swarm`. `agent-habilis/agent-swarm` returns 404. `agent-habilis/swarm` resolves to `agent-habilis/agent-gossip`. The project has carried at least six names (see History). The `agent-swarm` label is used below only where a source says so.

## What it is

The workspace builds one binary, `agent-gossip`, and a Rust library. The binary is a command-line tool, an MCP server, and a background daemon launcher. It gives an AI agent a peer mesh: create or join a named mesh, exchange messages and agent-to-agent tasks, and receive events through a background "bell" process. The networking engine, the daemon itself, and the protocol live in a separate repo, `habilis-network`, pinned by rev. This workspace holds the agent-facing layer: the CLI, the skills installed into each harness, the A2A bindings, the Claude Code Stop hook, and a browser peer crate.

## How it works

### Crates

Sizes are from the v0.12.4 snapshot.

- **`crates/agent-gossip`** (0.12.4, 114 Rust files, about 42.7k lines). Binary and library. Modules: `cli/` (commands, `plug`/`unplug` skill installer, `bell`, `session`, `doctor`), `a2a/` (agent-to-agent model, RPC, task state, surfaced events), `mcp/`, `bridge/` (tickets, card rewrite, directory, gate, expose), `api/` (in-process `MeshSession`), `output/` (JSON rendering), `harness/` (bench and adversarial suites, behind feature flags). Integration tests live in `crates/agent-gossip/tests/`.
- **`crates/agent-gossip-wasm-client`** (0.1.0, 3 files, 612 lines). Browser peer. Excluded from the root workspace (`Cargo.toml`, `exclude`), has its own lockfile, `publish = false`.
- **`crates/agent-gossip-test-fixtures`** (0.5.0, 1 file, 1,841 lines). Shared harness for the integration suites.
- **`crates/tasks`** (0.1.0, 18 files, 1,655 lines). Developer task runner. Renamed from `xtask` on 2026-05-23 (`fe4f786`). `release.yml` calls `cargo task man`.
- **`crates/slot-template`** (0.1.0, 708 lines). Pure templating crate. Declared as a dependency at `crates/agent-gossip/Cargo.toml:52`. No `slot_template` path appears under `crates/agent-gossip/src`. Not checked in tests or `build.rs`.

Workspace comment, `Cargo.toml`: the engine is pinned "by **rev**, not a path to a sibling checkout," and "an engine change is now push-then-bump here."

### Daemon and its lifecycle

There is no daemon code in this workspace. The daemon is `habilis_network::daemon` at `crates/habilis-network/src/daemon/` in the pinned engine rev. This workspace starts it and gives it an owner.

Start:

- `crates/agent-gossip/src/cli/mod.rs:161` (`detach_if_owned`). With `--owner-pid`, the launcher re-executes itself with `--detached-child`, calls `setsid` in `pre_exec` (about `cli/mod.rs:183`), and exits 0. The inline comment says `process_group(0)` is not enough "because Claude Code also walks processes by session id."
- Stdio: a captured pipe or socket is replaced by `/dev/null`, so the caller is not blocked. A file or tty is inherited, so the session `.stderr` file still gets startup errors (`cli/mod.rs`, `detached_stdio`).

Owner tracking and exit:

- `habilis-network/crates/habilis-network/src/daemon/shutdown.rs:154` (`validate_owner_pid`) and `:176` (`Owner`). The owner is identified by pid plus start time, because "the pid alone cannot tell the owner from a later process that reuses the pid."
- `shutdown.rs:238` (`watch_owner`). Polls the owner's start time at an interval. When it changes, the daemon sends a quit on the same channel as SIGTERM, which "broadcasts `left` and exits cleanly."
- `shutdown.rs:214` (`spawn_orphan_watch`). A daemon with no owner watches its parent pid instead. The watch is skipped when the parent is pid 1.
- `shutdown.rs:113-134`. ctrl-c, SIGTERM, SIGHUP, and SIGQUIT all route through the graceful path.
- `leave` stops the daemon on demand (`skills/shared/daemon-session.md`, Claude Code block).

Paths and files:

- Runtime base `/tmp/agent-gossip-<uid>`. `crates/agent-gossip/src/lib.rs:92-100`. The doc comment calls it "a live filesystem contract" that `skills/shared/daemon-session.md` hardcodes.
- Session state file, passed by each skill as `--state-file /tmp/agent-gossip-$(id -u)/sessions/${PPID}.json` (`skills/shared/daemon-session.md`).
- Engine state file writer: `habilis-network/.../daemon/state_file.rs:164` (`try_write`), written to a tempfile and renamed (`:225`), born with mode `0600` (`:216`). Fields include `ready`, `last_updated`, `pid`, `peer_count`, `owner_pid`.
- IPC control socket at `<mesh runtime dir>/<nickname>.ipc.sock`, `habilis-network/.../transport/ipc.rs:24-27`. Bound before `ready` is set (`ipc.rs:84-86`). Chmod `0600` (`ipc.rs:115`). The socket has no in-band authentication; the doc comment relies on the `0700` runtime base (`ipc.rs` around line 94).

### Stop hook and bell

Install path. The hook is not written to a settings file. It sits in the YAML front matter of four session skills: `gossip-create`, `gossip-join`, `gossip-topic`, and `gossip-reattach`. The source is `skills/shared/bell-hook.yaml`, which `cli/agent.rs:331` includes. The test `session_starting_skills_carry_the_bell_stop_hook` (`cli/agent.rs:381`) asserts which skills carry it. `plug` writes skill directories to `~/.claude/skills` (`cli/agent.rs:132`), `~/.pi/agent/skills`, `~/.codex/skills`, and `~/.cursor/skills` (`cli/agent.rs:132-135`).

Hook body, verbatim from `skills/shared/bell-hook.yaml`:

```
agent-gossip bell-check --session-pid "$PPID" || true
```

Event `Stop`, timeout 15 s.

`bell-check`, `crates/agent-gossip/src/cli/session.rs:411-438`:

- Finds live sessions owned by `$PPID` (`owned_sessions`, `:377`).
- For each session, a session counts as ready from its state file (`is_ready`, about `:399`). It counts as armed if an OS lock probe on `<mesh runtime>/<nickname>.bell` succeeds (`cli/bell.rs:46-53`, `is_armed`, a shared-lock probe that fails when another bell holds the exclusive lock).
- If any ready session is unarmed after a grace period, it prints `{"decision":"block","reason":"gossip bell not armed ... run the Receive loop (poll + re-arm) before ending the turn"}` and returns true. The caller exits 3.
- The `|| true` in the hook means the exit code never blocks. The JSON on stdout does the blocking. The comment at `session.rs:408-410` says "Claude Code still reads the JSON."

The bell itself:

- A background process: `agent-gossip poll --state-file ... --long`. Claude Code bells add `--max-secs 7000`.
- `cli/bell.rs:23-44` (`acquire`). Opens `<nickname>.bell` with mode `0600`, takes an exclusive `try_lock`, retries for 500 ms. The file is never unlinked. The doc comment: "An OS lock, not daemon state: the kernel drops it the instant the bell dies."
- `cli/mod.rs:757-763`. The poll builds `IpcCommand::Poll { mesh, after, long }` and takes the bell lock. It then sends that command over the daemon socket.
- Daemon side: per the earlier survey (not re-read here), the daemon answers a long poll at once when an unserved event exists and parks it otherwise.
- Ending: the bell exits when an unserved event arrives, or at `--max-secs`. `cli/agent.rs:590` (`claude_code_bells_end_before_the_harness_limit`) asserts every Claude Code bell ends with `--max-secs 7000`. The reason, from the test's doc comment: Claude Code stops a background task at its timeout "with a notice the agent must not see."

Wake. The bell's exit is the only signal. `skills/shared/receive-loop.md`: "a harness that notifies you gets a push bell for free; one that does not (Codex) catches events on the next turn instead." So the wake is the harness reporting that a background command exited. I did not trace the harness side.

Receive loop, from `skills/shared/receive-loop.md`. On bell exit, the agent makes one foreground poll for content, and in the same message re-arms a fresh background bell. Message bodies never go through the background channel. Its own rule: "Never run a poll that prints events in the background."

Hook history. The Stop hook arrived in `d31543a` (2026-09-23, "refuse a turn that ends with the gossip bell unarmed (#8)"), released as 0.10.0 (2026-09-24). `bell-check` gained exit 3 and the task keep-alive in `e883286` (2026-09-25, #15), released as 0.11.1.

### Wasm client

- Introduced in `165c559` (2026-08-14, "run a gossip peer in the browser"). Last touched in `9efee1c` (2026-10-14, "carry habilis-network PR 16 into agent-gossip (#51)").
- Depends on the same engine rev `795c4f8` with `default-features = false`, which drops the host-only pieces. Also depends on `habilis-network-iroh-webrtc-transport` with the `web` feature.
- Exported `GossipPeer` (`crates/agent-gossip-wasm-client/src/lib.rs`): `create` (`:57`), `join` (`:93`), getters `meshId`, `name`, `nickname`, `peers`, `messages(after)` (`:146`, returns a JSON string), `broadcast(text)` (`:154`), `leave` (`:180`).
- The module comment: "A browser has no mDNS and no DHT; it does not need them." Discovery uses a rendezvous identity derived from the mesh id seed.
- No workflow under `.github/` references wasm. The client is not built in CI.

### Installation and packaging

- **Release flow.** Knope drives versioning. `.changeset/` holds change files, and `knope.toml` names `crates/agent-gossip/Cargo.toml` and `Cargo.lock` as versioned files. `auto-release.yml` runs `knope-dev/action@v2.1.2`. `release.yml` checks that the tag matches `Cargo.toml`, builds archives with `taiki-e/upload-rust-binary-action`, then writes the version and sha256 values into `Formula/agent-gossip.rb` in the tap through a second job that pushes to the tap. CHANGELOG 0.12.3 says this is "the first one that the new flow cuts": "No release PR and no formula PR wait for an admin merge."
- **Targets.** The formula covers `aarch64-apple-darwin`, `x86_64-apple-darwin`, `x86_64-unknown-linux-gnu`, and `aarch64-unknown-linux-gnu`. Intel macOS was dropped in `9fb6b2e` (2026-06-01, "drop Intel macOS release and bump runner to macos-26") and restored in `45c5927` (2026-07-27, "build and serve an Intel macOS binary"). A comment at `release.yml` lines 82-84 says the formula has no `url` on Intel Mac without that target.
- **Formula contents.** Installs the binary and generated man pages. The formula caveats tell the user to run `agent-gossip plug` and then `agent-gossip doctor`. A comment in the formula says `plug` "cannot run from `install` or `post_install`," because both run sandboxed with `deny_read_home`.
- **Other paths.** `cargo install --git https://github.com/agent-habilis/agent-gossip agent-gossip` (`README.md:92`). An agent-runnable install guide at `docs/agentic-installation.md`, reached from the README's "Agentic installation" block. Added in `9e50c31` (2026-07-27).
- **Not packaged.** The `packages/` directory holds web libraries (`moonspace`, `visage-*`). I did not check the npm registry for any package named for the CLI.
- **Not checked.** The sha256 values in the formula were not compared with release assets.

### How agent-swarm and agent-gossip relate

These are one repo under successive names, and the engine was split out to a second repo.

- **Same repository.** The first commit `c4212fc` (2026-05-18) has a README titled "agent-habilis-swarm," described as "a peer-to-peer mesh chat protocol for AI agents." Commit `c4f2500` (2026-05-18) says "point references at renamed repo agent-habilis/swarm." The GitHub repo record shows creation on 2026-05-19. I could not establish the GitHub rename date from the API.
- **Engine fork.** `agent-habilis/habilis-network` at `795c4f8`, `FORKED.md`: the workspace "began as a verbatim vendoring of a subset of `agent-habilis/agent-gossip`," with divergence commit `f81b0529`. The engine used to be called "fofoca": `98f517c` (2026-08-05, "consume the fofoca engine instead of vendoring it") and `23c3c0c` (2026-10-13, "move the engine from fofoca to habilis-network (#38)"). No public `fofoca` repo was found (404).
- **Second consumer.** `agent-habilis/agent-share` (created 2026-08-01) says in its `Cargo.toml` comments that "agent-gossip provably build against the same fofoca" (lines 35-42). The workspace `Cargo.toml` also names `mallorca` as a consumer. `habilis-network` commit `29d3895` (2026-10-03) has the subject "rewrite the README for consumers and drop mallorca." No `mallorca` repo was found (404).

## Why, by their own account

- The engine README: "Serverless — no server to host, no account to create." The same README calls the engine "portable" and "built on iroh."
- The `habilis-network` `README.md` features list says "Peers find each other, form a mesh, and exchange signed messages and shared state, with no server in the middle."
- CHANGELOG 0.12.0: "agent-gossip now runs on habilis-network, the successor of the previous engine. This release is breaking."
- `Cargo.toml` (workspace) on the engine pin: "The cost is real and deliberate ... don't quietly restore the path dep."
- `crates/agent-gossip/src/lib.rs`: the library surface is "deliberately tiny and iroh-free."
- `crates/agent-gossip/src/cli/bell.rs` on the lock: "An OS lock, not daemon state."
- `crates/agent-gossip/src/cli/agent.rs` test comment: "Only the model enforced the one-bell contract, and a model that forgot left the gossip deaf." This explains the Stop hook.

## How it evolved

Dates are commit dates. Names come from commit subjects.

- **2026-05-18, start.** `c4212fc` initial commit. README describes a HyParView and Plumtree-style gossip over iroh-gossip, shipped as CLI, MCP server, or Claude Code plugin.
- **2026-05-19 to 06-27, first renames.** The CLI binary moves `ah-s` (`01edfc2`), then `ahs` (`b254f57`), then `ahsw` (`6e610cd`). "Drop P2P branding" is `61bfc15` (05-19). The task substrate renames to `exchange` (`2e30e8a`) and then `task` (`722daef`). Removed: the per-author rate limiter (`74660e9`, 06-28), the whoami skill (`efb23af`, 05-23).
- **2026-06-01.** Intel macOS release dropped (`9fb6b2e`).
- **2026-07-02 to 07-03.** `pipe`, `mount`, `port`, `sh`, and `file` subcommands removed (`70de613`, `2600ae4`, `a8d4f8f`, `9f76e5e`, `79da240`). `poll --wait` replaced by a no-timeout `--long` (`788ad61`, 07-02).
- **2026-07-04 to 07-05.** Project and binary renamed to `agent-gossip` (`8b46635`, 07-04). Then `agent-gossip` becomes `agent-mesh` and `swarm` becomes `mesh` (`91bb268`, 07-05).
- **2026-07-06 to 07-18.** `agent-mesh` becomes `agent-square`, `mesh` becomes `square` (`63d84f9`, `1d75e16`). `agent-square` returns to `agent-gossip`, and `square` becomes `room` (`9153588`, 07-17). `room` becomes `gossip` and `participant` becomes `peer` (`78e2a5d`, 07-18).
- **2026-07-10 to 07-11.** The `--spool` frame mirror is removed as "incomplete" (`5b708c9`, 07-10), after it was added in `155a9db`. The interactive surface is removed, leaving JSON-only output (`4dd28ee`, 07-11). The directed-over-gossip transport is removed (`5dc1507`, 07-11).
- **2026-07-15 to 07-24.** Handover skill removed (`0752da7`). Task content cap of 100 messages removed (`50505bf`, 07-24).
- **2026-07-27.** Intel macOS binary restored (`45c5927`). Agent install guide added (`9e50c31`).
- **2026-07-30 to 08-05.** A2A and product name stripped from the engine (`5fe1194`). Engine consumed from fofoca instead of vendored, and iroh dependency and patch table dropped (`98f517c`, `50bdc88`, 08-05).
- **2026-08-14.** Browser peer added (`165c559`).
- **2026-09-23 to 09-25.** Stop hook and bell guard (`d31543a`, #8). Tasks kept alive and the bell kept armed (`e883286`, #15). Released as 0.10.0 and 0.11.1.
- **2026-09-30.** Claude Code daemon survives the 2-hour background limit through `--owner-pid` and `setsid` (`c7475291`, #27). Released as 0.11.3.
- **2026-10-13.** Engine moves to `habilis-network` (`23c3c0c`, #38). Released as 0.12.0, which breaks older gossips: "Every gossip hash, mesh id and invite ticket made by an older version stops working." Also added in 0.12.0: file attach to `a2a call` (0.12.1, `c73abe9`).
- **2026-10-14 to 10-15.** Loopback rooms heal after a split (0.12.2). Release flow runs without a human merge (0.12.3). Delivery receipts and reader liveness (0.12.4, `30d8747`).
- **Reverts.** No commit subject is a git revert. One commit body reverts a design: `69ca1c2` (2026-05-26, "upgrade to iroh 1.0-rc") says "Reverts our aggressive QUIC keep-alive/idle override back to iroh's."

## Where it strains

- **Hook scope.** The Stop guard sits in four skills only: `gossip-create`, `gossip-join`, `gossip-topic`, and `gossip-reattach` (`cli/agent.rs:381`). Whether the hook stays registered after the skill loads depends on the harness, which I did not trace.
- **Model-dependent contract.** The bell rule is enforced by the model. The hook only refuses the turn end, and its block text tells the model to re-arm. The test comment at `cli/agent.rs` says "a model that forgot left the gossip deaf."
- **Upgrade hazard.** CHANGELOG 0.11.1: "After you upgrade, the Stop hook refuses the first stop of a live session once." Self-flagged.
- **Harness-dependent wake.** `skills/shared/receive-loop.md` says a harness "that does not [notify] (Codex) catches events on the next turn instead." Pi needs a separate extension (`skills/shared/daemon-session.md`, Pi block).
- **Full disk.** CHANGELOG 0.11.x, self-flagged: "the state-file heartbeat reports its own write failure the same way, so a daemon on a full disk can still abort within about 10 s."
- **Directory meshes ignore the app's transport policy.** CHANGELOG 0.12.0 "Known limit." Same finding as item 7 in `HABILIS_NETWORK_CHANGES.md`.
- **Stale engine docs.** `FORKED.md` lines 23-40 list crates that no longer exist, per `HABILIS_NETWORK_CHANGES.md` item 3. That file says "Nothing here is applied." Status of items 3-6 is unknown.
- **Name compatibility shims.** The engine reads the pre-rename `room` key for a daemon from the previous release (`habilis-network/.../state_file.rs`, around line 288).
- **Doc tension.** The engine README says "no server in the middle." CHANGELOG 0.12.0 says "The relay carries payload when `relay` is in `--lookup`." The org relay replaced an older one in commit `d5e3c9e` ("replace the retired swarm relay with relay.agent-habilis.com").
- **Unused dependency.** `slot-template` is declared at `crates/agent-gossip/Cargo.toml:52` with no `slot_template` reference under `src/`. I did not check tests or `build.rs`.
- **Wasm client untested in CI.** Nothing in `.github/` builds it. Open issue #2 says a native peer cannot message a browser peer, and the error claims the failure is transient.

Open issues at observation time, titles only, not read in full: #2 (native to browser messaging), #28 (join with a live nickname should fail), #29 (rejoin after the daemon dies), #37 (stuck-task detection), #40 (`gossip-join` drops `--nickname`), #42 (two tests fail under host load), #44 (peer's model stale after a model change).

## Observations for the owner

- **At least six names in under three months.** The project went from `swarm` to `ahs`, `ahsw`, `agent-gossip`, `agent-mesh`, `agent-square`, and back to `agent-gossip`. The bee prefix survived, since commit `d1eab75` (2026-06-28) says "keep 🐝 swarm prefix."
- **Two runtimes, two repos.** The daemon and protocol are in `habilis-network`. The CLI, skills, and the Stop hook are here. The MCP path has no daemon (earlier survey).
- **Pinning by rev.** This app and the browser client pin engine rev `795c4f8`. The workspace `Cargo.toml` says `agent-share` pins the same rev too, which I did not verify. The workspace comment says the engine change is "push-then-bump." The `Cargo.toml` comment asks that agreement be checked by hand: "so every consumer can be checked for agreement instead of assumed to agree."
- **Push depends on the host.** Claude Code gets the Stop hook and push bells. Codex and Pi get different wake paths. The design says so in `receive-loop.md`.
- **Armed state is an OS lock.** `cli/bell.rs` keeps the bell's state in an exclusive file lock, not in daemon memory, by design. Its doc comment gives the reason.
- **July narrowing.** Many removals in July cut the surface toward JSON-only agent use: the pipe, mount, port, sh, and file subcommands, the interactive UI, the spool mirror, and directed-over-gossip. The changelog gives no single rationale for the set.
- **Transport churn.** The QUIC keep-alive override was added and then reverted (`69ca1c2`). The iroh dependency was dropped (`50bdc88`), and the engine moved from fofoca to habilis-network.

## Not read

- **habilis-network:** `event_loop.rs`, `gossip/`, `lookup/`, `protocol/`, `node.rs`, `setup.rs`, `timers.rs`, `heal.rs`, `beacon_arm.rs`, `util/` (`mesh_runtime_dir`). `state_file.rs` and `ipc.rs` only in part. The IPC frame format. `shutdown.rs` outside the owner and signal sections. The engine's full history.
- **agent-gossip source:** `cli/session.rs` `owned_sessions` and `discover` bodies, `cli/doctor.rs`, `cli/plug.rs` install body, `cli/agent.rs` skill generation outside the test regions, `a2a/` (except the earlier survey's cites), `bridge/`, `api/inproc.rs`, `output/`.
- **Wasm client:** `driver.rs`, `wire.rs`, and the full `lib.rs`. Not built, not run.
- **Skills:** all of `skills/` except `shared/bell-hook.yaml`, `shared/daemon-session.md`, `shared/receive-loop.md`, and `shared/bell-guard.md`.
- **Workflows:** `release.yml` past line 160, all of `ci.yml`, all of `auto-release.yml` past line 60. No workflow run logs.
- **Packaging:** formula sha256 values, `agent-jail.rb` in the tap, npm registry.
- **Sibling repos:** `agent-share` beyond its README and the pin comments. No `fofoca` or `mallorca` repo exists under the org (404), so none was read.
- **Releases and issues:** no release notes older than 0.4.4 were read. v0.2.0 has a tag but no GitHub release. Issue bodies were not read; only titles and states.
- **Tests and runtime:** no test or build was run. The harness side of the Stop hook and the bell wake was not traced. The MCP path is covered by the earlier survey and was not re-read.
