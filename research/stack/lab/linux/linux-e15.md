# Linux run: E15 workaround experiment (W1 rebind) on Linux

lab-sibling, 2026-10-21, for resident-anarchist; brief `/home/lab/ra/linux-e15.md`.

## Answer

W1 heals the stall on Linux as on macOS, and the diagnostic transport fix stops the stall there too. With n=3 runs per arm:

- **W1 healed every stalled pair:** T=3 s 18/18 (3 of 3 runs stalled), T=10 s 18/18 (3/3), W1+L1 12/12 (2/3 runs stalled). The control and L1+L2 healed none (0/12 and 0/18).
- **W1 timing:** first rebind 6.9 / 10.4 / 14.0 s after the kill at T=3 s (min/median/max over 3 runs; macOS 7-24 s); heartbeat back a median 4.2 s after the rebind (macOS 4.1 s). One of the 8 stalled W1 runs relapsed with a second rebind (macOS 5 of 13). No rebind in the no-kill cell (0 of 3 runs, 18/18 pairs flowing).
- **Diagnostic transport:** with the drain fix, no stall in 6/6 runs (no levers 3/3, L1+L2 3/3); with the fix off, 3/3 stalled and 0/18 pairs healed.

Every number below is from the 27 runs I made (runs 1-3 of each arm). The command in the brief, `analyze_e15.py logs/e15`, mixes in macOS data (next section).

## A defect in the brief's procedure: `logs/e15/` already holds macOS runs

The branch `spike/e15-workaround` ships `spikes/e10-gossip-main/logs/e15/` with macOS runs 4 and 5 of the arms that have n=5 there (and runs 1-3 of the n=3 arms). `e15-archive.sh` writes runs 1-3 over the shipped files and leaves runs 4-5 in place, so `analyze_e15.py logs/e15` on this directory reports five runs for A0, A1, A2 and A3 where I made three. I saw it because the first table showed n=5, matching macOS's n, and `git status` showed `logs/e15/a-1w-4.raw.log.gz` and `-5` untouched (mtime 00:01, before my first cell at 00:02).

What I did: the three analysis commands were re-run on only the 54 files my runs overwrote (`git status` M files under `logs/e15`; copy in `reports/raw/linux-e15/logs-e15/`). Those are the tables used here (`reports/raw/linux-e15-{table,runs}.md`, `-delta.txt`). The mixed outputs the brief's commands produced are kept as `reports/raw/linux-e15-{table,runs}-with-macos-runs-4-5.md` and `-delta-with-macos-runs-4-5.txt`; do not read them as Linux. After copying, I restored the tracked files in the clone (`git checkout -- spikes/e10-gossip-main/logs`).

## Setup

- Commit `37b0a1acbeb917e6e49ddfbd52fa3ea943908cee` (`spike/e15-workaround`, from `/home/lab/ra/e15.bundle`); no source file changed.
- `rustc 1.99.1 (58cf8f9c3 2026-10-13)`; kernel `6.8.0-138-generic` (Linux, x86_64, 2 vCPU AMD EPYC-Rome VM, 3819 MiB RAM, Ubuntu 24.04.4); loopback.
- Builds: `cargo build --features a` 12.08 s (incremental; dependencies cached from earlier E10/E12 builds); diagnostic `e15-diag-gossip` 135.56 s after `sh ../e14-repro-patched/vendor.sh` (exit 0, `patching file src/socket/transports/relay/actor.rs`). Main binary sha256 `d7ee8ce5b65fdf1a…`. Build outputs: `reports/raw/linux-e15/build-*.txt`.
- Each cell ran 3 runs, about 9 min 15 s, all `rc=0`; `pgrep -fl e10-` printed nothing before every cell, and `pgrep -fl "e10-a|e15-diag"` printed nothing at the end. Cell start times, uptime lines, and the run script: `reports/raw/linux-e15/{cells.txt,uptime.txt,pgrep.txt,run-e15.sh}`.

| cell | start (UTC) | uptime line before it |
|---|---|---|
| a 1 w | 00:02:36 | load average: 0.30, 0.08, 0.03 |
| a 1 l12w | 00:11:51 | 0.09, 0.11, 0.06 |
| a 1 w1w | 00:21:05 | 0.00, 0.03, 0.04 |
| a 1 w1w10 | 00:30:21 | 0.51, 0.35, 0.18 |
| a 1 w1l1w | 00:39:36 | 0.18, 0.27, 0.20 |
| a 0 w1w | 00:48:51 | 0.75, 0.61, 0.39 |
| a 1 pw (E14_FIX=drain) | 01:00:23 | 1.66, 1.04, 0.64 |
| a 1 pl12w (E14_FIX=drain) | 01:09:38 | 0.27, 0.48, 0.53 |
| a 1 pc | 01:18:53 | 0.04, 0.34, 0.45 |

The pw cell's 1.66 is left over from the diagnostic build that finished at about 01:00.

- One deviation: the old `/tmp/e10` held a-1w-1..3 and a-1w-101 from my earlier 180 s run, which the `a-1w-` archive pattern would have taken; I moved it to `/tmp/e10-linux-e14w` and started with an empty `/tmp/e10`.

## Arms beside macOS

macOS columns are the brief's table. "Stalled pairs flowing at 180 s" is healed pairs over stalled pairs; for the three arms with no stall it is pairs flowing over all 6 per run. A run counts as stalled when any of its 6 pairs had a heartbeat gap of 5 s or more.

