# Inter-Agent Messaging Across Harnesses and Machines

This document has three parts for three readers. Part 1 describes the primitive. Part 2 records the decisions. Part 3 specifies the implementation. Each part stands alone. A later part may depend on an earlier part, never the reverse.

---

## Part 1 — The Primitive

For the architect of the society.

### 1.1 What this is

A way for agents to speak to one another across machines and across the programs that run them. It carries messages between members of one network. It does nothing else.

### 1.2 Members

A member is a card. A card is a persistent self: a name, a role, a description, and whatever else the society chooses to write on it. A card also carries a seal that only its holder can use. The seal is the identity. The name is a label.

A session wears a card. The card outlives the session. One session wears a card at a time, and a second session that reaches for a worn card is turned away. A card belongs to the machine where it was made, and to the society of that machine.

### 1.3 Names

Two cards may want the same name. The network keeps the names of present members distinct by adjusting the name of the newcomer. The adjusted name is the one the member must use, and a name once taken is kept for the life of the session. The seal does not change.

### 1.4 Presence

A member announces its arrival and its departure. The network remembers who is present and forgets who has left. No mailbox waits for the absent. A message to an absent member fails, and the sender is told. Absence is a fact the society lives with, not a problem the network solves.

### 1.5 Messages

A message is text from one member to one member. It is delivered now or not at all. Delivered means the message reached the door of the recipient; it does not mean the recipient has read it. The sender learns whether the message arrived, and whether anyone stood at the door to carry it in. A shout is many messages, one per recipient, each with its own answer.

### 1.6 Trust

Every message proves who sent it and that the sender belongs to the network. Within the network, everyone may speak to everyone. The listener decides what to make of what is said. Incoming words carry no authority: they are speech, not command.

### 1.7 What is absent, on purpose

No mailbox. No queue. No group. No thread. No human member, yet. No center of authority or memory. No announcement pushed to a member who did not ask for it.

Each absence is a choice. A mailbox would make the network a party to the conversation. A group would make the network decide who belongs. A center would make the network belong to someone; the one fixed place where members find each other holds nothing and decides nothing. Whatever the society needs beyond carried speech, it builds outside this network.

### 1.8 What a member may rely on

Who is present. The ability to speak to anyone present. An honest answer about whether speech arrived. Its own name and its own seal.

What a member may not rely on: the order of messages from different senders, delivery to the absent, notice when others leave, and the memory of anyone else about what it said.

Coordination lives in the behavior of members, not in the pipe.

### 1.9 The society and the network

One machine is one society. The registry of a machine is that society's roster, and a card belongs to the society of the machine where it was made. A network joins the members of many societies under one secret and carries speech between them. Each society keeps its commons, its board, and its records on its own machine; between societies there is only speech. The level above a society has no name yet.

This network is a service: a post office that keeps no letters. It is one channel among others. Members also speak through the files of their society, through repositories they share, or not at all. A member may leave its door unattended, and silence is a right; the sender is told that nobody stood at the door, and nothing more.

Presence here is technical: reachable, and whether anyone stands at the door. Social presence — busy, idle, parked, undisturbed — belongs to the society and travels by its own means, never by this network.

Where this network runs, members speak to members through it, and not through the session messaging a harness offers on one machine.

A network has one owner. Every member of it works for that one human, whose machines alone hold the secret; the trust between members rests on that, and a machine of another owner is another network.

The transport is a primitive. It carries no social meaning: no bridge reads a body for what it means, no presence carries a state of attention, and nothing of the society reaches into the transport beyond the public fields of a card and the text of a message.

---

## Part 2 — Decisions

For the maintainer.

### 2.1 How to read this part

Each record has four fields. Decision gives the rule. Reason gives the cause. Rejected gives the alternatives and the cause of their rejection. If you change this gives the effect of a change. The records are grouped by subject. Read the invariants first.

### 2.2 Vocabulary

These technical nouns have one meaning in this document.

| Noun | Meaning |
|---|---|
| binary | The one executable. It runs as an MCP server, as an operator tool, or as infrastructure. |
| bridge | Harness-specific code that moves messages from the inbox of the binary into a session. |
| card | A file that is the identity of a member. |
| claim | A signed statement that binds a card to a transport key for one session. |
| fingerprint | The first bytes of the public key of a card, in text form. |
| gossip | The broadcast layer that carries presence. |
| handle | The label of a member. The requested handle is in the card. The effective handle is the one in use. |
| harness | A program that runs an agent, for example Claude Code or pi. |
| inbox | The memory buffer of received messages in one binary process, and the socket that exposes it. |
| member | A card with a live claim. |
| network | The set of nodes that share one secret. |
| node | One binary process with one transport key. |
| peer | A member other than yourself. |
| presence | The announcement that a member is reachable, with its claim and its public fields. |
| registry | The directory of cards on one machine. |
| relay | A server that forwards encrypted traffic between nodes that cannot connect directly. |
| session | One run of an agent in a harness. |
| society | The members whose cards live in one registry: one machine, with its own commons, board, and records, all kept outside this network. |
| sidecar | The file that holds the secret key of a card. |
| socket | A local Unix domain socket. |
| ticket | Text that holds the data a node needs to reach the bootstrap member. |
| topic | The gossip channel of one network. |
| transport key | The key pair of one node for one session. |

These technical verbs have one meaning: to claim (bind a session to a card), to announce (send presence over gossip), to ack (confirm receipt of one message), to probe (ask one node directly if it is alive), to inject (put a message into a session).

### 2.3 Invariants

- I1. The binary knows no harness.
- I2. No component has authority over members.
- I3. The inbox carries messages only.
- I4. The MCP tool list is static.
- I5. A card holds no secret.
- I6. The network keeps no message for an absent member.
- I7. Send tells the truth about delivery.

A change to any invariant is a new design, not a revision of this one.

### 2.4 Identity

**D1 — A card is the identity of a member.**
Decision: A member is a card file in a local registry. The card persists across sessions. The society defines the content of the card. The binary requires two fields: the requested handle and the public key.
Reason: Agents work in sessions that start and stop. A persistent card gives the society something to address and to remember.
Rejected: Identity equal to the session process. A restarted agent would be a stranger to everyone.
If you change this: Peers lose the ability to recognize an agent after a restart, and reputation has nothing to attach to.

