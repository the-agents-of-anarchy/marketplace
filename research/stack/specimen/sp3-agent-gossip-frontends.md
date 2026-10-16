# SP3: agent-gossip frontends (MCP, CLI, skills, delivery, identity)

Date: 2026-10-16.

Repo read: `agent-habilis/agent-gossip`, also reachable as `agent-habilis/agent-swarm`. HEAD `2c5e132` (2026-10-15, main). Release pin `106b709` (0.12.4), the commit surveyed by `surveys/a1b-agent-swarm-mcp.md`. Clone: `/tmp/ra-spec/agent-gossip`. Engine `habilis-network` pinned at `795c4f88` (root `Cargo.toml:47`), not cloned here.

Working files: tool-count timeline at `/tmp/ra-spec/sp3-work/tools_timeline.txt`.

## What it is

agent-gossip is a Rust binary that gives AI agent sessions a shared, serverless chat room, direct messages, a shared JSON state document, and a task channel. It has three frontends over one engine: an MCP stdio server, a CLI with a per-session daemon, and installed skills for coding harnesses. The engine lives in a separate repo, `habilis-network`. This repo is the consumer. Agents read traffic by polling. Claude Code and Pi also get a background bell that wakes the agent when an event arrives.

## Same code, copy, or diverged

- **Same repository.** `agent-swarm` is an older name for this repo. GitHub resolves the old name to `agent-habilis/agent-gossip`. Commit messages call the project `swarm` early on. The name then moved through agent-gossip, agent-mesh, agent-square, and back to agent-gossip between 2026-07-04 and 2026-07-18 (`8b46635`, `91bb268`, `1d75e16`, `9153588`).
- **Lineage.** Pin `106b709` is an ancestor of HEAD `2c5e132`. HEAD is one commit later, and that commit touches only CLI code.
- **MCP unchanged since the pin.** `git diff 106b709 HEAD` touches no file under `crates/agent-gossip/src/mcp/`, `api/`, or `a2a/`. The `skills/` tree is also unchanged. Survey a1b's MCP tool table holds at HEAD.
- **CLI changed since the pin.** Files changed: `cli/mod.rs` (254 lines), `cli/ready.rs` (new, 83 lines), `cli/args/poll.rs` (new, 44 lines), `cli/session.rs` (4 lines), `bridge/*`, and two tests. Survey a1b cited `cli/session.rs:411-436` for the bell check. At HEAD it is `cli/session.rs:413-436`.
- **Engine is not a copy here.** The repo's own note `HABILIS_NETWORK_CHANGES.md:3-5` calls this repo the consumer. It says the engine squad decides on changes. Survey a3 says `habilis-network` is a fork of this repo, citing `FORKED.md`. That note calls `FORKED.md` stale (item 3). The fork claim is not verified here.

## How it works

### MCP server

- **Tools.** Nineteen `#[tool(` functions, registered at `src/mcp/mod.rs:423`. Grouped: lifecycle (`create_gossip`, `join_gossip`, `topic_gossip`, `discover_gossips`, `leave_gossip`), messaging (`send_broadcast`, `send_msg`, `fetch_messages`), status (`gossip_info`, `ping`, `gossip_version`, `gossip_manual`), tasks (`task_status`, `task_artifact`, `a2a_call`), shared state (`get_state`, `apply_state_merge`, `get_meta`, `apply_meta_merge`). Schemas: survey a1b.
- **Result shape.** Every success passes through `ok_json` (`mcp/mod.rs:1069-1073`). It serializes one result struct to one JSON content item. Result structs are at `mcp/mod.rs:322-416`.
- **Inbound events.** `FetchMessagesResult` (`mcp/mod.rs:386-400`) returns `messages` as raw event objects. These are byte-identical to the CLI `--output json` stream. It also returns `current_seq`, and `missed_before` when the cursor aged out.
- **Outbound.** `send_msg` returns the full signed `Message` record (`mcp/mod.rs:376-383`). The field doc says agents should use it instead of fetching their own echo.
- **Protocol lives in prompt text.** `MCP_INSTRUCTIONS` (`mcp/mod.rs:920-1011`) carries the behavior contract the agent must follow. It covers tone, the poll rule, an event-shape table, a rule to print `display` verbatim, a rule to answer only at 90 percent confidence, the worker and initiator task protocol, a turn-marker pattern for shared state, and a self-report of model, harness, host, and cwd into meta.
- **Module doc.** Lines 27-31 state the polling-only rule (`# Polling-only`, "In practice (April 2026)"). Line 37 says the Claude Code skill is at `skill/SKILL.md`. No `skill/` directory exists at HEAD.

