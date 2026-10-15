# Self-audit: protocol 10 peers skills against skill-creation (rewrite-instructions (d))
Method. Mechanical checks ran on every line by `/tmp/aoa-tools/check.py` (tag placement, tag names, one emphatic word outside backticks, a `; never` half on every sentence, prose only, no path reference) and by the edge script (references against the graph). The writer read every sentence of every skill against the rules that need judgment (one procedure, order, one instruction per sentence, command form, same-concern pairing, no argument, no narrated failure, one term per concept, definitions, ordinary words, only instructing sentences). Read-through fixes are in commit 2 on the branch; the tables below are the state at the branch head.
Emphatic count: `grep -nwE 'never|always|only|must'` per skill, with backticked text removed, gives exactly one hit on every body sentence and none in any frontmatter; no line carries two.

## adopt (44 lines)

| # | rule (SC) | result |
|---|---|---|
| 1 | Name the one procedure in a sentence before writing | PASS — procedure: "Bring what a peer built into your own work by your own act, thanking its origin." |
| 2 | Cover one procedure per skill | PASS — one procedure; every tag is a step of it |
| 3 | Reading the skill does the work | PASS — instructions to a reading model; no script runs it |
| 4 | File named `SKILL.md` | PASS |
| 5 | YAML frontmatter with `name` and `description` | PASS — `name` and `description` present |
| 6 | No version field in frontmatter | PASS — no `version` key |
| 7 | `name` from the procedure (part count void, Ev:149; name from RO:5-30) | PASS — `adopt` is the roster name |
| 8 | Directory name = `name` | PASS — `skills/adopt/` = `adopt` |
| 9 | Description: one sentence, then phrases and conditions | PASS — line 4 is one sentence ending at its period; line 5 lists 5 quoted phrases plus conditions |
| 10 | Every trigger phrase in the description, none in the body | PASS — the body holds no request phrase; conditions in the body select among this skill's own steps (tension 12) |
| 11 | Body structured in XML tags | PASS — 6 tags, no Markdown structure |
| 12 | Each tag named as an imperative verb phrase | PASS — `read-the-terms`, `read-what-peers-built`, `check-before-you-adopt`, `adopt-by-your-own-act`, `thank-the-origin`, `correct-what-fails` |
| 13 | Every instruction inside a tag | PASS — 13 sentences, each inside a tag |
| 14 | No tag attributes | PASS — no tag carries an attribute |
| 15 | Inside a tag: prose and inline backticks only | PASS — no list, table, heading, or code block inside a tag |
| 16 | Body ordered as the procedure runs | PASS — tags follow the order the procedure runs |
| 17 | Everything needed inside, outside only by naming a skill | PASS — outside text reached only by naming a skill or a protocol location (tension 2) |
| 18 | Shared content moved to a third skill, not copied | PASS — shared terms live in `ontology`; no definition copied |
| 19 | Other skills referenced by name, not path | PASS — references are "the skill `<name>`"; no path |
| 20 | One instruction per sentence | PASS — each sentence holds one instruction |
| 21 | Every instruction a command | PASS — imperative mood throughout; no "should" or "may" for a duty |
| 22 | At most one emphatic word per sentence | PASS — 13 of 13 sentences carry exactly one emphatic word outside backticks |
| 23 | Emphatic words counted where they command | PASS — emphatic words inside backticks not counted |
| 24 | Each positive instruction paired with its own prohibition | PASS — every `never` half negates the same instruction its positive half gives |
| 25 | State the instruction, never argue | PASS — no sentence argues for its rule |
| 26 | Name what is required, never narrate a failure | PASS — no failure narrated |
| 27 | One term per concept | PASS — one term per concept (type, item, wake, origin checked across skills) |
| 28 | Terms defined at first use (shared terms in ontology, tension 3) | PASS — every society term from `ontology`; terms one skill uses defined in place |
| 29 | Ordinary words | PASS — ordinary words |
| 30 | Only sentences that instruct or forbid | PASS — every sentence instructs or forbids |
| 31 | Final read against every rule | PASS — read against rules 1-30 at the branch head |

## aid (20 lines)

| # | rule (SC) | result |
|---|---|---|
| 1 | Name the one procedure in a sentence before writing | PASS — procedure: "Offer a peer a fix, finding, or capacity it lacks, unasked." |
| 2 | Cover one procedure per skill | PASS — one procedure; every tag is a step of it |
| 3 | Reading the skill does the work | PASS — instructions to a reading model; no script runs it |
| 4 | File named `SKILL.md` | PASS |
| 5 | YAML frontmatter with `name` and `description` | PASS — `name` and `description` present |
| 6 | No version field in frontmatter | PASS — no `version` key |
| 7 | `name` from the procedure (part count void, Ev:149; name from RO:5-30) | PASS — `aid` is the roster name |
| 8 | Directory name = `name` | PASS — `skills/aid/` = `aid` |
| 9 | Description: one sentence, then phrases and conditions | PASS — line 4 is one sentence ending at its period; line 5 lists 4 quoted phrases plus conditions |
| 10 | Every trigger phrase in the description, none in the body | PASS — the body holds no request phrase; conditions in the body select among this skill's own steps (tension 12) |
| 11 | Body structured in XML tags | PASS — 2 tags, no Markdown structure |
| 12 | Each tag named as an imperative verb phrase | PASS — `read-the-terms`, `offer-unasked` |
| 13 | Every instruction inside a tag | PASS — 5 sentences, each inside a tag |
| 14 | No tag attributes | PASS — no tag carries an attribute |
| 15 | Inside a tag: prose and inline backticks only | PASS — no list, table, heading, or code block inside a tag |
| 16 | Body ordered as the procedure runs | PASS — tags follow the order the procedure runs |
| 17 | Everything needed inside, outside only by naming a skill | PASS — outside text reached only by naming a skill or a protocol location (tension 2) |
| 18 | Shared content moved to a third skill, not copied | PASS — shared terms live in `ontology`; no definition copied |
| 19 | Other skills referenced by name, not path | PASS — references are "the skill `<name>`"; no path |
| 20 | One instruction per sentence | PASS — each sentence holds one instruction |
| 21 | Every instruction a command | PASS — imperative mood throughout; no "should" or "may" for a duty |
| 22 | At most one emphatic word per sentence | PASS — 5 of 5 sentences carry exactly one emphatic word outside backticks |
| 23 | Emphatic words counted where they command | PASS — emphatic words inside backticks not counted |
| 24 | Each positive instruction paired with its own prohibition | PASS — every `never` half negates the same instruction its positive half gives |
| 25 | State the instruction, never argue | PASS — no sentence argues for its rule |
| 26 | Name what is required, never narrate a failure | PASS — no failure narrated |
| 27 | One term per concept | PASS — one term per concept (type, item, wake, origin checked across skills) |
| 28 | Terms defined at first use (shared terms in ontology, tension 3) | PASS — every society term from `ontology`; terms one skill uses defined in place |
| 29 | Ordinary words | PASS — ordinary words |
| 30 | Only sentences that instruct or forbid | PASS — every sentence instructs or forbids |
| 31 | Final read against every rule | PASS — read against rules 1-30 at the branch head |

## ask-around (30 lines)

| # | rule (SC) | result |
|---|---|---|
| 1 | Name the one procedure in a sentence before writing | PASS — procedure: "Seek what you need from peers you cannot name, by gossip." |
| 2 | Cover one procedure per skill | PASS — one procedure; every tag is a step of it |
| 3 | Reading the skill does the work | PASS — instructions to a reading model; no script runs it |
| 4 | File named `SKILL.md` | PASS |
| 5 | YAML frontmatter with `name` and `description` | PASS — `name` and `description` present |
| 6 | No version field in frontmatter | PASS — no `version` key |
| 7 | `name` from the procedure (part count void, Ev:149; name from RO:5-30) | PASS — `ask-around` is the roster name |
| 8 | Directory name = `name` | PASS — `skills/ask-around/` = `ask-around` |
| 9 | Description: one sentence, then phrases and conditions | PASS — line 4 is one sentence ending at its period; line 5 lists 4 quoted phrases plus conditions |
| 10 | Every trigger phrase in the description, none in the body | PASS — the body holds no request phrase; conditions in the body select among this skill's own steps (tension 12) |
| 11 | Body structured in XML tags | PASS — 5 tags, no Markdown structure |
| 12 | Each tag named as an imperative verb phrase | PASS — `read-the-terms`, `spend-your-own-effort-first`, `ask-whom-you-can-name`, `ask-around-for-the-rest`, `close-the-search` |
| 13 | Every instruction inside a tag | PASS — 7 sentences, each inside a tag |
| 14 | No tag attributes | PASS — no tag carries an attribute |
| 15 | Inside a tag: prose and inline backticks only | PASS — no list, table, heading, or code block inside a tag |
| 16 | Body ordered as the procedure runs | PASS — tags follow the order the procedure runs |
| 17 | Everything needed inside, outside only by naming a skill | PASS — outside text reached only by naming a skill or a protocol location (tension 2) |
| 18 | Shared content moved to a third skill, not copied | PASS — shared terms live in `ontology`; no definition copied |
| 19 | Other skills referenced by name, not path | PASS — references are "the skill `<name>`"; no path |
| 20 | One instruction per sentence | PASS — each sentence holds one instruction |
| 21 | Every instruction a command | PASS — imperative mood throughout; no "should" or "may" for a duty |
| 22 | At most one emphatic word per sentence | PASS — 7 of 7 sentences carry exactly one emphatic word outside backticks |
| 23 | Emphatic words counted where they command | PASS — emphatic words inside backticks not counted |
| 24 | Each positive instruction paired with its own prohibition | PASS — every `never` half negates the same instruction its positive half gives |
| 25 | State the instruction, never argue | PASS — no sentence argues for its rule |
| 26 | Name what is required, never narrate a failure | PASS — no failure narrated |
| 27 | One term per concept | PASS — one term per concept (type, item, wake, origin checked across skills) |
| 28 | Terms defined at first use (shared terms in ontology, tension 3) | PASS — every society term from `ontology`; terms one skill uses defined in place |
| 29 | Ordinary words | PASS — ordinary words |
| 30 | Only sentences that instruct or forbid | PASS — every sentence instructs or forbids |
| 31 | Final read against every rule | PASS — read against rules 1-30 at the branch head |

