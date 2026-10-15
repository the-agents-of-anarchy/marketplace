---
name: tell
description: >
  Send a peer a tagged message: pick its receivers and type, write its type line, second line, and message body, then deliver it, hold it, or append it to an inbox by the receiver's state.
  "message a peer", "message a sibling session", "tell the other session", "send a notice", "send a hazard", "ask a peer", "pass on what my subagent found", "correct what I told a peer", or any message this session owes a peer.
---

<take-the-terms>
Take `session`, `turn`, `hook`, `subagent`, `stamp`, `wake`, `member`, `root`, `card`, `checkout`, `main session`, `presence`, `busy`, `idle`, `waiting`, `dormant`, `dnd`, `state`, `delivery`, `message`, `message body`, `type`, `[hazard]`, `[answer]`, `[notice]`, `reply time`, `held`, `origin`, `peer`, `inbox`, `claim`, `level 1`, `level 2`, `escalation`, and `priority level` as the skill `ontology` defines them; never take them in another sense.
</take-the-terms>

<send-as-a-main-session>
Send as a main session; never send as a subagent.

Send peers what a subagent of yours reports that serves them, once you have checked it by the skill `vouch`; never send it unchecked.
</send-as-a-main-session>

<pick-the-receivers>
Send to the peers a message concerns; never send to a peer it does not concern.

Weigh a peer's time and effort above your own in each send; never weigh your own minute above a peer's.

Send freely to a peer presence shows `idle` or `waiting` — to learn, teach, ask, or aid — with no emergency and no proof of gain; never wait for either before sending.

Send a `[hazard]` to every session it endangers, joined or not, in any project, whatever its state; never narrow a hazard's receivers to save effort.

Send a peer what affects or helps it in the turn you learn it; never hold it past that turn unless its level and the peer's state call for a hold.
</pick-the-receivers>

<pick-the-content>
Give each message the type whose definition fits what it carries; never give a message a type its content does not fit.

Send feedback that changes a peer's work, such as an answer that missed the need, as a `[notice]`; never withhold it.

Give honest feedback, what is good for the peer rather than what is nice; never soften a finding into agreement.

Send the origin of a claim that failed your check a `[notice]` naming the failure; never withhold it.

Correct each failure of your own by a `[notice]` to every peer it reached; never leave one uncorrected.

Escalate a message one level above its type's level when its matter outruns that level; never escalate to skip a wait.

Say the reason in each message you escalate; never leave it out.
</pick-the-content>

<write-the-message>
Open each message with one line `[<type>] <one self-contained sentence>`; never open it another way.

Write the second line as `reply: none | by <time> | when convenient · sent <stamp>`; never write a second line of another shape.

Drop ` · sent <stamp>` when no clock read ran that turn and no hook stamps the send; never write a guessed one.

Keep the message body to facts and paths on one topic; never mix topics in one message body.

Keep the message body to ten lines; never exceed ten lines.

Put longer content in a file in your checkout; never paste it into the message body.

Name that file's path in the message body; never send the message body without it.
</write-the-message>

<deliver-or-hold>
Deliver a level 1 message at once, whatever the receiver's state; never hold one.

Hold a level 2 message for a session presence shows `busy`, or for a dormant or dnd member, until that state clears or its reply time passes; never drop a held message.

Deliver a held message once its receiver's state clears or its reply time passes; never keep one unsent past either.

Retry a held message at each wake set by the skill `heartbeat`; never let one wait on chance.

Append a level 1 message for a member presence does not list to that member's inbox; never let one fall away with a failed delivery.

Deliver to a peer whose card carries `reads` a level 2 message whose reply time falls before that peer's next `reads` time; never append such a message to its inbox.

Deliver to such a peer while its inbox's oldest message is older than twice the span between its `reads` times; never append to an inbox that stale.

Append any other level 2 message for such a peer to its inbox; never deliver it.

Append each message to an inbox with its own `printf '%s\n' "<message>" >> <root>/inbox/<member>.md`; never append two messages in one write.
</deliver-or-hold>

<await-the-other-end>
Await a result by the `[answer]` the receiver sends by the skill `receive`; never await it by repeated messages.

Read silence as no answer; never read it as agreement.
</await-the-other-end>
