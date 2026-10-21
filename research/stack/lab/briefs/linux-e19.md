# Brief: E19 combined workaround on Linux

From resident-anarchist, 2026-10-21. One task, about 90 min of runs plus a build. Start it only after your linux-e18 report is committed. Reply with one [answer] when done; no notices in between.

## Why

E19 (macOS) measured the relay-death workaround with all its parts together (B1: W1 rebind + C2 relay probe and lookup scrub + 5 s join timeout + the on_join fix at the bootstrap node), against W1 alone (B0) and the combination without C2 (B2). The question for Linux: same outcome.

macOS results (n=8 per kill arm, interleaved by batch):

| Arm | tag | runs stalled | runs with a second rebind | stalled pairs flowing at 180 s | all stalled pairs flowing from, s min / med / max |
|---|---|---|---|---|---|
| B0 W1 alone | y0w | 8 | 3 | 46/48 | 15.7 / 17.1 / 148.8 (one run never all flowing) |
| B1 combined | y1w | 7 | 0 | 42/42 | 29.3 / 31.2 / 33.2 |
| B2 combined without C2 | y2w | 8 | 5 | 48/48 | 14.1 / 141.4 / 162.6 |
| B1 no kill | 0 y1w | 0 | 0 REBIND, 0 JOIN_FAIL in 3 | - | - |

## Commands

Run in the foreground, in order. Do not change any source file. Do not commit anything in ~/estafette.

```
cd ~/estafette
git fetch /home/lab/ra/e19.bundle spike/e19-combined:spike/e19-combined
git checkout spike/e19-combined
git log --oneline -1
```
Expected: the line starts with `b1357d1`.

```
cd ~/estafette/spikes/e18-attach-gossip
sh vendor.sh
cargo build --features a
mkdir -p target/bin && cp target/debug/e18-attach-gossip target/bin/e10-a
cd ../e10-gossip-main
export E18_LOGDIR=logs/e19-linux
unset E17_FRESH_LOOKUP E17_PROBE E18_JOIN_T_MS E18_FIX
```
Keep `E18_LOGDIR` exported in every shell you run the cells from (set it again in a new shell).

Runs, about 185 s each; one line per call. Before each line `pgrep -fl "e10-a|e18-attach"` must print nothing; record `uptime` before the first line and before the last.
```
sh e18-run.sh 0 y1w 2930
sh e18-batch.sh 1 y0w 2900 3
sh e18-batch.sh 1 y1w 2910 3
sh e18-batch.sh 1 y2w 2920 3
sh e18-batch.sh 1 y0w 2903 3
sh e18-batch.sh 1 y1w 2913 3
sh e18-batch.sh 1 y2w 2923 3
sh e18-batch.sh 1 y0w 2906 2
sh e18-batch.sh 1 y1w 2916 2
sh e18-batch.sh 1 y2w 2926 2
sh e18-batch.sh 0 y1w 2931 2
```
Each run ends with `no stray`; if not, stop and report.

Analysis (only your logs):
```
R=~/work/reports/raw/linux-e19; mkdir -p $R
python3 -I analyze_e19_table.py logs/e19-linux > $R/table.md
python3 -I analyze_e19_stats.py logs/e19-linux > $R/stats.txt
python3 -I analyze_e19.py logs/e19-linux --second $(ls logs/e19-linux | grep raw.log.gz | sed 's/.raw.log.gz//' | grep -v "a-0y") > $R/second_rebinds.txt
cp -R logs/e19-linux $R/logs
```

## What to report

Write `~/work/reports/linux-e19.md` and commit it in ~/work (do not push):
1. Setup: commit, rustc, kernel, uptime lines, build time.
2. The table above with Linux values beside each macOS value, from `table.md` and `stats.txt`, plus the p values `stats.txt` prints.
3. For each second rebind: its class from `second_rebinds.txt` (inferred re-block, late join, other).
4. Every difference from macOS, with its n; what could make the comparison wrong.

Then send one message: [answer], with the one-line result, the report path and the commit.
