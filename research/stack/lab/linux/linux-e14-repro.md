# Linux run: the single-file E14 bug-report repro

lab-sibling, 2026-10-20, for resident-anarchist; brief `/home/lab/ra/linux-e14-repro.md`.

## Answer

The failure reproduces on Linux, but not on every run. With burst 200 and the dead relay, the stock build (iroh 1.3.0) failed 19/20 and the iroh main build (rev 55908a5) failed 18/20; macOS: 20/20 FAIL for both. The controls pass (no kill 10/10, burst 0 10/10, burst 64 5/5). Both candidate fixes passed 20/20 (`drain`, `drop`), and the patched build without a fix failed 5/5. The runs that passed had 0 failed dials and a first success at 0 ms, so the stall did not start in those runs.

## Setup

- Commit `983118f3fcb4727d798e9e170a266a0e8bc25455` (`spike/e14-bug-report`, fetched from `/home/lab/ra/e14-report.bundle`); no source file changed.
- `rustc 1.99.1 (58cf8f9c3 2026-10-13)`; kernel `Linux 6.8.0-138-generic #138-Ubuntu SMP PREEMPT_DYNAMIC Fri Jul 31 22:41:49 UTC 2026 x86_64`; 2 vCPU AMD EPYC-Rome VM, 3819 MiB RAM, Ubuntu 24.04.4; loopback.
- Uptime lines (`reports/raw/linux-e14-repro/uptime.txt`):

```
first 22:09:46  22:09:46 up  4:36,  3 users,  load average: 1.67, 0.85, 0.41
last  22:27:29  22:27:29 up  4:54,  3 users,  load average: 0.46, 0.83, 0.62
```

The first line's load of 1.67 is left over from the stock build that ended 2 minutes earlier.
- Builds, all `cargo build --quiet`: stock 147.07 s, main 127.53 s (the fetch from GitHub succeeded; `Cargo.lock` pins iroh at `55908a5809b61c72ec8deeff024038f4a9d68ab7`), patched 153.21 s after `sh vendor.sh` (1.92 s, `patching file src/socket/transports/relay/actor.rs`, exit 0). No build error and no warning in any build output.
- `pgrep -fa e14-repro` printed nothing after the last run.
- Deviation: I ran the commands from two wrapper scripts (`run-stock.sh`, `run-rest.sh` in `reports/raw/linux-e14-repro/`) in the brief's order; nothing else changed.

## Results

Counts from `cut -d' ' -f2 <file> | sort | uniq -c`. Every file has the expected number of RESULT lines; none is missing.

| file | runs | PASS | FAIL | macOS expectation |
|---|---|---|---|---|
| stock-b200 | 20 | 1 | 19 | 20 FAIL |
| stock-nokill | 10 | 10 | 0 | 10 PASS |
| stock-b0 | 10 | 10 | 0 | 10 PASS |
| stock-b64 | 5 | 5 | 0 | PASS |
| stock-b100 | 5 | 2 | 3 | FAIL |
| stock-rebind | 3 | 1 | 2 | PASS (first_ok_after_burst_ms about 7400) |
| main-b200 | 20 | 2 | 18 | 20 FAIL |
| patched-drain | 20 | 20 | 0 | 20 PASS |
| patched-drop | 20 | 20 | 0 | 20 PASS |
| patched-stock | 5 | 0 | 5 | 5 FAIL |

Fields of each RESULT line:

- stock-b200: the 19 FAIL runs all show `failed_dials=4 first_ok_after_burst_ms=None wait_secs=15`; the PASS run (the 14th) shows `failed_dials=0 first_ok_after_burst_ms=Some(0)`.
- main-b200 (`--wait-secs 8`): the 18 FAIL runs show `failed_dials=2 first_ok_after_burst_ms=None`; the two PASS runs (the 4th and 10th) show `failed_dials=0`, `Some(0)`.
- stock-b100 (`--wait-secs 5`): FAIL runs show `failed_dials=2`, `None`; the PASS runs (the 2nd and 5th) show `failed_dials=0`, `Some(0)`.
- patched-drain and patched-drop: all 40 runs `failed_dials=0 first_ok_after_burst_ms=Some(0)`. patched-stock: all 5 `failed_dials=2`, `None`.
- stock-nokill, stock-b0, stock-b64: all `failed_dials=0`, `Some(0)`.

### Rebind runs (`--rebind-on-fail`, 3 runs)

| run | RESULT | failed_dials | first_ok_after_burst_ms |
|---|---|---|---|
| 1 | PASS | 0 | Some(0) |
| 2 | FAIL | 1 | Some(5446) |
| 3 | FAIL | 1 | Some(5454) |

macOS expectation: PASS with first_ok_after_burst_ms about 7400. In the source (`src/main.rs`, `let pass = fails == 0 && first_ok.is_some();`) a run passes only with zero failed dials, so a rebind run that recovers after one failed dial prints FAIL. Runs 2 and 3 recovered, 5.4 s after the burst, and are labelled FAIL by that rule; run 1 had no failed dial, so the rebind never triggered. I did not keep the full `T +…` lines (the brief pipes through `grep RESULT`), so I have no per-dial timeline.

## Differences from macOS

1. **Stall-free runs.** Of 48 runs that kill R1 and send a burst of at least 100 (stock-b200 20, main-b200 20, stock-b100 5, rebind 3), six had no failed dial: stock-b200 1, main-b200 2, stock-b100 2, rebind 1. macOS had 0/40 for b200 stock and main (the brief gives no count for b100 or rebind beyond the verdict). With n=20 a single 19/20 against 20/20 is not distinguishable from chance; the three non-failing b200 runs among 40 (7.5%) against 0/40 is suggestive but not established.
2. **b100:** 3/5 FAIL on Linux; the brief's macOS expectation is FAIL without a count.
3. **Rebind:** two recoveries at 5.4 s against about 7.4 s on macOS; one run never stalled. Pass labels differ for the reason given above.
4. The controls and both fixes match macOS: `no-kill`, `burst 0`, `burst 64`, `drain` and `drop` all passed every run; the patched build without a fix failed 5/5.

## What could make the comparison wrong

- The runs inside each file went back to back; I did not randomise order. The stall-free runs fall at positions 14 (stock-b200), 4 and 10 (main-b200), 2 and 5 (b100) and 1 (rebind), not only in the first run after a build, but I did not test whether run order matters.
- No per-run trace was kept, so I cannot say why the stall-free runs did not stall (for example, whether the burst's datagrams went out before R1 closed).
- n is 20 or fewer per file. macOS counts are the brief's stated expectations; I did not read macOS's raw logs for this task.
- The stock-b200 files use `wait_secs=15` and the main and patched ones `wait_secs=8`, as the brief asked; `failed_dials` differs (4 against 2) because of that window.
- Different machine in every respect at once (x86_64 VM against Apple M2 Max; Linux 6.8 against macOS 15), debug builds, loopback. `Cargo.lock` pins the same iroh 1.3.0 and main rev as the brief; I did not diff dependencies against the macOS build.
- Load averages were 0.46-1.67 at the two recorded points; I did not record uptime before each file. resident-anarchist's SSH work could have overlapped.
- I did not verify that the vendored patch matches the macOS patch beyond the successful `patch` run.

## Files

- Report: `/home/lab/work/reports/linux-e14-repro.md`
- Raw: `/home/lab/work/reports/raw/linux-e14-repro/` (`stock-*.txt`, `main-b200.txt`, `patched-*.txt`, `uptime.txt`, `build-*.txt`, `vendor.txt`, `run-stock.sh`, `run-rest.sh`)
