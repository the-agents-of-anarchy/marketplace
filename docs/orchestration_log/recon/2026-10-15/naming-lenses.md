# Naming lenses: principles and ranked options for the peers skills

Brief: `recon/2026-10-15/naming-lenses-brief.md`. No name chosen here; the society chooses.

Sources, abbreviated:
- SDC `.claude/manifesto-repo/LLM_MANIFESTOS/manifestos/self-documenting-code.md`
- R, D, A101 `~/.local/share/agents-of-anarchy/culture/{roots.md, deliberations.md, anarchy-101.html}`
- SP `~/pp/claude-skills/orchestration_log/recon/2026-10-14/agents-of-anarchy/spec.md`
- J, G `~/pp/aoa-participation/peers/skills/{join,gossip}/SKILL.md`; HK `peers/hooks/templates/peer-join.txt`
- PJ `peers/.claude-plugin/plugin.json`; MJ `aoa-participation/.claude-plugin/marketplace.json`
- SC `~/.claudes/meta/plugins/cache/memento/memento/0.5.1/skills/skill-creation/SKILL.md`
- EV `docs/orchestration_log/history/2026-10-14/events.md` (this repo); STR `LLM_MANIFESTOS/instructions/strunk_spr_v3_complete.xml`

Marks: **D** derived (follows from the quote), **I** inferred (my reading).

## 1. Principles per lens

### Lens 1: self-documenting code
| id | Principle | Quote | Mark |
|---|---|---|---|
| 1.1 | Name the intent, not the mechanism | SDC:50 "They should reveal intent, not implementation." | D |
| 1.2 | Use domain words (card, commons, go-between), not plumbing (inbox, hook, SendMessage) | SDC:264 "Require business-domain names, not technical jargon" | D |
| 1.3 | Prefer the specific word to the generic one (`use-`, `do-`, `handle-` fail) | SDC:54 `get_data(id)` weak vs `fetch_positive_balance_transactions_for_user(user_id)` strong | D |
| 1.4 | No "and" or "or" in a name; a joined name means two procedures | SDC:175 "If you need "and" in your function name, it's doing too much" | D |
| 1.5 | No catch-all bucket | SDC:184 "'Utils' and 'Helpers' are where self-documentation goes to die" | D |
| 1.6 | Names listed together read as the process they serve | SDC:60 "Your code should read like prose"; SDC:62-71 | I |
| 1.7 | Structure follows how practitioners think | SDC:86 "match how domain experts think" | D |
| 1.8 | Write names for the newcomer, not for the insider | SDC:255 "couldn't guess what `proc_dt_calc` meant" | D |
| 1.9 | A mode belongs in the name or in its own skill; never hide it inside one | SDC:192-197 `process_without_validation(data)` | I |

### Lens 2: the anarchy philosophy
| id | Principle | Quote | Mark |
|---|---|---|---|
| 2.1 | Write names that strangers can read | SP:6 "naming speak to strangers from day one" | D |
| 2.2 | The society owns the vocabulary and changes it by consent | SP:20 "the society takes ownership after, changing it by consent"; D:22 "it never decides alone" | D |
| 2.3 | Name an act any member performs, never a rank | R:39 "no session decides for others"; A101:894 "Everybody has some, but nobody has very much" | I |
| 2.4 | No legislative words (vote, elect, majority, govern) | R:51 "the society counts no votes"; A101:961 "not a legislature. No one is elected." | D |
| 2.5 | Stewardship is service, not property (`serve` over `hold`, `own`, `claim`) | D:34 "a stewardship is a service any session may question"; D:35 "Given up: first claim as title" | D |
| 2.6 | Draw on the seed words | SP:15 "band, trade-partners/gifts, go-between, neighbors watching, federation upside down, direct action" | D |
| 2.7 | Plain, with a wink | SP:21 "a skeptic's questions answered plainly, with a wink" | D |
| 2.8 | Use everyday words over political ones | A101:906 "everyday life is almost entirely anarchist" | I |
| 2.9 | Keep Black's term where the protocol took it | R:44 "mutual aid — cooperation rather than competition"; A101:1025 | D |
| 2.10 | Keep the owner out of the society: a name may cite the owner's word, never cast the owner as a member | R:45 "the owner stands outside the society as its deity" | I |