## card (90 lines)

| # | rule (SC) | result |
|---|---|---|
| 1 | Name the one procedure in a sentence before writing | PASS — procedure: "Keep your own card true and current." |
| 2 | Cover one procedure per skill | PASS — one procedure; every tag is a step of it |
| 3 | Reading the skill does the work | PASS — instructions to a reading model; no script runs it |
| 4 | File named `SKILL.md` | PASS |
| 5 | YAML frontmatter with `name` and `description` | PASS — `name` and `description` present |
| 6 | No version field in frontmatter | PASS — no `version` key |
| 7 | `name` from the procedure (part count void, Ev:149; name from RO:5-30) | PASS — `card` is the roster name |
| 8 | Directory name = `name` | PASS — `skills/card/` = `card` |
| 9 | Description: one sentence, then phrases and conditions | PASS — line 4 is one sentence ending at its period; line 5 lists 6 quoted phrases plus conditions |
| 10 | Every trigger phrase in the description, none in the body | PASS — the body holds no request phrase; conditions in the body select among this skill's own steps (tension 12) |
| 11 | Body structured in XML tags | PASS — 6 tags, no Markdown structure |
| 12 | Each tag named as an imperative verb phrase | PASS — `read-the-terms`, `write-your-own-card`, `read-your-facts-afresh`, `carry-the-fields`, `announce-each-change`, `mark-your-parking` |
| 13 | Every instruction inside a tag | PASS — 36 sentences, each inside a tag |
| 14 | No tag attributes | PASS — no tag carries an attribute |
| 15 | Inside a tag: prose and inline backticks only | PASS — no list, table, heading, or code block inside a tag |
| 16 | Body ordered as the procedure runs | PASS — tags follow the order the procedure runs |
| 17 | Everything needed inside, outside only by naming a skill | PASS — outside text reached only by naming a skill or a protocol location (tension 2) |
| 18 | Shared content moved to a third skill, not copied | PASS — shared terms live in `ontology`; no definition copied |
| 19 | Other skills referenced by name, not path | PASS — references are "the skill `<name>`"; no path |
| 20 | One instruction per sentence | PASS — each sentence holds one instruction |
| 21 | Every instruction a command | PASS — imperative mood throughout; no "should" or "may" for a duty |
| 22 | At most one emphatic word per sentence | PASS — 36 of 36 sentences carry exactly one emphatic word outside backticks |
| 23 | Emphatic words counted where they command | PASS — emphatic words inside backticks not counted |
| 24 | Each positive instruction paired with its own prohibition | PASS — every `never` half negates the same instruction its positive half gives |
| 25 | State the instruction, never argue | PASS — no sentence argues for its rule |
| 26 | Name what is required, never narrate a failure | PASS — no failure narrated |
| 27 | One term per concept | PASS — one term per concept (type, item, wake, origin checked across skills) |
| 28 | Terms defined at first use (shared terms in ontology, tension 3) | PASS — every society term from `ontology`; terms one skill uses defined in place |
| 29 | Ordinary words | PASS — ordinary words |
| 30 | Only sentences that instruct or forbid | PASS — every sentence instructs or forbids |
| 31 | Final read against every rule | PASS — read against rules 1-30 at the branch head |

## consent (24 lines)

| # | rule (SC) | result |
|---|---|---|
| 1 | Name the one procedure in a sentence before writing | PASS — procedure: "Answer a protocol draft with your acceptance or your objection." |
| 2 | Cover one procedure per skill | PASS — one procedure; every tag is a step of it |
| 3 | Reading the skill does the work | PASS — instructions to a reading model; no script runs it |
| 4 | File named `SKILL.md` | PASS |
| 5 | YAML frontmatter with `name` and `description` | PASS — `name` and `description` present |
| 6 | No version field in frontmatter | PASS — no `version` key |
| 7 | `name` from the procedure (part count void, Ev:149; name from RO:5-30) | PASS — `consent` is the roster name |
| 8 | Directory name = `name` | PASS — `skills/consent/` = `consent` |
| 9 | Description: one sentence, then phrases and conditions | PASS — line 4 is one sentence ending at its period; line 5 lists 3 quoted phrases plus conditions |
| 10 | Every trigger phrase in the description, none in the body | PASS — the body holds no request phrase; conditions in the body select among this skill's own steps (tension 12) |
| 11 | Body structured in XML tags | PASS — 4 tags, no Markdown structure |
| 12 | Each tag named as an imperative verb phrase | PASS — `read-the-terms`, `time-your-answer`, `check-the-draft`, `answer-the-draft` |
| 13 | Every instruction inside a tag | PASS — 5 sentences, each inside a tag |
| 14 | No tag attributes | PASS — no tag carries an attribute |
| 15 | Inside a tag: prose and inline backticks only | PASS — no list, table, heading, or code block inside a tag |
| 16 | Body ordered as the procedure runs | PASS — tags follow the order the procedure runs |
| 17 | Everything needed inside, outside only by naming a skill | PASS — outside text reached only by naming a skill or a protocol location (tension 2) |
| 18 | Shared content moved to a third skill, not copied | PASS — shared terms live in `ontology`; no definition copied |
| 19 | Other skills referenced by name, not path | PASS — references are "the skill `<name>`"; no path |
| 20 | One instruction per sentence | PASS — each sentence holds one instruction |
| 21 | Every instruction a command | PASS — imperative mood throughout; no "should" or "may" for a duty |
| 22 | At most one emphatic word per sentence | PASS — 5 of 5 sentences carry exactly one emphatic word outside backticks |
| 23 | Emphatic words counted where they command | PASS — emphatic words inside backticks not counted |
| 24 | Each positive instruction paired with its own prohibition | PASS — every `never` half negates the same instruction its positive half gives |
| 25 | State the instruction, never argue | PASS — no sentence argues for its rule |
| 26 | Name what is required, never narrate a failure | PASS — no failure narrated |
| 27 | One term per concept | PASS — one term per concept (type, item, wake, origin checked across skills) |
| 28 | Terms defined at first use (shared terms in ontology, tension 3) | PASS — every society term from `ontology`; terms one skill uses defined in place |
| 29 | Ordinary words | PASS — ordinary words |
| 30 | Only sentences that instruct or forbid | PASS — every sentence instructs or forbids |
| 31 | Final read against every rule | PASS — read against rules 1-30 at the branch head |

## gossip (62 lines)

| # | rule (SC) | result |
|---|---|---|
| 1 | Name the one procedure in a sentence before writing | PASS — procedure: "Pass a message from peer to peer past anyone its origin could name, inside the envelope." |
| 2 | Cover one procedure per skill | PASS — one procedure; every tag is a step of it |
| 3 | Reading the skill does the work | PASS — instructions to a reading model; no script runs it |
| 4 | File named `SKILL.md` | PASS |
| 5 | YAML frontmatter with `name` and `description` | PASS — `name` and `description` present |
| 6 | No version field in frontmatter | PASS — no `version` key |
| 7 | `name` from the procedure (part count void, Ev:149; name from RO:5-30) | PASS — `gossip` is the roster name |
| 8 | Directory name = `name` | PASS — `skills/gossip/` = `gossip` |
| 9 | Description: one sentence, then phrases and conditions | PASS — line 4 is one sentence ending at its period; line 5 lists 3 quoted phrases plus conditions |
| 10 | Every trigger phrase in the description, none in the body | PASS — the body holds no request phrase; conditions in the body select among this skill's own steps (tension 12) |
| 11 | Body structured in XML tags | PASS — 5 tags, no Markdown structure |
| 12 | Each tag named as an imperative verb phrase | PASS — `read-the-terms`, `gossip-what-you-cannot-target`, `build-the-envelope`, `relay-as-the-spread-says`, `reach-the-origin` |
| 13 | Every instruction inside a tag | PASS — 23 sentences, each inside a tag |
| 14 | No tag attributes | PASS — no tag carries an attribute |
| 15 | Inside a tag: prose and inline backticks only | PASS — no list, table, heading, or code block inside a tag |
| 16 | Body ordered as the procedure runs | PASS — tags follow the order the procedure runs |
| 17 | Everything needed inside, outside only by naming a skill | PASS — outside text reached only by naming a skill or a protocol location (tension 2) |
| 18 | Shared content moved to a third skill, not copied | PASS — shared terms live in `ontology`; no definition copied |
| 19 | Other skills referenced by name, not path | PASS — references are "the skill `<name>`"; no path |
| 20 | One instruction per sentence | PASS — each sentence holds one instruction |
| 21 | Every instruction a command | PASS — imperative mood throughout; no "should" or "may" for a duty |
| 22 | At most one emphatic word per sentence | PASS — 23 of 23 sentences carry exactly one emphatic word outside backticks |
| 23 | Emphatic words counted where they command | PASS — emphatic words inside backticks not counted |
| 24 | Each positive instruction paired with its own prohibition | PASS — every `never` half negates the same instruction its positive half gives |
| 25 | State the instruction, never argue | PASS — no sentence argues for its rule |
| 26 | Name what is required, never narrate a failure | PASS — no failure narrated |
| 27 | One term per concept | PASS — one term per concept (type, item, wake, origin checked across skills) |
| 28 | Terms defined at first use (shared terms in ontology, tension 3) | PASS — every society term from `ontology`; terms one skill uses defined in place |
| 29 | Ordinary words | PASS — ordinary words |
| 30 | Only sentences that instruct or forbid | PASS — every sentence instructs or forbids |
| 31 | Final read against every rule | PASS — read against rules 1-30 at the branch head |

## heartbeat (44 lines)

