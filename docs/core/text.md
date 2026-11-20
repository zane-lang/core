# Text

This page covers `String`, `core`'s UTF-8 text type: literals, joining and comparing, converting, and working with its bytes.

## Strings

```zane
package hello;

import core$;

Unit main() {
	console Console(@program$console);
	name String = String("Zane");
	greeting String = "Hello, " + name + "!";
	console!print(greeting);
	same Bool = name == "Zane";
	count String = String(name:byteCount());
	console!print("\%name has \%count bytes");
	console!print(String(42) + " and " + String(2.5));
	return Unit();
}
```

```output
Hello, Zane!
Zane has 4 bytes
42 and 2.5
```

| Verb | What it does |
|---|---|
| `a + b` | joins two strings; either may be a literal |
| `a == b`, `a ~= b` | compares the bytes |
| `String(v)` | the text of an `Int`, `Float`, `I32`, `F32`, `U8` or `Bool`; a `U8` is written as its number |
| `n:hex()` | the digits of an `Int`, `I32` or `U8` in base 16, lowercase: no leading zeros and a `-` before a negative number, except that a `U8` always has two digits |
| `s:byteCount()` | the length in bytes |
| `s:byteAt(i)` | the byte at position `i`, from 1, as a `U8`; a position outside the string stops the program |
| `s:parseInt()`, `s:parseFloat()` | the number written in the text, or an abort ([Numbers](numbers.md#reading-numbers-from-text)) |
| `String(bytes)` | a string of the bytes in a `List<U8>` |
| `s:hashBytes()` | a hash of the bytes, equal for equal strings within one run |

A literal passed as an argument becomes a `String`, and so does a literal
next to a `String` operand of `+` or `==`. In a literal, `\n`, `\t`, `\r`,
`\0` and `\\` are escapes, `\"` is a double quote, and `\%name` inserts the
value of the `String` symbol `name`.

## Bytes

A `String` is a sequence of bytes holding UTF-8. Positions count bytes from
1, so a character outside ASCII takes several positions:

```zane
package hello;

import core$;

Unit main() {
	console Console(@program$console);
	word String = String("héllo");
	console!print(String(word:byteCount()));
	console!print(String(word:byteAt(Int(1))) + " is " + word:byteAt(Int(2)):hex());

	bytes List<U8> = List(U8);
	i Int(1);
	i!to(word:byteCount()) {
		b U8 = word:byteAt(i);
		ascii Bool = if(b < 128) {
			bytes!push(b);
		}
	}
	console!print(String(bytes));
	return Unit();
}
```

```output
6
104 is c3
hllo
```

## Searching for bytes

A `ByteSet` is a set of bytes, made from a `List<Bool>` of 256 flags (byte
`b`'s flag at position `b + 1`) by `flags:byteSet()`. `s:findAny(from, count,
set)` searches the `count` positions starting at `from`, and returns the first
position whose byte is in `set`, or 0 when there is none.
`s:findPair(from, count, first, gap, second)` returns the first position whose
byte is in `first` and whose byte `gap` positions later is in `second`. Both
functions test many bytes at a time.

```zane
package hello;

import core$;

Unit main() {
	console Console(@program$console);
	flags List<Bool> = List(Bool);
	b Int(0);
	b!to(Int(255)) {
		flags!push(b == 44);
	}
	commas ByteSet = flags:byteSet();
	line String = String("name,age,city");
	first Int = line:findAny(Int(1), line:byteCount(), commas);
	console!print(String(first));
	return Unit();
}
```

```output
5
```

## Source

[`lib/core/primitives.zn`](https://github.com/zane-lang/std/blob/main/lib/core/primitives.zn)