| Arm | tag | macOS runs stalled | macOS flowing at 180 s | Linux runs stalled | Linux flowing at 180 s |
|---|---|---|---|---|---|
| A0 control, no levers | w | 4/5 | 0/24 | 2/3 | 0/12 |
| A1 L1+L2 | l12w | 4/5 | 2/24 | 3/3 | 0/18 |
| A2 W1, T=3 s | w1w | 5/5 | 30/30 | 3/3 | 18/18 |
| A2b W1, T=10 s | w1w10 | 3/3 | 16/16 | 3/3 | 18/18 |
| A3 W1 + L1 | w1l1w | 5/5 | 30/30 | 2/3 | 12/12 |
| A2c W1, no kill | a 0 w1w | 0/3 | 18/18 | 0/3 | 18/18 |
| A4 drain fix, no levers | pw | 0/3 | 18/18 | 0/3 | 18/18 |
| A4b drain fix, L1+L2 | pl12w | 0/3 | 18/18 | 0/3 | 18/18 |
| A4c diag build, fix off | pc | 3/3 | 0/18 | 3/3 | 0/18 |

The stall-free runs on Linux are a-1w-1 (A0) and a-1w1l1w-1 (A3): in a-1w-1 every pair's longest heartbeat gap is 1.0-1.02 s (checked from the raw log). A1's L2 made 39 rejoins in each of its 3 runs (180 s window).

## W1 timing on Linux (`linux-e15-table.md`, `linux-e15-delta.txt`)

| measure | A2 (T=3 s) | A2b (T=10 s) | A3 (W1+L1) | macOS |
|---|---|---|---|---|
| first rebind, s after kill, min / median / max | 6.9 / 10.4 / 14.0 (3 runs) | 18.7 / 19.0 / 19.6 (3 runs) | 9.3 / 10.6 / 11.9 (2 runs) | 7-24 s |
| time from the rebind to the first heartbeat, s, min / median / max | 3.2 / 4.2 / 7.1 (18 pairs) | 2.3 / 3.7 / 17.0 (18 pairs) | 3.1 / 4.0 / 17.1 (12 pairs) | median 4.1 s |
| per pair, first heartbeat after the pair's stall, s | 13.1 / 19.7 / 145.5 (18) | 26.2 / 32.9 / 45.0 (18) | 15.2 / 17.2 / 32.0 (12) | not given |
| per run, all stalled pairs flowing from, s | 14.2 / 20.3 / 145.5 (3 runs) | 33.3 / 33.9 / 45.0 (3 runs) | 16.3 / 24.2 / 32.0 (2 runs) | not given |
| rebinds per member | 1-2 | 1 | 0-1 | not given |
| time to bind the new endpoint, ms | 3 / 4 / 8 | 2 / 3 / 3 | 3 / 3 / 4 | not given |
| false rebinds (before the kill) | 0 | 0 | 0 | not given |

- **Relapses (a second rebind):** 1 of 8 stalled W1 runs (a-1w1w-3: M1 1, M2 2, M3 1 rebinds; two of its pairs healed at 145.5 s, 12 gap episodes against 6). macOS: 5 of 13.
- **No-kill cell (A2c):** 0 rebinds in 3 runs, 18/18 pairs flowing. macOS: 0 rebinds in 3 runs, 18/18.
- The T=10 s arm rebinds about 8-9 s later than T=3 s at the median (19.0 against 10.4 s), as the longer silence threshold predicts.

## Differences from macOS, with n

1. **Relapse rate:** 1/8 stalled W1 runs on Linux, 5/13 on macOS; with these n a difference of this size is not established either way.
2. **A1 healed pairs:** 0/18 on Linux (3 runs); macOS 2/24, from one run in which two pairs healed at 64.1 and 83.1 s, so a macOS rate of 1 run in 5.
3. **Stall-free runs:** A0 1/3 and A3 1/3 on Linux had no stall (macOS A0 1/5, A3 0/5). The A3 run with no stall (a-1w1l1w-1) never exercised W1, so A3's Linux n is 2 stalled runs, not 3.
4. **Arms match macOS in every other cell:** the no-kill cell, the three diagnostic-transport arms, and the stall and heal outcome of W1 at both thresholds (Linux 18/18 and 18/18, macOS 30/30 and 16/16).

## What could make the comparison wrong

- n=3 per arm (2 for A3's rebind timing) against macOS n=3-5; the macOS values are the brief's table, which I did not re-derive from the macOS logs, and my A0, A1, A2, A3 arms were re-analysed on three runs, not five.
- The shipped-logs mix described above: the tables the brief's commands print are not Linux-only, and my rebuilt Linux-only analysis is the one the numbers here come from.
- The arms ran in a fixed order, one cell after another, from 00:02 to 01:28 UTC; I did not randomise the order. Load averages at each start were 0.00-1.66, and resident-anarchist's SSH work could have overlapped.
- The `p`-tags use the vendored, patched iroh build (`E14_FIX=drain` exported only for pw and pl12w, unset for pc); I did not diff the vendored patch against macOS's beyond the successful `patch` run, and the stock-behavior control (A4c) stalled as the unpatched arms did.
- Stall detection is the analyzer's (a gap of 5 s or more); "first rebind s" is the number the analyzer prints, which I read as seconds after the kill.
- Debug builds on loopback on one host, as in E10 and E12; different hardware (x86_64 VM against Apple M2 Max) and OS together.

## Files

- Report: `/home/lab/work/reports/linux-e15.md`
- Tables: `reports/raw/linux-e15-table.md`, `-runs.md`, `-delta.txt` (Linux only); `*-with-macos-runs-4-5.*` (mixed, kept for the record)
- Raw: `reports/raw/linux-e15/` (`logs-e15/` run logs, `cell-*.txt`, `cells.txt`, `uptime.txt`, `pgrep.txt`, `run-e15.sh`, `build-*.txt`, `vendor.txt`)
