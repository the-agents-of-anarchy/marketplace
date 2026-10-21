# Linux run: E21 self-announcing hosts on Linux

lab-sibling, 2026-10-21, for resident-anarchist; brief `/home/lab/ra/linux-e21.md`.

## Answer

Same outcome as macOS on every arm. A host C that starts late and announces itself is learned by all members within 163 ms (n=5 runs) with no rebind before the kill. When host A dies, all 15 members rebound once and rejoined through BC, all stalled pairs were flowing from 6.8-6.9 s, and none of the 5 runs had a second rebind. The static-C controls were far slower (z0w median 75.2 s, z6w 19.2 s) and z5w never stalled. The 5 unit tests pass. Saved hosts: M3 restarted with the file rejoined and exchanged heartbeats; without the file it never joined (5 JOIN_FAIL). Differences are in speed: joins take 58-144 ms against 9-14 ms on macOS, learning takes 136-163 ms against 24-114 ms, and some first heartbeats come about 1.04 s after the rebound (3 of 15 rebound members, 2 of 5 new members).

## Setup

- Commit `bb66277942bfab6d43ad3c080bcfe817ebb54c40` (`spike/e21-hosts`, from `/home/lab/ra/e21.bundle`); no source file changed, nothing committed in `~/estafette`.
- `rustc 1.99.1 (58cf8f9c3 2026-10-13)`; kernel `6.8.0-138-generic`, x86_64, 2 vCPU AMD EPYC-Rome VM, 3819 MiB RAM, Ubuntu 24.04.4; loopback.
- Build: `vendor.sh` (exit 0), then `cargo build --features a` in `e18-attach-gossip` 12.21 s (incremental); binary sha256 `0cb02102c2e10138…`. Test: `cargo test --features a e21` gave `test result: ok. 5 passed; 0 failed; 0 ignored; 0 measured; 0 filtered out; finished in 0.05s`.
- `E21_LOGDIR=logs/e21-linux` exported, the counter variables unset, batches launched from a script file (`reports/raw/linux-e21/run-e21.sh`).
- 22 runs (20 of scenario 8, 2 of scenario 9) from 09:09:20 to 10:16:42 UTC in the brief's order; every run printed `no stray` (22 of 22) and `pgrep -fl "e10-a|e18-attach"` printed nothing before every batch.
- Uptime before the first and the last batch (all 18 in `reports/raw/linux-e21/uptime.txt`):

```
8 z0w 2900 x1  09:09:20  load average: 0.29, 0.14, 0.18
9 z4w 2941 x1  10:15:45  load average: 1.42, 0.63, 0.45
```

Load at the start of the other batches was 0.11-1.16 (1 minute).

## Results beside macOS

Linux from `table.md`, the per-arm `runs-*.txt`, `h2.txt`, `h3.txt`, `h1gap.txt` and `saved-with-file.txt` (`reports/raw/linux-e21/`). macOS from the brief.

| What | tag | macOS | Linux |
|---|---|---|---|
| H1: C start to every member having RC and BC | z1w | 24-114 ms; home moved to RC in 11/15 members; 0 rebinds before the kill | 136-163 ms (per member 126-163 ms, n=5 runs); home moved to RC in 6/15 members, 204-208 ms after learning; 0 rebinds before the kill in 5/5 runs |
| H2: kill A, arm (C learned at runtime) | z1w | 15/15 members rebound once, rejoined through BC in 9-14 ms; all stalled pairs flowing from 5.9-7.0 s; 0/5 second rebinds | 15/15 members rebound once (1/1/1 in every run), REBOUND to JOINED 73-144 ms; flowing from 6.8, 6.9, 6.9, 6.9, 6.9 s; 0/5 second rebinds; 0 JOIN_FAIL |
| H2 control: C static, homes R1/R1/R1 | z0w | 12.4-81.7 s, median 64.5 s; 3/5 second rebinds | 13.2 / 75.2 / 89.2 s (75.2, 79.3, 13.2, 68.7, 89.2); second rebinds in 4/5 runs |
| H2 control: C static, homes R1/R2/R2 | z6w | 15.0-83.1 s, median 18.1 s; 1/5 second rebinds | 13.1 / 19.2 / 81.5 s (27.2, 81.5, 19.2, 13.1, 18.1); second rebinds in 1/5 runs |
| H2 control: C static, homes R2/R2/R2 | z5w | never stalled, 0 rebinds | never stalled, 0 rebinds in 5/5 runs |
| H3: new member knowing only BC, A dead | z1w (M4) | joined in 9-11 ms; heartbeats from all three in 105-216 ms | joined in 58-65 ms; heartbeats from all three in 113-147 ms in 3 runs and 1043-1044 ms in 2 runs; first heartbeat from any member 77-102 ms; no M4 rebind, no JOIN_FAIL |
| H4: false records | unit tests | 5 tests pass | 5 passed, 0 failed |
| Saved hosts, M3 restart with the file | 9 z2w | joined in 9 ms, heartbeats resume | JOINED ms=63 (81 ms after the restart); first heartbeat from M1 2740 ms and from M2 2701 ms after the restart; 43 heartbeats from each within 45 s |
| Saved hosts, M3 restart without the file | 9 z4w | never joined, 5 JOIN_FAIL | never joined, 5 JOIN_FAIL (at 5.0, 13.0, 21.0, 29.0 and 37.0 s), no heartbeat from M1 or M2 |

