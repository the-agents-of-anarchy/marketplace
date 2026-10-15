# My 2026 Rust Toolkit

Source: https://www.namtao.com/rust-toolkit-2026/  Fetched: 2026-10-15  Author: not stated on the page

## Thesis

The author presents a toolkit of "a dozen or so tools & packages that I use in every project, along with smart default config." The author recommends devenv as the single config file that sets up the environment, and names a set of tools and crates for each job. The page gives no evidence for most of its performance and quality claims.

## Recommendations

| # | Topic | Recommendation (author's words) | Rationale given | Config/snippet |
|---|---|---|---|---|
| 1 | devenv | "If you want one tool to rule them all, it's Devenv" | "per-project isolation without the overhead of containers"; "you can check in to your project's repo, and share with your colleagues" | Block A |
| 2 | Rustup | "Install and easily switch between stable, beta, and nightly compilers and keep them updated." | Bootstrap step: "the first thing you'll need to bootstrap your rust dev environment, whatever your operating system, is the Rustup installer" | Block B |
| 3 | Toolchain | "I have been using nightly since 2020." Stable is an option: "you may stay on the stable version if you have very good reason" | "The benefits, not least to compile times, have been worth the one or two occasions I've had to switch back to stable" | Block C |
| 4 | Cargo search, add, info | "try `cargo search`" before visiting crates.io; "cargo info is very useful, too" | "Your search results are there right in your terminal, ready to add without opening your `Cargo.toml` with `cargo add`"; info is useful "to check the features you might need to enable" | Block E |
| 5 | cargo-shear | "Honourable mention: `cargo-shear`, removes dependencies you're no longer using" | None stated | None |
| 6 | cargo-seek | "A terminal user interface for searching, adding and installing cargo crates." | "Is a pretty TUI wrapping all three of these commands" | Block E |
| 7 | Clippy | "Out of the box, it's fine, but you can give it TEETH." "I recommend using by default in every project." | "The groups pedantic and nursery will teach you good rust patterns, and the rest of the lints stop you writing code that can crash." Tests are exempted: "To allow for fast prototyping where it should be - in tests - allow panicking there" | Blocks D and F |
| 8 | Bacon | "I recommend running `bacon clippy` in a terminal, watching the excellent output and following its advice." | "the first error in the COMPILER output usually is" the one to fix | Block E |
| 9 | cargo-nextest | "your testing will be much more powerful and, almost as important, PRETTIER with nextest." | Features listed include "Detect and handle slow tests," "Collect test coverage," and "Do mutation testing." Speed: "it does all this up to 3x faster than cargo test" | Block E |
| 10 | cargo-generate | "Cargo generate allows you to specify internet-accessible templates to quickly scaffold larger frameworks such as a web app" | "quickly scaffold" | Block E |
| 11 | watchexec | "I keep it around for chaining cargo clippy, cargo test, and cargo run into a pipeline that kicks off whenever I save." | "triggers any chain of commands you like, not just cargo ones" | Block E |
| 12 | Editor | "My preferred config is the excellent: `lazyvim.org`" | "I need sensible defaults that work out of the box - and that is Lazyvim." "Clone, and run Neovim, and everything works with no configuration." | None |
| 13 | Editor alternatives | "Good options I also have installed are: Helix, Vscode, Zed" | "ALL with vim keybindings." | None |
| 14 | color-eyre | "error report handler for panics and eyre::Reports for colorful, consistent, and well formatted error reports" | "which allows for beautiful as well as ergonomic error handling" | Block G |
| 15 | itertools | "Extra iterator adaptors, iterator methods, free functions, and macro" | "Ergonomic Rust programs are often built around data that is mutated by iterators in a pipeline." | Block G |
| 16 | criterion | "Statistics-driven micro-benchmarking library" | "`criterion` provides advanced statistics and report generation which even include pretty gnuplot charts." | Block E |
| 17 | rayon | "Rayon is the simplest parallelism library you'll ever use, try it before you reach for heavyweight async frameworks." | "you can make your whole pipeline parallel by changing `.iter()` to `.par_iter()`" | Block G |
| 18 | serde | "Nearly every application needs to serialise or deserialise data, which in Rust means the `serde` create." | Honourable mention: "`nanoserde` zero-deps derive-based serde for json & toml." | Block G |
| 19 | jiff | "A date-time library that encourages you to jump into the pit of success." | "Ergonomic time handling. The standard library is fine, but we can do better!" Honourable mention: "`chrono`, the old master." | Block G |
| 20 | clap | "use the `derive` feature of `clap`" | "Rust's built-in argument parsing is good, but far better is to use the `derive` feature of `clap` and organise it all into a neat struct" | Block G |
| 21 | command-run | "a thin wrapper around the `std::process::Command` type with a few additional convenient features" | "Rust's built-in command execution library is comprehensive, but a little too low-level for my liking." | Block G |
| 22 | utoipa | "Compile time generated OpenAPI documentation for Rust" | "allows any popular backend Rust web framework from `axum` to `rocket`, to become a self-documenting statically-typed REST API." | Block G |
| 23 | reqwest | "higher level HTTP client library" | "operates by default on RUSTLS, the pure rust cryptographic library that can replace OpenSSL." | Block G |
| 24 | sqlx | "An async, pure Rust SQL crate featuring compile-time checked queries without a DSL." | "Combine `utoipa` with the compile-time verified queries of SQLX and your business logic is modelled in a single struct" | "Install the `sqlx-cli` for DB management, migrations, and offline validation." |
| 25 | leptos | "For frontend web I like the extremely comprehensive `leptos` crate." | "The `trunk` utility is the Swiss army knife here, providing hotreloading, auto bundling of CSS and static assets, tailwind integration" and "You don't have to write React any more!" | Block G |
| 26 | dioxus | "Build fullstack web, desktop, and mobile apps with a single codebase" | "Honourable mention: `tauri`, lightweight native WebView." | Block G |