### Lens 3: peer-to-peer communication
| id | Principle | Quote | Mark |
|---|---|---|---|
| 3.1 | Names follow the address form peers already use | J:67 role is "one to three lowercase hyphen-joined words naming its ongoing work" | D |
| 3.2 | Wire tokens are single reserved words; a name holding one should mean that token | J:223 tags `[notice]` `[hazard]` `[ask]` `[answer]`; G:45 `from:` `spread:` `relay:` `has:` | D (tokens), I (rule) |
| 3.3 | A name must fit the sentence slot "by the skill `X`" | J:261 "by the skill `gossip`"; J:339; J:407; SC:52 "Reference another skill by name" | D |
| 3.4 | Name the act as peers say it aloud | G:5 "ask around", "who knows", "pass it on" | I |
| 3.5 | Name the stable function, not the current location | J:67 "never name a member by its address" | I |
| 3.6 | A hook line pairs each name with its purpose; the name should predict the purpose | HK:1 "load peers:gossip to spread a need or finding you cannot target" | D |
| 3.7 | Topic words are shared across `knows`, commons tags, and names | J:209 `knows` "as the commons tag words" | I |

### Lens 4: namespace mechanics
| id | Principle | Quote | Mark |
|---|---|---|---|
| 4.1 | A name resolves as `peers:<skill>`; the marketplace never appears | SP:28 "install `peers@agents-of-anarchy`, skills `peers:<skill>`"; PJ:2; MJ:2 | D |
| 4.2 | The prefix already says "peers"; a name that repeats it wastes a part | STR:1295 "OMIT NEEDLESS WORDS"; SC:26 three-part cap | I |
| 4.3 | The bare name travels alone, in skill text and in journals | J:261 "by the skill `gossip`"; EV:112 "skill `amend` renamed" | D |
| 4.4 | Because of 4.3, a bare name must not clash with another installed skill | follows 4.3; list in section 4 | I |
| 4.5 | Name = directory = every site that cites it; each rename moves a directory and edits every citing site | SC:28 "Set the directory name to `name`"; EV:118 "list every name site … for a mechanical rename" | D |
| 4.6 | The hyphen joins parts and also sits inside compounds (`go-between`), so a part count can be ambiguous | SC:26 "hyphen-joined" | I |

## 2. Tensions and convergences per pair

| Pair | Tension (both sides) | Convergence |
|---|---|---|
| 1–2 | SDC:54 long specific names vs SP:21 "plainly, with a wink" (`gossip`, `pitch-in`) | SDC:255 newcomer = SP:6 stranger: both name for the outsider |
| 1–3 | SDC:50 "reveal intent" vs J:223/G:45 wire tokens: `ask-around` names an intent and also echoes the `[ask]` tag | One term per concept (SC:70): a token word in a name means that token |
| 1–4 | SDC:54 specificity vs SC:26 "never carry a fourth part" | SDC:86 structure carries meaning: the `peers:` prefix supplies context the name drops |
| 2–3 | R:39 no ranks vs J:405 "the scribe", a named role peers must address | A101:1015 direct action and J:67 role = "ongoing work": both name work, not station |
| 2–4 | SP:20 vocabulary changes by consent at any time vs SC:28 + EV:118: every rename moves directories and edits every citing site, hooks, cards, journals | SP:27 plugin `peers` chosen for meaning ("band" recalls music only); the prefix already speaks for the society |
| 3–4 | J:261 bare names in prose vs 4.4 bare names clash across plugins (`owner-ruling`, `relay`) | J:67 `<project>/<role>` mirrors `peers:<skill>`: both are a prefix plus a short work name |
| 1–1 internal | SDC:175 no "and" vs procedures stated with "and" (P6, A2) | Signal to split, per SC:12 |

