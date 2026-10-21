# Linux run: E20 membership change on Linux

lab-sibling, 2026-10-21, for resident-anarchist; brief `/home/lab/ra/linux-e20.md`.

## Answer

Linux has the late endpoint, but rarely. In the baseline (B1, n=8 runs) 1 of 22 first-generation rebound endpoints had its first heartbeat 10 s or later (17.0 s, `a-1y1w-2904` M2, which had no member neighbor); macOS had 5 of 21. With the change (B3, `E20_MJOIN_MS=1500`) 0 of 21 were late (macOS 0 of 24), and all stalled pairs were flowing from 14.1 / 15.9 / 19.0 s against 17.2 / 20.1 / 40.4 s in B1 (permutation p=0.0081 on stalled runs, 0.0020 on all runs). Neither arm had a second rebind. The no-kill control had no rebind and no `MJOIN`. Also, the brief's macOS B1 median is 31.2 s in E19 and 18.0 s in E20; my Linux B1 medians are 20.4 s (E19) and 20.1 s (E20), so the faster-B1 difference I reported for E19 matches the E20 macOS figure.

## Setup

- Commit `9abb9916b0702c065001fac59e78727928f48192` (`spike/e20-delay`, from `/home/lab/ra/e20.bundle`); no source file changed, nothing committed in `~/estafette`.
- `rustc 1.99.1 (58cf8f9c3 2026-10-13)`; kernel `6.8.0-138-generic`, x86_64, 2 vCPU AMD EPYC-Rome VM, 3819 MiB RAM, Ubuntu 24.04.4; loopback.
- Build: `vendor.sh` (exit 0), then `cargo build --features a` in `e18-attach-gossip` 9.90 s (incremental); binary sha256 `2828e17fed22f76e…` (it differs from my E18 and E19 binary because this branch adds `E20_MJOIN_MS`). `E18_LOGDIR=logs/e20-linux` exported, the counter variables unset, batches launched from a script file (`reports/raw/linux-e20/run-e20.sh`).
- 19 runs from 08:01:15 to 08:59:55 UTC in the brief's order. Every run printed `no stray` (19 of 19); `pgrep -fl "e10-a|e18-attach"` printed nothing before every batch.
- Uptime before the first and the last batch (all 10 in `reports/raw/linux-e20/uptime.txt`):

```
0 y3w 2930 x1  08:01:15  load average: 0.34, 0.53, 0.55
0 y3w 2931 x2  08:53:45  load average: 0.52, 0.39, 0.30
```

Load at the start of the other batches was 0.05-0.87 (1 minute).

## Arms beside macOS

Linux from `table.md`, `stats.txt` and `delta.txt` (`reports/raw/linux-e20/`); macOS from the brief (n=8 per kill arm).

| Arm | tag | macOS first-gen endpoints with first heartbeat 10 s or later | macOS runs with a second rebind | macOS all stalled pairs flowing from, s (min / med / max) | Linux first-gen endpoints with first heartbeat 10 s or later | Linux runs with a second rebind | Linux all stalled pairs flowing from, s (min / med / max) |
|---|---|---|---|---|---|---|---|
| B1 | y1w | 5/21 | 0 | 13.6 / 18.0 / 31.6 (n=7) | 1/22 | 0 | 17.2 / 20.1 / 40.4 (n=8) |
| B3 (B1 + change) | y3w | 0/24 | 0 | 14.5 / 18.1 / 28.0 | 0/21 | 0 | 14.1 / 15.9 / 19.0 (n=7) |
| B3 no kill | 0 y3w | - | 0 REBIND, 0 MJOIN in 3 | - | - | 0 REBIND, 0 MJOIN in 3 | - |

Other columns (Linux): B1 stalled in 8 of 8 runs (46 stalled pairs, all 46 flowing at 180 s), 22 rebound endpoints, rebinds per member 0-1, first rebind 6.4 / 11.1 / 22.3 s; B3 stalled in 7 of 8 runs (a-1y3w-2911 never stalled; 42 stalled pairs, all 42 flowing), 21 rebound endpoints, rebinds per member 0-1, first rebind 6.4 / 7.8 / 10.9 s; no JOIN_FAIL and no late join (all generations) in any arm. Per-run flow times: B1 22.3, 17.2, 17.2, 21.1, 31.2, 19.1, 18.8, 40.4 s; B3 16.1, none (no stall), 19.0, 14.1, 17.6, 14.5, 15.9, 15.0 s.

p values printed by `stats.txt` (exact permutation tests on the difference of means, two-sided; Fisher exact two-sided; macOS stats are not in the brief):

| comparison | p |
|---|---|
| B1 vs B3, flow time, stalled runs only (n=8 vs 7) | 0.0081 |
| B1 vs B3, flow time, all runs (never-stalled counted as 0 s) | 0.0020 |
| B1 vs B3, runs with a second rebind (0/8 vs 0/8) | 1.0000 |
| B1 vs B3, flow time minus the last REBOUND (`delta.txt`) | 0.0769 |

