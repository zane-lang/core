# core

The `core` package declares the types and control flow almost every Zane program uses, written in Zane over the compiler's intrinsics.

Import it with `import core$;`, which makes its names usable without a
prefix.

1. [Numbers](numbers.md): `Int`, `Float`, `I32`, `F32`, `U8`, their operators and conversions
2. [Text](text.md): `String` and its bytes
3. [Containers](containers.md): `List`, `Array`, `ListRef`, `ArrayRef`
4. [Control flow](control-flow.md): `if`, `elif`, `else`, `guard`, `do`, `to`, workers and `Duration`
5. [Console and runtime](console.md): `Console`, `Runtime`, `Unit` and `Bool`
