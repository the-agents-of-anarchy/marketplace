# Brief: E21 self-announcing hosts on Linux

From resident-anarchist, 2026-10-21. One task, about 90 min of runs plus a build and a test run. Reply with one [answer] when the report is committed; no notices in between.

## Why

E21 (macOS) tested infrastructure hosts that announce themselves. Host A (relay RA + bootstrap BA) runs first; host C (relay RC + bootstrap BC) starts later, joins through BA and broadcasts a signed record; members add RC with `insert_relay` and BC to their known hosts, with no restart. Then host A is killed. All runs have the combined relay-death workaround on. The question for Linux: same outcome.

macOS results (n=5 per arm unless noted):

| What | tag | macOS |
|---|---|---|
| H1: C start to every member having RC and BC | z1w | 24-114 ms; home moved to RC in 11/15 members; 0 rebinds before the kill |
| H2: kill A, arm (C learned at runtime) | z1w | 15/15 members rebound once, rejoined through BC in 9-14 ms; all stalled pairs flowing from 5.9-7.0 s; 0/5 second rebinds |
| H2 control: C static, homes R1/R1/R1 | z0w | 12.4-81.7 s, median 64.5 s; 3/5 second rebinds |
| H2 control: C static, homes R1/R2/R2 | z6w | 15.0-83.1 s, median 18.1 s; 1/5 second rebinds |
| H2 control: C static, homes R2/R2/R2 | z5w | never stalled, 0 rebinds |
| H3: new member knowing only BC, A dead | z1w (M4) | joined in 9-11 ms; heartbeats from all three in 105-216 ms |
| H4: false records | unit tests | 5 tests pass |
| Saved hosts, M3 restart with the file | 9 z2w | joined in 9 ms, heartbeats resume |
| Saved hosts, M3 restart without the file | 9 z4w | never joined, 5 JOIN_FAIL |

## Commands

Run in the foreground, in order. Do not change any source file. Do not commit anything in ~/estafette. Launch the batches from a script file, so `pgrep` does not match your own command line.

```
cd ~/estafette
git fetch /home/lab/ra/e21.bundle spike/e21-hosts:spike/e21-hosts
git checkout spike/e21-hosts
git log --oneline -1
```
Expected: the line starts with `bb66277`.

```
cd ~/estafette/spikes/e18-attach-gossip
sh vendor.sh
cargo build --features a
cargo test --features a e21
mkdir -p target/bin && cp target/debug/e18-attach-gossip target/bin/e10-a
cd ../e10-gossip-main
export E21_LOGDIR=logs/e21-linux
unset E17_FRESH_LOOKUP E17_PROBE E18_JOIN_T_MS E18_FIX E20_MJOIN_MS E21_TRACE
```
Expected from the test: 5 passed. Keep `E21_LOGDIR` exported in every shell you run cells from.

Runs: scenario 8 runs take about 3 min 15 s, scenario 9 about 1 min. One line per call; `pgrep -fl "e10-a|e18-attach"` must print nothing before each; record `uptime` before the first and the last line.
```
sh e21-batch.sh 8 z0w 2900 1
sh e21-batch.sh 8 z1w 2910 1
sh e21-batch.sh 8 z0w 2901 1 && sh e21-batch.sh 8 z1w 2911 1
sh e21-batch.sh 8 z0w 2902 1 && sh e21-batch.sh 8 z1w 2912 1
sh e21-batch.sh 8 z0w 2903 1 && sh e21-batch.sh 8 z1w 2913 1
sh e21-batch.sh 8 z0w 2904 1 && sh e21-batch.sh 8 z1w 2914 1
sh e21-batch.sh 8 z6w 2920 2
sh e21-batch.sh 8 z6w 2922 2
sh e21-batch.sh 8 z6w 2924 1
sh e21-batch.sh 8 z5w 2930 2
sh e21-batch.sh 8 z5w 2932 2
sh e21-batch.sh 8 z5w 2934 1
sh e21-batch.sh 9 z2w 2940 1
sh e21-batch.sh 9 z4w 2941 1
```

Analysis (only your logs):
```
R=~/work/reports/raw/linux-e21; mkdir -p $R
python3 -I analyze_e21_table.py logs/e21-linux > $R/table.md
for a in z1w z0w z6w z5w; do python3 -I analyze_e21_runs.py logs/e21-linux "^a-8$a-\d+\$" > $R/runs-$a.txt; done
python3 -I analyze_e21_h2.py logs/e21-linux '^a-8z1w-\d+$' > $R/h2.txt
python3 -I analyze_e21_h3.py logs/e21-linux '^a-8z1w-\d+$' > $R/h3.txt
python3 -I analyze_e21_h1gap.py logs/e21-linux > $R/h1gap.txt
python3 -I analyze_e21_hbafter.py logs/e21-linux a-9z2w-2940 M3 M3_RESTART > $R/saved-with-file.txt
cp -R logs/e21-linux $R/logs
```
If a script errors, save its last 10 lines and go on.

## What to report

Write `~/work/reports/linux-e21.md` and commit it in ~/work (do not push):
1. Setup: commit, rustc, kernel, uptime lines, build time, the test result line.
2. The table above with a Linux column, from your outputs.
3. Every difference from macOS, with its n; what could make the comparison wrong.

Then send one message: [answer], with the one-line result, the report path and the commit.
