# Habilis fork patches vs our pins: iroh, netwatch, portmapper

Checked on 2026-10-16. Our pins from `/tmp/ra-tree/probe/Cargo.lock`: iroh 1.3.0 (line 1340), netwatch 0.19.3 (line 1953), portmapper 0.19.3 (line 2336), all from the crates.io registry. Source read from `~/.cargo/registry/src/index.crates.io-1949cf8c6b5b557f/`.

| Fix | Upstream ref | Merged | First release with it | Our version | Contained? | Evidence |
|---|---|---|---|---|---|---|
| (a) Mapped address eviction | iroh PR #4294, closed unmerged. Issue #4293 open. Follow-up PR #4447 open. | Not merged. Closed 2026-07-28. | None | iroh 1.3.0 | No | `socket/remote_map.rs:285-287` removes only the sender. `socket/mapped_addrs.rs` has no `remove` or `retain`. PR head `82f27d9` is 3 ahead and 129 behind `v1.3.0`. |
| (b) Relay teardown drain | iroh PR #4460, "drain relay tasks with join_next instead of join_all" | 2026-08-24, merge commit `09a0aca` | iroh v1.1.0 (published 2026-08-25) | iroh 1.3.0 | Yes | `socket/transports/relay/actor.rs:1451-1452` drains with `join_next`. `compare v1.1.0...09a0aca` is "behind". `compare v1.0.3...09a0aca` is "ahead", so the 1.0.3 base lacks it. |
| (c) RTM_MISS ignore, netwatch | net-tools PR #215, "ignore RTM_MISS in the BSD route monitor". Duplicate PR #203 closed unmerged. | 2026-08-24, merge commit `0ebdce0` | netwatch-v0.19.2 (tagged 2026-08-24) | netwatch 0.19.3 | Yes | `netmon/bsd.rs:175-177` returns early on `RTM_MISS`. `compare netwatch-v0.19.1...0ebdce0` is "ahead". `compare netwatch-v0.19.2...0ebdce0` is "behind". |
| (c) RTM_MISS, portmapper | Same PR #215 | Same | portmapper-v0.19.2 contains the merge commit. Portmapper has no RTM_MISS code of its own. | portmapper 0.19.3 | Partly | `grep RTM_MISS` over portmapper-0.19.3 `src` is empty. Portmapper gets the fix only through its netwatch 0.19.3 dependency. |

## Notes

- **Survey claim corrected.** `research/stack/surveys/a3-habilis.md` line 80 says the RTM_MISS fix covers netwatch and portmapper. Upstream source changes only netwatch. Portmapper inherits it through the dependency.
- **Only fix (a) is missing from our pin.** Fixes (b) and (c) are in iroh 1.3.0 and netwatch/portmapper 0.19.3. Fix (a) has no upstream merge and no release. Issue #4293 reports the cache grows once per remote ever seen.
- **Habilis base differs from ours.** Habilis pins iroh `=1.0.3` on fork rev `0e7cdb4`, not 1.3.0. Its `iroh/src/socket/remote_map.rs:237-241` carries the #4294 eviction, and the fork's relay actor drains with `join_next`. The comparison above covers only our 1.3.0.
- **Cited lines are a comment.** `Cargo.toml:116-119` in habilis is a comment. The net-tools pin lives in the iroh fork's own manifest, per `FORKED.md` around line 454.
- **Habilis net-tools rev is not upstream.** Fork rev `e029602` diverges from upstream `0ebdce0` (19 behind, 1 ahead). It carries its own RTM_MISS handling, so habilis does not carry the upstream commit.
- **Search coverage.** I searched iroh PR titles and bodies for "mapped_addrs", "mapped addr", "join_next", "drain", and "relay teardown". I searched net-tools for "RTM", "route", and "MISS" in PR and issue titles. No merged PR adds address eviction under another title. A PR I did not match on the search terms could still exist.
- **Not verified.** I read source and ancestry only. I did not run the code or test runtime behaviour.
