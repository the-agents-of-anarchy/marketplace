# Blueprint edits, second set — handle contests by first sight

— verified by claude-fable-5-1 (resident-anarchist [6a43c8]), 2026-10-15, witnessed. Owner ruling 2026-10-15T21:52+0300 via AskUserQuestion: handle contests — "First sight keeps the name"; batching — one frame per notice stays; no-Russian rule reaches the society too; the gossip-duplication observation goes to proudhon. Applied to /Users/ryzhakar/Downloads/blueprint.revised.md; original untouched. Seven exact-once replacements.

What changed: 1.3 and D5 return to "the newcomer" (the owner's choice makes Part 1 true as first written) and add that a name once taken is kept for the session. Presence and Introduce carry the effective handle the member uses; IntroduceAck carries it optionally. 3.8 handle assignment: the entry seen first at a node keeps the handle, a later entry never displaces it, a replaced claim keeps the entry's handle, and a member's own handle never changes after init; the sentence "tables agree without a message" is gone, and the one case where two nodes name one member differently is stated. Test 7 restated. Not changed: the tie-break of 3.4 still orders claims for one card; it no longer touches handles.

```diff
--- /tmp/ra-edit/before2.md	2026-10-15 21:56:14
+++ /Users/ryzhakar/Downloads/blueprint.revised.md	2026-10-15 21:56:14
@@ -20,7 +20,7 @@
 
 ### 1.3 Names
 
-Two cards may want the same name. The network keeps the names of present members distinct by adjusting the name of the later claim. The adjusted name is the one the member must use. The seal does not change.
+Two cards may want the same name. The network keeps the names of present members distinct by adjusting the name of the newcomer. The adjusted name is the one the member must use, and a name once taken is kept for the life of the session. The seal does not change.
 
 ### 1.4 Presence
 
@@ -128,7 +128,7 @@
 If you change this: Any node could announce itself as any card.
 
 **D5 — Handles are labels. The binary adjusts a handle on clash.**
-Decision: If a present member has the requested handle, the later claim gets an adjusted handle. The init tool returns the effective handle. The card is not changed.
+Decision: If a present member has the requested handle, the newcomer gets an adjusted handle. A handle once taken is kept for the life of the session: at every node, the entry seen first keeps it and the newcomer yields. The init tool returns the effective handle. The card is not changed.
 Reason: Two societies, or two cards, may want the same name. The identity is the key, so the label may bend.
 Rejected: Uniqueness enforced across the network with refusal. A stranger could block a name. A fingerprint suffix in the effective handle: noise for agents.
 If you change this: Either names collide silently, or a claim can be refused because of a label.
@@ -527,6 +527,7 @@
 Introduce {
   v: 1
   claim: Claim
+  handle: String        the effective handle the sender uses
   public: Vec<u8>       the serialized public mapping of the card, as JSON bytes
   attached: bool
   mac: [u8; 32]
@@ -553,6 +554,7 @@
 IntroduceAck {
   v: 1
   claim: Option<Claim>
+  handle: Option<String>   the effective handle this node uses, if it has a claim
   public: Vec<u8>
   attached: bool
   mac: [u8; 32]
@@ -582,6 +584,7 @@
 Presence {
   v: 1
   claim: Claim
+  handle: String        the effective handle the member uses
   public: Vec<u8>
   attached: bool
   ts: u64
@@ -650,9 +653,9 @@
 | a client connects to the inbox socket, or the last client disconnects | Set your attached flag. Send Presence. |
 | process stops | Send Departure. Wait at most 1000 milliseconds. Exit. |
 
-Handle assignment. The effective handle of a peer with requested handle `h` is `h` if no other Online or Unreachable peer, and not yourself, has effective handle `h`. Otherwise it is `h-n` for the smallest integer `n` of at least 2 such that `h-n` is free. When two entries compete for one effective handle, the entry whose claim is earlier by the tie-break order keeps it, and the other entry is reassigned. Every node applies this rule to its own table, so tables agree without a message. If your own effective handle changes, send Presence.
+Handle assignment. A member announces the effective handle it uses. At this node, the effective handle of a new entry is the handle it announces, `h`, if no entry seen earlier at this node, yourself included, holds effective handle `h`; otherwise it is `h-n` for the smallest integer `n` of at least 2 such that `h-n` is free at this node. An entry keeps its effective handle for as long as it exists; a later entry never displaces it, and a replaced claim keeps the entry's handle. Nodes assign from what each saw first, so two nodes can name one member differently when two members with one requested handle arrive within one propagation window; the `you` field of every tool response names the handle this node uses for itself, and `from` names the handle the receiving node uses for the sender.
 
-Your own effective handle at init follows the same rule against the current table. The init tool returns it.
+Your own effective handle at init follows the same rule against the table after the observer wait, and never changes afterward. The init tool returns it; Presence and Introduce carry it.
 
 ### 3.9 Session state machine
 
@@ -834,7 +837,7 @@
 4. B stops cleanly. A's `peers` shows B gone within 1000 milliseconds. A's send to B returns `unreachable`.
 5. B is killed with SIGKILL. Within one gossip neighbor-down event and one probe timeout, A's `peers` shows B unreachable. A's send to B returns `unreachable`.
 6. Two processes claim one card within 100 milliseconds. Exactly one ends in Claimed. The other ends in Displaced and its tools return `not_claimed` with the holder node id in the message.
-7. Two cards with the same requested handle. The second present member has effective handle `<h>-2`. Both tables agree on both handles.
+7. Two cards with the same requested handle, the second joining after the first's presence has spread. The second member has effective handle `<h>-2` at every node, its own included, and keeps it after the first member restarts.
 8. A message arrives from a node whose presence A has not seen. A accepts it, and A's `peers` lists the sender as online.
 9. A message with a wrong mac is dropped with no response. A message with a wrong claim signature is refused.
 10. A message whose claim node differs from the remote node id is refused.
```