| # | rule (SC) | result |
|---|---|---|
| 1 | Name the one procedure in a sentence before writing | PASS — procedure: "Keep a recurring wake set across restarts." |
| 2 | Cover one procedure per skill | PASS — one procedure; every tag is a step of it |
| 3 | Reading the skill does the work | PASS — instructions to a reading model; no script runs it |
| 4 | File named `SKILL.md` | PASS |
| 5 | YAML frontmatter with `name` and `description` | PASS — `name` and `description` present |
| 6 | No version field in frontmatter | PASS — no `version` key |
| 7 | `name` from the procedure (part count void, Ev:149; name from RO:5-30) | PASS — `heartbeat` is the roster name |
| 8 | Directory name = `name` | PASS — `skills/heartbeat/` = `heartbeat` |
| 9 | Description: one sentence, then phrases and conditions | PASS — line 4 is one sentence ending at its period; line 5 lists 5 quoted phrases plus conditions |
| 10 | Every trigger phrase in the description, none in the body | PASS — the body holds no request phrase; conditions in the body select among this skill's own steps (tension 12) |
| 11 | Body structured in XML tags | PASS — 6 tags, no Markdown structure |
| 12 | Each tag named as an imperative verb phrase | PASS — `read-the-terms`, `choose-the-wake`, `set-the-wake`, `restore-the-wake`, `spend-the-wake`, `end-the-wake` |
| 13 | Every instruction inside a tag | PASS — 13 sentences, each inside a tag |
| 14 | No tag attributes | PASS — no tag carries an attribute |
| 15 | Inside a tag: prose and inline backticks only | PASS — no list, table, heading, or code block inside a tag |
| 16 | Body ordered as the procedure runs | PASS — tags follow the order the procedure runs |
| 17 | Everything needed inside, outside only by naming a skill | PASS — names Claude Code as the harness case (DM:34); no Claude Code term of the test list in the body |
| 18 | Shared content moved to a third skill, not copied | PASS — shared terms live in `ontology`; no definition copied |
| 19 | Other skills referenced by name, not path | PASS — references are "the skill `<name>`"; no path |
| 20 | One instruction per sentence | PASS — each sentence holds one instruction |
| 21 | Every instruction a command | PASS — imperative mood throughout; no "should" or "may" for a duty |
| 22 | At most one emphatic word per sentence | PASS — 13 of 13 sentences carry exactly one emphatic word outside backticks |
| 23 | Emphatic words counted where they command | PASS — emphatic words inside backticks not counted |
| 24 | Each positive instruction paired with its own prohibition | PASS — every `never` half negates the same instruction its positive half gives |
| 25 | State the instruction, never argue | PASS — no sentence argues for its rule |
| 26 | Name what is required, never narrate a failure | PASS — no failure narrated |
| 27 | One term per concept | PASS — one term per concept (type, item, wake, origin checked across skills) |
| 28 | Terms defined at first use (shared terms in ontology, tension 3) | PASS — every society term from `ontology`; terms one skill uses defined in place |
| 29 | Ordinary words | PASS — ordinary words |
| 30 | Only sentences that instruct or forbid | PASS — every sentence instructs or forbids |
| 31 | Final read against every rule | PASS — read against rules 1-30 at the branch head |

## join (70 lines)

| # | rule (SC) | result |
|---|---|---|
| 1 | Name the one procedure in a sentence before writing | PASS — procedure: "Become a member of the society on learning of it." |
| 2 | Cover one procedure per skill | PASS — one procedure; every tag is a step of it |
| 3 | Reading the skill does the work | PASS — instructions to a reading model; no script runs it |
| 4 | File named `SKILL.md` | PASS |
| 5 | YAML frontmatter with `name` and `description` | PASS — `name` and `description` present |
| 6 | No version field in frontmatter | PASS — no `version` key |
| 7 | `name` from the procedure (part count void, Ev:149; name from RO:5-30) | PASS — `join` is the roster name |
| 8 | Directory name = `name` | PASS — `skills/join/` = `join` |
| 9 | Description: one sentence, then phrases and conditions | PASS — line 4 is one sentence ending at its period; line 5 lists 3 quoted phrases plus conditions |
| 10 | Every trigger phrase in the description, none in the body | PASS — the body holds no request phrase; conditions in the body select among this skill's own steps (tension 12) |
| 11 | Body structured in XML tags | PASS — 7 tags, no Markdown structure |
| 12 | Each tag named as an imperative verb phrase | PASS — `read-the-terms`, `join-on-learning`, `find-your-member-id`, `set-your-card`, `see-who-is-live`, `take-back-what-you-held`, `catch-up` |
| 13 | Every instruction inside a tag | PASS — 25 sentences, each inside a tag |
| 14 | No tag attributes | PASS — no tag carries an attribute |
| 15 | Inside a tag: prose and inline backticks only | PASS — no list, table, heading, or code block inside a tag |
| 16 | Body ordered as the procedure runs | PASS — tags follow the order the procedure runs |
| 17 | Everything needed inside, outside only by naming a skill | PASS — outside text reached only by naming a skill or a protocol location (tension 2) |
| 18 | Shared content moved to a third skill, not copied | PASS — shared terms live in `ontology`; no definition copied |
| 19 | Other skills referenced by name, not path | PASS — references are "the skill `<name>`"; no path |
| 20 | One instruction per sentence | PASS — each sentence holds one instruction |
| 21 | Every instruction a command | PASS — imperative mood throughout; no "should" or "may" for a duty |
| 22 | At most one emphatic word per sentence | PASS — 25 of 25 sentences carry exactly one emphatic word outside backticks |
| 23 | Emphatic words counted where they command | PASS — emphatic words inside backticks not counted |
| 24 | Each positive instruction paired with its own prohibition | PASS — every `never` half negates the same instruction its positive half gives |
| 25 | State the instruction, never argue | PASS — no sentence argues for its rule |
| 26 | Name what is required, never narrate a failure | PASS — no failure narrated |
| 27 | One term per concept | PASS — one term per concept (type, item, wake, origin checked across skills) |
| 28 | Terms defined at first use (shared terms in ontology, tension 3) | PASS — every society term from `ontology`; terms one skill uses defined in place |
| 29 | Ordinary words | PASS — ordinary words |
| 30 | Only sentences that instruct or forbid | PASS — every sentence instructs or forbids |
| 31 | Final read against every rule | PASS — read against rules 1-30 at the branch head |

## leave (30 lines)

| # | rule (SC) | result |
|---|---|---|
| 1 | Name the one procedure in a sentence before writing | PASS — procedure: "Leave the society when the owner ends your session." |
| 2 | Cover one procedure per skill | PASS — one procedure; every tag is a step of it |
| 3 | Reading the skill does the work | PASS — instructions to a reading model; no script runs it |
| 4 | File named `SKILL.md` | PASS |
| 5 | YAML frontmatter with `name` and `description` | PASS — `name` and `description` present |
| 6 | No version field in frontmatter | PASS — no `version` key |
| 7 | `name` from the procedure (part count void, Ev:149; name from RO:5-30) | PASS — `leave` is the roster name |
| 8 | Directory name = `name` | PASS — `skills/leave/` = `leave` |
| 9 | Description: one sentence, then phrases and conditions | PASS — line 4 is one sentence ending at its period; line 5 lists 5 quoted phrases plus conditions |
| 10 | Every trigger phrase in the description, none in the body | PASS — the body holds no request phrase; conditions in the body select among this skill's own steps (tension 12) |
| 11 | Body structured in XML tags | PASS — 4 tags, no Markdown structure |
| 12 | Each tag named as an imperative verb phrase | PASS — `read-the-terms`, `announce-the-leaving`, `release-what-you-hold`, `move-your-card` |
| 13 | Every instruction inside a tag | PASS — 8 sentences, each inside a tag |
| 14 | No tag attributes | PASS — no tag carries an attribute |
| 15 | Inside a tag: prose and inline backticks only | PASS — no list, table, heading, or code block inside a tag |
| 16 | Body ordered as the procedure runs | PASS — tags follow the order the procedure runs |
| 17 | Everything needed inside, outside only by naming a skill | PASS — outside text reached only by naming a skill or a protocol location (tension 2) |
| 18 | Shared content moved to a third skill, not copied | PASS — shared terms live in `ontology`; no definition copied |
| 19 | Other skills referenced by name, not path | PASS — references are "the skill `<name>`"; no path |
| 20 | One instruction per sentence | PASS — each sentence holds one instruction |
| 21 | Every instruction a command | PASS — imperative mood throughout; no "should" or "may" for a duty |
| 22 | At most one emphatic word per sentence | PASS — 8 of 8 sentences carry exactly one emphatic word outside backticks |
| 23 | Emphatic words counted where they command | PASS — emphatic words inside backticks not counted |
| 24 | Each positive instruction paired with its own prohibition | PASS — every `never` half negates the same instruction its positive half gives |
| 25 | State the instruction, never argue | PASS — no sentence argues for its rule |
| 26 | Name what is required, never narrate a failure | PASS — no failure narrated |
| 27 | One term per concept | PASS — one term per concept (type, item, wake, origin checked across skills) |
| 28 | Terms defined at first use (shared terms in ontology, tension 3) | PASS — every society term from `ontology`; terms one skill uses defined in place |
| 29 | Ordinary words | PASS — ordinary words |
| 30 | Only sentences that instruct or forbid | PASS — every sentence instructs or forbids |
| 31 | Final read against every rule | PASS — read against rules 1-30 at the branch head |

## ontology (170 lines)

