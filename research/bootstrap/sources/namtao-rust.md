# namtao.com/rust

Source: https://www.namtao.com/rust/  Fetched: 2026-10-15

## Index

The URL is one page, not an index. Its section anchors are `#my-standard-library`, `#strict-lints`, `#rust-devenv`, `#typestate-pattern`, and `#rust-function-signatures`. The page body links to no other posts. Site-level links to other posts appear in the page markup but not in its body; see Fetch notes.

| # | Post | URL | One line |
|---|---|---|---|
| 1 | Rust (single page, sections: "My Standard Library", "Strict Lints", "Rust Devenv", "Typestate Pattern", "Rust Function Signatures") | https://www.namtao.com/rust/ | Author's preferred crates, strict Clippy lint config, dev environment, typestate example, and a note on function signatures. |

## Per post

### Rust

Source: https://www.namtao.com/rust/

#### Thesis

The page sets out the author's preferred Rust crates, a strict Clippy configuration, a Nix dev environment, a typestate example, and a note on function signatures. The page states no single thesis. Its one stated purpose is for the lint set: "These lints do two things: Teach you rust / Stop panics at runtime".

#### Recommendations

| # | Topic | Recommendation (author's words, quoted) | Rationale given | Config/snippet if any |
|---|---|---|---|---|
| 1 | Command-line parsing crate | "# COMMAND LINE PARSING" | Label only. | `clap = { version = "4.5.53", features = ["derive"] }` |
| 2 | Datetime crate | "# ERGONOMIC DATETIMES" | Label only. | `chrono = "0.4.42"` |
| 3 | Error handling crate | "# SIMPLE PRETTY ERROR HANDLING" | Label only. | `color-eyre = "0.6.5"` |
| 4 | Benchmarking crate | "# BENCHMARKING" | Label only. | `criterion = "0.8.1"` |
| 5 | Iterator crate | "# SUPERPOWERED ITERATORS" | Label only. | `itertools = "0.14.0"` |
| 6 | Parallel iterator crate | "# PARALELL ITERATORS" (sic) | Label only. | `rayon = "1.11.0"` |
| 7 | Serialisation crate | "# SERIALISATION / DESERIALISATION" | Label only. | `serde = { version = "*", features = ["derive"] }` |
| 8 | Test runner | "And I dig running tests with https://nexte.st/" | "I dig" only; no reason given. | None. |
| 9 | Clippy lint set | "Run them with bacon clippy ." | Stated purpose: "Teach you rust" and "Stop panics at runtime". | `[lints.clippy]` block with `pedantic = { level = "deny", priority = -1 }`, `nursery = { level = "deny", priority = -1 }`, and 13 further `"deny"` entries for panic-related and conversion lints: `unwrap_used`, `expect_used`, `indexing_slicing`, `arithmetic_side_effects`, `unreachable`, `unimplemented`, `unchecked_time_subtraction`, `todo`, `string_slice`, `panic_in_result_fn`, `panic`, `exit`, `as_conversions`. |
| 10 | Test exemptions | "But allow these in tests, in your clippy.toml:" | Quoted from page: "If you're wondering how to prototype code quickly using .unwrap() and friends - put them in unit tests, clippy ignores those!" | `allow-unwrap-in-tests = true`, `allow-expect-in-tests = true`, `allow-panic-in-tests = true`, `allow-indexing-slicing-in-tests = true` |
| 11 | Quick lint command | "Also here's an 80% of the above as a one-liner:" | No rationale given. | `cargo clippy -- -D clippy::pedantic -D clippy::nursery` |
| 12 | External lint article | "I also dig what is written here:" | "I also dig" only; no reason given. | https://emschwartz.me/your-clippy-config-should-be-stricter/ |
| 13 | Dev environment | "Here's a reasonable devenv.nix" | "reasonable" only; no justification given. | See Rust Devenv below. |
| 14 | Toolchain | Nightly channel, with components `rustc`, `cargo`, `clippy`, `rustfmt`, `rust-analyzer`. | None given. | `languages.rust = { enable = true; channel = "nightly"; components = [ "rustc" "cargo" "clippy" "rustfmt" "rust-analyzer" ]; };` |
| 15 | Dev tools | Packages list: `bacon`, `cargo-seek`, `cargo-nextest`, `cargo-generate`. | None given. | `packages = with pkgs; [ bacon cargo-seek cargo-nextest cargo-generate ];` |
| 16 | Watch script | "Rebuilds and runs app with supressed warnings" | Description given in the script. | `watchexec -c -e rs "cargo clippy && cargo test && cargo run"` |
| 17 | C libraries | "# C LIBRARIES" | Label only. | `env.LD_LIBRARY_PATH = lib.makeLibraryPath [ pkgs.openssl ];` |
| 18 | Overlay | "Then add oxalica's rust-overlay with:" | None given. | `devenv inputs add rust-overlay github:oxalica/rust-overlay --follows nixpkgs` |
| 19 | Typestate pattern | "The typestate pattern is an API design pattern that encodes information about an object's run-time state in its compile-time type." | Definition only. | Pseudocode: `struct Red; struct Yellow; struct Green;`, `trait SignalState {}`, `struct TrafficSignal<S: SignalState> { _marker: PhantomData<S>, data: String, }`, `impl TrafficSignal<Red> { pub fn next(self) -> TrafficSignal<Green> { ... } }`. The page marks it: "//NOTE: This is psudocode, read the repo for working code". |
| 20 | Typestate reference | "I maintain the best example of this pattern I could find here:" | Asserted "best"; no comparison given. | https://github.com/0atman/typestate-template |
| 21 | Function signatures | "Are complex, but they can be understood through thorougher thought though." | Asserted; no argument given. | Example from `nom::combinator`: `pub fn cut<I, E: ParseError<I>, F>(parser: F) -> impl Parser<I, Output = <F as Parser<I>>::Output, Error = E> where F: Parser<I, Error = E>`. |
| 22 | Bound equivalence | "is equivalant to" (between `fn walk_pet<W: Walk>(pet: &mut W)` and `fn walk_pet<W>(pet: &mut W) where W: Walk`) | Asserted equivalence; no argument given. | Both forms shown above. |
| 23 | Further reading | "Good stuff here:" | None given. | https://github.com/pretzelhammer/rust-blog/blob/master/posts/tour-of-rusts-standard-library-traits.md#scope |

