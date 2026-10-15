---
name: post
description: >
  Get a written message to its receivers at the time its level and each receiver's state allow: deliver it, hold it, or append it to an inbox by the receiver's state, and retry what waits.
  "deliver this message", "is the peer busy", "wait until they're free", "retry held messages", "append to the inbox", a message written and ready to go, or a wake that retries held messages.
---

<take-the-terms>
Take `session`, `wake`, `member`, `root`, `card`, `presence`, `busy`, `dormant`, `dnd`, `state`, `delivery`, `message`, `reply time`, `held`, `peer`, `inbox`, `level 1`, `level 2`, and `priority level` as the skill `ontology` defines them; never take them in another sense.
</take-the-terms>

<deliver-or-hold>
Deliver a level 1 message at once, whatever the receiver's state; never hold one.

Hold a level 2 message for a session presence shows `busy`, or for a dormant or dnd member, until that state clears, a dnd member's end time passes, or its reply time passes; never drop a held message.

Deliver a held message once its receiver's state clears or its reply time passes; never keep one unsent past either.

Retry a held message at each wake; never let one wait on chance.
</deliver-or-hold>

<append-to-an-inbox>
Append a level 1 message for a member presence does not list to that member's inbox; never let one fall away with a failed delivery.

Deliver to a peer whose card carries `reads` a level 2 message whose reply time falls before that peer's next `reads` time; never append such a message to its inbox.

Deliver to such a peer while its inbox's oldest message is older than twice the span between its `reads` times; never append to an inbox that stale.

Append any other level 2 message for such a peer to its inbox; never deliver it.

Append each message to an inbox with its own `printf '%s\n' "<message>" >> <root>/inbox/<member>.md`; never append two messages in one write.
</append-to-an-inbox>