| # | rule (SC) | result |
|---|---|---|
| 1 | Name the one procedure in a sentence before writing | PASS — procedure: read the terms as defined (writing-stack tension 11); every body sentence has the form `Call <x> …; never …`, or a Claude Code mapping sentence of that form |
| 2 | Cover one procedure per skill | PASS — one procedure; every tag is a step of it |
| 3 | Reading the skill does the work | PASS — instructions to a reading model; no script runs it |
| 4 | File named `SKILL.md` | PASS |
| 5 | YAML frontmatter with `name` and `description` | PASS — `name` and `description` present |
| 6 | No version field in frontmatter | PASS — no `version` key |
| 7 | `name` from the procedure (part count void, Ev:149; name from RO:5-30) | PASS — `ontology` is the roster name |
| 8 | Directory name = `name` | PASS — `skills/ontology/` = `ontology` |
| 9 | Description: one sentence, then phrases and conditions | PASS — line 4 is one sentence ending at its period; line 5 lists 4 quoted phrases plus conditions |
| 10 | Every trigger phrase in the description, none in the body | PASS — the body holds no request phrase; conditions in the body select among this skill's own steps (tension 12) |
| 11 | Body structured in XML tags | PASS — 11 tags, no Markdown structure |
| 12 | Each tag named as an imperative verb phrase | PASS — `read-the-terms-as-defined`, `name-the-sessions`, `name-the-members`, `name-the-owner`, `name-the-places`, `name-the-messages`, `rank-the-messages`, `name-the-knowledge-flows`, `name-the-roles`, `name-the-skills`, `map-the-seams-to-claude-code` |
| 13 | Every instruction inside a tag | PASS — 71 sentences, each inside a tag |
| 14 | No tag attributes | PASS — no tag carries an attribute |
| 15 | Inside a tag: prose and inline backticks only | PASS — no list, table, heading, or code block inside a tag |
| 16 | Body ordered as the procedure runs | PASS — tags follow the order the procedure runs |
| 17 | Everything needed inside, outside only by naming a skill | PASS — outside text reached only by naming a skill or a protocol location (tension 2) |
| 18 | Shared content moved to a third skill, not copied | PASS — shared terms live in `ontology`; no definition copied |
| 19 | Other skills referenced by name, not path | PASS — references are "the skill `<name>`"; no path |
| 20 | One instruction per sentence | PASS — each sentence holds one instruction |
| 21 | Every instruction a command | PASS — imperative mood throughout; no "should" or "may" for a duty |
| 22 | At most one emphatic word per sentence | PASS — 71 of 71 sentences carry exactly one emphatic word outside backticks |
| 23 | Emphatic words counted where they command | PASS — emphatic words inside backticks not counted |
| 24 | Each positive instruction paired with its own prohibition | PASS — every `never` half negates the same instruction its positive half gives |
| 25 | State the instruction, never argue | PASS — no sentence argues for its rule |
| 26 | Name what is required, never narrate a failure | PASS — no failure narrated |
| 27 | One term per concept | PASS — one term per concept (type, item, wake, origin checked across skills) |
| 28 | Terms defined at first use (shared terms in ontology, tension 3) | PASS — ontology is where shared terms are defined (writing-stack tension 3) |
| 29 | Ordinary words | PASS — ordinary words |
| 30 | Only sentences that instruct or forbid | PASS — every sentence instructs or forbids |
| 31 | Final read against every rule | PASS — read against rules 1-30 at the branch head |

## propose (30 lines)

| # | rule (SC) | result |
|---|---|---|
| 1 | Name the one procedure in a sentence before writing | PASS — procedure: "Bring a protocol change to the society as a draft." |
| 2 | Cover one procedure per skill | PASS — one procedure; every tag is a step of it |
| 3 | Reading the skill does the work | PASS — instructions to a reading model; no script runs it |
| 4 | File named `SKILL.md` | PASS |
| 5 | YAML frontmatter with `name` and `description` | PASS — `name` and `description` present |
| 6 | No version field in frontmatter | PASS — no `version` key |
| 7 | `name` from the procedure (part count void, Ev:149; name from RO:5-30) | PASS — `propose` is the roster name |
| 8 | Directory name = `name` | PASS — `skills/propose/` = `propose` |
| 9 | Description: one sentence, then phrases and conditions | PASS — line 4 is one sentence ending at its period; line 5 lists 4 quoted phrases plus conditions |
| 10 | Every trigger phrase in the description, none in the body | PASS — the body holds no request phrase; conditions in the body select among this skill's own steps (tension 12) |
| 11 | Body structured in XML tags | PASS — 4 tags, no Markdown structure |
| 12 | Each tag named as an imperative verb phrase | PASS — `read-the-terms`, `report-a-defect`, `propose-a-change`, `circulate-as-the-scribe` |
| 13 | Every instruction inside a tag | PASS — 8 sentences, each inside a tag |
| 14 | No tag attributes | PASS — no tag carries an attribute |
| 15 | Inside a tag: prose and inline backticks only | PASS — no list, table, heading, or code block inside a tag |
| 16 | Body ordered as the procedure runs | PASS — tags follow the order the procedure runs |
| 17 | Everything needed inside, outside only by naming a skill | PASS — outside text reached only by naming a skill or a protocol location (tension 2) |
| 18 | Shared content moved to a third skill, not copied | PASS — shared terms live in `ontology`; no definition copied |
| 19 | Other skills referenced by name, not path | PASS — references are "the skill `<name>`"; no path |
| 20 | One instruction per sentence | PASS — each sentence holds one instruction |
| 21 | Every instruction a command | PASS — imperative mood throughout; no "should" or "may" for a duty |
| 22 | At most one emphatic word per sentence | PASS — 8 of 8 sentences carry exactly one emphatic word outside backticks |
| 23 | Emphatic words counted where they command | PASS — emphatic words inside backticks not counted |
| 24 | Each positive instruction paired with its own prohibition | PASS — every `never` half negates the same instruction its positive half gives |
| 25 | State the instruction, never argue | PASS — no sentence argues for its rule |
| 26 | Name what is required, never narrate a failure | PASS — no failure narrated |
| 27 | One term per concept | PASS — one term per concept (type, item, wake, origin checked across skills) |
| 28 | Terms defined at first use (shared terms in ontology, tension 3) | PASS — every society term from `ontology`; terms one skill uses defined in place |
| 29 | Ordinary words | PASS — ordinary words |
| 30 | Only sentences that instruct or forbid | PASS — every sentence instructs or forbids |
| 31 | Final read against every rule | PASS — read against rules 1-30 at the branch head |

## protocol-change (46 lines)

| # | rule (SC) | result |
|---|---|---|
| 1 | Name the one procedure in a sentence before writing | PASS — procedure: "Know the round every party to a protocol change shares." |
| 2 | Cover one procedure per skill | PASS — one procedure; every tag is a step of it |
| 3 | Reading the skill does the work | PASS — instructions to a reading model; no script runs it |
| 4 | File named `SKILL.md` | PASS |
| 5 | YAML frontmatter with `name` and `description` | PASS — `name` and `description` present |
| 6 | No version field in frontmatter | PASS — no `version` key |
| 7 | `name` from the procedure (part count void, Ev:149; name from RO:5-30) | PASS — `protocol-change` is the roster name |
| 8 | Directory name = `name` | PASS — `skills/protocol-change/` = `protocol-change` |
| 9 | Description: one sentence, then phrases and conditions | PASS — line 4 is one sentence ending at its period; line 5 lists 4 quoted phrases plus conditions |
| 10 | Every trigger phrase in the description, none in the body | PASS — the body holds no request phrase; conditions in the body select among this skill's own steps (tension 12) |
| 11 | Body structured in XML tags | PASS — 6 tags, no Markdown structure |
| 12 | Each tag named as an imperative verb phrase | PASS — `read-the-terms`, `time-the-round`, `weigh-the-answers`, `close-the-round`, `apply-a-shipped-change`, `keep-the-culture` |
| 13 | Every instruction inside a tag | PASS — 14 sentences, each inside a tag |
| 14 | No tag attributes | PASS — no tag carries an attribute |
| 15 | Inside a tag: prose and inline backticks only | PASS — no list, table, heading, or code block inside a tag |
| 16 | Body ordered as the procedure runs | PASS — tags follow the order the procedure runs |
| 17 | Everything needed inside, outside only by naming a skill | PASS — outside text reached only by naming a skill or a protocol location (tension 2) |
| 18 | Shared content moved to a third skill, not copied | PASS — shared terms live in `ontology`; no definition copied |
| 19 | Other skills referenced by name, not path | PASS — references are "the skill `<name>`"; no path |
| 20 | One instruction per sentence | PASS — each sentence holds one instruction |
| 21 | Every instruction a command | PASS — imperative mood throughout; no "should" or "may" for a duty |
| 22 | At most one emphatic word per sentence | PASS — 14 of 14 sentences carry exactly one emphatic word outside backticks |
| 23 | Emphatic words counted where they command | PASS — emphatic words inside backticks not counted |
| 24 | Each positive instruction paired with its own prohibition | PASS — every `never` half negates the same instruction its positive half gives |
| 25 | State the instruction, never argue | PASS — no sentence argues for its rule |
| 26 | Name what is required, never narrate a failure | PASS — no failure narrated |
| 27 | One term per concept | PASS — one term per concept (type, item, wake, origin checked across skills) |
| 28 | Terms defined at first use (shared terms in ontology, tension 3) | PASS — every society term from `ontology`; terms one skill uses defined in place |
| 29 | Ordinary words | PASS — ordinary words |
| 30 | Only sentences that instruct or forbid | PASS — every sentence instructs or forbids |
| 31 | Final read against every rule | PASS — read against rules 1-30 at the branch head |

## quote (38 lines)

