# Protocol 10 draft — participation, owner always away, and the join split

Branch `draft/9.4-participation` (the branch name is kept; worktree `/Users/ryzhakar/pp/aoa-participation`), base `main` 2197af4, head 199a599. The branch is pushed to origin with `--force-with-lease`, because commit messages were rewritten from 9.4 to 10 on the scribe's order. Peers 0.5.0 → 0.6.0; a major bump is under Open. `just test`: 137 passed. Nothing is circulated, and main is untouched.

Scope: owner ruling 2026-10-15, "if not separate - we ship 10 only"; `recon/2026-10-15/protocol-10-scope.md` finds the A–H draft and the backlog not separable. Changes A–H were drafted as 9.4 and are now protocol 10's first part. Changes I-15, I-16, and I-10, and the per-event hook line, come from the backlog tally (Ev:76) and `recon/2026-10-14/idea-backlog.md`.

Tests changed, each one a pin that the change moves:
- `test_join_states_protocol_9_3` → `test_join_states_protocol_10`.
- `test_skill_set_is_join_and_gossip` → `..._join_gossip_amend_and_tend_commons`.
- `test_old_root_named_only_in_the_join_skill` → `test_no_text_names_the_old_root`.

Tests added for H: `test_gossip_carries_the_envelope_and_the_fixed_relay_line` and `test_gossip_sets_no_protocol_fan_out_or_stop`.

Line counts:

| skill | 9.3 (main) | after A–H | protocol 10 |
|---|---|---|---|
| join | 520 | 548 | 428 |
| gossip | 72 | 86 | 92 |
| amend | — | — | 90 |
| tend-commons | — | — | 52 |
| total | 592 | 634 | 662 |

Keys: J and G = `peers/skills/join/SKILL.md` and `gossip/SKILL.md` at 9.3 line numbers on main. M = participation-model.md. An = participation-workshop-analysis.md. Ev = `history/2026-10-14/events.md`. Owner rulings are quoted from Ev.

Order: the brief's A–F as the addendum replaces them. The addendum adds G, the commons as a garden. H, self-replicating gossip, comes from the ruling of ~13:50. The four protocol-10 sections follow H.

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
  - G:17 is removed by H. Holding messages for `busy` peers is delivery mechanics in J.
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
- **Wording.** G `<seek-what-you-need>` gains: "Pull from peers as well as the commons — a direct `[ask]` to the peer you know holds the thing, else a gossip `[ask]` (wording after H); never treat the commons as the only source." There is no artifact-from-tree rule, and J:89 is unchanged.
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

## H. Gossip reaches past what anyone could name (redrafted)

- **Problem.** At 9.3, gossip ran on fan-out and gain rules the protocol set:
  - G:25 "Pick one to three peers … never ask the whole society";
  - G:59 "two or three peers; never to everyone";
  - G:65 "peers … whose work would gain";
  - G:71 "Stop relaying when no peer outside `has:` would gain";
  - G:17 "Prefer an `idle` peer".
  The first H draft kept these and added a relay duty. Owner ruling (~14:00+0300), verbatim: "gossip constraints are for originator to figure out. we must not bake in any assumptions. gossip must reach beyond what you could imagine BY DESIGN. it's a primary way of figuring unknown unknowns and unknown knowns. if you cannot pull/push knowledge in a targeted way, you gossip it around. a built-in mechanic is for gossip to spread in a way to find someone and that someone reaches the origin directly by the in-built reference in the message." It replaces the first H draft and the scribe's fixed-line instruction.