## 3. Conflicts with skill-creation's name rule (SC:26)

Rule: "two or three lowercase parts, hyphen-joined, naming what it does; never carry a fourth part."

1. One part: `join`, `gossip`, `ontology` (owner-accepted, EV:116, EV:144); `amend` (working name, EV:139); candidate `leave`. All five fail "two or three". The rules file carries no exception for an owner acceptance.
2. "Naming what it does": `ontology` names content, not an act. SC:38 makes the same distinction for tags ("never name a tag for its content alone"). `commons` (EV:121 pick) failed on the same ground and was withdrawn (EV:131).
3. The rule does not require verb-object form. The ecosystem holds two patterns: verb-object (`tend-commons`, `check-back`, `work-silently`) and object-gerund (`record-writing`, `skill-creation`, `owner-ruling`). Lens 1.6 and 3.4 favour verb-object, because names in a hook line then read as acts.
4. Lens 1.3 specificity against the three-part cap: `volunteer-when-idle` fits the cap; `steward-shared-thing-or-resource` does not.
5. Idioms (`pass-it-on`, `pitch-in`, `take-leave`) meet the form but name what the skill does only through the idiom (2.7 vs 1.8).
6. Hyphenated compounds (4.6): `ask-go-between` holds two or three parts depending on how one counts.
7. Convergence: SDC:175 "no and" = SC:12 "one procedure per skill"; a name that needs "and" or "or" marks a skill that must split.

## 4. Namespace analysis

Resolution: plugin `peers` (PJ:2) in marketplace `agents-of-anarchy` (MJ:2). The skill is invoked as `peers:<skill>` (SP:28) and its directory is `peers/skills/<skill>/` (SC:28). The marketplace never appears in the reference. Two plugins named `peers` from two marketplaces therefore share one prefix.

The split of information:
- The prefix `peers:` says "society business".
- The name says the act.
- Repeating the prefix (`peers:peer-protocol` in `my-claude-skills/peers/0.3.0`; candidate `peers:message-peer`) spends a part on what the prefix said (4.2).
- Naming the society in a name (`agents-of-anarchy-…`) breaks the cap at once.

Installed today in `~/.claudes/meta/plugins/cache` and `~/.claude/plugins/cache` (89 skill copies, 69 distinct names):

| Word or name | Where installed | Clash with |
|---|---|---|
| plugin `peers` twice | `my-claude-skills/peers/0.3.0` (`peer-protocol`, `gossip-around`); `agents-of-anarchy/peers/0.4.0, 0.4.2` (`join`, `gossip`) | the prefix itself; SP:37 dropped the old home, but its cache remains |
| `peer-protocol` | `my-claude-skills/agent-conduct/1.7.0`, `my-claude-skills/peers/0.3.0` | any name with `peer` |
| `gossip-around` | `my-claude-skills/peers/0.3.0` | `gossip` (stale predecessor) |
| `owner-ruling` | `memento/memento/0.5.1`, `my-claude-skills/memento/0.5.1` | candidate `relay-owner-ruling` (substring; journal grep hits both) |
| `staging-relay` | memento 0.5.1 | `relay` also G:51 envelope line |
| `record-writing`, `record-promotion` | memento 0.5.1 | candidate `keep-own-records` |
| `authority-check` | memento 0.5.1 | J:53 "authority check" (same concept, different owner: consistent) |
| "amend" (word) | memento `schema-resolution/SKILL.md:42` "Amend the schema on the owner's word" | `amend`, `amend-protocol`: memento reserves the verb to the owner (EV:126) |
| `check-back` | `my-claude-skills/agent-conduct` | wake in P5 (same mechanism, different act) |
| `init`, `setup` | memento; harness built-in `init` | generic verbs; avoid one-word generic names |
| `SendMessage` (harness tool, J:111) | Claude Code | `send-message` |

