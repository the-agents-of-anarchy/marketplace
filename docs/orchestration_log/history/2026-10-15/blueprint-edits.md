# Blueprint edits applied — the no-runner-up set

— verified by claude-fable-5-1 (resident-anarchist [6a43c8]), 2026-10-15, witnessed. Owner word (17:20+0300): "any edits you would suggest that don't really have close runner-up alternatives without boosting them unjustly - all those edits you're free to apply. copy the file, re-read, edit." Original untouched: /Users/ryzhakar/Downloads/blueprint.md (sha1 815456a7e7b613e912e4e9763bfd3e7f57dd5fd0). Revised copy: /Users/ryzhakar/Downloads/blueprint.revised.md. Copy re-read whole before editing. 24 exact-once replacements by script; no invariant of 2.3 touched.

## Applied

| # | Where | Edit | Why no runner-up |
|---|---|---|---|
| 1 | 1.3, D5 | "the newcomer" → "the later claim" | Part 1 promised what Part 3 does not do; the only honest alternative was changing Part 3's handle order, which has a real trade-off (table convergence) and is not applied. |
| 2 | 1.7 | "No center" → "No center of authority or memory"; the fixed place holds nothing and decides nothing; "builds from speech" → "builds outside this network" | D14 is a center of reachability; the owner's ruling (17:12) makes the service one channel among others. Both sentences were false as written. |
| 3 | D6, D7, 3.4, 3.8, 3.9, 3.16, tests 18 and 20 | A held claim is replaced only after a probe: an earlier claim when its node answers, a later claim when the held node fails. Displaced only after the winner answers a probe. | A timestamp is a claim; a probe is a fact. Without this a crash restart is unreachable for the life of the network and a replayed presence displaces a live member. The mechanism (Probe, D20) already exists. |
| 4 | 3.7, test 19 | Dropped "drop any Presence whose claim.node differs from the gossip sender node id". | iroh-gossip `api::Message.delivered_from` is documented as the forwarder, "not the same as the original author". The check drops every relayed presence. The signature already binds node to card; 3.6 step 4 keeps the check where the node id is a fact. |
| 5 | 3.8 (process starts), 3.10 list_cards | Endpoint and subscription start at process start, receive only; Presence at init; `list_cards` waits the observer wait on its first call. | As written the table was empty until init, so `held` was always false and `card_held` could not fire. Uses the observer of D40. |
| 6 | D18, 3.8 | Introduce on neighbor up. | The only event-driven recovery from a lost first presence; no timer, per 3.16. |
| 7 | D37, 3.12 | Token auth line on every connection; no `crossSessionInbound` value; doctor checks no `refuse`. | Claude Code docs: a message carrying the session's token is delivered as the session's own child's, no `accept` needed; `accept` admits every native session (the banned channel, owner 17:12); `refuse` drops the bridge's frames. |
| 8 | D31, 3.10, 3.11, 3.12 template | `sent_at` is the fifth field of a received message. | The wire already carries it; dropping it discards the one stamp a receiver cannot guess. The society's guessed-stamp failures (full-picture F2) rest on exactly this. |
| 9 | 3.1, 3.8 | `effective handle` defined: a handle or a handle plus `-n`. | `h-n` on a 31- or 32-character handle broke the handle grammar. |
| 10 | D33 | "Any process of the same user can connect: the socket trusts the user, not the bridge." | A fact about 0600 in a 0700 directory, unstated. |
| 11 | 2.12 | Rotation and revocation of the network secret deferred explicitly. | Open either way; unlisted it was invisible. |

## Suggested, not applied (a close runner-up exists)

- Handle contest by first sight instead of timestamp order (deliberation §1.D): timestamp order buys table convergence without a message; first sight buys name stability for present members. A trade-off, the owner's.
- Batched injection in `seq` order (deliberation §2.2.7): the one-frame-one-notice rule keeps the native notice form's per-message semantics. A trade-off.
- Receiver-side holds in the bridge (deliberation §2.2.1a): superseded by the owner's rulings; attaching is a right, holds are the society's.
- D9 re-announce on card edit: withdrawn under "technical and social presence are separate".
- Part 1 §1.5 wording on `attached`: fine as is once D33's sentence stands.

## Unverified in this pass

- How Claude Code labels an own-child socket message to the model; D37's Reason now rests on the docs' delivery rule, not on an observed label.
- iroh-gossip `NeighborUp` firing per new neighbor (docs list the event; its cadence was not read).

## Diff

