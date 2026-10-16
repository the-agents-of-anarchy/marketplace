# Small pieces

Date 2026-10-16. Registry: crates.io API with user agent, and `cargo tree` in a scratch crate at /tmp/ra-s1-scratch (not the probe). Repo archive status: `gh repo view`. Crate sources: /tmp/ra-s1-crates. Probe tree: /tmp/ra-tree/probe (toolchain 1.99.1). Spec: spec/blueprint.md.

| # | Need | Spec | In tree? | Candidates (version, updated, maintained, deps) | Copy cost (lines) | Evidence |
|---|---|---|---|---|---|---|
| 1 | YAML card file: read `public_key`, `handle`, `public` mapping (max 4096 bytes serialized), ignore other keys; write `handle` and `public_key` | 3.5 (blueprint.md:501-515) | no | serde_yaml 0.9.34+deprecated: 2024-03-25, unmaintained, repo archived, 5 direct / 14 transitive. serde_yml 0.0.13: 2026-05-27, shim to noyalib, repo archived, 2 direct / 15 transitive. serde_norway 0.9.42: 2024-12-21, hard fork, repo active (pushed 2025-08-04), 5 direct / 14 transitive. serde_yaml_ng 0.10.0: 2024-05-26, fork of serde-yaml, repo active (pushed 2025-09-14), 5 direct / 14 transitive. saphyr 0.2.2: 2026-10-15, active, no serde support, 5 direct / 15 transitive. saphyr-serde 0.0.0: placeholder, 1 version, no repository. yaml-rust2 0.13.0: 2026-09-11, active, no serde support, 3 direct / 6 transitive. | Not copyable. Parser sources: saphyr 4274, yaml-rust2 5372, serde_yaml 11386 src lines. Serde value layer not measured. | crates.io API; `gh repo view`; scratch `cargo tree -p X -e normal`; READMEs and Cargo.toml (see notes) |
| 2 | TOML network config: `secret`, `relay`, `bootstrap` | 3.3 (blueprint.md:459-467) | no | toml 1.1.8+spec-1.1.0: 2026-10-09, active (repo pushed 2026-10-09), 6 transitive unique by `cargo tree` (serde_core, serde_spanned, toml_datetime, toml_parser, toml_writer, winnow). crates.io lists 2 required and 8 optional deps; `cargo tree` is the default-feature closure. | Hand parse not written. Crate src 9139 lines. | crates.io API; scratch `cargo tree`; toml-1.1.8/Cargo.toml |
| 3 | Lowercase base32, no padding: 52-char card key, 7-char fingerprint, network secret | 3.1 table (blueprint.md:405-423, key row at 409) | yes: data-encoding 2.11.1 (in lock; dep of data-encoding-macro 0.1.21, which comes via iroh-base 1.3.0) | data-encoding 2.11.1: 2026-08-03, active (repo pushed 2026-10-14), 0 deps. No lowercase built-in. | 0 lines: one `const` with `symbols` string, via `new_encoding!` macro. No new lock entries needed. | data-encoding lib.rs:2259-2264 (BASE32_NOPAD and its spec example), lib.rs:2280-2304 (NOCASE); data-encoding-macro-0.1.21/src/lib.rs:44-50 |
| 4 | UUIDv7 message id, 16 bytes on wire | 3.1 table (blueprint.md:405-423, message id row) | yes: uuid 1.28.0 via rmcp 3.5.1. Enabled: `default` (std), `rng`, `v4`. `v7` is off. | uuid 1.28.0: 2026-10-10, active (repo pushed 2026-10-10). `v7` = ["rng"], so no new crate; rng is already on. | 0 lines. Add feature `v7` to the existing dependency. `Uuid::now_v7()` is the call. | uuid-1.28.0/Cargo.toml:137 (v7), :113 (rng); src/v7.rs:16-17; probe `cargo tree -e features -i uuid` |
| 5 | XDG dirs: config `$XDG_CONFIG_HOME` or `$HOME/.config`; data `$XDG_DATA_HOME` or `$HOME/.local/share`; runtime `$XDG_RUNTIME_DIR` or `$TMPDIR` or `/tmp`, plus user id, 0700 | 3.3 (blueprint.md:437-445) | no | dirs 7.0.0: 2026-09-05, active, repo on codeberg (not checked with gh), 1 direct (dirs-sys) / 3 transitive. directories 6.0.0: 2025-01-12, repo archived, 1 / 3. etcetera 0.11.0: 2025-10-28, active (pushed 2026-08-04), 1 transitive. xdg 3.0.0: 2025-05-04, active (pushed 2025-05-04), 0 required, 1 optional, 0 transitive by default. | Hand code about 10 lines of std::env (estimate, not compiled). Crate src: dirs 440, etcetera 1437, xdg 1354 lines. | crates.io API; scratch `cargo tree`; dirs-7.0.0/src/mac.rs:7,10; etcetera-0.11.0/src/base_strategy/xdg.rs:163-169, :211 |
| 6 | Signals and stdin close: session state machine enters Stopping on "stdin closed or signal" | 3.9 (blueprint.md:679) | tokio 1.53.3 yes. Probe features: bytes, default, fs, io-std, io-util, libc, macros, mio, net, rt, socket2, sync, test-util, time, tokio-macros. Absent: `signal`, `process`. | Feature `signal` pulls signal-hook-registry 1.4.8 (2025-12-25; deps errno, libc). errno is not in the probe tree. | Signals: about 4 lines plus the feature. Stdin: no crate; a `std::io::stdin` read loop on a thread is about 8 lines (estimate). | tokio-1.53.3/Cargo.toml:122-128; probe `cargo tree -e features -i tokio`; `cargo tree -i errno` empty; tokio src/io/stdin.rs:12-22 |
| 7 | Unix socket, 0600, inside 0700 runtime dir | 3.11 (blueprint.md:758); 3.3 runtime row (blueprint.md:444) | yes: tokio `net` feature on. UnixListener is gated by `cfg_net_unix`. | None. std::os::unix::fs::PermissionsExt is in std. | About 4-6 lines (estimate). | tokio-1.53.3/src/net/mod.rs:54; src/net/unix/listener.rs:76 (bind) |
| 8 | Stale socket: remove socket if no process with that pid exists | 3.3 (blueprint.md:467) | libc 0.2.190 yes (tokio `libc` feature; via reqwest chain). rustix and nix: not in probe lock. | libc 0.2.190: 2026-10-02, active. rustix 1.1.5: 2026-09-16, not in tree. nix 0.31.3: 2026-05-11, not in tree. | About 6 lines with one unsafe call (estimate). | libc-0.2.190/src/unix/mod.rs:1288 (`kill`); `cargo tree -i rustix` and `-i nix` both: no match |