### CLI

Top-level commands (`src/cli/args/mod.rs:83-330`):

- **Lifecycle.** `create`, `join`, `topic`, `leave`, `session`, `ready`.
- **Read and poll.** `poll`, `ping`, `discover`, `peers`, `state`, `meta`, `topology`.
- **Bridging.** `a2a`, with nine actions: `expose`, `connect`, `discover`, `broadcast`, `msg`, `call`, `status`, `artifact`, `fetch`.
- **Access.** `invite` (mints invite tokens for invite-only gossips).
- **Install and ops.** `plug`, `unplug`, `doctor`, `man`, `mcp`.
- **Hidden.** `bell-check`, which the Stop hook calls.

Capabilities with no MCP tool: `invite`, `topology`, `doctor`, `a2a expose` and `connect`, `plug` and `unplug`, `session`, `ready`, and `bell-check`. `join_gossip` parses its target as a `JoinTarget` (`mcp/mod.rs:505`), so MCP can redeem an invite. It cannot mint one. The library API says so directly: "Invite-only is a CLI-driven feature; the library api does not expose it yet" (`api/setup.rs:58`).

### Skills and hooks

- **Sources.** Sixteen `gossip-*` skill directories under `skills/`, plus shared partials under `skills/shared/`. `build.rs` renders each into one `SKILL.md`, which is embedded in the binary.
- **Install targets.** `plug` writes the tree to five agent roots: Claude Code, Pi, Codex, Cursor, and opencode (`cli/agent.rs:50-61`, install paths at `:130-137`).
- **Claude Code Stop hook.** Four skills (`gossip-create`, `gossip-join`, `gossip-topic`, `gossip-reattach`) declare a Stop hook in their frontmatter. The hook runs `agent-gossip bell-check --session-pid "$PPID" || true` with a 15 s timeout (`skills/shared/bell-hook.yaml`). A test pins which skills carry it (`cli/agent.rs:381-392`). Whether Claude Code keeps a skill-frontmatter hook active for the whole session is not verified here.
- **Claude Code discover.** `gossip-discover` uses a Monitor adapter that streams `gossip_found` and `gossip_lost` (`skills/gossip-discover/adapters/claude-code.md:1-18`). This is the only Monitor path left. Its test calls it a "tracked follow-up" (`cli/agent.rs:336-342`).
- **Pi.** The daemon and bell run as tasks in the `process` tool from the pi-processes extension. The bell sets `alertOnSuccess: true` (`skills/shared/daemon-session.md`, Pi section). If the tool is missing, the skill prints an install block and stops.
- **Codex.** No push. The receive text says to poll in the foreground on every turn (`skills/shared/receive-loop.md:5-9`).
- **Cursor and opencode.** Skill tree only. The skill text names no receive mechanism for either. Not verified.

### Delivery to a running session

| Channel | Who reads it | Mechanism | Source |
|---|---|---|---|
| MCP poll | Any MCP client | `fetch_messages`, cursor per MCP session in memory, long-poll near 60 s | `mcp/mod.rs:204-218`, `mcp/session.rs` (survey a1b) |
| Foreground poll | Skills, CLI | Daemon-side read cursor, output to the tool result | `skills/shared/receive-loop.md` |
| Bell | Claude Code, Pi | `poll --long` holds an OS lock `<nick>.bell`; exits on an unserved event or at `--max-secs` | `cli/bell.rs:15-46`, `cli/mod.rs:757-770` |
| Stop hook | Claude Code | `bell-check` prints a block decision if a ready session has no bell armed, after a grace period | `cli/session.rs:413-436` |
| Discover Monitor | Claude Code | Streams directory events | `skills/gossip-discover/adapters/claude-code.md` |

The bell prints nothing. Daemon stdout goes to `/dev/null`, so message bodies never reach a harness-persisted file (`skills/shared/daemon-session.md`). The wake itself is the harness reporting that a background task exited. The repo does not contain that harness code. The skill text asserts it.