```diff
--- /Users/ryzhakar/Downloads/blueprint.md	2026-10-15 15:40:04
+++ /Users/ryzhakar/Downloads/blueprint.revised.md	2026-10-15 16:28:12
@@ -20,7 +20,7 @@
 
 ### 1.3 Names
 
-Two cards may want the same name. The network keeps the names of present members distinct by adjusting the name of the newcomer. The adjusted name is the one the member must use. The seal does not change.
+Two cards may want the same name. The network keeps the names of present members distinct by adjusting the name of the later claim. The adjusted name is the one the member must use. The seal does not change.
 
 ### 1.4 Presence
 
@@ -36,9 +36,9 @@
 
 ### 1.7 What is absent, on purpose
 
-No mailbox. No queue. No group. No thread. No human member, yet. No center. No announcement pushed to a member who did not ask for it.
+No mailbox. No queue. No group. No thread. No human member, yet. No center of authority or memory. No announcement pushed to a member who did not ask for it.
 
-Each absence is a choice. A mailbox would make the network a party to the conversation. A group would make the network decide who belongs. A center would make the network belong to someone. Whatever the society needs beyond speech, it builds from speech.
+Each absence is a choice. A mailbox would make the network a party to the conversation. A group would make the network decide who belongs. A center would make the network belong to someone; the one fixed place where members find each other holds nothing and decides nothing. Whatever the society needs beyond carried speech, it builds outside this network.
 
 ### 1.8 What a member may rely on
 
@@ -128,19 +128,19 @@
 If you change this: Any node could announce itself as any card.
 
 **D5 — Handles are labels. The binary adjusts a handle on clash.**
-Decision: If a present member has the requested handle, the newcomer gets an adjusted handle. The init tool returns the effective handle. The card is not changed.
+Decision: If a present member has the requested handle, the later claim gets an adjusted handle. The init tool returns the effective handle. The card is not changed.
 Reason: Two societies, or two cards, may want the same name. The identity is the key, so the label may bend.
 Rejected: Uniqueness enforced across the network with refusal. A stranger could block a name. A fingerprint suffix in the effective handle: noise for agents.
 If you change this: Either names collide silently, or a claim can be refused because of a label.
 
 **D6 — One live holder per card. A second claim is refused. Simultaneous claims use a tie-break.**
-Decision: A claim for a card that has a present holder is refused. If two claims for one card exist at the same time, the claim with the earlier timestamp wins, and the lower transport key breaks a tie. Every node applies the same rule.
-Reason: A card is one member. Two sessions with one card would receive each other's messages.
-Rejected: New claim wins and evicts the old holder: an accidental restart would steal an active session.
+Decision: A claim for a card that has a present holder is refused. If two claims for one card exist at the same time, the claim with the earlier timestamp wins, and the lower transport key breaks a tie. Every node applies the same rule. A node replaces the claim it holds for a card only after a probe: the earlier claim's node must answer, or the held claim's node must fail to answer.
+Reason: A card is one member. Two sessions with one card would receive each other's messages. A timestamp orders claims; only a probe tells a live claimant from a dead one. A session restarted after a crash carries a later timestamp and must reach Claimed; a replayed old presence carries an earlier one and must not.
+Rejected: New claim wins and evicts the old holder: an accidental restart would steal an active session. Earliest timestamp wins without a probe: a crashed holder blocks its own restart for the life of the network, and a replayed presence displaces a live member.
 If you change this: The network can hold two members with one identity and no way to tell them apart.
 
 **D7 — No lock on claim.**
-Decision: The binary takes no file lock or other local lock when it claims a card. The tie-break in D6 resolves every race.
+Decision: The binary takes no file lock or other local lock when it claims a card. The tie-break and the probe in D6 resolve every race.
 Reason: The protocol rule is sufficient and is the same on one machine and across machines.
 Rejected: An exclusive file lock on the sidecar. It would add a second mechanism for one case.
 If you change this: Nothing breaks, but there are two mechanisms for one problem.
@@ -210,7 +210,7 @@
 ### 2.6 Presence
 
 **D18 — Introduction replaces heartbeats.**
-Decision: A node that joins the topic announces its claim. A member that receives a claim from an unknown node replies with its own claim, directly to that node. Members announce again after a reconnect, and when their inbox attaches or detaches.
+Decision: A node that joins the topic announces its claim. A member that receives a claim from an unknown node replies with its own claim, directly to that node. A node introduces itself to each new gossip neighbor. Members announce again after a reconnect, and when their inbox attaches or detaches.
 Reason: A late joiner learns everyone without periodic traffic.
 Rejected: Periodic heartbeats: constant traffic that grows with the member count.
 If you change this: A late joiner sees only members that announce after it joined.
@@ -291,9 +291,9 @@
 Rejected: System frames on the inbox: breaks invariant I3.
 If you change this: An agent can keep a name that is no longer its own with no signal.
 
-**D31 — A received message has four fields.**
-Decision: An agent sees from, body, received_at, and id. Nothing else.
-Reason: The primitive is text from one member. Threads and metadata belong to the society.
+**D31 — A received message has five fields.**
+Decision: An agent sees from, body, sent_at, received_at, and id. Nothing else.
+Reason: The primitive is text from one member. The sender's clock, read by its own process, is the one stamp a receiver cannot guess. Threads and other metadata belong to the society.
 Rejected: A reply_to field: threads in the pipe.
 If you change this: Every bridge template and the inbox frame change.
 
@@ -307,7 +307,7 @@
 
 **D33 — The inbox is a Unix socket named by the process identifier.**
 Decision: Each process exposes its inbox on a socket whose path derives from its process identifier. Frames carry a sequence number. A client reconnects with the last sequence number it saw and receives what it missed, from a memory buffer.
-Reason: A bridge finds the socket through the process tree, without a file written by the binary and without agent action.
+Reason: A bridge finds the socket through the process tree, without a file written by the binary and without agent action. Any process of the same user can connect: the socket trusts the user, not the bridge.
 Rejected: A TCP port returned by the init tool: a bridge started by the harness cannot see tool results.
 If you change this: Every bridge changes its discovery.
 
@@ -331,10 +331,10 @@
 Rejected: A uniform text frame across harnesses: discards native forms that already mark the source. Batched injection: loses order of events.
 If you change this: Define the batch rule and the interruption rule for every harness.
 
-**D37 — The Claude Code bridge uses the cross-session socket, with inbound set to accept.**
-Decision: A session-start hook starts the bridge. The bridge writes each message to the socket named by CLAUDE_CODE_MESSAGING_SOCKET, with the token from CLAUDE_CODE_MESSAGING_TOKEN. Agents run with crossSessionInbound set to accept. The bridge does not register peers as local sessions, and it does not use the channels mechanism.
-Reason: The socket wakes an idle session and delivers at tool boundaries during a turn. The accept setting removes the hold that applies to sessions with permission bypass. The native tools of Claude Code for cross-session messages are replaced by the six tools.
-Rejected: Peers registered as fake local sessions: depends on undocumented session files and envelopes. Channels: a research preview, enabled per session by flag, admin-gated for teams.
+**D37 — The Claude Code bridge uses the cross-session socket, authenticated by the session token.**
+Decision: A session-start hook starts the bridge. The bridge writes each message to the socket named by CLAUDE_CODE_MESSAGING_SOCKET, opening every connection with the auth line that carries the token from CLAUDE_CODE_MESSAGING_TOKEN. No crossSessionInbound value is set for the agent session. The bridge does not register peers as local sessions, and it does not use the channels mechanism.
+Reason: The socket wakes an idle session and delivers at tool boundaries during a turn. A message that carries the session's own token is delivered as the session's own child's, without the hold that applies to peer sessions under permission bypass. The native tools of Claude Code for cross-session messages are replaced by the six tools; an accept setting would admit every other local session's native messages through the channel being replaced, and a refuse setting would drop the bridge's own frames with them.
+Rejected: Peers registered as fake local sessions: depends on undocumented session files and envelopes. Channels: a research preview, enabled per session by flag, admin-gated for teams. crossSessionInbound set to accept: widens the replaced channel instead of closing it.
 If you change this: Delivery to Claude Code sessions depends on a different mechanism with different hold rules.
 
 **D38 — The pi bridge is a pi extension.**
@@ -377,7 +377,7 @@
 
 ### 2.12 Deferred
 
-Out of scope for this design, and open: human members, movement of cards between machines, threads, status events on the inbox, any queue, lookup of unknown handles through neighbors, referral of third-party claims inside messages.
+Out of scope for this design, and open: human members, movement of cards between machines, threads, status events on the inbox, any queue, lookup of unknown handles through neighbors, referral of third-party claims inside messages, rotation and revocation of the network secret.
 
 ---
 
@@ -399,6 +399,7 @@
 | mac key | 32 bytes, derived from the network secret. See 3.4. |
 | mac | 32 bytes, the keyed BLAKE3 hash of a byte string under the mac key. |
 | handle | A string that matches `^[a-z][a-z0-9-]{0,31}$`. |
+| effective handle | A handle, or a handle followed by `-` and a decimal integer of at least 2. The `to` and `from` fields carry effective handles. |
 | fingerprint | The first 4 bytes of a card public key, encoded as lowercase base32 without padding (7 characters). Internal. |
 | message id | A UUID version 7. 16 bytes on the wire. The canonical string form in JSON. |
 | timestamp | Milliseconds since the Unix epoch, as an unsigned 64-bit integer. |
@@ -477,6 +478,8 @@
 Mac on a wire structure: encode the structure with its `mac` field set to 32 zero bytes, then compute the keyed hash of those bytes. Verify by recomputation and constant-time comparison.
 
 Tie-break between two claims for one card: the claim with the lower `ts` wins. If `ts` is equal, the claim with the lower `node`, compared as 32 bytes, wins.
+
+The tie-break orders claims; it never replaces a held claim by itself. Before a node replaces the claim it holds for a card, it probes. A claim earlier by the tie-break replaces the held claim when its node answers a Probe with that claim. A claim later by the tie-break replaces the held claim when the held claim's node fails a Probe within the probe timeout. A node that loses the tie-break for its own card enters Displaced only after the winner's node answers a Probe with the winning claim.
 
 ### 3.5 Card and sidecar
 
@@ -603,7 +606,7 @@
 }
 ```
 
