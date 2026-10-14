import json
import os
import subprocess
from pathlib import Path

import pytest

SCRIPT = Path(__file__).resolve().parent.parent / "bin" / "peers-card"
REF = "abc123"
HOST = "testhost"
SESSION_ID = "11111111-2222-3333-4444-555555555555"
MODEL = "claude-real-model"

CARD = """\
member: demo/tester
harness: stale-harness
address: claude-code://oldhost/aaaaaa
name: old-name
project: /old/project
checkout: /old/checkout
branch: old-branch
login: /old/login
model: old-model
protocol: 9.2
focus: keep this line
updated: 2000-01-01T00:00+0000
"""


@pytest.fixture
def home(tmp_path):
    path = tmp_path / "home"
    path.mkdir()
    return path


@pytest.fixture
def repo(tmp_path):
    path = tmp_path / "re po & co"
    path.mkdir()
    for args in (["init", "-q", "-b", "main"], ["commit", "-q", "--allow-empty", "-m", "init"]):
        subprocess.run(
            ["git", "-c", "user.name=t", "-c", "user.email=t@t", *args],
            cwd=path, check=True, capture_output=True,
            env={**os.environ, "GIT_CONFIG_GLOBAL": "/dev/null"},
        )
    return path


@pytest.fixture
def transcript(home):
    directory = home / ".claude" / "projects" / "proj"
    directory.mkdir(parents=True)
    entry = {"type": "assistant", "message": {"model": MODEL, "content": []}}
    (directory / f"{SESSION_ID}.jsonl").write_text(json.dumps(entry) + "\n")


@pytest.fixture
def card(tmp_path):
    path = tmp_path / "tester.md"
    path.write_text(CARD)
    return path


@pytest.fixture
def run_card(home, repo, stub_path, fixed_clock, transcript):
    def run(*args, cwd=None, **env_extra):
        env = {
            "PATH": stub_path(date=fixed_clock.date_script, uname="#!/bin/sh\necho Darwin\n",
                              scutil=f"#!/bin/sh\necho {HOST}\n"),
            "HOME": str(home),
            "GIT_CONFIG_GLOBAL": "/dev/null",
            "GIT_CONFIG_SYSTEM": "/dev/null",
            "CLAUDECODE": "1",
            "CLAUDE_CODE_SESSION_ID": SESSION_ID,
            **env_extra,
        }
        return subprocess.run([str(SCRIPT), *args], cwd=cwd or repo, env=env, capture_output=True, text=True)

    return run


def lines_of(path):
    return dict(line.partition(": ")[::2] for line in path.read_text().splitlines())


def test_updated_takes_the_current_stamp(run_card, card, fixed_clock):
    result = run_card("--ref", REF, str(card))
    assert result.returncode == 0, result.stderr
    assert lines_of(card)["updated"] == fixed_clock.stamp


def test_address_names_the_host_and_the_ref(run_card, card):
    run_card("--ref", REF, str(card))
    assert lines_of(card)["address"] == f"claude-code://{HOST}/{REF}"


@pytest.mark.parametrize("key", ["harness", "login", "model", "checkout", "branch"])
def test_checked_facts_replace_their_card_lines(run_card, card, home, repo, key):
    expected = {
        "harness": "claude-code",
        "login": str(home / ".claude"),
        "model": MODEL,
        "checkout": str(repo.resolve()),
        "branch": "main",
    }
    run_card("--ref", REF, str(card))
    assert lines_of(card)[key] == expected[key]


FACT_KEYS = ("harness", "address", "login", "model", "checkout", "branch", "updated")
UNFINISHED_CARD = (
    CARD
    + "\n# note: not a fact\nknows:\n  - gossip\n  model: indented, so not the model line\nmodel_note: kept"
)


def non_fact_lines(text):
    return [line for line in text.split("\n") if line.split(":")[0] not in FACT_KEYS]


def test_other_lines_stay_byte_identical(run_card, tmp_path):
    path = tmp_path / "unfinished.md"
    path.write_text(UNFINISHED_CARD)
    run_card("--ref", REF, str(path))
    after = path.read_text()
    assert non_fact_lines(after) == non_fact_lines(UNFINISHED_CARD)
    assert len(after.split("\n")) == len(UNFINISHED_CARD.split("\n"))
    assert not after.endswith("\n")


def test_dry_run_prints_the_diff_and_leaves_the_card(run_card, card, fixed_clock):
    result = run_card("--dry-run", "--ref", REF, str(card))
    assert result.returncode == 0, result.stderr
    assert card.read_text() == CARD
    printed = result.stdout.splitlines()
    assert "-updated: 2000-01-01T00:00+0000" in printed
    assert f"+updated: {fixed_clock.stamp}" in printed
    assert f"+address: claude-code://{HOST}/{REF}" in printed
    assert all(line[:1] in "-+@ " for line in printed)


def test_name_option_sets_the_name_line(run_card, card):
    run_card("--name", "fresh-name", "--ref", REF, str(card))
    assert lines_of(card)["name"] == "fresh-name"