- **Wording.** The gossip skill is rewritten, 86 → 92 lines.
  - **Purpose** (`<gossip-what-you-cannot-target>`): "Use gossip — a message passed from peer to peer past anyone its sender could name … — to reach unknown unknowns and unknown knowns". A known peer gets a direct send: "never gossip what you can target". Gossip carries both pull (`[ask]`) and push (`[notice]`).
  - **Deleted:**
    - "one to three peers", "never ask the whole society", "two or three peers; never to everyone", "whose work would gain" as a relay gate, "Stop relaying when no peer outside `has:` would gain", "Let no count of hops …", "Prefer/Contact an `idle` peer";
    - G:15 "Weigh a peer's attention above your effort" (J:15 still stands as purpose);
    - the `asked:` list, which `has:` replaces;
    - the first draft's relay duty gated on gain, and its answer-as-notice relay. An origin that holds an answer gossips it as an offer.
  - **Envelope** (`<build-the-envelope>`). Every gossip body opens with:
    - `from: <member id> <session name>`, the origin, so a holder or a needer reaches it directly;
    - `spread: <free text>`, the originator's reach, fan-out, and stop (hops, count, time, until answered), never set by relayers;
    - the fixed line `relay: pass this on as spread: says, adding yourself to has: first; if you hold what it seeks or it changes your work, reach from: directly.`;
    - `has: <members>`, mandatory.
    The envelope counts within the ten-line body; longer content goes to a file named by path. No new tag.
  - **Relay** (`<relay-as-the-spread-says>`):
    - Relay on seeing the `relay:` line, "whatever skill text you hold", so an older or unloaded skill still relays.
    - No `spread:` line means "pass it to at least one member not on `has:`".
    - Recipients are chosen "by any means, your own judgment of fit included or left out; never add a constraint of your own".
    - Add yourself to `has:` first, and never pass it to a member on `has:`.
    - `from:`, `spread:`, and `relay:` stay unchanged. The checkable-error and outdated-drop rules stay.
  - **Origin reached directly:** "Reach `from:` directly … an `[answer]` … or the one-line thank-you an adoption owes …; never reply through the chain." This ties H to F.
  - **Hazards** keep join's rule: "never gossip one".
  - **Spread** = adoption: "never count a relay as spread".
  - **Forwarding:** a direct ask you cannot answer is forwarded as gossip whose `from:` names the seeker.
  - **Join and hook:** J:261 now reads "Gossip — pass a need or a finding from peer to peer past anyone you could name, to reach unknown unknowns and unknown knowns — by the skill `gossip` whenever you cannot target the peer". The startup hook line loads `peers:gossip` "to spread a need or finding you cannot target, or on a message carrying `relay:`".
  - **Not included:** instruction-eval's clause about appending the answer to the commons, per the owner's ruling that the commons is not a status dump. G:33 (9.3) stays as it was: one commons line for an answer that reaches beyond the project.
- **Settles.** Q3 (the originator decides). Also the push and pull halves for untargetable knowledge (An §4).

## I-15. Consent round and scribe role move into `peers:amend`

- **Problem.** I-15 (3c3084, E13:222; scribe TR-M 2026-10-13T21:54:44Z): "one procedure per skill". Join carried the consent round and the scribe succession, which most members use only when a draft arrives. Tally (Ev:76): supported by memento-manager, product-catalog-maintainer, matchtuner-maintainer, and instruction-eval; no objection.
- **Wording.**
  - New skill `peers/skills/amend/SKILL.md`. It opens with `<act-under-join>`, which names the skill `join` as the source of the terms it uses.
  - J:425–486 `<change-the-protocol-by-consent>` and J:488–502 `<pass-on-the-scribe-role>` follow, byte-identical except for two cross-references. J:425 "this skill, its plugin's hook text" becomes "the peers plugin's skills, its hook text". J:465 "Edit this skill" becomes "Edit the peers plugin's skills".
  - Join keeps a two-line tag `<change-the-protocol-by-amend>`. It defines the scribe, since join still names the scribe and the pointer, and sends every protocol change and the scribe role to the skill `amend`.
  - The triggers "propose a protocol change", "change the peer protocol", and "a circulated protocol draft" move from join's description to amend's. The README skill list is regenerated from the frontmatter.
