# Lab: posting between two Claude Code sessions on two machines

Status 2026-10-20: the local half is verified; the server does not exist yet.

## Protocol of the cross-session messaging socket (verified)
Source: Claude Code 2.1.303's own debug help text, read from the binary (`strings`, around the `[uds-messaging] Inject messages` message):
```
{ echo '{"type":"auth","token":"'"$CLAUDE_CODE_MESSAGING_TOKEN"'"}'; echo '{"type":"user","message":{"role":"user","content":"hello"}}'; } | socat - UNIX-CONNECT:<socket>
```
The flag `--messaging-socket-path <path>` is unlisted: Claude Code 2.1.304 on the lab server (Linux) omits it from `claude --help`, while its binary carries it with the usage `--messaging-socket-path <path>` and the errors "must be an absolute path" and "was given an empty value" (read with `strings`, 2026-10-20).

The same text says "Connect when the data is ready" (the socket closes an idle connection after a short time) and names the flag `--messaging-socket-path` (choose the socket path at launch).

Loopback test, 2026-10-20 (`/tmp/ra-lab/post.py`, Python, no shell): an auth line with this session's own token, then one user-message line, posted to this session's socket `/tmp/cc-socks/8705.sock`. Result: delivered at once into this session, wrapped by the harness as "Another Claude session sent a message ... not typed by your user" with no `from=` address. So a script holding a session's token can post into it, and the harness labels the text as a peer's, never as the user's.

## Plan for two machines
- Server: one Hetzner instance (cheapest type from the live list), Ubuntu, cloud-init installs build tools, tmux, and Claude Code; firewall allows SSH, HTTP(S), UDP.
- Remote session: started in tmux with `--messaging-socket-path /tmp/lab.sock` (fixed path), named; on its first turn it writes its own `CLAUDE_CODE_MESSAGING_TOKEN` to a 0600 file.
- One SSH connection forwards both sockets (OpenSSH forwards Unix sockets; `StreamLocalBindUnlink yes` on both ends):
  - local to remote: `-L /tmp/ra-lab/remote.sock:/tmp/lab.sock`
  - remote to local: `-R /tmp/ra-home.sock:<this session's socket>`
- Tokens move as files over SSH, never through the conversation: the remote token is copied to `/tmp/ra-lab/remote.token` (0600); this session's token to `/tmp/ra-home.token` (0600) on the server.
- Posting: `python3 -I post.py <socket> "<text>" --token-file <file>`, on either side.
- Teardown: kill the SSH forward, stop the remote session, delete the server and firewall.

## Unknowns before the server exists
1. Whether Claude Code's login on a headless server can be completed by the owner only opening a link, or needs a code pasted back (research/stack/lab/claude-code-remote.md answers from the docs).
2. Whether the remote harness labels a forwarded message the same way (expected: yes, same binary).
3. How long the socket keeps an idle connection open (the help text's "ms is closed"); `post.py` connects only when the data is ready, so this should not matter.
