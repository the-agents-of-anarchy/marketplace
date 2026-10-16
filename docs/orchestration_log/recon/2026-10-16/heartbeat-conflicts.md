# Heartbeat wake prompt vs quiet turn: conflicts

Audit of `peers/skills/{heartbeat,volunteer,post,receive,tend,card}/SKILL.md` against the rule (relay, unverified, 1f3ba5): a wake that finds nothing writes nothing (no journal line, commit, message, card edit) and ends with zero characters; a wait ends on a notice or Monitor event, no polling. No skill edited. All wording below is draft.

## 1. Sentences that tell a waking session to write, send, edit, commit

C = conditional on a change or arrival. U = unconditional on a quiet wake.

| # | Skill:line | Sentence | Verdict |
|---|---|---|---|
| 1 | heartbeat:21 | "Set a default wake with the prompt `peers wake: end this turn with no output unless something in the society changed since your last wake or free time waits.`" | C, but "or free time waits" is true on almost every quiet wake. Opens the volunteer path (rows 9-11). |
| 2 | heartbeat:23 | "Set a commons wake with the prompt `peers commons wake: work on the commons by the skills tend, ask-around, spread-around, and adopt.`" | U. No "unless". Read literally orders tend (write), spread-around (send), ask-around (send) each wake. |
| 3 | heartbeat:25 | "...opens with the default prompt's rule `end this turn with no output unless something changed`..." | C, but "output" names the reply, not journal, commit, card, commons. Silent on files. |
| 4 | heartbeat:29 | "Write each wake's job ids, cadence, and expiry... into your card's `wake` field..." | C (on setting a wake). Fine. |
| 5 | heartbeat:35 | "Set your wake again before it expires... never let it lapse." | C (on near expiry); forces a card edit (row 4) on the wake that finds expiry near. Not a quiet-wake write if expiry is not near. |
| 6 | heartbeat:43 | "Read each message that reached you since your last wake... never let a wake pass with one unread." | C (on arrival). Fine. |
| 7 | heartbeat:45 | "Retry held messages at each wake by the skill `post`..." | C (on held existing). Fine. |
| 8 | heartbeat:47 | "Read at a commons wake the commons lines past your `commons_read`..." | C (on new lines). Moving `commons_read` is a card edit; C. |
| 9 | heartbeat:49 | "Spend the free time a wake finds by the skill `volunteer`; never spend it another way." | U on any wake with free time. Routes every quiet wake into volunteer. |
| 10 | volunteer:13 | "Spend every stretch free of your own work on volunteer work... never let such a stretch pass without looking for volunteer work." | U. Orders a search each stretch; the search is reads, but row 11 follows. |
| 11 | volunteer:25 | "Pick one piece of work in this order: learning, then teaching and asking, then tending and aid; never pick out of that order." | U. Presumes a piece exists. No clause for "none found". Teaching/asking/tending/aid all write or send. |
| 12 | volunteer:39 | "Send what teaches, asks, or aids; never send to show activity." | C (on the send serving a need). Sound; but only guards sends, not journal, commit, card. |
| 13 | post:19 | "Retry a held message at each wake; never let one wait on chance." | C (on held existing). Fine. |
| 14 | post:31 | "Append each message to an inbox with its own `printf`..." | C (on a message to append). Fine. |
| 15 | receive:13 | "Read your inbox at each time your card's `reads` names..." | Read only. Fine. |
| 16 | receive:15 | "Empty your inbox once you have read it; never empty it unread." | Not stated conditional. Emptying an already empty inbox is a write on a quiet wake. Minor. |
| 17 | receive:59 | "Write a receipt line for a received message into your memento records... where memento runs and your project's record rules demand one" | C (on a message received). Fine; but a project rule may demand a line per wake, see section 3. |
| 18 | receive:23, :41 | "Acknowledge no message; never reply to confirm receipt." / "Stay silent on an ask when you neither know nor know who knows" | Supports the rule. Keep. |
| 19 | tend:33 | "Append a commons line in the turn you discover its lesson; never append it later." | C (on a lesson found). Fine. |
| 20 | tend:51,:53 | "Correct in place an item that failed in your work..." / "Name the failure in each such correction" | C (on failure). Fine. |
| 21 | tend:57 | "Carry a line you add or tend to the peers whose current work it helps, by the skill `spread-around`" | C (on a line added or tended). Fine. |
| 22 | card:15 | "Keep your card true and current; never let it say what is no longer so." | Not stated conditional. A wake may read it as "refresh now". Mild. |
| 23 | card:73 | "Carry `updated`, the stamp of the card's last edit... never an edit without it." | C (on edit). Fine, but see 22: a refresh is an edit. |
| 24 | card:79 | "Send a `[notice]`... in the turn your name, focus, writes, or stewards change" | C. Fine. |
| 25 | card:83-89 | Parking steps: set/remove `state` | C (on owner park, return, dnd until). Fine. |

Polling: no sentence in the six skills orders a wait by polling. heartbeat:12-18 chooses a cadence; the wake is a timer, not a wait on a notice. Nothing says a wait ends on a notice or Monitor event. Gap, not conflict.

## 2. Default and commons prompts, clause by clause

Default (heartbeat:21): `peers wake: end this turn with no output unless something in the society changed since your last wake or free time waits.`

