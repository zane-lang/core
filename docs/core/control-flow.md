# Control flow

This page covers `core`'s branching, loops and workers, which are ordinary functions that take a block.

| Verb | What it does |
|---|---|
| `if(condition) { … }` | runs the block when `condition` holds, and returns a `Bool` that records whether the block ran |
| `chain!elif(condition) { … }` | on the `Bool` an `if` returned: runs the block when no earlier branch ran and `condition` holds |
| `chain:else() { … }` | runs the block when no branch of the chain ran |
| `guard(condition)` | ends the block it is called in when `condition` holds |
| `do() { … }` | runs the block once |
| `i!to(end) { … }` | runs the block for each value of `i` up to `end`, advancing `i` |
| `s!work(step)` | calls `step` on `s` until `step` returns `false` |
| `s!register(source, step)` | works like `work`, and calls `step` again only once the `EventSource` `source` is ready |
| `s!setInterval(every, step)` | `register` on a timer: calls `step` each time the `Duration` `every` has passed since the timer was last ready |

```zane
package hello;

import core$;

type Countdown = struct {
	left Int;
}
Countdown(left Int) => init{ left; }

Unit main() {
	console Console(@program$console);
	n Int(15);
	fizz Bool = if(n / 15 * 15 == n) {
		console!print("FizzBuzz");
	}
	fizz!elif(n / 3 * 3 == n) {
		console!print("Fizz");
	}
	fizz:else() {
		console!print(String(n));
	}

	i Int(1);
	i!to(Int(4)) {
		guard(i == 2);
		console!print("pass " + String(i));
	}

	c Countdown(Int(3));
	c!setInterval(Duration.milliseconds(1), Bool(this Countdown) mut {
		this.left = this.left - 1;
		return 0 < this.left;
	});
	console!print("countdown at " + String(c.left));
	return Unit();
}
```

```output
FizzBuzz
pass 1
pass 3
pass 4
countdown at 0
```

A step is a lambda that takes the subject as `this` and is `mut`, so it can
change the subject. `work`, `register` and `setInterval` take no block, so
they may be started with `spawn` to run in the background.

`register` waits for its event source between steps. The wait holds back
only that worker: every spawned call and every worker pool's worker keeps
running meanwhile. `EventSource.every(interval)` makes a timer, which is
ready each time `interval` has passed since it was last ready; a step
slower than the interval runs again once, not once for each tick it
missed. [Worker pools](workers.md) take the same event sources. To run many workers at once, each on an element of
its own, use a [worker pool](workers.md).

## `Duration`

A `Duration` is a span of time, a whole number of nanoseconds:
`Duration.seconds(n)`, `Duration.milliseconds(n)` and `Duration.nanoseconds(n)`
make a `Duration`, and `d:nanoseconds()` returns its length in nanoseconds.

The Learn pages explain [how these verbs work](https://github.com/zane-lang/docs/blob/main/docs/tour/control-flow.md),
and the spec gives [the rules](https://github.com/zane-lang/spec/blob/main/spec/control-flow.md#3-branching-and-repetition).

## Source

[`lib/core/controlflow.zn`](https://github.com/zane-lang/std/blob/main/lib/core/controlflow.zn)
