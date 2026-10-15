# Audit A, round 4: ontology, join, resume, card, tell, receive, leave

Branch `draft/10-skills`, head e336865, `/Users/ryzhakar/pp/aoa-skills/peers/skills/<name>/SKILL.md`. Same rules (one-part-name rule void). Done from scratch on the current text; `self-audit.md` not read.

Mechanical checks, all seven skills: R3, R4 (no `version`), R6, R7, R9-R13, R17 PASS. R20/R21 PASS: grep `only|always|must` empty; a script counted exactly one `never` outside backticks in every body sentence. R16 PASS. Edges PASS and unchanged from round 3: join names card, receive, heartbeat; card names tell; tell names receive; receive names adopt, vouch, tell, gossip, quote, consent; leave names tell, card, steward, scribe, heartbeat, sweep; ontology and resume (join only) as before; no extra edge. The terms test (pytest stubbed) reports used-not-listed `[]` and listed-not-used `[]` for join, resume, card, tell, receive, leave.

## Extra check: sense of each listed term in the body
Method: for every term in each skill's terms sentence, listed every body or description line the test's pattern matches (up to three read per term, all read when fewer) and compared each use with the ontology definition. Sample of checked pairs (definition, then use):
- `body`: ontology 45 "a member's body the session that currently runs it" / card 35 "your body's address from presence" OK; ontology 111 "a message body the lines of a message after its second line" / tell 53 "Keep the message body to facts and paths on one topic" OK.
- `state`: ontology 101 "what presence shows of its session together with its card's `state` line" / card 71 "Carry `state` while you are parked" OK; tell 27 "the peer's state" OK.
- `held`: ontology 117 "a message held while its sender keeps it unsent until the receiver's state clears" / tell 65 "never drop a held message" OK.
- `origin`: ontology "the member whose line, answer, or message first brought it" / tell 37 "Send the origin of a claim that failed your check" OK.
- `seeker`: ontology "the member whose need an `[ask]` carries" / receive 29, 35, 37 OK.
- `stamp`: ontology 37 "a minute in the form `2026-10-14T09:30+0300`, read from the clock" / card 73 "the stamp of the card's last edit, read from `date`" and join 39 "its last-edit stamp" OK.
- `wake`: ontology 39 "a timer the harness fires" / join 69, resume 21, card 69, leave 17 OK.
- `checkout`: ontology 61 "the absolute path of the worktree a member works in" / join 23, 25, 27; tell 57 "a file in your checkout" OK.
- `peer`: ontology "any live member with a card in the root" / join 21 to 29, tell 19 to 25, leave 21 OK.
- `live`, `presence`, `busy`/`idle`/`waiting`, `dormant`/`dnd`, `member id`, `departed card`, `pointer`, `change line`, `commons line`, `commons_read`, `inbox`, `gossip`, `from:`, `has:`, `relay:`, `spread:`, `claim`, `escalation`, `level 1`/`level 2`, `delivery`, `leave notice`, `stewardship`, `compaction`, `plugin`, `host`, `login`, `worktree`: every use read in the sense the ontology gives.
Wrong-sense uses found (word listed under `ontology`, used in another sense):
| line | ontology definition | body use |
|---|---|---|
| tell 43 | `state`: "what presence shows of its session together with its card's `state` line" | "State the reason in each message you escalate" (verb) |
| tell 5 | `relaying`: "passing a received gossip on to members who lack it" (ontology 163) | description: "relay what my subagent found" (not gossip) |
| card 19 | `turn`: "one stretch in which a session works" | "never turn it into a project record" (verb) |
| card 51 | `records`: "the files its project keeps for decisions, owner rulings, ..." | "the model ID your harness records on your latest reply" (verb) |
| join 67 | `act`: "a tool call" | "Act on the messages waiting for you" (verb) |
| resume 17, 19 | `act`: "a tool call" | "never act from a condensed memory of it" (verb) |
| receive 17, 19, 21 | `acting on a level 1 message`: "making each act it calls for ... from you" | "Act on each message at the moment its priority level sets", "before acting on it" (any level) |
Leave: no wrong-sense use.

## Remaining violations per skill

### ontology: 2
| rule | line: text |
|---|---|
| R26 | 4, 9, 29, 31, 53: "skill" (a protocol artifact the whole ontology speaks of: "never call a skill a hook", "a package of skills and hooks") is not defined |
| R26 | 197 (level 1): "or the sessions or scope a `[quote]`'s sender knows it concerns" ("scope" undefined; names no rule) |
Verdict: **2 violations**.

### join: 1
| rule | line: text |
|---|---|
| R26 (wrong sense) | 67: "Act on the messages waiting for you" (see table) |
Verdict: **1 violation**.

### resume: 1
| rule | line: text |
|---|---|
| R26 (wrong sense) | 17: "never act from a condensed memory of it"; 19: "never act from a condensed memory of one" |
Verdict: **1 violation**.

### card: 2
| rule | line: text |
|---|---|
| R26 (wrong sense) | 19: "never turn it into a project record" |
| R26 (wrong sense) | 51: "the model ID your harness records on your latest reply" |
Verdict: **2 violations**.

### tell: 2
| rule | line: text |
|---|---|
| R26 (wrong sense) | 43: "State the reason in each message you escalate" |
| R26 (wrong sense) | 5: "relay what my subagent found" against `relaying` listed at 9 |
Verdict: **2 violations**.

### receive: 1
| rule | line: text |
|---|---|
| R26 (wrong sense) | 17: "Act on each message at the moment its priority level sets"; 19: "before acting on it"; 21: "before acting on it" |
Verdict: **1 violation**.

### leave: 0
Verdict: **CONFORMS**.

## Round-3 findings
- ontology: FIXED body senses (111 defines message body; 161 uses "gossip's message body"), forward use of "state" (87 now spells out mid-turn, between turns, at a prompt) and "type" (107 now says "one of the bracketed words below"), "plugin" (31 defines it), "sender's rule" (197 reworded; residual "scope" above).
- tell: FIXED "body" (message body listed, defined, used at 53-59).
All round-3 findings fixed.

## New violations from round 4's changes
- tell 5 / 9: listing `relaying` (new in round 4) exposes the description's "relay" as a wrong sense.
- ontology 197: the reworded level 1 sentence introduces "scope".
- The test now scans descriptions and derived forms, which surfaces the verb uses above (state, turn, records, act); none were introduced by round 4 text except tell 5 and the ontology 197 "scope". The ontology still never defines "skill".

## Summary
Round 4 fixed all round-3 findings and every skill's terms sentence lists the terms its body and description use. The spot-check of each listed term found the ontology's sense in nearly every use, with wrong-sense uses of the words state (tell 43), turn (card 19), records (card 51), relay (tell 5) and act (join 67, resume 17-19, receive 17-21) used as verbs or in a wider sense, plus ontology gaps at "skill" and "scope" (197). Counts: ontology 2, join 1, resume 1, card 2, tell 2, receive 1, leave 0.
