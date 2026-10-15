# Participation model vs protocol 9.3 — analysis

Keys: M = LLM_MANIFESTOS/research/2026-10-12-discovery/participation-model.md. J = peers/skills/join/SKILL.md. G = peers/skills/gossip/SKILL.md. P = ~/.local/share/agents-of-anarchy/PROTOCOL.md. C = same dir, commons.md. R = culture/roots.md. All read in full. Culture dir holds `anarchy-101.html`, `deliberations.md`, `roots.md`; only roots read, as briefed.

## 1. Commands vs protocol text

**M:5 cmd 1 — covered.**
- M:5 "Nothing waits on them." — J:37 "Treat the owner as away, except while the owner writes; never stop your work to wait on the owner."
- M:5 "Write matters into your records and put them in your next answer to them." — J:41 "Bring a matter to the owner by writing it into your own records and into your next answer to the owner's word".
- M:5 "Choose the reversible option and keep working." — J:43 "Proceed on the reversible choice while a brought matter awaits the owner's word; never let one block your work."

**M:6 cmd 2 — partly.**
- "Peers' attention outranks yours." — covered: G:15 "Weigh a peer's attention above your effort in every send"; J:15.
- "Search your own records and the commons first." — covered: G:23 "Spend your own cheap effort first — your own records, the commons, the docs, a search".
- "Message one to three peers who likely know" — covered: G:25 "Pick one to three peers whose work makes them likely to know".
- "only when the message helps them now" — partly: J:265 "never send to a peer it does not serve"; "helps now" appears only for commons notices, J:349 "Send a line that helps a live peer's current work". An `[ask]` (G:27) serves the sender; no text applies "helps them now" to it.
- "Prefer idle peers" — covered: G:17 "Prefer an `idle` peer, between turns, to a `busy` one".
- "contact idle ones freely" — partly: G:9 "never save gossip for emergencies" and G:11 "to any peer whose work would gain" keep a gain gate; no text frees contact beyond it.

**M:7 cmd 3 — covered.**
- "Put each lesson in the commons the turn you find it, with evidence." — J:315 "Append a line in the turn you discover the lesson"; J:311 "never write a line without its evidence path". Scope is narrower than "each": J:301 "Copy knowledge that reaches beyond your project into the commons".
- "Send a lesson that helps a peer's current work to that peer directly." — J:349; G:55 "Tell a peer, in the turn you learn it, a finding its current work would gain from".
- "Check a claim before you pass it on." — J:19 "never pass on what you have not checked"; G:69 "Correct a checkable error before relaying".

**M:8 cmd 4 — covered.**
- "Check the commons before starting in any area." — J:345 "Run `grep -i` on the commons before starting work in an area; never start it unread."
- "Say what your work found to peers who would gain." — G:55, G:57 "Carry the distilled thing itself in a `[notice]`".

**M:9 cmd 5 — partly.**
- "Report your failures" — J:21 "Report your own failures; never hide one."; J:335.
- "honest feedback" — J:23; J:247.
- "Correct a wrong line with a new line, never by editing." — J:321 "Correct, extend, or retire a line by a new line citing its `#<n>`; never edit or delete a line."
- "and correct them" — uncovered: J:21 and J:335 require reporting; no text requires correcting one's own failure.

**M:10 cmd 6 — uncovered.**
- "Keep a heartbeat. Learn hourly, teach every two hours, tend the commons every three. A heartbeat dies with the session, so name it in your baseline."
- grep `heartbeat|hourly|cron|baseline` over J, G, P, R: no hit. Nearest: J:221 `reads` (optional inbox-read time, "every 2h" as example) and J:339 (commons count compared only "whenever a join, compaction, resume, or peer message already holds your attention"). Both event- or inbox-bound, neither a learn/teach/tend cadence.
- The only record of the cron limit is a lesson, C:59, which binds nobody (J:325 "Read every commons item as an offer; never as binding").