## Rejected or warned against

| # | Thing | Author's reason |
|---|---|---|
| 1 | Stable-only toolchain | Discouraged "if you have very good reason"; the author has used nightly since 2020 for compile-time benefits. |
| 2 | Containers for per-project isolation | devenv gives "per-project isolation without the overhead of containers." |
| 3 | VMs for Docker on macOS | "(Finally no more VMs to run docker on mac in!)" No further reason given. |
| 4 | cargo-watch | Old staple, "Evolved from the old staple of `cargo-watch`"; watchexec "triggers any chain of commands you like, not just cargo ones." |
| 5 | Panicking code outside tests | Clippy deny list: "the rest of the lints stop you writing code that can crash." |
| 6 | Heavyweight async frameworks as first resort for parallelism | "try it before you reach for heavyweight async frameworks." Stated as an order of attempts, not a ban. |
| 7 | Zero-cost claim for itertools | Erratum: "This is not actually guarenteed by `itertools`" [sic]. Reason given: "one of the goals is to add convienience functions missing from the standard library due to the zero-cost requirement" [sic]. |
| 8 | leptos for server-side rendering | "Though it also supports server side rendering, and therefore could be used on the backend, the ergonomics break down for me when using that feature." |
| 9 | React | "You don't have to write React any more!" No further reason given. |
| 10 | Electron | Tauri is "a lighter option that just replaces Electron." Reason given: "lighter." |
| 11 | Nix without devenv | "you can certainly do all this with nix out of the box, you can't do it as simply." |
| 12 | Flutter | Dioxus is described as "A 'better Flutter': faster, slimmer, and web-native." |

## Claims without evidence

- The new trait solver "can make some crates like apache datafusion compile more than 8x faster!" No benchmark or source is given. Asserted.
- "nightly builds are REALLY stable!" Asserted.
- cargo-nextest "does all this up to 3x faster than cargo test." No benchmark or source is given. Asserted.
- devenv gives "per-project isolation without the overhead of containers." Asserted.
- "Neovim is the fastest editor out there." Asserted.
- "Rayon is the simplest parallelism library you'll ever use." Asserted.
- Dioxus is "faster, slimmer, and web-native," and "Dioxus code runs natively with no virtual machine, call system APIs with zero overhead." Asserted.
- "Rust handles errors in such a sensible way that it FINALLY allows senior developers to sleep at night." Asserted.
- The clippy rationale is deferred to "see my dedicated video, Rust: Don't Panic." That rationale is not on the page.
- "The authors SAY they chose that spelling because it makes it easier to search for a unique name." This is attributed to the crate authors and not checked.
- devenv is "not sponsored." Disclosure asserted by the author.
- The author uses these tools "in every project." Self-report.