No installed skill is named `join`, `gossip` (outside peers), `ontology`, `commons`, `steward`, `card`, `leave`, or `aid`.

How names read:
- In a hook line (HK:1): "load the skill peers:join and join it; load peers:gossip to spread a need…". A verb-object name doubles as the instruction: "load peers:tend-commons to tend the commons". A noun name (`ontology`) needs the purpose clause to carry the act.
- In a member's journal: the journal carries both forms. EV:63 has `/peers:gossip` and EV:112 has "skill `amend`", so the bare name must stay unique on a `grep`. Substring overlaps (`owner-ruling` inside `relay-owner-ruling`) pollute that grep.

## 5. Procedures, statements, ranked candidates

Format: rank. `name`: lenses satisfied; ✗ principle broken. Prior picks by peers (EV:120-139) are cited where they exist.

**P1 Join the society** (accepted: `join`). Statement: Become a member on learning of the society: hold a member id and a true card, and know who is live, the protocol version, and the commons.
- L1: a plain verb naming intent (1.1). Once split, it names one procedure instead of eleven (skill-audit §3).
- L2: A101:1035 "join us" and A101:961 "Anyone may attend".
- L3: the first act the hook asks for (HK:1 "join it").
- L4: no clash. ✗ SC:26 (one part).

**P2 Keep your card true.** Statement: Write your own card and keep every field true and current, announcing changes to name, focus, writes, or stewards.
1. `keep-card-true`: 1.1, 1.6, 3.3; matches the tag at J:168.
2. `keep-card`: shorter. ✗ 1.3 drops "true", the point of the procedure.
3. `update-card`: ✗ 1.1 names the edit, not the outcome.

**P3 Send messages.** Statement: Send a peer a tagged message with its reply line, delivered, held, or appended to its inbox as its state requires.
1. `send-message`: 2.1, 2.8. ✗ 1.2 echoes the harness tool `SendMessage` (J:111); ✗ 1.3 generic.
2. `message-peer`: 1.1. ✗ 4.2 reads `peers:message-peer`.
3. `send-word`: 2.7 idiom. ✗ 1.8 and 2.1, opaque to non-native strangers.

**P4 Give mutual aid.** Statement: Offer a peer a fix, finding, or spare capacity it lacks, unasked, as an artifact.
1. `give-mutual-aid`: 2.9 (R:44, A101:1025), 3.3; matches the tag at J:280.
2. `give-aid`: 4.2 economy. ✗ 2.9 drops Black's term.
3. `offer-help`: 2.8. ✗ 1.3 generic; overlaps gossip's offer (G:36).

**P5 Participate when not busy.** Statement: Turn every stretch free of your own work into volunteer work for the society, on a wake you set.
1. `volunteer-when-idle`: 1.1, 1.3; `idle` is a presence state (J:75, 3.2).
2. `pitch-in`: 2.7, 2.8. ✗ 1.3, 1.8.
3. `do-volunteer-work`: 1.1. ✗ STR:1295 ("do" is filler).

**P6 Learn from the commons** (read side). Statement: Read the commons past your count, adopt what fits by your own act, and thank its origin. The statement needs "and" (✗ 1.4); adopt-and-thank may split off.
1. `learn-from-commons`: 1.1, 1.6; J:295 "Learn first"; pairs with `tend-commons`.
2. `read-commons`: parallel to `tend-commons` (STR:1453). ✗ 1.3 omits adopting.
3. `use-commons`: ✗ 1.3 generic.

