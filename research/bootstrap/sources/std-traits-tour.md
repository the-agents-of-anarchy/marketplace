# Tour of Rust's Standard Library Traits
Source: https://raw.githubusercontent.com/pretzelhammer/rust-blog/refs/heads/master/posts/tour-of-rusts-standard-library-traits.md  Fetched: 2026-10-15  Author: not stated in the fetched text (repository owner per URL: pretzelhammer). Article header date: 31 March 2021.  Length: 5201 lines (144146 bytes)

## General rules (author's words)
| # | Rule | Quote |
|---|------|-------|
| 1 | Use associated types for one impl per type | "Use associated types when there should only be a single impl of the trait per type." |
| 2 | Use generic types for many impls per type | "Use generic types when there can be many possible impls of the trait per type." |
| 3 | No fixed verdict on the choice in the Add example | "So which `Add` trait above is the best? It really depends on the requirements of your program! They're all good in the right situations." |
| 4 | Trait items need the trait in scope | "Trait items cannot be used unless the trait is in scope." |
| 5 | Default impls may be overridden | "Traits can provide default impls for their functions and methods." |
| 6 | Generic blanket impls are not overridable | "Unlike default impls, which provide _an_ impl, generic blanket impls provide _the_ impl, so they are not overridable." |
| 7 | Overlapping impls are rejected | "These impls overlap, hence they conflict, hence Rust rejects the code to ensure trait coherence." |
| 8 | Subtrait bound is on Self | "It's a subtle yet important distinction to understand that the bound is on `Self`, i.e. the type impling `Subtrait`, and not on `Subtrait` itself." |
| 9 | Subtrait model | "In my opinion, the most simple and elegant mental model for understanding the relationship between subtraits and supertraits is: subtraits _refine_ their supertraits." |
| 10 | No rule links subtrait and supertrait impls | "Furthermore, there are no rules for how a type must impl both a subtrait and a supertrait. It can use the methods from either in the impl of the other." |
| 11 | Trait objects go behind a pointer | "Trait objects are unsized, so they must always be behind a pointer." |
| 12 | Object-safety, trait level | "A trait is object-safe if it meets these requirements: - trait doesn't require `Self: Sized` - all of the trait's methods are object-safe" |
| 13 | Object-safety, method level | "A trait method is object-safe if it meets these requirements: - method requires `Self: Sized` or - method only uses a `Self` type in receiver position" |
| 14 | Marker traits mark a property | "Their job is to \"mark\" the implementing type as having some property which is otherwise not possible to represent using the type system." |
| 15 | Auto traits must be marker traits | "Auto traits must be marker traits so the compiler can provide an automatic default impl for them, which would not be possible if they had any trait items." |
| 16 | Unsafe marking | "Traits can be marked unsafe to indicate that impling the trait might require unsafe code." |
| 17 | Derive macro conventions are not rules | "Note: derive macros are just procedural macros and can do anything. There's no hard rule that they must impl a trait, or that they can only work if all the members of the type impl a trait. These are just the conventions followed by the derive macros in the standard library." |
| 18 | Derive macros are named after their traits | "The derive macros are named after the traits they impl:" |
| 19 | Clone may be slow | "`Clone` makes no promises about the efficiency of this conversion, so it can be slow and expensive." |
| 20 | Priority order for performance | "For many programs, the best order of priorities is usually to build for correctness first, elegance second, and performance third, and only focus on performance after the program has been profiled and the performance bottlenecks have been identified." |
| 21 | Copy is opt-in | "Although `Copy` could be an auto trait, the Rust language designers decided that it's simpler and safer for types to explicitly opt into copy semantics, rather than silently inheriting copy semantics whenever the type is eligible, as the latter can cause surprising confusing behavior, which often leads to bugs." |
| 22 | Any rarely needed | "This trait rarely _needs_ to be used, because on top of parametric polymorphism being superior to ad-hoc polymorphism in most scenarios, the latter can also be emulated using enums, which are more type-safe and require less indirection." |
| 23 | Do not hand-implement ToString | "There's no need for us to impl this ourselves. In fact, we can't, because of this generic blanket impl that already automatically impls `ToString` for any type which impls `Display`" |
| 24 | Debug is for developers | "While the result of `Display` is intended to be seen by end users of a program, the `Debug` result is intended to only be shown to developers." |
| 25 | Cross-type equality only for same kind of data | "Generally, we should only impl equality between different types _if they contain the same kind of data_, and the only difference between the types is how they represent the data or how they allow interacting with the data." |
| 26 | Hash and Eq: derive both or implement both | "So we should always use the derive macro to impl both or manually impl both, but not mix the two, otherwise we risk breaking the above invariant." |
| 27 | Deref only for smart pointers | "`Deref` and `DerefMut` should only be implemented for smart pointer types." |
| 28 | Drop for external resource cleanup | "In general, if you're impling an abstraction over some resource that needs to be cleaned up after use, then that's a great reason to make use of the `Drop` trait." |
| 29 | Implement From, not Into | "We should only impl `From<T>` for our types, because the `Into<T>` impl is automatically provided by this generic blanket impl:" |
| 30 | No fixed rules for From | "There are no rules for when, how, or why we should impl `From<T>` for our types, so it's up to us to use our best judgement for every situation." |
| 31 | Errors are returned | "In Rust, errors are returned, not thrown." |
| 32 | Do not implement TryInto | "Similarly to `Into`, we should not impl `TryInto`, because its impl is provided by this generic blanket impl:" |
| 33 | No TryFrom where From exists | "Furthermore, we cannot impl `TryFrom` for a type if it already has a `From` impl, as an infallible `TryFrom` impl is automatically provided by this generic blanket impl:" |
| 34 | FromStr and TryFrom&lt;&amp;str&gt; forward to each other | "It doesn't matter which one we impl for a type first, as long as we forward the impl to the other one." |
| 35 | AsRef for wrappers | "Generally, it often only makes sense to impl `AsRef` for a type if it wraps some other type, to either provide additional functionality around the inner type, or to protect some invariant on the inner type." |
| 36 | AsRef only between semantically equivalent things | "`AsRef` is for cheap reference to reference conversions between semantically equivalent things" |
| 37 | Borrow and BorrowMut rarely implemented | "it's very rare that we would ever need to impl these traits for any of our types" |
| 38 | ToOwned rarely implemented | "it's very rare that we'll ever need to impl it for any of our types." |
| 39 | Iterators are usually separate types | "If a type is iterable, we almost always impl some other custom iterator type to iterate over it, rather than trying to make it iterate over itself:" |
| 40 | No rules on what can be an iterator | "there are no rules or conventions on what can or cannot be an iterator. If the type impls `Iterator` then it's an iterator." |
| 41 | ExactSizeIterator needs accurate size_hint | "We can also now impl `ExactSizeIterator` for `Range`, because it's a marker trait that marks the type as having an accurate `size_hint` impl:" |
| 42 | Override count, last, nth when size is known | "We should also provide our own impls for `count`, `last`, and `nth`, as their default impls assume the size of the iterator is unknown and rely on repeatedly calling `next`." |
| 43 | Reuse Extend in FromIterator | "If we're going to impl `FromIterator` for our own type, it's best to reuse an `Extend` impl if one exists:" |
| 44 | Mutable references to Read and Write | "These say that any mutable reference to a `Read` type is also `Read`, and same with `Write`." |
| 45 | Explicit conversion over implicit | "`AsRef` works above, because it makes the conversion between types explicit, and there's no room left over to develop any wrong ideas or expectations." |
| 46 | Closure traits not implementable on stable | "Although these traits exist, it's not possible to impl them for our own types in stable Rust. The only types we can create which impl these traits are closures." |
| 47 | Operators are trait calls | "All operators in Rust are associated with traits. If we'd like to impl operators for our types, we have to impl the associated traits." |
| 48 | T, &T, and &mut T need separate impls | "Within Rust's type system, for some type `T`, the types `T`, `&T`, and `&mut T` are all treated as unique distinct types, which means we have to provide trait impls for each of them separately." |
| 49 | Generics vs trait objects | "Generics give us compile-time polymorphism, while trait objects give us run-time polymorphism." |
| 50 | Implicit Sized bounds | "All generic types get an implicit `Sized` bound." |
| 51 | Implicit ?Sized on traits | "There's an implicit `?Sized` bound on all traits." |
| 52 | PartialEq must be symmetric and transitive | "All `PartialEq<Rhs>` impls must ensure that equality is symmetric and transitive." |
| 53 | PartialOrd must be asymmetric and transitive | "All `PartialOrd` impls must ensure that comparisons are asymmetric and transitive." |
| 54 | Copy is a fast clone | "A clone may be slow and expensive but a copy is guaranteed to be fast and cheap, so a copy is just a fast clone." |