#### Rejected or warned against

- The page names no practice it explicitly rejects.
- The deny list in the lint config forbids, in code outside tests: `unwrap`, `expect`, indexing and slicing, `panic!`, `todo!`, `unimplemented!`, `unreachable!`, `exit`, `as` conversions, unchecked arithmetic, and unchecked time subtraction. The page's stated purpose for these is "Stop panics at runtime".
- The page permits `.unwrap()` and friends only in unit tests: "put them in unit tests, clippy ignores those!"

#### Claims without evidence

- "Teach you rust" and "Stop panics at runtime" are the lint set's purposes. Asserted. No evidence given.
- "clippy ignores those" (unit tests). Asserted. The page gives config keys for this, but no Clippy reference.
- "80% of the above" for the one-liner. Asserted. No measurement given.
- "a reasonable devenv.nix". Asserted. No justification given.
- "I maintain the best example of this pattern I could find". Asserted. No comparison given.
- "can be understood through thorougher thought though". Asserted. No argument given.
- "is equivalant to" (generic bound and where-clause forms). Asserted. No argument given.
- "I dig" (nextest, the Clippy-config article). Opinion only.

## Fetch notes

- The fetch was successful. The page is one page with no linked posts in its body.
- The WebFetch summary was model-generated, so its wording is not the page's. It dropped "in its compile-time type" from the typestate definition. Quotes in this file come from the raw HTML, retrieved with curl and text-extracted.
- The page markup links to other site posts: `/rust-is-the-new-c/`, `/misusing-macros-for-fn-and-profit/`, `/async-isn-t-real-and-can-t-hurt-you/`, `/rust-dont-panic/`, and `/rust-toolkit-2026/`. None is in the body. I did not fetch them. `/rust-dont-panic/` and `/rust-toolkit-2026/` are reserved for another agent.
- No publication date for the page was found. The only dates in the markup are asset version stamps (2026-09-10, 2026-09-17).
- No author name was found in the extracted page text.
