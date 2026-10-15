# Your Clippy Config Should Be Stricter

Source: https://emschwartz.me/your-clippy-config-should-be-stricter/  Fetched: 2026-10-15  Author: Evan Schwartz (named only in WebFetch summaries; the raw page text shows no byline, so this attribution is asserted)

Page date as shown on the raw page: 30 Apr, 2026.

## Thesis

- "If it compiles, it works." is a feeling Rust engineers value, and the author says "I realized that it's useful to enable more Clippy lints to catch bugs that the compiler won't prevent by itself."
- The motivating bug: "byte index 200 is not a char boundary", a panic that stopped a Tokio worker running an email sending loop. The author says "A function naively truncated article summaries without checking for UTF-8 character boundaries."
- The author argues the risk is higher with coding agents: "A seasoned Rust engineer might naturally avoid patterns that could cause problems. An agent or a junior colleague might not."
- The method is selective opt-in: "I'm outlining a selective opt-in here."
- Stated scope: "stricter linting can make your code safer, whether or not you're coding with LLMs."

## Config snippets (verbatim)

Block 1, from the "My Configs" section, verbatim from the raw `<pre>` element:

```toml
# Workspace Cargo.toml

[workspace.lints.clippy]
# Don't Panic - prevent panics from unwraps and unsafe slicing or indexing
string_slice = "warn"
indexing_slicing = "warn"
unwrap_used = "warn"
panic = "warn"
todo = "warn"
unimplemented = "warn"
unreachable = "warn"
get_unwrap = "warn"
unwrap_in_result = "warn"
unchecked_time_subtraction = "warn"
panic_in_result_fn = "warn"
# Optional - see post for caveats
# expect_used = "warn"
# arithmetic_side_effects = "warn"

# Don't Fail Silently - prevent dropped futures and swallowed errors
let_underscore_future = "warn"
let_underscore_must_use = "warn"
unused_result_ok = "warn"
map_err_ignore = "warn"
assertions_on_result_states = "warn"

# Don't Do Bad Async Stuff - prevent deadlocks and concurrency bugs
await_holding_lock = "warn"
await_holding_refcell_ref = "warn"
if_let_mutex = "warn"  # only relevant on editions before 2024
large_futures = "warn"

# Don't Do Unsafe Things with Memory
mem_forget = "warn"
undocumented_unsafe_blocks = "warn"
multiple_unsafe_ops_per_block = "warn"
unnecessary_safety_doc = "warn"
unnecessary_safety_comment = "warn"

# Don't Do Potentially Incorrect Things with Numbers
float_cmp = "warn"
float_cmp_const = "warn"
lossy_float_literal = "warn"
cast_sign_loss = "warn"
invalid_upcast_comparisons = "warn"
# Optional - these effectively force you to document numeric invariants
# cast_possible_wrap = "warn"
# cast_precision_loss = "warn"
# cast_possible_truncation = "warn"

# Don't Do Bad Things That are Easy to Avoid
rc_mutex = "warn"
debug_assert_with_mut_call = "warn"
iter_not_returning_iterator = "warn"
expl_impl_clone_on_copy = "warn"
infallible_try_from = "warn"
dbg_macro = "warn"

# Don't `allow` Your Way Around These Lints - every suppression must be
# a deliberate #[expect(..., reason = "…")] rather than a silent #[allow]
allow_attributes = "warn"
allow_attributes_without_reason = "warn"
```

Block 2, from the "My Configs" section, verbatim from the raw `<pre>` element:

```toml
# Workspace clippy.toml

allow-indexing-slicing-in-tests = true
allow-panic-in-tests = true
allow-unwrap-in-tests = true
allow-expect-in-tests = true
allow-dbg-in-tests = true
```

Block 2 is labeled clippy.toml by the page heading, and the file name is inferred from that heading.

No `#![...]` attributes and no shell commands appear on the page.

## Lints named

Level set: every lint in Block 1 is `"warn"`. The author's stated preference: "I personally prefer setting these to `warn` and running Clippy with `-D warnings` before committing and on CI."

Reasons are the author's description bullets or section sentences. Where the author gave only a group sentence, the group sentence is quoted and marked (group).