## Traits

### Trait Basics
Concepts the article covers before the traits. Each row is a concept, not a trait.

| Trait | Purpose | Implement/derive rule (quoted) | Gotcha (quoted) |
|---|---|---|---|
| Self | "`Self` always refers to the implementing type." | none stated | none stated |
| Functions (trait items) | "A trait function is any function whose first parameter does not use the `self` keyword." | none stated | none stated |
| Methods (trait items) | "A trait method is any function whose first parameter uses the `self` keyword and is of type `Self`, `&Self`, `&mut Self`." | none stated | none stated |
| Associated types (trait items) | "A trait can have associated types. This is useful when we need to use some type other than `Self` within function signatures" | "Use associated types when there should only be a single impl of the trait per type." | none stated |
| Generic parameters (trait items) | "The term _\"generic parameters\"_ broadly refers to generic type parameters, generic lifetime parameters, and generic const parameters." | none stated | none stated |
| Scope | "Trait items cannot be used unless the trait is in scope." | "Trait items cannot be used unless the trait is in scope." | "Most Rustaceans learn this the hard way the first time they try to write a program that does anything with I/O, because the `Read` and `Write` traits are not in the standard library prelude" |
| Derive macros | "quickly and conveniently impl a trait on a type if all of its members also impl the trait" | "The derive macros are named after the traits they impl:" | none stated |
| Default impls | "Traits can provide default impls for their functions and methods." | "Traits can provide default impls for their functions and methods." | none stated |
| Generic blanket impls | "A generic blanket impl is an impl on a generic type instead of a concrete type." | "Unlike default impls, which provide _an_ impl, generic blanket impls provide _the_ impl, so they are not overridable." | "These impls overlap, hence they conflict, hence Rust rejects the code to ensure trait coherence." |
| Subtraits and supertraits | "the bound is on `Self`, i.e. the type impling `Subtrait`, and not on `Subtrait` itself" | "subtraits _refine_ their supertraits." | "Hopefully, the examples above show that the relationship between subtraits and supertraits can be complex." |
| Trait objects | "Generics give us compile-time polymorphism, while trait objects give us run-time polymorphism." | "A trait is object-safe if it meets these requirements: - trait doesn't require `Self: Sized` - all of the trait's methods are object-safe" | none stated |
| Marker traits | "Marker traits are traits that have no trait items." | "Their job is to \"mark\" the implementing type as having some property which is otherwise not possible to represent using the type system." | none stated |
| Auto traits | "Auto traits are traits that get automatically implemented for a type if all of its members also impl the trait." | "Auto traits must be marker traits so the compiler can provide an automatic default impl for them" | none stated |
| Unsafe traits | "Traits can be marked unsafe to indicate that impling the trait might require unsafe code." | "Both `Send` and `Sync` are marked `unsafe`, because if they aren't automatically implemented for a type, that means it must contains some non-`Send` or non-`Sync` member" | none stated |