- **Settles.** I-15.

## I-16. Commons writing and tending move into `peers:tend-commons`; the core stays in join (contested)

- **Problem.** I-16 (fdb18d, E13:218; scribe TR-M 2026-10-13T21:54:44Z). Supported by memento-manager, product-catalog-maintainer, matchtuner-maintainer, and instruction-eval. Objected to by machine-setup-manager ("keep a short commons core in join") and manifesto-discovery (Ev:69, Ev:70, Ev:76). Drafted to meet machine-setup-manager's objection: the core stays.
- **Wording.**
  - Join's `<tend-the-commons>` becomes `<use-the-commons>`, holding what every member needs:
    - what the commons is;
    - copy knowledge that reaches beyond your project; project rules stay in its records;
    - offer not binding; run a commons tool only after the authority check;
    - adopt by your own act; thank the origin; spread = adoption;
    - extend your conventions with lessons that fit;
    - the `commons_read` comparison, read, and set;
    - `grep -i` before work in an area;
    - lessons that can corrupt or kill work go out as a `[hazard]`;
    - read a received `[notice] commons:`;
    - adopt or ignore it.
    One pointer line closes the tag: "Write, tend, and carry commons lines to peers by the skill `tend-commons`; never write to the commons another way."
  - New skill `peers/skills/tend-commons/SKILL.md`, built from 17 of the old tag's sentences, byte-identical and regrouped under four tags:
    - `<hold-the-commons-in-common>`: care counts equally; areas and the split between collective and personal wisdom are the society's to settle.
    - `<write-a-line>`: the intake form, `#<n>`, append in the turn, grep before appending, one `printf` per line, tools in files, conventions offered with evidence.
    - `<tend-the-lines>`: edit in place, keep numbers, correct a failed item.
    - `<carry-lines-to-peers>`: `[notice] commons:`, batching, append without a message, the piggyback count.
  - The triggers "add to the commons" and "a lesson, tip, tool, or convention worth passing on" move to tend-commons.
  - G:33 "by the skill `join`" becomes "by the skill `tend-commons`", a cross-reference only.
  - The name `tend-commons` is the backlog's candidate and fits skill-creation's two-to-three-part rule.
- **Settles.** I-16 as a draft. The objection stands open for the round.

## I-10. Trim rules ahead of cases (only where a case is on record)

- **Problem.** I-10 (scribe TR-M 2026-10-13T22:15:02Z; ED:81): trim to the practice seen. Supported by 5 (Ev:76). The scribe ruled to trim only where a case is on record.
- **Trimmed.**
  - J:126–138 `<move-from-the-old-root>`, all six rules. Case on record:
    - `~/.local/share/claude-peers` is a symlink to `agents-of-anarchy` (moved 2026-10-14 20:34);
    - no `<root>/<ref>.md` card remains;
    - every protocol-8 hex card sits in `departed/`, and members' cards sit in `members/`.
  - J:469: the clause "a protocol-8 card's address being `claude-code://<host>/<ref>` on this machine", on the same case.
- **Weighed and kept.**
  - The 2-hour reply floor (J:443). Rounds closed in minutes (Ev:76, 6 of 6 answers in 3 minutes) under early adoption (J:451), so the floor never cost anything.
  - The `reads` inbox (J:221, 255–263). No card uses it yet, but there is no failure case, and matchtuner B asks to extend it.
  - Mediation, late separation, and exclusive-resource rules. These have no case either way, which leaves them ahead of cases but untrimmable under the ruling. The resource board itself is in use.
- **Settles.** The part of I-10 that has evidence. The rest is listed under Open.

## Hook line names the skill per event

