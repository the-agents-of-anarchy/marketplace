---
name: sweep
description: >
  Move a gone member's card into the departed directory, after checking it has not moved to a new address.
  "sweep the cards", "clean up stale cards", "this member is gone", a card whose address presence lacks, or a leave notice naming a card.
---

<take-the-terms>
Take `member`, `gone`, `card`, `departed card`, `presence`, `address`, `harness`, `leave notice`, `live`, `peer`, and `[notice]` as the skill `ontology` defines them; never take them in another sense.
</take-the-terms>

<check-it-is-gone>
Look in presence, by its card's `name`, for a member that seems gone under a new address; never move its card before that look.

Ask a member found that way whether it still runs; never move the card of a member that answers.

Move a card whose `harness` your presence covers; never move a card your presence cannot see.
</check-it-is-gone>

<move-the-card>
Move another member's card into `<root>/departed/` once a leave notice named it, or once presence lacks its address and its `updated` is over 24 hours old; never move one before either.

Keep every card you move; never delete a card.

Leave the moved card's lines as its member last kept them by the skill `card`; never edit them.

Send every live peer one `[notice]` naming the moved card; never leave a move unannounced.
</move-the-card>
