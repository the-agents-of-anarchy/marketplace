# Writing stack for the protocol-10 skill rewrite

Reader: the single fable agent that rewrites the peers skills. Bind every element below before your first edit. Open with the binding report the manifesto-oath protocol requires: what you loaded, from where, the interplay, and the paired commitments.

Keys used here and in `rewrite-instructions.md`:
- `SC:<n>` is a line of the skill-creation rules file.
- `Ev:<n>` is a line of `/Users/ryzhakar/pp/agents-of-anarchy-marketplace/docs/orchestration_log/history/2026-10-14/events.md`.
- `RO:<n>` is a line of `/Users/ryzhakar/pp/agents-of-anarchy-marketplace/docs/orchestration_log/recon/2026-10-15/skill-roster.md`.
- `STR rule <n>` is a rule id in the Strunk file.

## 1. Elements

### 1.1 skill-creation

- Source: skill `memento:skill-creation`, version 0.5.1. Local file: `/Users/ryzhakar/.claudes/meta/plugins/cache/memento/memento/0.5.1/skills/skill-creation/SKILL.md` (82 lines). The copy under `/Users/ryzhakar/.claude/plugins/cache/memento/memento/0.5.1/` is byte-identical.
- Governs: the form of every skill. That covers one procedure per skill, frontmatter, description, XML tags, body order, cross-references, and every sentence rule (SC:56-76). It also covers the final read-through (SC:80).
- Not governed: name length. The owner voided the "two or three parts" clause of SC:26 (Ev:149, Ev:150). The rest of SC:26 and SC:28 still bind.
- Binding command: **Bind to skill-creation — show your commitments before working.**

### 1.2 strunk-spr-v3

- Source: `https://raw.githubusercontent.com/ryzhakar/LLM_MANIFESTOS/refs/heads/main/instructions/strunk_spr_v3_complete.xml`, as named by `/Users/ryzhakar/pp/agents-of-anarchy-marketplace/.manifestos.yaml` under `subagents.instruction-writer`. Local copy: `/Users/ryzhakar/pp/agents-of-anarchy-marketplace/.claude/manifesto-repo/LLM_MANIFESTOS/instructions/strunk_spr_v3_complete.xml` (2924 lines).
- Governs: word choice and sentence build inside the form skill-creation fixes. The rules that apply:
  - STR rule 10: active voice.
  - STR rule 11: positive form for the command half.
  - STR rule 12: concrete, specific words.
  - STR rule 13: omit needless words.
  - STR rule 15: parallel construction, which every `<command>; never <same command>` pair is.
  - STR rule 16: related words together.
  - STR rule 5: no comma splice.
  - STR rule 3: definitions set off by paired commas or dashes.
  - Genre `technical_documentation`: imperative mood, and one term for one concept.
- Binding command: **Bind to strunk-spr-v3 — show your commitments before working.**

### 1.3 first-principles

- Source: `https://raw.githubusercontent.com/ryzhakar/LLM_MANIFESTOS/refs/heads/main/manifestos/first-principles.md`, as named in `.manifestos.yaml`. Local copy: `/Users/ryzhakar/pp/agents-of-anarchy-marketplace/.claude/manifesto-repo/LLM_MANIFESTOS/manifestos/first-principles.md`.
- Governs: what each skill must achieve, and whether each sentence earns its place.
  - Derive each skill's procedure from the act the roster names. Never derive it from the layout of the 9.3 tags.
  - Test each source sentence: does a step of this procedure need it? A sentence no step needs is dropped with its reason.
  - Read a 9.3 sentence as a hypothesis about what a member must do. Never read it as a form to copy.
- Binding command: **Bind to first-principles — show your commitments before working.**

### 1.4 self-documenting-code

- Source: `/Users/ryzhakar/pp/agents-of-anarchy-marketplace/.claude/manifesto-repo/LLM_MANIFESTOS/manifestos/self-documenting-code.md`. The owner named it as the first lens for naming (Ev:146).
- Governs: names inside the skills (tag names, terms in ontology) and the absence of explanation.
  - Tag names reveal intent ("Names That Tell Stories", lines 48-56).
  - No tag name joins two acts with "and" ("The 'And' Smell", lines 173-180).
  - No catch-all tag or term ("The 'Utils' Catastrophe", lines 182-188).
  - Domain words over plumbing words (line 264).
  - A sentence that explains a rule is a comment, and comments are dropped (lines 13-25). This matches SC:66.
  - Every ontology term must pass the newcomer test (lines 251-257).
- Binding command: **Bind to self-documenting-code — show your commitments before working.**

### 1.5 Owner rulings (binding input)