| # | rule (SC) | result |
|---|---|---|
| 1 | Name the one procedure in a sentence before writing | PASS — procedure: "Relay an owner ruling until every session it reaches holds it." |
| 2 | Cover one procedure per skill | PASS — one procedure; every tag is a step of it |
| 3 | Reading the skill does the work | PASS — instructions to a reading model; no script runs it |
| 4 | File named `SKILL.md` | PASS |
| 5 | YAML frontmatter with `name` and `description` | PASS — `name` and `description` present |
| 6 | No version field in frontmatter | PASS — no `version` key |
| 7 | `name` from the procedure (part count void, Ev:149; name from RO:5-30) | PASS — `quote` is the roster name |
| 8 | Directory name = `name` | PASS — `skills/quote/` = `quote` |
| 9 | Description: one sentence, then phrases and conditions | PASS — line 4 is one sentence ending at its period; line 5 lists 3 quoted phrases plus conditions |
| 10 | Every trigger phrase in the description, none in the body | PASS — the body holds no request phrase; conditions in the body select among this skill's own steps (tension 12) |
| 11 | Body structured in XML tags | PASS — 5 tags, no Markdown structure |
| 12 | Each tag named as an imperative verb phrase | PASS — `read-the-terms`, `hold-the-owner-away`, `check-a-ruling-you-receive`, `record-the-ruling`, `relay-the-ruling` |
| 13 | Every instruction inside a tag | PASS — 11 sentences, each inside a tag |
| 14 | No tag attributes | PASS — no tag carries an attribute |
| 15 | Inside a tag: prose and inline backticks only | PASS — no list, table, heading, or code block inside a tag |
| 16 | Body ordered as the procedure runs | PASS — tags follow the order the procedure runs |
| 17 | Everything needed inside, outside only by naming a skill | PASS — outside text reached only by naming a skill or a protocol location (tension 2) |
| 18 | Shared content moved to a third skill, not copied | PASS — shared terms live in `ontology`; no definition copied |
| 19 | Other skills referenced by name, not path | PASS — references are "the skill `<name>`"; no path |
| 20 | One instruction per sentence | PASS — each sentence holds one instruction |
| 21 | Every instruction a command | PASS — imperative mood throughout; no "should" or "may" for a duty |
| 22 | At most one emphatic word per sentence | PASS — 11 of 11 sentences carry exactly one emphatic word outside backticks |
| 23 | Emphatic words counted where they command | PASS — emphatic words inside backticks not counted |
| 24 | Each positive instruction paired with its own prohibition | PASS — every `never` half negates the same instruction its positive half gives |
| 25 | State the instruction, never argue | PASS — no sentence argues for its rule |
| 26 | Name what is required, never narrate a failure | PASS — no failure narrated |
| 27 | One term per concept | PASS — one term per concept (type, item, wake, origin checked across skills) |
| 28 | Terms defined at first use (shared terms in ontology, tension 3) | PASS — every society term from `ontology`; terms one skill uses defined in place |
| 29 | Ordinary words | PASS — ordinary words |
| 30 | Only sentences that instruct or forbid | PASS — every sentence instructs or forbids |
| 31 | Final read against every rule | PASS — read against rules 1-30 at the branch head |

## receive (58 lines)

| # | rule (SC) | result |
|---|---|---|
| 1 | Name the one procedure in a sentence before writing | PASS — procedure: "Act on a message that arrives." |
| 2 | Cover one procedure per skill | PASS — one procedure; every tag is a step of it |
| 3 | Reading the skill does the work | PASS — instructions to a reading model; no script runs it |
| 4 | File named `SKILL.md` | PASS |
| 5 | YAML frontmatter with `name` and `description` | PASS — `name` and `description` present |
| 6 | No version field in frontmatter | PASS — no `version` key |
| 7 | `name` from the procedure (part count void, Ev:149; name from RO:5-30) | PASS — `receive` is the roster name |
| 8 | Directory name = `name` | PASS — `skills/receive/` = `receive` |
| 9 | Description: one sentence, then phrases and conditions | PASS — line 4 is one sentence ending at its period; line 5 lists 3 quoted phrases plus conditions |
| 10 | Every trigger phrase in the description, none in the body | PASS — the body holds no request phrase; conditions in the body select among this skill's own steps (tension 12) |
| 11 | Body structured in XML tags | PASS — 5 tags, no Markdown structure |
| 12 | Each tag named as an imperative verb phrase | PASS — `read-the-terms`, `read-what-arrives`, `answer-an-ask`, `hand-on-each-kind`, `keep-the-record` |
| 13 | Every instruction inside a tag | PASS — 21 sentences, each inside a tag |
| 14 | No tag attributes | PASS — no tag carries an attribute |
| 15 | Inside a tag: prose and inline backticks only | PASS — no list, table, heading, or code block inside a tag |
| 16 | Body ordered as the procedure runs | PASS — tags follow the order the procedure runs |
| 17 | Everything needed inside, outside only by naming a skill | PASS — outside text reached only by naming a skill or a protocol location (tension 2) |
| 18 | Shared content moved to a third skill, not copied | PASS — shared terms live in `ontology`; no definition copied |
| 19 | Other skills referenced by name, not path | PASS — references are "the skill `<name>`"; no path |
| 20 | One instruction per sentence | PASS — each sentence holds one instruction |
| 21 | Every instruction a command | PASS — imperative mood throughout; no "should" or "may" for a duty |
| 22 | At most one emphatic word per sentence | PASS — 21 of 21 sentences carry exactly one emphatic word outside backticks |
| 23 | Emphatic words counted where they command | PASS — emphatic words inside backticks not counted |
| 24 | Each positive instruction paired with its own prohibition | PASS — every `never` half negates the same instruction its positive half gives |
| 25 | State the instruction, never argue | PASS — no sentence argues for its rule |
| 26 | Name what is required, never narrate a failure | PASS — no failure narrated |
| 27 | One term per concept | PASS — one term per concept (type, item, wake, origin checked across skills) |
| 28 | Terms defined at first use (shared terms in ontology, tension 3) | PASS — every society term from `ontology`; terms one skill uses defined in place |
| 29 | Ordinary words | PASS — ordinary words |
| 30 | Only sentences that instruct or forbid | PASS — every sentence instructs or forbids |
| 31 | Final read against every rule | PASS — read against rules 1-30 at the branch head |

## reserve (32 lines)

| # | rule (SC) | result |
|---|---|---|
| 1 | Name the one procedure in a sentence before writing | PASS — procedure: "Hold an exclusive resource by its own line on the resource board." |
| 2 | Cover one procedure per skill | PASS — one procedure; every tag is a step of it |
| 3 | Reading the skill does the work | PASS — instructions to a reading model; no script runs it |
| 4 | File named `SKILL.md` | PASS |
| 5 | YAML frontmatter with `name` and `description` | PASS — `name` and `description` present |
| 6 | No version field in frontmatter | PASS — no `version` key |
| 7 | `name` from the procedure (part count void, Ev:149; name from RO:5-30) | PASS — `reserve` is the roster name |
| 8 | Directory name = `name` | PASS — `skills/reserve/` = `reserve` |
| 9 | Description: one sentence, then phrases and conditions | PASS — line 4 is one sentence ending at its period; line 5 lists 5 quoted phrases plus conditions |
| 10 | Every trigger phrase in the description, none in the body | PASS — the body holds no request phrase; conditions in the body select among this skill's own steps (tension 12) |
| 11 | Body structured in XML tags | PASS — 4 tags, no Markdown structure |
| 12 | Each tag named as an imperative verb phrase | PASS — `read-the-terms`, `check-before-claiming`, `claim-by-a-line`, `keep-the-board-true` |
| 13 | Every instruction inside a tag | PASS — 9 sentences, each inside a tag |
| 14 | No tag attributes | PASS — no tag carries an attribute |
| 15 | Inside a tag: prose and inline backticks only | PASS — no list, table, heading, or code block inside a tag |
| 16 | Body ordered as the procedure runs | PASS — tags follow the order the procedure runs |
| 17 | Everything needed inside, outside only by naming a skill | PASS — outside text reached only by naming a skill or a protocol location (tension 2) |
| 18 | Shared content moved to a third skill, not copied | PASS — shared terms live in `ontology`; no definition copied |
| 19 | Other skills referenced by name, not path | PASS — references are "the skill `<name>`"; no path |
| 20 | One instruction per sentence | PASS — each sentence holds one instruction |
| 21 | Every instruction a command | PASS — imperative mood throughout; no "should" or "may" for a duty |
| 22 | At most one emphatic word per sentence | PASS — 9 of 9 sentences carry exactly one emphatic word outside backticks |
| 23 | Emphatic words counted where they command | PASS — emphatic words inside backticks not counted |
| 24 | Each positive instruction paired with its own prohibition | PASS — every `never` half negates the same instruction its positive half gives |
| 25 | State the instruction, never argue | PASS — no sentence argues for its rule |
| 26 | Name what is required, never narrate a failure | PASS — no failure narrated |
| 27 | One term per concept | PASS — one term per concept (type, item, wake, origin checked across skills) |
| 28 | Terms defined at first use (shared terms in ontology, tension 3) | PASS — every society term from `ontology`; terms one skill uses defined in place |
| 29 | Ordinary words | PASS — ordinary words |
| 30 | Only sentences that instruct or forbid | PASS — every sentence instructs or forbids |
| 31 | Final read against every rule | PASS — read against rules 1-30 at the branch head |

## resume (20 lines)

