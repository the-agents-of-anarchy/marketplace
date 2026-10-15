# Blueprint edits, fourth set — one owner, society-blind transport

— verified by claude-fable-5-1 (resident-anarchist [6a43c8]), 2026-10-15, witnessed. From the owner's rulings of 22:24+0300 on items 3 and 4 of federation-prep-rulings.md. Four exact-once replacements on /Users/ryzhakar/Downloads/blueprint.revised.md; original untouched.

```diff
--- /tmp/ra-edit/before4.md	2026-10-15 22:13:24
+++ /Users/ryzhakar/Downloads/blueprint.revised.md	2026-10-15 22:13:24
@@ -58,6 +58,10 @@
 
 Where this network runs, members speak to members through it, and not through the session messaging a harness offers on one machine.
 
+A network has one owner. Every member of it works for that one human, whose machines alone hold the secret; the trust between members rests on that, and a machine of another owner is another network.
+
+The transport is a primitive. It carries no social meaning: no bridge reads a body for what it means, no presence carries a state of attention, and nothing of the society reaches into the transport beyond the public fields of a card and the text of a message.
+
 ---
 
 ## Part 2 — Decisions
@@ -189,7 +193,7 @@
 If you change this: Delivery loses its ack, and the ack is the whole delivery guarantee.
 
 **D13 — A network is a secret. The secret is set once per machine.**
-Decision: An operator command stores the secret for a named network on the machine. The MCP mode uses the stored secret. The topic identifier and the message authentication key derive from the secret.
+Decision: An operator command stores the secret for a named network on the machine. The MCP mode uses the stored secret. The topic identifier and the message authentication key derive from the secret. The secret of a network is set only on the machines of its one owner.
 Reason: Membership is possession of the secret. The MCP mode needs no configuration of its own.
 Rejected: Open networks: anyone who finds a node can join. Invitations signed by members: more machinery and a social process.
 If you change this: Define membership again, and define how a node proves it to another node.
@@ -337,7 +341,7 @@
 If you change this: Invariant I1 breaks.
 
 **D36 — A bridge injects one message per frame, in the native notice form of its harness, with its own mid-turn policy.**
-Decision: A bridge injects each inbox frame as one notice. Where the harness has a notice form that is not user input, the bridge uses it. The bridge decides whether a message interrupts a turn or waits for a boundary.
+Decision: A bridge injects each inbox frame as one notice. Where the harness has a notice form that is not user input, the bridge uses it. The bridge decides whether a message interrupts a turn or waits for a boundary. The bridge reads no meaning from a body.
 Reason: Harnesses differ. The one rule that must hold everywhere is that a peer message never looks like the owner of the session.
 Rejected: A uniform text frame across harnesses: discards native forms that already mark the source. Batched injection: loses order of events.
 If you change this: Define the batch rule and the interruption rule for every harness.
@@ -786,7 +790,7 @@
 Reply with the send tool.
 ```
 
-Rate limit, per sender handle: at most 10 injections in any 60 seconds, and no injection of a body identical to the previous body from that sender within 30 seconds. Count dropped frames and report them in the doctor output of the bridge.
+Rate limit, per sender handle: at most 10 injections in any 60 seconds, and no injection of a body identical to the previous body from that sender within 30 seconds. Count dropped frames and report them in the doctor output of the bridge. A bridge applies no policy that depends on the content of a body beyond its identity with the previous one.
 
 Claude Code bridge:
 
```
