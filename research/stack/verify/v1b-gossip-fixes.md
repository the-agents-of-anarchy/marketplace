# Habilis fork patches vs our pins: iroh-gossip, swarm-discovery

Checked 2026-10-16 against the GitHub API, crates.io, and the habilis-network manifest. Our pins are the versions the lead stated: iroh-gossip 0.101.0 and swarm-discovery 0.6.1. No lockfile of ours is in this repo, so those pins are not read from source.

| Fix | Upstream ref | State | Merged | First release with it | Our version | Contained? | Evidence |
|---|---|---|---|---|---|---|---|
| Connection-churn leak (superseded connections, peer-state pruning) | n0-computer/iroh-gossip#147, PR | Closed 2026-09-22 without merge | No. Merge sha 8994d0f is not an ancestor of main (main is 8 ahead, 3 behind) | None. Latest release v0.101.0 (2026-06-15) lacks it | iroh-gossip 0.101.0 | No | PR API: merged false, merged_at null. Maintainer closed it "in favor of #161 and #162". v0.101.0 src/net.rs has no superseded-connection code. |
| Peer lifecycle, successor to #147 | n0-computer/iroh-gossip#161, PR | Merged 2026-10-09 | Yes, main at fcd81ae | None. Not in v0.101.0 (fcd81ae is 5 commits ahead of it) | iroh-gossip 0.101.0 | No | PR API: merged_at 2026-10-09T12:30:18Z. Compare v0.101.0...fcd81ae: ahead. |
| Close idle or stale connections, successor to #147 | n0-computer/iroh-gossip#162, PR | Closed 2026-10-09 without merge; content moved to #178 | No | None | iroh-gossip 0.101.0 | No | PR API: merged false. #178 says "Supersedes #162." |
| Connection lifecycle fixes, successor to #162 | n0-computer/iroh-gossip#178, PR | Merged 2026-10-14 | Yes, main at f02f79e | None. Unreleased | iroh-gossip 0.101.0 | No | PR API: merged_at 2026-10-14T12:24:50Z. Body: a 0.101.0 node may lose joins from new nodes, so it needs #189. |
| Do not close connections to older peers | n0-computer/iroh-gossip#189, PR | Merged 2026-10-14 | Yes, main at cd73d93 | None. Unreleased | iroh-gossip 0.101.0 | No | PR API: merged_at 2026-10-14T12:41:33Z. Body: "Connections to old peers still leak, as on main." |
| 10 ms GC retry loop | rkuhn/swarm-discovery#28, issue | Closed 2026-08-02, commented "fixed by #27" | Fix is PR #27, merged 2026-07-13 at b41dbcc | 0.6.4, release commit 3608118, published 2026-10-08. Releases 0.6.2 (2026-06-12) and 0.6.3 (2026-06-30) predate the merge | swarm-discovery 0.6.1 | No | Compare 3b4bb8b...b41dbcc: ahead by 10, so 0.6.1 lacks the fix. Compare b41dbcc...3608118: ahead by 3, so 0.6.4 contains it. 0.6.1 src/updater.rs lines 18-19 still retry at 10 ms. crates.io max version 0.6.4. |

## Notes

- **Habilis carries both fixes.** The habilis-network manifest pins iroh-gossip to its fork rev 28676ce. It pins swarm-discovery through the iroh-address-lookups fork, whose lockfile resolves swarm-discovery to rev b41dbcc, the #27 fix commit. The survey cites the issue number, but the code fix is PR #27.
- **The iroh-gossip fix exists only in the habilis fork.** The fork's src/net.rs has superseded-connection handling at lines 1264, 1921, and 1953. v0.101.0 has none. The #147 commit SHAs are not ancestors of the fork rev, so the fork carries reworked copies, not the upstream commits. The manifest comment says the fork's PR #5 is not merged.
- **Our swarm-discovery pin is not fixed by the version number alone.** iroh-mdns-address-lookup 0.6.0 depends on swarm-discovery "^0.6", which accepts 0.6.4. Our 0.6.1 holds only while our lockfile pins it. A lock refresh moves us to 0.6.4, which contains the fix.
- **Our iroh-gossip pin has no released fix.** The newest release is 0.101.0. Main has three merged fixes (#161, #178, #189) that are unreleased. Main is 9 commits ahead of v0.101.0. Per #189, connections to older peers still leak on main.
- **Habilis's comment on swarm-discovery is stale.** Its manifest says to drop the swarm fork once swarm-discovery 0.6.4 ships. 0.6.4 shipped 2026-10-08. The swarm half of that condition is met. The iroh pins are a separate condition.
- **Habilis's fork notes list one change.** The fork's FORKED.md documents only the Disconnect::left field. The manifest comments and the commit list show more changes than that file records.
- **Limits.** "Contained" means the commit or code is in the named release. I did not run the leak or retry tests, so I have not shown the bugs are gone. I did not read our lockfile.