Scope, prelude list as the article gives it: "AsMut, AsRef, Clone, Copy, Default, Drop, Eq, Fn, FnMut, FnOnce, From, Into, ToOwned, IntoIterator, Iterator, PartialEq, PartialOrd, Send, Sized, Sync, ToString, Ord."

### Auto Traits

| Trait | Purpose | Implement/derive rule (quoted) | Gotcha (quoted) |
|---|---|---|---|
| Send and Sync | "If a type is `Send`, that means it's safe to send between threads. If a type is `Sync`, that means it's safe to share references of it between threads." | "Both `Send` and `Sync` are marked `unsafe`, because if they aren't automatically implemented for a type, that means it must contains some non-`Send` or non-`Sync` member, and we have to take extra care as the implementers" | "The only notable `Send` exception is `Rc` and the only notable `Sync` exceptions are `Rc`, `Cell`, and `RefCell`." |
| Sized | "If a type is `Sized`, that means its size in bytes is known at compile-time, and it's possible to put instances of the type on the stack." | "All generic types get an implicit `Sized` bound." | "Sizedness of types, and its implications, is a subtle, yet huge, topic that affects a lot of different aspects of the language." |

### General Traits

| Trait | Purpose | Implement/derive rule (quoted) | Gotcha (quoted) |
|---|---|---|---|
| Default | "It's possible to construct default values of `Default` types." | "There's also a `Default` derive macro, which works when all of a types's members are `Default`" | none stated |
| Clone | "We can convert immutable references of `Clone` types into owned values, i.e. `&T` -> `T`." | "To quickly impl `Clone` on a type, we can use the derive macro:" | "`Clone` makes no promises about the efficiency of this conversion, so it can be slow and expensive." Also: "People also commonly use cloning as an escape hatch, to avoid dealing with the borrow checker." |
| Copy | "`Copy` promises the copy operation will be a simple bitwise copy, so it will be very fast and efficient." | "We cannot impl `Copy` ourselves, only the compiler can provide an impl, but we can tell it to do so by using the `Copy` derive macro, together with the `Clone` derive macro since `Copy` is a subtrait of `Clone`" | "Impling `Copy` for a type changes its behavior when it gets moved." |
| Any | "Rust's style of polymorphism is parametric, but if we're looking to use a more ad-hoc style of polymorphism, similar to dynamically-typed languages, then we can emulate that using the `Any` trait." | "We don't have to manually impl this trait for our types, because it's already covered by this generic blanket impl:" | "This trait rarely _needs_ to be used" |

