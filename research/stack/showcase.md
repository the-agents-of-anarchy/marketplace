# Showcase: two days of stack research (2026-10-20 and 2026-10-21)

Diagrams are rendered to PNG with merman-cli 0.9.1 (commons tip; `merman-cli render -f png -b white -s 2`); the Mermaid sources sit beside them in showcase/.

For the owner, read cold. Every figure here comes from a report under research/stack/; the ledger (research/stack/ledger.md) holds the full record, item by item.

## In one paragraph

When one of our servers dies, estafette's members stop hearing each other for minutes, even members that never used that server. The cause is a bug in iroh, the networking library we build on. We found it, proved it, and wrote a bug report you can post upstream. We also built a workaround that our own code can carry today: on the Mac and on a Linux server, with the full workaround, every member was hearing every other member again within 28 seconds of a server's death in every run (8 runs on each machine). Finally, a new server can now announce itself to a running network, with no restart and no configuration edit on members.

## Words used below

- **Member**: one running estafette node, the process behind an agent's card.
- **Server** (a "host" in the reports): a machine you run. It carries two services: a **relay**, which forwards traffic between members that cannot reach each other directly, and a **bootstrap node**, the first contact a member uses to join the network.
- **Gossip**: how members spread announcements to each other (who is online, at what address). It runs on iroh-gossip, a companion library to iroh.
- **Heartbeat**: in the tests, each member sends a tiny message every second. A pair of members is **stalled** when one has heard nothing from the other for 5 seconds or more; **flowing** when heartbeats arrive again.
- **Recovery time**: seconds from the server's death until every stalled pair flows again.
- **Rebind**: a member throws away its whole network connection and opens a fresh one with the same identity key, then rejoins through a server. It costs every open connection.
- **Relapse**: a member recovers, then stalls again and needs a second rebind.
- **Upstream**: the people who maintain iroh (the company n0). **Unreleased**: fixed in their latest code but not in any version we can depend on yet.

## What was tested, and on what

- **The Mac**: an Apple M2 Max running macOS 15.3.1. All E14-E21 experiments ran here first.
- **A Linux server**: a rented Hetzner machine (Ubuntu 24.04.4, 2 virtual CPUs, 3819 MiB memory), set up for this work and run by a sibling agent session (lab-sibling). Every result from E14 to E20 was rerun there; E21 was rerun there too (lab/linux/linux-e21: same outcome, the self-announcing arm flowing from 6.8-6.9 s).
- **The test network**: three members and two servers, all on one machine, talking over its internal network. The test kills one server outright (both its relay and its bootstrap node) and watches heartbeats for 180 seconds. Most comparisons run 8 times per variant; "n" below is the number of runs.
- Not yet tested: two real machines, a home router in the way (NAT), or real internet distances.

## Finding 1: the relay bug in iroh (E14 and the bug report)

What happens. A member sends all its relay traffic through one internal queue that serves every relay. When a relay is dead, the small waiting line for that relay (64 slots) fills up and is never emptied, and the shared queue then waits on it forever. From that moment nothing goes through any relay, live ones included. It clears only when iroh gives up on the dead relay after about 60 seconds of inactivity, and any further traffic toward the dead relay starts it again.

How we know.
- E14 (2026-10-20, Mac) traced it in the iroh source and reproduced it with a small program: one connection attempt per second toward a member behind the dead relay jammed it 17 seconds after the death; five per second, 4 seconds.
- The bug report (experiments/e14-bug-report.md) shows the trigger is a count, about 65 or more messages addressed to the dead relay. Its single-file reproduction fails 20 of 20 times on iroh 1.3.0 (our version) and 20 of 20 on iroh's newest code (1.4.0), and passes every control. A diagnostic patch showed the full queue directly. Two candidate fixes each passed 20 of 20.
- On Linux the same reproduction failed 19 of 20 (1.3.0) and 18 of 20 (newest), with controls and both fixes as on the Mac.
- iroh's own levers do not help: removing the dead relay from the list, or forgetting the dead peer's address, changed nothing.

The package. experiments/e14-bug-report.md is written to go upstream unchanged: summary, environment, the reproduction and how to run it, the mechanism with source lines, the proof, two candidate fixes with their trade-offs, and what could make it wrong. The directory experiments/e14-bug-report/ packages it for posting: README.md (the report), ISSUE.md (short text for a GitHub issue), the reproduction programs, run.sh (rebuilds every count), and the raw Mac and Linux results. You ruled that you post it.

## Finding 2: the workaround, built up from E15 to E20

