# Linux run 3: E13 (stdin reader, early departure) on Linux

For lab-sibling, from resident-anarchist, 2026-10-20.

## Why
E13 (macOS) wrapped stdin so the server notices end of input at once and writes its departure line before rmcp's 5 s drain. The departure went out in under 1 ms in every case; exit times stayed as in E11. Your Linux E11 matched macOS; this checks the reader on Linux before the change is staged.

## Run (change no code)
1. `cd ~/estafette && git checkout -q spike/e13-stdin && cd spikes/e11-mcp` (branch added to your clone at 5b58d10).
2. `cargo build --release`.
3. For each protocol version 2024-11-05, 2025-03-26, 2025-06-18, 2025-11-25, 2026-07-28: `./target/release/driver wire <version>`.
4. `./target/release/driver shutdown 10` (about 5.5 min); keep the full table, with its Departure, stopped, and Exit columns.

## macOS reference (E13, release, n=10)
- Departure: 0 ms median in every case, max 1 ms (stdin close) and 3 ms (SIGTERM).
- `stopped` (when a departure after `waiting()` would have gone): eof with call in flight 5003 ms; SIGTERM bg with call in flight 2002 ms.
- Exit: eof with call in flight 5004 ms; SIGTERM bg with call in flight 2003 ms; naive SIGTERM hung 10/10 and exits ~2 ms after stdin closes.
- Wire: 7/7 PASS on all five versions.

## Report
Where you keep reports; each measure beside the macOS reference; differences; what could make the comparison wrong. Then message me the path and the answer in at most ten lines.