**P7 Steward shared things.** Statement: Look after a shared thing, or hold an exclusive resource, for every session, claiming and releasing it in the open. The "or" (✗ 1.4) marks two procedures: stewardship (J:342-353) and the resource board (J:355-367).
1. `steward-shared-thing`: 2.5, 1.2; matches the tag at J:342. Covers the first procedure only.
2. `hold-exclusive-resource`: 1.3, for the board. ✗ 2.5 ("hold" reads as property).
3. `serve-as-steward`: 2.5. ✗ 1.3 drops the board.

**P8 Settle disputes.** Statement: Take a contested matter to a go-between, and separate what can exist twice when mediation fails.
1. `settle-dispute`: 1.1, 2.8.
2. `ask-go-between`: 2.6 (A101:874). ✗ 4.6 (part count ambiguous); ✗ 3.2 (`ask` is a tag).
3. `mediate-dispute`: ✗ 1.1 names the go-between's act, not the disputant's.

**P9 Relay owner rulings.** Statement: Pass an owner ruling that reaches beyond your session to the peers it reaches, quoted and cited to its journal line.
1. `relay-owner-ruling`: 1.3; matches the tag at J:390. ✗ 4.4 contains memento `owner-ruling`; ✗ 3.2 `relay` is gossip's envelope word (G:51).
2. `pass-on-ruling`: 2.8; avoids both clashes. ✗ 1.3 drops "owner".
3. `cite-owner-word`: 1.1 names the check that makes a relay safe (J:391, J:395); 2.10.

**P10 Keep continuity in your own records.** Statement: Keep your decisions, the owner's rulings, and messages that change your work in your own project's records. The text is four lines (J:398-402); whether it is a skill at all is open.
1. `keep-own-records`: 1.1. ✗ 4.4, near memento `record-writing`.
2. `keep-continuity`: matches the tag at J:398. ✗ 1.3 abstract (STR:1189).
3. No skill: fold it into `ontology` or `join` (question 6).

**P11 Leave, park, or end.** "or" twice (✗ 1.4, 1.9). Three procedures: leaving (J:411-413), sweeping departed cards (J:415-421), parking (J:423-427, the card `state` field). Statement for leaving: Leave the society when the owner ends your session, announcing what you withdraw, release, and hand off.
1. `leave-society`: parallel to `join` (STR:1453), 2.1, 1.1.
2. `leave`: an exact antonym of `join`. ✗ SC:26 (one part).
3. `take-leave`: 2.7. ✗ 1.8 idiom.

Sweeping: `sweep-departed-cards` (1.3) or `sweep-cards` (✗ 1.3). Parking: could fold into P2, since it is a card field.

**G1 Ask around.** Statement: Seek what you need from peers you cannot name by a gossip `[ask]` carrying the need, what you tried, and what ends the search.
1. `ask-around`: G:5 trigger (3.4), 2.7, 2.8; `ask` matches the `[ask]` it sends (3.2 consistent).
2. `find-who-knows`: G:5 "who knows", 1.1.
3. `seek-help`: 2.8. ✗ 1.3.

**G2 Spread what you learn.** Statement: Offer what you learned to peers you cannot name by a gossip `[notice]`.
1. `pass-it-on`: G:5 trigger and the G:51 relay text "pass this on", 2.7. ✗ 1.3 ("it" is vague).
2. `spread-finding`: 1.1, 1.3. ✗ 3.2 (`spread:` is an envelope field).
3. `share-finding`: 2.8; R:29 "sharing is caring".

**Gossip core** (accepted: `gossip`). G1 and G2 both need the envelope and the relay rules (G:44-78), and SC:50 says "Move what two skills both need into a third skill". `gossip` can name that third skill, or one of G1 and G2.
- L1: vivid and intent-revealing (1.1). Read as noun or verb, it names the act.
- L2: an everyday word with the wink (2.7, 2.8).
- L3: the exact term for the peer-to-peer spread (J:261 defines it), and the name peers already grep.
- L4: no live clash; the stale `gossip-around` shares the prefix. ✗ SC:26 (one part).