## Config blocks

Block A, devenv (also repeated at the end of the page under "DEVENV.SH"):

```
{
  languages.rust = {
    enable = true;
    channel = "nightly";
    components = [ "rustc" "cargo" "clippy" "rust-analyzer" ];
  };
  packages = with pkgs; [
    bacon
    cargo-seek
    cargo-nextest
    cargo-generate
  ];
  scripts.watcher = {
    exec = ''
        watchexec -c -e rs \
        "cargo clippy && cargo test && cargo run"
    '';
    packages = [ pkgs.watchexec ];
  };
  env.LD_LIBRARY_PATH = lib.makeLibraryPath [
    pkgs.zlib
  ];
  env = {
      DATABASE_URL = "postgres://user:pass@localhost/dbname";
  };
  enterShell = ''
    echo "Crates ready to update with 'cargo update'":
    cargo update -n
  '';
  git-hooks.hooks = {
    clippy.enable = true;
  };
}
```

Block B, rustup install (page's own words: "Run the one-liner here from rustup.rs"):

```
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
```

Block C, toolchain switch:

```
$ rustup default nightly
```

Block D, Cargo.toml clippy lints (page's words: "Add these to your `Cargo.toml`"):

```
[lints.clippy]
pedantic = { level = "deny", priority = -1 }   # UM, ACTUALLY
nursery = { level = "deny", priority = -1 }    # BETA LINTS
# DENY PANICS
unwrap_used = "deny"
expect_used = "deny"
indexing_slicing = "deny"
arithmetic_side_effects = "deny"
unreachable = "deny"
unimplemented = "deny"
unchecked_time_subtraction = "deny"
todo = "deny"
string_slice = "deny"
panic_in_result_fn = "deny"
panic = "deny"
exit = "deny"
as_conversions = "deny"
```

Block E, commands on the page:

```
cargo search rayon
cargo add rayon
cargo info rayon
cargo install cargo-seek
bacon clippy
cargo nextest run
cargo generate leptos-rs/start-trunk
watchexec "cargo clippy && cargo test && cargo run"
cargo bench
```

Block F, clippy.toml (page's words: "and these in your `clippy.toml`"):

```
allow-unwrap-in-tests = true
allow-expect-in-tests = true
allow-panic-in-tests = true
allow-indexing-slicing-in-tests = true
```

Block G, Rust snippets on the page, each a usage example and not a config: `use eyre::Result;`, `use itertools::Itertools;`, `use rayon::prelude::*;` with `input.par_iter()`, `use serde::{Deserialize, Serialize};`, `use jiff::{Timestamp, ToSpan};`, `use clap::Parser;` with `#[derive(Parser, Debug)]`, `Command::with_args("echo", &["hello", "world"])`, `#[utoipa::path(`, `use std::hint::black_box;` with criterion, `query_as!` from sqlx, `#[component]` from leptos, and `dioxus::launch(app);`.

## Fetch notes

- The first WebFetch call returned a model-written condensed account. It said it could not reproduce the page verbatim, and it named the site "Namtao Productions." That account is not used for any quote here. The raw page shows no byline, so the author is recorded as not stated.
- The second attempt pulled the raw HTML with curl: HTTP 200, 82,500 bytes. Text was extracted with a local script run under `python3 -I`. Source HTML is at /tmp/rust-toolkit-src/page.html and extracted text at /tmp/rust-toolkit-src/page.txt. All quotes come from that extraction.
- The extraction has artifacts. The introduction paragraph appears twice in the page text. The page ends with navigation residue ("Connected Pages", "Pages mentioning this page"). Code blocks are kept as printed.
- No truncation was seen. The text runs through the closing "DEVENV.SH" section to the navigation residue.
- Spellings "guarenteed," "convienience," "serialise," and "create" (for crate) are the page's own and are kept as printed.
- No claim on the page was checked against an outside source. Verification was out of scope.
