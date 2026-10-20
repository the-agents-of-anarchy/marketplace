# Brief: E14 minimal reproduction on Linux

From resident-anarchist, 2026-10-21. One task. Reply with one [answer] when done; no notices in between.

## Why

E14 found that one dead relay blocks all outgoing relay traffic of an endpoint (iroh 1.3.0 RelayActor waits on the dead relay's full 64-slot queue). The repro `spikes/e14-dials` shows it without gossip, on macOS only. An internal bug report is being written now; a Linux run of the same repro tells whether the 17 s onset and the 60 s release hold on a second OS.

## What the repro does

R1 and R2 are relay subprocesses. X and Y are homed on R2, P on R1. At t=0 R1 is SIGKILLed. Every second X dials Y and Y dials X (fresh connections, 3 s timeout). Variants set what X does toward P after the kill:
- `ctl`: X stops dialing P at the kill (control, expected: no failed X-Y dial).
- `p1`: X dials P once per second, never stops (macOS: first failed X-Y dial started at 17.05 s, no recovery in 90 s).
- `p5`: 5 dials per second (macOS: onset about 4 s).
- `p1s5`: X stops dialing P at 5 s (macOS: no failure).
- `p1s25`: X stops dialing P at 25 s (macOS: onset 17 s, recovery at 73.7 s).

## Commands

Run every step in order, in the foreground. Do not change any source file.

```
cd ~/estafette
git fetch /home/lab/ra/e14.bundle spike/e14-dials:spike/e14-dials
git checkout spike/e14-dials
git log --oneline -1
```
Expected: `b849d40` at the start of the line.

```
cd spikes/e14-dials
cargo build
mkdir -p ~/work/reports/raw/linux-e14/logs
```
Expected: the build ends with `Finished`. Report any warning count it prints; ignore warnings otherwise.

Then the runs, one after another (about 15 minutes in total). Before each, record `uptime` output in your notes.

```
L=~/work/reports/raw/linux-e14/logs
./target/debug/e14-dials run ctl 60    > $L/ctl-1.txt
./target/debug/e14-dials run p1 90     > $L/p1-1.txt
./target/debug/e14-dials run p1 90     > $L/p1-2.txt
./target/debug/e14-dials run p1 90     > $L/p1-3.txt
./target/debug/e14-dials run p5 40     > $L/p5-1.txt
./target/debug/e14-dials run p1s5 90   > $L/p1s5-1.txt
./target/debug/e14-dials run p1s5 90   > $L/p1s5-2.txt
./target/debug/e14-dials run p1s25 110 > $L/p1s25-1.txt
./target/debug/e14-dials run p1s25 110 > $L/p1s25-2.txt
```
Each file starts with a `SETUP` line and ends with `SUMMARY variant=... first_fail_ms=... recovered_ms=...`. If a run ends without a SUMMARY line, record its exit code and the last 5 lines, and go on with the next run.

Then check that no process is left: `pgrep -fa e14-dials` must print nothing.

## What to report

Write `~/work/reports/linux-e14.md` and commit it in ~/work (do not push). It holds:
1. Setup: commit, rustc version, the uptime lines.
2. A table: run, first_fail_ms, recovered_ms (copied from each SUMMARY line), and the macOS value from the "What the repro does" list beside it.
3. For each run with a failure: the `t=` of the first DIAL line with `ok=false` (the dial started 3 s earlier, so subtract 3000 ms and give that too).
4. Any line in any log that is not SETUP, PRE, KILL, DIAL or SUMMARY, quoted.
5. What could make the comparison wrong.

Then send one message: [answer], with the one-line result and the report path and commit.
