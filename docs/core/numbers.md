# Numbers

This page covers `core`'s number types, their operators, the conversions between them, and reading numbers from text.

## The types

| Type | What it is | Use it for |
|---|---|---|
| `Int` | a 64-bit signed integer | counts, indices, loops, general arithmetic |
| `Float` | a 64-bit floating-point number | general arithmetic with fractions |
| `I32` | a 32-bit signed integer | compact storage: a `List<I32>` takes 4 bytes per element |
| `F32` | a 32-bit floating-point number | compact storage of fractions |
| `U8` | an unsigned byte, 0 to 255 | bytes; it has comparisons but no arithmetic |

`Int` and `Float` are the defaults: an integer literal becomes an `Int`, and a
float literal a `Float`, unless the call it is passed to asks for another
number type. A parameter of type `I32` takes an integer literal as an `I32`,
and one of type `F32` a float literal as an `F32`.

## Operators

`Int`, `Float`, `I32` and `F32` each have `+`, `-`, `*`, `/`, `~` (negation),
`==`, `~=`, `<`, `>`, `<=` and `>=`. A literal may stand on either side of an
operator whose other operand is one of these types, as long as it is the
matching kind: an integer literal beside an `Int` or `I32`, a float literal
beside a `Float` or `F32`. An operator does not convert its operands, so
`Float(2.5) * 4` is an error; write `Float(2.5) * 4.0`:

```zane
package hello;

import core$;

Unit main() {
	console Console(@program$console);
	n Int(17);
	console!print(String(n + 1) + " " + String(n - 20) + " " + String(n * 2) + " " + String(n / 5));
	console!print(String(~n));
	x Float(2.5);
	console!print(String(x * 4.0) + " " + String(1.0 / x));
	small I32 = I32(7);
	console!print(String(small * 6));
	inRange Bool = 0 <= n and n < 100;
	equal Bool = n ~= 18;
	return Unit();
}
```

```output
18 -3 34 3
-17
10 0.4
42
```

Integer division rounds toward zero. `I32` arithmetic wraps around on
overflow: `I32(2147483647) + 1` is the smallest `I32`.

## Conversions

No number type converts to another on its own. The conversions are
constructors. Each one that drops part of the number has a name that says
how, except `Float(i)` from an `Int`, which rounds:

| Conversion | Result |
|---|---|
| `Float(i)` for an `I32` or `F32` | the same number as a `Float` |
| `Float(i)` for an `Int` | the nearest `Float`, which may differ from it beyond 2⁵³: `Float(Int(9007199254740993))` is `9007199254740992` |
| `Int(i)` for an `I32` or `U8` | the same number as an `Int` |
| `Int.truncate(f)` | an `Int`: the `Float` rounded toward zero, held to the `Int` range |
| `I32.wrap(i)` | the low 32 bits of an `Int` |
| `I32.truncate(f)` | an `I32`: the `Float` or `F32` rounded toward zero, held to the `I32` range |
| `F32.round(x)` | the nearest `F32` to a `Float`, `Int` or `I32` |
| `U8.wrap(i)` | the low 8 bits of an `Int` |

```zane
package hello;

import core$;

Unit main() {
	console Console(@program$console);
	f Float(7.9);
	console!print(String(Int.truncate(f)) + " " + String(Int.truncate(~f)));
	console!print(String(Float(Int(3)) / 2.0));
	console!print(String(I32.wrap(Int(4294967298))));
	console!print(String(Int(U8.wrap(Int(300)))));
	return Unit();
}
```

```output
7 -7
1.5
2
44
```

## Reading numbers from text

`text:parseInt()` reads an integer, written with digits and an optional `-`,
and `text:parseFloat()` an integer or a float. Both abort with `Unit` when the
text spells no number, or one too large for the type:

```zane
package hello;

import core$;

Unit main() {
	console Console(@program$console);
	a Int = String("42"):parseInt() ?? Int(0);
	b Int = String("-7"):parseInt() ?? Int(0);
	c Int = String("4x"):parseInt() ?? Int(~1);
	d Float = String("2.5"):parseFloat() ?? Float(0.0);
	console!print(String(a) + " " + String(b) + " " + String(c) + " " + String(d));
	return Unit();
}
```

```output
42 -7 -1 2.5
```

`text:parseFloat(start, count)` reads only the `count` bytes from byte
`start` (counted from 1), without copying them out of `text`.

The [`math`](../math.md) package adds square roots, powers, trigonometry,
rounding and bit operations.

## Source

[`lib/core/primitives.zn`](https://github.com/zane-lang/std/blob/main/lib/core/primitives.zn)