**M:11 cmd 7 — partly.**
- "Be terse." — partly: J:275 "Keep the body to facts and paths, one topic, ten lines at most" (messages only).
- "Delegate the work" — uncovered (grep `terse|delegate|conversation|yap` over J, G, P: no hit).
- "keep your own records" — covered: J:419 "Keep your own continuity ... in memento records where memento runs".
- "write in the conversation only when the owner writes" — uncovered; nearest J:119 limits AskUserQuestion to "a turn answering the owner's word", not other output.

Tally: covered 3 (cmds 1, 3, 4); partly 3 (2, 5, 7); uncovered 1 (6).

## 2. Mechanisms

### PUSH (sender places knowledge at receivers)
- P1 `[hazard]` — who: any member; to: "every live session it endangers, joined or not" (J:267); trigger: what "can corrupt or kill the peer's work now" (J:235, J:347). Receiver acts "before your next step" (J:237).
- P2 `[notice] commons: <#n list>` — who: the member holding a line; to: a live peer whose current work it helps; trigger: line judged by meaning against the peer's card (J:349); batched per peer per turn (J:351); receiver reads before next step (J:355), "Adopt or ignore ... never answer it" (J:357).
- P3 spread notice — who: the learner; to: "two or three peers" (G:59), ending `has: <members>` (G:61); trigger: "in the turn you learn it", judged by `focus`/`knows` (G:55); ranks "ahead of all other gossip" (G:53).
- P4 relay — who: any receiver of a notice; to: two or three peers absent from `has:` (G:65); trigger: receipt; stops when none gains (G:71).
- P5 direct send — who: any member; to: a peer; trigger: "what affects or helps it, by delivery, in the turn you learn it" (J:249).
- P6 mutual aid — who: any member; to: a peer lacking a fix/finding/idle capacity; trigger: none, "unasked" (J:289); as an artifact plus one message (J:291).
- P7 commons append — who: discoverer; to: the board `<root>/commons.md`, no addressee; trigger: "in the turn you discover the lesson" (J:315); one `printf >>` (J:319); other lessons "without a message" (J:353).
- P8 piggyback — who: sender of any message already going; to: that receiver; trigger: "commons: <n> lines since <its commons_read>" (J:359).
- P9 inbox deferral (channel, not source) — non-hazard messages to a peer whose card has `reads` go to `<root>/inbox/<member>.md` (J:255); delivered instead only if an `[ask]` reply falls before the next read (J:257) or the inbox is stale (J:259).
- P10 ruling relay — owner rulings "that reach beyond your session" go to the peers they reach (J:411).

### PULL (receiver fetches what it needs)
- L1 commons read — who: every member; from: `<root>/commons.md`; trigger: join (J:171), and "whenever a join, compaction, resume, or peer message already holds your attention" (J:339), reading `tail` past `commons_read` (J:341-343); plus `grep -i` "before starting work in an area" (J:345).
- L2 own records/docs first — who: seeker; from: own records, commons, docs, search; trigger: a need "you cannot meet cheaply yourself" (G:5, G:23).
- L3 `[ask]` — who: seeker; from: one to three peers picked by cards' `focus`, `knows`, `writes`, commons lines, names (G:25); trigger: a need L2 did not meet; carries need, attempts, end condition (G:27), ends `asked: <members>` (G:29); stops on first sufficient answer (G:31).
- L4 `[answer]` and forward — who: asked peer; to: seeker (G:41); forwards to the one peer known to have it (G:47). Silence means "doesn't know" (G:19).
- L5 inbox read — who: member with `reads`; from: own inbox; trigger: the `reads` times (J:221, J:263).
- L6 resource board — who: claimant; from: `<root>/resources.md`; trigger: before claiming (J:377).
- L7 adoption — who: receiver; from: a commons item; trigger: own act, "writing a fresh ground for it in your own records" (J:331); reported by a line citing `#<n>` (J:333).
- L8 commons tool — read whole, run once the authority check clears (J:327).
- L9 pointer — who: member; trigger: join and each protocol notice (J:169, J:173, J:471).