## Notes per item

### 1. YAML card file

- Registry state, quoted: serde_yaml README:10 says "_(This project is no longer maintained.)_". Version string is `0.9.34+deprecated`. Repo dtolnay/serde-yaml is archived (`gh`, pushed 2024-03-25). Crates.io download count is 438036298. Downloads are not a maintenance signal here.
- serde_yml 0.0.13 Cargo.toml:35 quoted: "DEPRECATED — `serde_yml` is unmaintained. This release is a thin compatibility shim that forwards every call to `noyalib`". Its README names RUSTSEC-2025-0068 as fixed in 0.0.13. Repo sebastienrousseau/serde_yml is archived.
- serde_norway README:9: "A hard-fork of Serde YAML."
- serde_yaml_ng README:12: "This library is a fork from the latest commit of serde-yaml". Its README install line shows `serde_yaml_ng = "0.9"`, while crates.io max is 0.10.0. The README is stale on the version.
- saphyr: `serde` appears only once in src, at emitter.rs:470, in a comment. Cargo.toml has no serde dependency and no feature. So no serde layer.
- saphyr-serde on crates.io: description "tmp", repository None, one version 0.0.0, 1619 downloads, Cargo.toml description "tmp". It is a placeholder, not a usable crate.
- yaml-rust2 Cargo.toml has no serde entry. Parser only.
- Spec consequence: the `public` mapping must travel verbatim (3.5, blueprint.md:501-515). Every serde-based option gives a typed value. A non-serde parser needs a converter from its tree to a serde-compatible value. That converter is not measured here.

### 2. TOML config

- Spec example (blueprint.md:461-465): keys `secret`, `relay`, `bootstrap`. Matches the three-key count.
- crates.io dependency list is not the default-feature closure. It shows 2 required and 8 optional. `cargo tree` on a scratch crate with default features shows 6 unique transitive crates. Use the `cargo tree` number.
- Hand-parse cost is not written, so no line count is measured. The crate itself is 9139 src lines.

### 3. Base32 lowercase, no padding

