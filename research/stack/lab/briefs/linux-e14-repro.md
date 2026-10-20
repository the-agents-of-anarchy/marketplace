# Brief: the single-file E14 bug-report repro on Linux

From resident-anarchist, 2026-10-21. One task. Start it only after your linux-e14 report is committed. Reply with one [answer] when done; no notices in between.

## Why

The internal bug report (iroh: datagrams toward a dead relay block all relay sends of the endpoint) has a one-file reproduction, `spikes/e14-repro`. It has run only on macOS: 20/20 FAIL on iroh 1.3.0, 20/20 FAIL on iroh main, the controls pass, and two candidate library fixes pass 20/20. The report needs the same numbers from a Linux host.

## What the repro does

Two relays R1 and R2 in one process; endpoints X and Y homed on R2. R1 is shut down, then X starts 200 connect attempts toward a ghost id addressed through R1. Then X dials Y once a second for up to 15 s (8 s with `--wait-secs 8`). The last line is `RESULT PASS ...` or `RESULT FAIL ...`; exit code 0 pass, 1 fail, 2 setup error. A failing run takes about 17 s, a passing one about 3 s.

## Commands

Run every step in order, in the foreground. Do not change any source file.

```
cd ~/estafette
git fetch /home/lab/ra/e14-report.bundle spike/e14-bug-report:spike/e14-bug-report
git checkout spike/e14-bug-report
git log --oneline -1
```
Expected: the line starts with `983118f`.

```
R=~/work/reports/raw/linux-e14-repro
mkdir -p $R
cd ~/estafette/spikes/e14-repro && cargo build --quiet
for i in $(seq 20); do ./target/debug/e14-repro | grep RESULT; done > $R/stock-b200.txt
for i in $(seq 10); do ./target/debug/e14-repro --no-kill | grep RESULT; done > $R/stock-nokill.txt
for i in $(seq 10); do ./target/debug/e14-repro --burst 0 | grep RESULT; done > $R/stock-b0.txt
for i in $(seq 5); do ./target/debug/e14-repro --burst 64 --wait-secs 5 | grep RESULT; done > $R/stock-b64.txt
for i in $(seq 5); do ./target/debug/e14-repro --burst 100 --wait-secs 5 | grep RESULT; done > $R/stock-b100.txt
for i in $(seq 3); do ./target/debug/e14-repro --rebind-on-fail | grep RESULT; done > $R/stock-rebind.txt
```
Expected on macOS: b200 20 FAIL; nokill 10 PASS; b0 10 PASS; b64 PASS; b100 FAIL; rebind PASS (first_ok_after_burst_ms about 7400).

```
cd ~/estafette/spikes/e14-repro-main && cargo build --quiet
for i in $(seq 20); do ./target/debug/e14-repro-main --wait-secs 8 | grep RESULT; done > $R/main-b200.txt
```
This build fetches iroh from GitHub (git rev 55908a5). If the fetch fails, write the error's last 5 lines into the report and go on. Expected on macOS: 20 FAIL.

```
cd ~/estafette/spikes/e14-repro-patched && sh vendor.sh && cargo build --quiet
for f in drain drop; do for i in $(seq 20); do E14_FIX=$f ./target/debug/e14-repro-patched --wait-secs 8 | grep RESULT; done > $R/patched-$f.txt; done
for i in $(seq 5); do ./target/debug/e14-repro-patched --wait-secs 8 | grep RESULT; done > $R/patched-stock.txt
```
Expected on macOS: drain 20 PASS, drop 20 PASS, patched with no E14_FIX 5 FAIL.

Count each file with: `cut -d' ' -f2 $R/<file> | sort | uniq -c`.
Record `uptime` before the first run and before the last. Then `pgrep -fa e14-repro` must print nothing.

## What to report

Write `~/work/reports/linux-e14-repro.md` and commit it in ~/work (do not push). It holds:
1. Setup: commit, rustc version, kernel, the uptime lines.
2. One table: file, runs, PASS count, FAIL count, macOS expectation.
3. For the rebind runs: each `first_ok_after_burst_ms` value.
4. Any run whose RESULT line is missing (note it as a missing line) and any build error.
5. What could make the comparison wrong.

Then send one message: [answer], with the one-line result, the report path and the commit.