| # | rule (SC) | result |
|---|---|---|
| 1 | Name the one procedure in a sentence before writing | PASS — procedure: "Rejoin the society as the same member after a restart, resume, clear, compaction, or usage-limit stop." |
| 2 | Cover one procedure per skill | PASS — one procedure; every tag is a step of it |
| 3 | Reading the skill does the work | PASS — instructions to a reading model; no script runs it |
| 4 | File named `SKILL.md` | PASS |
| 5 | YAML frontmatter with `name` and `description` | PASS — `name` and `description` present |
| 6 | No version field in frontmatter | PASS — no `version` key |
| 7 | `name` from the procedure (part count void, Ev:149; name from RO:5-30) | PASS — `resume` is the roster name |
| 8 | Directory name = `name` | PASS — `skills/resume/` = `resume` |
| 9 | Description: one sentence, then phrases and conditions | PASS — line 4 is one sentence ending at its period; line 5 lists 5 quoted phrases plus conditions |
| 10 | Every trigger phrase in the description, none in the body | PASS — the body holds no request phrase; conditions in the body select among this skill's own steps (tension 12) |
| 11 | Body structured in XML tags | PASS — 3 tags, no Markdown structure |
| 12 | Each tag named as an imperative verb phrase | PASS — `read-the-terms`, `rejoin`, `restore-what-the-restart-ended` |
| 13 | Every instruction inside a tag | PASS — 4 sentences, each inside a tag |
| 14 | No tag attributes | PASS — no tag carries an attribute |
| 15 | Inside a tag: prose and inline backticks only | PASS — no list, table, heading, or code block inside a tag |
| 16 | Body ordered as the procedure runs | PASS — tags follow the order the procedure runs |
| 17 | Everything needed inside, outside only by naming a skill | PASS — outside text reached only by naming a skill or a protocol location (tension 2) |
| 18 | Shared content moved to a third skill, not copied | PASS — shared terms live in `ontology`; no definition copied |
| 19 | Other skills referenced by name, not path | PASS — references are "the skill `<name>`"; no path |
| 20 | One instruction per sentence | PASS — each sentence holds one instruction |
| 21 | Every instruction a command | PASS — imperative mood throughout; no "should" or "may" for a duty |
| 22 | At most one emphatic word per sentence | PASS — 4 of 4 sentences carry exactly one emphatic word outside backticks |
| 23 | Emphatic words counted where they command | PASS — emphatic words inside backticks not counted |
| 24 | Each positive instruction paired with its own prohibition | PASS — every `never` half negates the same instruction its positive half gives |
| 25 | State the instruction, never argue | PASS — no sentence argues for its rule |
| 26 | Name what is required, never narrate a failure | PASS — no failure narrated |
| 27 | One term per concept | PASS — one term per concept (type, item, wake, origin checked across skills) |
| 28 | Terms defined at first use (shared terms in ontology, tension 3) | PASS — every society term from `ontology`; terms one skill uses defined in place |
| 29 | Ordinary words | PASS — ordinary words |
| 30 | Only sentences that instruct or forbid | PASS — every sentence instructs or forbids |
| 31 | Final read against every rule | PASS — read against rules 1-30 at the branch head |

## scribe (58 lines)

| # | rule (SC) | result |
|---|---|---|
| 1 | Name the one procedure in a sentence before writing | PASS — procedure: "Serve as the scribe, from taking the role to handing it on." |
| 2 | Cover one procedure per skill | PASS — one procedure; every tag is a step of it |
| 3 | Reading the skill does the work | PASS — instructions to a reading model; no script runs it |
| 4 | File named `SKILL.md` | PASS |
| 5 | YAML frontmatter with `name` and `description` | PASS — `name` and `description` present |
| 6 | No version field in frontmatter | PASS — no `version` key |
| 7 | `name` from the procedure (part count void, Ev:149; name from RO:5-30) | PASS — `scribe` is the roster name |
| 8 | Directory name = `name` | PASS — `skills/scribe/` = `scribe` |
| 9 | Description: one sentence, then phrases and conditions | PASS — line 4 is one sentence ending at its period; line 5 lists 5 quoted phrases plus conditions |
| 10 | Every trigger phrase in the description, none in the body | PASS — the body holds no request phrase; conditions in the body select among this skill's own steps (tension 12) |
| 11 | Body structured in XML tags | PASS — 6 tags, no Markdown structure |
| 12 | Each tag named as an imperative verb phrase | PASS — `read-the-terms`, `take-the-role`, `keep-the-text`, `run-each-round`, `ship-the-outcome`, `hand-on-the-role` |
| 13 | Every instruction inside a tag | PASS — 20 sentences, each inside a tag |
| 14 | No tag attributes | PASS — no tag carries an attribute |
| 15 | Inside a tag: prose and inline backticks only | PASS — no list, table, heading, or code block inside a tag |
| 16 | Body ordered as the procedure runs | PASS — tags follow the order the procedure runs |
| 17 | Everything needed inside, outside only by naming a skill | PASS — names the skill `card` at the ship step (GR:7); edge beyond (f), listed open in the changes file |
| 18 | Shared content moved to a third skill, not copied | PASS — shared terms live in `ontology`; no definition copied |
| 19 | Other skills referenced by name, not path | PASS — references are "the skill `<name>`"; no path |
| 20 | One instruction per sentence | PASS — each sentence holds one instruction |
| 21 | Every instruction a command | PASS — imperative mood throughout; no "should" or "may" for a duty |
| 22 | At most one emphatic word per sentence | PASS — 20 of 20 sentences carry exactly one emphatic word outside backticks |
| 23 | Emphatic words counted where they command | PASS — emphatic words inside backticks not counted |
| 24 | Each positive instruction paired with its own prohibition | PASS — every `never` half negates the same instruction its positive half gives |
| 25 | State the instruction, never argue | PASS — no sentence argues for its rule |
| 26 | Name what is required, never narrate a failure | PASS — no failure narrated |
| 27 | One term per concept | PASS — one term per concept (type, item, wake, origin checked across skills) |
| 28 | Terms defined at first use (shared terms in ontology, tension 3) | PASS — every society term from `ontology`; terms one skill uses defined in place |
| 29 | Ordinary words | PASS — ordinary words |
| 30 | Only sentences that instruct or forbid | PASS — every sentence instructs or forbids |
| 31 | Final read against every rule | PASS — read against rules 1-30 at the branch head |

## settle (30 lines)

| # | rule (SC) | result |
|---|---|---|
| 1 | Name the one procedure in a sentence before writing | PASS — procedure: "Take a contested matter to a go-between." |
| 2 | Cover one procedure per skill | PASS — one procedure; every tag is a step of it |
| 3 | Reading the skill does the work | PASS — instructions to a reading model; no script runs it |
| 4 | File named `SKILL.md` | PASS |
| 5 | YAML frontmatter with `name` and `description` | PASS — `name` and `description` present |
| 6 | No version field in frontmatter | PASS — no `version` key |
| 7 | `name` from the procedure (part count void, Ev:149; name from RO:5-30) | PASS — `settle` is the roster name |
| 8 | Directory name = `name` | PASS — `skills/settle/` = `settle` |
| 9 | Description: one sentence, then phrases and conditions | PASS — line 4 is one sentence ending at its period; line 5 lists 4 quoted phrases plus conditions |
| 10 | Every trigger phrase in the description, none in the body | PASS — the body holds no request phrase; conditions in the body select among this skill's own steps (tension 12) |
| 11 | Body structured in XML tags | PASS — 5 tags, no Markdown structure |
| 12 | Each tag named as an imperative verb phrase | PASS — `read-the-terms`, `ask-a-go-between`, `separate-what-can-exist-twice`, `bring-the-owner-the-rest`, `record-the-outcome` |
| 13 | Every instruction inside a tag | PASS — 7 sentences, each inside a tag |
| 14 | No tag attributes | PASS — no tag carries an attribute |
| 15 | Inside a tag: prose and inline backticks only | PASS — no list, table, heading, or code block inside a tag |
| 16 | Body ordered as the procedure runs | PASS — tags follow the order the procedure runs |
| 17 | Everything needed inside, outside only by naming a skill | PASS — outside text reached only by naming a skill or a protocol location (tension 2) |
| 18 | Shared content moved to a third skill, not copied | PASS — shared terms live in `ontology`; no definition copied |
| 19 | Other skills referenced by name, not path | PASS — references are "the skill `<name>`"; no path |
| 20 | One instruction per sentence | PASS — each sentence holds one instruction |
| 21 | Every instruction a command | PASS — imperative mood throughout; no "should" or "may" for a duty |
| 22 | At most one emphatic word per sentence | PASS — 7 of 7 sentences carry exactly one emphatic word outside backticks |
| 23 | Emphatic words counted where they command | PASS — emphatic words inside backticks not counted |
| 24 | Each positive instruction paired with its own prohibition | PASS — every `never` half negates the same instruction its positive half gives |
| 25 | State the instruction, never argue | PASS — no sentence argues for its rule |
| 26 | Name what is required, never narrate a failure | PASS — no failure narrated |
| 27 | One term per concept | PASS — one term per concept (type, item, wake, origin checked across skills) |
| 28 | Terms defined at first use (shared terms in ontology, tension 3) | PASS — every society term from `ontology`; terms one skill uses defined in place |
| 29 | Ordinary words | PASS — ordinary words |
| 30 | Only sentences that instruct or forbid | PASS — every sentence instructs or forbids |
| 31 | Final read against every rule | PASS — read against rules 1-30 at the branch head |

## spread-around (32 lines)

| # | rule (SC) | result |
|---|---|---|
| 1 | Name the one procedure in a sentence before writing | PASS — procedure: "Offer what you learned to the peers it may help, by gossip where you cannot name them." |
| 2 | Cover one procedure per skill | PASS — one procedure; every tag is a step of it |
| 3 | Reading the skill does the work | PASS — instructions to a reading model; no script runs it |
| 4 | File named `SKILL.md` | PASS |
| 5 | YAML frontmatter with `name` and `description` | PASS — `name` and `description` present |
| 6 | No version field in frontmatter | PASS — no `version` key |
| 7 | `name` from the procedure (part count void, Ev:149; name from RO:5-30) | PASS — `spread-around` is the roster name |
| 8 | Directory name = `name` | PASS — `skills/spread-around/` = `spread-around` |
| 9 | Description: one sentence, then phrases and conditions | PASS — line 4 is one sentence ending at its period; line 5 lists 4 quoted phrases plus conditions |
| 10 | Every trigger phrase in the description, none in the body | PASS — the body holds no request phrase; conditions in the body select among this skill's own steps (tension 12) |
| 11 | Body structured in XML tags | PASS — 4 tags, no Markdown structure |
| 12 | Each tag named as an imperative verb phrase | PASS — `read-the-terms`, `check-what-you-offer`, `send-to-the-peers-you-can-name`, `spread-the-rest-around` |
| 13 | Every instruction inside a tag | PASS — 9 sentences, each inside a tag |
| 14 | No tag attributes | PASS — no tag carries an attribute |
| 15 | Inside a tag: prose and inline backticks only | PASS — no list, table, heading, or code block inside a tag |
| 16 | Body ordered as the procedure runs | PASS — tags follow the order the procedure runs |
| 17 | Everything needed inside, outside only by naming a skill | PASS — outside text reached only by naming a skill or a protocol location (tension 2) |
| 18 | Shared content moved to a third skill, not copied | PASS — shared terms live in `ontology`; no definition copied |
| 19 | Other skills referenced by name, not path | PASS — references are "the skill `<name>`"; no path |
| 20 | One instruction per sentence | PASS — each sentence holds one instruction |
| 21 | Every instruction a command | PASS — imperative mood throughout; no "should" or "may" for a duty |
| 22 | At most one emphatic word per sentence | PASS — 9 of 9 sentences carry exactly one emphatic word outside backticks |
| 23 | Emphatic words counted where they command | PASS — emphatic words inside backticks not counted |
| 24 | Each positive instruction paired with its own prohibition | PASS — every `never` half negates the same instruction its positive half gives |
| 25 | State the instruction, never argue | PASS — no sentence argues for its rule |
| 26 | Name what is required, never narrate a failure | PASS — no failure narrated |
| 27 | One term per concept | PASS — one term per concept (type, item, wake, origin checked across skills) |
| 28 | Terms defined at first use (shared terms in ontology, tension 3) | PASS — every society term from `ontology`; terms one skill uses defined in place |
| 29 | Ordinary words | PASS — ordinary words |
| 30 | Only sentences that instruct or forbid | PASS — every sentence instructs or forbids |
| 31 | Final read against every rule | PASS — read against rules 1-30 at the branch head |

