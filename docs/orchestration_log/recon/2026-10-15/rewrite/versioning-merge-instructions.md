# Instructions: one version for the protocol and the plugin (on draft/10.1-split)

Role: skill-rewriter. Owner ruling (verbatim): "change the protocol versioning - merge it with plugin versioning. then circulate." Work in /Users/ryzhakar/pp/aoa-skills-101 on branch draft/10.1-split (head 65661e7). Same writing stack and guards; `just test` green; commit by explicit path; never touch main, the pointer file, cards or the commons.

Rule: the protocol's version is the version of the peers plugin (peers/.claude-plugin/plugin.json and the peers entry in .claude-plugin/marketplace.json, both 0.8.0 for these changes). There is no second number.

Make exactly these changes:
1. card:55 "Carry `protocol: 10.1`, the protocol version of the skills you loaded; never raise it by applying change lines." becomes an instruction to carry `protocol`, the version of the peers plugin your loaded skills ship with, read from `peers-facts`; add `plugin_version` to peers/bin/peers-facts output (read from the plugin's plugin.json by path relative to the script) and say in card to take the value from it; never raise it by applying change lines. Update test_skills.py:64 so it checks card's text against plugin.json instead of a literal "10.1"; add a test that card's version source (peers-facts plugin_version) equals plugin.json's version.
2. ship: the bump sentence reads in terms of the plugin version only (patch for a fix, minor for a rule, 1.0.0 needs the owner; before 1.0.0 breaking changes ride a minor); the pointer's version line is set to that plugin version and each change line opens with it; ship:33 sends `[notice] protocol <version>` (the plugin version) instead of `protocol v<N>`; ship's description drops "protocol version" wording that names a second number (keep the trigger phrases members say).
3. protocol-change:37 "[notice] protocol v<N>" → "[notice] protocol <version>"; "your loaded version" now means the plugin version your skills ship with.
4. ontology: the terms `pointer` (line 221) and `separating` (line 233) say version in the one sense (the peers plugin's version); add one definition of `protocol version`: the version of the peers plugin; no other definition of the number; fix every other wording that implies two numbers (grep: 'protocol version', 'version' across peers/skills and peers/README.md).
5. README: line 151 and any other line that names a protocol number or "raise the versions"; regenerate from the frontmatters where the README is generated.
6. Hooks: peer-join.sh and its templates must not state a protocol number; leave as is if they do not.
7. The mapping of old numbers (protocol 9.3 was peers 0.5.0; protocol 10 was peers 0.7.0) is NOT skill text: record it in the changes file for the scribe to write as one line into the pointer at shipping.
8. Update protocol-10.1-changes.md with a "Versioning" section (each site, old → new) and traceability.md for the changed sentences (every sentence still lands in one skill or is dropped with a ground).
Run the terms guards, the other-sense test, the no-copy test, `just test`; push; report the head sha, the test count and residuals. Nothing else.
