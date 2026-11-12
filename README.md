# core

The basic types and control flow of the [Zane](https://github.com/zane-lang/zane)
programming language, written in Zane.

The language itself provides only machine-level building blocks (the
`@primitives$`, `@operators$` and `@controlflow$` intrinsics). Everything you
normally write with, such as `Int`, `String`, `List`, `if` and loops, is
declared here, in ordinary Zane source you can read.

This repository holds two library packages:

- **`core`** ([`lib/core/`](lib/core/)): the types and verbs almost every
  program uses.
- **`math`** ([`lib/math/`](lib/math/)): math functions over `core`'s `Int`
  and `Float`, and over the narrow `I32` and `F32`.

## Using it

Add it to a project with the [`zane`](https://github.com/zane-lang/zane)
command. `core` publishes no prebuilt objects, so it is compiled from source:

```sh
zane add https://github.com/zane-lang/core --from-source
```

Then import it. `import core$;` makes its names usable directly; `import math;`
keeps the `math$` prefix:

```zane
package hello;

import core$;
import math;

Unit main() {
	console Console(@program$console);
	root Float = math$sqrt(Float(2.0));
	big Bool = if(Float(1.4) < root) {
		console!print("sqrt(2) is more than 1.4");
	}
	return Unit();
}
```

## What is in it

| File | What it declares |
|---|---|
| [`primitives.zn`](lib/core/primitives.zn) | `Unit`, `Bool`, `Int`, `Float`, `String`, and the narrow scalars `I32` and `F32` (compact storage; `Int` and `Float` stay the defaults), with their operators and conversions |
| [`controlflow.zn`](lib/core/controlflow.zn) | `if`, `elif`, `else`, `guard`, `do`, and the counting loop `to` |
| [`containers.zn`](lib/core/containers.zn) | `Array` and `List` (values), `ArrayRef` and `ListRef` (for owners that must stay in place) |
| [`console.zn`](lib/core/console.zn) | `Console`, which prints |
| [`runtime.zn`](lib/core/runtime.zn) | `Runtime`: the program's command-line `arguments` and its thread count |
| [`math.zn`](lib/math/math.zn) | `sqrt`, `pow`, `sin` and the other trigonometric functions, `floor`/`ceil`/`trunc`, `min`/`max`, bit operations on `Int`, each also over `I32` and `F32` |

A program is handed its console and runtime as `@program$console` and
`@program$runtime`, and wraps them in `Console` and `Runtime`. Code it does not
pass them to cannot print or read the arguments.

The rules these follow are in the [specification](https://github.com/zane-lang/spec):
[`control-flow.md`](https://github.com/zane-lang/spec/blob/main/spec/control-flow.md)
for the control flow, [`generics.md`](https://github.com/zane-lang/spec/blob/main/spec/generics.md)
for the containers, [`math.md`](https://github.com/zane-lang/spec/blob/main/spec/math.md)
for `math`, and [`effects.md`](https://github.com/zane-lang/spec/blob/main/spec/effects.md)
for the console and runtime.

## Testing

Each package has a test package in [`test/`](test/) that imports it the way a
user does and prints `yes` for every check that holds. They are also the
largest collection of working Zane code, and a good place to see how each
verb is used.

```sh
zane test
```

A check that fails prints `no` and the run carries on, so `zane test` still
reports the package as passed: read the output for any `no`.

`zane test` uses the compiler `core` pins. When no release archive of that
version exists for your platform, point `ZANE_COMPILER` at a newer `zanec`.

`zane.coda` pins the compiler version `core` is built with, and
`zane-lock.coda` its exact commit. A change that needs a newer compiler moves
both together, to a compiler that has a release tag.

## License

`core` is under the MIT No Attribution license (MIT-0); see
[`LICENSE`](LICENSE). Its code is compiled into every Zane program, and
MIT-0 asks nothing of those programs, not even a copyright notice.
