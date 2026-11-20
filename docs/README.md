# Library

These pages document `std`, Zane's standard library: the `core`, `math` and `regex` packages.

The language itself provides only machine-level building blocks, the
compiler's intrinsics. `Int`, `String`, `List`, `if`, loops and printing are
declared in `std`, in ordinary Zane source you can read.

1. [core](core/README.md): numbers, text, containers, control flow, the console, worker pools
2. [math](math.md): square roots, powers, trigonometry, rounding, bit operations
3. [regex](regex.md): regular expressions with groups, searched in linear time

## Using it

Add it to a project; `std` publishes no prebuilt objects, so it is compiled
from source:

```sh
zane add https://github.com/zane-lang/std --from-source
```

Then import its packages in each file that uses them:

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

```output
sqrt(2) is more than 1.4
```

These pages describe `std` v0.15, which pins compiler v0.39; their examples
are checked with compiler v0.40, which builds it too. To learn the
language itself, start with the
[Learn pages](https://github.com/zane-lang/docs/blob/main/docs/README.md).
