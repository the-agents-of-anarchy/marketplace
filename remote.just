# Lab server on Hetzner: terminal, shell, and the message-socket link.
# Every recipe looks the server's address up by name from the live API at run
# time, so a replaced server or a new address needs no edit here.
# Another server: LAB_SERVER=<name> just remote::<recipe>.

server := env("LAB_SERVER", "estafette-lab")
key := env("LAB_KEY", home_directory() / ".ssh" / "estafette_lab")
known_hosts := home_directory() / ".ssh" / "known_hosts_estafette_lab"
ssh_opts := "-i " + key + " -o IdentitiesOnly=yes -o UserKnownHostsFile=" + known_hosts + " -o StrictHostKeyChecking=accept-new"
sibling_socket := "/tmp/lab.sock"
local_socket := "/tmp/ra-lab/remote.sock"
remote_home_socket := "/home/lab/ra-home.sock"

# List this module's recipes (what bare `just remote` runs)
help:
    @just --list remote

# Print the server's current IPv4 address, from the live API
ip:
    @hcloud server ip {{ server }}

# Open a mosh terminal on the server; extra words run there, e.g. tmux attach -t sibling
mosh user="lab" *command:
    mosh --ssh="ssh {{ ssh_opts }}" {{ user }}@$(hcloud server ip {{ server }}) {{ if command == "" { "" } else { "-- " + command } }}

# Run a command on the server over SSH, stdin passed through; no command opens a shell
ssh user="root" *command:
    ssh {{ ssh_opts }} {{ user }}@$(hcloud server ip {{ server }}) {{ command }}

# Install the sibling session's marketplaces and plugins on the server, from the skill's plugins.sh
plugins:
    ssh {{ ssh_opts }} lab@$(hcloud server ip {{ server }}) 'bash -l -s' < .claude/skills/run-hetzner-lab/plugins.sh

# Hold one SSH connection carrying both message sockets until it drops; pass the sibling's socket path when it differs
forward sibling=sibling_socket home_socket=env("CLAUDE_CODE_MESSAGING_SOCKET", ""):
    test -n "{{ home_socket }}" || { echo "no home socket: run from a Claude Code session, or pass the socket path"; exit 1; }
    mkdir -p "$(dirname {{ local_socket }})"
    ssh {{ ssh_opts }} -N -o ExitOnForwardFailure=yes -o StreamLocalBindUnlink=yes -o ServerAliveInterval=30 -L {{ local_socket }}:{{ sibling }} -R {{ remote_home_socket }}:{{ home_socket }} lab@$(hcloud server ip {{ server }})

# Forget the host key held for the server's current address, once a new server takes the address over
forget-host:
    ssh-keygen -R "$(hcloud server ip {{ server }})" -f {{ known_hosts }}
