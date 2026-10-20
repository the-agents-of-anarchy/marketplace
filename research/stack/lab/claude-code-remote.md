# Lab: Claude Code on a headless server, auth and the cross-session socket

Author: peer lab-claude-code (claude-code-guide agent), returned as a message to resident-anarchist at 2026-10-20 19:47 +0300; the agent could not write files. Saved verbatim below by resident-anarchist. Peer content: unverified except where marked.

## Checked by resident-anarchist (2026-10-20 19:48 +0300)
Raw pages fetched from https://code.claude.com/docs/en/<page>.md into /tmp/ra-docs/ and grepped:
- authentication.md:17 — the `Paste code here if prompted` sentence and the SSH condition: verbatim.
- authentication.md:284 and :306 — setup-token prints the token, saves it nowhere, can only make model requests, no Remote Control: verbatim.
- cross-session-messaging.md:140-141 — same machine over a per-session socket; another machine through Anthropic servers over Remote Control: verbatim.
- cross-session-messaging.md:251 and :260-262 — the auth line and the own-child rule: verbatim.
- permission-modes.md:701 and :711 — the acceptance dialog writes `skipDangerousModePermissionPrompt: true` to ~/.claude/settings.json; bypass refused as root or under sudo: verbatim.

Correction to section 4 below. Lines 261-262 say Linux verifies an own child by process evidence, and name the token as the fallback only on macOS after the poster exits, in a container where Claude Code is PID 1, and on native Windows. On the Linux server, a post arriving through sshd carries sshd as its process evidence, so "the token alone establishes it" does not follow there. Inference, to test live: the server session holds a forwarded post unless it sets `crossSessionInbound: accept`. On the Mac, the forwarding ssh client is this session's own descendant and runs for the whole connection, so a post arriving through it may pass as own-child by process evidence; also to test live.

Answered by earlier evidence: the message line after the auth line, and the label the model sees, are verified in research/stack/lab/socket-bridge.md (the binary's own help text, and a loopback post that arrived marked as another session's message).

## The agent's report, verbatim

