# regex

Regular expressions over a string's bytes. A pattern is compiled once, then
searched in time linear in the text: matching never backtracks, so no pattern
can make a search take exponential time.

```zane
package hello;

import core$;
import regex$;

Unit main() {
	console Console(@program$console);
	date Regex = compile("(?<year>\\d{4})-(?<month>\\d\\d)") ? e {
		console!print("bad pattern: " + e.message);
		return Unit();
	}
	text String = String("released 2026-11, patched 2027-01");
	c Captures = date:captures(text);
	console!print(c:named("year"):text(text));
	console!print(String(date:count(text)));
	return Unit();
}
```

This prints `2026` and `2`.

## Using it

| Verb | What it gives |
|---|---|
| `compile(pattern)` | The `Regex`, or a `RegexError` (its `message`, and `at`, the byte of the pattern where it was found) |
| `r:isMatch(text)` | Whether `r` matches anywhere in `text` |
| `r:find(text)` | The leftmost-first match, a `Match` |
| `r:findFrom(text, from)` | The leftmost-first match starting at or after byte `from` |
| `r:findAll(text)` | Every match, left to right, as a `List<Match>` |
| `r:count(text)` | The number of matches `findAll` finds |
| `r:captures(text)`, `r:capturesFrom(text, from)` | A match and its groups, a `Captures` |
| `r:capturesAll(text)` | Every match with its groups |
| `r:groupCount()` | The number of groups in the pattern |

A `Match` is a position and a length, counted as `byteAt` counts: `start` is
its first byte (from 1), `count` its number of bytes, `m:end()` the byte after
it, and `m:text(text)` the bytes it covers. When nothing is found, `start` is
0, which `m:found()` tests.

A `Captures` holds group 0, the whole match, then each group in the order its
`(` opens. `c:group(k)` is group `k`'s match, and `c:named(name)` the match of
the group named `name`. A group that took no part in the match, a group the
pattern does not have, and every group of a search that found nothing give a
`Match` whose `start` is 0. `c:found()` says whether there was a match, and
`c:size()` counts the groups, group 0 included.

`findAll` and `count` take the matches left to right without overlap, as
Rust's `find_iter` does. An empty match never comes right where the previous
match ended: `a*` on `aab` finds `aa`, then the empty match after the `b`.

`findFrom` and `capturesFrom` start the search at a byte, but an assertion
still sees the bytes before it: `\bx` does not match at the `x` of `ax` even
when the search starts there.

## Syntax

Matching is **leftmost-first**, as in Perl, PCRE, Python and Rust: of the
matches that start leftmost, the one the pattern prefers wins, so `a|ab` on
`ab` matches `a`.

| Pattern | Matches |
|---|---|
| `x` | The byte `x`; a byte that is an operator is escaped, as `\.` or `\(` |
| `.` | Any byte but a newline; any byte with the `s` flag |
| `[abc]`, `[a-z]`, `[^a-z]` | A byte in the class, or with `^` not in it. A `]` right after the `[` or `[^` is one of the class's bytes, and so is a `-` at either end |
| `[[:alpha:]]`, `[[:^digit:]]` | A POSIX class, inside a class: `alnum`, `alpha`, `ascii`, `blank`, `cntrl`, `digit`, `graph`, `lower`, `print`, `punct`, `space`, `upper`, `word`, `xdigit`; `^` negates it |
| `\d`, `\w`, `\s` | A digit, a word byte (`[0-9A-Za-z_]`), a space byte (`[\t\n\v\f\r ]`); `\D`, `\W` and `\S` are their complements. They work inside classes too |
| `\n`, `\t`, `\r`, `\f`, `\v`, `\a`, `\xHH` | A newline, tab, carriage return, form feed, vertical tab, bell, or the byte with hexadecimal value `HH` |
| `xy`, `x\|y` | `x` then `y`; `x` or else `y` |
| `x*`, `x+`, `x?` | Zero or more, one or more, zero or one `x`, as many as can match |
| `x{n}`, `x{n,}`, `x{n,m}` | Exactly `n`, at least `n`, `n` to `m` of `x`; the bounds are at most 1000. A `{` that starts none of these is the byte `{` |
| `x*?`, `x+?`, `x??`, `x{n,m}?` | The same repeats, as few as can match |
| `(x)` | `x`, captured as the next group |
| `(?<name>x)`, `(?P<name>x)` | `x`, captured as the next group, named `name` |
| `(?:x)` | `x`, grouped without capturing |
| `^`, `$` | The start and the end of the text; with the `m` flag, of a line as well |
| `\A`, `\z` | The start and the end of the text, whatever the flags |
| `\b`, `\B` | A word boundary, where a word byte meets a byte that is none or the edge of the text; anywhere else |
| `(?flags)` | Sets flags until the end of the enclosing group |
| `(?flags:x)` | `x` with the flags set |

The flags are `i`, matching ASCII letters in either case, `m`, making `^` and
`$` match at the start and end of every line, and `s`, letting `.` match a
newline. A `-` turns the flags after it off: `(?i)a(?-i)b` matches `Ab` but
not `AB`.

The pattern is bytes, and so is the text: the classes, the cases and the word
bytes are ASCII's. A byte of a UTF-8 character outside ASCII matches only
itself, so a literal non-ASCII character matches, but `.` takes one byte of it.

Not supported: look-ahead and look-behind (`(?=`, `(?!`, `(?<=`, `(?<!`),
back-references, possessive repeats, atomic groups, Unicode classes, and the
`x` flag. Each is refused with a `RegexError` rather than read some other way.

A repeat of a part that can itself match the empty string, such as `(a*)*` or
`(?:x?)+`, may choose a different match, or different groups, from a
backtracking engine's: which of its empty iterations wins depends on the order
a backtracking engine tries them in.

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