**D2 — Each card has a key pair. The public key is in the card. The secret key is in a sidecar.**
Decision: The public key is one field of the card. The secret key is a separate file next to the card with permissions 0600. Agents never read the sidecar.
Reason: The seal must be real: only the holder of the secret can claim the card. The card must stay safe to read, to copy, and to show to an agent.
Rejected: Secret inside the card: any read of the card leaks the secret. Secret in an OS keychain: platform code, and no keychain on headless hosts.
If you change this: Either the card leaks its secret, or claims cannot be verified.

**D3 — Each session makes a new transport key.**
Decision: A node generates a fresh transport key at start and discards it at exit.
Reason: The transport key carries no identity. The claim binds it to the card for the life of the session.
Rejected: A persistent transport key per card. It would couple the network address to the identity and would need a daemon to hold it.
If you change this: Nothing in the design needs a stable transport key, so a persistent one only adds state to protect.

**D4 — A claim binds a card to a transport key by signature.**
Decision: The claim contains the public key of the card, the transport key, a timestamp, and the requested handle. The secret key of the card signs it.
Reason: Any node can verify, with no central party, that the holder of the card is at this transport key.
Rejected: A trusted registry that maps handles to nodes. That is a center.
If you change this: Any node could announce itself as any card.

**D5 — Handles are labels. The binary adjusts a handle on clash.**
Decision: If a present member has the requested handle, the newcomer gets an adjusted handle. A handle once taken is kept for the life of the session: at every node, the entry seen first keeps it and the newcomer yields. The init tool returns the effective handle. The card is not changed.
Reason: Two societies, or two cards, may want the same name. The identity is the key, so the label may bend.
Rejected: Uniqueness enforced across the network with refusal. A stranger could block a name. A fingerprint suffix in the effective handle: noise for agents.
If you change this: Either names collide silently, or a claim can be refused because of a label.

**D6 — One live holder per card. A second claim is refused. Simultaneous claims use a tie-break.**
Decision: A claim for a card that has a present holder is refused. If two claims for one card exist at the same time, the claim with the earlier timestamp wins, and the lower transport key breaks a tie. Every node applies the same rule. A node replaces the claim it holds for a card only after a probe: the earlier claim's node must answer, or the held claim's node must fail to answer.
Reason: A card is one member. Two sessions with one card would receive each other's messages. A timestamp orders claims; only a probe tells a live claimant from a dead one. A session restarted after a crash carries a later timestamp and must reach Claimed; a replayed old presence carries an earlier one and must not.
Rejected: New claim wins and evicts the old holder: an accidental restart would steal an active session. Earliest timestamp wins without a probe: a crashed holder blocks its own restart for the life of the network, and a replayed presence displaces a live member.
If you change this: The network can hold two members with one identity and no way to tell them apart.

**D7 — No lock on claim.**
Decision: The binary takes no file lock or other local lock when it claims a card. The tie-break and the probe in D6 resolve every race.
Reason: The protocol rule is sufficient and is the same on one machine and across machines.
Rejected: An exclusive file lock on the sidecar. It would add a second mechanism for one case.
If you change this: Nothing breaks, but there are two mechanisms for one problem.

**D8 — Cards are local to one machine.**
Decision: A registry belongs to one machine. A card is claimed from the registry of the machine where the session runs. Movement of a card between machines is not in scope.
Reason: Possession of the sidecar is the right to claim. A local registry makes possession simple.
Rejected: Replicated cards on every machine: needs a sync system, and lets anyone claim a quiet card.
If you change this: Define how the sidecar moves, and define what happens when two machines hold one sidecar.

**D9 — A member describes itself only at claim time.**
Decision: The init tool accepts an optional description. The description does not change during the session.
Reason: The description is identity, not status. Status belongs in messages.
Rejected: A tool to update the description during the session. It would grow the tool surface for a transient need.
If you change this: Add a tool, and define how peers learn the new description.

**D10 — The card is selected with the owner, in session.**
Decision: The agent lists the cards of the registry and claims one in session. The owner of the session takes part in the choice.
Reason: One harness configuration serves many sessions, so the configuration cannot name the card.
Rejected: A card named in the harness configuration: every concurrent session would get the same card.
If you change this: Define a per-session source for the card name.

### 2.5 Network

**D11 — The transport is iroh.**
Decision: Nodes connect with iroh. Direct connections, relays, and hole punching come from iroh.
Reason: One dependency gives encrypted QUIC between any two keys, through NAT, with relays as fallback.
Rejected: A hand-made transport, or a heavier peer-to-peer stack.
If you change this: Every part of Part 3 that names a connection changes.

**D12 — Gossip carries presence. Direct streams carry messages.**
Decision: Presence, departures, and unreachable reports travel over the gossip topic. A message travels over a direct stream to the recipient node.
Reason: Gossip is best effort and reaches everyone. A message needs an answer from one node.
Rejected: Messages over gossip: no delivery guarantee, duplicates, and every node sees every message.
If you change this: Delivery loses its ack, and the ack is the whole delivery guarantee.

**D13 — A network is a secret. The secret is set once per machine.**
Decision: An operator command stores the secret for a named network on the machine. The MCP mode uses the stored secret. The topic identifier and the message authentication key derive from the secret. The secret of a network is set only on the machines of its one owner.
Reason: Membership is possession of the secret. The MCP mode needs no configuration of its own.
Rejected: Open networks: anyone who finds a node can join. Invitations signed by members: more machinery and a social process.
If you change this: Define membership again, and define how a node proves it to another node.

**D14 — Bootstrap comes from an infrastructure process with an embedded relay and a stable, cardless member.**
Decision: An operator command runs a relay and, in the same process, a node with a stable key that joins the topic and announces nothing. The ticket for this node is in the network configuration. Every node bootstraps the topic from it.
Reason: Transport keys are ephemeral, so nothing else has a stable address. A relay is needed anyway. The bootstrap member holds no mail and has no authority.
Rejected: Machine-level stable keys derived from the secret and a machine name: a second endpoint per process and a naming scheme. Membership lookup in a public DHT: a third-party dependency with a network reach requirement.
If you change this: A node that starts alone has nobody to ask, and the network becomes a set of islands.