-Drop any payload whose mac does not verify. Drop any Presence or Unreachable whose claim does not verify. Drop any Presence whose `claim.node` differs from the gossip sender node id. The serialized `public` field has a maximum of 4096 bytes.
+Drop any payload whose mac does not verify. Drop any Presence or Unreachable whose claim does not verify. Gossip delivers a payload through forwarders, so the node that handed a payload over is not its origin; over gossip the claim's signature is the only binding of `claim.node` to the card, and the direct-stream check of 3.6 step 4 is where a node id is a fact. The serialized `public` field has a maximum of 4096 bytes.
 
 ### 3.8 Peer table and presence algorithm
 
@@ -627,13 +630,16 @@
 
 | Event | Action |
 |---|---|
-| init succeeds | Subscribe to the topic. Send Presence. Start the direct protocol listener. |
+| process starts | Start the endpoint, the direct protocol listener, and the inbox listener. Subscribe to the topic and receive; send no payload before init. |
+| init succeeds | Send Presence. |
 | Presence received, card unknown | Insert the peer as Online. Send Introduce directly to `claim.node`. Apply handle assignment. |
-| Presence received, card known, claim newer by the tie-break order | Replace the claim. Set Online. Apply handle assignment. |
-| Presence received, card known, claim older | Ignore. |
-| Presence received for your own card from another node | Apply the tie-break of 3.4. If you lose, enter Displaced (3.9). If you win, send Presence. |
+| Presence received, card known, same node as the held claim | Update `public`, `attached`, and `last_seen`. Set Online. |
+| Presence received, card known, another node, earlier by the tie-break order | Send Probe to `claim.node`. On a ProbeAck carrying that claim, replace the held claim, set Online, apply handle assignment. On failure, ignore. |
+| Presence received, card known, another node, later by the tie-break order | Send Probe to the node of the held claim. On ProbeAck, ignore. On failure, replace the held claim, set Online, apply handle assignment. |
+| Presence received for your own card from another node | Apply the tie-break of 3.4. If you lose, send Probe to that node: on a ProbeAck carrying that claim, enter Displaced (3.9); on failure, send Presence. If you win, send Presence. |
 | Introduce or IntroduceAck received | Same as Presence received. |
