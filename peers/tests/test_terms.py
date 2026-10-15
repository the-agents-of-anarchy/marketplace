import re
from pathlib import Path

import pytest

SKILLS = Path(__file__).resolve().parent.parent / "skills"
ONTOLOGY = SKILLS / "ontology" / "SKILL.md"
TERMS_TAG = "take-the-terms"

# Each ontology term, in ontology order, with the pattern that finds it in a skill body.
TERMS = [
    ("harness", r"\bharness(es)?\b(?!-ref)"),
    ("session", r"\bsessions?\b"),
    ("host", r"\bhosts?\b"),
    ("harness-ref", r"harness-ref"),
    ("address", r"\baddress(es)?\b"),
    ("turn", r"\bturns?\b"),
    ("tool round", r"tool round"),
    ("act", r"\bact(s|ing)?\b"),
    ("skill", r"\bskills?\b"),
    ("hook", r"\bhooks?\b"),
    ("plugin", r"\bplugins?\b"),
    ("compaction", r"\bcompaction\b"),
    ("subagent", r"\bsubagents?\b"),
    ("login", r"\blogins?\b"),
    ("stamp", r"\bstamps?\b"),
    ("wake", r"\bwakes?\b"),
    ("member", r"\bmembers?('s)?\b"),
    ("body", r"(?<!message )\bbod(y|ies)('s)?\b"),
    ("root", r"<root>|\broot\b"),
    ("society", r"\bsociety('s)?\b"),
    ("protocol", r"\bprotocol\b(?! change)"),
    ("member id", r"member id"),
    ("card", r"\bcards?('s)?\b"),
    ("departed card", r"\bdeparted\b"),
    ("worktree", r"\bworktrees?\b"),
    ("checkout", r"\bcheckouts?\b"),
    ("owner", r"\bowner('s)?\b"),
    ("owner message", r"owner message"),
    ("owner ruling", r"owner ruling|\brulings?\b"),
    ("records", r"\brecords\b"),
    ("memento records", r"\bmemento\b"),
    ("journal", r"\bjournals?\b"),
    ("question tool", r"question tool"),
    ("bringing a matter to the owner", r"\bbring\w* (the owner|\w+ (\w+ )?to the owner)|\bBring the owner\b"),
    ("brought matter", r"\bbrought (matter|dispute)"),
    ("authority check", r"authority check"),
    ("main session", r"main session"),
    ("presence", r"\bpresence\b"),
    ("busy", r"\bbusy\b"),
    ("idle", r"\bidl(e|ing|ed)\b"),
    ("waiting", r"`waiting`"),
    ("dormant", r"\bdormant\b"),
    ("dnd", r"\bdnd\b"),
    ("state", r"\bstates?\b"),
    ("delivery", r"\bdeliver(y|s|ed|ing)?\b"),
    ("transport", r"\btransports?\b"),
    ("message", r"\bmessages?\b"),
    ("message body", r"message bod(y|ies)"),
    ("type", r"\btypes?\b"),
    ("[hazard]", r"\[hazard\]"),
    ("[ask]", r"\[ask\]|\b(an|the|every|each|your|a direct|a gossip|direct|gossip) asks?\b|\basks\b"),
    ("[answer]", r"\[answer\]|\b(an|the|its|by its) answer\b|\banswers\b"),
    ("[notice]", r"\[notice\]"),
    ("[quote]", r"\[quote\]"),
    ("reply time", r"reply time"),
    ("held", r"\bheld message|\bHold a (level 2|relay)\b|\bfor a hold\b|\bnever hold one\b"),
    ("origin", r"\borigin('s)?\b"),
    ("seeker", r"\bseekers?\b"),
    ("leave notice", r"leave notice"),
    ("live", r"\blive\b"),
    ("gone", r"\bgone\b"),
    ("peer", r"\bpeers?('s)?\b"),
    ("commons", r"\bcommons\b"),
    ("intake", r"\bintake\b"),
    ("commons line", r"commons lines?"),
    ("#<n>", r"#<n>|<#n"),
    ("commons item", r"\bitems?\b"),
    ("commons_read", r"commons_read"),
    ("exclusive resource", r"exclusive resources?"),
    ("resource board", r"resource board|<root>/resources\.md|\bboard lines?\b|\bthe board\b"),
    ("inbox", r"\binbox(es)?\b"),
    ("gossip", r"\bgossip"),
    ("relaying", r"\brelay(s|ing|ed|er|ers)?\b(?!:)"),
    ("scope", r"\bscopes?\b"),
    ("envelope", r"\benvelope\b"),
    ("from:", r"\bfrom:"),
    ("spread:", r"\bspread:"),
    ("relay:", r"\brelay:"),
    ("has:", r"\bhas:"),
    ("push", r"\bpush"),
    ("pull", r"\bpull"),
    ("adoption", r"\badopt(ion|s|ed|ing)?\b"),
    ("diffusion", r"\bdiffusion\b"),
    ("claim", r"\bclaims?\b|\bclaimant"),
    ("stewardship", r"\bstewardships?\b"),
    ("steward", r"\bsteward('s)?\b|\bstewards\b"),
    ("open stewardship", r"open stewardship"),
    ("scribe", r"\bscribe('s)?\b"),
    ("go-between", r"go-between"),
    ("level 1", r"\blevel 1\b"),
    ("level 2", r"\blevel 2\b"),
    ("level 3", r"\blevel 3\b"),
    ("escalation", r"\bescalat\w*"),
    ("priority level", r"priority level|\blevels?\b"),
    ("acting on a level 1 message", r"\bact on (each|a) (level 1 )?message"),
    ("pointer", r"\bpointer('s)?\b"),
    ("change line", r"change lines?"),
    ("protocol change", r"protocol change"),
    ("draft", r"\bdrafts?('s)?\b"),
    ("round", r"(?<!tool )\brounds?('s)?\b"),
    ("enacted", r"\benact(ed|s)?\b"),
    ("separating", r"\bseparat\w*"),
    ("bound", r"\bbound\b"),
    ("shipping", r"\bship(s|ped|ping)?\b"),
    ("<root>/culture/", r"culture"),
    ("reloaded", r"\breload"),
]


