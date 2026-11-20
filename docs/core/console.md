# Console and runtime

This page covers `Console`, which prints, and `Runtime`, which provides the program's arguments and sets the size of its thread pool.

Both wrap a capability the program receives from the language:
`@program$console` and `@program$runtime`. Only the program's own package can
name these, so other code prints or reads arguments only when it is given a
`Console` or `Runtime`.

```zane
package hello;

import core$;

Unit main() {
	console Console(@program$console);
	runtime Runtime(@program$runtime);
	console!print("Hello");
	args List<String> = runtime:arguments();
	console!print(String(args:size()) + " arguments");
	runtime!setThreads(Int(4)) ? e {
		console!print("could not resize the thread pool");
		resolve Unit();
	}
	return Unit();
}
```

```output
Hello
0 arguments
```

| Verb | What it does |
|---|---|
| `Console(@program$console)` | the program's console |
| `console!print(text)` | writes `text` and a newline to standard output |
| `Runtime(@program$runtime)` | the program's runtime |
| `runtime:arguments()` | the command-line arguments, without the program's name, as a `List<String>` |
| `runtime!setThreads(count)` | sets the thread pool's size to `count` threads; aborts with `Unit` when `count` is below one |
| `runtime!setThreadsAuto()` | sets the thread pool's size to the number of threads the hardware runs at once |

## `Unit` and `Bool`

`Unit` is the type with one value, `Unit()`, returned by functions that have
nothing else to return. A `Bool` is `true` or `false`, made with `Bool(true)`
or `Bool(false)`, and has the operators `and`, `or`, `~` (not), `==` and `~=`.
`String(b)` returns the text `"true"` or `"false"`:

```zane
package hello;

import core$;

Unit main() {
	console Console(@program$console);
	small Bool = Int(1) < Int(2);
	console!print("1 < 2 is " + String(small) + ", and its opposite " + String(~small));
	return Unit();
}
```

```output
1 < 2 is true, and its opposite false
```

## Source

[`lib/core/console.zn`](https://github.com/zane-lang/std/blob/main/lib/core/console.zn),
[`lib/core/runtime.zn`](https://github.com/zane-lang/std/blob/main/lib/core/runtime.zn)
and [`lib/core/primitives.zn`](https://github.com/zane-lang/std/blob/main/lib/core/primitives.zn)