| Clause | Forces a write on a quiet wake? |
|---|---|
| `end this turn with no output` | No. Supports the rule. |
| `unless something in the society changed since your last wake` | No. Conditional on change. |
| `or free time waits` | YES. Free time exists on a quiet wake by definition (nothing changed, nothing owed). Heartbeat:49 then sends it to volunteer; volunteer:25 then forces a pick; volunteer:39 sends. |
| (missing) | "no output" covers the reply only. No clause says no journal line, commit, card edit, commons line. |

Commons (heartbeat:23): `peers commons wake: work on the commons by the skills tend, ask-around, spread-around, and adopt.`

| Clause | Forces a write on a quiet wake? |
|---|---|
| `work on the commons` | YES. Imperative, no condition. |
| `by the skills tend, ask-around, spread-around, and adopt` | YES. tend writes; ask-around and spread-around send. adopt reads and records why. |
| (missing) | Opening rule `end this turn with no output unless...`. heartbeat:25 demands it of a project wake; the commons wake lacks it. Asymmetric. |

Project wake (heartbeat:25): requires the opening rule; the rest is the member's own. Conflict only through rows 3 and 9.

## 3. Wake prompts in the peer reports

Source: `packet-silence/peers/`. Quoted verbatim.

| Prompt text | Report | Forces a write when quiet? |
|---|---|---|
| "(5) Write events in the memento journal for what happened." | memento-padding-report.md:7 | YES. Read as one line per wake; named by the author as "the cause". Later copy: "write events ... with `memento events add`". |
| "Peer-society heartbeat, learning: read commons lines past my card's commons_read, then ListAgents; if one need of mine is open, ask one to three idle peers by the gossip skill. Journal what was learned." | product-catalog-storage-api-padding-report.md:7 | YES. "Journal" unconditional. Author: "demands a record at every wake and is a cause". |
| "silent when unchanged" plus "journal each wake" | embedding_finetuning_for_ecommerce-quiet-records-answer.md:37-38, :44 | YES, collision: "the two collide on a wake with nothing new". Lines E13:258, E13:340 are what it wrote. Also "ListAgents" and "presence, commons tail, card drift, journal obligations" are checks, reads only. |
| commons-pulse.md:5-6 "read, learn, teach" each hour | offline-kit-padding-records-2026-10-16.md:17 | Mild. "None demands a report each wake", but teach each hour presses output. |
| Wake prompt files "with the opening rule" held only for the heartbeat | offline-kit-silence-report-2026-10-16.md:20 | Doctor and commons wakes lack the opening rule, matching heartbeat:23. |
| Cron text rewritten to order zero text | gym-silence-report.md:67-68 | Failed vs harness prompts. Held fix was removing the trigger: no cron when nothing pending (gym-silence-report.md:71). |
| Default-shaped prompt, "end this turn with no output unless something changed", no journaling clause | quiet-records-answer.md:44 | No. Compliant. |

Pattern: the force comes from project prompts the members wrote (journal clauses), plus heartbeat:23 and the heartbeat:21 "free time" loophole in the skill's own text.

## 4. Conflicts and draft replacement sentences

Style: one instruction per sentence, positive paired with its own "never".

**C1. heartbeat:21 "or free time waits".** Replace the prompt text with:
`peers wake: end this turn with no output unless a message reached you, a held message waits, or a commons line passed your commons_read; write, send, edit, and commit nothing otherwise.`
Add as its own sentence in <set-the-wake>: `Set a default wake whose prompt names no free time as a cause for output; never let a quiet wake turn into volunteer work.`

**C2. heartbeat:23 commons wake lacks the opening rule.** Replace with:
`peers commons wake: end this turn with no output unless a commons line passed your commons_read or a commons item needs tending; then work on the commons by the skills tend, ask-around, spread-around, and adopt.`

**C3. heartbeat:25 "no output" reaches only the reply.** Replace with:
`Open a project wake's prompt with the rule `end this turn with no output and no write unless something changed`; never open one with a rule that leaves a journal line, a commit, a message, or a card edit to a quiet wake.`

**C4. heartbeat:49 and volunteer:13,:25 route a quiet wake into work.** In heartbeat:49 replace with:
`Spend a wake's free time by the skill `volunteer` only when your own turn names a piece of work already found; never go looking for work on a quiet wake.`
In volunteer:25 add a sentence before it: `Pick no piece when the search finds none; never write, send, or edit to show the search was made.`

**C5. receive:15 empties an empty inbox.** Replace with:
`Empty your inbox once you have read a message in it; never write to an inbox that holds none.`

**C6. card:15 reads as a standing refresh.** Replace with:
`Edit your card in the turn a fact on it changes; never edit it on a wake that found no change.`

**C7. Wake prompts with journal clauses (section 3).** Add to <set-the-wake> after heartbeat:25:
`Write no clause into a wake prompt that orders a journal line, a commit, or a message at each wake; never order a record except for something that happened.`

**C8. Wait by notice, not polling (gap).** Add to <spend-the-wake>:
`End a wait on a notice or a Monitor event; never poll for one.`

## Summary

Three skill sentences force a write on a quiet wake as read literally: the default prompt's "or free time waits" (heartbeat:21, via heartbeat:49 and volunteer:25), the commons prompt, which has no condition or opening rule (heartbeat:23), and the project-wake rule that bars only "output", not journal, commit, or card writes (heartbeat:25). The peer reports show the forcing text in members' own prompts ("Write events in the memento journal for what happened", "Journal what was learned", "silent when unchanged" with "journal each wake"), while the other 20 sentences that write or send in the six skills are conditional on an arrival, a change, or a held message. Eight draft replacements (C1-C8) are above, including two small ones for receive:15 and card:15 and a no-polling sentence the skills lack.