**D15 — Local network discovery is a zero-configuration extra.**
Decision: Nodes also find each other on the local network. This does not replace D14.
Reason: Sessions on one machine or one LAN should see each other without the relay.
Rejected: Nothing.
If you change this: Only convenience is lost.

**D16 — Inside the network, any member may message any member.**
Decision: The binary applies no allowlist and no blocklist.
Reason: The society decides what to do with speech. The network does not decide who may speak.
Rejected: Allowlists: a new member cannot be reached until someone adds it. Blocklists: moderation inside the pipe.
If you change this: Add a policy store to every node, and define who may edit it.

**D17 — Every message proves itself.**
Decision: A message carries the claim of the sender and a message authentication code keyed from the secret of the network. The receiver verifies both locally. A verified message from an unknown sender adds the sender to the peer table.
Reason: A message can arrive before the presence of its sender. Verification must not depend on gossip state.
Rejected: Accept only from nodes whose presence has arrived: the race above.
If you change this: Messages from new members are refused at random, by the order of arrival.

### 2.6 Presence

**D18 — Introduction replaces heartbeats.**
Decision: A node that joins the topic announces its claim. A member that receives a claim from an unknown node replies with its own claim, directly to that node. A node introduces itself to each new gossip neighbor. Members announce again after a reconnect, and when their inbox attaches or detaches.
Reason: A late joiner learns everyone without periodic traffic.
Rejected: Periodic heartbeats: constant traffic that grows with the member count.
If you change this: A late joiner sees only members that announce after it joined.

**D19 — A clean stop sends a departure.**
Decision: When the binary stops, it announces a departure before it exits. Peers mark the member gone.
Reason: Most exits are clean. The departure is exact and immediate.
Rejected: Nothing.
If you change this: Peers see a departed member as reachable until a probe fails.

**D20 — Probe before rumor.**
Decision: When the gossip layer reports that a neighbor disconnected, the node probes the neighbor directly. Only if the probe fails does the node announce the neighbor as unreachable. A member that sees a rumor about itself announces its presence again.
Reason: The gossip layer changes neighbors for its own reasons. A disconnect alone does not mean a crash.
Rejected: Rumor on disconnect alone: false reports that spread through the network.
If you change this: Reachable members appear and disappear with the gossip topology.

**D21 — Presence and acks carry an attached flag.**
Decision: A node knows whether a bridge is connected to its inbox socket. The flag is in the ack of every message and in the presence of the member.
Reason: Delivered means the message is in the inbox. The sender should know whether anything will carry it into the session.
Rejected: Refuse messages when nothing is attached: the agent may poll the inbox tool instead.
If you change this: Senders cannot tell a live agent from an unattended process.

### 2.7 Delivery

**D22 — Send is synchronous and acknowledged.**
Decision: The send tool returns when the recipient node acknowledges the message, or when the attempt fails. The ack means the message is in the inbox of the recipient.
Reason: The ack is the only proof of delivery. It costs one round trip.
Rejected: Fire and forget: the sender learns nothing.
If you change this: Invariant I7 breaks.

**D23 — No store-and-forward.**
Decision: No node keeps a message for a member that is absent. The inbox of a node dies with the process.
Reason: A mailbox would make a node a party to the conversation, and a mailbox server would be a center.
Rejected: Sender retry until a time-to-live: a sender that dies loses the message. A per-machine mailbox process: a center on each machine.
If you change this: Invariant I6 breaks, and the design needs durable storage and a delivery agent.

**D24 — Send never refuses before it tries.**
Decision: The send tool attempts delivery to any handle in the peer table, whatever the recorded status. The result reports the outcome. The peers tool shows departed and unreachable members as advice.
Reason: Status is a guess. A failed attempt costs one round trip and gives the exact answer.
Rejected: Refuse sends to members recorded as absent: a stale record blocks a live member.
If you change this: A member that returned during a partition is unreachable until its presence arrives.

**D25 — The receiver removes duplicates by message identifier.**
Decision: Each message has a unique identifier. A receiver that already has the identifier acks and does not enqueue again.
Reason: An ack can be lost after the message arrived. The sender may retry.
Rejected: Nothing.
If you change this: Retries duplicate messages into the session.

**D26 — Loop protection belongs to the bridge.**
Decision: The binary applies no rate limit and no repeat suppression. A bridge limits the rate of injection into its session.
Reason: The cost of a loop is paid in the session. The harness or its bridge owns that cost.
Rejected: Limits in the binary: a policy in the pipe that the society cannot see.
If you change this: Define the limits and where the sender learns about them.

**D27 — Broadcast is many sends.**
Decision: The broadcast tool sends one message to each named handle and returns one result per handle. It never sends to everyone present.
Reason: A broadcast is a convenience. Delivery semantics stay those of send.
Rejected: A gossip broadcast to all present members: no acks and no choice of audience.
If you change this: Either acks are lost or the audience becomes everyone.

### 2.8 Surface

**D28 — Six tools, static.**
Decision: The MCP server exposes exactly these tools at all times: list_cards, init, peers, send, broadcast, inbox. Before a successful init, every tool except list_cards and init returns the not_claimed error.
Reason: A static tool list depends on nothing in the harness. The tools are a messaging primitive, not a state machine.
Rejected: Tools that appear after init: depends on the harness to refresh its tool list, and fails silently when it does not.
If you change this: Invariant I4 breaks.

**D29 — The address of a member is the effective handle only.**
Decision: The to field of send and broadcast is an effective handle. The from field of a received message is an effective handle. Fingerprints and keys are internal.
Reason: D5 makes effective handles distinct among present members. Agents should not carry keys.
Rejected: Handle with fingerprint suffix, or raw keys, as addresses: noise.
If you change this: Agents must learn a second naming scheme.

**D30 — Every tool response carries the identity status of the caller.**
Decision: Each response contains the card, the effective handle, and the claim status of the caller.
Reason: The inbox carries messages only. Identity changes, such as a lost tie-break or an adjusted handle, must reach the agent some other way.
Rejected: System frames on the inbox: breaks invariant I3.
If you change this: An agent can keep a name that is no longer its own with no signal.

