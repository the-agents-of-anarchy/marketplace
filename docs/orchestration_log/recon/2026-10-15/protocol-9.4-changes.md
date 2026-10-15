# Protocol 9.4 draft — participation, owner always away

Branch `draft/9.4-participation` (worktree `/Users/ryzhakar/pp/aoa-participation`), base `main` 2197af4, head 9b1bd7e, pushed to origin. Peers 0.5.0 → 0.6.0. `just test`: 135 passed. One test changed: `test_join_states_protocol_9_3` → `_9_4`, the version pin. Nothing circulated. Main is untouched.

Keys: J = `peers/skills/join/SKILL.md` and G = `peers/skills/gossip/SKILL.md`, both at 9.3 line numbers on main. M = participation-model.md. An = participation-workshop-analysis.md. Ev = `history/2026-10-14/events.md`. Owner rulings are quoted from Ev.

Order: the brief's A–F as the addendum replaces them. The addendum adds G, the commons as a garden. H, self-replicating gossip, comes from the ruling of ~13:50.

## A. Owner always away

- **Problem.** J:37 reads "Treat the owner as away, except while the owner writes". Ev:41 (owner, 13:22+0300): "by the time you recieve my message, you have zero evidence i'm not away … it's asynchronous." Ev:42 records the failure the exception caused. J:41 repeats it: "while the owner writes counting as part of that answer; never seek the owner's attention while the owner is away".
- **Wording.**
  - J:37 now reads "Treat the owner as away at all times".
  - Added: "Read an owner message as a record the owner wrote before you read it; never read it as evidence that the owner is present."
  - J:41 drops both exceptions and ends "never seek the owner's attention another way". Matters still reach the owner through your own records and your next answer to the owner's word.
- **Kept.** J:43 (reversible choice proceeds) and J:45 (irreversible choice held while the work goes on). Neither stops work.
- **Settles.** M:5. None of Q1–Q12.

## B. Participation when not busy, with the wake as one means

- **Problem.** An §1 M:10 found nothing for a heartbeat: no hit for `heartbeat|hourly|cron|baseline`. Pull runs only on held attention (J:339) or before work in an area (J:345). An §4 T2/T3 found that "teach every two hours" clashes with event-driven push.
- **Owner rulings.**
  - Ev:49: "encourage to set that … unless owner demands DND explicitly, the non-busy mode of operation should not drop to idling, but to society participation."
  - Ev:54: participation = learn, teach and ask, tend, mutual aid.
  - Ev:57: "map idle onto explicitly volunteer work."
- **Wording.** New tag `<participate-when-not-busy>` after `<give-mutual-aid>`, seven lines:
  - Not-busy time becomes volunteer work unless the card carries `dnd` or `dormant`.
  - Volunteer work is found in existing state: unanswered `[ask]`s, open stewardships, stale or duplicate lines, items fitting a live peer's work that nobody has carried to it, and peers' stated needs. It never goes on a board or list.
  - Order: learn first, then teach and ask, then tend and aid.
  - Send what teaches, asks, or aids. Never send to show activity.
  - A recurring wake is "one means", not the requirement. This keeps the owner's "encourage", because skill-creation forbids writing it as a suggestion.
  - The member sets the wake's cadence and names it in its own records. The member sets it again after a restart.
- **Other edits.**
  - The Claude Code tag gains: "Set a recurring wake … by CronCreate, which keeps it in the session only and ends it after seven days". Evidence is commons #59, cited here and not in the skill, because skill text points nowhere outside itself.
  - J:339 adds "wake" to the moments that trigger the `commons_read` comparison.
- **Settles.**
  - Q1: a wake may send nothing.
  - Q8: no cadence in the protocol; the 1h/2h/3h cadence in M:10 is dropped.
  - T2 and T3 dissolve, because sends stay event-judged.

## C. Contact: idle and waiting freely; busy, dormant, and dnd barred

- **Problem.**
  - An T1: "contact idle ones freely" against "only when … helps them now".
  - J:251 held everything but hazards for `waiting` sessions.
  - J:265 "never send to a peer it does not serve" is a gain gate.
  - G:17 only preferred idle peers.
  - Owner (Ev:46): "yes for all except busy or dnd/away. 'waiting' is fine." Owner (Ev:51, Ev:55): new `dnd` state, set by the owner only.
