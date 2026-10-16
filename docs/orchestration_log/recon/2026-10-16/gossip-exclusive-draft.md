# Draft: gossip-exclusive ask-around and spread-around

Draft only. Not circulated, not shipped, no version bump, no pointer edit. Enactment needs the society's round (gather / protocol-change).

## Owner word

2026-10-16 evening, verbatim: "enforce ask-around and the other one to USE GOSSIP MECHANIC EXCLUSIVELY".

"The other one" = spread-around. Confirmed by gossip:15-17, which names exactly two originators: "Originate a gossip `[ask]` by the skill `ask-around`" and "Originate a gossip `[notice]` by the skill `spread-around`". No other skill fits better. Candidates checked and rejected: quote (level 1, its own gossip rules), aid (offers to a peer whose breakage you see, not an originator named by gossip).

Source: origin/main `peers/skills/*` at 4237ec4 (peers 0.8.0). Identical to the plugin cache 0.8.0 for both skills (diff empty).

## Old to new wording

### ask-around

| Line | Old | New |
|---|---|---|
| 4 (description) | "Seek what you need from peers you cannot name, by gossip, after your own cheap effort and a direct ask to any peer you know has it." | "Seek what you need from peers by gossip alone, after your own cheap effort." |
| 9 (terms) | ``Take `records`, `delivery`, `[ask]`, `[answer]`, `peer`, `commons`, `gossip`, and `pull` ...`` | adds `state` and `has:` (now used) |
| 16-18 `<ask-whom-you-can-name>` | "Send a direct `[ask]` by the skill `tell` to the peer you know has the thing; never gossip a need you can target." | removed; section replaced by `<ask-by-gossip>` |
| 20-21 `<ask-around-for-the-rest>` | "Gossip an `[ask]` by the skill `gossip` when you know no peer who has the thing; never leave a need unasked for want of a known holder." | "Ask only by a gossip `[ask]`, by the skill `gossip`, even when you know a peer who has the thing; never send a need by a direct `[ask]`." |
| new | — | "Seed it to two or three peers whose state lets them receive, any peer you know has the thing among them, and list on `has:` only you and them; never send it to every member you can name." |
| 23 | "Carry in every ask the need behind the question..." | unchanged, moved into `<ask-by-gossip>` |

`<spend-your-own-effort-first>` and `<close-the-search>` unchanged.

### spread-around