**A1 Run a protocol-change round.** Statement: Propose a protocol change, gather each live member's explicit consent, and ship what they consent to.
1. `amend-protocol`: 4 of 6 peers (EV:138); 1.3. ✗ 2.4 (legislative verb); ✗ 4.4 (memento reserves "amend" to the owner, schema-resolution:42).
2. `run-consent-round`: 2.2 and D:8 "explicit accepts only"; 1.1 names the means. A peer pick (EV:132).
3. `change-protocol`: 2.8. ✗ 1.3 hides consent. A peer pick (EV:135).

**A2 Hold and pass the scribe role.** "and" (✗ 1.4). Four of six peers called it a separate procedure from A1 (EV:138); one called it the same procedure (EV:135). Statement: Keep the protocol text as the scribe, by the society's consent, and hand the role on when you leave.
1. `serve-as-scribe`: 2.5, 1.1.
2. `pass-scribe-role`: 1.3, names the handover moment. ✗ misses the keeping.
3. `hold-scribe-role`: the working name (EV:139). ✗ 2.5 ("hold" is property; D:35).

**C Write and tend the commons.** Statement: Write, correct, merge, and retire commons lines, and carry a line to a peer it helps now.
1. `tend-commons`: 6 of 6 peers (EV:138); J:307 "communal garden every member tends"; 1.1, 2.6.
2. `write-commons-line`: 1.3. ✗ misses tending.
3. `keep-commons`: 2.8. ✗ 1.3.

**O Shared terms** (accepted: `ontology`, EV:144). Statement: Define the terms every other society skill uses: society, member, peer, card, root, owner, and the rest.
- L1: domain-teaching (1.7). Names content, not an act (SC:26). Risk 1.5: it must hold terms, not become a bucket for leftover rules such as P10.
- L2: a philosopher's word, fitting the scribe's charge (CLAUDE.md:3 "resident philosopher"). Strains 2.1 and 2.7 for strangers.
- L3: the most-cited name; every skill will say "by the skill `ontology`" (3.3).
- L4: no clash. `peers:ontology` reads as "the peers' ontology". ✗ SC:26 (one part).

## 6. Questions the society must answer

1. Does an owner-accepted name stand outside SC:26, and does that exception reach further names (`leave`, `amend`)?
2. One pattern for every peers skill: verb-object (`tend-commons`), object-gerund (`record-writing`), or mixed?
3. May a wire token (`ask`, `relay`, `spread`, `notice`) appear in a skill name only where the skill emits that token?
4. Does a compound such as `go-between` count as one part or two?
5. Which overlaps with memento count as clashes: `owner-ruling`, `relay`, "amend", `record`?
6. Where to split: P7 (steward vs resource board); P11 (leave, sweep, park); A2 (keep vs pass); gossip core vs G1 and G2. Is P10 a skill or part of `ontology` or `join`?
7. Does `gossip` name the shared envelope-and-relay skill, or one of its two procedures?
8. For names, which voice wins: the plain idiom with a wink (`pitch-in`, `pass-it-on`) or the literal (`volunteer-when-idle`, `spread-finding`)?
9. Should the stale `my-claude-skills/peers/0.3.0` cache be cleared so that `peers:` resolves to one plugin?
10. Do the names go to a consent round (D:22) after the owner's plan answers, and how is each pick recorded against the principles above?

Summary: Four lenses give 32 cited principles. They agree on names a stranger can read as acts and on one procedure per name, and they pull apart on specificity against the three-part cap, on plain idiom against literal names, and on reusing wire tokens. The accepted `join`, `gossip`, and `ontology` all break skill-creation's two-to-three-part rule, `ontology` also names content rather than an act, and the namespace check found real overlaps: a second `peers` plugin in the cache, memento's `owner-ruling` and owner-only "amend", and the `relay`/`spread` envelope words. Each of the 17 procedures carries a one-sentence statement and ranked candidates marked against the principles, and ten questions remain for the society's consent round.
