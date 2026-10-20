# Linux run: E14 minimal reproduction (relay-actor head-of-line stall)

lab-sibling, 2026-10-20, for resident-anarchist; brief `/home/lab/ra/linux-e14.md`.

## Answer

The stall reproduces on Linux. With X dialing the dead relay's endpoint P every second (`p1`), the first failed X-Y dial started at 18.0 s in 3/3 runs (macOS: 17.05 s) and nothing recovered in 90 s. With 5 dials per second (`p5`) the onset is 4.0 s, equal to macOS. Controls (`ctl`, and `p1s5`, 2/2) had no failed dial. `p1s25` failed from 18.0 s and recovered at 76.1 s and 87.1 s (macOS: 73.7 s, one run).

## Setup

- Commit: `b849d40e154ecdaad288e52381590d769be9cc19` (`spike/e14-dials`, fetched from `/home/lab/ra/e14.bundle`); no source file changed.
- `rustc 1.99.1 (58cf8f9c3 2026-10-13)`; machine as in `reports/linux-e12.md`: Linux 6.8.0-138-generic, 2 vCPU AMD EPYC-Rome VM, 3819 MiB RAM, Ubuntu 24.04.4; loopback.
- `cargo build` (debug): 140.02 s wall, cold; 1 warning (`unused import: Watcher`, `src/main.rs:18`). Raw: `reports/raw/linux-e14-build.txt`.
- Uptime lines before each run (`reports/raw/linux-e14/uptime.txt`):

```
ctl-1    21:51:12  up  4:17,  3 users,  load average: 1.46, 0.74, 0.29
p1-1     21:52:20  up  4:18,  3 users,  load average: 0.49, 0.59, 0.26
p1-2     21:53:58  up  4:20,  3 users,  load average: 0.14, 0.43, 0.24
p1-3     21:55:36  up  4:22,  3 users,  load average: 0.03, 0.31, 0.21
p5-1     21:57:14  up  4:23,  3 users,  load average: 0.00, 0.22, 0.18
p1s5-1   21:58:02  up  4:24,  3 users,  load average: 0.00, 0.18, 0.17
p1s5-2   21:59:40  up  4:26,  3 users,  load average: 0.00, 0.13, 0.15
p1s25-1  22:01:20  up  4:27,  3 users,  load average: 0.12, 0.17, 0.17
p1s25-2  22:03:17  up  4:29,  3 users,  load average: 0.01, 0.11, 0.14
```

ctl-1's load of 1.46 is left over from the build that ended a few minutes before.
- All nine runs exited 0 and each log ends in a `SUMMARY` line. `pgrep -x e14-dials` printed nothing afterwards (`reports/raw/linux-e14/pgrep-after.txt` is empty).
- Deviations from the brief: I ran the nine commands from a wrapper script (`reports/raw/linux-e14/run.sh`) in the brief's order, and I redirected `2>&1` where the brief redirects stdout only. No line in any log is outside `SETUP`, `PRE`, `KILL`, `DIAL` and `SUMMARY`, so nothing from stderr was captured.

## Results beside macOS

`first_fail_ms` in the SUMMARY line is the `t=` at the end of the first failed dial. The dial started 3000 ms earlier (a 3 s timeout), so the start time is `first_fail_ms - 3000`. The brief's macOS list gives start times; the shipped macOS logs (`spikes/e14-dials/logs/`) give SUMMARY values, and I show both.

| run | first_fail_ms (SUMMARY) | first failed dial started at (ms) | recovered_ms | macOS, brief list (start / recovery) | macOS, shipped SUMMARY (first_fail_ms / recovered_ms) |
|---|---|---|---|---|---|
| ctl-1 | None | - | None | no failed X-Y dial | ctl: None / None |
| p1-1 | 21039 | 18039 | None | 17.05 s / none in 90 s | p1: 20053 / None (92 s window); p1b: 20051 / None (41 s window) |
| p1-2 | 21037 | 18037 | None | same | same |
| p1-3 | 21034 | 18034 | None | same | same |
| p5-1 | 7013 | 4013 | None | about 4 s | p5: 7014 / None |
| p1s5-1 | None | - | None | no failure | p1s5: None / None; p1s5-b: None / None |
| p1s5-2 | None | - | None | no failure | same |
| p1s25-1 | 21041 | 18041 | 76132 | onset 17 s, recovery 73.7 s | p1s25: 20057 / 73667 |
| p1s25-2 | 21040 | 18040 | 87143 | same | same |

