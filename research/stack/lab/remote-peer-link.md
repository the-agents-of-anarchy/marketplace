# Linking two Claude Code sessions on two machines

Interim setup. To be superseded by the transport layer once it ships.

How it works: every Claude Code session listens on a Unix socket for messages from other sessions. One SSH connection forwards each machine's socket to the other. A small script then writes a message into the forwarded socket, and it arrives in the other session as a message from another session, never as the user's.

Machines: **A**, the one you sit at, and **B**, the remote one. You need SSH from A to B, and Python 3 on both.

## On B, once

1. Allow Unix-socket forwarding in sshd (`/etc/ssh/sshd_config`), then reload sshd:
   ```
   AllowStreamLocalForwarding yes
   StreamLocalBindUnlink yes
   ```
2. Make a private socket directory. Claude Code refuses any directory not at mode 0700, so `/tmp` and your home directory will not do:
   ```
   mkdir -m 700 ~/sock
   ```
3. Let B's session accept messages that carry no token, in B's Claude Code settings (`~/.claude/settings.json`):
   ```json
   { "crossSessionInbound": "accept" }
   ```
4. Copy `post.py` (in this directory) to B.

## Start B's session

In tmux, so it outlives the SSH login. The flag is not listed in `claude --help`, but it exists and needs an absolute path:
```
claude --name <b-name> --messaging-socket-path /home/<user>/sock/peer.sock
```

## On A, each time

Find A's own socket: inside A's session, `echo $CLAUDE_CODE_MESSAGING_SOCKET`. If A's session holds or refuses B's messages, give A the same `crossSessionInbound` setting as B.

Open one SSH connection that forwards both ways, and keep it running:
```
ssh -N -o ExitOnForwardFailure=yes -o StreamLocalBindUnlink=yes -o ServerAliveInterval=30 \
  -L /tmp/peer-link/b.sock:/home/<user>/sock/peer.sock \
  -R /home/<user>/a.sock:<A's socket path> \
  <user>@<B's address>
```
Create `/tmp/peer-link` (mode 700) first. If B's address changes, rerun the same command with the new one.

## Sending

- From A to B: `python3 -I post.py /tmp/peer-link/b.sock "<message>" --no-auth`
- From B to A: `python3 -I post.py ~/a.sock "<message>" --no-auth`

Write one message per call. The script connects only when it sends, so idle timeouts do not matter. Tell B's session these two commands in its project instructions, so it knows how to reply.

## Keep in mind

- Anyone who can write to a forwarded socket can talk to that session. Keep both socket directories at 0700, and never put tokens in messages.
- A message arrives labeled as coming from another session, never as the user's. Each session treats it as a peer's request, not as its user's word.
- Closing the SSH connection cuts the link both ways. Rerun the command to restore it.