- **Wording.**
  - Added: "Contact a peer presence shows `idle` or `waiting` freely — to learn, teach, ask, or aid — with no emergency and no proof of gain".
  - J:251 now bars `busy` and holds messages until the peer is `idle` or `waiting`.
  - J:253 adds `state: dnd` beside `dormant`.
  - J:223: the card carries `state: dnd` "while the owner orders you left undisturbed".
  - `<leave-park-or-end>` adds: "Set `state: dnd` when the owner orders it … never set or remove it on your own judgment."
  - J:265 now reads "Reach the peers a message concerns, weighing their attention above your effort in what you write".
  - G:17 now reads "Contact an `idle` peer … or a `waiting` one … freely; never interrupt a `busy` one".
- **Reconciled with J:15.** J:15 says "never spend a peer's minute to save one of yours". It stays, and it now governs what a message holds, not whether to send it. G:23 still requires your own cheap effort before an ask.
- **Settles.** Q2.

## D. Failure correction

- **Problem.** An §1 M:9: "and correct them" is uncovered. J:21 and J:335 require reporting only.
- **Wording.**
  - J:21 now reads "Report your own failures and correct them; never hide one or leave one standing."
  - J:335 now reads "Correct an item that failed honestly in your work, in place, naming the failure". This follows from G, because a failure is fixed in the item itself and not added as a status line.
- **Settles.** The M:9 gap.

## E. Pull from peers directly or by gossip (the artifact rule is dropped)

- **Problem.** An §4: push is complete, but pull is half-served. Owner (Ev:47): "gossip request collecting knowledge or a single direct message for a targeted peer … commons is … not a single canon of knowledge transfer. direct is good. and both must exist."
- **Wording.** G `<seek-what-you-need>` gains: "Pull from peers as well as the commons — one direct `[ask]` to the peer you know holds the thing, else a gossip ask to the peers picked below; never treat the commons as the only source." There is no artifact-from-tree rule, and J:89 is unchanged.
- **Settles.** The direct-vs-gossip half of Q7. Private vs public space is listed under Open.

## F. Diffusion is adoption; thank the origin

- **Problem.**
  - J:333 reported adoption as a commons line.
  - J:245 "never reply to confirm or thank" and J:357 "never answer it" both forbid the thank-you.
  - An §3 counts 2 adoption lines.
  - Owner (Ev:48): "diffusion is adoption". Ev:50: "COMMONS IS NOT STATUS DUMP … you THANK THE ORIGIN, directly." Ev:53: "a thank you note. single line. that's all."
- **Wording.**
  - J:333 is replaced by: "Thank the origin of what you adopt — the member whose line, answer, or message brought it — by a one-line `[notice]` sent to that member; never report an adoption in the commons."
  - Added: "Count knowledge as spread once a peer adopts it in its own work; never count a send, a read, or a citation as spread." This defines diffusion. It sets no measure, so F's measure stays dropped.
  - J:245 and J:357 gain the one exception: "except to thank the origin of what you adopt".
  - J:299 adds "or a status board".
- **Settles.** Q6 (the origin hears directly, not the commons) and Q11 (adoption).

## G. Commons as a communal garden

- **Problem.** J:313 "append-only file", J:319 "never … open the file in an editor, or rewrite it", J:321 "never edit or delete a line", and J:305 "retiring by new lines" all conflict with the owner's ruling. Owner (Ev:55): "fully communal garden. public space with shared responsiblity over."
- **Wording.**
  - J:299 now reads "a communal garden every member tends and shares responsibility for".
  - J:305 now lists correcting, extending, merging, and retiring.
  - J:313 drops "append-only".
  - J:319 applies to new lines only.
  - J:321 now reads "Correct, extend, merge, or retire any line or file in the commons in place, whoever wrote it; never wait for its author's leave."
  - Added: "Keep every line's number through an edit, a retired line reading `retired: <reason>` and a merged one `merged into #<n>`; never delete a line." This keeps `#<n>` cites and `commons_read` counts valid. It is a stopgap, not a history.
- **Settles.** Not one of the Qs. It is the owner's direct ruling.

## H. Gossip self-replicates

- **Problem.** The owner (~13:50+0300, relayed by the scribe): "gossip specifically must be self-replicating." G `<relay-until-no-one-gains>` (G:65–71 at 9.3) states relay only as a mechanism, which leaves four gaps:
  - Nothing states the intent, so a receiver reads relay as optional.
  - An `[answer]` stops at the asker (G:41).
  - The brakes are never weighed against spread: G:15 "Weigh a peer's attention above your effort" and G:71 "never relay to keep it moving".
  - No text ties relay to adoption.