### Formatting Traits

| Trait | Purpose | Implement/derive rule (quoted) | Gotcha (quoted) |
|---|---|---|---|
| Display and ToString | "`Display` types can be serialized into `String`s that are friendly to the end users of the program." | "There's no need for us to impl this ourselves. In fact, we can't, because of this generic blanket impl that already automatically impls `ToString` for any type which impls `Display`" (ToString) | none stated |
| Debug | "the `Debug` result is intended to only be shown to developers." | "`Debug` can be derived on a type if all of its members are `Debug`:" | "The only downside is that `dbg!` isn't automatically stripped in release builds, so we have to manually remove it from our code if we don't want to ship it in the final executable." |

### Operator Traits

| Trait | Purpose | Implement/derive rule (quoted) | Gotcha (quoted) |
|---|---|---|---|
| PartialEq and Eq | "`PartialEq<Rhs>` types can be checked for equality to `Rhs` types using the `==` operator." | "If all the members of a type impl `PartialEq` then it can be derived:" and "Generally, we should only impl equality between different types _if they contain the same kind of data_" | "It works and kinda makes sense." then "However, something's missing: symmetry!" then "But adding symmetry just broke transitivity! Oops." Eq: "Floats are `PartialEq` but not `Eq`, because `NaN != NaN`." |
| Hash | "`Hash` types can be hashed using a `Hasher`." | "So we should always use the derive macro to impl both or manually impl both, but not mix the two, otherwise we risk breaking the above invariant." | Invariant, stated as "If a type impls both `Hash` and `Eq`, those impls must agree with each other, such that for all `a` and `b`, if `a == b` then `a.hash() == b.hash()`." |
| PartialOrd and Ord | "`PartialOrd<Rhs>` types can be compared to `Rhs` types using the `<`, `<=`, `>`, and `>=` operators." | "If all the members of a type impl `PartialOrd` then it can be derived:" | "The `PartialOrd` derive macro orders types based on the lexicographical order of their members:" Field order changes the impl: "generates DIFFERENT PartialOrd impl that orders Points based on y member first and x member second". Floats: "Floats impl `PartialOrd`, but not `Ord`, because both `NaN < 0 == false` and `NaN >= 0 == false` are simultaneously true." |
| Add and AddAssign | "`Add<Rhs, Output = T>` types can be added to `Rhs` types and will produce `T` as output." | "Within Rust's type system, for some type `T`, the types `T`, `&T`, and `&mut T` are all treated as unique distinct types, which means we have to provide trait impls for each of them separately." | "We have two separate impls of `Add` for `Point` and `&Point` and they _happen_ to do the same thing currently, but there's no guarantee that they will in the future!" |
| FnOnce, FnMut, Fn | Closure invocation, per the article's table: `Fn` immutable, `FnMut` mutable, `FnOnce` one-time. | "Although these traits exist, it's not possible to impl them for our own types in stable Rust. The only types we can create which impl these traits are closures." | "An `FnOnce` closure can only be called once, because it consumes some value as part of its execution:" |
| Deref and DerefMut | "`Deref<Target = T>` types can be dereferenced to `T` types using the dereference operator `*`." | "`Deref` and `DerefMut` should only be implemented for smart pointer types." | "The main takeaway from this section is: do not try to be cute or clever with `Deref` and `DerefMut` impls." Also: "First of all, deref coercion only works on references, so it doesn't work when we actually want to pass ownership:" Also: "In languages with OOP-style data inheritance, the value of `self` within a method is always equal to the type that called the method, but in the case of Rust, the value of `self` is always equal to the type that implemented the method:" Also: "We never implemented `Clone` for `SortedVec` so when we call the `.clone()` method the compiler is using deref coercion to resolve that method call on `Vec` and so it returns a `Vec` and not a `SortedVec`!" |
| Index and IndexMut | "We can index `[]` into `Index<T, Output = U>` types with `T` values, and the index operation will return `&U` values." | "there's no requirement that the `Idx` type has to be a number type or a `Range`, it could be an enum!" | "It's kinda confusing at first, because it seems like the `Index` trait does not follow its own method signature, but really it's just questionable syntax sugar." |
| Drop | "If a type impls `Drop`, then `drop` will be called on the type when it goes out of scope but before it's destroyed." | "We will rarely need to impl this for our types, but a good example of where it's useful is if a type holds on to some external resources that need to be cleaned up when the type is destroyed." | none stated |