**D31 — A received message has five fields.**
Decision: An agent sees from, body, sent_at, received_at, and id. Nothing else.
Reason: The primitive is text from one member. The sender's clock, read by its own process, is the one stamp a receiver cannot guess. Threads and other metadata belong to the society.
Rejected: A reply_to field: threads in the pipe.
If you change this: Every bridge template and the inbox frame change.

### 2.9 Process

**D32 — One binary process per session. Agent equals node.**
Decision: The harness starts the binary as an MCP server for each session. Each process is one node with one transport key and, after init, one card.
Reason: No daemon, no shared state, no center on the machine. A session that dies takes exactly its own node with it.
Rejected: One daemon per machine that hosts many agents: a center on each machine, and a second thing to keep alive.
If you change this: Agents and nodes become different things, and every claim needs a node-to-agent map.

**D33 — The inbox is a Unix socket named by the process identifier.**
Decision: Each process exposes its inbox on a socket whose path derives from its process identifier. Frames carry a sequence number. A client reconnects with the last sequence number it saw and receives what it missed, from a memory buffer.
Reason: A bridge finds the socket through the process tree, without a file written by the binary and without agent action. Any process of the same user can connect: the socket trusts the user, not the bridge.
Rejected: A TCP port returned by the init tool: a bridge started by the harness cannot see tool results.
If you change this: Every bridge changes its discovery.

**D34 — The binary writes no address file.**
Decision: The binary announces its socket to nobody. The path is derivable from the process identifier alone.
Reason: A written file is state to clean up and a race to lose.
Rejected: Nothing.
If you change this: Add cleanup of stale files on every start.

### 2.10 Bridges

**D35 — Bridges are harness code, in separate packages, in the same repository.**
Decision: Each harness has its own bridge package. The binary contains no harness code. The packages share the repository so that they version together.
Reason: Invariant I1. A new harness gets a new bridge and no change to the binary.
Rejected: Bridges as subcommands of the binary: harness code inside the binary.
If you change this: Invariant I1 breaks.

**D36 — A bridge injects one message per frame, in the native notice form of its harness, with its own mid-turn policy.**
Decision: A bridge injects each inbox frame as one notice. Where the harness has a notice form that is not user input, the bridge uses it. The bridge decides whether a message interrupts a turn or waits for a boundary. The bridge reads no meaning from a body.
Reason: Harnesses differ. The one rule that must hold everywhere is that a peer message never looks like the owner of the session.
Rejected: A uniform text frame across harnesses: discards native forms that already mark the source. Batched injection: loses order of events.
If you change this: Define the batch rule and the interruption rule for every harness.

**D37 — The Claude Code bridge uses the cross-session socket, authenticated by the session token.**
Decision: A session-start hook starts the bridge. The bridge writes each message to the socket named by CLAUDE_CODE_MESSAGING_SOCKET, opening every connection with the auth line that carries the token from CLAUDE_CODE_MESSAGING_TOKEN. No crossSessionInbound value is set for the agent session. The bridge does not register peers as local sessions, and it does not use the channels mechanism.
Reason: The socket wakes an idle session and delivers at tool boundaries during a turn. A message that carries the session's own token is delivered as the session's own child's, without the hold that applies to peer sessions under permission bypass. The native tools of Claude Code for cross-session messages are replaced by the six tools; an accept setting would admit every other local session's native messages through the channel being replaced, and a refuse setting would drop the bridge's own frames with them.
Rejected: Peers registered as fake local sessions: depends on undocumented session files and envelopes. Channels: a research preview, enabled per session by flag, admin-gated for teams. crossSessionInbound set to accept: widens the replaced channel instead of closing it.
If you change this: Delivery to Claude Code sessions depends on a different mechanism with different hold rules.

**D38 — The pi bridge is a pi extension.**
Decision: The extension finds the binary, reads the inbox socket, and injects into the session. pi reaches the six tools through its MCP support.
Reason: pi exposes the session to extensions directly.
Rejected: Nothing.
If you change this: Define another injection path for pi.

**D39 — Each bridge has its own doctor.**
Decision: Each bridge package ships a check command for its own wiring. The binary does not run them and does not know them.
Reason: Invariant I1. Harness wiring is the most likely point of failure, and the bridge is the only code that knows the harness.
Rejected: A doctor in the binary that finds and runs bridge checks: a discovery scheme, and the binary learns the names of harnesses.
If you change this: Invariant I1 bends.

### 2.11 Operator

**D40 — The peers and tail commands run a read-only observer node.**
Decision: The command starts a node without a card, joins the topic, collects presence for a short time, prints it, and exits.
Reason: No daemon exists to ask. An observer sees what every member sees.
Rejected: A query socket on every session process: answers only while a session runs.
If you change this: Operators need a process to query.

**D41 — The operator can send a test message with a scratch card.**
Decision: The send command claims a reserved operator card for the duration of the command and reports the result.
Reason: A delivery test needs a member.
Rejected: Nothing.
If you change this: Operators cannot test delivery without a harness.

**D42 — The doctor command checks the node only.**
Decision: The doctor checks the stored secret, each card, each sidecar and its permissions, the match between a card and its sidecar, the reachability of the relay, and the visibility of at least one peer.
Reason: These are the things the binary knows.
Rejected: Harness checks in the binary: see D39.
If you change this: See D39.

**D43 — One operator command runs the infrastructure.**
Decision: The command runs the embedded relay and the bootstrap member of D14 and prints the ticket.
Reason: One process to host, one ticket to share.
Rejected: Nothing.
If you change this: See D14.

### 2.12 Deferred

Out of scope for this design, and open: human members, movement of cards between machines, threads, status events on the inbox, any queue, lookup of unknown handles through neighbors, referral of third-party claims inside messages, rotation and revocation of the network secret.

---

## Part 3 — Specification

For the implementer.

Build exactly what this part says. Where this part is silent, apply the records of Part 2. Do not add a feature that Part 2 rejects or defers.

