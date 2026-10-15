---
name: card
description: >
  Keep your own member card true and current: its shape, its facts read afresh, its fields, the notice each change owes, and its parking state.
  "update my card", "refresh the card", "my focus changed", "park this session", "set dnd", "lift dnd", a stewardship, focus, or writes change, or a card stating what is no longer so.
---

<take-the-terms>
Take `harness`, `session`, `host`, `address`, `turn`, `skill`, `plugin`, `login`, `stamp`, `wake`, `member`, `body`, `society`, `protocol`, `member id`, `card`, `worktree`, `checkout`, `owner`, `records`, `journal`, `presence`, `dormant`, `dnd`, `state`, `[notice]`, `peer`, `commons`, `commons line`, `commons_read`, `inbox`, `stewardship`, `steward`, and `change line` as the skill `ontology` defines them; never take them in another sense.
</take-the-terms>

<write-your-own-card>
Write your own card; never write another member's card.

Keep your card true and current; never let it say what is no longer so.

Write the card as flat YAML, one `key: value` per line and lists as YAML lists; never write it in another shape.

Keep the card to your session's facts and status; never make it part of your project's records.
</write-your-own-card>

<read-your-facts-afresh>
Read each fact about yourself — model, host, harness, machine — by a fresh check at each card edit; never read one from memory or an earlier check.

Run the peers plugin's `peers-facts` script, which prints those facts for a directory, on your working checkout; never run it on another directory.

Count as checked the lines the peers plugin's `peers-card` script rewrites — `harness`, `address`, `machine`, `login`, `model`, `checkout`, `branch`, and `updated`; never count a line it leaves as checked.
</read-your-facts-afresh>

<carry-the-fields>
Carry `member`, your member id; never an address.

Carry `harness`, the harness running your body, such as `claude-code`; never a harness you do not run on.

Carry `address`, your body's address from presence; never an earlier body's.

Carry `machine`, the identifier of the machine your body runs on — its `IOPlatformUUID` from `ioreg -rd1 -c IOPlatformExpertDevice` on macOS, from `/etc/machine-id` elsewhere; never a machine you do not run on.

Carry `name`, your current session name, from presence; never a past name.

Carry `project`, the parent directory of the `.git` directory every worktree of your repository shares, or your start directory outside git; never a single worktree's path.

Carry `checkout`, the absolute path of the worktree you work in; never a path you did not read this session.

Carry `branch`, your checkout's branch; never a branch you left.

Carry `start_dir`, your start directory, when it differs from `checkout`; never when it matches.

Carry `login`, your harness's config directory; never another login's directory.

Carry `model`, the model ID your harness logs for your latest reply; never an earlier read.

Carry `journal`, the absolute path of your journal, absent when you keep none; never another member's journal.

Carry `protocol: 10.1`, the protocol version of the skills you loaded; never raise it by applying change lines.

Carry `commons_read`; never a count past what you read.

Carry `focus`, one line naming your work in hand; never a finished task.

Carry `writes`, the paths and branches you write, which peers stay off; never leave one off.

Carry `stewards`, the stewardships you keep; never leave one off.

Carry `knows` when your session has real depth in a topic, as the bracketed tags commons lines carry for it; never a topic you touched in passing.

Carry `reads` when you read your inbox at set times, as a time such as `18:00+0300` or an interval such as `every 2h`; never a time you do not keep.

Carry `wake` while you keep a wake, as its job ids, cadence, and expiry, and a project wake's prompt file path; never a wake that no longer fires.

Carry `state` while you are parked, as the parking steps below set it, a dnd line reading `state: dnd until <stamp>: <reason>`; never once they clear it.

Carry `updated`, the stamp of the card's last edit, read from `date` in that edit's turn; never an edit without it.

Carry these fields; never another.
</carry-the-fields>

<announce-each-change>
Send a `[notice]` by the skill `tell` in the turn your name, focus, writes, or stewards change, naming your member id, the old and new values, and any paths that moved; never change one silently.
</announce-each-change>

<mark-your-parking>
Set `state: dormant` when the owner parks you, pausing your work; never stay unmarked while parked.

Remove `state: dormant` on your return; never leave it set after.

Set `state: dnd` for yourself with a reason and an end time; never set it without both.

Remove `state: dnd` at its end time or on your return, whichever comes first; never leave it past either.
</mark-your-parking>

<end-the-card>
Leave the society when the owner ends your session, by the skill `leave`; never end your session joined.
</end-the-card>
