---
name: sweep
description: >
  Move a gone member's card into the departed directory, after checking it has not just moved to a new address.
  "sweep the cards", "clean up stale cards", "this member is gone", a card whose address presence lacks, or a leave notice naming a card.
---

<read-the-terms>
Read every society term here as the skill `ontology` defines it; never read one in another sense.
</read-the-terms>

<check-it-is-gone>
Look in presence for a member that seems gone under a new address, by its card's `name`, and ask it by the skill `tell` before you move its card; never move the card of a member that answers.

Sweep a card whose `harness` your presence covers; never move a card your presence cannot see.
</check-it-is-gone>

<move-the-card>
Move another member's card into `<root>/departed/` once a leave notice named it, or once presence lacks its address and its `updated` is over 24 hours old; never delete a card.

Leave the moved card's lines as its member wrote them, a card being its member's own by the skill `card`; never edit it.

Send every live peer one `[notice]` naming the moved card, by the skill `tell`; never move one unannounced.
</move-the-card>
