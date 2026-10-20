# Linux 180 s cells: a-1w and a-1npw (E14's 60 s release test)

lab-sibling, 2026-10-20, for resident-anarchist; ask at 2026-10-20T23:58+0300.

## Answer

The 60 s idle exit happens on Linux, and fresh dials recover right after it, but gossip heartbeats never resume in 180 s. In the traced a-1w-101 run, each member's dead-relay actor logged `Inactive, exiting. RELAY_INACTIVE_CLEANUP_TIME=60s` at 61.1 s (M2), 76.5 s (M3) and 79.6 s (M1) after the kill. Each pair's first successful fresh dial came 0.1-2.4 s after the later of its two members' exits. M1 exited a second time at 145.9 s, and its pairs recovered at 146-148 s. Heartbeats: 0/16 pairs flowing again at window end across the four probers-on runs.

This corrects my first reading in `reports/linux-dial-after-60s.md`: no fresh dial succeeded after 60 s in 88 s windows on Linux, but with 180 s windows the first success after 60 s is at 74-87 s in all four runs, so the 88 s window ended just as the release began (see "What this changes" below).

## Setup

- Same machine and toolchain as `reports/linux-e12.md`: Linux 6.8.0-138 on a 2 vCPU AMD EPYC-Rome VM, Ubuntu 24.04.4, rustc 1.99.1; loopback.
- Branch `spike/e12-rejoin` d4b4ca0, debug build `--features a` (`target/bin/e10-a`, sha256 `568f8429bbbf3d25…`). The tags `w` and `npw` set no `E12_*` variable, so L1 and L2 are off.
- Cells, as asked: `./run-cell.sh a 1 w 3` and `./run-cell.sh a 1 npw 3`, then (my addition) one traced run per cell with run number 101: `E12_TRACE="iroh=debug,iroh_relay=debug,iroh_gossip=info" ./run-cell.sh a 1 <w|npw> 1 101`. The n=3 cells are untraced.
- Run script and raw outputs: `reports/raw/linux-e14w/` (`run.sh`, `cells.txt`, `cell-*.txt`, `diag-*.txt`, traces in `diag-w/` and `diag-npw/`, analysis in `analyze.txt` and `runs.txt`). Run logs: `reports/raw/linux-e14w/logs/`.

| run | command | start (UTC) | load avg (1/5/15) at start | wall |
|---|---|---|---|---|
| a-1w-1..3 | `a 1 w 3` | 20:54:00 | 0.16 0.18 0.09 | 554.45 s |
| a-1npw-1..3 | `a 1 npw 3` | 21:03:14 | 0.23 0.15 0.10 | 554.55 s |
| a-1w-101 (traced) | `a 1 w 1 101` | 21:12:29 | 0.02 0.06 0.08 | 184.98 s |
| a-1npw-101 (traced) | `a 1 npw 1 101` | 21:15:34 | 0.48 0.24 0.14 | 184.56 s |

All exited 0. `analyze.py --table` pools run 101 with the n=3 cells (its groups read `a-1w-\d+`, so n=4); the numbers below separate them, from `runs.txt`.

## Heartbeats (n=3 untraced, then traced run 101)

| run | M1 re-home s | M2-M3 longest gap s | M2-M3 flowing again | M1 pairs stalled | M1 pairs flowing again |
|---|---|---|---|---|---|
| a-1w-1 | 38.5 | 169.3 | no | 4/4 | 0/4 |
| a-1w-2 | 41.1 | 170.1 | no | 4/4 | 0/4 |
| a-1w-3 | 44.7 | 173.3 | no | 4/4 | 0/4 |
| a-1w-101 | 42.8 | 170.1 | no | 4/4 | 0/4 |
| a-1npw-1 | 46.4 | 173.1 | no | 4/4 | 0/4 |
| a-1npw-2 | 41.4 | 174.0 | no | 4/4 | 0/4 |
| a-1npw-3 | 40.2 | 176.1 | no | 4/4 | 0/4 |
| a-1npw-101 | 45.8 | 1.1 | n/a (not stalled) | 0/4 | 0/0 |

- a-1w: M2-M3 stalled 3/3 (4/4 with the traced run); no HB resumed in 180 s (0/12 M1 pairs, 0/16 with the traced run).
- a-1npw: M2-M3 stalled 3/3 untraced; the traced run did not stall (gap 1.1 s). No stalled pair resumed.
- macOS 180 s reference (E10, variant A): probers on, 2/2 stalled, none healed, gap 154-176 s; probers off, 1/3 stalled, none healed. Linux probers-on matches. Linux probers-off stalled 3/3 against 1/3 on macOS; with n=3 each this is within the spread E10 showed (probers-off stall rates of 2/3 on both OSes at 88 s).

## Fresh dials, probers on (`w`)

Dial recovery from `analyze.py`, in seconds after the kill (macOS from `logs-macos/results-table.md`):

| measure | Linux a-1w-1 / -2 / -3 / -101 | macOS (n=2) |
|---|---|---|
| fresh dial by id to M1 ok again (earlier of M2, M3) | 164.0 / 74.3 / 152.8 / 148.3 | 85.1 / 156.1 (median 120.6) |
| fresh dial M2-M3 ok again (either direction) | Linux min 76.6, median 80.3, max 87.3 (n=4) | 79.0 / 158.0 (median 118.5) |