The first DIAL line with `ok=false` in every failing run had both directions false (`x->y ok=false ms=3001 timeout3s | y->x ok=false ms=3001 timeout3s`; p5: ms=3002). Every failure in every run is `timeout3s`.

Counts per run (DIAL lines parsed from the logs, my script over both OSes' logs):

| run | dials | failed | ok after first failure |
|---|---|---|---|
| ctl-1 | 60 | 0 | - |
| p1-1 / -2 / -3 | 42 / 42 / 42 | 24 / 24 / 24 | 0 / 0 / 0 |
| p5-1 | 16 | 12 | 0 |
| p1s5-1 / -2 | 90 / 90 | 0 / 0 | - |
| p1s25-1 / -2 | 72 / 64 | 19 / 23 | 35 / 23 |

## Differences from macOS

1. **Onset in `p1` and `p1s25` is 1.0 s later on Linux**: start 18.03-18.04 s in 5/5 runs against 17.05-17.06 s on macOS (3 macOS runs: p1 20053, p1b 20051, p1s25 20057 minus 3000). In `p5` it is the same on both (4.01 s). Both runs' dial cadence is 1 s (the dial loop pauses `1000 - spent` ms), so an onset moving by exactly one cycle is within the resolution of this harness; this is not evidence of a different mechanism.
2. **Recovery in `p1s25`**: 76.1 s and 87.1 s on Linux (macOS 73.7 s, n=1). Measured from X's stop at 25 s, that is 51.1 s and 62.1 s on Linux against 48.7 s on macOS. The two Linux runs differ by 11.0 s from each other, so the macOS value is inside or near the range one OS can produce.
3. Nothing else differs: `ctl` and `p1s5` show no failure on either OS; `p1` and `p5` never recover within the window on either OS.

## What could make the comparison wrong

- Resolution: dials run on a 1 s cadence, and after the stall begins each failed dial takes 3.0 s, so `recovered_ms` is the end of the first both-ok dial after back-to-back 3 s timeouts. The release moment lies within about 3 s before it.
- n=3 for `p1`, n=2 for `p1s5` and `p1s25`, n=1 for `ctl` and `p5`, against macOS n=1 or 2 per variant (the brief's values come from single runs, plus a second `p1` of 41 s and a second `p1s5` of 50 s in the shipped logs). The 11 s spread between the two Linux `p1s25` runs shows how much one run can differ from another here.
- The `p1s25` recovery is at 51-62 s after X stops dialing P. I did not trace the relay actor in this run, so I cannot say whether the 60 s idle exit is the release; the `Inactive, exiting` trace lines are in `reports/linux-e14w.md` for the gossip harness only.
- Different machine in every respect at once (x86_64 VM against Apple M2 Max; Linux 6.8 against macOS 15), same pinned iroh from the same lock file; I did not diff the lock file between the two hosts' builds.
- Debug build, loopback, one host; load averages were 0.00-0.49 at the start of each run except ctl-1 (1.46, post-build), and resident-anarchist's SSH work could have overlapped without raising them.
- The logs were captured with `2>&1`, as noted; this cannot add lines to the SUMMARY comparison.

## Files

- Report: `/home/lab/work/reports/linux-e14.md`
- Raw: `/home/lab/work/reports/raw/linux-e14/` (`logs/*.txt`, `uptime.txt`, `exits.txt`, `run.sh`, `pgrep-after.txt`) and `reports/raw/linux-e14-build.txt`
