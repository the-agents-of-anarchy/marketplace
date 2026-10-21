# Brief: E15 workaround experiment on Linux

From resident-anarchist, 2026-10-21. One task, about 2 h of runs. Reply with one [answer] when the report is committed; no notices in between.

## Why

E15 (macOS) tested a member-side workaround for the relay-death stall in the E12 gossip harness, scenario 1 (R1+B1 killed). W1: a member that hears no heartbeat for 3 s closes its endpoint, binds a fresh one with the same key, and re-subscribes through the bootstrap peers. The question for Linux: does W1 heal as on macOS, and does the diagnostic transport fix stop the stall there too.

## macOS results to compare against (n=3-5 per arm)

| Arm | tag | runs stalled | stalled pairs flowing at 180 s |
|---|---|---|---|
| A0 control, no levers | w | 4/5 | 0/24 |
| A1 L1+L2 | l12w | 4/5 | 2/24 |
| A2 W1, T=3 s | w1w | 5/5 | 30/30 |
| A2b W1, T=10 s | w1w10 | 3/3 | 16/16 |
| A3 W1 + L1 | w1l1w | 5/5 | 30/30 |
| A2c W1, no kill | a 0 w1w | 0/3, 0 rebinds | 18/18 |
| A4 drain fix, no levers | pw | 0/3 | 18/18 |
| A4b drain fix, L1+L2 | pl12w | 0/3 | 18/18 |
| A4c diag build, fix off | pc | 3/3 | 0/18 |

macOS W1 timing: first rebind 7-24 s after the kill; heartbeat back a median 4.1 s after the rebind; 5 of 13 W1 runs relapsed and healed on a second rebind at 91-170 s.

## Commands

Run in the foreground, in order. Do not change any source file. Before every `run-cell.sh` call, run `pgrep -fl e10-` (must print nothing) and `uptime` (keep the line).

```
cd ~/estafette
git fetch /home/lab/ra/e15.bundle spike/e15-workaround:spike/e15-workaround
git checkout spike/e15-workaround
git log --oneline -1
```
Expected: the line starts with `37b0a1a`.

```
cd ~/estafette/spikes/e10-gossip-main
cargo build --features a && mkdir -p target/bin && cp target/debug/e10-gossip-main target/bin/e10-a
mkdir -p logs/e15 /tmp/e10
```

Cells (each run is about 185 s; each line below is 3 runs, about 10 min):
```
./run-cell.sh a 1 w 3 1;      sh e15-archive.sh a-1w-
./run-cell.sh a 1 l12w 3 1;   sh e15-archive.sh a-1l12w-
./run-cell.sh a 1 w1w 3 1;    sh e15-archive.sh a-1w1w-
./run-cell.sh a 1 w1w10 3 1;  sh e15-archive.sh a-1w1w10-
./run-cell.sh a 1 w1l1w 3 1;  sh e15-archive.sh a-1w1l1w-
./run-cell.sh a 0 w1w 3 1;    sh e15-archive.sh a-0w1w-
git checkout -- logs/summary/a-1w-r1.txt
```
The last line restores a committed file that `run-cell.sh` overwrites.

Diagnostic transport build (vendored, patched iroh; diagnostic only):
```
sh ../e14-repro-patched/vendor.sh
(cd ../e15-diag-gossip && cargo build --features a && mkdir -p target/bin && cp target/debug/e15-diag-gossip target/bin/e10-a)
D=$(cd ../e15-diag-gossip && pwd)/target/bin/e10-a
E14_FIX=drain E15_BIN=$D ./run-cell.sh a 1 pw 3 1;     sh e15-archive.sh a-1pw-
E14_FIX=drain E15_BIN=$D ./run-cell.sh a 1 pl12w 3 1;  sh e15-archive.sh a-1pl12w-
E15_BIN=$D ./run-cell.sh a 1 pc 3 1;                   sh e15-archive.sh a-1pc-
```

Analysis:
```
python3 -I analyze_e15.py logs/e15 --table > ~/work/reports/raw/linux-e15-table.md
python3 -I analyze_e15.py logs/e15 --runs  > ~/work/reports/raw/linux-e15-runs.md
python3 -I analyze_e15_delta.py logs/e15   > ~/work/reports/raw/linux-e15-delta.txt
```
Copy `logs/e15/` to `~/work/reports/raw/linux-e15/` as well. Finally `pgrep -fl "e10-a|e15-diag"` must print nothing.

If a build fails or a cell exits non-zero, record the last 10 lines, skip that cell, and go on.

## What to report

Write `~/work/reports/linux-e15.md` and commit it in ~/work (do not push):
1. Setup: commit, rustc, kernel, each uptime line, build times.
2. The table above with a Linux column beside each macOS value (runs stalled; stalled pairs flowing at 180 s), from `linux-e15-table.md`.
3. W1 timing on Linux: first rebind min/median/max, rebind-to-heartbeat median (from `linux-e15-delta.txt`), relapses (runs with a second rebind), and rebinds in the no-kill cell.
4. Every difference from macOS, each with its n.
5. What could make the comparison wrong.

Then send one message: [answer], with the one-line result, the report path and the commit.
