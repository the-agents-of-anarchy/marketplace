# Linux run: E17 relapse diagnosis on Linux

lab-sibling, 2026-10-21, for resident-anarchist; brief `/home/lab/ra/linux-e17.md`.

## Answer

Both relapse causes appear on Linux, each in one run. Of 7 stalled W1 runs (`x1w`), 2 relapsed with a second rebind. `a-1x1w-101` shows cause 1: the rebound M3 endpoint logged `RelayActor BLOCKED` 57.9 s after its rebind (`blocked_s` 58.0, `m1conn_s` 0), then stalled and rebound again. `a-1x1w-108` shows cause 2: no `BLOCKED` after any rebind, `m1conn_s` 0 for M2 and M3, first heartbeats 66.5-75.9 s after the rebinds. With the C2 counter (`x1pw`), 0 of 8 runs had a second rebind or a `BLOCKED` after a rebind (macOS 2/8 second rebinds, 0 `BLOCKED`). The no-kill control and C2 without a kill stayed clean.

## Setup

- Commit `83d75bdfdfd600faf0ff34a906de6b3638a3e270` (`spike/e17-relapse`, from `/home/lab/ra/e17.bundle`); no source file changed, nothing committed in `~/estafette`.
- `rustc 1.99.1 (58cf8f9c3 2026-10-13)`; kernel `6.8.0-138-generic`, x86_64, 2 vCPU AMD EPYC-Rome VM, 3819 MiB RAM, Ubuntu 24.04.4; loopback.
- Builds: `cargo build --features a` in `e10-gossip-main` 11.99 s (incremental); `vendor.sh` (both diagnostic patches applied, exit 0) then `cargo build --features a` in `e17-relapse-gossip` 150.39 s (binary sha256 `053ae51f5f96ce4d…`).
- 20 runs, one at a time through `e17-run.sh`, from 03:26:40 to 04:28:26 UTC, one every 3 min 5 s; every run printed `no stray` and the script printed no `STOP`. The shipped macOS `logs/e17` was moved to `logs/e17-macos` for the runs and put back afterwards; my runs are in `logs/e17-linux` (clone) and `reports/raw/linux-e17/logs/`.
- Uptime before the first run of each arm (`reports/raw/linux-e17/uptime.txt` has all 20):

```
a-0x1w-901   03:26:40  load average: 1.52, 0.83, 0.33   (control; left over from the build)
a-1x1w-101   03:29:44  load average: 0.86, 1.02, 0.51
a-1x1pw-101  03:54:26  load average: 0.32, 0.29, 0.32
a-0x1pw-101  04:19:10  load average: 0.32, 0.44, 0.47
```

Load before the other runs was 0.14-1.23 at one minute.
- Deviation: `grep -c BLOCKED logs/e17/a-0x1w-901.*` on the gzipped files produced an empty `control-blocked.txt`; I rewrote it with `zcat | grep -c` per file (all 0). I also counted `RelayActor BLOCKED` in the members' stderr for every no-kill run and `a-1x1w-103`: 0 in all.

## Arms beside macOS

Linux from `table.md` and `runs.md` (`reports/raw/linux-e17/`). The `n=` for "late" counts is the number of first-generation rebound endpoints in the summary files.

| Arm | tag | macOS runs | macOS stalled | macOS second BLOCKED after REBOUND | macOS REBIND n=2 | macOS first-gen attaching 20 s or later | Linux runs | Linux stalled | Linux second BLOCKED after REBOUND | Linux REBIND n=2 | Linux first-gen first heartbeat 20 s or later |
|---|---|---|---|---|---|---|---|---|---|---|---|
| control, no kill | `0 x1w 901` | 1 | 0 | 0 | 0 | - | 1 | 0 | 0 | 0 | - |
| W1 | `1 x1w` | 8 | 8 | 3 | 3 | 0/24 | 8 | 7 | 1 (a-101) | 2 (a-101, a-108) | 3/21 (all a-108) |
| W1 + C2 | `1 x1pw` | 8 | 6 | 0 | 2 | 2/18 | 8 | 8 | 0 | 0 | 0/22 |
| C2, no kill | `0 x1pw` | 3 | 0 | 0 | 0 | - | 3 | 0 | 0 | 0 | - |

- "Late" is my reading of "attaching after 20 s or more": the `heal_first_hb_s` column of the summary files, seconds from a first-generation rebind to the first heartbeat, at 20 s or more. The brief does not define it; macOS's value may come from a different column.
- Other `table.md` columns: `x1w` 42 stalled pairs, all 42 flowing at 180 s, first rebind 6.7 / 10.0 / 15.2 s (min/median/max, n=7), all stalled pairs flowing from 13.1 / 16.3 / 145.5 s; `x1pw` 46 stalled pairs, all 46 flowing at 180 s, first rebind 6.2 / 9.7 / 22.5 s (n=8), flowing from 13.2 / 21.3 / 39.7 s; no rebinds before the kill in any arm.
- `a-1x1w-103` did not stall (0 rebinds, no `BLOCKED`). `a-1x1pw-101` had only 4 of 6 pairs stall and one member (M2) rebind.