- Source: `Ev:41-197`. Every entry marked `owner ruling, ryzhakar` binds. Entries marked `verified by` are the scribe session's decisions that rest on a ruling. They bind only where the cited ruling does.
- Governs: content, the roster, names, the reference graph, the priority table, and the scope of the rewrite. On content, a ruling outranks every manifesto above.
- The rulings that change the text, verbatim or near-verbatim:
  - **The owner is always away.** Ev:41: "by the time you recieve my message, you have zero evidence i'm not away".
  - **Contact.** Ev:46: "yes for all except busy or dnd/away. 'waiting' is fine." Ev:51 and Ev:55: `dnd` is a card state set by the owner only.
  - **Pull.** Ev:47: "gossip request collecting knowledge or a single direct message for a targeted peer … both must exist".
  - **Diffusion.** Ev:48: "diffusion is adoption".
  - **Not-busy time.** Ev:49: "encourage to set [heartbeats] … the non-busy mode of operation should not drop to idling, but to society participation". Ev:54: participation is "learn, teach and ask, tend the commons, mutual aid". Ev:57: "map idle onto explicitly volunteer work".
  - **Adoption.** Ev:50: "COMMONS IS NOT STATUS DUMP … you THANK THE ORIGIN, directly". Ev:53: "a thank you note. single line. that's all."
  - **The commons is shared.** Ev:55: "fully communal garden. public space with shared responsiblity over."
  - **Gossip.** Ev:78: "gossip specifically must be self-replicating". Ev:93: "gossip constraints are for originator to figure out. we must not bake in any assumptions." Ev:165: "gossip propagation shoul filter through both 'has' and current status".
  - **Versions.** Ev:113: "before 1.0.0 we're in alpha … breaking changes left and right". Ev:114 applies it: no major-bump approval before 1.0.0.
  - **Conformance.** Ev:127: "anyone weighin-in on SKILLS specifically must learn /memento:skill-creation first!" Ev:144: "i fucking told you" (protocol 10 is the conformance rewrite) and "ontology skill" (shared terms live in one skill).
  - **Names.** Ev:149: "join for actually joining in, not for catch-all … 2-3-parts is bogus, ignore that … peers:<verb> is great".
  - **Roster rulings.**
    - Ev:181: "quote, should use gossip underneath and have priority reach as hazards do"; "reserve"; "tell".
    - Ev:183: "the commons are not a file, they are a location in which arbitraty complexity can be built by the society. tend."
    - Ev:183: "seeking and offering are APPLICATIONS of gossip mechanic … [verb]-around".
    - Ev:186: "i want the opposing parties to be able to know only their part and some common context. 2+shared, enabling 1+shared load at most." Scribe is its own skill. New skills: "receive, vouch, heartbeat".
    - Ev:188: `protocol-change`. Quote has "Hazard priority, keeps spreading". Parking goes "In card".
    - Ev:190: "adopt, no learn".
  - **Priority.** Ev:191: "priority levels with specific scopes … 3 levels, but a single extension to message types"; level 1 overrides dnd; the table lives inside ontology; a sender may escalate.
  - **Reference graph.** Ev:193: "skills form a connected (not fully connected!) graph of references … skills reference eagerly. only obvious low-hanging hooks. join is requested on sessionstart".
  - **One agent, and the pointer.** Ev:195: "rewrite handled by a single fable agent". On the pointer: "this one is a part of protocol: a location we intend to use".
- The settled roster, priority table, and graph are `RO:5-74`.
- Binding command: **Bind to the owner rulings at Ev:41-197 and the roster at RO:1-74 — show your commitments before working.**

## 2. Tensions and the rule that resolves each

Each row names both sides with their sources, then the rule. Apply the rule; never reopen it.

1. **Name length.**
   - Tension: SC:26 asks for "two or three lowercase parts". Ev:149 says "2-3-parts is bogus, ignore that".
   - Rule: take every name from `RO:5-30` exactly. The owner ruling outranks SC:26 on length alone.
   - Still binding: SC:26's "naming what it does" and SC:28's "directory name = `name`".
2. **Pointing outside the skill.**
   - Tension: SC:48 says "never point outside it to fetch". 9.3 join and amend fetch change lines from `<root>/PROTOCOL.md`. Ev:195 says the pointer "is a part of protocol: a location".
   - Rule: ontology defines the pointer as a protocol location beside the commons, the cards, and the resource board. A skill may name a protocol location the way it names `<root>/members/`.
   - Still forbidden: shipping a non-skill file that a skill fetches instructions from. The rule targets that case (Ev:196).
