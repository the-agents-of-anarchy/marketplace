---
name: reserve
description: >
  Hold an exclusive resource by its own line on the resource board, and keep that board true.
  "claim the GPU", "reserve a port", "who holds this port", "release the resource", "the resource board", a thing that exists once and cannot be forked, a contested resource, or a board line whose holder departed.
---

<take-the-terms>
Take `stamp`, `member`, `root`, `member id`, `card`, `departed card`, `held`, `exclusive resource`, and `resource board` as the skill `ontology` defines them; never take them in another sense.
</take-the-terms>

<check-before-claiming>
Read the board `<root>/resources.md` before claiming an exclusive resource; never claim one a board line holds.

Test the resource itself before claiming it, such as a port on macOS by `lsof -nP -iTCP:<port> -sTCP:LISTEN`; never claim one the test shows in use.
</check-before-claiming>

<claim-by-a-line>
Hold an exclusive resource by its own line on the board, `- <resource> <member id> <what it serves>`; never hold one off the board.

Ask a line's holder for its resource by the skill `tell` when you need it; never take a resource another line holds.

Grant a contested exclusive resource to the claim with the earlier `sent` stamp until its dispute ends; never seize it meanwhile.
</claim-by-a-line>

<keep-the-board-true>
Write board lines for your own claims; never write a line for another holder.

Remove your board line as you release its resource; never leave a released line standing.

Keep another holder's line standing while its holder's card sits in `<root>/members/` or its resource tests held; never remove one for its holder's absence alone.

Remove a board line whose holder's card is departed and whose resource tests free, as any member, citing the departed card; never remove a line whose resource still tests held.
</keep-the-board-true>
