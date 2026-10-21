# Brief: E20 membership change on Linux

From resident-anarchist, 2026-10-21. One task, about 60 min of runs plus a build. Reply with one [answer] when the report is committed; no notices in between.

## Why

E20 (macOS) found that a rebound member sometimes has no gossip neighbor among the other members; it then hears heartbeats only through the bootstrap node, 11-16 s late. The change `E20_MJOIN_MS=1500` (tag `y3w`): 1.5 s after a rebind's join, a member with no member neighbor asks the other members directly, every 3 s. Your E19 run showed B1 healing faster on Linux than on macOS; this run shows whether Linux has the late endpoints at all, and what the change does there.

macOS results (n=8 per kill arm):

| Arm | tag | first-generation endpoints with first heartbeat 10 s or later | runs with a second rebind | all stalled pairs flowing from, s min / med / max |
|---|---|---|---|---|
| B1 | y1w | 5/21 | 0 | 13.6 / 18.0 / 31.6 (n=7) |
| B3 (B1 + change) | y3w | 0/24 | 0 | 14.5 / 18.1 / 28.0 |
| B3 no kill | 0 y3w | - | 0 REBIND, 0 MJOIN in 3 | - |

## Commands

Run in the foreground, in order. Do not change any source file. Do not commit anything in ~/estafette. Launch the batches from a script file (as you did for E19), so `pgrep` does not match your own command line.

```
cd ~/estafette
git fetch /home/lab/ra/e20.bundle spike/e20-delay:spike/e20-delay
git checkout spike/e20-delay
git log --oneline -1
```
Expected: the line starts with `9abb991`.

```
cd ~/estafette/spikes/e18-attach-gossip
sh vendor.sh
cargo build --features a
mkdir -p target/bin && cp target/debug/e18-attach-gossip target/bin/e10-a
cd ../e10-gossip-main
export E18_LOGDIR=logs/e20-linux
unset E17_FRESH_LOOKUP E17_PROBE E18_JOIN_T_MS E18_FIX E20_MJOIN_MS
```

Runs, about 185 s each, one line per call; `pgrep -fl "e10-a|e18-attach"` must print nothing before each; record `uptime` before the first and the last line.
```
sh e18-batch.sh 0 y3w 2930 1
sh e18-batch.sh 1 y1w 2900 2
sh e18-batch.sh 1 y3w 2910 2
sh e18-batch.sh 1 y1w 2902 2
sh e18-batch.sh 1 y3w 2912 2
sh e18-batch.sh 1 y1w 2904 2
sh e18-batch.sh 1 y3w 2914 2
sh e18-batch.sh 1 y1w 2906 2
sh e18-batch.sh 1 y3w 2916 2
sh e18-batch.sh 0 y3w 2931 2
```
Each run ends with `no stray`; if not, stop and report.

Analysis (only your logs):
```
R=~/work/reports/raw/linux-e20; mkdir -p $R
python3 -I analyze_e20_table.py logs/e20-linux > $R/table.md
python3 -I analyze_e20_stats.py logs/e20-linux > $R/stats.txt
python3 -I analyze_e20_delta.py logs/e20-linux > $R/delta.txt
python3 -I analyze_e20_who.py logs/e20-linux 'a-1y1w-*' > $R/who-y1w.txt
python3 -I analyze_e20_who.py logs/e20-linux 'a-1y3w-*' > $R/who-y3w.txt
python3 -I analyze_e20_online.py logs/e20-linux 'a-1y1w-*' > $R/online-y1w.txt
cp -R logs/e20-linux $R/logs
```

## What to report

Write `~/work/reports/linux-e20.md` and commit it in ~/work (do not push):
1. Setup: commit, rustc, kernel, uptime lines, build time.
2. The table above with Linux values beside each macOS value, plus the p values `stats.txt` prints.
3. For each late endpoint in `who-y1w.txt`: whether it had a member neighbor, and who sent it Neighbor.
4. The home-relay connect times from `online-y1w.txt` (min / median / max).
5. Every difference from macOS, with its n; what could make the comparison wrong.

Then send one message: [answer], with the one-line result, the report path and the commit.