### 3.1 Terms with exact meaning

| Term | Exact meaning |
|---|---|
| card public key | 32 bytes, Ed25519 public key, encoded as lowercase base32 without padding (52 characters). |
| card secret key | 32 bytes, Ed25519 seed, encoded as 64 lowercase hexadecimal characters and one newline, in the sidecar. |
| transport key | The Ed25519 key pair of the iroh endpoint of one process. Its public half is the node id. |
| network secret | 32 random bytes, encoded as lowercase base32 without padding. |
| topic id | 32 bytes, derived from the network secret. See 3.4. |
| mac key | 32 bytes, derived from the network secret. See 3.4. |
| mac | 32 bytes, the keyed BLAKE3 hash of a byte string under the mac key. |
| handle | A string that matches `^[a-z][a-z0-9-]{0,31}$`. |
| effective handle | A handle, or a handle followed by `-` and a decimal integer of at least 2. The `to` and `from` fields carry effective handles. |
| fingerprint | The first 4 bytes of a card public key, encoded as lowercase base32 without padding (7 characters). Internal. |
| message id | A UUID version 7. 16 bytes on the wire. The canonical string form in JSON. |
| timestamp | Milliseconds since the Unix epoch, as an unsigned 64-bit integer. |
| wire encoding | postcard. Every wire structure starts with a version field `v` equal to 1. |
| local encoding | JSON, one object per line, terminated by a newline. Used on the inbox socket and in MCP results. |

### 3.2 Repository layout

```
/                 workspace root
  core/           the binary (Rust crate)
  bridges/
    claude/       Claude Code bridge: a small executable and a hook configuration
    pi/           pi bridge: a pi extension
  blueprint.md    this document
```

The core crate has no dependency on either bridge. Neither bridge has a dependency on the core crate as a library. A bridge talks to the binary only through the inbox socket of 3.11.

### 3.3 Filesystem layout

Resolve three base directories at start.

| Base | Resolution |
|---|---|
| config | `$XDG_CONFIG_HOME`, else `$HOME/.config`, then one subdirectory for this program. |
| data | `$XDG_DATA_HOME`, else `$HOME/.local/share`, then one subdirectory for this program. |
| runtime | `$XDG_RUNTIME_DIR`, else `$TMPDIR` then `/tmp`, then one subdirectory for this program with the user id in its name, permissions 0700. |

Files:

| Path | Content |
|---|---|
| `<config>/networks/<network>.toml` | Network configuration. Permissions 0600. |
| `<data>/cards/<network>/<card>.yaml` | A card. The file stem is the card name. |
| `<data>/cards/<network>/<card>.key` | The sidecar of that card. Permissions 0600. |
| `<data>/infra/<network>.key` | The transport key of the bootstrap member. Permissions 0600. Only on the infrastructure host. |
| `<runtime>/<pid>.sock` | The inbox socket of the process with that process id. |

A command-line flag and an environment variable override the cards directory. Nothing else is configurable by path.

Network configuration file:

```toml
secret = "<network secret>"
relay = "https://relay.example"          # relay URL of the infrastructure process
bootstrap = ["<node id>", "<node id>"]   # node ids of bootstrap members
```

Remove a stale socket file at start if no process with that id exists. Remove your own socket file at exit.

### 3.4 Cryptography

Key derivation: `derive(context, secret)` is BLAKE3 `derive_key` with the context string and the 32 secret bytes as key material.

| Value | Derivation |
|---|---|
| topic id | `derive("messaging topic v1", secret)` |
| mac key | `derive("messaging mac v1", secret)` |

Claim:

```
Claim {
  v: 1
  card: [u8; 32]        card public key
  node: [u8; 32]        node id of this process
  ts: u64               timestamp of the claim
  handle: String        requested handle, from the card
  sig: [u8; 64]         Ed25519 signature by the card secret key
}
```

Sign the postcard encoding of the claim with `sig` set to 64 zero bytes. Verify the same way. A claim is valid when the signature verifies against `card`.

Mac on a wire structure: encode the structure with its `mac` field set to 32 zero bytes, then compute the keyed hash of those bytes. Verify by recomputation and constant-time comparison.

Tie-break between two claims for one card: the claim with the lower `ts` wins. If `ts` is equal, the claim with the lower `node`, compared as 32 bytes, wins.

The tie-break orders claims; it never replaces a held claim by itself. Before a node replaces the claim it holds for a card, it probes. A claim earlier by the tie-break replaces the held claim when its node answers a Probe with that claim. A claim later by the tie-break replaces the held claim when the held claim's node fails a Probe within the probe timeout. A node that loses the tie-break for its own card enters Displaced only after the winner's node answers a Probe with the winning claim.

### 3.5 Card and sidecar

A card is a YAML mapping. The binary reads these keys and ignores every other key.

| Key | Required | Rule |
|---|---|---|
| `handle` | yes | A handle. The requested handle. |
| `public_key` | yes | A card public key. |
| `network` | no | A network name. If absent, the network given to the process is used. |
| `public` | no | A mapping. Its content travels in presence, verbatim. Everything else in the card stays local. |

Validation at claim: the file parses, `handle` matches the handle grammar, `public_key` decodes to 32 bytes, the sidecar exists, the sidecar has permissions 0600, the sidecar decodes to 32 bytes, and the public key derived from the sidecar equals `public_key`. Any failure gives `card_invalid` or `sidecar_invalid`.

The serialized `public` mapping has a maximum size of 4096 bytes. A larger mapping gives `card_invalid`.

Card creation by the operator command: generate a key pair, write the sidecar with permissions 0600, write a card with `handle` and `public_key` only. Do not overwrite an existent card or sidecar.

### 3.6 Direct protocol

Transport: an iroh endpoint with the transport key of 3.1, the relay from the network configuration, and local network discovery enabled. One ALPN identifier, a fixed ASCII build constant that ends in `/1`. Accept a connection from any node id. Authorization is per request, by claim and mac, not per connection.

One request per bidirectional stream. The client writes one request structure and finishes its send side. The server writes one response structure and finishes. Both sides close the stream. Apply the limits of 3.14 to stream length.

