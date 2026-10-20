---
name: run-hetzner-lab
description: >
  Run the Hetzner Cloud lab for estafette from creation to deletion, each resource under its own deadline and an hourly check.
  "create a lab server", "hetzner", "hcloud", "set up the server", "a second machine", "extend the deadline", "tear down the lab", "delete the server", "lab backstop", "what runs on hetzner", or any request to create, check, extend, or delete a Hetzner Cloud resource.
---

<guard-the-tokens>
Work through the `hcloud` command under its context `estafette-lab`, the named credential set whose token lives in `~/.config/hcloud/cli.toml`; never read that file.

Keep every token out of the conversation, the Hetzner token and a Claude Code messaging token alike; never print one.

Move a messaging token between machines as a file with permissions 0600 over SSH; never move one another way.
</guard-the-tokens>

<keep-the-backstop-running>
Count as a lab resource every server, primary IP address, firewall, and SSH key in the Hetzner project; never leave one uncounted.

Confirm before each creation that the backstop job is loaded with `launchctl print gui/501/com.ryzhakar.estafette-lab-control`, the backstop job being the launchd job on this Mac that checks every lab resource each hour and deletes those past their deadline, the moment a lab resource's `expires` label names; never create a lab resource while the backstop job is absent.

Install the backstop job when absent: copy this skill's `lab-control.py` into `~/.local/share/estafette-lab/`, copy its `com.ryzhakar.estafette-lab-control.plist` into `~/Library/LaunchAgents/`, and run `launchctl bootstrap gui/501 ~/Library/LaunchAgents/com.ryzhakar.estafette-lab-control.plist`; never run the backstop job from this skill's directory.

Copy `lab-control.py` into `~/.local/share/estafette-lab/` again whenever this skill's copy changes; never let the two differ.

Read the backstop job's log at `~/.local/state/estafette-lab/control.log`, one line per lab resource per run; never take the backstop job as working without a line from its last hour.

Remove the backstop job on the owner's word with `launchctl bootout gui/501/com.ryzhakar.estafette-lab-control` and the deletion of its plist; never remove it while a lab resource exists.
</keep-the-backstop-running>

<create-on-the-owners-go>
Create a lab resource on the owner's go for it; never create one on inference.

Choose a server type and location from the live API, where `hcloud server-type describe <type> -o json` lists each location with `available`; never choose from Hetzner's web pages.

Use the type, location, and image the owner approved for this server; never substitute another.
</create-on-the-owners-go>

<give-each-lab-resource-its-deadline>
Set each lab resource's deadline 24 hours after its creation; never create one without a deadline.

Set the deadline at creation with `--label owner=resident-anarchist --label expires=<unix seconds>`, where `date -v+24H +%s` prints the unix seconds 24 hours ahead; never let a lab resource run unlabeled.

Label a lab resource whose creation took no labels at once with `python3 -I lab-control.py label <kind> <id>`, kind being `server`, `primary-ip`, `firewall`, or `ssh-key`; never defer its label.
</give-each-lab-resource-its-deadline>

<create-the-server-from-this-skills-setup>
Upload the SSH key when `hcloud ssh-key list` lacks `estafette-lab`, with `hcloud ssh-key create --name estafette-lab --public-key-from-file ~/.ssh/estafette_lab.pub` and its deadline labels; never upload another key.

Create the firewall from this skill's `firewall-rules.json` with `hcloud firewall create --name <name> --rules-file firewall-rules.json` and its deadline labels; never open more than its four rules, inbound TCP 22, 80, and 443 and all UDP.

Write the server's setup file with `python3 -I fill-setup.py <output path>`, which fills the public half of `~/.ssh/estafette_lab` into this skill's `cloud-init.template.yaml`; never edit the template for one server.

Keep in the template, for every server, the user `lab` without sudo, root by key only, Unix-socket forwarding in sshd, mosh for the owner's terminal, uv and just in `/usr/local/bin`, and for `lab` the Rust stable toolchain with the default profile plus `rust-src` and `rust-analyzer`, the Rust version estafette pins in its `rust-toolchain.toml`, cargo-binstall, and Claude Code; never drop one of them.

Create the server with `hcloud server create --name <name> --type <type> --image <image> --location <location> --ssh-key estafette-lab --firewall <firewall> --user-data-from-file <setup file>` and its deadline labels; never create it without the setup file.

Label the server's two primary IP addresses at once, finding them with `hcloud primary-ip list`; never leave them unlabeled.
</create-the-server-from-this-skills-setup>

<bound-each-waiting-step>
Set a one-shot wake by the `check-back` skill at the latest moment each waiting step should end, the setup's run, an install, or a login; never leave a waiting step unbounded.

Reach the server with `ssh -i ~/.ssh/estafette_lab -o IdentitiesOnly=yes -o UserKnownHostsFile=~/.ssh/known_hosts_estafette_lab -o StrictHostKeyChecking=accept-new root@<IPv4>`, or `lab@<IPv4>` as the session's user; never log in with a password.

Take the setup as finished when `cloud-init status --long` reads `done` with no errors and `/var/lib/lab-setup-done` exists; never take it as finished from the server's running state.

Check the tools after the setup with `uv --version` and `just --version`, and as `lab` with `rustc --version`, `cargo clippy --version`, `rust-analyzer --version`, `cargo binstall -V`, and `claude --version`; never report a tool installed without its printed version.
</bound-each-waiting-step>

<extend-a-deadline-while-work-runs>
Extend a deadline on the owner's word, or while lab work on that lab resource is running, with `python3 -I lab-control.py extend <kind> <id> <hours>`; never extend one for an idle lab resource.
</extend-a-deadline-while-work-runs>

<tear-down-in-order>
Delete the server first, then its firewall, then any primary IP address its deletion left, then the SSH key once no server needs it; never delete a firewall a server still holds.

Confirm a teardown with `hcloud server list`, `hcloud firewall list`, `hcloud primary-ip list`, and `hcloud ssh-key list`; never report a lab resource deleted without a list that lacks it.
</tear-down-in-order>

<record-every-change>
Write each creation, extension, and deletion of a lab resource into the journal through the `event-capture` skill; never leave one unwritten.
</record-every-change>
