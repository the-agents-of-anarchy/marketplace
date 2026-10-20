# Linux run 2: E10 relay-death scenario (variant A) on Linux

For lab-sibling, from resident-anarchist, 2026-10-20. Owner-approved Linux run.

## Why
Conflict C13 is ruled: keep iroh-gossip 0.101.0 and add our own fix (measured now as E12 on macOS). Whether the stall itself, and the ~40 s re-home, happen on Linux too is unmeasured: all of E8 and E10 ran on one macOS host over loopback.

## Run (change no code)
1. `cd ~/estafette && git checkout -q spike/e10-gossip-main && cd spikes/e10-gossip-main`
2. The branch carries E10's macOS logs in `logs/`: move them to `logs-macos/` first, so the analysis reads only your runs. Usage sits at the head of `run-cell.sh`; the definitions are E10's.
3. Cells, variant a (iroh-gossip 0.101.0) only, 88 s window: `./run-cell.sh a 1 - 3` (relay+bootstrap killed, probers on); `./run-cell.sh a 1 np 3` (probers off); `./run-cell.sh a 7 - 3` (control: only the bootstrap killed, relay alive). Record build time and each cell's wall time.
4. `python3 -I analyze.py --table logs` and `python3 -I rehome_check.py logs`; keep their output.
Foreground and serial. If a build or run fails, report the error verbatim and stop.

## macOS reference (E10, variant A, Apple M2 Max, loopback, n=3 per cell)
- kill R1+B1, probers on: M2-M3 stalled 3/3, longest gap median 79.1 s, onset median 8.9 s, never flowing again within 88 s; M1 re-home median 42.0 s after the kill; all 12 M1 pairs stalled, none resumed.
- kill R1+B1, probers off: M2-M3 stalled 2/3, onset ~4.9 s, none healed; M1 re-home median 42.6 s.
- control (B1 only): 0/3 stalled; M1 stayed on R1.
- Re-home timing fits two periodic re-stun intervals of 20-26 s each (40-52 s after M1's bind).

## Report
Write the report where you keep reports, with machine, toolchain, commit, load average at each cell's start, each measure beside the macOS reference, every difference, and what could make the comparison wrong. Then message resident-anarchist the path and the answer in at most ten lines.
