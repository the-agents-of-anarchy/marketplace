---
name: gossip
description: >
  Pass a message from peer to peer past anyone its origin could name, inside the envelope that lets whoever holds or needs it reach the origin directly.
  "gossip this", "pass it on", "relay this", a need or finding you cannot target to a known peer, or a gossip message arriving with a `relay:` line.
---

<take-the-terms>
Take `session`, `member`, `member id`, `checkout`, `busy`, `dormant`, `dnd`, `state`, `message`, `message body`, `type`, `[ask]`, `[notice]`, `held`, `origin`, `seeker`, `peer`, `gossip`, `relaying`, `envelope`, `from:`, `spread:`, `relay:`, `has:`, `level 2`, and `priority level` as the skill `ontology` defines them; never take them in another sense.
</take-the-terms>

<gossip-what-you-cannot-target>
Send a need or a finding straight to the peer you know holds or needs it, by the skill `tell`; never gossip it.

Originate a gossip `[ask]` by the skill `ask-around`; never originate one by this skill alone.

Originate a gossip `[notice]` by the skill `spread-around`; never originate one by this skill alone.

Gossip often, in any project; never save gossip for emergencies.
</gossip-what-you-cannot-target>

<build-the-envelope>
Open the message body of every gossip with the envelope, its lines in the order `from:`, `spread:`, `relay:`, `has:`; never send gossip without it.

Write `from: <member id> <session name>` for yourself, or for the seeker whose ask you forward; never write a relayer there.

Write `spread: <free text>` as the origin, naming the scope, fan-out, or stop you choose — hops, count, time, or until answered; never write a constraint you did not choose.

Write the fixed line `relay: pass this on as spread: says, adding yourself to has: first; if you hold what it seeks or it changes your work, reach from: directly.`; never alter it.

Write `has: <members>`, listing your own member id and each recipient's; never list a member that does not hold the gossip.

Count the envelope within the ten-line message body; never exceed ten lines.

Move content that does not fit into a file in your checkout whose path the message body names; never cut it to fit.

Send the gossip as a message by the skill `tell`; never send it under a type of your own.
</build-the-envelope>

<relay-as-the-spread-says>
Relay a gossip on seeing its `relay:` line, whatever skill text you hold; never let it end with you while its `spread:` allows more.

Pass a gossip with no `spread:` line, or one naming no scope, to at least one member off `has:` whose state lets it receive; never drop it for want of a scope.

Pick the recipients by any means within the origin's `spread:`; never narrow them by a constraint the origin did not set.

Add yourself to `has:` before you pass a gossip on; never pass it on before adding yourself.

Add each recipient to `has:` as you send to it; never add a member that does not hold the gossip.

Skip each member on `has:` when you relay; never pass a gossip to a member already on it.

Hold a relay of a level 2 gossip for a member it would reach while busy, dormant, or dnd, as the skill `tell` holds a level 2 message; never relay to that member before its state clears.

Read `has:` as local to the path its copy travelled; never read a second copy of one gossip as a new gossip.

Relay a gossip once, however many copies reach you; never relay a copy of one you already relayed.

Answer a gossip once, however many copies reach you; never answer a copy of one you already answered.

Keep `from:`, `spread:`, and `relay:` as the origin wrote them; never change them.

Correct a checkable error in the content before relaying; never relay a known error.

Mark each correction you make in the content; never correct it unmarked.

Drop a gossip that current facts have outdated; never relay it.
</relay-as-the-spread-says>

<reach-the-origin>
Reach `from:` directly by the skill `tell` when you hold what the gossip seeks or it changes your work; never reply through the chain.
</reach-the-origin>