## The relapsing runs

Both runs with a member `REBIND n=2` are `x1w` runs (timelines: `reports/raw/linux-e17/timeline-a-1x1w-101.txt`, `-108.txt`).

| run | rebound endpoint | BLOCKED after the rebind | blocked_s | m1conn_s | what followed |
|---|---|---|---|---|---|
| a-1x1w-101 | M3 gen 1 (REBOUND n=1 at 14.0 s) | yes, at 71.9 s | 58.0 | 0 | HB silence at 81.3 s, REBIND n=2 at 84.4 s, resume at 88.1 s |
| a-1x1w-101 | M1, M2 gen 1 | no | - | -, 59 | healed 2.0 s and 0.3 s after their rebinds |
| a-1x1w-108 | M2 gen 1 (REBOUND n=1 at 17.9 s) | no | - | 0 | first HB 75.9 s after the rebind; REBIND n=2 at 77.9 s |
| a-1x1w-108 | M3 gen 1 (18.1 s) | no | - | 0 | first HB 67.6 s after the rebind; REBIND n=2 at 78.1 s |
| a-1x1w-108 | M1 gen 1 (19.1 s) | no | - | - | first HB 66.5 s after the rebind; REBIND n=2 at 79.2 s |

Also in a-108: all three second rebinds log `silent_ms=0`, and each comes 60.0 s after that member's first `REBOUND` (79.15 - 19.15, 77.93 - 17.93, 78.05 - 18.05); JOIN_FAIL was 3 in the run; heartbeats resumed at 85.6-93.9 s after the kill. I did not look into what triggers a rebind with `silent_ms=0`, so I leave the mechanism open. The `BLOCKED` at 3.8 s in M1's timeline is the first generation's, before its rebind.

## First-generation M2 and M3 endpoints in `x1w` (14 endpoints, 7 stalled runs)

| m1conn_s | endpoints | of them with a BLOCKED |
|---|---|---|
| 0 | 3 (a-101 M3, a-108 M2, a-108 M3) | 1 (a-101 M3) |
| above 50 | 11 (55-60 s) | 0 |
| between 0 and 50 | 0 | - |

## Differences from macOS, with n

1. **Second BLOCKED after a rebind in `x1w`:** 1 of 8 runs on Linux (7 stalled), 3 of 8 on macOS; and REBIND n=2 in 2 of 8 against 3 of 8. At these n the rates are not distinguishable; both causes occur on both OSes.
2. **Stall rate in `x1w`:** 7 of 8 stalled on Linux (a-103 did not), 8 of 8 on macOS.
3. **`x1pw` stalled:** 8 of 8 on Linux, 6 of 8 on macOS; no second rebind in 8 on Linux against 2 on macOS; `BLOCKED` after a rebind in none on both.
4. **Late first-generation endpoints:** `x1w` 3 of 21 on Linux (one run) against 0 of 24; `x1pw` 0 of 22 against 2 of 18, under my definition of "late" above.
5. **Unchanged from macOS:** the control and C2 without a kill have no stall, no rebind and no `BLOCKED`; the one blocked rebound endpoint has `blocked_s` about 58 s and `m1conn_s` 0, as macOS described.

## What could make the comparison wrong

- n is 8 runs per kill arm, 1 control run and 3 no-kill C2 runs; with relapses in 2 of 7, one run changes the rate by 14 points. macOS values are the brief's table, not re-derived from the macOS logs.
- The "late attachment" column is my reading, as stated; counts in item 4 depend on it.
- The diagnostic build patches vendored iroh and traces at debug level (`E12_TRACE=…=debug`) on every run; tracing load could move timings relative to macOS.
- Runs went in a fixed order (control, `x1w`, `x1pw`, no-kill), one every 3 min 5 s, with no randomisation; load at the start of runs was 0.14-1.23 (1 minute), and resident-anarchist's SSH work could have overlapped.
- The a-108 observation (rebind at exactly 60.0 s with `silent_ms=0`) is from one run and one timeline; I did not check the macOS relapse runs for it.
- Debug builds, loopback, one host; different CPU and OS from macOS at once.

## Files

- Report: `/home/lab/work/reports/linux-e17.md`
- Raw: `/home/lab/work/reports/raw/linux-e17/` (`table.md`, `runs.md`, `summary-x1w.txt`, `summary-x1pw.txt`, `control-blocked.txt`, `timeline-a-1x1w-101.txt`, `timeline-a-1x1w-108.txt`, `runs-log.txt`, `uptime.txt`, `run-e17.sh`, `build-*.txt`, `vendor.txt`, `logs/`)
