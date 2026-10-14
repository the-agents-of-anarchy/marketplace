import os
from dataclasses import dataclass

import pytest

FIXED_STAMP = "2026-10-14T09:30+0300"
FIXED_STAMP_UTC = "2026-10-14T06:30Z"
LOCAL_STAMP_FORMAT = "%Y-%m-%dT%H:%M%z"
UTC_STAMP_FORMAT = "%Y-%m-%dT%H:%MZ"
STUB_MODE = 0o755

DATE_STUB = f"""#!/bin/sh
for format; do :; done
printf '%s\\n' "${{format#+}}" | sed -e 's/{LOCAL_STAMP_FORMAT}/{FIXED_STAMP}/' -e 's/{UTC_STAMP_FORMAT}/{FIXED_STAMP_UTC}/'
"""


@dataclass(frozen=True)
class Clock:
    """A fixed clock: the stamp it reads and the `date` stub script that reads it."""

    stamp: str
    date_script: str


@pytest.fixture
def stub_path(tmp_path):
    """Return a builder of PATH values led by executable stubs, each named by keyword with its script text."""

    def build(**scripts: str) -> str:
        stubs = tmp_path / "stubs"
        stubs.mkdir(exist_ok=True)
        for name, script in scripts.items():
            stub = stubs / name
            stub.write_text(script)
            stub.chmod(STUB_MODE)
        return f"{stubs}:{os.environ['PATH']}"

    return build


@pytest.fixture
def fixed_clock() -> Clock:
    """Return the clock every stamp in a test reads."""
    return Clock(stamp=FIXED_STAMP, date_script=DATE_STUB)
