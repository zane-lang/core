# math

This page covers the `math` package: square roots, powers, trigonometry, rounding, and bit operations over `core`'s numbers.

`math` declares functions, not methods, so they are called as
`math$sqrt(x)` after `import math;`, or as `sqrt(x)` after `import math$;`.

```zane
package hello;

import core$;
import math;

Unit main() {
	console Console(@program$console);
	console!print(String(math$sqrt(Float(2.0))));
	console!print(String(math$pow(Float(2.0), Float(10.0))));
	console!print(String(math$hypot(Float(3.0), Float(4.0))));
	console!print(String(math$floor(Float(2.7))) + " " + String(math$ceil(Float(2.1))));
	console!print(String(math$abs(~Int(5))) + " " + String(math$max(Int(3), Int(9))));
	console!print(String(math$bitAnd(Int(12), Int(10))) + " " + String(math$shiftLeft(Int(1), Int(8))));
	console!print(String(math$popCount(Int(255))));
	return Unit();
}
```

```output
1.4142135623730951
1024
5
2 3
5 9
8 256
8
```

## `Float` and `F32`

These are exact: correctly rounded, and the same on every system, and at
compile time as at run time.

| Function | Result |
|---|---|
| `sqrt(x)` | the square root; NaN below zero |
| `abs(x)` | the magnitude |
| `floor(x)`, `ceil(x)` | rounded down, up |
| `trunc(x)` | rounded toward zero |
| `roundEven(x)` | rounded to the nearest integer, a tie going to the even one |
| `fma(a, b, c)` | `a * b + c`, rounded once |
| `copySign(magnitude, sign)` | `magnitude` with the sign of `sign` |
| `min(a, b)`, `max(a, b)` | the lesser, the greater; NaN when either is NaN |

These are approximate, computed by the platform's C math library, so the last
bits may differ between systems:

| Function | Result |
|---|---|
| `cbrt(x)` | the cube root |
| `sin(x)`, `cos(x)`, `tan(x)` | of an angle in radians |
| `asin(x)`, `acos(x)`, `atan(x)` | in radians |
| `atan2(y, x)` | the angle of the point (x, y), from -π to π |
| `exp(x)`, `log(x)` | e to the power `x`; the natural logarithm |
| `pow(base, exponent)` | `base` to the power `exponent` |
| `hypot(x, y)` | `sqrt(x * x + y * y)`, without overflow or underflow in between |

## `Int` and `I32`

| Function | Result |
|---|---|
| `abs(x)` | the magnitude; the most negative value gives itself back |
| `min(a, b)`, `max(a, b)` | the lesser, the greater |
| `bitAnd(a, b)`, `bitOr(a, b)`, `bitXor(a, b)` | each bit set in both, in either, in exactly one |
| `bitNot(x)` | every bit flipped |
| `shiftLeft(x, n)` | the bits moved `n` places up, zeros filling in |
| `shiftRight(x, n)` | moved down, copies of the sign bit filling in |
| `shiftRightLogical(x, n)` | moved down, zeros filling in |
| `rotateLeft(x, n)`, `rotateRight(x, n)` | moved, the bits shifted out filling in at the other end |
| `popCount(x)` | the number of set bits |
| `leadingZeros(x)`, `trailingZeros(x)` | the zero bits above the highest set bit, below the lowest; the width for zero |

Shift and rotate counts are taken modulo the width, 64 for `Int` and 32 for
`I32`.

## In the spec

[Math](https://github.com/zane-lang/spec/blob/main/spec/math.md): the
`@math$` intrinsics, and which functions are exact.

## Source

[`lib/math/math.zn`](https://github.com/zane-lang/std/blob/main/lib/math/math.zn)