RangeBounds appears only in the operator table, with no section.

### Conversion Traits

| Trait | Purpose | Implement/derive rule (quoted) | Gotcha (quoted) |
|---|---|---|---|
| From and Into | "`From<T>` types allow us to convert `T` into `Self`." and "`Into<T>` types allow us to convert `Self` into `T`." | "We should only impl `From<T>` for our types, because the `Into<T>` impl is automatically provided by this generic blanket impl" and "There are no rules for when, how, or why we should impl `From<T>` for our types, so it's up to us to use our best judgement for every situation." | "The impl is not symmetric, so if we'd like to convert `Point`s into tuples and arrays, we have to explicitly add those as well" |

### Error Handling

| Trait | Purpose | Implement/derive rule (quoted) | Gotcha (quoted) |
|---|---|---|---|
| Error | "In Rust, errors are returned, not thrown." | "The most idiomatic way to propagate errors is to use the `?` operator" | "The obvious downside of stringifying every error is that we throw away type information, which makes it harder for the caller to handle the errors." Box: "While being more concise, this seems to suffer from the same downside of the previous approach, by throwing away type information." |

### Conversion Traits Continued

| Trait | Purpose | Implement/derive rule (quoted) | Gotcha (quoted) |
|---|---|---|---|
| TryFrom and TryInto | "`TryFrom` and `TryInto` are the fallible versions of `From` and `Into`." | "Similarly to `Into`, we should not impl `TryInto`, because its impl is provided by this generic blanket impl" and "we cannot impl `TryFrom` for a type if it already has a `From` impl" | none stated |
| FromStr | "`FromStr` types allow performing a fallible conversion from `&str` into `Self`." | "It doesn't matter which one we impl for a type first, as long as we forward the impl to the other one." | none stated |
| AsRef and AsMut | "`AsRef` is for cheap reference to reference conversions." | "Generally, it often only makes sense to impl `AsRef` for a type if it wraps some other type" | "This works and kinda makes sense at first, but quickly falls apart if we add more members to `User`:" Also: "`Deref` didn't work in the prior version of the example above, because deref coercion is an implicit conversion between types, which leaves room for people to mistakenly formulate the wrong ideas and expectations for how it will behave." |
| Borrow and BorrowMut | "These traits were invented to solve the very specific problem of looking up `String` keys in `HashSet`s, `HashMap`s, `BTreeSet`s, and `BTreeMap`s using `&str` values." | "it's very rare that we would ever need to impl these traits for any of our types" | none stated |
| ToOwned | "`ToOwned` is a more generic version of `Clone`." | "it's very rare that we'll ever need to impl it for any of our types." | none stated |

