# Linux run: E18 late attachment on Linux

lab-sibling, 2026-10-21, for resident-anarchist; brief `/home/lab/ra/linux-e18.md`.

## Answer

Same mechanism, same effect of the counters. In the baseline `x1cw` (n=8 runs), 6 of 24 first-generation rebound endpoints joined late, after 57.0-60.0 s (macOS 7 of 22, 57.4-60 s). In the traced case (`a-1x1cw-2802`, M3) the bootstrap node B2 held M3 in both its active and pending sets when the new Join arrived and sent no Neighbor; the wait ended at M3's own 60 s join timeout. The member-side counter (`x2cw`, join timeout 5 s) turned every late join into a 5.0 s wait (8 of 24 endpoints, all ending in JOIN_FAIL then rebind). The gossip-side fix (`x3cw`) had 0 late joins in 24 endpoints. No-kill controls: 0 rebinds.

## Setup

- Commit `85ef8a212df13ac16f03e04ec2efde76925b3ad4` (`spike/e18-attach`, from `/home/lab/ra/e18.bundle`); no source file changed, nothing committed in `~/estafette`.
- `rustc 1.99.1 (58cf8f9c3 2026-10-13)`; kernel `6.8.0-138-generic`, x86_64, 2 vCPU AMD EPYC-Rome VM, 3819 MiB RAM, Ubuntu 24.04.4; loopback.
- Build: `vendor.sh` (patch applied to `src/proto/hyparview.rs`, exit 0), then `cargo build --features a` in `e18-attach-gossip` 135.78 s; binary sha256 `1b82d24dad3548ce…`. `E18_LOGDIR=logs/e18-linux` exported for every cell, so the shipped `logs/e18` was never touched.
- 28 runs from 05:06:20 to 06:33:09 UTC in the brief's order, one every 3 min 5 s. Uptime before each batch (all in `reports/raw/linux-e18/uptime.txt`):

```
0 x1cw 2800 x1  05:06:20  load average: 2.00, 0.88, 0.38   (left over from the build)
1 x1cw 2801 x3  05:09:52  0.21, 0.60, 0.37
1 x2cw 2811 x3  05:19:07  0.65, 0.52, 0.42
1 x3cw 2821 x3  05:28:22  0.28, 0.25, 0.31
1 x1cw 2804 x3  05:37:38  0.26, 0.37, 0.34
1 x2cw 2814 x3  05:46:53  0.24, 0.29, 0.31
1 x3cw 2824 x3  05:56:08  0.50, 0.36, 0.31
1 x1cw 2807 x2  06:05:22  0.60, 0.49, 0.37
1 x2cw 2817 x2  06:11:32  0.45, 0.45, 0.38
1 x3cw 2827 x2  06:17:42  0.37, 0.40, 0.37
0 x2cw 2831 x3  06:23:53  0.17, 0.31, 0.34
```

- Deviation: my first wrapper script stopped after the control run 2800, because the `pgrep -fl "e10-a|e18-attach"` in `e18-run.sh` matched my own launching bash (its command line held that pattern), not a stray process; the run had finished and archived. I continued with the remaining 27 runs from a second script launched by a short command (`reports/raw/linux-e18/run-e18b.sh`). Each of the 27 printed `no stray` (the wrapper checked every batch); run 2800 did not, for the reason above, and `pgrep` before every later batch printed nothing. Logged as a failure in the records.

## Arms beside macOS

Linux from `table.md` (`reports/raw/linux-e18/`); macOS from the brief (n=8 per kill arm).

| Arm | tag | macOS first-gen late joins | macOS late-join wait | macOS all stalled pairs flowing from, median (min-max) | Linux first-gen late joins | Linux late-join wait (min / median / max) | Linux all stalled pairs flowing from, median (min-max) |
|---|---|---|---|---|---|---|---|
| A0 baseline | x1cw | 7/22 | 57.4-60 s | 78.7 s (33.3-94.7) | 6/24 | 57.0 / 59.3 / 60.0 s (n=6) | 75.5 s (22.1-85.1) |
| A1 join timeout 5 s | x2cw | 4/22 | 5 s | 38.0 s (30.1-58.2) | 8/24 | 5.0 / 5.0 / 5.0 s (n=8) | 30.6 s (24.1-78.1) |
| A2 on_join fix | x3cw | 0/24 | - | 31.5 s (21.1-33.9) | 0/24 | - | 27.1 s (21.0-35.2) |
| control, no kill | 0 x1cw | 0 rebinds | - | - | 0 rebinds (1 run) | - | - |
| A1 control, no kill | 0 x2cw | 0 rebinds in 3 | - | - | 0 rebinds (3 runs) | - | - |