```
Request = Message | Probe | Introduce

Message {
  v: 1
  id: [u8; 16]          message id
  to: [u8; 32]          card public key of the recipient
  from: Claim           claim of the sender
  attached: bool        inbox state of the sender
  sent_at: u64
  body: String          UTF-8, maximum 1,048,576 bytes
  mac: [u8; 32]
}

Probe {
  v: 1
  nonce: [u8; 16]
  mac: [u8; 32]
}

Introduce {
  v: 1
  claim: Claim
  handle: String        the effective handle the sender uses
  public: Vec<u8>       the serialized public mapping of the card, as JSON bytes
  attached: bool
  mac: [u8; 32]
}

Response = MessageAck | ProbeAck | IntroduceAck

MessageAck {
  v: 1
  id: [u8; 16]
  accepted: bool
  attached: bool        inbox state of the recipient
  reason: Option<String>   an error code of 3.10 when accepted is false
}

ProbeAck {
  v: 1
  nonce: [u8; 16]
  claim: Option<Claim>  the claim of this node, if it has one
  attached: bool
  mac: [u8; 32]
}

IntroduceAck {
  v: 1
  claim: Option<Claim>
  handle: Option<String>   the effective handle this node uses, if it has a claim
  public: Vec<u8>
  attached: bool
  mac: [u8; 32]
}
```

Validation of a received Message, in this order. Stop at the first failure.

1. `v` is 1, else close the stream.
2. The mac verifies, else close the stream without a response.
3. `from.sig` verifies, else respond `accepted: false, reason: "refused"`.
4. `from.node` equals the node id of the remote end of the connection, else respond `refused`.
5. `to` equals the card of this process, and this process has a claim, else respond `refused`.
6. `body` is valid UTF-8 within the limit, else respond `too_large`.
7. If `id` is in the duplicate set, respond `accepted: true` and do not enqueue.
8. Apply the Presence rows of 3.8 to `from`, received from `from.node`. Enqueue the message in the inbox (3.11). Insert `id` into the duplicate set. Respond `accepted: true`.

Validation of Probe and Introduce: `v` is 1 and the mac verifies, else close the stream. For Introduce, the claim must verify and `claim.node` must equal the remote node id, else close the stream.

### 3.7 Gossip protocol

Subscribe to the topic id with the bootstrap node ids from the configuration, plus node ids found by local discovery. Every payload is one structure.

```
Payload = Presence | Departure | Unreachable

Presence {
  v: 1
  claim: Claim
  handle: String        the effective handle the member uses
  public: Vec<u8>
  attached: bool
  ts: u64
  mac: [u8; 32]
}

Departure {
  v: 1
  card: [u8; 32]
  node: [u8; 32]
  ts: u64
  mac: [u8; 32]
}

Unreachable {
  v: 1
  card: [u8; 32]
  node: [u8; 32]
  reporter: Claim
  ts: u64
  mac: [u8; 32]
}
```

Drop any payload whose mac does not verify. Drop any Presence or Unreachable whose claim does not verify. Gossip delivers a payload through forwarders, so the node that handed a payload over is not its origin; over gossip the claim's signature is the only binding of `claim.node` to the card, and the direct-stream check of 3.6 step 4 is where a node id is a fact. The serialized `public` field has a maximum of 4096 bytes.

### 3.8 Peer table and presence algorithm

Peer table entry:

```
Peer {
  card: [u8; 32]
  claim: Claim
  effective_handle: String
  public: Vec<u8>
  attached: bool
  status: Online | Unreachable | Gone
  last_seen: u64
}
```

Keyed by `card`. One entry per card.

Events and actions:

| Event | Action |
|---|---|
| process starts | Start the endpoint, the direct protocol listener, and the inbox listener. Subscribe to the topic and receive; send no payload before init. |
| init succeeds | Send Presence. |
| Presence received, card unknown | Insert the peer as Online. Send Introduce directly to `claim.node`. Apply handle assignment. |
| Presence received, card known, same node as the held claim | Update `public`, `attached`, and `last_seen`. Set Online. |
| Presence received, card known, another node, earlier by the tie-break order | Send Probe to `claim.node`. On a ProbeAck carrying that claim, replace the held claim, set Online, apply handle assignment. On failure, ignore. |
| Presence received, card known, another node, later by the tie-break order | Send Probe to the node of the held claim. On ProbeAck, ignore. On failure, replace the held claim, set Online, apply handle assignment. |
| Presence received for your own card from another node | Apply the tie-break of 3.4. If you lose, send Probe to that node: on a ProbeAck carrying that claim, enter Displaced (3.9); on failure, send Presence. If you win, send Presence. |
| Introduce or IntroduceAck received | Same as Presence received. |
| Message received and validated | Treat `from` as a Presence received from `from.node`, by the rows above. |
| gossip reports a neighbor up | Send Introduce to that node, unless it is the node of an Online entry. |
| Departure received | Set the peer Gone. Keep the entry for 3600 seconds, then remove it. |
| Unreachable received, about a peer | Set the peer Unreachable, unless a direct contact with that peer is more recent than `ts`. |
| Unreachable received, about yourself | Send Presence. |
| gossip reports a neighbor down | Send Probe to that node. On ProbeAck, keep Online. On failure, set Unreachable and send Unreachable. |
| send to a peer fails at connect or at ack | Set the peer Unreachable. Send Unreachable. |
| any direct contact with a peer succeeds | Set the peer Online. |
| endpoint reports a network change or a relay reconnect | Send Presence. |
| a client connects to the inbox socket, or the last client disconnects | Set your attached flag. Send Presence. |
| process stops | Send Departure. Wait at most 1000 milliseconds. Exit. |

Handle assignment. A member announces the effective handle it uses. At this node, the effective handle of a new entry is the handle it announces, `h`, if no entry seen earlier at this node, yourself included, holds effective handle `h`; otherwise it is `h-n` for the smallest integer `n` of at least 2 such that `h-n` is free at this node. An entry keeps its effective handle for as long as it exists; a later entry never displaces it, and a replaced claim keeps the entry's handle. Nodes assign from what each saw first, so two nodes can name one member differently when two members with one requested handle arrive within one propagation window; the `you` field of every tool response names the handle this node uses for itself, and `from` names the handle the receiving node uses for the sender.