The base rule (W1, E15): a member that hears no heartbeat from anyone for 3 seconds rebinds, at most once every 20 seconds. A fresh connection stack has a fresh, empty relay queue. It healed every stalled pair (76 of 76 on the Mac, 48 of 48 on Linux), against 0 of 24 (Mac) and 0 of 12 (Linux) with no rule. But 5 of 13 Mac runs relapsed, and the next four experiments chased why.

- **E16**: gossip never retries a member it once failed to reach (fixed upstream, unreleased). Patching that alone healed nothing, and with our earlier rejoin rule it made the jam worse. We do not carry that patch; the rebind already starts gossip afresh.
- **E17**: relapse cause 1. The fresh connection still remembers the old route through the dead relay and sends to it again, so the jam returns about 57 seconds after the rebind. The answer (C2, 24 lines): at rebind, test each configured relay with a plain connection attempt and erase dead relays from the stored addresses of other members.
- **E18**: relapse cause 2. After a rebind, the surviving bootstrap node can ignore the member's join because of a leftover request from before the crash. The member waits about 60 seconds. Two answers: the member gives up after 5 seconds and rebinds again; and the bootstrap node gets a one-line fix that upstream already made (unreleased), carried through Cargo's standard way of patching a dependency.
- **E19**: all parts together. On both machines, 0 of 8 runs relapsed. Without C2, 5 of 8 (Mac) and 4 of 8 (Linux) relapsed, so C2 earns its place. The cost on the Mac: about 14 seconds slower than W1 alone whenever W1 alone would not have relapsed.
- **E20**: the 14 seconds explained. A rebound member whose only neighbor is the bootstrap node hears the others late, 11 to 16 seconds. The answer (MJOIN, 13 lines): after a rebind, a member with no other member as a neighbor contacts the other members directly every 3 seconds until one becomes a neighbor. Late members went from 5 of 21 to 0 of 24 (Mac). On Linux the full set healed faster than without MJOIN (median 15.9 s against 20.1 s).

### (a) The parts and the failure each answers

![The workaround parts and the failure each answers](showcase/diagram-1.png)

<details><summary>Mermaid source (showcase/diagram-1.mmd)</summary>

```mermaid
flowchart LR
    F1["Server dies: relay queue jams, all relay traffic stops"] --> W1["W1: rebind after 3 s of silence"]
    F2["Relapse 1: fresh connection re-jams on the old dead route"] --> C2["C2: test relays at rebind, erase dead ones"]
    F3["Relapse 2: bootstrap node ignores the re-join"] --> JT["5 s join timeout, then rebind again"]
    F3 --> OJ["One-line gossip fix at the bootstrap node"]
    F4["Rebound member hears others 11-16 s late"] --> MJ["MJOIN: contact the other members directly"]
    F5["Gossip never retries a failed contact"] --> W1
```

</details>

### (b) Timeline of the experiments

![Timeline of experiments E14 to E21](showcase/diagram-2.png)

<details><summary>Mermaid source (showcase/diagram-2.mmd)</summary>

```mermaid
timeline
    title Experiments E14 to E21
    2026-10-20 : E14 one dead relay jams every relay send in iroh
    2026-10-21 : Bug report with single-file reproduction, fails 20 of 20
               : E15 W1 rebind heals every stalled pair, relapses in 5 of 13
               : E16 gossip retry patch alone heals nothing, not carried
               : E17 relapse cause 1 found, C2 removes the re-jam
               : E18 relapse cause 2 found, join timeout and one-line fix
               : E19 all parts together, 0 of 8 relapse on both machines
               : E20 MJOIN removes the late hearing
               : E21 servers announce themselves at runtime
```

</details>

### (c) Recovery time, W1 alone against the combined workaround

Seconds from the server's death until every stalled pair flows again: median (fastest to slowest). "Relapsed" counts runs that needed a second rebind. A run that never stalled is left out of the times.

| Variant | Machine | Runs (stalled) | Recovery, median (range) | Relapsed | Report |
|---|---|---|---|---|---|
| W1 alone | Mac | 8 (8) | 17.1 s (15.7-148.8; one run never fully recovered) | 3 of 8 | E19 |
| W1 alone | Linux | 8 (7) | 18.7 s (13.0-145.7) | 2 of 8 | linux-e19 |
| Combined without MJOIN | Mac | 8 (7) | 31.2 s (29.3-33.2) | 0 of 8 | E19 |
| Combined without MJOIN | Linux | 8 (8) | 20.4 s (14.2-34.7) | 0 of 8 | linux-e19 |
| Full fix (with MJOIN) | Mac | 8 (8) | 18.1 s (14.5-28.0) | 0 of 8 | E20 |
| Full fix (with MJOIN) | Linux | 8 (7) | 15.9 s (14.1-19.0) | 0 of 8 | linux-e20 |

