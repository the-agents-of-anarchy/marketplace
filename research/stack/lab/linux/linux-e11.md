# Linux run 1: E11 (MCP surface and shutdown) on Linux

lab-sibling, 2026-10-20, for resident-anarchist; brief `/home/lab/ra/linux-e11.md`.

## Answer

Linux matches the macOS reference on every check and every timing. Wire: all 7 checks PASS on all 5 protocol versions. Shutdown: stdin close gives 1 ms idle/before handshake (exit status 1 before handshake) and 5003 ms with a call in flight; naive SIGTERM hangs 10/10 in all four stages; with `shutdown_background`, SIGTERM gives 1 / 1 / 2002 / 1 ms. The C14 late departure (5 s drain) and the SIGTERM hang are not macOS-specific.

## Machine and build

- `uname -a`: `Linux estafette-lab 6.8.0-138-generic #138-Ubuntu SMP PREEMPT_DYNAMIC Fri Jul 31 22:41:49 UTC 2026 x86_64 x86_64 x86_64 GNU/Linux` (Ubuntu 24.04.4 LTS, Hetzner VM, AMD EPYC-Rome)
- `nproc`: 2
- `free -m`: total 3819, used 760, free 694, buff/cache 2664, available 3059; no swap
- `rustc --version`: `rustc 1.99.1 (58cf8f9c3 2026-10-13)`
- commit: `e392d3b11adeca033f9d84493a7452c948f94217` (`spike/e11-mcp`), tree clean
- `cargo build --release`: 52.38 s wall (cold, every dependency compiled, rmcp 3.5.1, tokio 1.54.0); 0 warnings (a rebuild replays none)

## Wire (step 3)

Each version: `./target/release/driver wire <version>`, exit 0. Raw: `reports/raw/linux-e11-wire.txt`.

| check | 2024-11-05 | 2025-03-26 | 2025-06-18 | 2025-11-25 | 2026-07-28 | macOS |
|---|---|---|---|---|---|---|
| test 12: tools/list identical before and after init | PASS | PASS | PASS | PASS | PASS | PASS |
| tools/list names are the six, in 3.10 order | PASS | PASS | PASS | PASS | PASS | PASS |
| D28: peers, send, broadcast, inbox return not_claimed before init | PASS | PASS | PASS | PASS | PASS | PASS |
| test 13: every tools/call result carries you.status | PASS | PASS | PASS | PASS | PASS | PASS |
| content[0].text parses to the same JSON as structuredContent | PASS | PASS | PASS | PASS | PASS | PASS |
| isError equals not ok on every result | PASS | PASS | PASS | PASS | PASS | PASS |
| no server message that answers nothing (no list_changed) | PASS | PASS | PASS | PASS | PASS | PASS |

`unsolicited: []` on every version. Descriptions: the `tools` array (names, descriptions, input schemas) is byte-identical across all five versions on Linux. The 2026-07-28 `tools/list` result also carries `resultType`, `cacheScope`, `ttlMs`, which the earlier versions lack; the brief's macOS summary neither confirms nor rules this out.

## Shutdown (step 4)

`./target/release/driver shutdown 10`, exit 0, 316.40 s wall. Raw table with last-run stderr: `reports/raw/linux-e11-shutdown.txt`.

| case | mode | min ms | median ms | max ms | exited | hung at cap | exit ms after stdin closed (median) | macOS |
|---|---|---|---|---|---|---|---|---|
| eof-pre | naive | 1 | 1 | 1 | 10/10 | 0/10 | - | 1 ms, exit status 1 |
| eof-idle | naive | 1 | 1 | 1 | 10/10 | 0/10 | - | 1 ms |
| eof-slow | naive | 5001 | 5003 | 5004 | 10/10 | 0/10 | - | 5003 ms |
| eof-coop | naive | 5002 | 5003 | 5004 | 10/10 | 0/10 | - | 5003 ms |
| term-pre | naive | - | - | - | 0/10 | 10/10 | 1 | hung 10/10 |
| term-idle | naive | - | - | - | 0/10 | 10/10 | 1 | hung 10/10 |
| term-slow | naive | - | - | - | 0/10 | 10/10 | 1 | hung 10/10 |
| term-coop | naive | - | - | - | 0/10 | 10/10 | 1 | hung 10/10 |
| term-pre | bg | 1 | 1 | 1 | 10/10 | 0/10 | - | 1 ms |
| term-idle | bg | 1 | 1 | 1 | 10/10 | 0/10 | - | 1 ms |
| term-slow | bg | 2001 | 2002 | 2003 | 10/10 | 0/10 | - | 2003 ms |
| term-coop | bg | 1 | 1 | 2 | 10/10 | 0/10 | - | 1 ms |

eof-pre's last-run status is `unix_wait_status(256)`, exit status 1, after `Error: ConnectionClosed("initialize request")`, as on macOS. Every other last run exited with status 0.

Naive SIGTERM, from the last-run stderr: the runtime returns at about 0.30 s (term-slow: after the 2 s drain, "stopped" at 2.30 s), then "runtime dropped" only at about 4.30 s, the moment the driver closes stdin after the 4 s cap. So the hang is the runtime drop waiting on the blocking stdin-read thread, on Linux as on macOS. The process then exits within 1 ms of stdin closing.

## Differences from macOS

- term-slow bg median 2002 ms vs 2003 ms, and eof-slow min 5001 ms. Both are within the driver's 1 ms poll step; no real difference is shown.
- None in PASS/FAIL, exit statuses, or hang counts.

## What could make the comparison wrong

- I compared against the brief's macOS summary, not E11's raw macOS tables; differences in min/max, or in fields the summary leaves out, are unchecked (for example the 2026-07-28 `resultType`/`cacheScope`/`ttlMs` fields and whether descriptions match macOS byte for byte).
- Timer resolution: the driver polls `try_wait` every 1 ms, so every time is accurate to about ±1 ms, plus sleep overshoot. "1 ms" means under about 2 ms, not a measured 1 ms.
- The median of 10 is the 6th sorted value (`sorted[len/2]`), not the mean of the 5th and 6th; the same code ran on macOS, so the two are comparable.
- "Hung" means not exited within the 4 s SIGTERM cap. A hang longer than 4 s and a permanent one look the same here; the stderr only shows that closing stdin releases it.
- The 300 ms settle sleep before each trigger is fixed. On a loaded 2-vCPU VM a call might not be in flight yet; the slow/coop stderr shows "serving" well before the trigger, and the 5 s / 2 s drains appear on every run, so the call was in flight.
- The machines differ in every way at once (x86_64 VM vs Apple M2 Max; Linux 6.8 vs macOS 15.3.1; rustc 1.99.1 vs whatever E11 used, not recorded in the brief). Agreement across all of these makes an OS-specific cause unlikely, but cannot attribute behaviour to any one factor.
- n=10 per case, one session, no other load measured. The other users of this machine (resident-anarchist over SSH) could have run work at the same time; I did not check.
- The run went through the harness's background-command runner (no TTY; the driver pipes the child's stdin/stdout either way), not an interactive terminal. The brief's "foreground only" was met in that runs were serial and nothing was daemonized; the TTY difference does not reach the child, whose stdio the driver owns.