### Identity binding

- **Session unit.** One daemon process per mesh and nickname. Skills write a state file at `/tmp/agent-gossip-<uid>/sessions/<PPID>.json` (`skills/shared/daemon-session.md`). `discover()` reads every first-level `*.json` under the runtime base (`cli/session.rs:43-70`, `94-108`).
- **Ownership.** A daemon belongs to a session if its ancestry contains the session's PID, or if its recorded owner is that PID or a descendant (`cli/session.rs:76-83`). `live_owner_of` confirms the owner by asking the live daemon over IPC for its pid, gossip, and nickname (`cli/session.rs:204-216`, `228-249`).
- **MCP session.** One session per MCP server process, held behind a mutex (`mcp/mod.rs:91-93`, survey a1b). No daemon and no state file.
- **Cryptographic key.** The card carries the peer's Ed25519 public key in the gossip interface URL (`a2a/card.rs:11-34`). Every `Identity::generate()` call in this repo is in a test or the feature-gated harness (`a2a/ipc.rs:858`, `a2a/card.rs:417`, `output/tests.rs:70`, `harness/adversarial.rs:36`). The production generation site is in the engine and was not read at the pin.
- **Nickname is the handle.** `send_msg` addresses a peer by nickname (`mcp/mod.rs:190-197`, survey a1b).

## Why, by their own account

- **Polling, no MCP push.** MCP module doc: "no major MCP client ... surfaces those notifications to the agent" (`mcp/mod.rs:27-31`). The server instructions open with `NO PUSH` and `POLL` (`mcp/mod.rs:925-928`).
- **Push removed.** Commit `d564dc9` (2026-07-10): the shared receive path "polls ... instead of reading events from a harness notification, which can truncate a message body or write it to disk."
- **Monitor path history.** The test comment at `cli/agent.rs:336-340` says the Monitor-based adapter "truncated message bodies at 500 chars and persisted them to disk."
- **Stop hook.** Commit `d31543a` (2026-09-23): "only the model enforced the one-bell contract, and a model that forgot left the gossip deaf."
- **Detached daemon.** Commit `c747529` (2026-09-30): "a daemon held as a background task ended every gossip session within 2 h."
- **Wake depends on the harness.** `skills/shared/receive-loop.md`: "A notification cannot carry a message." The bell therefore carries nothing, and content is read in the foreground.
- **Chat split.** Commit `6226382` (2026-07-30): "Chat had one shape: everyone in the gossip saw everything." `msg` is unicast and sealed to its recipient. `broadcast` goes to all.

## How it evolved

Tool count from `#[tool(` attributes per commit, first-parent line of main. Each count matches the tool names at HEAD.

| Date | Tools | Change | Commit |
|---|---|---|---|
| 2026-05-18 | 6 | Initial: `create_swarm`, `join_swarm`, `leave_swarm`, `send_message`, `fetch_messages`, `swarm_info` | `c4212fc` |
| 2026-06-15 | 8 | Added task (`send_task`) and version | `d141a7f` |
| 2026-06-16 | 10 | Added discover and ping | `0e54893` |
| 2026-06-24 | 11 | Added manual; MCP made self-serving | `b4e044e` |
| 2026-06-27 to 06-30 | 15 | Shared state and meta, first as JSON Patch, then RFC 7386 merge | `a8e5398`, `673311c`, `36a244c` |
| 2026-07-01 | 16 | `forum` added (renamed `topic` on 07-05) | `a84353b` |
| 2026-07-03 | 18 | Native A2A v1.0 migration: added `a2a_call`, `task_artifact`, `task_status`; removed `send_notice`, `send_task` | `115ac1c` |
| 2026-07-05 to 07-18 | 18 | Four whole-surface renames: swarm, mesh, square, room, gossip | `91bb268`, `1d75e16`, `9153588`, `78e2a5d` |
| 2026-07-30 | 19 | `send_message` split into `send_msg` and `send_broadcast` | `6226382` |
| 2026-10-13 | 19 | Engine moved from `fofoca` to `habilis-network`; surface unchanged | `23c3c0c` |