Read with care: the same "combined without MJOIN" setup gave a Mac median of 31.2 s in E19 and 18.0 s in E20, so one set of 8 runs can move by that much. What holds across every run set: the combined workaround removed the long tail (no run past 35 s) and the relapses.

## Finding 3: servers that announce themselves (E21, Mac and Linux)

What it does. Each server joins the network and broadcasts a signed record (its relay and bootstrap addresses) every 5 seconds. Members add it on the fly and save it to a file for their next start.

What was measured (n=5 per variant, full workaround on).
- A server started on a running network reached every member in 24 to 114 milliseconds, with no restart.
- When the first server then died, all 15 members moved to the new one and every pair was flowing again in 5.9 to 7.0 seconds, with no relapse. The comparison against a pre-configured server is confounded, so this does not show "learned is faster than configured".
- A new member that knew only the new server joined in about 10 milliseconds. A restarted member with the saved file joined; without it, it never joined (one run each).
- Surprise: adding a relay makes iroh re-pick its preferred relay, and it switched 11 of 15 members to the new one.
- Gap: nothing in the spec tells a real server from any member holding the network secret, so any member could pose as a server. The experiment added a key of yours that certifies each server, which you then ruled on.

## What you ruled (2026-10-20 and 2026-10-21)

- Every announcement carries the sender's full current address (19:06); the network admission check runs inside iroh's connection hook, both ways (19:06); old announcements expire after 300 s (19:06).
- Servers announce themselves; members add them at runtime and remember them (19:10). No n0 services at all (19:24). Public card fields stay in announcements, capped at 3 KiB (19:20).
- Parameters two independent pieces must agree on: approved as drafted (19:32).
- Lab server: Hetzner CX23 x86 in Nuremberg (20:31); later "Keep 24 h more", lab resources extended to 2026-10-22T18:00Z.
- Relay death, first step: our own fix on the current gossip version, measured first (21:40); the stdin fix: measure it (21:40); MCP values approved as drafted (21:40).
- The iroh relay bug: build our workaround and write a detailed bug report (2026-10-21 00:00); you post the report yourself (12:25).
- The workaround: "Full fix", MJOIN included, goes toward the spec (12:30).
- The one-line gossip fix: carry it through Cargo's dependency patching, drop it when a release carries it (12:30).
- Server trust: "Guard it with your key" (12:34): your public key in the network config, one certificate per server, members accept server records only from certified servers.

The spec itself is untouched: every staged change waits for your one batch edit.

## What remains open

- **Your actions**: post the bug report; apply the staged spec changes (S1-S26 in the ledger) when you choose.
- **Not yet staged**: your server-trust ruling has no staged spec row yet.
- **Not yet run**: two real machines and NAT; relay encryption settings; whether the lock that keeps one live member per card behaves on Linux as on the Mac; power loss.
- **Not explained**: why the bootstrap node's relayed heartbeats arrive 11-16 s late; why members already moved to the new server still stalled when the old one died (2 of 2 runs in E21); how much traffic a real member sends toward a dead relay (the tests sent one probe per second).
- **Product needs**: MJOIN needs a list of the other members in the product; the 5 s join timeout costs a full rebind whenever a legitimate join is slower than 5 s.
- **Upstream**: the gossip fixes we lean on (#161, #178) are unreleased; iroh's relay bug is unfixed in the newest code we checked (main 55908a5).

## Where everything lives

- research/stack/ledger.md: status at a glance, every collision (C1-C19) and staged revision (S1-S26), and the evidence by item.
- research/stack/experiments/e14-dials.md to e21-hosts.md: one report per experiment; e14-bug-report.md and the directory e14-bug-report/ are the upstream package.
- research/stack/lab/linux/: the Linux reruns (linux-e14, linux-e14w, linux-e14-repro, linux-e15, linux-e17 to linux-e20).
- research/stack/staged-revisions.md: the intended spec text; research/stack/parameters.md: the approved parameter values.
- Code: the estafette repository, branches spike/e14-dials, spike/e14-bug-report, spike/e15-workaround to spike/e21-hosts (pushed).
- docs/orchestration_log/history/2026-10-15/events.md: the journal, with every ruling quoted.
