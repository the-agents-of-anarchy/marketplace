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


def test_skill_set_is_join_and_gossip():
    assert sorted(p.name for p in SKILLS.iterdir() if p.is_dir()) == ["gossip", "join"]


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