def test_name_line_stays_without_the_name_option(run_card, card):
    run_card("--ref", REF, str(card))
    assert lines_of(card)["name"] == "old-name"


def test_missing_card_exits_2_and_creates_nothing(run_card, tmp_path):
    absent = tmp_path / "absent.md"
    result = run_card("--ref", REF, str(absent))
    assert result.returncode == 2
    assert result.stderr.strip() == f"error: {absent} is not a card file"
    assert not absent.exists()


def test_directory_as_card_exits_2(run_card, tmp_path):
    result = run_card("--ref", REF, str(tmp_path))
    assert result.returncode == 2


@pytest.mark.parametrize("ref", ["abc12", "ABC123", "abc12g", "abc1234", "", "abc123\nabc123"])
def test_bad_ref_exits_2_and_leaves_the_card(run_card, card, ref):
    result = run_card("--ref", ref, str(card))
    assert result.returncode == 2
    assert result.stderr.strip() == f"error: ref '{ref}' is not six lowercase hex characters"
    assert card.read_text() == CARD


def test_missing_ref_exits_2_and_leaves_the_card(run_card, card):
    result = run_card(str(card))
    assert result.returncode == 2
    assert result.stderr.strip() == "error: --ref <6hex> is required"
    assert card.read_text() == CARD


def test_unknown_option_exits_2(run_card, card):
    result = run_card("--bogus", "--ref", REF, str(card))
    assert result.returncode == 2
    assert result.stderr.strip() == "error: unknown option --bogus"
    assert card.read_text() == CARD


@pytest.mark.parametrize("option", ["--ref", "--name"])
def test_option_without_a_value_exits_2(run_card, card, option):
    result = run_card("--ref", REF, str(card), option)
    assert result.returncode == 2
    assert result.stderr.strip() == f"error: {option} needs a value"


def test_two_card_paths_exit_2(run_card, card):
    result = run_card("--ref", REF, str(card), str(card))
    assert result.returncode == 2
    assert result.stderr.strip() == "error: more than one card path"


def test_no_card_path_exits_2(run_card):
    result = run_card("--ref", REF)
    assert result.returncode == 2
    assert result.stderr.strip() == "error: card path is required"


def test_help_prints_usage_and_exits_0(run_card):
    result = run_card("--help")
    assert result.returncode == 0
    assert result.stdout.startswith("usage: peers-card ")


def test_unreadable_model_keeps_its_line_and_warns(run_card, card):
    result = run_card("--ref", REF, str(card), CLAUDE_CODE_SESSION_ID="")
    assert result.returncode == 0, result.stderr
    assert lines_of(card)["model"] == "old-model"
    assert "warning: model not refreshed: no checked fact" in result.stderr


def test_outside_claude_code_keeps_harness_and_address_and_warns(run_card, card, fixed_clock):
    result = run_card("--ref", REF, str(card), CLAUDECODE="")
    assert result.returncode == 0, result.stderr
    kept = lines_of(card)
    assert (kept["harness"], kept["address"]) == ("stale-harness", "claude-code://oldhost/aaaaaa")
    assert kept["updated"] == fixed_clock.stamp
    assert "warning: harness not refreshed: no checked fact" in result.stderr
    assert "warning: address not refreshed: no checked fact" in result.stderr


def test_outside_git_keeps_checkout_and_branch_and_warns(run_card, card, tmp_path):
    plain = tmp_path / "plain"
    plain.mkdir()
    result = run_card("--ref", REF, str(card), cwd=plain)
    assert result.returncode == 0, result.stderr
    kept = lines_of(card)
    assert (kept["checkout"], kept["branch"]) == ("/old/checkout", "old-branch")
    assert "warning: checkout not refreshed: no checked fact" in result.stderr
    assert "warning: branch not refreshed: no checked fact" in result.stderr


def test_fact_without_a_card_line_is_not_added_and_noted(run_card, tmp_path):
    path = tmp_path / "sparse.md"
    path.write_text("member: demo/tester\nupdated: 2000-01-01T00:00+0000\n")
    result = run_card("--ref", REF, str(path))
    assert result.returncode == 0, result.stderr
    assert len(path.read_text().splitlines()) == 2
    for key in ("harness", "address", "login", "model", "checkout", "branch"):
        assert f"note: card has no {key} line; not added" in result.stderr
    assert "note: card has no updated line" not in result.stderr


def test_empty_name_exits_2(run_card, card):
    result = run_card("--name", "", "--ref", REF, str(card))
    assert result.returncode == 2
    assert result.stderr.strip() == "error: --name needs a value"
    assert card.read_text() == CARD


def test_a_normal_run_prints_the_diff_and_writes_the_card(run_card, card, fixed_clock):
    result = run_card("--ref", REF, str(card))
    assert f"+updated: {fixed_clock.stamp}" in result.stdout.splitlines()
    assert lines_of(card)["updated"] == fixed_clock.stamp


def test_a_second_refresh_in_the_same_minute_changes_nothing(run_card, card):
    run_card("--ref", REF, str(card))
    refreshed = card.read_text()
    second = run_card("--ref", REF, str(card))
    assert second.stdout == ""
    assert card.read_text() == refreshed