The first successful probe at or after 60 s: 76, 78, 74 and 87 s after the kill (a-1w-101, -1, -2, -3). From then on probes mostly succeed: successful probes past 60 s numbered 334, 263, 395 and 156 (a-1w-101, -1, -2, -3), of which 287, 219, 303 and 154 came after 100 s; failures past 60 s were 95, 113, 82 and 140 (counted by my own `awk` over PROBE records; the same filter as in the earlier report).

## Traced runs: `Inactive, exiting` and `Dropped datagram(s)`

Times are seconds after the kill, from the trace timestamps against the KILL record (a-1w-101 killed 21:12:34.233Z, a-1npw-101 killed 21:15:38.802Z). Every line carries `RELAY_INACTIVE_CLEANUP_TIME=60s` and names the dead relay (`http://127.0.0.1:35675/` in w, `:37629/` in npw).

| run | member | `Inactive, exiting` | `Dropped datagram(s): ActiveRelayActor closed` |
|---|---|---|---|
| a-1w-101 | M2 | 61.1 | 61.1 |
| a-1w-101 | M3 | 76.5 | 76.5 |
| a-1w-101 | M1 | 79.6, 145.9 | 79.6, 145.9 |
| a-1npw-101 | M1 | 64.4 | none |
| a-1npw-101 | M2 | 66.3 | none |
| a-1npw-101 | M3 | 79.4 | none |

The exits fall 61-80 s after the kill, not at 60.0 s, so some sends to the dead relay reset the idle clock; with probers off the exits are at 64-79 s. `Dropped datagram(s)` appears with the exit only when probers are on (2 lines in M1's w trace, one per exit; 1 each in M2 and M3). In the npw trace no member logged a drop.

Per-pair first success after the kill, past 20 s (a-1w-101 PROBE records), beside the exits:

| pair (dialer>target) | first ok after 20 s | later of the two members' exits | gap |
|---|---|---|---|
| M3>M2 | 76.6 | 76.5 (M3) | +0.1 |
| M2>M3 | 78.3 | 76.5 (M3) | +1.8 |
| M1>M2 | 146.1 | 145.9 (M1, second) | +0.2 |
| M1>M3 | 146.0 | 145.9 (M1, second) | +0.1 |
| M2>M1 | 148.3 | 145.9 (M1, second) | +2.4 |
| M3>M1 | 148.3 | 145.9 (M1, second) | +2.4 |

Before the kill-side stall, every pair's last success before 20 s was at 6.9-9.2 s.

## What this changes in `reports/linux-dial-after-60s.md`

- In 88 s windows, six Linux runs (E10 a-1, E12 a-1l12) had 0 dial successes after 60 s. Here the first success after 60 s is at 74-87 s in four of four runs. The 88 s window leaves 1-14 s after those times, so zero successes in six runs is plausible but not guaranteed by this alone: it needs the release to fall late in each of them. I cannot rule out that Linux releases a little later than macOS on average (macOS first late successes there were 63.9, 76.5 and 85.1 s, and 10.0 s in a-1l12-5); the Linux times 74-87 s sit at the upper end of that spread.
- The retraction: "on Linux no release shows within the 88 s window" is true for those runs but is a window effect, not a Linux-specific failure to release.

## Differences from macOS (180 s)

1. Probers off stalled 3/3 on Linux against 1/3 on macOS; n=3 each, one macOS run did not stall and one Linux traced run did not stall (a-1npw-101, gap 1.1 s).
2. Heartbeats never resumed on either OS in 180 s for stalled pairs, even after the dead relay's actor exited and fresh dials succeeded. The Linux data show this directly: dials to every pair succeeded after 76-148 s, yet 0/16 pairs had heartbeats at the window end.
3. Dial recovery times overlap macOS (Linux 74-164 s, macOS 79-158 s).

## What could make the comparison wrong

- Tracing at `iroh=debug,iroh_relay=debug,iroh_gossip=info` slows the member and adds disk writes; the traced runs are one per cell and the a-1npw-101 run behaved differently from its three untraced siblings (no stall). I use it only for the log lines and the exit times, not for rates.
- The exit times include only what each member's own trace shows. I did not read the relay server's side.
- The exit times are one traced run per cell (n=1); the 61-80 s spread comes from three members of one run, not repeated runs. The `Inactive` clock may reset on any send, so I can't say that 60 s plus a fixed delay predicts it.
- The "later of the two exits" alignment is six pairs in one run, found after looking at the data, not a prediction I made first. A different rule, the dialer's own exit alone, fits three of the six rows (M3>M2, M1>M2, M1>M3) and misses M2>M3, M2>M1 and M3>M1.
- Dial counts come from my own `awk` over the raw logs, applied to both OSes in the earlier report; the macOS 180 s figures here come from `logs-macos/results-table.md` (n=2 probers-on).
- n=3 untraced runs per cell; every count is out of 3 or 4. Load was 0.02-0.48 at the starts; the debug build and loopback are as in E10.
- resident-anarchist's SSH work could have overlapped; the load averages show no sustained load.