| Line | Old | New |
|---|---|---|
| 4 (description) | "Offer what you learned to the peers it may help: straight to those you can name, by gossip to those you cannot, and commons lines and new ideas to the peers and discourse they serve." | "Offer what you learned to the peers it may help by gossip alone, and commons lines and new ideas to the peers and discourse they serve." |
| 9 (terms) | ``Take `turn`, `society`, `card`, ...`` | adds `state` and `has:` |
| 16 section | `<send-to-the-peers-you-can-name>` | `<spread-by-gossip>` |
| 17 | "Send a finding by the skill `tell` to each peer whose current work needs it, judged by its card's `focus`, the work it has in hand, and `knows`, the topics it has depth in, or by what you saw of its work, in the turn you learn it; never keep it back." | "Spread a finding only as a gossip `[notice]`, by the skill `gossip`, in the turn you learn it; never send it by a direct `[notice]` or keep it back." |
| new | — | "Seed it to two or three peers whose state lets them receive, first those whose current work needs it, judged by its card's `focus`, the work it has in hand, and `knows`, the topics it has depth in, or by what you saw of its work; list on `has:` only you and them; never send it to every member you can name." |
| 19 | "Carry the distilled thing itself; never carry where to find it alone." | unchanged |
| 21 | "Send a commons line that helps a live peer's current work, judged by meaning against its card, as a `[notice] commons: <#n list>` carrying the line; never broadcast a line." | "Spread a commons line that helps a live peer's current work, judged by meaning against its card, as a gossip `[notice] commons: <#n list>` carrying the line, seeded with that peer; never broadcast a line." |
| 23 | "Batch the lines going to one peer in a turn into one such notice; never send one message per line." | "Batch the lines you spread in a turn into one such gossip; never send one message per line." |
| 25 | "End a message already going to a peer with at most one line `commons: ...`" | unchanged (originates no send; see open question 3) |
| 29 | "Gossip a finding whose takers you cannot name as a `[notice]` by the skill `gossip`; never sit on it for want of a known taker." | removed (folded into line 17's replacement) |
| 31 | "Carry deferred matters and new ideas to the society's public discourse, the commons and peer messages; never park them with the owner." | "... the commons and gossip; ..." |
| 33 | "Leave a lesson no peer's current work needs in the commons alone; never message it." | unchanged |

`has:` rule: gossip:31 already lists only self and recipients. The new seed sentence states it at origin anyway, because defect 1 (ambiguity-feedback.md) shows an origin can list five members on `has:` and leave relayers nobody to pass to.

## Conflicts

Each fix is a proposal for the round. None applied.

| skill:line | Sentence | Fix |
|---|---|---|
| gossip:4 | "... a need or finding you cannot target to a known peer, or a gossip message arriving with a `relay:` line." | "... a need or finding to ask or spread, or a gossip message arriving with a `relay:` line." |
| gossip:12 | section `<gossip-what-you-cannot-target>` | rename `<originate-by-ask-around-and-spread-around>` |
| gossip:13 | "Send a need or a finding straight to the peer you know has or needs it, by the skill `tell`; never gossip it." | delete. Direct contradiction. Add seed rule (defect 1): "Seed an origin gossip to two or three peers whose state lets them receive, and list only them on `has:`; never send it to every member you can name." Then drop the seed sentences from ask-around and spread-around (one home). |
| ontology:167 | "Call gossip a message passed from peer to peer past anyone its origin could name, ...; never call a send to a named peer gossip." | "...; never call a send without the envelope gossip." (Seeds are named peers; the envelope, not the receivers, makes gossip.) |
| ontology:183 | "Call push carrying knowledge to a peer whose work it helps, by a direct send or by gossip; ..." | "... by gossip, or by a direct send outside the skill `spread-around`; ..." — or "by gossip" alone if aid also goes gossip (open question 2). |
| ontology:185 | "Call pull seeking knowledge by a direct `[ask]` to a peer who has it, or by a gossip `[ask]`; ..." | "Call pull seeking knowledge by a gossip `[ask]`; ..." |
| tell:5 | trigger list `"ask a peer"`, `"pass on what my subagent found"` | drop both triggers; they route to ask-around and spread-around. |
| tell:15 | "Send peers what a subagent of yours reports that serves them, once you have checked it by the skill `vouch`; never send it unchecked." | "Spread what a subagent of yours reports that serves peers by the skill `spread-around`, once you have checked it by the skill `vouch`; never send it unchecked." |
| tell:23 | "Send freely to a peer presence shows `idle` or `waiting` — to learn, teach, ask, or aid — ..." | "... — to learn, answer, or aid — ...; ask and teach by gossip, by the skills `ask-around` and `spread-around`." |
| tell:27 | "Send a peer what affects or helps it in the turn you learn it; never hold it past that turn unless the skill `post` keeps it back." | "Send a peer what affects it in the turn you learn it, and spread a finding that helps it by the skill `spread-around`; never hold either past that turn unless the skill `post` keeps it back." |
| receive:39 | "Forward a direct ask you cannot answer to the peer you know has the thing, as gossip whose `from:` names the seeker, by the skill `gossip`; ..." | Holds only for direct asks from other skills (propose, reserve, settle). With ask-around gossip-only, ask-around asks arrive with `relay:` and go by receive:45. Fix: "Forward an ask without a `relay:` line that you cannot answer as gossip whose `from:` names the seeker, seeded to the peer you know has the thing among two or three, by the skill `gossip`; ..." |
| aid:15 | "Hand over help as an artifact — a file, commit, or finding — with one `[notice]` by the skill `tell`; ..." | Overlaps spread-around (a finding routed direct). Not in the owner's word. Fix only if the round extends exclusivity: "... with one gossip `[notice]` by the skill `spread-around` seeded with that peer; ..." Otherwise leave and add to spread-around nothing. |
| reserve:21 | "Ask the member a line names for its resource by the skill `tell` when you need it; ..." | A targeted need sent direct. Coordination of an exclusive resource, not knowledge pull. Recommend leave as is; flag for the round. |
| volunteer:31, 33 | "Teach by the skill `spread-around`; ..." / "Ask by the skill `ask-around`; ..." | no conflict; volunteer inherits gossip-only. |
| adopt:41 | "Thank the origin of what you adopt by a one-line `[notice]` sent by the skill `tell`; ..." | no conflict (thanks, not a need or finding). |
| join:27 | "Send that peer one `[notice]` naming your member id, start directory, and checkout; ..." | no conflict (address notice). |
| post | no sentence routes a need or finding | no conflict. |

Non-conflicts by kind (protocol, role, or reply sends, not needs or findings): propose:13, 17; gather:21; consent:23, 25; ship:33; card:79; leave:21; settle:15; vouch:19; receive:29; gossip:69; quote:35 (level 1, own rule).

## Branch

- Name: `draft/gossip-exclusive` (base origin/main 4237ec4, not pushed)
- Commit: `38d2833` — draft(peers): ask-around and spread-around originate by gossip only
- Worktree: `/Users/ryzhakar/pp/aoa-draft-gossip-exclusive`
- Files: `peers/skills/ask-around/SKILL.md`, `peers/skills/spread-around/SKILL.md`

## Open questions

1. Seed rule home. Draft places it in both skills (brief scope). Single home is gossip:13 replacement; needs consent to edit gossip. Recommend gossip, then remove from the two skills.
2. Exclusivity reach. Owner named two skills. tell:15, 23, 27 and aid:15 still permit direct finding and asking. Round decides: extend gossip-only to them, or route their findings and asks through the two skills (draft fixes above take the second path).
3. spread-around:25 piggyback line rides any message, gossip or not. Kept: it originates no send. If gossip-only means every byte spread-around writes travels by gossip, cut it.
4. Feedback (tell:33) and failed-claim notices (vouch:19) to the peer concerned: read as replies, outside the owner's word. Round confirms.
5. Commons line to one live peer now reaches two or three seeds and their relays. "never broadcast a line" stays true only if `spread:` names a scope; consider adding "naming its scope in `spread:`".
6. Ride with ambiguity-feedback defect 1 (gossip seeding) in the same round: this draft carries its wording for ask-around in stronger form.
