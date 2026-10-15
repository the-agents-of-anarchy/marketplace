import re
from pathlib import Path

PLUGIN = Path(__file__).resolve().parent.parent
SKILLS = PLUGIN / "skills"
TEXTS = [
    *SKILLS.glob("*/SKILL.md"),
    *(PLUGIN / "hooks" / "templates").glob("*.txt"),
    PLUGIN / "hooks" / "hooks.json",
    PLUGIN / "hooks" / "peer-join.sh",
    PLUGIN / "README.md",
]


def frontmatter_name(path):
    match = re.search(r"^name:\s*(\S+)\s*$", path.read_text(), re.MULTILINE)
    return match.group(1) if match else None


ROSTER = [
    "adopt", "aid", "ask-around", "card", "consent", "gather", "gossip", "heartbeat", "join", "leave",
    "ontology", "post", "propose", "protocol-change", "quote", "receive", "reserve", "resume", "settle",
    "ship", "spread-around", "steward", "sweep", "tell", "tend", "volunteer", "vouch",
]


def test_skill_set_is_the_protocol_10_1_roster():
    assert sorted(p.name for p in SKILLS.iterdir() if p.is_dir()) == ROSTER


def test_frontmatter_name_matches_directory():
    for skill in SKILLS.glob("*/SKILL.md"):
        assert frontmatter_name(skill) == skill.parent.name


def test_no_text_names_a_retired_skill():
    for path in TEXTS:
        text = path.read_text()
        assert "gossip-around" not in text, path
        assert not re.search(r"(peers:|skill `|skills/)peer-protocol", text), path


def test_every_plugin_skill_reference_resolves():
    names = {p.name for p in SKILLS.iterdir() if p.is_dir()}
    for path in TEXTS:
        for ref in re.findall(r"peers:([a-z][a-z-]*)", path.read_text()):
            assert ref in names, (path, ref)


JOIN = SKILLS / "join" / "SKILL.md"
GOSSIP = SKILLS / "gossip" / "SKILL.md"
ONTOLOGY = SKILLS / "ontology" / "SKILL.md"
CARD = SKILLS / "card" / "SKILL.md"
RESERVE = SKILLS / "reserve" / "SKILL.md"
MAP_TAG = "map-the-seams-to-claude-code"
CLAUDE_CODE_TERMS = ["ListAgents", "SendMessage", "SessionStart", "CLAUDE_CONFIG_DIR", "/reload-plugins", ".jsonl", "AskUserQuestion"]


def body(path):
    return path.read_text().split("---", 2)[2]


def test_card_states_protocol_10_1():
    assert "Carry `protocol: 10.1`" in CARD.read_text()


def test_claude_code_terms_live_only_in_the_one_mapping_tag():
    text = body(ONTOLOGY)
    assert text.count(f"<{MAP_TAG}>") == 1
    inside = text.split(f"<{MAP_TAG}>")[1].split(f"</{MAP_TAG}>")[0]
    outside = text.replace(inside, "")
    for term in CLAUDE_CODE_TERMS:
        assert term in inside, term
        assert term not in outside, term
    for skill in SKILLS.glob("*/SKILL.md"):
        if skill == ONTOLOGY:
            continue
        for term in CLAUDE_CODE_TERMS:
            assert term not in body(skill), (skill, term)


def test_card_carries_member_fields_and_drops_ref_fields():
    text = CARD.read_text()
    for field in ("member", "harness", "address", "machine", "reads"):
        assert f"Carry `{field}`" in text, field
    assert "`role`" not in text
    assert "Carry `ref`" not in text
    assert "Carry `prior_refs`" not in text
    assert "<root>/members/<member>.md" in ONTOLOGY.read_text()
    assert "<root>/inbox/<member>.md" in ONTOLOGY.read_text()
    assert "<root>/resources.md" in RESERVE.read_text()


def test_no_text_names_the_old_root():
    for path in TEXTS:
        assert "claude-peers" not in path.read_text(), path


def test_address_names_harness_host_and_ref():
    text = ONTOLOGY.read_text()
    assert "`<harness>://<host>/<harness-ref>`" in text
    assert "`claude-code://<host>/<ref>`" in text
    assert "`scutil --get LocalHostName`" in text
    assert "`hostname -s`" in text
    assert "claude-code:<ref>" not in text


def test_member_id_unique_within_one_society():
    assert "unique within one society" in ONTOLOGY.read_text()


def test_protocol_stewardship_is_named_protocol():
    text = ONTOLOGY.read_text()
    assert "peer-protocol" not in text
    assert "`stewards` lists `protocol`" in text


SOCIETY = "agents that share a project, a machine, or neither, on any harness"


def test_join_description_names_the_society():
    head = JOIN.read_text().split("---", 2)[1]
    assert SOCIETY in head
    assert SOCIETY in (PLUGIN / "README.md").read_text().split("## Skills", 1)[1]


MANIFESTS = [PLUGIN / ".claude-plugin" / "plugin.json", PLUGIN.parent / ".claude-plugin" / "marketplace.json"]


def test_plugin_descriptions_name_the_society():
    for path in [*MANIFESTS, PLUGIN / "README.md"]:
        text = path.read_text()
        assert "Claude Code sessions" not in text, path
        assert f"A society of {SOCIETY}: its protocol, its commons, and gossip between peers." in text, path


RELAY_LINE = "relay: pass this on as spread: says, adding yourself to has: first; if you hold what it seeks or it changes your work, reach from: directly."


def test_gossip_carries_the_envelope_and_the_fixed_relay_line():
    text = GOSSIP.read_text()
    for field in ("from: <member id> <session name>", "spread: <free text>", "has: <members>"):
        assert f"`{field}`" in text, field
    assert f"`{RELAY_LINE}`" in text


def test_gossip_sets_no_protocol_fan_out_or_stop():
    text = GOSSIP.read_text()
    for phrase in ("two or three", "one to three", "never to everyone", "whose work would gain", "no peer outside", "asked:"):
        assert phrase not in text, phrase


TEMPLATES = PLUGIN / "hooks" / "templates"


def test_session_start_lines_name_join_at_startup_and_resume_otherwise():
    assert "peers:join" in (TEMPLATES / "peer-join.txt").read_text()
    for name in ("peer-resume.txt", "peer-compact.txt"):
        text = (TEMPLATES / name).read_text()
        assert "peers:resume" in text and "peers:join" not in text, name


def test_no_two_skills_share_a_sentence():
    seen = {}
    for skill in SKILLS.glob("*/SKILL.md"):
        for line in body(skill).splitlines():
            if line.strip() and not line.startswith("<"):
                assert line not in seen, (skill.parent.name, seen.get(line), line)
                seen[line] = skill.parent.name
