import json
import subprocess
from pathlib import Path

import pytest

from test_send_stamp import root, send, send_stamp_command, updated_message, STAMP  # noqa: F401

HOOKS_DIR = Path(__file__).resolve().parent.parent / "hooks"
PEER_JOIN = HOOKS_DIR / "peer-join.sh"


@pytest.mark.parametrize("switch", ["PEERS_HOOKS", "PEERS_SEND_STAMP"])
def test_send_stamp_off_switch_passes_a_tagged_message_unstamped(send, switch):
    assert send({"to": "peer", "message": "[ask] x\nreply: none"}, **{switch: "off"}) == ""


def test_send_stamp_bypasses_a_message_to_main(send):
    assert send({"to": "main", "message": "[notice] x\nreply: none"}) == ""


def test_send_stamp_still_stamps_with_switches_on(send):
    output = send({"to": "peer", "message": "[quote] x\nreply: none"}, PEERS_HOOKS="on", PEERS_SEND_STAMP="on")
    assert updated_message(output) == f"[quote] x\nreply: none · sent {STAMP}"


def run_peer_join(tmp_path, **env_extra):
    home = tmp_path / "home"
    (home / ".local" / "share" / "agents-of-anarchy").mkdir(parents=True)
    completed = subprocess.run(
        ["bash", str(PEER_JOIN), "join"],
        input=json.dumps({"hook_event_name": "SessionStart", "source": "startup"}),
        capture_output=True, text=True,
        env={"HOME": str(home), "CLAUDE_PLUGIN_ROOT": str(HOOKS_DIR.parent), "PATH": "/usr/bin:/bin", **env_extra},
    )
    assert completed.returncode == 0, completed.stderr
    return completed.stdout


def test_peer_join_prints_the_join_line_with_switches_on(tmp_path):
    assert "peers:join" in run_peer_join(tmp_path)


@pytest.mark.parametrize("switch", ["PEERS_HOOKS", "PEERS_JOIN_HOOK"])
def test_peer_join_off_switch_prints_nothing(tmp_path, switch):
    assert run_peer_join(tmp_path, **{switch: "off"}) == ""
