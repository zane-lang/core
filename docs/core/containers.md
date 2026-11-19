# Containers

This page covers `core`'s four containers: `List`, `Array`, `ListRef` and `ArrayRef`.

| Type | Size | Holds | Copied with the container |
|---|---|---|---|
| `List<T>` | grows and shrinks | values | yes: a `List` is a value |
| `Array<T, n>` | fixed at `n` | values | yes |
| `ListRef<T>` | grows and shrinks | owners of a reference type `T`, moved in and out | no: it is a reference type |
| `ArrayRef<T, n>` | fixed at `n` | elements that stay in place | no: it is a reference type |

Positions count from 1, so a container of `n` elements has positions `1` to
`n`. Reading or writing a position outside that range stops the program with
`index out of range`.

## `List`

```zane
package hello;

import core$;

Unit main() {
	console Console(@program$console);
	squares List<Int> = List(Int);
	i Int(1);
	i!to(Int(5)) {
		squares!push(i * i);
	}
	console!print(String(squares:size()) + " " + String(squares[Int(5)]));
	squares[Int(1)] = Int(100);

	gone Int = squares!remove(Int(2));
	console!print(String(gone) + " " + String(squares[Int(2)]));

	zeros List<Int> = List(Int(3), Int(0));
	copy List<Int> = zeros;
	copy!push(Int(7));
	console!print(String(zeros:size()) + " " + String(copy:size()));
	return Unit();
}
```

```output
5 25
4 9
3 4
```

| Verb | What it does |
|---|---|
| `List(T)` | an empty list of `T` |
| `List(n, value)` | `n` copies of `value`, made in one block |
| `l:size()` | the number of elements |
| `l[i]` | the element at `i`, which may be assigned |
| `l!push(value)` | adds `value` at the end |
| `l!remove(i)` | takes out the element at `i` and returns it, shifting the later ones down |
| `l!swapRemove(i)` | takes out the element at `i` and moves the last one into its place: faster, but the order changes |
| `l!appendRange(from, start, count)` | copies `count` elements of `from`, from `start`, onto the end |
| `l!appendOwn(start, count)` | the same, from the list itself |
| `l!copyRange(at, from, start, count)` | copies `count` elements of `from`, from `start`, over the list's own from `at` |
| `l!sort()` | sorts the elements in place, ascending, for lists of `Int`, `I32` or `U8` |
| `l:sameRange(start, other, otherStart, count)` | whether two ranges hold the same elements, for lists of integers |
| `l:hashRange(start, count)` | a hash of a range, for lists of integers |

`appendRange`, `appendOwn` and `copyRange` are for elements that own no
memory of their own, such as numbers. `l!sortBy(keys)` sorts a `List<I32>`
of positions by the keys they name; its source marks it as an experiment.

A `List` is a value, so copying one copies its elements, and a value type
may hold one as a field.

## `Array`

An `Array` has a length that is part of its type, and is made from a literal
in `[ ]`:

```zane
package hello;

import core$;

Unit main() {
	console Console(@program$console);
	days Array<String, 3> = Array([String("Mon"), String("Tue"), String("Wed")]);
	days[Int(3)] = String("Thu");
	i Int(1);
	i!to(days:size()) {
		console!print(days[i]);
	}
	return Unit();
}
```

```output
Mon
Tue
Thu
```

## `ListRef`

Owners of a reference type (a `#struct`) go in a `ListRef`. It moves its
elements as it grows, so nothing may refer to them: they are moved in, and
`remove` and `swapRemove` move one out, as a `^T`.

```zane
package hello;

import core$;

type Jar = #struct {
	beans Int;
}
Jar(beans Int) => init{ beans; }

Unit main() {
	console Console(@program$console);
	jars ListRef<Jar> = ListRef(Jar);
	jars!push(Jar(Int(1)));
	jars!push(Jar(Int(2)));
	jars[Int(2)].beans = Int(20);
	taken ^Jar = jars!remove(Int(1));
	console!print(String(taken.beans) + " " + String(jars[Int(1)].beans));
	return Unit();
}
```

```output
1 20
```

## `ArrayRef`

An `ArrayRef` is a fixed-size container that is itself a reference type: it
has one owner, is never copied, and its elements stay where they are.
`ArrayRef(values)` builds one from an array literal, borrowing and copying
each element, so its elements are values such as numbers:

```zane
package hello;

import core$;

Unit main() {
	console Console(@program$console);
	cells ArrayRef<Int, 3> = ArrayRef([Int(4), Int(5), Int(6)]);
	cells[Int(3)] = Int(60);
	console!print(String(cells[Int(1)] + cells[Int(3)]) + " in " + String(cells:size()) + " cells");
	return Unit();
}
```

```output
64 in 3 cells
```

`ArrayRef.roaming(values)` takes each element instead, so an owner of a
reference type moves in, and a value is copied. Its elements stay where they
are, so they are changed in place:

```zane
package hello;

import core$;

type Jar = #struct {
	beans Int;
}
Jar(beans Int) => init{ beans; }

Unit main() {
	console Console(@program$console);
	spare ^Jar = Jar(Int(2));
	jars ArrayRef<Jar, 2> = ArrayRef.roaming([Jar(Int(1)), spare]);
	jars[Int(2)].beans = jars[Int(2)].beans * 10;
	console!print(String(jars[Int(1)].beans) + " " + String(jars[Int(2)].beans));
	return Unit();
}
```

```output
1 20
```

## Source

[`lib/core/containers.zn`](https://github.com/zane-lang/std/blob/main/lib/core/containers.zn)
