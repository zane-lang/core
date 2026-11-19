# regex

Regular expressions over a string's bytes. A pattern is compiled once, then
searched in time linear in the text: matching never backtracks, so no pattern
can make a search take exponential time.

How to use it, its verbs and its pattern syntax are on the Library pages:
[`docs/regex.md`](../../docs/regex.md), also at <https://zane-lang.org/std/regex>.
This file describes how the package searches.

## How it searches

A pattern compiles to an NFA, and the NFA to two DFAs: one runs forward to find
where the leftmost-first match ends, and one runs the reversed pattern back
from that end to find where the match starts. Between matches a skip loop
passes over text where no match can start, testing the rarest bytes every
match must contain (with `findPair` and `findAny`, which test 16 bytes at a
time). Groups come from a Pike VM run over just the bytes the DFAs found.

A pattern whose DFAs would grow past 10,000 states, such as `[ab]*a[ab]{14}`,
is searched by the Pike VM instead. Its results are the same, found more
slowly.

One search is linear in the text. `findAll`, `capturesAll` and `count` start
each search where the last match ended, so a pattern that must read far ahead
to rule out a longer, earlier alternative reads that stretch again for every
match: `a.*b|a` over a long run of `a` without a `b` takes time quadratic in
its length. Rust's `regex` crate has the same worst case.
