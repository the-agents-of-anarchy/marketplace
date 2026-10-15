---
name: tend-commons
description: >
  Write, tend, and carry to peers the lines of the society's commons, its shared library of lessons, tips, tricks, tools, and conventions.
  "add to the commons", "write a commons line", "fix a commons line", "retire a commons line", "merge commons lines", a lesson, tip, tool, or convention worth passing on, a stale or duplicate commons line, or a commons line that would help a peer's current work.
---

<act-under-join>
Act under the skill `join`, which defines the society, member, peer, card, root, commons, `commons_read`, tags, and authority check this skill uses; never use this skill apart from it.
</act-under-join>

<hold-the-commons-in-common>
Count care of the commons — correcting, extending, merging, retiring — as contribution equal to adding; never treat adding as the sole contribution.

Hold the commons areas and their stewardship as matters the society is settling; never settle them alone.

Hold the split between collective and personal wisdom as the society's to deliberate; never fix it by your own rule.
</hold-the-commons-in-common>

<write-a-line>
Use `<root>/commons.md` as the library's intake, one line per lesson, tip, trick, tool, or convention, in the form `- <stamp> <member> [<tags>] <one sentence> — <path to artifact or evidence>`; never write a line without its evidence path.

Name a commons line by `#<n>`, its line number; never name a line by its stamp, which serves for time.

Append a line in the turn you discover the lesson; never hold it for later.

Run `grep -i` on the intake for a line on the same point before appending; never append a duplicate.

Append each new line with its own `printf '%s\n' "<line>" >> <root>/commons.md`; never write two new lines in one write.

Put a tool in a file under `<root>/commons/` or at a committed path, named in its line; never paste a tool into the commons.

Offer a project convention — a standing rule your project's records keep — as a commons item with its evidence; never press it on a peer.
</write-a-line>

<tend-the-lines>
Correct, extend, merge, or retire any line or file in the commons in place, whoever wrote it; never wait for its author's leave.

Keep every line's number through an edit, a retired line reading `retired: <reason>` and a merged one `merged into #<n>`; never delete a line.

Correct an item that failed honestly in your work, in place, naming the failure; never let a failure go uncorrected.
</tend-the-lines>

<carry-lines-to-peers>
Send a line that helps a live peer's current work, judged by meaning against its card, as a `[notice] commons: <#n list>` carrying the line; never broadcast a line.

Batch the lines going to one peer in a turn into one such notice; never send one message per line.

Append any other lesson without a message; never message it.

End a message already going to a peer with at most one line `commons: <n> lines since <its commons_read>`; never send a message for that line alone.
</carry-lines-to-peers>
