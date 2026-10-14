import json
import re
import shutil
import subprocess
from pathlib import Path

import pytest

HOOKS_DIR = Path(__file__).resolve().parent.parent / "hooks"
HOOKS_JSON = HOOKS_DIR / "hooks.json"
TOOL = "SendMessage"
STAMP = "2026-10-14T09:30+0300"


def send_stamp_command():
    entries = json.loads(HOOKS_JSON.read_text())["hooks"]["PreToolUse"]
    (command,) = [
        hook["command"]
        for entry in entries
        if re.fullmatch(entry.get("matcher", ".*"), TOOL)
        for hook in entry["hooks"]
        if "send-stamp.sh" in hook["command"]
    ]
    return command


@pytest.fixture
def root(tmp_path):
    path = tmp_path / "society"
    path.mkdir()
    return path


@pytest.fixture
def send(tmp_path, root, stub_path, fixed_clock):
    def run(tool_input, *, society=None, path=None, raw=None, **env_extra):
        payload = {"hook_event_name": "PreToolUse", "tool_name": TOOL, "tool_input": tool_input}
        env = {
            "HOME": str(tmp_path),
            "CLAUDE_PLUGIN_ROOT": str(HOOKS_DIR.parent),
            "AGENTS_OF_ANARCHY_ROOT": str(root if society is None else society),
            "PATH": path or stub_path(date=fixed_clock.date_script),
            **env_extra,
        }
        completed = subprocess.run(
            ["bash", "-c", send_stamp_command()],
            input=json.dumps(payload) if raw is None else raw, capture_output=True, text=True, env=env,
        )
        assert completed.returncode == 0, completed.stderr
        return completed.stdout

    return run


def updated_message(output):
    return json.loads(output)["hookSpecificOutput"]["updatedInput"]["message"]


def test_the_reply_line_gains_the_sent_stamp(send):
    output = send({"to": "peer", "message": "[ask] need the path\nreply: by 12:00\nbody line"})
    assert updated_message(output) == f"[ask] need the path\nreply: by 12:00 · sent {STAMP}\nbody line"


def test_other_tool_input_fields_pass_through_unchanged(send):
    tool_input = {"to": "peer", "summary": "short", "notify_when_idle": True, "message": "[ask] q\nreply: none"}
    updated = json.loads(send(tool_input))["hookSpecificOutput"]["updatedInput"]
    assert updated == {**tool_input, "message": f"[ask] q\nreply: none · sent {STAMP}"}


def test_the_output_allows_the_send(send):
    decision = json.loads(send({"to": "peer", "message": "[ask] q\nreply: none"}))["hookSpecificOutput"]
    assert (decision["hookEventName"], decision["permissionDecision"]) == ("PreToolUse", "allow")


@pytest.mark.parametrize(
    "message, expected",
    [
        ("[notice] hi", "[notice] hi\nsent {stamp}"),
        ("[notice] hi\nbody line", "[notice] hi\nsent {stamp}\nbody line"),
        ("[notice] hi\nbody\nreply: none", "[notice] hi\nsent {stamp}\nbody\nreply: none"),
    ],
)
def test_without_a_reply_line_a_sent_line_follows_the_first_line(send, message, expected):
    output = send({"to": "peer", "message": message})
    assert updated_message(output) == expected.format(stamp=STAMP)


UNTAGGED_MESSAGES = [
    "hello there",
    "[other] x\nreply: none",
    "no tag here\n[ask] second line",
    " [ask] leading space",
    "[asking] x",
    "[ASK] x",
    "",
]


@pytest.mark.parametrize("message", UNTAGGED_MESSAGES)
def test_an_untagged_message_passes_without_output(send, message):
    assert send({"to": "peer", "message": message}) == ""


@pytest.mark.parametrize(
    "tool_input",
    [
        {"to": "peer", "message": {"type": "shutdown_request"}},
        {"to": "peer", "message": 7},
        {"to": "peer", "message": None},
        {"to": "peer", "message": ["[ask] x"]},
        {"to": "peer"},
        {},
    ],
)
def test_a_message_that_is_no_string_passes_without_output(send, tool_input):
    assert send(tool_input) == ""


@pytest.mark.parametrize("tag", ["hazard", "ask", "answer", "notice"])
def test_each_protocol_tag_is_stamped(send, tag):
    output = send({"to": "peer", "message": f"[{tag}] x\nreply: none"})
    assert updated_message(output) == f"[{tag}] x\nreply: none · sent {STAMP}"


@pytest.mark.parametrize(
    "message",
    [
        "[ask] q\nreply: none · sent 2026-10-14T08:00+0300",
        "[notice] hi\nsent 2026-10-14T08:00+0300\nbody",
        "[hazard] h\nreply: none\nbody quoting sent 2025-01-01T00:00+0000",
    ],
)
def test_a_message_already_stamped_passes_without_output(send, message):
    assert send({"to": "peer", "message": message}) == ""


MESSAGE = {"to": "peer", "message": "[ask] q\nreply: none"}
STAMPED = f"[ask] q\nreply: none · sent {STAMP}"


def test_an_absent_root_passes_without_output_and_stays_absent(send, tmp_path):
    absent = tmp_path / "absent"
    assert send(MESSAGE, society=absent) == ""
    assert not absent.exists()


def test_the_root_defaults_under_xdg_data_home(send, tmp_path):
    xdg = tmp_path / "xdg"
    (xdg / "agents-of-anarchy").mkdir(parents=True)
    assert updated_message(send(MESSAGE, society="", XDG_DATA_HOME=str(xdg))) == STAMPED


def test_the_root_defaults_under_home(send, tmp_path):
    assert send(MESSAGE, society="") == ""
    (tmp_path / ".local" / "share" / "agents-of-anarchy").mkdir(parents=True)
    assert updated_message(send(MESSAGE, society="")) == STAMPED


def test_the_old_root_variable_does_not_open_the_gate(send, tmp_path):
    old = tmp_path / "old-root"
    old.mkdir()
    assert send(MESSAGE, society="", CLAUDE_PEERS_ROOT=str(old)) == ""


def test_without_jq_the_hook_passes_without_output(send, tmp_path, fixed_clock):
    bare = tmp_path / "bare"
    bare.mkdir()
    (bare / "bash").symlink_to(shutil.which("bash"))
    (bare / "date").write_text(fixed_clock.date_script)
    (bare / "date").chmod(0o755)
    assert send(MESSAGE, path=str(bare)) == ""


def test_malformed_input_passes_without_output(send):
    assert send(MESSAGE, raw="not json {") == ""


def test_an_unreadable_clock_passes_without_output(send, stub_path):
    assert send(MESSAGE, path=stub_path(date="#!/bin/sh\nexit 1\n")) == ""


def test_a_trailing_newline_survives(send):
    output = send({"to": "peer", "message": "[ask] q\nreply: none\n"})
    assert updated_message(output) == f"{STAMPED}\n"


def test_quotes_unicode_and_backslashes_survive(send):
    body = 'say "hi" \\ — ünïcode \t tab'
    output = send({"to": "peer", "message": f"[notice] x\nreply: none\n{body}"})
    assert updated_message(output) == f"[notice] x\nreply: none · sent {STAMP}\n{body}"


def test_hooks_json_registers_the_hook_on_send_message_only():
    entries = json.loads(HOOKS_JSON.read_text())["hooks"]["PreToolUse"]
    assert [entry["matcher"] for entry in entries] == [TOOL]
    assert send_stamp_command() == "bash ${CLAUDE_PLUGIN_ROOT}/hooks/send-stamp.sh"
