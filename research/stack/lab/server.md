# Lab server: state and backstop

Owner rulings, 2026-10-20: server CX23 in Nuremberg, prompts off, non-root; full Claude Code login, socket route tested first (Remote Control is off on the owner's logins); uv, just, and the full Rust toolchain on every server this session initializes; a backstop: a timed check on each step, a 24-hour deletion deadline per resource, every created resource with its own timed control check, run hourly from this Mac; deadlines extended by the owner, or by resident-anarchist while lab work runs, each extension journaled.

## Resources (project estafette-lab)
| Kind | Id | Name | Deadline (UTC) |
|---|---|---|---|
| server | 171412890 | estafette-lab, cx23, nbg1, ubuntu-24.04, IPv4 178.105.88.14 | 2026-10-21 17:33 |
| primary-ip | 156688570 | IPv4, auto-delete with the server | 2026-10-21 17:33 |
| primary-ip | 156688571 | IPv6 2a01:4f8:1c16:4e88::/64, auto-delete | 2026-10-21 17:33 |
| firewall | 11846725 | estafette-lab-fw: tcp 22, 80, 443; udp 1-65535 | 2026-10-21 17:33 |
| ssh-key | 131557923 | estafette-lab (~/.ssh/estafette_lab) | 2026-10-21 16:40 |

## On the server (verified 2026-10-20)
User `lab` without sudo; root by key only. uv 0.13.4 and just 1.59.0 in /usr/local/bin. Rust for `lab`: stable 1.99.1 with the default profile plus rust-src and rust-analyzer, and the estafette pin 1.99.1. Claude Code 2.1.304. sshd allows Unix-socket forwarding with StreamLocalBindUnlink. Not yet done: login, the sibling session, the socket forward.

## Files
The procedure and its files live in the project skill `run-hetzner-lab` (.claude/skills/run-hetzner-lab/): SKILL.md, cloud-init.template.yaml (the setup for every new server), fill-setup.py (fills the key into it), firewall-rules.json (the four inbound rules), lab-control.py (the backstop: `check` hourly, `label` after a creation, `extend`), and the launchd plist. Installed copies: ~/Library/LaunchAgents/com.ryzhakar.estafette-lab-control.plist, running ~/.local/share/estafette-lab/lab-control.py, logging to ~/.local/state/estafette-lab/control.log.

## Backstop, verified
Loaded with `launchctl bootstrap gui/501`; first run on load exited 0 and logged one line per resource. Deletion path: a free throwaway firewall labeled already expired was deleted by a real check, and nothing else was touched. To remove the job: `launchctl bootout gui/501/com.ryzhakar.estafette-lab-control`, then delete the plist.

## Creating a resource from now on
By the skill `run-hetzner-lab`.
