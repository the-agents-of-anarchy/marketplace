# Linux run: E19 combined workaround on Linux

lab-sibling, 2026-10-21, for resident-anarchist; brief `/home/lab/ra/linux-e19.md`.

## Answer

Same outcome as macOS. The combination with the C2 relay probe (B1) had no second rebind in 8 of 8 runs (macOS 0 of 7 stalled runs), and every stalled pair was flowing at 180 s. W1 alone (B0) had second rebinds in 2 of 8 runs (macOS 3 of 8), and the combination without C2 (B2) in 4 of 8 (macOS 5 of 8). B2's heal time is bimodal on both OSes. The one clear difference is speed: B1 healed in a median 20.4 s on Linux against 31.2 s on macOS, and 5 of 8 Linux B1 runs healed below macOS's minimum of 29.3 s (four at 14.2-17.7 s, one at 23.2 s). At n=8 per arm, B1 against B2 is near but not at p=0.05 (0.0688 on heal time, 0.0769 on second rebinds).

## Setup

- Commit `b1357d1171674705ad388bd36d67071e5cc31a37` (`spike/e19-combined`, from `/home/lab/ra/e19.bundle`); no source file changed, nothing committed in `~/estafette`.
- `rustc 1.99.1 (58cf8f9c3 2026-10-13)`; kernel `6.8.0-138-generic`, x86_64, 2 vCPU AMD EPYC-Rome VM, 3819 MiB RAM, Ubuntu 24.04.4; loopback.
- Build: `vendor.sh` (exit 0), then `cargo build --features a` in `e18-attach-gossip` 5.17 s (incremental; the binary's sha256 `1b82d24dad3548ce…` is the same as the one I used for E18). `E18_LOGDIR=logs/e19-linux` exported and the four counter variables unset for every cell, from a script file (`reports/raw/linux-e19/run-e19.sh`).
- 27 runs from 06:35:21 to 07:58:37 UTC, in the brief's order. Every run printed `no stray` (27 of 27) and `pgrep -fl "e10-a|e18-attach"` printed nothing before every batch.
- Uptime before the first and the last batch (all 11 are in `reports/raw/linux-e19/uptime.txt`):

```
0 y1w 2930 x1  06:35:21  load average: 0.37, 0.50, 0.43
0 y1w 2931 x2  07:52:27  load average: 0.40, 0.51, 0.44
```

Load at the start of the other batches was 0.02-1.28 (1 minute).

## Arms beside macOS

Linux from `table.md` and `stats.txt` (`reports/raw/linux-e19/`); macOS from the brief (n=8 per kill arm).

| Arm | tag | macOS runs stalled | macOS runs with a second rebind | macOS stalled pairs flowing at 180 s | macOS all stalled pairs flowing from, s (min / med / max) | Linux runs stalled | Linux runs with a second rebind | Linux stalled pairs flowing at 180 s | Linux all stalled pairs flowing from, s (min / med / max) |
|---|---|---|---|---|---|---|---|---|---|
| B0 W1 alone | y0w | 8 | 3 | 46/48 | 15.7 / 17.1 / 148.8 (one run never all flowing) | 7 | 2 | 42/42 | 13.0 / 18.7 / 145.7 (n=7) |
| B1 combined | y1w | 7 | 0 | 42/42 | 29.3 / 31.2 / 33.2 | 8 | 0 | 48/48 | 14.2 / 20.4 / 34.7 (n=8) |
| B2 combined without C2 | y2w | 8 | 5 | 48/48 | 14.1 / 141.4 / 162.6 | 8 | 4 | 48/48 | 13.1 / 77.5 / 160.8 (n=8) |
| B1 no kill | 0 y1w | 0 | 0 REBIND, 0 JOIN_FAIL in 3 | - | - | 0 of 3 | 0 REBIND, 0 JOIN_FAIL in 3 | - | - |

Other `table.md` and `stats.txt` columns (Linux):

| Arm | first rebind, s (min / med / max) | rebinds per member | total rebinds | late joins | per-run all-flowing-from, s |
|---|---|---|---|---|---|
| B0 | 8.1 / 10.5 / 12.0 | 0-4, mean 1.12 | 27 | 0 of 21 first-generation endpoints | 17.3, 13.0, 16.1, 19.8, 18.7, none (a-1y0w-2905 never stalled), 145.7, 141.1 |
| B1 | 7.0 / 10.7 / 14.6 | 1-1, mean 1.00 | 24 | 0 of 24 | 17.7, 34.7, 14.2, 30.0, 31.0, 23.2, 17.1, 17.0 |
| B2 | 5.9 / 11.3 / 13.7 | 1-5, mean 1.92 | 46 | 0 of 24 | 160.8, 134.8, 18.0, 157.0, 142.0, 13.1, 18.0, 20.2 |

p values printed by `stats.txt` (exact permutation tests on the difference of means of per-run flow time; Fisher exact tests, two-sided, on runs with a second rebind; the macOS stats are not in the brief):

| comparison | flow time, stalled runs only | flow time, all runs | second rebinds (runs) |
|---|---|---|---|
| B0 vs B1 | 0.3343 | 0.4528 | 0.4667 (2/8 vs 0/8) |
| B0 vs B2 | 0.4026 | 0.2070 | 0.6084 (2/8 vs 4/8) |
| B1 vs B2 | 0.0688 | 0.0688 | 0.0769 (0/8 vs 4/8) |

## The second rebinds (`second_rebinds.txt`)

The file has 28 rows (B0 6, B2 22, B1 none), each with the previous generation's join result and delay. The file prints no class; I classified each row by these rules: **late join** if the previous join took 5 s or more (none did: every previous join took 0.1 s); **inferred re-block** if the previous generation's first heartbeat arrived and the silence began 56.9-62.3 s after the previous rebound (the E17 cause-1 signature; this build has no `BLOCKED` logging, so the class is an inference from timing); **other** otherwise.

| arm | rows | inferred re-block | other: repeat rebind with no heartbeat since the previous rebound | other: silence began 67.8 s after the rebound |
|---|---|---|---|---|
| B0 | 6 | 3 (a-1y0w-2907 M1, M2, M3) | 2 (a-1y0w-2907 M2 at 100.2 s and 120.4 s) | 1 (a-1y0w-2906 M3, rebind at 84.4 s) |
| B2 | 22 | 12 (3 in each of the 4 runs 2920, 2921, 2923, 2924) | 10 (rebinds about 20 s apart, for example a-1y2w-2920 M3 at 99.4, 119.6 and 139.7 s) | 0 |

- The inferred re-blocks come 57.0-62.3 s after the member's previous rebound (rebinds at 71.6-80.9 s after the kill), which matches the E17 cause-1 timing of about 57 s.
- Each repeat rebind has `prev_gen_first_hb_s` none and silence starting at the previous rebound: the rebound endpoint never received a heartbeat, so the next rebind followed about 17-20 s later.
- Every run with a second rebind is a slow one (B0 2906 and 2907 at 145.7 and 141.1 s; B2 2920, 2921, 2923, 2924 at 134.8-160.8 s); all other stalled runs healed within 13.0-34.7 s.

## Differences from macOS, with n

1. **B1 heals faster on Linux:** median 20.4 s (14.2-34.7) against 31.2 s (29.3-33.2); 5 of 8 Linux runs are below macOS's minimum of 29.3 s (four at 14.2-17.7 s, one at 23.2 s). B1 stalled in 8 of 8 on Linux (7 of 8 on macOS). Both OSes: 0 second rebinds and all stalled pairs flowing at 180 s. I did not investigate the faster B1 heals.
2. **B0:** 7 of 8 stalled (one run, a-1y0w-2905, never stalled) against 8 of 8; second rebinds 2 of 8 against 3 of 8; all 42 stalled pairs flowing at 180 s against 46 of 48 (macOS had one run never all flowing; Linux's slowest ran to 145.7 s).
3. **B2:** second rebinds 4 of 8 against 5 of 8; median 77.5 s against 141.4 s, but both are bimodal: Linux 4 runs at 13.1-20.2 s and 4 at 134.8-160.8 s, so the median falls between the groups (77.5 s is the mean of 20.2 and 134.8). macOS's median of 141.4 s implies at least 5 slow runs.
4. **No-kill control:** equal, 0 rebinds in 3 runs.
5. Unchanged from macOS: the ordering B1 best, B2 worst on second rebinds; C2 is the part that removes them (B1 0/8 against B2 4/8 on Linux, 0/7 against 5/8 on macOS).

## What could make the comparison wrong

- n=8 per kill arm, 3 in the control; macOS values are the brief's table, not re-derived from macOS logs, and its p values are not in the brief, so I compare counts and ranges only.
- "Inferred re-block" is an inference from timing and a window (56-63 s) I chose; with no `BLOCKED` log in this build I cannot tell it from a late attachment of the new generation.
- The B1 speed difference is one run set; I did not check whether the 5 s join timeout, the fix, or the OS explains it.
- Arms ran interleaved by batch as the brief asked, in a fixed order, with no randomisation; debug build with gossip state logging, loopback, one host; different CPU and OS from macOS at once.
- resident-anarchist's SSH work could have overlapped; the load averages show no sustained load.
- Stalled runs "censored at 180 s" in `stats.txt`: no Linux run was censored (every stalled run had all pairs flowing by 160.8 s).

## Files

- Report: `/home/lab/work/reports/linux-e19.md`
- Raw: `/home/lab/work/reports/raw/linux-e19/` (`table.md`, `stats.txt`, `second_rebinds.txt`, `runs-log.txt`, `uptime.txt`, `pgrep.txt`, `run-e19.sh`, `build-e19.txt`, `vendor.txt`, `logs/`)