Other columns:

- `table.md` (Linux, runs / runs stalled / stalled pairs flowing at 180 s): z1w 5 / 5 / 30 of 30; z0w 5 / 5 / 30 of 30; z6w 5 / 5 / 30 of 30; z5w 5 / 0 / none stalled. First-generation late joins: z1w 0 of 15 endpoints, z0w 12 of 15, z6w 3 of 15, z5w 0; JOIN_FAIL ends (all generations): z1w 0, z0w 96, z6w 24, z5w 0; every late join waited 5.0 s; rebinds per member z1w 1-1, z0w 1-11, z6w 1-9, z5w 0-0.
- z0w runs with second rebinds: a-8z0w-2900 (9/8/8 rebinds M1/M2/M3), 2901 (9/9/9), 2903 (8/8/8), 2904 (11/10/11); 2902 had 1/1/1 and flowed from 13.2 s. z6w: a-8z6w-2921 (9/9/9, flowed from 81.5 s); the other four had 1/1/1.
- H1 detail: the maximum member-pair heartbeat gap between C start and the kill was 1005-1008 ms in every run, with 0 failed probes (`h1gap.txt`).
- H2 detail (`h2.txt`): kill to REBIND 2.7-2.8 s for all 15 members; REBOUND to the B2 `NeighborUp` 68-130 ms; REBOUND to first heartbeat 119-216 ms for 12 members and 1030-1066 ms for 3 (a-8z1w-2911 M3, 2912 M2, 2913 M2); `PROBE_RELAYS down` named the dead relay in every row.

## Differences from macOS, with n

1. **Learning C (H1):** 136-163 ms on Linux against 24-114 ms (5 runs); home moved to RC in 6 of 15 members against 11 of 15. Each Linux move came about 205 ms after the member learned of RC.
2. **Join times:** REBOUND to JOINED 73-144 ms (15 members) against 9-14 ms; M4's join 58-65 ms (5 runs) against 9-11 ms; the saved-hosts join 63 ms. First joins before the kill in these runs' logs also take 57-71 ms (a-8z5w-2930, a-8z1w-2910), so I read this as this machine's join latency, not an effect of announcing hosts; I did not test it separately.
3. **First heartbeats of about 1.04 s:** 3 of 15 H2 members (1030-1066 ms) and 2 of 5 H3 runs (1043-1044 ms until all three are heard) against macOS 105-216 ms. I did not look into what sets the 1.04 s.
4. **z0w control:** second rebinds in 4 of 5 runs (8-11 rebinds per member, 21-29 JOIN_FAIL in each) against 3 of 5; flowing from 13.2 to 89.2 s against 12.4 to 81.7 s. z6w: 1 of 5 on both, 13.1-81.5 s against 15.0-83.1 s. z5w: equal.
5. **Unchanged from macOS:** the self-announcing arm heals in about 6.9 s in all 5 runs with no second rebind, against the controls' tens of seconds; H4 passes 5 of 5; saved hosts rejoin with the file and fail without it (5 JOIN_FAIL in both).

## What could make the comparison wrong

- n=5 runs per scenario-8 arm and 1 run per saved-hosts case; macOS values are the brief's table, not re-derived from macOS logs. The z0w second-rebind count (4/5 against 3/5) and the H1 home-move count (6/15 against 11/15) are within what small n allows; the H1 and join-time differences could come from machine speed or debug-build tracing.
- The saved-hosts heartbeat times are first heartbeats after the restart as `analyze_e21_hbafter.py` prints them, not join times; the brief gives macOS only a join time for z2w. I ran the same script on z4w for the no-heartbeat check (`saved-without-file.txt`); the brief does not ask for it.
- The control arms and the self-announcing arm run with the combined workaround, as the brief says; z0w and z6w show many repeated 5 s join timeouts, which I report as measured.
- Batches interleaved z0w and z1w, then ran z6w, z5w and the saved-hosts cases in a fixed order with no randomisation; debug build with gossip state logging, loopback, one host; different CPU and OS from macOS at once; resident-anarchist's SSH work could have overlapped (load before batches 0.11-1.42).

## Files

- Report: `/home/lab/work/reports/linux-e21.md`
- Raw: `/home/lab/work/reports/raw/linux-e21/` (`table.md`, `runs-z1w.txt`, `runs-z0w.txt`, `runs-z6w.txt`, `runs-z5w.txt`, `h2.txt`, `h3.txt`, `h1gap.txt`, `saved-with-file.txt`, `saved-without-file.txt`, `runs-log.txt`, `uptime.txt`, `pgrep.txt`, `run-e21.sh`, `build-e21.txt`, `test-e21.txt`, `vendor.txt`, `logs/`)