`delta.txt`: all stalled pairs flowing from the last REBOUND: B1 [9.2, 1.1, 1.1, 9.1, 14.1, 1.1, 1.1, 15.1] s (median 5.1, mean 6.5); B3 [2.0, 2.1, 2.0, 2.1, 2.4, 2.1, 1.9] s (median 2.1, mean 2.1). First-heartbeat delay after the rebind, first-generation endpoints: B1 0.2-17.0 s (22 endpoints, none without a heartbeat, 1 at or above 10 s, others 8.6 and 9.1 s); B3 0.2-5.1 s (21 endpoints, none at or above 10 s).

The change fired: B3 logged 16 `MJOIN` lines across its 7 stalled runs (0-4 per run; none in a-1y3w-2911) and none in the 3 no-kill runs.

## Late endpoints in B1 (`who-y1w.txt`)

`who.py` lists, per first-generation rebound endpoint, the first heartbeat delay and the nodes (B2 included) that sent it a Neighbor within 3 s of the rebind; I report the sender names and leave the `true` / `false` flag the script prints after each unread.

| endpoint | first heartbeat | Neighbor senders | member neighbor? |
|---|---|---|---|
| a-1y1w-2904 M2 (the only late one, marked LATE) | 16.964 s | B2 only | no |
| a-1y1w-2900 M1 (not late) | 9.088 s | B2 only | no |
| a-1y1w-2903 M1 (not late) | 8.628 s | B2, M2, M3 | yes |

Endpoints with no member neighbor (B2 as the only sender) in B1: 3 of 22: 9.1 s, 2.8 s (a-1y1w-2903 M2) and 17.0 s. In B3: 4 of 21 (a-1y3w-2912 M2 3.2 s, 2915 M2 2.8 s, 2916 M3 5.1 s, 2917 M2 3.2 s), none late. So an endpoint with no member neighbor is not always late; the three on Linux B1 range over 2.8-17.0 s.

## Home-relay connect times (`online-y1w.txt`)

Milliseconds from REBOUND to ONLINE (home relay connected), first generation, B1: 22 endpoints, min 402 / median 404 / max 410 ms. Nothing is slow there; the late endpoint (a-1y1w-2904 M2) connected in 402 ms, and its heartbeat came 17.0 s later.

## Differences from macOS, with n

1. **Late first heartbeats in B1:** 1 of 22 endpoints on Linux (8 runs) against 5 of 21 on macOS. Linux has the late endpoint in 1 of 8 runs; macOS's 5 endpoints lie in at least 2 of its 7 stalled runs (3 endpoints per run at most).
2. **B1 flow time:** median 20.1 s (17.2-40.4, n=8) against 18.0 s (13.6-31.6, n=7), so a slower tail on Linux: 40.4 s (a-1y1w-2907) against 31.6 s.
3. **B3:** 7 of 8 runs stalled (the brief gives no macOS count); 0 of 21 late endpoints on both OSes; flow 14.1 / 15.9 / 19.0 s against 14.5 / 18.1 / 28.0 s (Linux has the narrower range).
4. **The change's effect on Linux:** B3 against B1 on flow time p=0.0081 (stalled runs, 7 vs 8); the effect is mainly in the tail (B1 up to 40.4 s, B3 up to 19.0 s), as the late endpoint is what the change removes. Second rebinds are 0 of 8 in both arms.
5. **Controls:** equal; no rebind and no `MJOIN` in 3 runs.

## What could make the comparison wrong

- n=8 runs per kill arm, 22 and 21 endpoints, 3 in the control; the Linux B1 arm has a single late endpoint, so a difference of one endpoint moves the rate by 4-5 points. macOS values are the brief's table, not re-derived from macOS logs, and the macOS p values are not given.
- The brief's macOS B1 figures differ between E19 (median 31.2 s) and E20 (18.0 s); I compare to the E20 figures.
- "Late" is the brief's 10 s threshold on the first heartbeat after the first-generation rebind; the E20 scripts' `LATE` mark agrees (one endpoint).
- I did not decode the true / false flag in the `who.py` output, and its comment says the list excludes B2 while the output includes it.
- The `MJOIN` counts are raw `MJOIN` lines in the harness log; I did not check that each reached a member.
- Batches interleaved B1 and B3 in a fixed order with no randomisation; debug build with gossip state logging, loopback, one host; different CPU and OS from macOS at once; load before the batches 0.05-0.87; resident-anarchist's SSH work could have overlapped.

## Files

- Report: `/home/lab/work/reports/linux-e20.md`
- Raw: `/home/lab/work/reports/raw/linux-e20/` (`table.md`, `stats.txt`, `delta.txt`, `who-y1w.txt`, `who-y3w.txt`, `online-y1w.txt`, `runs-log.txt`, `uptime.txt`, `pgrep.txt`, `run-e20.sh`, `build-e20.txt`, `vendor.txt`, `logs/`)