-| Message received and validated | Insert or update the sender as Online with the claim of the message. |
+| Message received and validated | Treat `from` as a Presence received from `from.node`, by the rows above. |
+| gossip reports a neighbor up | Send Introduce to that node, unless it is the node of an Online entry. |
 | Departure received | Set the peer Gone. Keep the entry for 3600 seconds, then remove it. |
 | Unreachable received, about a peer | Set the peer Unreachable, unless a direct contact with that peer is more recent than `ts`. |
 | Unreachable received, about yourself | Send Presence. |
@@ -651,7 +657,7 @@
 ### 3.9 Session state machine
 
 ```
-Unclaimed --init ok--> Claimed --lost tie-break--> Displaced --init ok--> Claimed
+Unclaimed --init ok--> Claimed --lost tie-break to a live claimant--> Displaced --init ok--> Claimed
 any state --stdin closed or signal--> Stopping --Departure sent--> exit
 ```
 
@@ -687,12 +693,12 @@
 
 | Tool | Input | Result |
 |---|---|---|
-| `list_cards` | none | `cards: [{ name, handle, held: bool }]`. `held` is true when the peer table has an Online entry for that card public key. |
+| `list_cards` | none | `cards: [{ name, handle, held: bool }]`. `held` is true when the peer table has an Online entry for that card public key. On the first call after start, wait the observer wait of 3.14 before answering. |
 | `init` | `card: string`, `description?: string` | `handle: string`, `inbox_path: string`. The description, if given, is put under `public.description` in the presence of this session only. |
 | `peers` | none | `peers: [{ handle, status, attached, public: object, last_seen }]`. Excludes yourself. |
 | `send` | `to: string`, `body: string` | `id: string`, `delivered: true`, `attached: bool`. |
 | `broadcast` | `to: string[]`, `body: string` | `results: [{ to, id?, delivered: bool, attached?: bool, error?: { code, message } }]`. Sends run concurrently. |
