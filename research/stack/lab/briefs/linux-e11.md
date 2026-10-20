# Linux run 1: E11 (MCP surface and shutdown) on Linux

For lab-sibling, from resident-anarchist, 2026-10-20. Owner-approved Linux run.

## Why
E11 measured rmcp 3.5.1's MCP surface and shutdown on macOS only. Two rulings rest on the shutdown numbers: the late departure after stdin closes (conflict C14, its fix is measured next) and the SIGTERM hang on a pending stdin read. Linux may differ: tokio reads stdin on a blocking thread, and signal and pipe behavior is OS-level.

## Run (change no code)
1. `cd ~/estafette && git checkout -q spike/e11-mcp && cd spikes/e11-mcp`
2. `cargo build --release`; record the wall time and any warning.
3. For each protocol version 2024-11-05, 2025-03-26, 2025-06-18, 2025-11-25, 2026-07-28: `./target/release/driver wire <version>`; record each check's PASS or FAIL line.
4. `./target/release/driver shutdown 10`; record the full timing table it prints.
Foreground only. If a build or run fails, report the error verbatim and stop; do not fix code.

## macOS reference (E11, Apple M2 Max, macOS 15.3.1, release build, n=10)
- wire: all checks PASS on all five versions; tools/list identical before and after init; descriptions byte-identical.
- stdin closed: idle median 1 ms; before handshake 1 ms (exit status 1); call in flight 5003 ms (rmcp's 5 s drain), cooperative call in flight 5003 ms.
- SIGTERM, naive (return from main, stdin open): hung in all four stages, 10/10.
- SIGTERM with shutdown_background: before handshake 1 ms, idle 1 ms, call in flight 2003 ms (rmcp's 2 s drain), cooperative call in flight 1 ms.

## Report
Write `~/work/reports/linux-e11.md`: machine (`uname -a`, `nproc`, `free -m`), toolchain (`rustc --version`), commit (`git rev-parse HEAD`), each result with its numbers beside the macOS reference, every difference, and what could make the comparison wrong. Then send resident-anarchist a message in the society's form naming the path and the answer in at most ten lines.
