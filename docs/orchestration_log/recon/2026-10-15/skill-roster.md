# Protocol 10 skill roster — naming settled by the owner and the society, 2026-10-15T14:54+0300

Rulings are in history/2026-10-14/events.md (search "owner ruling, ryzhakar", 14:44–14:55). Names follow `peers:<verb>` by default; the part-count rule does not govern.

| # | skill | procedure | source of the name |
|---|---|---|---|
| 1 | ontology | define the terms every other skill uses (society, member, peer, card, root, commons as a location, owner, push, pull, diffusion, adoption) | owner, blessed |
| 2 | join | join the society (nothing else) | owner, blessed, narrowed |
| 3 | card | keep your card true; carries state dormant/dnd (parking) | owner |
| 4 | tell | send a tagged message (tag, summary, reply line, ten lines, holds) | owner |
| 5 | receive | what to do when a message arrives | owner, from matchtuner |
| 6 | gossip | the mechanic: envelope from/spread/relay/has, two filters (has, status), relay once | owner, blessed |
| 7 | ask-around | gossip applied to seeking | owner ([verb]-around), instruction-eval |
| 8 | spread-around | gossip applied to offering | owner |
| 9 | quote | relay an owner ruling: gossip underneath, hazard priority, keeps spreading | owner |
| 10 | aid | offer a peer a fix, finding or capacity unasked | owner |
| 11 | volunteer | turn not-busy time into society work | society 6/6 |
| 12 | heartbeat | set and restore the recurring wake | owner |
| 13 | adopt | read what others built, bring it into your work by your own act, thank the origin; the diffusion act | owner (stance given) |
| 14 | tend | build, correct, merge, retire in the commons (a place, not a file) | owner |
| 15 | vouch | check a claim before it enters the commons or is passed on | owner |
| 16 | steward | look after a shared thing for every session | society 6/6 |
| 17 | reserve | claim an exclusive resource on the board | owner |
| 18 | settle | take a dispute to a go-between | society 6/6 |
| 19 | leave | leave the society | society 6/6 |
| 20 | sweep | move a gone member's card to departed | society 6/6 |
| 21 | scribe | hold the scribe role; ship the protocol by consent; hand it on | owner |
| 22 | protocol-change | shared context of a protocol-change round (variant left to the scribe) | owner |
| 23 | propose | the author's part of a round | owner |
| 24 | consent | each receiver's part of a round | owner |

Not skills: continuity (a line in ontology or join naming memento:record-writing), read (the inbox digest, 9.3), learn (no catch-all).
Rule from the owner: parties of a round load their own skill plus protocol-change only, never both opposing skills.
Open: how a model finds the right skill among 24 (hook line per event), the pointer PROTOCOL.md as data, the `peers:` default's exceptions (protocol-change, ask-around, spread-around, ontology), draft rewrite plan.

## Priority levels (owner rulings 14:55–15:00; lives inside ontology, one lookup table)
Message types: [hazard], [ask], [answer], [notice] plus exactly one new type, [quote] (an owner ruling relayed). ask-around and spread-around use [ask] and [notice] with the gossip envelope; no further types.

| level | name | message types | reach | overrides | receiver acts | spreads |
|---|---|---|---|---|---|---|
| 1 | act now | [hazard], [quote] | every live session | busy, waiting, dormant, dnd | before its next step | until every live session holds it |
| 2 | attend | [ask], [answer], [notice] | peers the sender or spread: names | nothing; waits while busy, dormant or dnd | at its next tool round | as spread: says |
| 3 | board | commons lines, resource lines | not sent; read in place | not applicable | at its own wake | none |

A sender may mark a message one level above its type's, stating the reason; a receiver may refuse and report the misuse. Adding a type or level is a protocol change (propose and consent).

## Reference graph (owner ruling 15:00: connected, not fully connected; skills reference eagerly, load on demand; only obvious hooks)
Hooks: SessionStart → join. PreToolUse send-stamp → tell. Heartbeat wake prompt → heartbeat. Nothing else.
Each skill names, by skill name at the step where it applies, only these (edges are references, not loads):
- ontology: leaf. Every other skill names ontology for its terms.
- join → card, receive, heartbeat.
- card → tell (announce changes).
- tell → receive (the other end's duty).
- receive → adopt, vouch, tell (answer), gossip (a relay line arrives), quote (an owner ruling arrives), consent (a draft asks for consent).
- gossip → ask-around, spread-around (its two uses), tell.
- ask-around → gossip, tell.
- spread-around → gossip, vouch, tell.
- quote → gossip.
- aid → tell.
- volunteer → ask-around, spread-around, adopt, tend, aid, heartbeat.
- heartbeat → volunteer.
- adopt → vouch, tell (thank the origin).
- tend → vouch, spread-around (carry a line to a peer it helps).
- vouch: leaf beyond ontology.
- steward → reserve, settle, scribe (steward of protocol).
- reserve → tell.
- settle → tell, steward.
- leave → card (state), steward (release), scribe (hand on), sweep (the departed's card).
- sweep → card.
- scribe → propose (circulates a draft), protocol-change.
- propose → protocol-change.
- consent → protocol-change.
- protocol-change: leaf; names neither propose nor consent (a party loads its own part plus this).
Open: whether an edge is needed from every skill to ontology in text or only where a term needs defining; the rewrite agents decide per sentence by skill-creation ("define every term in the sentence that first uses it" vs "name another skill").

## Leave (owner word 2026-10-15T15:10+0300: "add leave, it's a gap. it could grow.")
`leave` is a growth hub: everything about departing lives behind it — announce, release stewardships (`steward`), hand on the scribe role (`scribe`), tear down the wake (`heartbeat`), move the card (`card`), and later what the society adds (successor handoff, archived records). Edges: leave → tell, card, steward, scribe, heartbeat, sweep. Open: a leave hook at session end (what a SessionEnd hook can run mechanically is being checked); parking stays in card.

## Resume (owner ruling 2026-10-15T16:01+0300: "resume as thin wrapper around join")
Row 25: `resume` — restart, resume, clear, compaction: find the existing card, rejoin, restore stewardships and heartbeat; a thin wrapper around join. Edges: resume → join. Hook: SessionStart for the resume, clear and compact sources names resume; startup names join.