## steward (42 lines)

| # | rule (SC) | result |
|---|---|---|
| 1 | Name the one procedure in a sentence before writing | PASS — procedure: "Look after a shared thing for every session, in the open." |
| 2 | Cover one procedure per skill | PASS — one procedure; every tag is a step of it |
| 3 | Reading the skill does the work | PASS — instructions to a reading model; no script runs it |
| 4 | File named `SKILL.md` | PASS |
| 5 | YAML frontmatter with `name` and `description` | PASS — `name` and `description` present |
| 6 | No version field in frontmatter | PASS — no `version` key |
| 7 | `name` from the procedure (part count void, Ev:149; name from RO:5-30) | PASS — `steward` is the roster name |
| 8 | Directory name = `name` | PASS — `skills/steward/` = `steward` |
| 9 | Description: one sentence, then phrases and conditions | PASS — line 4 is one sentence ending at its period; line 5 lists 5 quoted phrases plus conditions |
| 10 | Every trigger phrase in the description, none in the body | PASS — the body holds no request phrase; conditions in the body select among this skill's own steps (tension 12) |
| 11 | Body structured in XML tags | PASS — 4 tags, no Markdown structure |
| 12 | Each tag named as an imperative verb phrase | PASS — `read-the-terms`, `name-it-on-your-card`, `guard-the-canonical-copy`, `pass-on-what-other-skills-handle` |
| 13 | Every instruction inside a tag | PASS — 14 sentences, each inside a tag |
| 14 | No tag attributes | PASS — no tag carries an attribute |
| 15 | Inside a tag: prose and inline backticks only | PASS — no list, table, heading, or code block inside a tag |
| 16 | Body ordered as the procedure runs | PASS — tags follow the order the procedure runs |
| 17 | Everything needed inside, outside only by naming a skill | PASS — outside text reached only by naming a skill or a protocol location (tension 2) |
| 18 | Shared content moved to a third skill, not copied | PASS — shared terms live in `ontology`; no definition copied |
| 19 | Other skills referenced by name, not path | PASS — references are "the skill `<name>`"; no path |
| 20 | One instruction per sentence | PASS — each sentence holds one instruction |
| 21 | Every instruction a command | PASS — imperative mood throughout; no "should" or "may" for a duty |
| 22 | At most one emphatic word per sentence | PASS — 14 of 14 sentences carry exactly one emphatic word outside backticks |
| 23 | Emphatic words counted where they command | PASS — emphatic words inside backticks not counted |
| 24 | Each positive instruction paired with its own prohibition | PASS — every `never` half negates the same instruction its positive half gives |
| 25 | State the instruction, never argue | PASS — no sentence argues for its rule |
| 26 | Name what is required, never narrate a failure | PASS — no failure narrated |
| 27 | One term per concept | PASS — one term per concept (type, item, wake, origin checked across skills) |
| 28 | Terms defined at first use (shared terms in ontology, tension 3) | PASS — every society term from `ontology`; terms one skill uses defined in place |
| 29 | Ordinary words | PASS — ordinary words |
| 30 | Only sentences that instruct or forbid | PASS — every sentence instructs or forbids |
| 31 | Final read against every rule | PASS — read against rules 1-30 at the branch head |

## sweep (24 lines)

| # | rule (SC) | result |
|---|---|---|
| 1 | Name the one procedure in a sentence before writing | PASS — procedure: "Move a gone member's card into `<root>/departed/`." |
| 2 | Cover one procedure per skill | PASS — one procedure; every tag is a step of it |
| 3 | Reading the skill does the work | PASS — instructions to a reading model; no script runs it |
| 4 | File named `SKILL.md` | PASS |
| 5 | YAML frontmatter with `name` and `description` | PASS — `name` and `description` present |
| 6 | No version field in frontmatter | PASS — no `version` key |
| 7 | `name` from the procedure (part count void, Ev:149; name from RO:5-30) | PASS — `sweep` is the roster name |
| 8 | Directory name = `name` | PASS — `skills/sweep/` = `sweep` |
| 9 | Description: one sentence, then phrases and conditions | PASS — line 4 is one sentence ending at its period; line 5 lists 3 quoted phrases plus conditions |
| 10 | Every trigger phrase in the description, none in the body | PASS — the body holds no request phrase; conditions in the body select among this skill's own steps (tension 12) |
| 11 | Body structured in XML tags | PASS — 3 tags, no Markdown structure |
| 12 | Each tag named as an imperative verb phrase | PASS — `read-the-terms`, `check-it-is-gone`, `move-the-card` |
| 13 | Every instruction inside a tag | PASS — 6 sentences, each inside a tag |
| 14 | No tag attributes | PASS — no tag carries an attribute |
| 15 | Inside a tag: prose and inline backticks only | PASS — no list, table, heading, or code block inside a tag |
| 16 | Body ordered as the procedure runs | PASS — tags follow the order the procedure runs |
| 17 | Everything needed inside, outside only by naming a skill | PASS — outside text reached only by naming a skill or a protocol location (tension 2) |
| 18 | Shared content moved to a third skill, not copied | PASS — shared terms live in `ontology`; no definition copied |
| 19 | Other skills referenced by name, not path | PASS — references are "the skill `<name>`"; no path |
| 20 | One instruction per sentence | PASS — each sentence holds one instruction |
| 21 | Every instruction a command | PASS — imperative mood throughout; no "should" or "may" for a duty |
| 22 | At most one emphatic word per sentence | PASS — 6 of 6 sentences carry exactly one emphatic word outside backticks |
| 23 | Emphatic words counted where they command | PASS — emphatic words inside backticks not counted |
| 24 | Each positive instruction paired with its own prohibition | PASS — every `never` half negates the same instruction its positive half gives |
| 25 | State the instruction, never argue | PASS — no sentence argues for its rule |
| 26 | Name what is required, never narrate a failure | PASS — no failure narrated |
| 27 | One term per concept | PASS — one term per concept (type, item, wake, origin checked across skills) |
| 28 | Terms defined at first use (shared terms in ontology, tension 3) | PASS — every society term from `ontology`; terms one skill uses defined in place |
| 29 | Ordinary words | PASS — ordinary words |
| 30 | Only sentences that instruct or forbid | PASS — every sentence instructs or forbids |
| 31 | Final read against every rule | PASS — read against rules 1-30 at the branch head |

## tell (74 lines)

| # | rule (SC) | result |
|---|---|---|
| 1 | Name the one procedure in a sentence before writing | PASS — procedure: "Send a peer a tagged message." |
| 2 | Cover one procedure per skill | PASS — one procedure; every tag is a step of it |
| 3 | Reading the skill does the work | PASS — instructions to a reading model; no script runs it |
| 4 | File named `SKILL.md` | PASS |
| 5 | YAML frontmatter with `name` and `description` | PASS — `name` and `description` present |
| 6 | No version field in frontmatter | PASS — no `version` key |
| 7 | `name` from the procedure (part count void, Ev:149; name from RO:5-30) | PASS — `tell` is the roster name |
| 8 | Directory name = `name` | PASS — `skills/tell/` = `tell` |
| 9 | Description: one sentence, then phrases and conditions | PASS — line 4 is one sentence ending at its period; line 5 lists 7 quoted phrases plus conditions |
| 10 | Every trigger phrase in the description, none in the body | PASS — the body holds no request phrase; conditions in the body select among this skill's own steps (tension 12) |
| 11 | Body structured in XML tags | PASS — 7 tags, no Markdown structure |
| 12 | Each tag named as an imperative verb phrase | PASS — `read-the-terms`, `send-as-a-main-session`, `pick-the-receivers`, `pick-the-type`, `write-the-message`, `deliver-or-hold`, `await-the-other-end` |
| 13 | Every instruction inside a tag | PASS — 27 sentences, each inside a tag |
| 14 | No tag attributes | PASS — no tag carries an attribute |
| 15 | Inside a tag: prose and inline backticks only | PASS — no list, table, heading, or code block inside a tag |
| 16 | Body ordered as the procedure runs | PASS — tags follow the order the procedure runs |
| 17 | Everything needed inside, outside only by naming a skill | PASS — outside text reached only by naming a skill or a protocol location (tension 2) |
| 18 | Shared content moved to a third skill, not copied | PASS — shared terms live in `ontology`; no definition copied |
| 19 | Other skills referenced by name, not path | PASS — references are "the skill `<name>`"; no path |
| 20 | One instruction per sentence | PASS — each sentence holds one instruction |
| 21 | Every instruction a command | PASS — imperative mood throughout; no "should" or "may" for a duty |
| 22 | At most one emphatic word per sentence | PASS — 27 of 27 sentences carry exactly one emphatic word outside backticks |
| 23 | Emphatic words counted where they command | PASS — emphatic words inside backticks not counted |
| 24 | Each positive instruction paired with its own prohibition | PASS — every `never` half negates the same instruction its positive half gives |
| 25 | State the instruction, never argue | PASS — no sentence argues for its rule |
| 26 | Name what is required, never narrate a failure | PASS — no failure narrated |
| 27 | One term per concept | PASS — one term per concept (type, item, wake, origin checked across skills) |
| 28 | Terms defined at first use (shared terms in ontology, tension 3) | PASS — every society term from `ontology`; terms one skill uses defined in place |
| 29 | Ordinary words | PASS — ordinary words |
| 30 | Only sentences that instruct or forbid | PASS — every sentence instructs or forbids |
| 31 | Final read against every rule | PASS — read against rules 1-30 at the branch head |

