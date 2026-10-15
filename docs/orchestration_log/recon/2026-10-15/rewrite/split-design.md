# Split design: `tell` and `scribe`

Brief: `rewrite/split-design-brief.md`. Design only; no skill edited. Paths are `peers/skills/<name>/SKILL.md` unless named in full. Source: main 321f2f9.
Test for each sentence: what triggers it, and who acts on it (skill-creation "Cover one procedure per skill"). Procedures:
- **C** compose: choose receivers and content, and write the tagged message.
- **D** deliver: get a written message to its receiver at the time its level and the receiver's state allow.
- **R** convene a round: turn requests into a draft, circulate it, close the round, and report the outcome.
- **S** ship: write an enacted change into the protocol text and announce it.

## 1. Sentence by sentence

**tell** (the 9 terms sentence is excluded)
| line | sentence (short) | proc. | note |
|---|---|---|---|
| 13 | send as main session | C | rule for whoever sends; join:15 carries the same rule for joining |
| 15 | relay subagent reports once vouched | C | |
| 19 | send to the peers it concerns | C | |
| 21 | weigh the peer's time | C | |
| 23 | send freely to idle/waiting | C | |
| 25 | hazard to every session it endangers | C | restates ontology:207, level 1 reach |
| 27 | send in the turn you learn it, unless a hold | C | its "hold" clause points to D |
| 31 | type fits content | C | |
| 33 | feedback as `[notice]` | C | |
| 35 | honest feedback, never softened | C | near copy of receive:35 ("never soften that into agreement") |
| 37 | `[notice]` to the origin of a claim that failed your check | **vouch** | triggered by a check failing; vouch:13-17 has no step for what follows a failure |
| 39 | correct your own failure | C | |
| 41, 43 | escalate one level, say why | C | the level a message is written at; D reads it |
| 47-59 | type line, second line, stamp, one topic, ten lines, file, path | C | the message form |
| 63-67 | level 1 at once; hold level 2 for busy/dormant/dnd; release a held message | D | 63 and 65 restate ontology:207/209 as orders |
| 69 | retry held at each wake | D | heartbeat:45 says the same thing from the wake's side |
| 71-79 | inbox: append level 1 for an absent member; `reads` rules; one write each | D | |
| 83, 85 | await `[answer]`; silence is no answer | C | the sender's end of an ask; the roster edge tell→receive (skill-roster:53) |