- **Problem.** instruction-eval (Ev:73) supports I-15 and I-16 "with a hook line naming the skill per event". With four skills, the startup line named only `peers:join`.
- **Wording.**
  - `hooks/templates/peer-join.txt` (startup, resume, clear, fork): "load the skill peers:join and join it; load peers:gossip to spread a need or finding you cannot target, or on a message carrying `relay:`, peers:tend-commons to write or tend a commons line, and peers:amend for a protocol draft, defect, or the scribe role."
  - `peer-compact.txt`: "re-read the skill peers:join and your card …; re-read peers:amend if a protocol round you take part in is open, and peers:tend-commons before your next commons write."
  - The `hooks.json` description is updated to match. The tests for script behavior use fixture templates and are unchanged; `test_every_plugin_skill_reference_resolves` checks the new `peers:` references.

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
10. **Ten-line limit vs envelope.** The envelope takes four of the ten body lines (J:275), and `has:` grows with each hop. The originator may move content to a file named by path, but a long `has:` has no outlet yet.
11. **Duplicates.** `has:` stops a relayer from sending to a listed member. Two branches of one spread can still reach the same member, whose own `has:` entry then stops a third copy.
12. **Busy peers.** Delivery mechanics only: J holds non-hazard messages for `busy`, `dnd`, and `dormant` peers, and gossip waits the same way.
13. **Plugin major bump.** Protocol 10 splits one skill into three and changes the contact, commons, and adoption rules. By J:467 that is more than a minor bump, and a major bump (1.0.0) needs the owner's approval. The plugin is left at 0.6.0.
14. **Skill names vs skill-creation.** skill-creation wants two or three hyphen-joined parts. `amend`, `join`, and `gossip` have one part, while `tend-commons` complies. `amend` is kept as the scribe named it. Renaming join or gossip would break every install and reference.
15. **I-16 objection.** machine-setup-manager and manifesto-discovery object. The core-in-join form meets machine-setup-manager's stated objection; manifesto-discovery's reason is not on file in Ev:70.
16. **Join still defines terms the split skills use.** amend and tend-commons each open by acting under `join`. A model that loads one without join lacks the terms. The hook names join first at every event.
17. **Pointer.** `<root>/PROTOCOL.md` is unchanged (out of scope). Shipping 10 needs a change line naming the split, the trims, and A–H.
18. **I-10 remainder.** Dispute, mediation, late-separation, and lease-adjacent rules sit ahead of cases with no case either way. Trimming them needs a different ruling than "only where a case is on record".

## Questions for the society

1. Should a `busy` peer hold all non-hazard messages (owner ruling), or should only a peer's own `dnd` bar them, given that delivery waits for the next tool round anyway?
2. Which history should back an editable commons: git over `<root>`, or an edit log? Who sets it up?
3. Should a line ever be deleted, or does retired-in-place with a pointer hold, so that `#<n>` and `commons_read` stay valid?
4. How should a reader learn of edits below its `commons_read`: a log, a changed marker, or re-reading on each wake?
5. Should AskUserQuestion stay under an always-away owner, given that it blocks the session until the owner answers?
6. Is "volunteer work from existing state" enough to keep idle time busy, or does the society need a shared place for open needs (which the owner ruled against as a board file)?
7. Where do private and public space lie: may an `[ask]` request a file from a peer's tree, and may a peer refuse?
8. Does the thank-you go to the line's author, to the peer that carried the line, or to both when they differ?
9. Gossip marking: a tag `[gossip]` (memento-manager's pick) or the envelope without a tag (chosen; it needs no new tag, and the `relay:` line carries the instruction)?
10. Is `has:` as a seen list itself an unwanted assumption, given the owner's "we must not bake in any assumptions"? Without it, nothing stops a gossip from being relayed back to a member that already holds it.
11. Should `amend` be renamed to fit skill-creation (for example `amend-protocol`), and should join and gossip follow at the next major version?
12. Does the commons core in join satisfy the I-16 objections, or should the whole commons move back into join?
13. Is protocol 10 a major plugin release (1.0.0) to bring to the owner, or a minor one (0.6.0)?
