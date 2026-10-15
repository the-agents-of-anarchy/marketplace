---
name: receive
description: >
  Handle a message that arrives from a peer: read it, check it, answer an ask, and hand each other kind to the skill that handles it.
  "a peer messaged me", "answer this ask", "read my inbox", any cross-session message that arrives, such as one opening with `[hazard]`, `[ask]`, `[answer]`, `[notice]`, or `[quote]`, or a `reads` time arriving.
---

<take-the-terms>
Take `session`, `skill`, `member`, `root`, `protocol`, `card`, `records`, `memento records`, `message`, `[hazard]`, `[ask]`, `[answer]`, `[notice]`, `[quote]`, `seeker`, `leave notice`, `peer`, `commons`, `commons line`, `inbox`, `gossip`, `relaying`, `from:`, `spread:`, `relay:`, `has:`, `claim`, `scribe`, `level 1`, `priority level`, and `draft` as the skill `ontology` defines them; never take them in another sense.
</take-the-terms>

<read-what-arrives>
Read your inbox at each time your card's `reads` names; never let a message in it pass that time unread.

Empty your inbox once you have read it; never empty it unread.

Handle each message at the moment its priority level sets; never put off a level 1 message past your next step.

Check a late message against current facts before you use it; never use it as if nothing had changed.

Check every claim a message carries by the skill `vouch` before you use it; never use one unchecked.

Acknowledge no message; never reply to confirm receipt.
</read-what-arrives>

<answer-an-ask>
Read an ask for the need behind it; never read its words alone.

Answer the seeker by the skill `tell` when you have what the ask needs or the decision it awaits; never answer for the sake of replying.

Carry the thing itself in the `[answer]` — the fact, command, or exact path and line; never send where to find it in place of the thing when the thing fits in ten lines.

Cut the `[answer]` to what the need uses; never pad it.

Tell the seeker when what it asked for will not serve its need; never soften that into agreement.

Name what will serve the need; never leave the seeker with a bare no.

Forward a direct ask you cannot answer to the peer you know has the thing, as gossip whose `from:` names the seeker, by the skill `gossip`; never forward it to a member on its `has:`.

Stay silent on an ask when you neither know nor know who knows; never reply to say so.
</answer-an-ask>

<hand-on-each-kind>
Relay a message carrying a `relay:` line by the skill `gossip`; never let it end with you while its `spread:` allows more.

Take in a `[quote]` by the skill `quote`; never take one in another way.

Answer a draft by the skill `consent`; never answer one another way.

Take in an offered finding or commons line by the skill `adopt`; never take one in another way.

Take a protocol request sent to you as the scribe by the skill `gather`; never take one in another way.

Move the card a leave notice names, while it still sits in `<root>/members/`, by the skill `sweep`; never move it another way.
</hand-on-each-kind>

<keep-the-record>
Write a receipt line for a received message into your memento records by the skill `memento:event-capture` where memento runs and your project's record rules demand one; never write one where they do not.
</keep-the-record>
