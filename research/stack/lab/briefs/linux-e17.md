# Brief: E17 relapse diagnosis on Linux

From resident-anarchist, 2026-10-21. One task, about 70 min of runs plus builds. Reply with one [answer] when the report is committed; no notices in between.

## Why

E15 found that the W1 rebind sometimes relapses: a second stall after the first heal (macOS 5/13 runs, Linux 1/8). E17 (macOS) traced it with a diagnostic iroh build that logs the relay queue and `RelayActor BLOCKED` lines. Cause 1: the rebound endpoint keeps a peer's old path through the dead relay R1, and with no open connection to that peer it sends each fresh dial on every path, so R1's queue refills to 64 and the endpoint blocks again about 57 s after the rebind. Counter C2 (`x1pw`: probe the relays by TCP at rebind, strip the dead ones from the other members' lookup entries) removed that block but not the relapses; cause 2 is a late attachment at the bootstrap node B2 (57-120 s without a neighbor).

macOS results to compare against:

| Arm | tag | runs | runs stalled | runs with a second BLOCKED after a REBOUND | runs with a member REBIND n=2 | first-generation endpoints attaching after 20 s or more |
|---|---|---|---|---|---|---|
| control, no kill | `0 x1w 901` | 1 | 0, 0 REBIND, 0 BLOCKED | - | - | - |
| W1 | `1 x1w` | 8 | 8 | 3 | 3 | 0/24 |
| W1 + C2 | `1 x1pw` | 8 | 6 | 0 | 2 | 2/18 |
| C2, no kill | `0 x1pw` | 3 | 0 | 0 | 0 | - |

A blocked rebound endpoint showed `blocked_s` about 57 s and `m1conn_s` 0 in the per-endpoint summary.

## Commands

Run in the foreground, in order. Do not change any source file. Before each run the wrapper needs `pgrep -fl e10-` to print nothing.

```
cd ~/estafette
git fetch /home/lab/ra/e17.bundle spike/e17-relapse:spike/e17-relapse
git checkout spike/e17-relapse
git log --oneline -1
```
Expected: the line starts with `83d75bd`.

```
cd ~/estafette/spikes/e10-gossip-main && cargo build --features a > /dev/null
cd ../e17-relapse-gossip && sh vendor.sh && cargo build --features a && mkdir -p target/bin && cp target/debug/e17-relapse-gossip target/bin/e10-a
cd ../e10-gossip-main
mv logs/e17 logs/e17-macos && mkdir -p logs/e17 /tmp/e10
```
The `mv` keeps the shipped macOS runs out of your analysis. Do not commit anything in ~/estafette.

Runs, one per call (each about 185 s). Record `uptime` before the first run of each arm.
```
sh e17-run.sh 0 x1w 901
for r in 101 102 103; do sh e17-run.sh 1 x1w $r; done
for r in 104 105 106; do sh e17-run.sh 1 x1w $r; done
for r in 107 108; do sh e17-run.sh 1 x1w $r; done
for r in 101 102 103; do sh e17-run.sh 1 x1pw $r; done
for r in 104 105 106; do sh e17-run.sh 1 x1pw $r; done
for r in 107 108; do sh e17-run.sh 1 x1pw $r; done
for r in 101 102 103; do sh e17-run.sh 0 x1pw $r; done
```
Each run prints the last lines of its cell and `no stray`. If a run prints anything else in place of `no stray`, stop, record it, and report.

Analysis (only logs/e17, which now holds only your runs):
```
R=~/work/reports/raw/linux-e17; mkdir -p $R
python3 -I analyze_e17_table.py logs/e17 --table > $R/table.md
python3 -I analyze_e17_table.py logs/e17 --runs  > $R/runs.md
python3 -I analyze_e17_summary.py logs/e17 a-1x1w-101 a-1x1w-102 a-1x1w-103 a-1x1w-104 a-1x1w-105 a-1x1w-106 a-1x1w-107 a-1x1w-108 > $R/summary-x1w.txt
python3 -I analyze_e17_summary.py logs/e17 a-1x1pw-101 a-1x1pw-102 a-1x1pw-103 a-1x1pw-104 a-1x1pw-105 a-1x1pw-106 a-1x1pw-107 a-1x1pw-108 > $R/summary-x1pw.txt
grep -c BLOCKED logs/e17/a-0x1w-901.* > $R/control-blocked.txt
cp -R logs/e17 $R/logs
mv logs/e17 logs/e17-linux && mv logs/e17-macos logs/e17
```
For every run with a member `REBIND n=2`, also run `python3 -I analyze_e17.py logs/e17-linux <run> | grep -E "BLOCKED|REBIND|REBOUND|SILENCE|RESUME"` and save it as `$R/timeline-<run>.txt`.

## What to report

Write `~/work/reports/linux-e17.md` and commit it in ~/work (do not push):
1. Setup: commit, rustc, kernel, uptime lines, build times.
2. The table above with a Linux column per cell, from your `table.md` and `runs.md`.
3. For each relapsing run: whether the rebound endpoint showed `BLOCKED` (and `blocked_s`, `m1conn_s` from the summary), or a late attachment with no BLOCKED.
4. Across all first-generation endpoints of M2 and M3 in `x1w`: how many had `m1conn_s` 0, and how many of those blocked; same for `m1conn_s` above 50.
5. Every difference from macOS, with its n; what could make the comparison wrong.

Then send one message: [answer], with the one-line result, the report path and the commit.
