# Linux run 4: E12 (own fix for the gossip stall) on Linux

lab-sibling, 2026-10-20, for resident-anarchist; brief `/home/lab/ra/linux-e12.md`.

## Answer

The levers behave on Linux as on macOS. L1 fired in 9/9 scenario-1 runs at 0.5 s, and M1 re-homed at 0.7 s. L2 rejoined 7-8 times per silent member and healed nothing: 0 of 38 stalled pairs were flowing again at window end. The control (scenario 7) had 0/3 stalled, no L1 fire and no rejoin.

Fresh dials also time out on Linux after the kill, and more uniformly than on macOS. With probers on, every probe dial after 4.1 s past the kill failed with `timeout3s` (125-127 per run, 0 succeeded) in 3/3 runs. On macOS, 4 of 5 runs had some fresh dials succeed more than 10 s after the kill.

## Machine, toolchain, commit

- Same machine as `reports/linux-e11.md`: `Linux estafette-lab 6.8.0-138-generic #138-Ubuntu SMP PREEMPT_DYNAMIC Fri Jul 31 22:41:49 UTC 2026 x86_64`, 2 vCPU AMD EPYC-Rome VM, 3819 MiB RAM, Ubuntu 24.04.4; loopback
- `rustc 1.99.1 (58cf8f9c3 2026-10-13)`, Python 3.12.3
- commit `d4b4ca0ffca75053af56f2d639c7d1854757b4dc` (`spike/e12-rejoin`); iroh 1.3.0, iroh-gossip 0.101.0
- `cargo build --features a` (debug): 11.69 s wall, incremental (dependencies cached from the E10 debug build), 0 warnings. `target/debug/e10-gossip-main` was copied to `target/bin/e10-a` (sha256 `568f8429bbbf3d25…`, identical).
- `/tmp/e10` was emptied before the cells (the Linux run 2 files went to `/tmp/e10-linux-run2`). After the cells it held exactly these 12 runs (20:33-20:50 UTC), which I copied into `logs/raw` (gzipped) and `logs/trace`.

## Cells

| cell | command | start (UTC) | load avg (1/5/15) at start | wall |
|---|---|---|---|---|
| a-1l12np | `./run-cell.sh a 1 l12np 3` | 20:32:09 | 0.39 0.10 0.03 | 279.26 s |
| a-1l12 | `./run-cell.sh a 1 l12 3` | 20:36:48 | 0.01 0.06 0.03 | 278.45 s |
| a-1l1np | `./run-cell.sh a 1 l1np 3` | 20:41:27 | 0.00 0.02 0.00 | 277.72 s |
| a-7l12 | `./run-cell.sh a 7 l12 3` | 20:46:04 | 0.00 0.00 0.00 | 279.45 s |

All exited 0.

## `analyze_e12.py logs --table` failed

It printed cells 1-3, then:

```
Traceback (most recent call last):
  File "/home/lab/estafette/spikes/e10-gossip-main/analyze_e12.py", line 97, in <module>
    {"--runs": runs_table, "--table": table}[sys.argv[2]](sys.argv[1])
  File "/home/lab/estafette/spikes/e10-gossip-main/analyze_e12.py", line 92, in table
    f"| {key} {label} | {n} | {st}/{n} | {rec}/{st} | {stat([m['m23_gap'] for m in ms])} | {anyst}/{n} | {sf}/{sp} | {stat([m['rehome'] for m in ms])} | {stat([m['l1_fire_first'] for m in ms])} | {min(rj)}-{max(rj)} | {sum(m['l1_fire_total'] for m in ms) if key == '5' else '-'} |"
                                                                                                                                                                                                     ^^^^^^^
ValueError: min() iterable argument is empty
```

Cell 4 (L2 alone, `a-1l2np`) is not in the brief, so it has no runs here, and `min()` over its empty rejoin list raises. I changed no code. I took the cell 5 (control) row below from `--runs`, which completed. Raw output: `reports/raw/linux-e12-{table,runs}.txt`.

## Per cell beside macOS

| cell | Linux (n=3) | macOS |
|---|---|---|
| **1 L1+L2, probers off, scn 1** | | (n=5) |
| M2-M3 stalled | 2/3 | 3/5 |
| flowing again at end, of stalled | 0/2 | 0/3 |
| M2-M3 longest gap s | 1.0 / 78.1 / 83.0 | 1.0 / 79.1 / 80.1 |
| stalled pairs flowing at end | 0/10 | 0/14 |
| M1 L1 fire / re-home s | 0.5 / 0.7 (3/3) | 0.5 / 0.7 (5/5) |
| rejoins per run after kill | 0-22 | 0-21 |
| **2 L1+L2, probers on, scn 1** | | (n=5) |
| M2-M3 stalled | 3/3 | 5/5 |
| flowing again at end | 0/3 | 0/5 |
| M2-M3 longest gap s | 84.1 / 84.1 / 84.2 | 77.9 / 82.2 / 84.5 |
| stalled pairs flowing at end | 0/18 | 0/30 |
| M1 L1 fire / re-home s | 0.5 / 0.7 (3/3) | 0.5 / 0.7 (5/5) |
| rejoins per run after kill | 22-24 | 21-22 |
| **3 L1 alone, probers off, scn 1** | | (n=3) |
| M2-M3 stalled | 1/3 | 2/3 |
| flowing again at end | 0/1 | 0/2 |
| M2-M3 longest gap s | 1.0 / 1.1 / 84.1 | 1.0 / 80.1 / 83.9 |
| any HB pair stalled | 2/3 | 2/3 |
| stalled pairs flowing at end | 0/10 | 0/10 |
| M1 L1 fire / re-home s | 0.5 / 0.7 (3/3) | 0.5 / 0.7 (3/3) |
| rejoins | 0 | 0 |
| **5 control scn 7, L1+L2, probers on** | | (n=3) |
| M2-M3 stalled | 0/3 | 0/3 |
| longest gap s | 1.0 / 1.0 / 1.0 | 1.0 / 1.1 / 1.1 |
| L1 fires | 0 | 0 |
| rejoins | 0 | 0 |
| M1 re-home to R2 | 1/3 (a-7l12-1, 36.8 s, R1 alive) | 1/3 (43.9 s) |

