# Linux run 3: E13 (own stdin reader, early departure) on Linux

lab-sibling, 2026-10-20, for resident-anarchist; brief `/home/lab/ra/linux-e13.md`.

## Answer

The reader works on Linux as on macOS. Departure went out at a median of 0 ms in all 12 cases, 10/10 each, with a maximum of 2 ms (eof-idle). Exit times are unchanged from Linux E11: eof with a call in flight exits at 5003 ms, SIGTERM bg with a call in flight at 2003 ms, and naive SIGTERM hangs 10/10 in all four stages, exiting 1 ms after stdin closes. Wire: 7/7 PASS on all five versions.

## Machine, toolchain, commit

- Same machine as `reports/linux-e11.md`: `Linux estafette-lab 6.8.0-138-generic #138-Ubuntu SMP PREEMPT_DYNAMIC Fri Jul 31 22:41:49 UTC 2026 x86_64`, 2 vCPU AMD EPYC-Rome VM, 3819 MiB RAM, Ubuntu 24.04.4
- `rustc 1.99.1 (58cf8f9c3 2026-10-13)`
- commit `5b58d1098de29812d978017abcbde4d758f1afa6` (`spike/e13-stdin`), tree clean in `spikes/e11-mcp`
- `cargo build --release`: 13.80 s wall, 0 warnings. The build was incremental, since dependencies were cached from the E11 build at e392d3b; only `e11-mcp` recompiled.
- Shutdown run: 320.05 s wall, exit 0. Raw output: `reports/raw/linux-e13-{build,wire,shutdown}.txt`.

## Wire

| version | PASS | FAIL | exit | macOS |
|---|---|---|---|---|
| 2024-11-05 | 7 | 0 | 0 | 7/7 PASS |
| 2025-03-26 | 7 | 0 | 0 | 7/7 PASS |
| 2025-06-18 | 7 | 0 | 0 | 7/7 PASS |
| 2025-11-25 | 7 | 0 | 0 | 7/7 PASS |
| 2026-07-28 | 7 | 0 | 0 | 7/7 PASS |

## Shutdown (`driver shutdown 10`), full table

| case | mode | departure ms min/med/max (n) | stopped ms (a departure after waiting() returns) | exit ms | exit ms after stdin closed (hung at cap) |
|---|---|---|---|---|---|
| eof-pre | naive | 0 / 0 / 1 (10/10) | - (0/10) | 1 / 1 / 2 (10/10) | - (0/10) |
| eof-idle | naive | 0 / 0 / 2 (10/10) | 0 / 0 / 2 (10/10) | 1 / 1 / 2 (10/10) | - (0/10) |
| eof-slow | naive | 0 / 0 / 0 (10/10) | 5001 / 5002 / 5002 (10/10) | 5001 / 5003 / 5003 (10/10) | - (0/10) |
| eof-coop | naive | 0 / 0 / 0 (10/10) | 5001 / 5001 / 5002 (10/10) | 5002 / 5003 / 5003 (10/10) | - (0/10) |
| term-pre | naive | 0 / 0 / 0 (10/10) | - (0/10) | - (0/10) | 1 / 1 / 1 (10/10) |
| term-idle | naive | 0 / 0 / 0 (10/10) | 0 / 0 / 0 (10/10) | - (0/10) | 1 / 1 / 1 (10/10) |
| term-slow | naive | 0 / 0 / 0 (10/10) | 2000 / 2002 / 2002 (10/10) | - (0/10) | 1 / 1 / 1 (10/10) |
| term-coop | naive | 0 / 0 / 0 (10/10) | 0 / 0 / 1 (10/10) | - (0/10) | 1 / 1 / 1 (10/10) |
| term-pre | bg | 0 / 0 / 0 (10/10) | - (0/10) | 1 / 1 / 1 (10/10) | - (0/10) |
| term-idle | bg | 0 / 0 / 0 (10/10) | 0 / 0 / 0 (10/10) | 1 / 1 / 1 (10/10) | - (0/10) |
| term-slow | bg | 0 / 0 / 0 (10/10) | 2001 / 2002 / 2002 (10/10) | 2002 / 2003 / 2003 (10/10) | - (0/10) |
| term-coop | bg | 0 / 0 / 0 (10/10) | 0 / 0 / 1 (10/10) | 1 / 1 / 2 (10/10) | - (0/10) |

eof-pre's last run exited with status 1 after `Error: ConnectionClosed("initialize request")`, with departure written 0.2 ms after stdin closed, before the error. All other last runs exited 0.

## Beside macOS (E13, release, n=10)

| measure | Linux | macOS |
|---|---|---|
| departure median, every case | 0 ms | 0 ms |
| departure max, stdin close | 2 ms (eof-idle) | 1 ms |
| departure max, SIGTERM | 0 ms | 3 ms |
| stopped, eof call in flight (slow / coop median) | 5002 / 5001 ms | 5003 ms |
| stopped, SIGTERM bg call in flight (slow) | 2002 ms | 2002 ms |
| exit, eof call in flight | 5003 ms (both) | 5004 ms |
| exit, SIGTERM bg call in flight | 2003 ms | 2003 ms |
| naive SIGTERM | hung 10/10 x4, exit 1 ms after stdin closes | hung 10/10, ~2 ms after stdin closes |
| wire | 7/7 PASS x5 | 7/7 PASS x5 |

Linux E11 (before the reader), for the exit columns: eof slow/coop 5003, bg slow 2002, naive SIGTERM hung 10/10, exit 1 ms after stdin closed. E13 leaves these unchanged, to within 1 ms.

## Differences

- Every difference is 1 ms or less in medians, or 1-3 ms in maxima. All of them are within the driver's 1 ms poll step and rounding, so none is a real difference.

## What could make the comparison wrong

- Departure is timed by when the driver reads the `departure` line from the child's stderr pipe. That adds pipe and thread-wakeup latency, and the times are rounded to whole ms. "0 ms" means under about 0.5 ms as the driver observed it; the last-run stderr shows +0.1 to +0.4 ms.
- The departure is a stub that only writes a line to stderr (`depart()` calls `eprintln!`). This measures when the reader notices EOF, or when SIGTERM is received, not a real broadcast's delivery time.
- In naive SIGTERM the departure goes out at 0 ms, but the process still hangs until stdin closes. The reader fixes notice, not the hang.
- The exit-time timer polls `try_wait` every 1 ms, and the median is the 6th of 10 sorted values; the same code ran on macOS.
- Incremental build: dependency artifacts came from the E11 build of the same Cargo.lock (rmcp 3.5.1, tokio 1.54.0). `git diff --stat e392d3b 5b58d10` touches only `src/main.rs` and `src/bin/driver.rs`, so Cargo.lock is unchanged.
- n=10, one session; the load was not recorded for this run (E10's cells ended at load 0.22, 12 minutes earlier). resident-anarchist's SSH work could have overlapped; I did not check.
- Different hardware and OS together (x86_64 VM, Linux 6.8 vs M2 Max, macOS 15.3.1); agreement does not attribute behaviour to one factor.
- Harness background runner, no TTY; the driver owns the child's stdio either way.