Other `table.md` columns: all three kill arms stalled in 8 of 8 runs (48 stalled pairs each), all flowing at 180 s. A0: 26 rebound endpoints over all generations, 6 late joins, 2 of them ending in JOIN_FAIL (the other 4 joined at 57.0-59.9 s), rebinds per member 1-2. A1: 36 rebound endpoints, 8 late joins, 8 JOIN_FAIL, rebinds per member 1-3. A2: 25 rebound endpoints, 0 late joins, rebinds per member 1-2. In A0, two runs healed at 22.1 s and 22.2 s (no late join), the other six at 72.5-85.1 s.

## B2 timeline: first late join (`a-1x1cw-2802`, member M3)

The first late join in `joins.txt` is `a-1x1cw-2802 M3`: Join at 13.94 s after the kill, `JOIN_FAIL` after 60.00 s, then a second join at 73.95 s that succeeded in 0.06 s. Timeline saved as `reports/raw/linux-e18/b2-a-1x1cw-2802-M3.txt`, times in seconds after the kill (B2 is `8139770ea8`, M3 `91a28a0b74`).

- **B2's state for M3 at its Join (13.94 s):** M3 is in B2's active view and in its pending set: `E18 handle Join active=[M1, M3, M2] pending=[M3] from=M3`. (Before the kill, at -4.2 s, M3's first Join found `pending=[M2]` only and B2 added it to active and sent a Neighbor.)
- **Neighbor out:** no. The log line is `E18 send_neighbor … peer=M3 fresh=false`, and the only messages B2 sent at 13.94 s are `PeerData` and two `ForwardJoin`s (to M1 and M2); no `Neighbor` to M3. A fresh Neighbor (`fresh=true`) went out at both of M3's earlier joins (-4.20 s and, at 73.95 s, the new one).
- **After the Join:** the connection M3 opened at 13.94 s closes at 14.91 s (`connection lost: timed out`). B2's views keep M3 in both sets for the next 59 s (the 55.28 s `shuffle_timer` line still shows `pending=[M3]`).
- **What ended the wait:** at 73.89 s B2 sees the connection close (`closed by peer: 0`), logs `connection_closed … pending=[M3]` and `NeighborDown(M3)`, and its views drop M3. At 73.95 s M3's new Join arrives with `active=[M1, M2] pending=[]`; B2 adds M3 to active and sends a fresh Neighbor, and M3 is joined 0.06 s after its Join. That close comes 59.95 s after the Join, and M3's `JOIN_FAIL` is logged at 60.00 s after its join start, after which the harness rebinds; I read the close as M3's old endpoint closing, so the harness's 60 s join timeout ended the wait (inferred from these timestamps, not from M3's own log lines).

## Differences from macOS, with n

1. **A0 late joins:** 6 of 24 first-generation endpoints against 7 of 22; the wait range matches (57.0-60.0 s against 57.4-60 s). Of Linux's 6 late joins, 2 ended in JOIN_FAIL at 60.00 s and 4 in JOINED at 56.98-59.87 s; I traced only the first, not why the other 4 ended just before the timeout.
2. **A1 late joins:** 8 of 24 against 4 of 22 on macOS; every Linux late join waited exactly 5.0 s and ended in JOIN_FAIL (8 of 8; macOS 5 s). A1 needed more rebinds on Linux (1-3 per member, 36 rebound endpoints); one A1 run took 78.1 s to flow, the rest 24.1-34.1 s, so the maximum is 78.1 s against 58.2 s on macOS. The median is 30.6 s against 38.0 s.
3. **A2:** 0 of 24 late joins on both; median 27.1 s against 31.5 s, range 21.0-35.2 against 21.1-33.9 s.
4. **Controls:** equal, 0 rebinds.
5. At n=8 runs per arm, the A1 late-join counts (8/24 against 4/22) and the A0 and A2 median differences are within what individual runs vary by; I make no claim that the OS caused them.

## What could make the comparison wrong

- n=8 per kill arm, 1 and 3 in the controls; macOS values are the brief's table, not re-derived from macOS logs, and my first-generation denominators (24 each) differ from macOS's (22, 22, 24).
- The B2 timeline is one run and one member; the other five A0 late joins are not traced here.
- The build is the diagnostic one (vendored iroh-gossip 0.101.0 with state logging, `iroh_gossip=debug` tracing on every run); logging load could move timings relative to macOS. Debug build, loopback, one host, different CPU and OS from macOS at once.
- Batches interleaved the arms as the brief asked, in a fixed order, with no randomisation; load before each batch was 0.17-0.65 (1 minute) apart from the first, post-build run (2.00).
- Run 2800 did not print `no stray` (explained above), so its stray check rests on the script's own abort check in `run-cell.sh`, which did not trigger.
- resident-anarchist's SSH work could have overlapped; the load averages show no sustained load.

## Files

- Report: `/home/lab/work/reports/linux-e18.md`
- Raw: `/home/lab/work/reports/raw/linux-e18/` (`table.md`, `joins.txt`, `b2-a-1x1cw-2802-M3.txt`, `runs-log.txt`, `uptime.txt`, `pgrep.txt`, `run-e18.sh`, `run-e18b.sh`, `build-e18.txt`, `vendor.txt`, `logs/`)