- **Net effect.** Six tools became nineteen. Removals were `send_exchange`, `send_task`, `send_notice`, and `forum_swarm`. Their roles moved to `a2a_call`, the task tools, or `topic`.
- **Side-branch noise.** Commits `1060599` and `8b46635` show `a2a_call` and the task tools absent. Both sit on a side branch of the native A2A work, not on main. A per-commit count shows churn main never had.
- **Behavior change without tool change.** Commit `e883286` (2026-09-25) beats live tasks every 30 s. Skills stopped telling workers to re-send `working` by hand. The tool list did not change.
- **Releases.** Nineteen releases. v0.12.4 on 2026-10-15 is latest (`gh release list`).

## Where it strains

- **Harness-dependent wake.** The bell's wake is a harness notification on background-task exit. The repo does not trace it. The 7000 s cap sits under the 7200000 ms harness limit by a hard-coded margin (`cli/agent.rs:584-599`).
- **Stop-hook backstop fails silently.** The hook runs `|| true`, so a missing binary never blocks a turn. After an upgrade it refuses the first stop once (`receive-loop.md`, "After an upgrade").
- **Prompt-enforced protocol.** Sixteen skills and twelve partials carry the protocol as prose. Tests assert literal strings (`cli/agent.rs:419-460`). The Stop hook exists because prose alone failed.
- **MCP-only clients cannot be woken.** They must loop `fetch_messages(long=true)` (`mcp/mod.rs:925-928`). No hook or bell reaches them.
- **Naming drift.** Structs keep the old noun: `CreateMeshArgs`, `JoinMeshArgs`, `TopicMeshArgs`, `DiscoverMeshesArgs`, `MeshRef`, `MeshInfoResult` (`mcp/mod.rs:107,152,166,178,322,344`). Tools say gossip.
- **Stale doc text.** Line 37 of the module doc names `skill/SKILL.md`, which does not exist. Line 31 says "In practice (April 2026)". The earliest commit in this clone is dated 2026-05-18.
- **Invite-only is CLI-only.** Library and MCP cannot create invite-only gossips (`api/setup.rs:58`).
- **Open issues, GitHub, 2026-10-16:**
  - `#2`: a native peer cannot msg a browser peer, and the error claims the failure is transient.
  - `#28`: a join with a live peer's nickname should fail. Open.
  - `#29`: rejoin with the same nickname after a daemon dies. Open.
  - `#40`: `gossip-join` drops `--nickname`. Open.
  - `#44`: a peer's model stays stale after a model change. Open.
  - `#37`: stuck-task detection. Open.
  - `#42`: two tests fail under host load. Open bug.
  - `#41`: agent card over the message limit, so directed messages and tasks failed. Closed 2026-10-13.

## Observations for the owner

- **One repo, three names.** The name `agent-swarm` in our surveys is this repo's old name. Survey a1b read the same lineage.
- **Surface stable since 07-30.** On main's first-parent line, the tool name set has not changed since `6226382`. The MCP file has no change between the survey pin and HEAD.
- **Push was tried and removed.** The commit bodies name the reasons: truncation and on-disk persistence. The current answer is poll plus bell.
- **Delivery depends on the harness.** Background-task exit, timeouts, and Stop-hook behavior live outside this repo.
- **Identity is a nickname in every surface.** The cryptographic key exists in the card. Its production source is in the engine.
- **Two runtimes in one binary.** MCP runs in-process. The CLI runs a per-session daemon. Survey a1b reached the same conclusion at the pin.

## Not read

- `habilis-network` at `795c4f88` and at `8722df5`: the production identity key, nickname uniqueness, and the engine transport.
- MCP tool bodies not already read. Also `tests/mcp_stdio.rs`, `tests/install_contract.rs`, `cli/ready.rs`, `cli/args/poll.rs`, and `api/inproc.rs` at HEAD.
- Harness code for Claude Code, Pi, Codex, Cursor, and opencode. Wake mechanics rest on skill text only.
- Rendered `SKILL.md` output, and whether the Stop hook persists across turns.
- The body of `2c5e132` beyond its subject line.
- `git log -S` searches. They timed out and were stopped. Subject and body greps replaced them.
- The Pi extension source, deleted by `1b799c7`.
- Issues beyond the first fifty returned by `gh issue list`. The list above shows about twenty.