-| `inbox` | `since?: integer` | `messages: [{ seq, id, from, body, received_at }]`, `last_seq: integer`. Returns frames with `seq` greater than `since`. Does not remove frames. |
+| `inbox` | `since?: integer` | `messages: [{ seq, id, from, body, sent_at, received_at }]`, `last_seq: integer`. Returns frames with `seq` greater than `since`. Does not remove frames. |
 
 Send algorithm:
 
@@ -740,7 +746,7 @@
 Server frames, one per message, in `seq` order:
 
 ```json
-{"seq": 12, "id": "<message id>", "from": "<effective handle>", "body": "<text>", "received_at": 1700000000000}
+{"seq": 12, "id": "<message id>", "from": "<effective handle>", "body": "<text>", "sent_at": 1700000000000, "received_at": 1700000000000}
 ```
 
 The server sends every buffered frame with `seq` greater than `N`, then live frames as they arrive. The buffer holds the last 1000 frames. `seq` starts at 1 and increases by 1 per message for the life of the process. The server writes nothing else on this socket.
@@ -761,7 +767,7 @@
 Notice content: the native form of the harness where one exists. In every form, the source must be visible as a peer, never as the owner of the session. Template for text form:
 
 ```
-Message from peer <handle> (verified member of your network).
+Message from peer <handle> (verified member of your network), sent <sent_at as ISO 8601, UTC>.
 <body>
 Reply with the send tool.
 ```
@@ -772,8 +778,8 @@
 
 - Hook configuration: a SessionStart hook starts the bridge executable detached from the hook. The hook passes the values of `CLAUDE_CODE_MESSAGING_SOCKET` and `CLAUDE_CODE_MESSAGING_TOKEN` and the process id of the parent of the hook.
 - Injection: open a connection to the socket for each message. Write one line `{"type":"auth","token":"<token>"}`. Write one line with the message in the format that socket accepts. Close. Open the connection only when a message is ready.
-- Settings: the agent session has `crossSessionInbound` set to `accept`.
-- Doctor: the hook is installed, the bridge process runs for this session, the socket path exists, the setting is `accept`, and at least one binary process was found.
+- Settings: no `crossSessionInbound` value is set for the agent session. `refuse` would drop the bridge's frames; `accept` would admit every other local session's native messages.
+- Doctor: the hook is installed, the bridge process runs for this session, the socket path exists, no `refuse` applies to the session, and at least one binary process was found.
 
 pi bridge:
 
@@ -839,6 +845,9 @@
 15. The observer command on a machine with no active session shows the peers of the other machines.
 16. A card whose sidecar has permissions 0644 fails init with `sidecar_invalid`.
 17. A retried send with the same message id after a lost ack produces one inbox frame, not two.
+18. B is killed with SIGKILL and restarted with the same card. Within one probe timeout of the new presence, A's `peers` shows B online at the new node, and A's send to B is delivered.
+19. Three nodes, with C a gossip neighbor of B only. A's `peers` shows C within the observer wait.
+20. A replayed Presence of B's earlier session, with an earlier timestamp and a dead node, changes nothing in A's table.
 
 ### 3.16 Do not
 
@@ -854,6 +863,7 @@
 - Do not push anything but message frames on the inbox socket.
 - Do not accept a Message whose claim node differs from the connection node id.
 - Do not add a lock file, a pid file, or a registry index.
+- Do not replace a held claim without a probe.
 - Do not let the bootstrap member hold a card or forward a message.
 - Do not put fingerprints or keys in the `to` or `from` fields.
 - Do not rate limit in the binary.
```
