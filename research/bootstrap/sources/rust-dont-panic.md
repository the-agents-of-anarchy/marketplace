# Rust Don't Panic

Source: https://www.namtao.com/rust-dont-panic/  Fetched: 2026-10-15  Author: "Tris", No Boilerplate (page states no publication date)

## Thesis

Memory safety does not settle the matter, since a crash is still a crash: "But this answer does not satisfy me." The author argues Rust code can be written to never crash at runtime, by replacing `unwrap()`-style calls with `Result` combinators and enforcing a ban on panicking methods through strict Clippy lints in every project and in CI.

## Recommendations

| # | Topic | Recommendation (author's words) | Rationale given | Snippet |
|---|---|---|---|---|
| R1 | Error handling | "NEVER unwrap." | "unwrap_or_default() ... removed a call to unwrap()" | S1 |
| R2 | Error handling | "make yourself familiar with all of these, in addition to the excellent question-mark operator" | Combinators list in the page's section "RESULTS" and "OPTIONS" | none; cheatsheet linked |
| R3 | Testing for Ok | "Here's how to do it properly:" | "This is a lot of messy code to check." | S1 |
| R4 | Team enforcement | "the solution is to get the local tooling and remote CI to throw out all code that can crash." | "Maybe you can trust yourself to never commit a line that panics, but for the other people in your team" | none |
| R5 | Scope of ban | "This means disallowing all unwraps, expects, and any panicking methods, even and especially, the implicit ones." | Implicit panics as in indexing past the end of a vector | S2 |
| R6 | Clippy config | "Enable these lints in every project." | "They do two things: Teach you rust; Stop panics at runtime" | S2 |
| R7 | Exemptions | "Single lines, functions, or whole files can be exempted if you find these lints to be overly burdensome." | None beyond "overly burdensome" | none |
| R8 | Tests | "you CAN use them in unit tests, by default clippy ignores them in that context, even using the strict lints I recommend." | "how on earth to prototype code quickly" | S3 |
| R9 | Stricter proof | "If, on the other hand, you want to be MORE strict, and want to PROVE your code never panics" | no-panic crate "may produce false positives" | S4 |
| R10 | Style | "It's not just safer if you don't unwrap, it's actually way nicer to code like this!" | Pipelines of data transformed through functions | S5 |
| R11 | Target level | "starting at 99% is probably a good idea!" | Caveat: failed allocations are not covered | none |

## Snippets

S1, from R1, R3:

```rust
fn parse_add_one_v1(num: &str) -> i32 {
    let number = num.parse::<i32>();
    if number.is_ok() {
        number.unwrap() + 1 
    } else {
        i32::default() + 1
    }
}

fn parse_add_one_v2(num: &str) -> i32 {
    let number = num.parse::<i32>();
    number.unwrap_or_default() + 1
}
```

S2, from R5, R6, verbatim Cargo.toml block the page gives:

```toml
[lints.clippy]
pedantic = { level = "deny", priority = -1 }
nursery = { level = "deny", priority = -1 }
# DENY PANICS:
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

The page says the up-to-date version is at namtao.com/rust, which was not fetched.

S3, from R8:

```rust
#[cfg(test)]
mod tests {

    #[test]
    fn clippy_dgaf() {
        regex::Regex::new(r"(\d{4})-(\d{2})-(\d{2})").unwrap();
    }
}
```

S4, from R9:

```rust
use no_panic::no_panic;
#[no_panic]
fn demo(s: &str) -> &str {
    &s[1..] // can panic
}
fn main() {
    println!("{}", demo("\u{1f980}input string"));
}
```

S5, from R10:

```rust
fn purchase(basket: Result<Basket>) -> Result<Order> {
   basket
       .map(check_stock)
       .and_then(stage_payment)
       .map_err(log_error)
       .and_then(take_payment)
}
```

## Rejected or warned against

| # | Thing | Author's reason |
|---|---|---|
| W1 | Explicit `panic!`, implicit panics (indexing), unwrapping an `Err` | Listed as "the three typical ways that we can crash our rust code" from the Rust Book, Chapter 9 |
| W2 | Treating memory safety as sufficient | "Look, crashing IS safe, technically: Memory safe." followed by "But this answer does not satisfy me." |
| W3 | `unwrap()` and `expect()` left in code | "unwrap(), and its cousin, expect(), are todos we put in our code, but we were never meant to leave them there." |
| W4 | Copied example code containing unwraps | "This is the primary way unwraps creep into our code I think, through code examples copied and pasted without critique or modification" |
| W5 | Clippy defaults | "Out of the box, it has sensible but conservative defaults that allow panicking" |
| W6 | Reading the Rust Book's example guidance as permission for production code | The author quotes the Book's placeholder language and reads unwrap as a marker "for when you're ready to make your program more robust" |
| W7 | Failure to act on the Cloudflare incident | "Cloudflare certainly should have done this!" |
| W8 | `is_ok()` then `unwrap()` pattern | Replaced by `unwrap_or_default()`: "a lot of messy code to check" |

## Claims without evidence

- "Rust NEVER had nulls, the ecosystem was built around the Result type from the very start ... with no exceptions." Asserted.
- "Often it's far better to kill the program when an unrecoverable state has been reached than carry on with weird, undefined memory behaviour." Asserted.
- "This is the primary way unwraps creep into our code I think" Asserted, hedged by the author.
- "Clippy ... Out of the box, it has sensible but conservative defaults that allow panicking." Asserted. Not checked against Clippy documentation.
- "Enabling the groups pedantic and nursery will teach you good rust habits." Asserted.
- "errors are enriched with sensible suggestions and defaults." Asserted.
- "by default clippy ignores them in that context" Asserted for the test exemption. Not checked against Clippy documentation.
- Lint names in S2 (for example `indexing_slicing`, `unchecked_time_subtraction`) are reproduced as the page gives them. They were not checked against Clippy's lint list.
- "As Cloudflare showed ... badly written Rust can still cause problems" Asserted. The Cloudflare post is linked but was not fetched, so the causal link is unverified.
- "Most Rust types implement the default trait" Asserted.
- The no-panic output sample and the Clippy warning sample are shown without a stated Rust or Clippy version.
- "Code that has no execution paths that can panic at runtime ... for most applications, it's really good!" Asserted.

## Fetch notes

- First WebFetch attempt returned a summary, not the text. It declined to reproduce the page verbatim.
- Second WebFetch with a section-by-section prompt returned most of the page. That output is model-mediated, so quotes may differ in punctuation or capitalization.
- Raw HTML was fetched with curl, 65,097 bytes, and converted to text. Quotes in this file were checked against that text. The Rust Book quotes were checked against the page's own quotation of the Book, not against the Book.
- Not retrieved: the Clippy logo and meme images, site navigation, and the sidebar pages other than "Rust Don't Panic."
- Not fetched: the Cloudflare blog post, the Rust Book chapter, the wasabifan combinator cheatsheet, the emschwartz article, the no-panic crate, the "Rust on Rails" video, and namtao.com/rust.
- No publication date appears in the page HTML. The page says "4 years ago" for an earlier video and mentions a 2025 Cloudflare outage.