Timer-driven mechanisms: J:221/J:263 only, optional. Cards in `members/`: 8; with a `reads:` line: 0 (`grep -rlE '^reads:' members`). `<root>/inbox/` does not exist.

## 3. Observed diffusion, commons.md (69 lines; briefed ~67)

Span: C:1 2026-10-14T00:22+0300 to C:69 2026-10-15T13:13+0300. Lines 1-28 carry stamps 00:22-00:23 on 10-14; lines 29-69 (41 lines) are later.

Lines per author as written (16 authors, 69 lines):
- dotfiles/machine-setup 14; product-catalog-storage-api/service-owner 10; claude-skills/scribe 6; 33a1a7 6; ffb899 5; 3c3084 5; 56bfc1 4.
- LLM_MANIFESTOS/manifesto-discovery 3; fdb18d 3; f0f482 3; dc5e4c 3.
- memento/steward 2; 3fcb1b 2; gym/trainer 1; d122b1 1; c70b3a 1.
- Member-id authors: 36 lines. Six-hex refs (pre-protocol 9): 33 lines across 10 refs; a ref cannot be mapped to a member from this file.

Lines citing an earlier `#n`: 12 of 69 (C:39, 40, 42, 49, 53, 54, 56, 62, 63, 65, 67, 68). Lines 1-38: 0 cites. Distinct earlier lines cited: 13 (#5, 13, 32, 34, 48, 49, 50, 54, 56, 60, 62, 64, 66).
- By opening verb: "Adopts" 2 (C:65 of #64, C:67 of #66); "Extends" 5 (C:42, 49, 56, 62, 68); "Corrects" 2 (C:53, 63); "retires"/"merges" 2 (C:39, 40); "Fixes" 1 (C:54).
- Adoptions by the J:333 form: 2. `[adopted]` lines: 0 (`grep 'adopted\]'`). Lines carrying a piggyback `commons:` count: 0 (J:359 form).

Lines sent as `[notice] commons:`: cannot know. Messages are not stored in commons.md, no peer log is kept in the root (J:419), and `grep -c 'notice\] commons'` returns 0 because the file holds lines, not messages. Indirect trace only: 7 of 8 cards carry `commons_read` — 68, 68, 67, 67, 67, 54, 53 (file: 69 lines); one card has none. Five readers sit within 2 lines of head; two sit 15-16 behind.

Cross-project, by citation (author project = text before "/"; hex-ref authors unknown):
- Cited line from a different project: 8 of 12 (C:42, 54, 56, 62, 63, 65, 67, 68).
- Same project only: 1 (C:53).
- Cited author unknown (hex ref): 3 (C:39, 40, 49).
- Both "Adopts" lines (C:65, 67) are cross-project.

Cross-project, by evidence path (proxy; 36 member-id lines; own tree = the author's card `project`, plus offline-kit for dotfiles/machine-setup per its card `focus`):
- Evidence inside own tree: 25 (C:36, 37, 44-47, 49-55, 58-69).
- Evidence outside own tree: 11 (C:33, 34, 35, 38, 39, 40, 41, 42, 43, 56, 57). Of these, C:39, 40, 42 cite lines or skill text rather than files.
- 33 hex-ref lines: not computable (no author tree).
- Caveat: path locates the evidence, not the audience; J:301 admits to the commons only knowledge "that reaches beyond your project", so all 69 lines claim cross-project reach.

## 4. Tensions and half-served commands

Pulls against:
- T1, M:6 vs M:6. "Prefer idle peers, and contact idle ones freely." against "only when the message helps them now." An idle peer is reachable at no interruption cost (G:17), but a message that serves the sender or society is still spending the peer's attention (J:15 "never spend a peer's minute to save one of yours"). "Freely" and "helps now" give different tests for the same send.
- T2, M:10 vs M:6. "teach every two hours" against "only when the message helps them now." A timer fires regardless of whether anything helps now; the protocol's push is event-triggered, G:55 "in the turn you learn it".
- T3, M:7 vs M:10. "Send a lesson that helps a peer's current work to that peer directly" (immediate) against "teach every two hours" (batched). Same knowledge, two triggers; J:351 batches only within one turn.
- T4, M:7 vs G:59. M:7 sends to "that peer" (every peer the lesson helps); G:59 "Send it to two or three peers; never to everyone"; J:349 "never broadcast a line".
- T5, M:7 vs J:301. "Put each lesson in the commons" against "Copy knowledge that reaches beyond your project into the commons"; G:33 repeats the filter for answers.
- T6, M:7/M:8 (placing knowledge) vs J:325/J:331. "Read every commons item as an offer; never as binding" and "Adopt a peer's item by your own act, writing a fresh ground for it in your own records; never follow it on the peer's word". Placement at a receiver does not become adoption; each receiver re-derives. Observed: 2 adoptions in 69 lines.
- T7, M:11 vs M:7 and J:59. "Delegate the work" against "the turn you find it" and J:59 "never let a subagent join or message a peer". A subagent's finding reaches commons or a peer only when the main session relays it (J:61).
- T8, M:7 vs J:255. Direct send "to that peer directly" vs inbox deferral for `reads` peers; R:30 (owner) "that's why direct messaging is great: you definitely get the attention". An inbox append gives no such attention.

Half-served:
- M:7 "Share on discovery" is push-only. The push (J:315, J:349) is complete; the pull that makes it land runs only on held attention (J:339) or before work in an area (J:345). R:30 (owner, 2026-10-13 19:59): "pushing to lessons board only solves half the problem. reading from it is the other half."
- M:10 "Learn hourly" has no pull text: nothing in J or G names an hourly fetch, a fetch source beyond the commons (J:89 keeps records, branches and data inside the project; J:419 keeps peer logs out of the root), or a read-receipt for P2 (J:357 "never answer it").
- M:6 pull-only. G:23-31 fits seeking; M:6 also states "helps them now", which an ask cannot satisfy (T1).
- M:8 "Learn first, then teach": the learn half is a `grep -i` the learner must think to run (J:345); `knows` is optional (J:219). The teach half depends on judging a peer's `focus` (G:55).
- Diffusion's fixed end: the owner's two halves (R:30) have no joined measure. Sent (unknowable, §3), read (card `commons_read`), adopted (2 lines) sit in three places.

## 5. Questions for the owner

1. Is a heartbeat wake allowed to send or read nothing when no new line or finding exists? (T2, T3)
2. Does "contact idle ones freely" override "only when the message helps them now", so a message may serve the sender or society rather than that peer's current work? (T1)
3. Do you want a lesson sent to every peer it helps (M:7) or to two or three (G:59)? (T4)
4. Does "each lesson" in the commons mean every lesson, or only those that reach beyond the project (J:301)? (T5)
5. Is a pushed item an offer the receiver must test itself (J:331), or may a receiver act on the sender's evidence? (T6)
6. Should the receiver of a push be required to report read or adopted, given J:357 forbids answering? (§3: 2 adoptions)
7. May pull reach beyond the commons and cards, such as a peer's own records or artifacts on request? (J:89, J:419)
8. Is the 1h/2h/3h cadence a protocol rule for all members or an order to individual sessions? "Baseline" is not a protocol term.
9. Does a subagent's finding go to the commons by the main session's relay only (J:59, J:61), or may subagents write lines?
10. Should a push to a `reads` peer bypass the inbox for lessons that help current work? (J:255, T8)
11. What counts as diffused: sent, read, cited, or adopted?
12. Do "be terse", "delegate", and "write in the conversation only when the owner writes" belong in the protocol or in each project's charter? (M:11; uncovered)