3. **Where terms are defined.**
   - Tension: SC:72 says to define each term "in the sentence that first uses it". Ev:144 says "shared terms … ontology skill". SC:50 says "Move what two skills both need into a third skill".
   - Rule: every term outside ordinary English lives only in `ontology`. Every other skill names `ontology` once, at its first step, as the source of its terms (RO:50). A term that only one skill uses is defined in that skill, at first use (SC:72).
4. **Tables inside a skill.**
   - Tension: SC:44 says "Inside a tag write prose and inline backticks; never write anything else." RO:36 and Ev:191 ask for "one lookup table" of priority levels.
   - Rule: write each level as one prose sentence in a single ontology tag. Each sentence names the level's number, name, message types, reach, overrides, when the receiver acts, and spread. Never write a Markdown table in a skill.
5. **Suggestion vs command.**
   - Tension: Ev:49 says "encourage to set" a wake. SC:58 says "never as a suggestion".
   - Rule: command the participation (Ev:49, "should not drop to idling"). Command the wake as one means to it, never as the requirement. This is the draft's wording at `aoa-participation/peers/skills/join/SKILL.md:299`.
6. **Statement of the protocol version.**
   - Tension: SC:76 says "never keep" a sentence that neither instructs nor forbids, and 9.3 join:9 "This skill is peer protocol 9.3." is such a sentence. 9.3 join:209 needs a version the loaded text states.
   - Rule: state the version inside an instruction in the skill `card`: the `protocol` field carries `10`. Drop the bare statement. Re-pin the test to the card sentence.
7. **Judgment vs the absolute rules.**
   - Tension: Strunk's judgment protocol ("You MAY break a rule when…") and its hierarchy (clarity over correctness) allow deviation. SC:80 says "never deliver a skill that breaks one".
   - Rule: inside a skill, skill-creation has no exceptions. Strunk chooses among wordings that all pass skill-creation.
8. **Positive form vs the mandatory prohibition.**
   - Tension: STR rule 11 says "PUT STATEMENTS IN POSITIVE FORM". SC:64 requires a `never` half in every sentence.
   - Rule: the command half is positive. `never` appears once, in the prohibition half. That prohibition negates the same command (SC:64), which STR rule 11 allows as antithesis ("Not X, but Y").
9. **Inherited text vs first principles.**
   - Tension: first-principles says "Discard the Playbook". The brief says to take sentences from the 9.3 and draft text, and the rulings bind.
   - Rule: owner rulings and adopted 9.3 behavior are axioms. Their wording is not. Keep the behavior a sentence encodes and rewrite its form. Drop a sentence only for a reason: an owner ruling, a skill-creation rule, a case on record, or no step needing it. Never drop one for taste.
10. **Specific names vs plain names with a wink.**
    - Tension: self-documenting-code wants long, specific names (lines 52-56). Ev:149 sets "peers:<verb>" and "Plain with a wink".
    - Rule: skill names come from the roster. Self-documenting-code governs tag names and ontology terms only.
11. **One procedure vs ontology.**
    - Tension: SC:12 says "Cover one procedure per skill". Ontology names content, not an act (naming-lenses.md:83). The owner blessed it (Ev:149).
    - Rule: ontology's procedure is "read the society's terms as defined here". Every ontology sentence is an instruction of the form `Call <x> <definition>; never call <other> <x>`, the pattern of 9.3 join:81. Never let ontology carry a rule whose act belongs to another skill's procedure, except where `rewrite-instructions.md` places it there provisionally and lists it as an open item.
12. **Reference edges vs triggers in the body.**
    - Tension: SC:32 forbids trigger conditions in the body. RO:47-73 asks for edges "at the step where it applies", and some steps are conditional (receive: "a relay line arrives").
    - Rule: an edge names the skill that does a step's act ("…by the skill `gossip`"). A condition inside a step selects among that skill's own steps. Phrases a request matches go only in the description.
13. **Shared parts of the protocol round.**
    - Tension: SC:50 says to move shared content into a third skill. Ev:186 says "1+shared load at most". RO:33 says "never both opposing skills".
    - Rule: `propose` and `consent` each name `protocol-change`. `protocol-change` names neither. A sentence both parties need goes to `protocol-change`.
14. **Explanations.**
    - Tension: self-documenting-code allows a "WHY" comment as a last resort (line 238). SC:66 says "State the instruction; never argue for it."
    - Rule: skill text carries no why. A reason that matters goes to the changes file.

## 3. Priority when a conflict remains

Apply the elements in this order:
1. Owner rulings, on content.
2. skill-creation, on form.
3. first-principles, on whether a sentence earns its place.
4. self-documenting-code, on names inside skills.
5. strunk-spr-v3, on wording.

Record a conflict this order cannot settle as an open item in the changes file, and ask the scribe. Never settle it yourself.
