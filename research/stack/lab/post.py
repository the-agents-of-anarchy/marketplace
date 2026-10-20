"""post.py: post one message to a Claude Code cross-session messaging socket.

Protocol, as Claude Code's own debug help text documents it (binary 2.1.303): an
optional auth line {"type":"auth","token":...}, then one line
{"type":"user","message":{"role":"user","content":...}}. The docs make the auth
line optional on macOS and Linux.

usage: python3 -I post.py <socket-path> <text> [--no-auth | --token-env NAME | --token-file PATH]
Default token source: the CLAUDE_CODE_MESSAGING_TOKEN environment variable.
"""
import json
import os
import socket
import sys


def main(argv):
    if len(argv) < 3:
        print(__doc__)
        return 2
    path, text = argv[1], argv[2]
    token = os.environ.get("CLAUDE_CODE_MESSAGING_TOKEN", "")
    if "--token-env" in argv:
        token = os.environ.get(argv[argv.index("--token-env") + 1], "")
    if "--token-file" in argv:
        with open(argv[argv.index("--token-file") + 1]) as f:
            token = f.read().strip()
    lines = [json.dumps({"type": "user", "message": {"role": "user", "content": text}})]
    if "--no-auth" not in argv:
        lines.insert(0, json.dumps({"type": "auth", "token": token}))
    payload = ("\n".join(lines) + "\n").encode()
    s = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    s.settimeout(5)
    s.connect(path)
    s.sendall(payload)
    s.shutdown(socket.SHUT_WR)
    reply = b""
    try:
        while True:
            chunk = s.recv(4096)
            if not chunk:
                break
            reply += chunk
    except socket.timeout:
        pass
    s.close()
    print("sent", len(payload), "bytes; reply:", reply.decode(errors="replace").strip() or "(none)")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