- BASE32_NOPAD is uppercase (lib.rs:2264). Its doc example (lib.rs:2259-2262) builds the same encoding from a Specification with `symbols` "ABCDEFGHIJKLMNOPQRSTUVWXYZ234567" and no padding.
- No lowercase constant exists. BASE32_NOPAD_NOCASE encodes uppercase and decodes lowercase (lib.rs:2280-2304).
- Custom lowercase: `new_encoding!` with symbols "abcdefghijklmnopqrstuvwxyz234567". The macro doc (data-encoding-macro lib.rs:44-50) shows the `const` form. A const avoids the runtime `Specification::encoding()` call, which is not const.
- The macro crate is a transitive dep of iroh-base. Naming it directly in estafette adds no new lock entries.

### 4. UUIDv7

- uuid features on in the probe: `default`, `rng`, `v4`, `std`. `v7` is off. `rng` is on, and v7 needs only `rng`.
- `now_v7()` is in src/v7.rs:17, with the std clock path at :16.
- The `uuid` version 1.28.0 is the one rmcp 3.5.1 resolves. Enabling v7 here changes only the feature union for that crate.

### 5. XDG dirs

- dirs on macOS: config_dir is `~/Library/Application Support` (dirs-7.0.0/src/mac.rs:7, :10). Spec 3.3 (blueprint.md:440-442) says `$XDG_CONFIG_HOME` or `$HOME/.config`. The two disagree on the darwin host where this runs. Adopting dirs as written would move config on macOS. This is a spec-versus-crate conflict to record, not a verdict.
- etcetera's Xdg strategy (base_strategy/xdg.rs:163-169) follows XDG env vars and $HOME. Its runtime dir reads only `XDG_RUNTIME_DIR` (xdg.rs:211). No `$TMPDIR` or `/tmp` fallback, which spec 3.3 requires.
- directories 6.0.0 repo is archived (soc/directories-rs, `gh`).
- Hand-coded version is the only one that matches 3.3 on every row. Estimate ~10 lines.

### 6. Signals and stdin close

- The probe's tokio has `io-std` on, so `tokio::io::stdin` compiles. It lacks `signal`, so `tokio::signal` is not compiled in.
- tokio's own doc for stdin, src/io/stdin.rs:17-20: "it is impossible to cancel that read. This can make shutdown of the runtime hang until the user presses enter." Spec 3.9 needs stdin close to lead to Stopping (blueprint.md:679). Using tokio's stdin for that trigger has a documented hang on shutdown.
- `signal` feature (tokio-1.53.3/Cargo.toml:122-128) pulls libc, mio/os-ext, and signal-hook-registry. signal-hook-registry 1.4.8 needs errno and libc. errno is not in the tree, so it would be a new lock entry.

### 7. Unix socket

- tokio UnixListener is gated by `cfg_net_unix` (src/net/mod.rs:54). The probe has `net` on. `bind` is at src/net/unix/listener.rs:76.
- Permissions have no crate need. std::os::unix::fs::PermissionsExt sets the mode.
- Not measured: whether the socket file exists with a wider mode between `bind` and the chmod. Mitigation in the spec is the parent runtime dir at 0700 (blueprint.md:444). That mitigation is reasoning from the spec text, not tested here.

### 8. Process-exists

- libc::kill declared at libc-0.2.190/src/unix/mod.rs:1288. Signal 0 checks existence without sending a signal.
- Limit, from the function semantics: kill(pid, 0) succeeding shows a process with that pid exists, not the process that wrote the socket. Spec 3.3 uses the same test ("no process with that id exists"), so spec and mechanism match literally.
- rustix and nix would avoid the raw call. Neither is in the probe lock, so either adds new crates.

## Cross-project observations

- Not applicable. One project read (probe tree plus crates.io). Single-source survey.

## Not read

- noyalib (serde_yml's target): not read.
- serde_norway, serde_yaml_ng, saphyr-parser, yaml-rust2: read only Cargo.toml and README; no src walk for serde value conversion.
- serde_json conversion path for the `public` mapping: not checked. serde_json is listed as in-tree in round 1, not verified here.
- toml src beyond manifest: not read. Hand-parse not written.
- dirs Linux branch and runtime_dir on macOS: not read.
- tokio signal source (src/signal): not read. Only Cargo.toml feature lines and the stdin doc.
- uuid v7.rs beyond `now_v7` signature: not read.
- directories and etcetera tests: not read.
- Card serialized-size check (4096 bytes): not tied to any crate here.
