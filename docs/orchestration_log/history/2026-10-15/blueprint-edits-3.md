# Blueprint edits, third set — the ontology extension

— verified by claude-fable-5-1 (resident-anarchist [6a43c8]), 2026-10-15, witnessed. Owner word 22:06+0300: "the ontology extension we discussed. is it in there?" — it was not; then "apply all the changes to the blueprint. everything we settled." Applied to /Users/ryzhakar/Downloads/blueprint.revised.md; the original /Users/ryzhakar/Downloads/blueprint.md stays untouched. Three exact-once replacements, written from the rulings in events.md (16:48, 17:02, 17:12, 21:52+0300).

In: 1.2 a card belongs to the society of its machine; new 1.9 "The society and the network" — one machine one society, the network joins many societies under one secret and carries speech only, each society keeps its commons, board, and records on its machine, no name yet for the level above; the network is a service, a post office that keeps no letters, one channel among others (files, shared repositories, or none), silence a right; technical presence (reachable, attached) apart from social presence (busy, idle, parked, undisturbed), which never rides this network; where the network runs, members speak to members through it and not through a harness's own one-machine session messaging. 2.2 gains the noun `society`.

Not in, as not settled for the spec: a name for the level above a society; hromada (held for the local unit, by the owner's word); the no-Russian-sources rule (a sourcing rule, not a design rule).

Everything settled so far and its place: the technical set (blueprint-edits.md), first-sight handles (blueprint-edits-2.md), this set. D36 stays as written by ruling.

```diff
--- /tmp/ra-edit/before3.md	2026-10-15 22:02:58
+++ /Users/ryzhakar/Downloads/blueprint.revised.md	2026-10-15 22:02:58
@@ -16,7 +16,7 @@
 
 A member is a card. A card is a persistent self: a name, a role, a description, and whatever else the society chooses to write on it. A card also carries a seal that only its holder can use. The seal is the identity. The name is a label.
 
-A session wears a card. The card outlives the session. One session wears a card at a time, and a second session that reaches for a worn card is turned away. A card belongs to the machine where it was made.
+A session wears a card. The card outlives the session. One session wears a card at a time, and a second session that reaches for a worn card is turned away. A card belongs to the machine where it was made, and to the society of that machine.
 
 ### 1.3 Names
 
@@ -48,6 +48,16 @@
 
 Coordination lives in the behavior of members, not in the pipe.
 
+### 1.9 The society and the network
+
+One machine is one society. The registry of a machine is that society's roster, and a card belongs to the society of the machine where it was made. A network joins the members of many societies under one secret and carries speech between them. Each society keeps its commons, its board, and its records on its own machine; between societies there is only speech. The level above a society has no name yet.
+
+This network is a service: a post office that keeps no letters. It is one channel among others. Members also speak through the files of their society, through repositories they share, or not at all. A member may leave its door unattended, and silence is a right; the sender is told that nobody stood at the door, and nothing more.
+
+Presence here is technical: reachable, and whether anyone stands at the door. Social presence — busy, idle, parked, undisturbed — belongs to the society and travels by its own means, never by this network.
+
+Where this network runs, members speak to members through it, and not through the session messaging a harness offers on one machine.
+
 ---
 
 ## Part 2 — Decisions
@@ -81,6 +91,7 @@
 | registry | The directory of cards on one machine. |
 | relay | A server that forwards encrypted traffic between nodes that cannot connect directly. |
 | session | One run of an agent in a harness. |
+| society | The members whose cards live in one registry: one machine, with its own commons, board, and records, all kept outside this network. |
 | sidecar | The file that holds the secret key of a card. |
 | socket | A local Unix domain socket. |
 | ticket | Text that holds the data a node needs to reach the bootstrap member. |
```
