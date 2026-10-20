# Linux run 2: E10 relay-death scenario (variant A) on Linux

lab-sibling, 2026-10-20, for resident-anarchist; brief `/home/lab/ra/linux-e10.md`.

## Answer

The stall and the ~40 s re-home both happen on Linux. Kill R1+B1 with probers on: M2-M3 stalled 3/3 with nothing flowing again within 88 s, and all 12 M1 pairs stalled with none resumed. M1 re-homed at a median 41.2 s after the kill. Probers off: stalled 2/3, none healed, re-home at a median 41.1 s. Control (B1 only): 0/3 stalled. Re-home timing fits two re-stun intervals: 42.0-50.0 s after M1's bind, against the predicted 40-52 s.

There are two differences. Stall onset is earlier with probers (median 3.7 s vs 8.9 s) and later without them (8.5 s vs 4.9 s). In one control run (a-7-1), M1 re-homed to R2 while R1 was still alive, at 42.8 s, with no stall; macOS variant A showed 0/3 such flips.

## Machine, toolchain, commit

- `uname -a`: `Linux estafette-lab 6.8.0-138-generic #138-Ubuntu SMP PREEMPT_DYNAMIC Fri Jul 31 22:41:49 UTC 2026 x86_64 x86_64 x86_64 GNU/Linux` (Ubuntu 24.04.4 LTS, Hetzner VM, AMD EPYC-Rome, 2 vCPU, 3819 MiB RAM, no swap)
- `rustc 1.99.1 (58cf8f9c3 2026-10-13)`, Python 3.12.3
- commit `a7e39b6d1b0ddd3a765416d4c294766de6a6c608` (`spike/e10-gossip-main`), with iroh 1.3.0 and iroh-gossip 0.101.0
- Build: `cargo build --features a` (debug, matching E10 on macOS per resident-anarchist), 130.92 s wall, cold, 0 warnings. `target/debug/e10-gossip-main` was copied to `target/bin/e10-a` (sha256 identical). A release build ran first (`--release --features a`, 278.77 s, 0 warnings); it is not used.
- Network: loopback, as on macOS. Relays, bootstrap and members are all child processes of `e10-a ctl` on this host.

## Cells

| cell | command | start (UTC) | load avg (1/5/15) at start | wall |
|---|---|---|---|---|
| a-1 | `./run-cell.sh a 1 - 3` | 18:57:05 | 1.62 1.46 0.77 | 278.99 s |
| a-1np | `./run-cell.sh a 1 np 3` | 19:01:44 | 0.09 0.67 0.61 | 278.22 s |
| a-7 | `./run-cell.sh a 7 - 3` | 19:06:22 | 0.00 0.26 0.44 | 280.27 s |

All exited 0. a-1's 1-minute load of 1.62 is left over from the debug build that finished just before it. For comparison, macOS loads at cell start were 8.45 (a-1), 3.34 (a-1np) and 3.00 (a-7).

## Results beside macOS (variant A, n=3 per cell)

Source: `analyze.py --table logs` (Linux) vs `logs-macos/results-table.md`. Times are in ms after the kill unless marked.

| measure | Linux min / median / max (n) | macOS min / median / max (n) |
|---|---|---|
| **kill R1+B1, probers on** | | |
| M2-M3 stalled (gap >= 5 s) | 3/3 | 3/3 |
| M2-M3 longest HB gap | 81275 / 84272 / 85106 | 78076 / 79066 / 82463 |
| M2-M3 stall onset | 2894 / 3728 / 6725 | 5537 / 8934 / 9924 |
| M2-M3 flowing again at window end | 0/3 | 0/3 |
| M1 re-home | 39130 / 41155 / 45637 | 41367 / 42038 / 44094 |
| M1 HB pairs stalled | 12/12, 0 resumed | 12/12, 0 resumed |
| fresh dial by id to M1 ok again | 0/3 | 1/3 (78101) |
| fresh dial M2-M3 ok again | 0/3 | 0/3 |
| **kill R1+B1, probers off** | | |
| M2-M3 stalled | 2/3 (a-1np-1 did not stall: gap 1006) | 2/3 |
| M2-M3 longest HB gap | 1006 / 79053 / 79996 | 1011 / 83061 / 83203 |
| M2-M3 stall onset | 8004 / 8475 / 8947 (2) | 4797 / 4868 / 4939 (2) |
| M2-M3 flowing again | 0/2 | 0/2 |
| M1 re-home | 37773 / 41074 / 41084 | 41731 / 42616 / 43952 |
| M1 HB pairs stalled | 4/12, 0 resumed | 8/12, 0 resumed |
| **control: kill B1 only** | | |
| M2-M3 stalled | 0/3 | 0/3 |
| M2-M3 longest HB gap | 1009 / 1089 / 1094 | 1012 / 1014 / 1090 |
| M1 re-home to R2 | 1/3 (a-7-1, 42824) | 0/3 |
| M1 HB pairs stalled | 0/12 | 0/12 |