Totals, scenario 1: L1 fired 9/9 at 0.5 s (500 ms debounce), with re-home 0.2 s later in every run. Stalled pairs flowing again at window end: 0/38 on Linux, 0/54 on macOS (the brief's "0 of 62" includes macOS cell 4).

L2 detail (`--runs`): each silent member made 7-8 `join_peers` calls in 88 s, all returning `join_peers=ok ms=0`, at silences of about 3, 5, 9, 17 and 33 s and onward (doubling backoff). No member in a healthy run, and none before the kill, made a call. In a-1l12np-1 only M3 rejoined (0/0/7), because only its pairs went silent.

## Fresh dials after the kill (the point to watch)

The probers make a fresh dial by node id to each peer, with a 3 s timeout. Counted from the raw logs, after the KILL record, probers-on runs only:

| run | ok | fail | last ok (s after kill) | errors |
|---|---|---|---|---|
| Linux a-1l12-1 | 14 | 125 | 4.0 | timeout3s:125 |
| Linux a-1l12-2 | 17 | 125 | 4.1 | timeout3s:125 |
| Linux a-1l12-3 | 9 | 127 | 4.1 | timeout3s:127 |
| macOS a-1l12-1 | 38 | 121 | 87.6 | timeout3s:121 |
| macOS a-1l12-2 | 14 | 127 | 4.0 | timeout3s:127 |
| macOS a-1l12-3 | 30 | 121 | 88.0 | timeout3s:121 |
| macOS a-1l12-4 | 17 | 122 | 77.5 | timeout3s:122 |
| macOS a-1l12-5 | 100 | 112 | 87.4 | timeout3s:102, No addressing information available:10 |
| Linux a-7l12-1/2/3 (control) | 522 / 516 / 516 | 0 | 88.0 / 87.5 / 87.4 | - |
| macOS a-7l12-1/2/3 (control) | 522 each | 0 | ~87.8 | - |

On Linux, every fresh dial after about 4 s past the kill timed out, in 3/3 runs, and none succeeded for the rest of the window. The successes before 4 s precede the stall onset (failed dials start at 3.0-8.1 s, per the harness summary). On macOS, a-1l12-2 matches Linux. The other four macOS runs had some dials succeed more than 10 s after the kill, scattered across pairs: for example, a-1l12-5 had 6-8 per pair, and a-1l12-3 had 2-3 per pair on M2-M3 only. The macOS successes did not restore heartbeats: 0/30 pairs were flowing at the end. On Linux the failure is uniform: 100% `timeout3s`, with no `No addressing information` errors.

Probers-off cells make no fresh dials, so they show nothing here: the harness summary reports every dial field as NA.

## Differences

1. **Fresh dials:** Linux 0/3 runs with any success after 4.1 s; macOS 4/5 runs with late successes. With n=3 against n=5 this is suggestive, not established (Fisher exact, one-sided, 0/3 vs 4/5: p≈0.07). If it holds, the timeouts on Linux are not a macOS artifact, and Linux is the cleaner place to trace them.
2. **Stall rates** are lower in cells 1 and 3 on Linux (2/3 vs 3/5, 1/3 vs 2/3). These are counts out of 3, within run-to-run variation; E10 on both OSes showed one probers-off run in three not stalling.
3. **Control flip:** a-7l12-1 re-homed at 36.8 s, below E10's 40-52 s-after-bind window as measured from the kill. I did not compute the time after bind for this run. macOS also had 1/3 flip (43.9 s).
4. **Longest gaps with probers on** are 84.1 s every run, which is window-bounded (stall onset about 4 s, window 88 s).

## What could make the comparison wrong

- n=3 per cell against macOS's n=5 (cells 1 and 2); every rate here has a wide interval.
- The fresh-dial counts are my own `awk` over the raw logs (PROBE records after the KILL record, field 5 `ok`/`fail`, field 7 error), not a script of E12's. The same filter ran on both OS's logs. Command: `zcat <log> | awk '$3=="KILL"{k=$1} $3=="PROBE"&&k{...}'`.
- `analyze_e12.py --table` crashed (above); I took the cell 5 row from `--runs` by hand.
- Debug build on both, but a different CPU (x86_64 VM vs M2 Max). Load was 0.00-0.39 here and is not recorded for E12 on macOS in the brief.
- Loopback only, on one host; this does not test two machines.
- The incremental build reused dependency artifacts from the E10 debug build. Between a7e39b6 and d4b4ca0, `Cargo.toml` and `Cargo.lock` differ only by the added `tracing-subscriber` (0.3, env-filter); iroh and iroh-gossip are unchanged.
- resident-anarchist's SSH work could have overlapped. The low load averages show no sustained load.

## Files

- Report: `/home/lab/work/reports/linux-e12.md`
- Raw: `/home/lab/work/reports/raw/linux-e12-{build,cells,cell-a-1l12np,cell-a-1l12,cell-a-1l1np,cell-a-7l12,table,runs}.txt`, and run logs in `reports/raw/linux-e12-logs/`
- In the clone: `~/estafette/spikes/e10-gossip-main/logs/` (Linux), `logs-macos/` (shipped)