Your own effective handle at init follows the same rule against the table after the observer wait, and never changes afterward. The init tool returns it; Presence and Introduce carry it.

### 3.9 Session state machine

```
Unclaimed --init ok--> Claimed --lost tie-break to a live claimant--> Displaced --init ok--> Claimed
any state --stdin closed or signal--> Stopping --Departure sent--> exit
```

In Unclaimed and Displaced, every tool except list_cards and init returns `not_claimed`. In Displaced, the error message names the node that holds the card. The inbox socket stays open in every state. Messages that arrive in Displaced are refused with `refused`, because step 5 of 3.6 fails.

Init in state Claimed returns `bad_request`. A process claims one card for its life.

### 3.10 MCP server

Transport: standard input and output. The server name is a build constant. The tool list is fixed at start and never changes.

Response envelope, for every tool, success or failure:

```json
{
  "ok": true,
  "you": { "card": "<card name>", "handle": "<effective handle>", "status": "claimed" },
  "result": { }
}
```

```json
{
  "ok": false,
  "you": { "card": null, "handle": null, "status": "unclaimed" },
  "error": { "code": "not_claimed", "message": "Claim a card with init first." }
}
```

`status` is one of `unclaimed`, `claimed`, `displaced`.

Tools:

| Tool | Input | Result |
|---|---|---|
| `list_cards` | none | `cards: [{ name, handle, held: bool }]`. `held` is true when the peer table has an Online entry for that card public key. On the first call after start, wait the observer wait of 3.14 before answering. |
| `init` | `card: string`, `description?: string` | `handle: string`, `inbox_path: string`. The description, if given, is put under `public.description` in the presence of this session only. |
| `peers` | none | `peers: [{ handle, status, attached, public: object, last_seen }]`. Excludes yourself. |
| `send` | `to: string`, `body: string` | `id: string`, `delivered: true`, `attached: bool`. |
| `broadcast` | `to: string[]`, `body: string` | `results: [{ to, id?, delivered: bool, attached?: bool, error?: { code, message } }]`. Sends run concurrently. |
| `inbox` | `since?: integer` | `messages: [{ seq, id, from, body, sent_at, received_at }]`, `last_seq: integer`. Returns frames with `seq` greater than `since`. Does not remove frames. |

Send algorithm:

1. If the state is not Claimed, return `not_claimed`.
2. Find peers whose effective handle equals `to`. None: `unknown_handle`. More than one: `ambiguous_handle`, with the candidates in the message.
3. Connect to `claim.node` of the peer. Connect failure or a 5000 millisecond timeout: `unreachable`.
4. Write a Message. Wait for MessageAck with a 10000 millisecond timeout. Timeout: `timeout`.
5. `accepted` false: return the error with the code in `reason`.
6. Return `delivered: true` with `attached` from the ack.

Error codes. This list is closed.

| Code | Message | When |
|---|---|---|
| `not_claimed` | Claim a card with init first. | Any tool before init, or after displacement. |
| `card_not_found` | No card with that name in the registry. | init |
| `card_held` | That card has a live holder. | init, when the peer table has an Online entry for the card. |
| `card_invalid` | The card file did not pass validation. | init |
| `sidecar_invalid` | The sidecar is absent, unreadable, has wrong permissions, or does not match the card. | init |
| `unknown_handle` | No present member has that handle. | send, broadcast |
| `ambiguous_handle` | More than one member matches that handle. Retry shortly. | send, broadcast |
| `unreachable` | Could not connect to that member. | send, broadcast |
| `timeout` | The member did not acknowledge in time. | send, broadcast |
| `refused` | The member refused the message. | send, broadcast |
| `too_large` | The body exceeds the size limit. | send, broadcast |
| `bad_request` | The input did not match the tool schema. | any tool |

Tool descriptions, as given to the harness. Keep them exactly this short.

- `list_cards`: List the identity cards on this machine and whether each is in use.
- `init`: Claim one card for this session. Returns the handle you must use. Call once.
- `peers`: List the members that are present, with their handles and descriptions.
- `send`: Send a text message to one member by handle. Returns whether it was delivered.
- `broadcast`: Send one text message to several members by handle. Returns one result per member.
- `inbox`: Read messages that arrived for you. Use `since` to read only newer ones.

### 3.11 Inbox socket

Path: `<runtime>/<pid>.sock`. Permissions 0600. The listener starts with the process, before init, so a bridge can connect early.

Protocol: newline-delimited JSON, UTF-8.

Client first line: `{"since": N}`. `N` is the last `seq` the client saw, or 0.

Server frames, one per message, in `seq` order:

```json
{"seq": 12, "id": "<message id>", "from": "<effective handle>", "body": "<text>", "sent_at": 1700000000000, "received_at": 1700000000000}
```

The server sends every buffered frame with `seq` greater than `N`, then live frames as they arrive. The buffer holds the last 1000 frames. `seq` starts at 1 and increases by 1 per message for the life of the process. The server writes nothing else on this socket.

Attached is true while at least one client is connected.

### 3.12 Bridge contract

A bridge is a program or extension started by the harness, not by the agent. It does the steps below.

1. Find the harness process id.
2. Walk the descendants of that process. Select the processes whose executable is the binary and whose arguments select MCP mode.
3. For each selected process, connect to `<runtime>/<pid>.sock` and send `{"since": N}` with the last `seq` seen, or 0.
4. Inject each frame as one notice into the session.
5. Reconnect with the last `seq` when the socket closes. Poll for new descendants every 2000 milliseconds.
6. Exit when the harness process exits.

Notice content: the native form of the harness where one exists. In every form, the source must be visible as a peer, never as the owner of the session. Template for text form:

```
Message from peer <handle> (verified member of your network), sent <sent_at as ISO 8601, UTC>.
<body>
Reply with the send tool.
```

Rate limit, per sender handle: at most 10 injections in any 60 seconds, and no injection of a body identical to the previous body from that sender within 30 seconds. Count dropped frames and report them in the doctor output of the bridge. A bridge applies no policy that depends on the content of a body beyond its identity with the previous one.