The `ext:` rows `analyze.py --table` prints repeat the base cells, because only runs 1-3 exist here; they add nothing. Raw output: `reports/raw/linux-e10-analyze.txt`.

### Re-home timer (`rehome_check.py logs`)

| run | after kill s | after M1 bind s | kill after bind s |
|---|---|---|---|
| a-1-1 | 45.64 | 50.02 | 4.38 |
| a-1-2 | 39.13 | 43.24 | 4.11 |
| a-1-3 | 41.16 | 45.39 | 4.23 |
| a-1np-1 | 41.08 | 45.26 | 4.17 |
| a-1np-2 | 37.77 | 41.96 | 4.19 |
| a-1np-3 | 41.07 | 45.41 | 4.34 |
| a-7-1 (control flip) | 42.82 | 47.69 | 4.87 |

Kill runs, n=6: after the kill 37.8 / 41.1 / 45.6 s; after M1's bind 42.0 / 45.3 / 50.0 s. On macOS (variant A and B together, n=28) these were 38.4 / 43.0 / 46.6 s and 42.5 / 46.8 / 50.7 s. All six Linux kill runs, and the control flip, fall inside the predicted 40-52 s after bind.

Onsets (`analyze.py --onsets`): variant a had 5 stalled runs, all with onset under 10 s: a-1-3 2.9, a-1-1 3.7, a-1-2 6.7, a-1np-3 8.0, a-1np-2 8.9.

## Differences

1. **Onset order flips.** With probers on, Linux stalls earlier (median 3.7 s vs 8.9 s); without them, later (8.5 s vs 4.9 s). On macOS, across all its variant-A runs (n=10 stalled, including extensions), onsets spread from 3.7 s to 26.0 s, and the probers-on and probers-off ranges overlap. With n=3 and n=2 per cell, this difference is within the spread macOS showed; it does not show an OS effect.
2. **Control flip.** In a-7-1, M1 re-homed to R2 at 42.8 s after the kill (47.7 s after bind) while R1 was alive, and nothing stalled. macOS variant A had 0/3 flips, but macOS variant B had one (b-7-2, 49.2 s after bind). So the flip is the periodic re-stun choosing R2, not a reaction to R1's death, and it does not by itself cause a stall.
3. **Longest gap with probers is about 5 s longer** (84.3 s vs 79.1 s median). With onset about 5 s earlier and the window fixed at 88 s, the stalls ran to the window end in both cases. The gap is window-bounded and carries no separate information.
4. **Fresh dial by id to M1 recovered 0/3, against 1/3 on macOS** (at 78.1 s, near the window end). With n=3, one event in either direction is not a difference.
5. **Probers off: M1 pairs stalled 4/12 vs 8/12.** One of the three runs (a-1np-1) did not stall at all, as one in three did on macOS.
6. **Re-home about 1 s earlier on Linux** (medians 41.2 and 41.1 s vs 42.0 and 42.6 s). This is well within the U(20, 26) s per-interval jitter.

## What could make the comparison wrong

- n=3 per cell; every count above is out of 3 (or 12 pairs, which are not independent within a run). None of the differences is statistically supported, and nor is their absence.
- I collected the logs by hand: the harness writes raw logs and traces to `/tmp/e10/`, and `analyze.py` and `rehome_check.py` read `logs/raw/`. I copied all 9 raw logs and traces from `/tmp/e10/` (which held only these 9 runs, written 18:58-19:11 UTC) into `logs/raw/` and `logs/trace/`, then gzipped the raw logs, because `rehome_check.py` reads only `*.raw.log.gz` (the macOS layout has `.gz`). The brief does not state this step, so it is my reconstruction of E10's procedure. `/tmp/e10/` still holds the uncompressed originals.
- Load differs: macOS ran at load 3-8.5, Linux at 0-1.6, on 2 vCPU. Timing-sensitive onsets could shift with scheduling contention; the onset difference could come from load and not the OS.
- Debug build on both, but a different CPU architecture and speed (x86_64 EPYC-Rome VM vs Apple M2 Max). Debug code is slow enough that CPU speed can move timings in the seconds range only through timers, which dominate here, so the effect should be small. I did not test this.
- rustc version on macOS is not recorded in the brief; the dependency versions are pinned (`=`) in Cargo.toml and come from the same Cargo.lock.
- Loopback on both, so this tests the OS network stack and timers, not a real two-machine network.
- Other users of this machine (resident-anarchist over SSH) could have run work during the cells; the load averages (0.00-1.62) show no sustained load.
- Runs used the harness's background-command runner, serially; no TTY. The harness's child processes take no input from a TTY.

## Files

- Report: `/home/lab/work/reports/linux-e10.md`
- Raw: `/home/lab/work/reports/raw/linux-e10-{build,build-debug,cells,cell-a-1-,cell-a-1np,cell-a-7-,analyze,analyze-runs,onsets,rehome}.txt`
- Run logs: `~/estafette/spikes/e10-gossip-main/logs/` (summary, raw .gz, trace); macOS logs moved to `logs-macos/`.
