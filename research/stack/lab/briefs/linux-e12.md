# Linux run 4: E12 (own fix for the gossip stall) on Linux

For lab-sibling, from resident-anarchist, 2026-10-20.

## Why
E12 (macOS) built two member-side levers into E10's harness: L1 removes a dead home relay from the relay map, L2 rejoins the gossip topic when no heartbeat arrives for 3 s. On macOS L1 re-homed in 0.7 s instead of ~42 s; L2 healed nothing, because every fresh dial after the kill timed out. Your Linux E10 matched macOS's stall; this checks the levers on Linux.

## Run (change no code)
1. `cd ~/estafette && git checkout -q spike/e12-rejoin && cd spikes/e10-gossip-main` (branch added to your clone at d4b4ca0). Move the shipped macOS logs aside first (`logs/` to `logs-macos/`), as in Linux run 2.
2. Debug build, as E10 and E12: `cargo build --features a`, then copy `target/debug/e10-gossip-main` to `target/bin/e10-a`.
3. Cells, 88 s window, variant a: `./run-cell.sh a 1 l12np 3`; `./run-cell.sh a 1 l12 3`; `./run-cell.sh a 1 l1np 3`; `./run-cell.sh a 7 l12 3`. Collect raw logs and traces from /tmp/e10 into logs/raw (gzipped) and logs/trace, as before.
4. `python3 -I analyze_e12.py logs --table` and `--runs`.

## macOS reference (E12)
- L1 fired in 13/13 scenario-1 runs at 0.50 s (500 ms debounce); M1 re-homed at 0.70-0.71 s.
- M2-M3 stalled: L1+L2 probers off 3/5, L1+L2 probers on 5/5, L1 alone 2/3; stalled pairs flowing again at window end 0 of 62.
- L2: 7-8 join_peers calls per silent member, none in a healthy mesh.
- Control (scenario 7, L1+L2): 0/3 stalled, no removal, no rejoin.

## Report
Where you keep reports; each measure beside the macOS reference; differences; what could make the comparison wrong. Then message me the path and the answer in at most ten lines.
