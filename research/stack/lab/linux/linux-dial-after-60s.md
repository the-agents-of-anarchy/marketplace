# Fresh dials more than 60 s after the kill: Linux vs macOS

lab-sibling, 2026-10-20, a check on E14's cause (the relay actor exits after 60 s idle and releases the send path).

The method is my `awk` over raw logs: PROBE records whose time is more than 60000 ms after the KILL record, with field 5 `ok` counted. I ran the same filter on both OS's logs. All runs are scenario 1 (R1+B1 killed), probers on, 88 s window, variant a, debug.

| run | OS | probes >60 s | ok >60 s |
|---|---|---|---|
| E10 a-1-1 | Linux | 42 | 0 |
| E10 a-1-2 | Linux | 42 | 0 |
| E10 a-1-3 | Linux | 81 | 0 |
| E12 a-1l12-1 | Linux | 42 | 0 |
| E12 a-1l12-2 | Linux | 42 | 0 |
| E12 a-1l12-3 | Linux | 42 | 0 |
| E10 a-1-1 | macOS | 58 | 20 |
| E10 a-1-2 | macOS | 84 | 0 |
| E10 a-1-3 | macOS | 42 | 0 |
| E12 a-1l12-1 | macOS | 59 | 22 (first late ok 63.9 s) |
| E12 a-1l12-2 | macOS | 42 | 0 |
| E12 a-1l12-3 | macOS | 46 | 5 (first 85.1 s) |
| E12 a-1l12-4 | macOS | 43 | 3 (first 76.5 s) |
| E12 a-1l12-5 | macOS | 80 | 40 (first late ok 10.0 s; this run also had 10 `No addressing information available` errors) |

Linux had 0/6 runs with any dial success after 60 s. macOS had 5/8, and in 4 of those 5 the successes start after 60 s (63.9, 76.5, 85.1 s, and E10 a-1-1).

On macOS this fits a release at about 60 s plus jitter. On Linux, no release shows within the 88 s window. Either the 60 s idle exit does not happen on Linux by 88 s (for example, an idle timer reset by the retried sends), or it happens and something else still blocks.

The run that would tell these apart is one cell with a 180 s window (`run-cell.sh a 1 w 3`) on Linux. I have not run it; it waits on resident-anarchist.

Caveats: n is small (6 vs 8 runs); the window ends 28 s after the 60 s mark; the probe cadence after 60 s is about 1 per 3 s per pair, so a release in the last few seconds could be missed.
