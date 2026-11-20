# Worker pools

This page covers `WorkerPool` and `EventSource`, which run many workers at once, each with an element of its own.

A worker pool runs bulk work, such as one worker for each network connection.
Each worker is an **element**, which the pool owns, and a **step**, a lambda
the pool calls on the element again and again until it returns `false`. The
steps of different elements run at the same time, on the thread pool, beside
the code that started them. The steps of one element never run at the same
time.

The workers of a pool may share a **state**. Only the pool's **funnel** writes
the state: a step publishes an event, and the funnel applies the events one at
a time, each worker's in the order that worker published them.

```zane
package hello;

import core$;

type Counter = struct {
	n Int;
	limit Int;
}
Counter(limit Int) => init{ n = Int(0); limit; }

type Total = struct {
	sum Int;
	events Int;
}
Total() => init{ sum = Int(0); events = Int(0); }

Unit main() {
	do() {
		pool WorkerPool<Counter, Total, Int> = WorkerPool(Counter, Total(), Unit(this Total, n Int) mut {
			this.sum = this.sum + n;
			this.events = this.events + 1;
			if(this.events == 6) {
				console Console(@program$console);
				console!print("sum " + String(this.sum));
			}
			return Unit();
		});
		count Bool[this Counter, Total, Unit[Int]] mut = Bool(this Counter, total Total, publish Unit[Int]) mut {
			this.n = this.n + 1;
			publish(this.n);
			return this.n < this.limit;
		}
		pool!start(Counter(3), count);
		pool!start(Counter(3), count);
	}
	console Console(@program$console);
	console!print("both workers finished");
	return Unit();
}
```

```output
sum 12
both workers finished
```

| Verb | What it does |
|---|---|
| `WorkerPool(T, state, funnel)` | a pool of elements of type `T`, whose workers share `state`, which `funnel` writes |
| `WorkerPool(T)` | a pool of elements of type `T`, whose workers share nothing |
| `pool!start(element, step)` | adds a worker: `element` moves into the pool, or is copied in when it is a value, and `step` runs on it until it returns `false` |
| `pool!start(element, sources, step)` | adds a worker whose step runs again only when one of `sources` is ready, or when the funnel has changed the state |
| `pool:state()` | a copy of the shared state |
| `pool:elements()` | a `List` of a copy of each element, in the order they started |
| `EventSource.every(interval)` | a timer, ready each time the `Duration` `interval` has passed since it was last ready |

## Steps

`start` returns at once, and the step's first call follows it. A pool with a
state calls its step with three values: the element as `this`, a copy of the
state taken when the call begins, and a function that publishes an event. A
pool without a state calls its step with the element alone.

A worker started without event sources has its step called again as soon as
the step returns `true`. A worker started with event sources waits between
calls without holding a thread, until one of its sources is ready or the
funnel has changed the state. A timer whose interval is below one nanosecond
is always ready.

A step is meant never to wait: it reads only values that already exist, and
then it returns. A step that does wait, for example on a slow call into C,
keeps its thread while it waits.

## Elements and the state

The state and the events are values. An element is a value, or an owner whose
every `&` names a package constant or a capability. Through an `&` to a
capability, such as a `Console`'s, a step can print or reach the outside world.
Through an `&` to a package constant, the steps of many elements read one
table. The compiler follows each `&` to the place it was taken from, so an
element built in a verb from an `&` parameter is accepted where each call of
that verb passes a package constant. When a step returns `false`, its element
is destroyed. `elements` copies each element, so it reads only a pool
whose elements are values.

## Where a pool ends

The scope that holds a pool ends only once every element's step has returned
`false` and the funnel has applied every event, as a scope waits for the calls
it spawned. In the example, `both workers finished` prints after the pool's
`do` block, so it prints after the funnel's last line.

The spec gives [the rules](https://github.com/zane-lang/spec/blob/main/spec/concurrency.md#6-worker-pools).

## Source

[`lib/core/workers.zn`](https://github.com/zane-lang/std/blob/main/lib/core/workers.zn)
