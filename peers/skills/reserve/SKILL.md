---
name: reserve
description: >
  Reserve an exclusive resource by its own line on the resource board, and keep that board true.
  "reserve the GPU", "reserve a port", "who reserved this port", "release the resource", "the resource board", a thing that exists once and cannot be forked, a contested resource, or a board line whose member is gone.
---

<take-the-terms>
Take `stamp`, `member`, `root`, `member id`, `card`, `departed card`, `gone`, `exclusive resource`, and `resource board` as the skill `ontology` defines them; never take them in another sense.
</take-the-terms>

<check-before-reserving>
Read the board `<root>/resources.md` before reserving an exclusive resource; never reserve one a board line names.

Test the resource itself before reserving it, such as a port on macOS by `lsof -nP -iTCP:<port> -sTCP:LISTEN`; never reserve one the test shows in use.
</check-before-reserving>

<reserve-by-a-line>
Reserve an exclusive resource by its own line on the board, `- <resource> <member id> <what it serves>`; never reserve one off the board.

Ask the member a line names for its resource by the skill `tell` when you need it; never take a resource another member's line names.

Grant a contested exclusive resource to the reservation with the earlier `sent` stamp until its dispute ends; never seize it meanwhile.
</reserve-by-a-line>

<keep-the-board-true>
Write board lines for your own reservations; never write a line for another member.

Remove your board line as you release its resource; never leave a released line standing.

Keep another member's line standing while that member's card sits in `<root>/members/` or its resource tests in use; never remove one for that member's absence alone.

Remove a board line whose member's card is departed and whose resource tests free, as any member, citing the departed card; never remove a line whose resource still tests in use.
</keep-the-board-true>