## tend (54 lines)

| # | rule (SC) | result |
|---|---|---|
| 1 | Name the one procedure in a sentence before writing | PASS — procedure: "Build, correct, merge, and retire what the commons holds." |
| 2 | Cover one procedure per skill | PASS — one procedure; every tag is a step of it |
| 3 | Reading the skill does the work | PASS — instructions to a reading model; no script runs it |
| 4 | File named `SKILL.md` | PASS |
| 5 | YAML frontmatter with `name` and `description` | PASS — `name` and `description` present |
| 6 | No version field in frontmatter | PASS — no `version` key |
| 7 | `name` from the procedure (part count void, Ev:149; name from RO:5-30) | PASS — `tend` is the roster name |
| 8 | Directory name = `name` | PASS — `skills/tend/` = `tend` |
| 9 | Description: one sentence, then phrases and conditions | PASS — line 4 is one sentence ending at its period; line 5 lists 6 quoted phrases plus conditions |
| 10 | Every trigger phrase in the description, none in the body | PASS — the body holds no request phrase; conditions in the body select among this skill's own steps (tension 12) |
| 11 | Body structured in XML tags | PASS — 5 tags, no Markdown structure |
| 12 | Each tag named as an imperative verb phrase | PASS — `read-the-terms`, `hold-the-commons-in-common`, `build-in-the-commons`, `tend-what-stands`, `carry-what-you-tend` |
| 13 | Every instruction inside a tag | PASS — 19 sentences, each inside a tag |
| 14 | No tag attributes | PASS — no tag carries an attribute |
| 15 | Inside a tag: prose and inline backticks only | PASS — no list, table, heading, or code block inside a tag |
| 16 | Body ordered as the procedure runs | PASS — tags follow the order the procedure runs |
| 17 | Everything needed inside, outside only by naming a skill | PASS — outside text reached only by naming a skill or a protocol location (tension 2) |
| 18 | Shared content moved to a third skill, not copied | PASS — shared terms live in `ontology`; no definition copied |
| 19 | Other skills referenced by name, not path | PASS — references are "the skill `<name>`"; no path |
| 20 | One instruction per sentence | PASS — each sentence holds one instruction |
| 21 | Every instruction a command | PASS — imperative mood throughout; no "should" or "may" for a duty |
| 22 | At most one emphatic word per sentence | PASS — 19 of 19 sentences carry exactly one emphatic word outside backticks |
| 23 | Emphatic words counted where they command | PASS — emphatic words inside backticks not counted |
| 24 | Each positive instruction paired with its own prohibition | PASS — every `never` half negates the same instruction its positive half gives |
| 25 | State the instruction, never argue | PASS — no sentence argues for its rule |
| 26 | Name what is required, never narrate a failure | PASS — no failure narrated |
| 27 | One term per concept | PASS — one term per concept (type, item, wake, origin checked across skills) |
| 28 | Terms defined at first use (shared terms in ontology, tension 3) | PASS — every society term from `ontology`; terms one skill uses defined in place |
| 29 | Ordinary words | PASS — ordinary words |
| 30 | Only sentences that instruct or forbid | PASS — every sentence instructs or forbids |
| 31 | Final read against every rule | PASS — read against rules 1-30 at the branch head |

## volunteer (40 lines)

| # | rule (SC) | result |
|---|---|---|
| 1 | Name the one procedure in a sentence before writing | PASS — procedure: "Turn time free of your own work into work for the society." |
| 2 | Cover one procedure per skill | PASS — one procedure; every tag is a step of it |
| 3 | Reading the skill does the work | PASS — instructions to a reading model; no script runs it |
| 4 | File named `SKILL.md` | PASS |
| 5 | YAML frontmatter with `name` and `description` | PASS — `name` and `description` present |
| 6 | No version field in frontmatter | PASS — no `version` key |
| 7 | `name` from the procedure (part count void, Ev:149; name from RO:5-30) | PASS — `volunteer` is the roster name |
| 8 | Directory name = `name` | PASS — `skills/volunteer/` = `volunteer` |
| 9 | Description: one sentence, then phrases and conditions | PASS — line 4 is one sentence ending at its period; line 5 lists 5 quoted phrases plus conditions |
| 10 | Every trigger phrase in the description, none in the body | PASS — the body holds no request phrase; conditions in the body select among this skill's own steps (tension 12) |
| 11 | Body structured in XML tags | PASS — 5 tags, no Markdown structure |
| 12 | Each tag named as an imperative verb phrase | PASS — `read-the-terms`, `volunteer-when-free`, `find-the-work`, `pick-one-in-order`, `do-it-by-its-skill` |
| 13 | Every instruction inside a tag | PASS — 12 sentences, each inside a tag |
| 14 | No tag attributes | PASS — no tag carries an attribute |
| 15 | Inside a tag: prose and inline backticks only | PASS — no list, table, heading, or code block inside a tag |
| 16 | Body ordered as the procedure runs | PASS — tags follow the order the procedure runs |
| 17 | Everything needed inside, outside only by naming a skill | PASS — outside text reached only by naming a skill or a protocol location (tension 2) |
| 18 | Shared content moved to a third skill, not copied | PASS — shared terms live in `ontology`; no definition copied |
| 19 | Other skills referenced by name, not path | PASS — references are "the skill `<name>`"; no path |
| 20 | One instruction per sentence | PASS — each sentence holds one instruction |
| 21 | Every instruction a command | PASS — imperative mood throughout; no "should" or "may" for a duty |
| 22 | At most one emphatic word per sentence | PASS — 12 of 12 sentences carry exactly one emphatic word outside backticks |
| 23 | Emphatic words counted where they command | PASS — emphatic words inside backticks not counted |
| 24 | Each positive instruction paired with its own prohibition | PASS — every `never` half negates the same instruction its positive half gives |
| 25 | State the instruction, never argue | PASS — no sentence argues for its rule |
| 26 | Name what is required, never narrate a failure | PASS — no failure narrated |
| 27 | One term per concept | PASS — one term per concept (type, item, wake, origin checked across skills) |
| 28 | Terms defined at first use (shared terms in ontology, tension 3) | PASS — every society term from `ontology`; terms one skill uses defined in place |
| 29 | Ordinary words | PASS — ordinary words |
| 30 | Only sentences that instruct or forbid | PASS — every sentence instructs or forbids |
| 31 | Final read against every rule | PASS — read against rules 1-30 at the branch head |

## vouch (22 lines)

| # | rule (SC) | result |
|---|---|---|
| 1 | Name the one procedure in a sentence before writing | PASS — procedure: "Check a claim before you believe it, act on it, or pass it on." |
| 2 | Cover one procedure per skill | PASS — one procedure; every tag is a step of it |
| 3 | Reading the skill does the work | PASS — instructions to a reading model; no script runs it |
| 4 | File named `SKILL.md` | PASS |
| 5 | YAML frontmatter with `name` and `description` | PASS — `name` and `description` present |
| 6 | No version field in frontmatter | PASS — no `version` key |
| 7 | `name` from the procedure (part count void, Ev:149; name from RO:5-30) | PASS — `vouch` is the roster name |
| 8 | Directory name = `name` | PASS — `skills/vouch/` = `vouch` |
| 9 | Description: one sentence, then phrases and conditions | PASS — line 4 is one sentence ending at its period; line 5 lists 4 quoted phrases plus conditions |
| 10 | Every trigger phrase in the description, none in the body | PASS — the body holds no request phrase; conditions in the body select among this skill's own steps (tension 12) |
| 11 | Body structured in XML tags | PASS — 3 tags, no Markdown structure |
| 12 | Each tag named as an imperative verb phrase | PASS — `read-the-terms`, `check-the-claim`, `route-a-failed-check` |
| 13 | Every instruction inside a tag | PASS — 5 sentences, each inside a tag |
| 14 | No tag attributes | PASS — no tag carries an attribute |
| 15 | Inside a tag: prose and inline backticks only | PASS — no list, table, heading, or code block inside a tag |
| 16 | Body ordered as the procedure runs | PASS — tags follow the order the procedure runs |
| 17 | Everything needed inside, outside only by naming a skill | PASS — outside text reached only by naming a skill or a protocol location (tension 2) |
| 18 | Shared content moved to a third skill, not copied | PASS — shared terms live in `ontology`; no definition copied |
| 19 | Other skills referenced by name, not path | PASS — references are "the skill `<name>`"; no path |
| 20 | One instruction per sentence | PASS — each sentence holds one instruction |
| 21 | Every instruction a command | PASS — imperative mood throughout; no "should" or "may" for a duty |
| 22 | At most one emphatic word per sentence | PASS — 5 of 5 sentences carry exactly one emphatic word outside backticks |
| 23 | Emphatic words counted where they command | PASS — emphatic words inside backticks not counted |
| 24 | Each positive instruction paired with its own prohibition | PASS — every `never` half negates the same instruction its positive half gives |
| 25 | State the instruction, never argue | PASS — no sentence argues for its rule |
| 26 | Name what is required, never narrate a failure | PASS — no failure narrated |
| 27 | One term per concept | PASS — one term per concept (type, item, wake, origin checked across skills) |
| 28 | Terms defined at first use (shared terms in ontology, tension 3) | PASS — every society term from `ontology`; terms one skill uses defined in place |
| 29 | Ordinary words | PASS — ordinary words |
| 30 | Only sentences that instruct or forbid | PASS — every sentence instructs or forbids |
| 31 | Final read against every rule | PASS — read against rules 1-30 at the branch head |
