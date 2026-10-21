# Brief: E18 late attachment on Linux

From resident-anarchist, 2026-10-21. One task, about 90 min of runs plus a build. Reply with one [answer] when the report is committed; no notices in between.

## Why

E18 (macOS) explained the late attachment after a W1 rebind: the bootstrap node B2 still holds a stale pending Neighbor request to the member's id, so it never answers the member's new Join; the member waits until the harness's 60 s join timeout. Two counters were measured: `x2cw` (member side: join timeout 5 s, then rebind) and `x3cw` (gossip side: B2 drops the pending request on Join, the fix iroh-gossip main has). Baseline `x1cw` is W1 with a fresh lookup at each rebind. The question for Linux: same mechanism, same effect of the counters.

macOS results (n=8 per kill arm):

| Arm | tag | first-generation late joins | late-join wait | all stalled pairs flowing from, median (min-max) |
|---|---|---|---|---|
| A0 baseline | x1cw | 7/22 | 57.4-60 s | 78.7 s (33.3-94.7) |
| A1 join timeout 5 s | x2cw | 4/22 | 5 s | 38.0 s (30.1-58.2) |
| A2 on_join fix | x3cw | 0/24 | - | 31.5 s (21.1-33.9) |
| control, no kill | 0 x1cw | 0 rebinds | - | - |
| A1 control, no kill | 0 x2cw | 0 rebinds in 3 | - | - |

## Commands

Run in the foreground, in order. Do not change any source file. Do not commit anything in ~/estafette.

```
cd ~/estafette
git fetch /home/lab/ra/e18.bundle spike/e18-attach:spike/e18-attach
git checkout spike/e18-attach
git log --oneline -1
```
Expected: the line starts with `85ef8a2`.

```
cd ~/estafette/spikes/e18-attach-gossip
sh vendor.sh
cargo build --features a
mkdir -p target/bin && cp target/debug/e18-attach-gossip target/bin/e10-a
cd ../e10-gossip-main
export E18_LOGDIR=logs/e18-linux
```
`E18_LOGDIR` sends your archives to `logs/e18-linux`, apart from the shipped macOS logs in `logs/e18`. Keep it exported in every shell you run the cells from (set it again if your shell is new).

Runs, about 185 s each; one line below per call (3 runs, under 10 min). Before each line, `pgrep -fl "e10-a|e18-attach"` must print nothing; record `uptime` before the first run of each arm. The three kill arms are interleaved by batch.
```
sh e18-run.sh 0 x1cw 2800
sh e18-batch.sh 1 x1cw 2801 3
sh e18-batch.sh 1 x2cw 2811 3
sh e18-batch.sh 1 x3cw 2821 3
sh e18-batch.sh 1 x1cw 2804 3
sh e18-batch.sh 1 x2cw 2814 3
sh e18-batch.sh 1 x3cw 2824 3
sh e18-batch.sh 1 x1cw 2807 2
sh e18-batch.sh 1 x2cw 2817 2
sh e18-batch.sh 1 x3cw 2827 2
sh e18-batch.sh 0 x2cw 2831 3
```
Each run ends with `no stray`; if not, stop and report.

Analysis (only your logs):
```
R=~/work/reports/raw/linux-e18; mkdir -p $R
python3 -I analyze_e18_table.py logs/e18-linux > $R/table.md
python3 -I analyze_e18.py logs/e18-linux --joins $(ls logs/e18-linux | grep raw | sed 's/.raw.log.gz//' | grep -v a-0x) > $R/joins.txt
cp -R logs/e18-linux $R/logs
```
For the first late join you find in `joins.txt` (an A0 run), also save `python3 -I analyze_e18.py logs/e18-linux --b2 <run> <member> -8 80 > $R/b2-<run>-<member>.txt`.

## What to report

Write `~/work/reports/linux-e18.md` and commit it in ~/work (do not push):
1. Setup: commit, rustc, kernel, uptime lines, build time.
2. The table above with Linux values beside each macOS value, from your `table.md`.
3. For the B2 timeline you saved: B2's state for the member at its Join (active? pending?), whether a Neighbor went out, and what ended the wait.
4. Every difference from macOS, with its n; what could make the comparison wrong.

Then send one message: [answer], with the one-line result, the report path and the commit.