| # | Lint | Level set | Author's reason |
|---|---|---|---|
| 1 | string_slice | warn | "`&s[a..b]` on `&str` (UTF-8 boundary panic). This would have caught my initial bug." |
| 2 | indexing_slicing | warn | "`arr[i]` / `&arr[a..b]`"; "using safe methods like `.get()` and iterators instead of slicing prevents pretty severe footguns" |
| 3 | unwrap_used | warn | "`Option::unwrap` / `Result::unwrap`" (group: "This group prevents panics from unwraps and unsafe slicing or indexing") |
| 4 | panic | warn | "`panic!()` calls" (group) |
| 5 | todo | warn | "placeholder-panic macros" (group) |
| 6 | unimplemented | warn | "placeholder-panic macros" (group) |
| 7 | unreachable | warn | "placeholder-panic macros" (group) |
| 8 | get_unwrap | warn | "`vec.get(i).unwrap()`" (group) |
| 9 | unwrap_in_result | warn | "`.unwrap()` inside functions that return a `Result`" (group) |
| 10 | unchecked_time_subtraction | warn | "`Instant - Instant` panics if the second is larger" |
| 11 | panic_in_result_fn | warn | "`panic!`/`assert!` inside a function that returns a `Result`" |
| 12 | let_underscore_future | warn | "`let _ = future` drops without awaiting" (group: "prevent dropped futures and swallowed errors") |
| 13 | let_underscore_must_use | warn | "`let _ = result_returning()` swallows errors" |
| 14 | unused_result_ok | warn | "`result.ok();` silently drops `Err`" |
| 15 | map_err_ignore | warn | "`.map_err(|_| MyErr)` loses source error" |
| 16 | assertions_on_result_states | warn | "`assert!(r.is_ok())` discards the error message" |
| 17 | await_holding_lock | warn | "`MutexGuard` across `.await`" (group: "prevent deadlocks and concurrency bugs") |
| 18 | await_holding_refcell_ref | warn | "`RefCell::borrow_mut` across `.await`" (group) |
| 19 | if_let_mutex | warn | "`if let _ = mutex.lock() { other_lock() }` deadlock pattern." Caveat: "only relevant if you're using an earlier edition than 2024" (see relaxations) |
| 20 | large_futures | warn | "a `Future` that is too large can cause a stack overflow" |
| 21 | mem_forget | warn | "`mem::forget` leaks" (group: "Don't Do Unsafe Things with Memory") |
| 22 | undocumented_unsafe_blocks | warn | "every `unsafe {}` needs a `// SAFETY:` comment" |
| 23 | multiple_unsafe_ops_per_block | warn | "one unsafe op per block (one comment per op)" |
| 24 | unnecessary_safety_doc | warn | "only document safety where it belongs" (paired with 25) |
| 25 | unnecessary_safety_comment | warn | "only document safety where it belongs" (paired with 24) |
| 26 | float_cmp | warn | "`a == b` on floats" (group: "Don't Do Potentially Incorrect Things with Numbers") |
| 27 | float_cmp_const | warn | "stricter, also flags comparisons against constants" |
| 28 | lossy_float_literal | warn | "silently-rounded float literals (`16_777_217.0_f32`)" |
| 29 | cast_sign_loss | warn | "`(-1_i8) as u64` wraps to `u64::MAX`" |
| 30 | invalid_upcast_comparisons | warn | "`(x: i32 as i64) > i32::MAX as i64` always false" |
| 31 | rc_mutex | warn | "`Rc<Mutex<_>>` (`Rc` is single-threaded)" (group: "Don't Do Bad Things that are Easy to Avoid") |
| 32 | debug_assert_with_mut_call | warn | "`debug_assert!(stack.pop().is_some())` differs in debug vs release" |
| 33 | iter_not_returning_iterator | warn | "method named `iter` returning non-`Iterator`" |
| 34 | expl_impl_clone_on_copy | warn | "manual `Clone` impl that disagrees with `Copy`" |
| 35 | infallible_try_from | warn | "`TryFrom` impl whose error is `Infallible` should be `From`" |
| 36 | dbg_macro | warn | "`dbg!` calls should be removed after debugging" |
| 37 | allow_attributes | warn | "every `#[allow]` becomes `#[expect(..., reason = "…")]`" (group: "These two are especially useful if you're using a coding agent.") |
| 38 | allow_attributes_without_reason | warn | "every `#[expect]` requires a reason" |

Named by the author but not set in the config:

