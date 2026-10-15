---
name: card
description: >
  Keep your own member card true and current: its fields, its facts read afresh, its parking state, and the notice each change owes.
  "update my card", "refresh the card", "my focus changed", "park this session", "set dnd", "lift dnd", a stewardship, focus, or writes change, or a card stating what is no longer so.
---

<read-the-terms>
Read every society term here as the skill `ontology` defines it; never read one in another sense.
</read-the-terms>

<write-your-own-card>
Write your own card; never edit another member's card.

Keep your card true and current, as flat YAML with one `key: value` per line and lists as YAML lists; never let it state what is no longer so.

Keep the card as session plumbing; never turn it into a project record.
</write-your-own-card>

<read-your-facts-afresh>
Read each fact about yourself — model, host, harness, machine — afresh at each card edit, by any robust means; never state a fact no check in that edit gave you.

Use the peers plugin's `peers-facts` script as one such means: given a directory, the current one by default, it prints the stamp, host, machine, harness, model, session id, login, checkout, branch, project, project name, declared manifesto stack, and root for it; never run it on a directory other than your working checkout when you fill your card.

Use the peers plugin's `peers-card` script as one means to refresh your card: given your harness-ref and card path, it rewrites the card's existing `harness`, `address`, `machine`, `login`, `model`, `checkout`, `branch`, and `updated` lines from `peers-facts` and leaves every other line as you wrote it; never count a line it leaves as checked.
</read-your-facts-afresh>

<carry-the-fields>
Carry `member`, your member id; never an address.

Carry `harness`, the harness running your body, such as `claude-code`; never a harness you do not run on.

Carry `address`, your body's address from presence; never an earlier body's.

Carry `machine`, the identifier of the machine your body runs on — its `IOPlatformUUID` from `ioreg -rd1 -c IOPlatformExpertDevice` on macOS, from `/etc/machine-id` elsewhere; never a machine you do not run on.

Carry `name`, your current session name, from presence; never a past name.

Carry `project`, the parent directory of the git common directory every worktree of your repository shares, or your start directory outside git; never a single worktree's path.

Carry `checkout`, the absolute path of the worktree you work in; never a path you did not read this session.

Carry `branch`, your checkout's branch; never a branch you left.

Carry `start_dir`, your start directory, when it differs from `checkout`; never when it matches.

Carry `login`, your harness's config directory; never another login's directory.

Carry `model`, the model ID your harness records on your latest reply; never carry an earlier read.

Carry `journal`, the absolute path of the event log that memento, the plugin keeping each session's journal and notes, writes for your session, absent when you keep none; never another session's log.

Carry `protocol: 10`, the protocol version of the skills you loaded; never raise it by applying change lines.

Carry `commons_read`; never set it past what you read.

Carry `focus`, one line naming your work in hand; never a finished task.

Carry `writes`, the paths and branches you write, which peers stay off; never leave one off.

Carry `stewards`, the shared things you look after for every session; never leave one off.

Carry `knows`, at your choice, as the commons tag words for topics your session has real depth in; never list a topic you touched in passing.

Carry `reads`, at your choice, as a time such as `18:00+0300` or an interval such as `every 2h` at which you read your inbox; never name a time you do not keep.

Carry `state: dormant` while the owner parks you, `state: dnd` while the owner orders you left undisturbed, and no `state` otherwise; never leave it stale.

Carry `wake`, at your choice, as your recurring wake's job ids, cadence, and expiry; never list a wake that no longer fires.

Carry `updated`, the stamp of the card's last edit, read from `date` in that edit's turn; never leave an edit without it.

Carry these fields; never add another.
</carry-the-fields>

<announce-each-change>
Send a `[notice]` by the skill `tell` in the turn your name, focus, writes, or stewards change, naming your member id, the old and new values, and any paths that moved; never change one silently.
</announce-each-change>

<mark-your-parking>
Set `state: dormant` when the owner parks you; never stay unmarked while parked.

Remove `state: dormant` on return; never leave it stale.

Set `state: dnd` when the owner orders it; never set it on your own judgment.

Remove `state: dnd` when the owner lifts it; never remove it on your own judgment.

Keep your recurring wake as the skill `heartbeat` set it while you are parked; never end it for parking alone.
</mark-your-parking>