def body(path):
    return path.read_text().split("---", 2)[2]


def terms_sentence(path):
    text = body(path)
    return text.split(f"<{TERMS_TAG}>")[1].split(f"</{TERMS_TAG}>")[0].strip()


def description(path):
    head = path.read_text().split("---", 2)[1]
    return head.split("description:", 1)[1]


def scanned_body(path):
    text = description(path) + body(path)
    text = re.sub(rf"<{TERMS_TAG}>.*?</{TERMS_TAG}>", "", text, flags=re.S)
    text = re.sub(r"the skills? `[a-z:-]+`( and `[a-z-]+`)?", "", text)
    text = re.sub(r"peers:[a-z-]+", "", text)
    text = re.sub(r"by the skills [a-z-]+(, [a-z-]+)*,? and [a-z-]+", "", text)
    return text


def used_terms(path):
    text = scanned_body(path)
    return [label for label, pattern in TERMS if re.search(pattern, text, re.IGNORECASE if not label.startswith("[") else 0)]


def listed_terms(path):
    return re.findall(r"`([^`]+)`", terms_sentence(path).split(" as the skill ")[0].replace("``", "`"))


OTHER_SKILLS = sorted(p for p in SKILLS.glob("*/SKILL.md") if p != ONTOLOGY)


def test_every_term_label_is_defined_in_ontology():
    text = body(ONTOLOGY)
    for label, _ in TERMS:
        assert label.strip("`") in text, label


@pytest.mark.parametrize("skill", OTHER_SKILLS, ids=lambda p: p.parent.name)
def test_terms_sentence_names_every_ontology_term_the_body_uses(skill):
    listed = set(listed_terms(skill))
    missing = [term for term in used_terms(skill) if term.strip("`") not in listed]
    assert not missing, (skill.parent.name, missing)


# Ordinary-verb and other-sense uses of ontology terms, banned in every skill (ruling, round 5).
# Each entry: (term, phrases where the word carries the ontology sense, pattern of the other sense).
OTHER_SENSES = [
    ("held", ["Hold a level 2 message", "held message",
              "never hold one.", "never hold it past that turn", "call for a hold", "a held message",
              "message held", "<deliver-or-hold>", "</deliver-or-hold>", "deliver it, hold it, or append"],
     r"\b[Hh]old(s|ing)?\b|\bheld\b"),
    ("act", ["act now", "acted on", "acting on a level 1 message", "acting on it", "an act", "each act it calls"],
     r"\b[Aa]cts?\b(?= (on|from|as|upon)\b)|\bacting\b|\bacted\b"),
    ("relaying", [], r"relay\w* (an owner ruling|what my subagent|a ruling|the owner)|relayed ruling|a relay's"),
    ("claim", [], r"\bClaim (a|an|the)\b|\b(to|never|you|they) claim\b|\bclaim (with|arrives|on)\b|\bits claim\b|\bclaimed\b|\bclaiming\b"),
    ("records", [], r"\bRecord\b|\brecorded\b|\brecording\b|\b(harness|it|you) records\b|\ba record\b|\bproject record\b"),
    ("turn", [], r"\b[Tt]urn(s|ed)? (it|them|every|time|free)\b|\b(to|never|you) turn\b|\bTurn\b|\bturning\b"),
    ("state", [], r"\bState\b|\b(to|never|you|peers) state\b|\bstates (its|the|a)\b|\bstated\b"),
    ("delivery", [], r"\b[Dd]eliver(s|ed|ing)? (help|it as|a fix|an artifact)\b"),
    ("wake", [], r"\bwakes (an|the)\b|\bwaking\b"),
    ("live", [], r"\blives\b"),
    ("bound", [], r"\bbounds\b"),
    ("address", [], r"\baddressees?\b"),
    ("[notice]", [], r"unnotic"),
    ("type", [], r"\btyped\b"),
    ("resource board", [], r"\ba board\b(?! line)"),
]

ALL_SKILLS = sorted(SKILLS.glob("*/SKILL.md"))


@pytest.mark.parametrize("skill", ALL_SKILLS, ids=lambda p: p.parent.name)
def test_no_ontology_term_is_used_in_another_sense(skill):
    text = re.sub(r"`[^`]*`", "", description(skill) + body(skill))
    hits = []
    for term, allowed, pattern in OTHER_SENSES:
        scanned = text
        for phrase in allowed:
            scanned = scanned.replace(phrase, "")
        hits += [(term, m.group(0)) for m in re.finditer(pattern, scanned)]
    assert not hits, (skill.parent.name, hits)