**scribe** (the 9 terms sentence is excluded)
| line | sentence (short) | proc. | note |
|---|---|---|---|
| 13 | take up protocol once scribe gone, card edit + `[notice]` | **steward** | copy of steward:21; "never while live" is already held by ontology:199 (open = no live card names it) |
| 15 | a stewardship like any other, not an office | S | |
| 19 | keep canonical text; never write it without the stewardship | S | specialises steward:25 |
| 21 | keep the pointer | S | |
| 23 | write only what was consented to | S | |
| 27 | weigh the round's cost | R | |
| 29 | one `[ask] protocol draft: <path>` to every live peer | R | |
| 31 | close by protocol-change rules | R | |
| 33 | requests are a draft's source | R | |
| 37 | report each outcome with the path | R/S | deferred/separated close a round (R); enacted duplicates the 47 notice (S) |
| 39-49 | edit skills and hooks, raise card line, bump plugin, pointer line, `[notice] protocol v<N>`, flag lagging cards | S | |
| 53 | leave notice releases protocol, lists pending requests | **leave**/**steward** + R | release = steward:17; leave notice = leave:21; only "lists pending requests with their paths" is new, and it belongs to R |
| 55 | follow last shipped version while open; never edit | **protocol-change** | binds every peer, not the departing scribe; fits protocol-change:34-42 |
| 57 | keep requests as files while open | **propose** | copy of propose:19 + propose:23 |
| 59 | re-send pending requests to the new scribe | **propose** | the actor is the proposer; the scribe has left |

Checking the peers' claims (events.md:200, :201, :207). The tell split into compose and deliver holds. The scribe claim is half right. "Hand-on" is not a procedure the scribe performs: 53 copies leave and steward, 57 copies propose, and 55 and 59 are other parties' duties. The real seam is circulate against ship. ontology:237 already draws it: "never call circulating a draft shipping". ontology:229 defines a round as running from circulation to outcome, which is R exactly.

## 2. The split

**tell** (keeps its name): compose a tagged message to the peers it concerns and hand it to `deliver`.
- Keeps 13-35, 39-59, 83-85.
- 27 is reworded: "…never hold it past that turn unless the skill `deliver` holds it." The word "hold" stays inside the allowed phrase "never hold it past that turn" (test_terms OTHER_SENSES `held`).
- Adds one closing sentence for the C→D handoff: "Get each message to its receivers by the skill `deliver`; never deliver it by this skill alone."
- 37 moves to vouch as a new step after vouch:17, "Send the origin of a claim that failed your check a `[notice]` by the skill `tell`".

**deliver** (new): get a written message to its receiver at the time its level and the receiver's state allow.
- Receives tell:63-79.
- 69 stays only in deliver. heartbeat:45 becomes a pointer, "Retry held messages at each wake by the skill `deliver`", so the rule exists once.

**circulate** (new): turn protocol requests into a draft, circulate it, close its round, and report a deferred or separated outcome.
- Receives scribe:27, 29, 31, 33, and 37 narrowed to "deferred or separated".
- Adds "Name each pending request with its path in your leave notice when you leave keeping the stewardship `protocol`", the residue of 53.

**ship** (renamed from scribe; see §3): write an enacted protocol change into the protocol text and announce it.
- Keeps 15-23, 39-49.
- 47 now also covers the enacted outcome that 37 reported. One message replaces two (37 and 47 both reached every member).

Moves out, all into existing skills, with no new skill for hand-on:
- scribe:13 is deleted. steward:21 already covers it.
- scribe:53 splits. The release and the leave notice already live at steward:17 and leave:21; the pending-requests clause goes to circulate.
- scribe:55 → protocol-change, in `<apply-a-shipped-change>`: "Follow the last shipped version while the stewardship `protocol` is an open stewardship; never edit the protocol text meanwhile."
- scribe:57 is deleted (propose:19 and :23 cover it).
- scribe:59 → propose: "Re-send each open request to a new scribe once its `[notice]` taking up the stewardship `protocol` arrives; never drop one."

Copies the split would create, and how each is avoided:
- (a) tell:69 and heartbeat:45: one owner (deliver); heartbeat only points to it.
- (b) The level 1/2 behaviour in deliver and ontology:207/209: ontology defines it, deliver orders it. No sentence is shared, so test_skills:163 holds.
- (c) gossip:53 holds a level 2 relay "as the skill `tell` holds". Gossip sends by tell (gossip:37), which sends by deliver, so 53 becomes a copy. Delete it.
- (d) tell:35 and receive:35 are near copies. This exists before the split; flagged only.

## 3. Names (lenses: 1 self-documenting, 2 anarchy, 3 peer-to-peer, 4 namespace; principle ids from naming-lenses.md §1)

Installed-skill check (find over both plugin caches, 2026-10-15): no `deliver`, `route`, `post`, `circulate`, `convene`, `draft`, `ship`, `publish`, or `scribe` outside peers. Neither is any of them a peers skill (`ls peers/skills`).

**D: deliver procedure**
1. `deliver`: 1.1 intent, 2.8 everyday, 3.3 reads well in "by the skill `deliver`", 4.4 no clash. ✗ 3.2 partly: ontology:109 calls delivery the harness hand-off, and ontology:163 says an inbox append is not a delivered message. Fix: widen nothing; the inbox and hold branches are how a message is delivered later. Otherwise rename ontology's term.
2. `route`: 1.1, names the branch choice, no clash. ✗ 1.2 (plumbing word), ✗ 2.7 (no wink).
3. `post`: 2.7 (postal wink: the post office holds, boxes, and delivers), 2.8. ✗ 3.2 and 1.8: "post" reads as putting a line on a board, and level 3 board lines are never sent (ontology:211).

**R: convene procedure**
1. `circulate`: 1.1, names scribe:29's act; 3.4, already a trigger phrase (scribe:5 "circulate a protocol draft", peers/README.md:88); 3.2, matches the term ontology:229/237 uses; 2.8. ✗ 1.3 slightly: closing the round is implied, not named.
2. `draft`: 1.1, 2.8. ✗ 3.2: `draft` is an ontology noun (ontology:227), and a proposer also drafts wording (propose:19).
3. `convene`: 1.1. ✗ 2.4 (assembly/legislature tone); a peer flagged it at events.md:132.

**S: ship procedure**
1. `ship`: 1.1, 3.2 (exactly ontology:237's "shipping"), 2.8, `peers:<verb>`. The role noun "scribe" stays in ontology:201 and on cards.
2. `scribe`: 2.7 (to scribe = to write, a wink), zero rename cost, owner-named (skill-roster:27). ✗ 2.3: strangers read a rank-like role noun (naming-lenses:73). ✗ 1.1: names who, not what.
3. `publish`: 2.8, 1.1. ✗ 3.2: a second word for "shipping" (skill-creation "one term per concept").

**C: compose procedure** keeps `tell`: owner-named (skill-roster:10), the hook target (hooks.json:2), and 16 calling sentences (§4). Renaming it buys nothing.

## 4. Graph after the split

Edges are named references (skill → skill), `ontology` omitted.
- tell → vouch (15), deliver (new closing), receive (83). In: card:79, leave:21, receive:29, gossip:13, :37, :71, ask-around:17, spread-around:17, adopt:41, aid:15, settle:15, reserve:21, propose:13, :17, consent:23, :25, vouch (new, from tell:37). Every in-sentence keeps "by the skill `tell`" unchanged.
- deliver → (none besides ontology). In: tell (new), heartbeat:45 (was tell).
- circulate → protocol-change (31), propose (33), tell (29, 37 sends). In: steward:41, leave:15, receive (new, below).
- ship → card (41, names the card instruction), tell (47). In: steward:41.
- vouch → tell (new; vouch stops being a leaf, skill-roster:64).
- propose gains no edge; its new re-send sentence uses tell (existing edge).
- protocol-change stays a leaf (its new sentence names no skill).

Sentences in other skills that name tell or scribe, and what each becomes:
- steward:41 "Serve the stewardship `protocol` by the skill `scribe`" → "…by the skills `circulate` and `ship`". test_terms `scanned_body` strips "by the skills X, Y, and Z" lists; the two-item form "by the skills a and b" also matches its regex.
- leave:15 "Hand on the stewardship `protocol` by the skill `scribe`…" → "Name your pending protocol requests by the skill `circulate` when you keep the stewardship `protocol`; never leave with them unnamed."
- heartbeat:45 "…by the skill `tell`" → "by the skill `deliver`".
- gossip:53 is deleted (§2 c).
- receive gains in `<hand-on-each-kind>`: "Take a protocol request sent to you as the scribe by the skill `circulate`; never take one in another way." Without it, circulate is reachable only through steward.
- All other tell sentences are unchanged.

Reachability:
- join → card (join:51) → tell (card:79) → deliver.
- join → heartbeat (join:69) → deliver.
- join → receive (join:67) → circulate.
- join → card → leave (card:93) → steward (leave:13) → circulate, ship.
- resume → join (resume:13), so everything above is also reachable from resume.
- A party loads only its own skill plus protocol-change. The convener loads circulate, the proposer propose, a receiver consent, and none of the three names another.

## 5. Hooks and tests

- send-stamp.sh names no skill (send-stamp.sh:1-47). It stamps the second line, which stays in tell (tell:49-51). No change.
- hooks.json:2 says "the send stamp the skill peers:tell relies on". Still true, no change. The owner's hook ruling (SessionStart → join/resume, send-stamp → tell, wake → heartbeat) holds.
- Templates (peer-join/resume/compact.txt) name neither tell nor scribe. No change.
- test_skills.py:20-24 ROSTER: add `circulate`, `deliver`; replace `scribe` with `ship` (if rank 1). 25 → 27. Rename `test_skill_set_is_the_protocol_10_roster` (test_skills:27) to the shipped version.
- test_skills.py:63-64 `Carry \`protocol: 10\``: changes with the version ship raises (scribe:41).
- test_skills.py:163 (no shared sentence) is the guard for every move in §2. Run it after each move.
- test_skills.py:43 (every `peers:` reference resolves) covers peers/README.md. Its entries for scribe (README:128-130) and tell (README:163-165) need edits, deliver and circulate need new entries, and README:88 (propose, already stale: "as the scribe, circulate the draft") needs a fix.
- test_terms.py OTHER_SENSES `held` allow-list carries `"<deliver-or-hold>"`, `"</deliver-or-hold>"`, `"deliver it, hold it, or append"` (tell's tag and description), and `"Hold a relay of a level 2 gossip"`, `"holds a level 2 message"` (gossip:53). Move the first three to deliver's wording and drop the gossip pair.
- test_terms.py `test_terms_sentence_names_every_ontology_term_the_body_uses` needs:
  - each new skill's terms sentence generated from its body;
  - tell's list shrunk (inbox, dnd, held, delivery, level 2 leave);
  - vouch gaining `[notice]` and `origin`;
  - propose gaining `stewardship`/`open stewardship` and `scribe`;
  - protocol-change gaining `open stewardship` and `stewardship`.
- The plugin version gets a middle bump, since this is a rule change (scribe:43).

## 6. Other content in the wrong place

- **Ten-line limit** (tell:55; repeated as a number at receive:31, propose:21, gossip:33). It belongs in tell; it is the message form. A move into ontology:115's message-body definition would make ontology a rule bucket (naming-lenses:216). Keep it in tell. The three repeats state the same constant, so each could say "the message body limit the skill `tell` sets". Cost: three edits, and the terms tests re-run. Recommend: leave as is; the constant has not drifted.
- **Second line** (tell:49-51). It belongs in tell: the hook stamps it, and ontology:129 defines reply time by it. No move.
- **Level-based delivery** (tell:63-79) moves to deliver (§2). Cost: one new skill and four edits (heartbeat:45, gossip:53, two tests).
- **Hazard reach** (tell:25) restates ontology:207. Keep it: it is the order, and ontology the definition. No exact-line copy.
- **Claim-failure notice** (tell:37) → vouch (§1). Cost: vouch loses its leaf status and gains two terms.
- **Outcome report** (scribe:37) is split so an enacted change reaches members once (§2). Cost: rewording 37 and 47.
- **dnd self-set, bounded** (owner, events.md:326). Card changes are listed here, not made:
  - card:87 "Set `state: dnd` when the owner orders…; never on your own judgment" → "Set `state: dnd` for yourself with a reason and an end time; never set it without both."
  - card:89 → remove it at that end time or on your return, whichever comes first.
  - card:71 `state` carries the reason and the end (e.g. `state: dnd until <stamp>: <reason>`). Alternatively add a field, which breaks card:75 "never another" unless listed.
  - ontology:103: a member is dnd only while the end time is in the future.
  - deliver (from tell:65): hold for dnd until its end time, its clearing, or the reply time.
  - ontology:207 is unchanged (level 1 still reaches dnd).
  - card:5 description "set dnd", "lift dnd" stays.
  - No script touches `state` (`grep state peers/bin/*`: no hit).

## 7. Risks and questions

Risks:
- R1. Two new skills add to the 25 descriptions every session lists (events.md:200, "24 descriptions in every skill list"). The net is +2 skills; hand-on's dissolution saves the third.
- R2. If `scribe` is renamed to `ship`, the member id `…/scribe` (ontology:57 example) and the role noun stay. A reader may look for a skill named scribe. Mitigation: ship's description names "as the scribe".
- R3. `deliver` against ontology's narrower "delivery" (ontology:109, :163) could confuse until ontology words it as the harness act within the skill.
- R4. Moving scribe:59 to propose puts a duty on proposers that 10 does not carry. This is a protocol change that needs the round itself.
- R5. Deleting gossip:53 relies on gossip sending through tell→deliver. gossip:37 says so, but a model reading gossip alone loses the hold rule.

Questions for the owner:
- Q1. Rename `scribe` to `ship`, or keep `scribe` as the shipping skill's name?
- Q2. Name the delivery skill `deliver` (rank 1), or `route`?
- Q3. Name the round-convening skill `circulate` (rank 1), or another?
- Q4. Should the new failure-notice step make vouch a non-leaf (vouch → tell), or should tell:37 stay in tell?
- Q5. Should dnd's reason and end live inside `state:` or in a new card field?
- Q6. Do the split and the dnd change ship together as one protocol version and one round?

Summary: tell splits on a clean seam: everything that writes the message stays in `tell` (which keeps its name, its hook, and all 16 calling sentences), and the level- and state-based routing (tell:63-79) moves to a new `deliver`. scribe's "hand-on" is not a procedure but copies of steward, leave, and propose plus duties of other parties, so it dissolves into those skills, and the true seam, which ontology:237 already draws, is circulating a round (new `circulate`) against shipping the text (`ship`, or `scribe` kept). Hooks need no change, the tests need roster, terms, allow-list, and README edits, the dnd self-set change touches card:71/87/89, ontology:103, and deliver, and six one-sentence questions remain for the owner.