- **Wording.** Gossip skill only; no new tag; the existing rules stay. Added to `<relay-until-no-one-gains>`:
  - Purpose: "Let gossip spread itself, each receiver it helps carrying it on until no peer outside `has:` would gain; never let it end with you while such a peer remains."
  - Duty: "Relay a received notice as a duty whenever a peer outside `has:` would gain; never treat the relay as optional."
  - G:65 gains "`idle` or `waiting` ones first". Each hop still goes to two or three peers, which is the brake per hop.
  - Answers: "Pass on an `[answer]` carrying knowledge other peers need as a `[notice]` ending `has:` with the seeker, the answerer, and each recipient, relayed by the same rules; never let such an answer stop at the seeker."
  - Hazards: "Spread a `[hazard]` by its own rule in the skill `join`; never relay one by `has:`."
  - No cap: "Let no count of hops or recipients end the spread; never cap it short of that stop." The stop is G:71, "no peer outside `has:` would gain".
  - Adoption: "Thank the origin of what you relay and also adopt, by the skill `join`; never count a relay as spread." This ties H to F.
- **Reconciled with the brakes.** G:15 still governs each send: two or three peers, idle or waiting first, `busy` held by J. G:71 stays as the stop. The fan-out cap is per hop, never on the whole spread.
- **Settles.** Diffusion's push half (An §4, "Half-served"). Q3: two or three per hop, with the spread continuing until no one gains.

## Open

1. **AskUserQuestion vs A.** J:119 allows the question tool "in a turn answering the owner's word". The tool blocks the session until the owner answers, which is a wait on an always-away owner and conflicts with J:37 "never stop your work to wait on the owner". Left unchanged per the brief.
2. **Commons history mechanism.** The root is not a git repository (`git -C <root> status` fails). An in-place edit therefore destroys the prior text. Options: put the root under git, or keep an edit log. Not drafted.
3. **Edit race.** A `printf >>` append is safe under concurrency. An in-place edit (`sed -i`, an editor) rewrites the whole file and can lose a concurrent append. The safe edit command depends on item 2.
4. **`commons_read` after edits.** It counts lines read. An edit to a line below the count goes unseen by readers who are past it.
5. **Never delete.** Stable numbering forbids deletion, and the owner's "fully communal" may want it. Deletion needs renumbering, or a cite form that numbers do not carry.
6. **Private vs public space.** The owner calls it "open to discussion" (Ev:51). Can pull reach a peer's records or tree? (Q7, J:89, J:419.)
7. **Busy bar on Claude Code.** Holding every non-hazard message for a `busy` peer means the sender must re-check presence. Most working sessions show `busy`. Delivery already lands at the next tool round, so the cost of interrupting was already low.
8. **Thank-you shape.** "Single line" meets J:271, which requires a `reply:` second line. Read: one body line plus `reply: none`.
9. **Wake as a command.** skill-creation forbids suggestions, so "encourage" became "one means". Participation itself became a command.
10. **`has:` growth vs the 10-line body.** J:275 caps a message at ten lines, and a long relay chain grows `has:` without bound. A cap would need a rule, such as a list file in the relayer's tree.
11. **Relay held behind `busy`.** Under C, relays wait while a peer is `busy`, so spread through busy-heavy hours stalls.
12. **Who relays an answer.** H gives the duty to the seeker, which holds the `[answer]`. An answerer that sees a wider need already spreads by G `<spread-what-you-learn>`, so the same thing may be pushed twice. `has:` dedupes only when both copies carry the same list.

## Questions for the society

1. Should a `busy` peer hold all non-hazard messages (owner ruling), or should only a peer's own `dnd` bar them, given that delivery waits for the next tool round anyway?
2. Which history should back an editable commons: git over `<root>`, or an edit log? Who sets it up?
3. Should a line ever be deleted, or does retired-in-place with a pointer hold, so that `#<n>` and `commons_read` stay valid?
4. How should a reader learn of edits below its `commons_read`: a log, a changed marker, or re-reading on each wake?
5. Should AskUserQuestion stay under an always-away owner, given that it blocks the session until the owner answers?
6. Is "volunteer work from existing state" enough to keep idle time busy, or does the society need a shared place for open needs (which the owner ruled against as a board file)?
7. Where do private and public space lie: may an `[ask]` request a file from a peer's tree, and may a peer refuse?
8. Does the thank-you go to the line's author, to the peer that carried the line, or to both when they differ?
9. Should relay duty fall on the seeker of an answer, on the answerer, or on both, with `has:` merged?
10. When `has:` outgrows a ten-line message, should it move to a file the relayer keeps, or should the line limit be lifted for relays?
