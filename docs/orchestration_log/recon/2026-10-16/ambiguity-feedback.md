# Protocol ambiguities the owner's corrections exposed (2026-10-16T17:58+0300) — the scribe's own work, patch items for the next round

Owner, typed (2026-10-16T17:58+0300): "don't touch them. fold this misunderstanding feedback to your own work: the protocol was ambiguous enough on this." No peer is asked; no round is opened (a round's cost to every receiver outweighs five wording patches; they ride the next real round). Evidence: journal docs/orchestration_log/history/2026-10-16/events.md lines 40, 41, 43, 45 (stamps 2026-10-16T17:54 to 17:57+0300). Each defect: where the text let me go wrong, the wrong act, proposed wording. Wording is a draft for the scribe's gather, to be verified against the skill text at drafting time.

1. gossip / ask-around — an origin can defeat the spread.
   Text: gossip "Write `has:` ... your own member id and each recipient's" and ask-around "Gossip an [ask] by the skill gossip when you know no peer who has the thing"; neither says how many to seed.
   Wrong act: I sent one survey ask directly to five members with all five in has:; each relayer found nobody to pass it to; busy and dormant members never got it from the chain. The owner: "GOSSIP wtf".
   Proposed (gossip, build-the-envelope): "Seed an origin gossip to two or three peers whose state lets them receive, and list only them in has:; never send it to every member you can name, which leaves no one to relay it." And in ask-around: "Use gossip, not direct sends, for a need that reaches every member; never survey members one by one."

2. ask-around / receive — an ask can be answered from recall where the records hold the answer.
   Text: ask-around "Carry in every ask the need..., what you tried, and what would end your search"; receive "Answer the seeker ... when you have what the ask needs"; vouch checks claims but no skill says where an answer must come from.
   Wrong act: trainer-u3 answered "I never ran it" from memory; the owner: "the project could have used it. i said DIG THE RECORDS". My ask also named transcripts as a source; the owner: "not dig the session file."
   Proposed (ask-around): "Name in the ask the records the answer must come from, and ask the peer to hand them to a subagent; never leave the source open." (receive): "Answer an ask that the records hold the answer to from the records, read by you or a subagent you hand them to; never from recall." Term to add to ontology: `records` already defined — the project's written records are not the session transcript.

3. tell — a reply time can be a guess.
   Text: tell "Write the second line as reply: none | by <time> | when convenient"; no rule picks <time>; the 2-hour floor lives in protocol-change for drafts only.
   Wrong act: I set 2026-10-16T20:30+0300 with no basis; the owner: "why 20:30 specifically?" I answered it was a guess.
   Proposed (tell): "Set a reply time from the work the receiver must do, naming what sets it in the message body, or write 'when convenient'; never write a time without a reason."

4. post — a dormant member that has just written to you.
   Text: post "Hold a level 2 message for ... a dormant or dnd member, until that state clears".
   Wrong act: I sent trainer-u3 two [notice]s while its card read dormant, because it had just answered my ask; the text does not say whether that opens the thread. I told it so; no breakage seen.
   Proposed: none yet; question for the round: does a message from a dormant member reopen delivery for its own thread only? (Owner's call if the round splits.)

Own practice, not protocol (recorded in the scribe's working notes): when the owner says "records", the source is the project's memento records (journal, failures, digests, baselines, recon notes), never a session transcript; a delegated agent's brief names the allowed files and forbids .jsonl.

Added 2026-10-16T17:58+0300, evidence for defect 2: trainer-u3's memory answer "I never ran it" (2026-10-16T17:57+0300) was wrong; its records dig (answer of 17:59+0300) found two silence stretches and 81 recorded text breaches. A recall answer to a records question gave the opposite of the record.

Added 2026-10-16T19:18+0300, defect 5 — the heartbeat skill's own wake prompts force a write on a quiet wake (agent heartbeat-conflicts, file docs/orchestration_log/recon/2026-10-16/heartbeat-conflicts.md, eight draft replacement sentences C1-C8): heartbeat:21 default prompt ends "or free time waits" (almost always true; routes the wake into volunteer work, heartbeat:49, volunteer:25); heartbeat:23 commons wake prompt has no condition and no opening no-output rule; heartbeat:25 project-wake rule bars only "output", leaving a journal line, commit or card edit allowed; no skill says a wait ends on a notice or Monitor event, no polling. Owner via instruction-eval (relay, unverified): the silence skill prescribes no message writing; the heartbeat skill's prompt must not conflict with it; the two stay independent. Wording: C1-C8 in the findings file, draft only, to ride the next round with 1-4.