Sources (raw markdown from https://code.claude.com/docs/en/<page>.md, fetched 2026-10-20):
- Setup: https://code.claude.com/docs/en/setup
- Authentication: https://code.claude.com/docs/en/authentication
- Troubleshoot install and login: https://code.claude.com/docs/en/troubleshoot-install
- CLI reference: https://code.claude.com/docs/en/cli-reference
- Headless: https://code.claude.com/docs/en/headless
- Agent view: https://code.claude.com/docs/en/agent-view
- Permission modes: https://code.claude.com/docs/en/permission-modes
- Cross-session messaging: https://code.claude.com/docs/en/cross-session-messaging
- Environment variables: https://code.claude.com/docs/en/env-vars
- Settings reference: https://code.claude.com/docs/en/settings-reference
- Remote Control: https://code.claude.com/docs/en/remote-control
- Error reference: https://code.claude.com/docs/en/errors

Search-result blog posts disagreed with each other on details; I cite only the official pages.

1. INSTALL ON UBUNTU (x86_64, arm64)
- Recommended native installer (setup, "Native Install (Recommended)", "macOS, Linux, WSL"): curl -fsSL https://claude.ai/install.sh | bash. Then claude --version ("A working installation prints a version number").
- Apt: after adding the signed stable repo, sudo apt install claude-code. Verify key fingerprint 31DDDE24DDFAB679F42D7BD2BAA929FF1A7ECACE first. "Package manager installations do not auto-update through Claude Code."
- npm: npm install -g @anthropic-ai/claude-code (Node.js 22+). "Do NOT use sudo npm install -g".
- Architecture: "Hardware: 4 GB+ RAM, x64 or ARM64 processor"; "Ubuntu 20.04+". npm names linux-x64 and linux-arm64. Not documented: how the native installer picks the architecture, and which architectures the apt repo serves (its deb line has no arch field).

2. AUTHENTICATION ON A HEADLESS SERVER
- /login over SSH: a code must be pasted back. Authentication page: "If your browser shows a login code instead of redirecting back after you sign in, paste it into the terminal at the `Paste code here if prompted` prompt. This happens when the browser can't reach Claude Code's local callback server, which is common in WSL2, SSH sessions, and containers." Troubleshoot page: "When Claude Code runs in WSL2, on a remote machine over SSH, or inside a container, the browser usually opens on a different host and its redirect can't reach Claude Code's local callback server." Fallback: claude auth login, which "reads the pasted code from standard input".
- claude setup-token: "The command opens the same browser authorization flow as `/login`, and the token prints to the terminal after you approve access in the browser. It does not save the token anywhere; copy it and set it as the `CLAUDE_CODE_OAUTH_TOKEN` environment variable wherever you want to authenticate." Limit: "It can only make model requests, so it can't establish Remote Control sessions or fetch claude.ai connectors." Bare mode does not read this variable.
- CLAUDE_CODE_OAUTH_TOKEN: "Use this for CI pipelines and scripts where browser login isn't available." It is precedence 5 of 7, above /login (7).
- ANTHROPIC_API_KEY: no browser step. "In non-interactive mode (`-p`), the key is always used when present." Remote Control: "API keys are not supported."
- Owner-only-a-link: no option is documented as needing nothing beyond opening a link over SSH. /login needs the paste. setup-token over SSH: whether the paste applies is not documented. Closest route: run claude setup-token on the Mac, where the browser can reach a local callback (inference from the stated condition), then copy the printed token to the server's CLAUDE_CODE_OAUTH_TOKEN. The copy is a shell step on the server, and that token cannot do Remote Control.
- Linux credential storage: ~/.claude/.credentials.json, mode 0600. Expiry: "Once the stored login expires and can't be refreshed, each model request fails... until you sign in again." A Remote Control session "stops making progress once the credential expires and can't recover until you sign in again." Lifetime of a /login credential: not stated.
- claude auth status prints authMethod: none, claude.ai, oauth_token, api_key, api_key_helper, or third_party (CLI reference). Use it to confirm claude.ai auth.

3. ALIVE, NON-INTERACTIVE, NO PROMPTS, NAMED
- Plain claude in tmux: "a session started by running `claude` directly is tied to that terminal and ends when it closes, unless you send it to the background" (agent view). It stays alive while its pane process runs.
- claude -p is one-shot: "After Claude finishes its turn and stdin has closed, a `claude -p` run can stay open to wait for background work that Claude started." Whether it still takes messages after its last turn: not documented.
- Background alternative: claude --bg "<prompt>" ("Start the session as a background agent and return immediately"). "Background sessions don't need any terminal open to keep working." But when "unattached for about an hour" the supervisor stops the process; "Pin a session with Ctrl+T to keep its process running." Whether a message wakes a stopped session: not documented.
- Name: claude --name <name> (-n): "Set a display name for the session, shown in `/resume` and the terminal title." /rename changes it mid-session. Peers address the session by that name (cross-session page).
- No prompts: --permission-mode bypassPermissions (same as --dangerously-skip-permissions): "disables permission prompts and safety checks so tool calls execute immediately." Warning: "Only use this mode in isolated environments like containers, VMs, or dev containers without internet access, where Claude Code cannot damage your host system."
- Not as root: "Claude Code refuses to start in `bypassPermissions` mode when running as root or under `sudo`" on Linux and macOS (skipped inside a recognized sandbox).
- Acceptance: the first interactive start shows a dialog; accepting writes skipDangerousModePermissionPrompt: true to ~/.claude/settings.json. "With no acceptance recorded, `claude --bg --permission-mode bypassPermissions` is refused until you accept the dialog in an interactive session."
- defaultMode: "`auto` and `bypassPermissions` don't take effect from project or local settings, so set them in `~/.claude/settings.json` instead." (settings reference). --settings also applies.
- Lighter option: dontAsk with --allowedTools ("Locked-down CI and scripts"). For -p, --permission-prompts none (v2.1.259+).
- Bypass does not switch off messaging holds: "When no `crossSessionInbound` value applies, Claude Code holds an inbound message from another of your sessions for your approval, and delivers without asking only when the sending session identifies itself as also bypassing permission prompts." So set crossSessionInbound to accept on the server session (see 4).
- Do not use --bare: "When you start a session in bare mode, Claude Code doesn't bind the socket, so that session can't receive messages and doesn't appear in the agent list."

4. CROSS-SESSION SOCKET
- Auth line: the docs say a script "can send `{"type":"auth","token":"<token>"}` as the first line of its connection, where `<token>` is the value of `CLAUDE_CODE_MESSAGING_TOKEN`." Optional on macOS, Linux, and WSL 2; required on native Windows. "Claude Code closes a connection that hasn't sent a complete line within 30 seconds."
- Message line after auth: NOT DOCUMENTED. No page shows a message line, names any fields, or says whether the body is JSON or plain text or how it ends. Only rules: "Plain text only: Claude sends only plain text across sessions," and a size cap on "its serialized form", about 1,048,576 characters (error reference).
- Labeling to the model: "When session A messages session B, Claude Code tells B's Claude that the message came from another session, not from you." It receives "the sender's name and a reply address", except one-way cross-machine messages. The exact wrapper text the model sees: NOT DOCUMENTED. The user preview is `› Message from @api-worker: Schema migration finished (ctrl+o to expand)`.
- crossSessionInbound values: "accept" (Claude Code delivers each message to Claude), "hold" (shows a notice, does not deliver; released if an accept later applies), "refuse" (drops each message). Precedence (settings reference): "Claude Code reads managed settings first, then the `--settings` flag, then user settings, and applies the first value found. `refuse` is stricter than `hold`, and `hold` is stricter than `accept`." Unset: decided per message from permission-mode classes. Unrecognized value: treated as hold (refuse in managed settings). Requires v2.1.224.
- Own-child path: "when no `crossSessionInbound` value applies, Claude Code delivers a message it verifies came from the session's own child processes, such as a hook or Bash command posting back to its own session's socket." Verification is by process evidence where available (Linux and WSL 2; macOS only while the poster runs; none in containers running as PID 1 or on native Windows). Otherwise it "verifies a child that sent the session's exported `CLAUDE_CODE_MESSAGING_TOKEN` in the auth line". If neither works, the message is treated like any message asserting no permission class, so a bypassing session holds it for approval.
- Rule for a message presenting the session's own token: with no crossSessionInbound value set, a valid token counts as own-child and is delivered. If any value is set, that value decides.
- Risk for your plan: the docs do not say whether a token sent over a forwarded connection from another machine counts as own-child. Read literally, the token alone establishes it. Treat the token as a credential.
- Discovery: /status shows a "Peer address" row with a "uds:" prefix. The docs show the path there; they do not say /status shows the token.
- Each session exports its own socket and token. "Settings `env` blocks can't set it." (env-vars)

5. SESSIONS ON DIFFERENT MACHINES
- Delivery table: same machine uses a per-session socket "never through Anthropic servers"; "On another of your machines" goes "Through Anthropic servers, arriving over that machine's Remote Control connection"; cloud sessions go through Anthropic servers.
- Remote Control needs a claude.ai login. Cross-session page: "Claude can't find those sessions with an API key or on Amazon Bedrock, Claude Platform on AWS, Google Cloud's Agent Platform, and Microsoft Foundry." setup-token cannot run Remote Control. So with setup-token or an API key, the documented cross-machine route is unavailable.
- Starting a conversation with another machine's session requires v2.1.225.
- SSH socket forwarding: NOT DOCUMENTED, for delivery or for discovery. "A session appears only when it binds an inbox socket" applies to local sessions only.
- Headless fit: "Your local Claude Code session makes outbound HTTPS requests only and never opens inbound ports on your machine." If the terminal closes, "the session goes offline until you bring it back", so run it in tmux.
- Fetching off: CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC or DISABLE_GROWTHBOOK make Remote Control unavailable. Same-machine messaging still works, but "with flag fetching off, same-machine messaging requires Claude Code v2.1.248 or later."
- ListAgents rows: Subagents; Teammates; "Your other local sessions" (only those that bind a socket); cloud sessions (while connected to Remote Control); "Your Remote Control sessions on other machines", labeled Remote Control, which can show offline. Also "can't receive cross-session messages (off in that session)". Command: /list-agents (alias /peers).
- isolatePeerMachines: true makes SendMessage to other machines ask for approval, even in bypassPermissions mode.

NOT DOCUMENTED (summary)
- Message line format after the auth line, and how it ends.
- Model-facing wrapper text for incoming messages.
- Socket forwarding over SSH, for delivery or discovery.
- Whether setup-token over SSH needs the code paste.
- Whether a -p run takes messages after its last turn.
- Whether a message wakes a background session stopped for idleness.
- The callback port for the claude.ai login. Only MCP server OAuth has a fixed-port option (MCP_OAUTH_CALLBACK_PORT).
- Architecture selection in the native installer and the apt repo's architectures.
- Whether /status shows the messaging token.

PLAN IMPLICATIONS
1. The documented cross-machine route is Remote Control via Anthropic's servers, which needs a claude.ai login. It is not setup-token or an API key.
2. Forwarded-socket delivery is outside the docs, and the own-child token rule may treat a forwarded token as own-child. Test before relying on it.
3. Message format is undocumented, so verify with a live test.