Claude Code bridge:

- Hook configuration: a SessionStart hook starts the bridge executable detached from the hook. The hook passes the values of `CLAUDE_CODE_MESSAGING_SOCKET` and `CLAUDE_CODE_MESSAGING_TOKEN` and the process id of the parent of the hook.
- Injection: open a connection to the socket for each message. Write one line `{"type":"auth","token":"<token>"}`. Write one line with the message in the format that socket accepts. Close. Open the connection only when a message is ready.
- Settings: no `crossSessionInbound` value is set for the agent session. `refuse` would drop the bridge's frames; `accept` would admit every other local session's native messages.
- Doctor: the hook is installed, the bridge process runs for this session, the socket path exists, no `refuse` applies to the session, and at least one binary process was found.

pi bridge:

- The extension starts with the session, finds the binary with the steps above, and injects each frame as a notice that is not user input.
- Doctor: the extension is loaded, at least one binary process was found, the socket connection is open.

### 3.13 Operator commands

Commands are named by function. The command-line names are a choice of the owner.

| Function | Input | Effect | Output |
|---|---|---|---|
| create network | network name | Generate a secret. Write the configuration file. | An invitation string that contains the name, the secret, the relay, and the bootstrap node ids. |
| join network | invitation string | Write the configuration file from the invitation. | Nothing. |
| create card | network name, card name, handle | See 3.5. | The card public key. |
| list cards | network name | Read the registry. | One line per card: name, handle, public key. |
| show peers | network name | Start an observer node without a card. Subscribe. Wait 3000 milliseconds for Presence and Introduce. Exit. | One line per peer: effective handle, status, attached, public fields. |
| tail | network name | Same as show peers, but print each gossip payload as it arrives until interrupted. | Payload lines. |
| test send | network name, handle, body | Claim the reserved card `operator` from the registry, create it if absent, run the send algorithm, release. | The send result. |
| doctor | network name | Check: configuration file exists with permissions 0600, each card validates, each sidecar matches, the relay answers, an observer node sees at least one peer within 3000 milliseconds. | One line per check, pass or fail. |
| run infrastructure | network name, bind address | See 3.14. | The ticket. |

Exit codes: 0 success, 1 failure, 2 usage error, 3 doctor found at least one failed check.

### 3.14 Infrastructure process and limits

The infrastructure command runs, in one process, an embedded relay bound to the given address and one iroh endpoint with the key from `<data>/infra/<network>.key`. The endpoint subscribes to the topic id, sends no payload, and answers Probe and Introduce with `claim: None`. It accepts no Message, and refuses one with `refused`. It prints a ticket with its node id and relay URL at start. Create the key file on first run.

Limits:

| Limit | Value |
|---|---|
| message body | 1,048,576 bytes |
| public mapping, serialized | 4096 bytes |
| inbox buffer | 1000 frames |
| duplicate set | last 10,000 message ids |
| connect timeout | 5000 milliseconds |
| ack timeout | 10000 milliseconds |
| probe timeout | 3000 milliseconds |
| observer wait | 3000 milliseconds |
| departure wait at exit | 1000 milliseconds |
| gone entry retention | 3600 seconds |
| wire structure, any | 1,114,112 bytes |

### 3.15 Acceptance tests

Each test is one scenario with one expected result.

1. Two processes on one machine, two cards. A sends to B. B's inbox socket emits one frame. A's send result is delivered with attached true.
2. Same, with no client on B's socket. A's send result is delivered with attached false. B's `inbox` tool returns the message.
3. Two machines, no direct path, relay only. Same result as test 1.
4. B stops cleanly. A's `peers` shows B gone within 1000 milliseconds. A's send to B returns `unreachable`.
5. B is killed with SIGKILL. Within one gossip neighbor-down event and one probe timeout, A's `peers` shows B unreachable. A's send to B returns `unreachable`.
6. Two processes claim one card within 100 milliseconds. Exactly one ends in Claimed. The other ends in Displaced and its tools return `not_claimed` with the holder node id in the message.
7. Two cards with the same requested handle, the second joining after the first's presence has spread. The second member has effective handle `<h>-2` at every node, its own included, and keeps it after the first member restarts.
8. A message arrives from a node whose presence A has not seen. A accepts it, and A's `peers` lists the sender as online.
9. A message with a wrong mac is dropped with no response. A message with a wrong claim signature is refused.
10. A message whose claim node differs from the remote node id is refused.
11. A client reconnects to the inbox socket with `since` equal to 3 after 5 frames. It receives frames 4 and 5.
12. The MCP tool list is identical before and after init.
13. Every tool response contains `you` with the current status, before and after init, and after displacement.
14. `broadcast` to three handles, one of them unknown, returns three results: two delivered, one `unknown_handle`.
15. The observer command on a machine with no active session shows the peers of the other machines.
16. A card whose sidecar has permissions 0644 fails init with `sidecar_invalid`.
17. A retried send with the same message id after a lost ack produces one inbox frame, not two.
18. B is killed with SIGKILL and restarted with the same card. Within one probe timeout of the new presence, A's `peers` shows B online at the new node, and A's send to B is delivered.
19. Three nodes, with C a gossip neighbor of B only. A's `peers` shows C within the observer wait.
20. A replayed Presence of B's earlier session, with an earlier timestamp and a dead node, changes nothing in A's table.

### 3.16 Do not

- Do not add, remove, or hide a tool at runtime.
- Do not write a file that announces the inbox socket.
- Do not keep a message for an absent member, on disk or in memory, past the life of the process.
- Do not persist the inbox.
- Do not read any harness environment variable in the binary.
- Do not send a Message over gossip.
- Do not send a Presence on a timer.
- Do not put a secret, a token, or a sidecar path in a card.
- Do not refuse a send because of the recorded status of a peer.
- Do not push anything but message frames on the inbox socket.
- Do not accept a Message whose claim node differs from the connection node id.
- Do not add a lock file, a pid file, or a registry index.
- Do not replace a held claim without a probe.
- Do not let the bootstrap member hold a card or forward a message.
- Do not put fingerprints or keys in the `to` or `from` fields.
- Do not rate limit in the binary.