| Lint | Level set | Author's reason |
|---|---|---|
| expect_used | commented out (`# expect_used = "warn"`), marked "Optional" | "You might or might not want to enable `expect_used`." The message passed to `expect` "should already document why"; enabling it "may end up duplicating the same rationale" |
| arithmetic_side_effects | commented out, marked "Optional" | "a real judgement call"; "around 15% of the warnings caught real issues and 85% was just noise" (the author's estimate on their own codebase) |
| cast_possible_wrap | commented out, marked "Optional" | "these effectively force you to document numeric invariants"; "You might or might not find that useful." |
| cast_precision_loss | commented out, marked "Optional" | Same as cast_possible_wrap |
| cast_possible_truncation | commented out, marked "Optional" | Same as cast_possible_wrap |
| blanket_clippy_restriction_lints | not set | Named as the Clippy lint that exists "to discourage you from enabling this category" |
| big_endian_bytes | not set | Named as a contradiction: the restriction category "contains lints to enforce both `big_endian_bytes` and `little_endian_bytes`" |
| little_endian_bytes | not set | Same as big_endian_bytes |
| missing_lints_inheritance | not set | "On nightly, there's a `missing_lints_inheritance` lint that specifically checks for this." |

Config keys set in the clippy.toml block are not lints. They are Clippy options: allow-indexing-slicing-in-tests, allow-panic-in-tests, allow-unwrap-in-tests, allow-expect-in-tests, allow-dbg-in-tests, each set to `true`.

## Lints the author allows or relaxes, with reason

- **if_let_mutex**: still set to `"warn"` in the config, with a comment "only relevant on editions before 2024." The author's text: "The scoping was fixed in the 2024 edition so this is no longer an issue." The 2024 scoping claim is asserted; no source is cited.
- **expect_used**: commented out. Reason: the author is unsure, and says it may duplicate rationale.
- **arithmetic_side_effects**: commented out. Reason: noise. The author's estimate is "85%" noise on their codebase.
- **cast_possible_wrap, cast_precision_loss, cast_possible_truncation**: commented out. Reason: "You might or might not find that useful."
- **Test allowances in clippy.toml**: panic, unwrap, indexing/slicing, expect, and dbg are allowed in tests. The page gives no reason for this block. The key names imply test code only. This is an inference.
- **Suppression is allowed with a reason**: "Instead of letting the agent write `#[allow(lint_we_wanted_to_enable)]`, it should provide a reason wherever it's disabling a lint." Suppression is permitted when it carries `reason`.
- **Unenabled lints are allowed**: "Every project is different and you should look through the available lints to see which ones make sense for your project."

## Rejected or warned against

- **Enabling whole categories**: "Why Not Enable Lint Categories?" The author says "none of these categories cleanly map onto 'don't let this panic or do the wrong thing in production'." The author quotes the Clippy docs: "The `restriction` category should, emphatically, not be enabled as a whole."
- **Case-by-case enabling**: The author quotes the Clippy docs: "Lints should be considered on a case-by-case basis before enabling".
- **Silent allow**: "Instead of letting the agent write `#[allow(...)]`" (see relaxations for the permitted form).
- **Deny on CI without a pinned Rust version**: "if you set Clippy on CI to deny warnings, you should make sure to specify a specific Rust version. Otherwise, lints added in newer versions will cause your build to fail."
- **MSRV mismatch**: "check when lints landed in stable if your Minimum Supported Rust Version predates 1.95, as some of these may have been added after your MSRV."
- **Assuming workspace inheritance**: "each workspace crate needs to opt in to inheriting lints with `lints.workspace = true`, rather than inheriting the lints by default."
- **Noisy lints**: indexing_slicing and string_slice "may produce many warnings"; arithmetic_side_effects is "noise" in the author's estimate.

## Claims without evidence

- "This would have caught my initial bug." (string_slice) Asserted. The article gives no test showing the lint fires on the original code.
- "Inapplicable lints serve as cheap tripwires in case the given pattern is ever added later." Asserted.
- "Stricter Clippy rules make it easier to rely on code you didn't personally write." Asserted.
- "enabling new lints on an existing codebase is tedious, and exactly the kind of task that is good to hand to a coding agent." Asserted.
- "the Cloudflare `unwrap` bug that 'broke the internet'" (2025). Cited only by name, with no link. Asserted as an analogy.
- The Scour incident (the Friday email job stopping): a single author report. The article shows the panic message, not a reproduction.
- "around 15% of the warnings caught real issues and 85% was just noise." One codebase, one estimate. Anecdotal.
- "The scoping was fixed in the 2024 edition." No citation.
- "prevents pretty severe footguns, so I would argue that it's worth it." Argued, not measured.
- "a `Future` that is too large can cause a stack overflow" (large_futures). No example given.
- Lints `big_endian_bytes` and `little_endian_bytes` contradict each other. The author's example. Not checked against Clippy source here.
- "lints added in newer versions will cause your build to fail." Credited to a commenter, "Thanks to u/scook0 for pointing this out!" Not tested.
- Attribution of quotes to "the Clippy docs" is the author's. Not checked against the Clippy docs, which were not fetched.

## Fetch notes

- **WebFetch, first call**: Returned a summary, not the full article. The tool said it could not reproduce the article verbatim.
- **WebFetch, retry asking for every code block**: Returned a second summary and declined to reproduce every block.
- **curl, same URL**: HTTP 200, 48,323 bytes. The article text and both config blocks were extracted from the raw HTML with entities decoded. The config blocks were checked against the raw `<pre>` elements. The raw page was saved to `/tmp/clippy-fetch/page.html`, outside the repo.
- **Byline**: Absent from the raw page text. The name Evan Schwartz comes only from the WebFetch summaries.
- **Not read**: The follow-up post "Your Clippy Config Should Be Stricter-er" by Billy Levin, which the page links. The Clippy docs. The Cloudflare incident. The r/rust, Lobsters, and Hacker News discussions.
- **Quote fidelity**: Quotes are from the raw article text. Inline `<code>` markup was rendered as backticks in this file.