### Iteration Traits

| Trait | Purpose | Implement/derive rule (quoted) | Gotcha (quoted) |
|---|---|---|---|
| Iterator | "`Iterator<Item = T>` types can be iterated and will produce `T` types." | "If a type is iterable, we almost always impl some other custom iterator type to iterate over it, rather than trying to make it iterate over itself:" | "Something that is not immediately obvious to beginner Rustaceans, but that intermediate Rustaceans take for granted, is that most types are not their own iterators." Also: "Not very easy to discover. But anyway, now we know." |
| ExactSizeIterator | "a marker trait that marks the type as having an accurate `size_hint` impl" (article wording) | "We should also provide our own impls for `count`, `last`, and `nth`, as their default impls assume the size of the iterator is unknown and rely on repeatedly calling `next`." | "The default impls provided by the `Iterator` trait for the methods `size_hint`, `count`,  `last`, and `nth` are suboptimal if we know the exact size of the data we're iterating over" Also: "It's not useful at all!" (on the default size_hint) |
| IntoIterator | "`IntoIterator` types can be converted into iterators, hence the name." | none stated | none stated |
| Extend | "`Extend` types can be extended from an iterator. They're usually collections." | "The above example is meant to be illustrative, the idiomatic solution would be to defer to the inner `Vec`'s `extend` impl" | none stated |
| FromIterator | "`FromIterator` types can be created from an iterator, hence the name." | "If we're going to impl `FromIterator` for our own type, it's best to reuse an `Extend` impl if one exists:" | none stated |

### I/O Traits

| Trait | Purpose | Implement/derive rule (quoted) | Gotcha (quoted) |
|---|---|---|---|
| Read and Write | Byte-stream reading and writing. The article uses them to show tests: "so we can easily unit test our file handling functions using `String`s" | "These say that any mutable reference to a `Read` type is also `Read`, and same with `Write`." | none stated |

## Fetch notes
- Fetched with `curl -sL` to `/tmp/ra-std-traits.md` on 2026-10-15. The file is 5201 lines and 144146 bytes. I read all of it in eight consecutive parts.
- The fetched text names no author. The URL places it in the pretzelhammer/rust-blog repository.
- Traits listed only in the operator table, with no section: BitAnd, BitAndAssign, BitXor, BitXorAssign, Div, DivAssign, Mul, MulAssign, Neg, Not, Rem, RemAssign, Shl, ShlAssign, Shr, ShrAssign, Sub, SubAssign, RangeBounds. The article says: "Going over all of these would be very redundant."
- Snippet typos in the fetched text: the TryFrom blanket impl declares `enum Inflallible {}` but returns `Infallible`. The article writes `Index<T, Output = U>` where the Index trait is `Index<Idx>`. I recorded quotes exactly as written.
- I did not compile the article's code. Compiler error text and ✅/❌ markers are the article's own. The Copy section presents an impl as "what the derive macro generates"; I report that as the article's claim.
- Linked article `sizedness-in-rust.md` is referenced but not fetched. It sits outside this extraction's scope.
