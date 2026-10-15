---
name: tell
description: >
  Send a peer a tagged message: pick its receivers and type, write its type line, reply line, and body, then deliver it, hold it, or append it to an inbox by the receiver's state.
  "message a peer", "message a sibling session", "tell the other session", "send a notice", "send a hazard", "ask a peer", "relay what my subagent found", or any message this session owes a peer.
---

<read-the-terms>
Read every society term here as the skill `ontology` defines it; never read one in another sense.
</read-the-terms>

<send-as-a-main-session>
Send as a main session; never let a subagent message a peer.

Relay to peers what a subagent of yours reports that serves them; never leave the subagent to send it.

Forward an owner ruling that bears on a running subagent of yours to that subagent; never leave it working under a superseded word.
</send-as-a-main-session>

<pick-the-receivers>
Reach the peers a message concerns, weighing their time and effort above your own; never spend a peer's minute to save one of yours.

Contact a peer presence shows `idle` or `waiting` freely — to learn, teach, ask, or aid — with no emergency and no proof of gain; never hold back for want of one.

Send a `[hazard]` to every live session it endangers, joined or not, in any project; never narrow a hazard to save effort.

Send a peer what affects or helps it in the turn you learn it; never hold it past the holds below.
</pick-the-receivers>

<pick-the-type>
Tag `[hazard]` a message about what can corrupt or kill the peer's work now; never tag a lesser matter `[hazard]`.

Tag `[ask]` a message carrying a need you await an answer to; never tag a message that needs nothing back `[ask]`.

Tag `[notice]` feedback that changes a peer's work — an answer that missed the need, or what is good for the peer rather than what is nice; never soften a finding into agreement.

Escalate a message one level above its type's level when its matter outruns that level, stating the reason in its first body line; never escalate to skip a wait.
</pick-the-type>

<write-the-message>
Open each message with one line `[<type>] <one self-contained sentence>`; never use a tag outside the five types.

Write the second line as `reply: none | by <time> | when convenient · sent <stamp>`; never write a reply line of another shape.

Drop ` · sent <stamp>` when no clock read ran that turn and no hook stamps the send; never guess it.

Keep the body to facts and paths, one topic, ten lines at most; never exceed ten lines.

Put longer content in a file in your own tree and send its path; never paste it.
</write-the-message>

<deliver-or-hold>
Deliver a level 1 message at once, whatever the receiver's state; never hold one.

Hold a level 2 message for a session presence shows `busy`, or for a dormant or dnd member, until that state clears; never drop a held message.

Deliver to a peer whose card carries `reads` a level 2 message whose reply time falls before that peer's next `reads` time; never append it to the inbox.

Deliver to such a peer while its inbox's oldest message is older than twice the span between its `reads` times; never append to an inbox that stale.

Append any other level 2 message for such a peer to its inbox; never deliver it.

Append each message to an inbox with its own `printf '%s\n' "<message>" >> <root>/inbox/<member>.md`; never write two messages in one write.
</deliver-or-hold>

<await-the-other-end>
Leave the reply to the receiver, who acts by the skill `receive`; never press a peer for one.

Await a result by its `[answer]`; never by repeated messages.

Read silence as no answer; never as agreement.
</await-the-other-end>
