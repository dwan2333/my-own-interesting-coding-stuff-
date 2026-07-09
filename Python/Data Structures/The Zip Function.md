# The Zip Function

_Research compiled 2026-07-08 — Python built-in `zip()`_

> Companion to [The Enumerate Function](<The Enumerate Function.md>) and [Sorting](<Sorting.md>). **`zip()`** pairs up items from **two or more iterables** position by position — so you can loop over several lists *together* instead of juggling indexes. Think of a zipper joining two rows of teeth into one.

---

## Branch 1 — What `zip()` Does

It takes several iterables and yields **tuples**, one item from each, matched by position: the 1st items together, the 2nd items together, and so on.

```python
names = ['Ann', 'Bo', 'Cy']
ages  = [30, 25, 40]

print(list(zip(names, ages)))
# [('Ann', 30), ('Bo', 25), ('Cy', 40)]
```

---

## Branch 2 — The Main Use: Loop Over Two Lists Together

This is the everyday reason to reach for `zip()` — walk two (or more) related lists in lockstep, unpacking each pair as you go.

```python
names = ['Ann', 'Bo', 'Cy']
ages  = [30, 25, 40]

for name, age in zip(names, ages):
    print(f'{name} is {age}')
# Ann is 30
# Bo is 25
# Cy is 40
```

It replaces the clumsy index-based version:

```python
# the long way zip() saves you from:
for i in range(len(names)):
    print(f'{names[i]} is {ages[i]}')
```

More than two works the same way:

```python
for a, b, c in zip([1, 2], ['a', 'b'], [True, False]):
    print(a, b, c)
# 1 a True
# 2 b False
```

---

## Branch 3 — It Stops at the Shortest

`zip()` quits as soon as the **shortest** iterable runs out — extra items in the longer ones are **silently dropped**.

```python
print(list(zip([1, 2, 3], ['a', 'b'])))
# [(1, 'a'), (2, 'b')]        — the 3 is dropped (no partner)
```

> [!warning] Mismatched lengths lose data quietly
> If your lists should be the same length, `zip()` won't warn you when they aren't — it just truncates. If you need *all* items (padding the short one), use `itertools.zip_longest()` instead.

---

## Branch 4 — It's a Lazy Iterator

Like [`enumerate()`](<The Enumerate Function.md>), `zip()` returns a **lazy iterator**, not a list — it produces pairs on demand (memory-friendly). Wrap it in `list()` (or `dict()`) to materialize them.

```python
names = ['Ann', 'Bo']
ages  = [30, 25]
print(zip(names, ages))         # <zip object at 0x...>
print(list(zip(names, ages)))   # [('Ann', 30), ('Bo', 25)]
```

> [!note] A zip object is single-use
> Once you loop through it (or call `list()` on it) it's exhausted — looping again yields nothing. Rebuild the `zip()` if you need it twice.

---

## Branch 5 — Two Handy Patterns

### Build a dict from two lists

Pair keys with values, then hand the pairs to `dict()`:

```python
names = ['Ann', 'Bo', 'Cy']
ages  = [30, 25, 40]
print(dict(zip(names, ages)))
# {'Ann': 30, 'Bo': 25, 'Cy': 40}
```

### "Unzip" — split pairs back apart with `zip(*...)`

Putting `*` in front unpacks the list of pairs *into* `zip`, which regroups them — turning rows back into columns.

```python
pairs = [('Ann', 30), ('Bo', 25), ('Cy', 40)]
names, ages = zip(*pairs)
print(names)    # ('Ann', 'Bo', 'Cy')
print(ages)     # (30, 25, 40)
```

(The `*` here is the unpacking operator — see [Star Parameters](<../Core Language/Star Parameters - args and kwargs.md>).)

---

## Key Takeaways

- **`zip(a, b, …)`** pairs items from several iterables by position, yielding **tuples** — the clean way to loop over related lists **together** (`for x, y in zip(a, b)`).
- It **stops at the shortest** iterable and silently drops the rest — use `itertools.zip_longest()` if you need to keep everything.
- It returns a **lazy, single-use iterator** (like `enumerate`); wrap in `list()` or `dict()` to materialize.
- **`dict(zip(keys, values))`** builds a dictionary from two lists; **`zip(*pairs)`** "unzips" pairs back into separate sequences.

---

## Exercises

> [!example] Exercise 1 — Pair and print two lists
> **Problem.** Given `fruits = ['apple', 'pear']` and `prices = [1.2, 0.8]`, print each as `apple: $1.2` and `pear: $0.8` using `zip()`.
>
> > [!success]- Click to reveal solution
> > **Solution.** Loop the two lists together and unpack each pair.
> > ```python
> > fruits = ['apple', 'pear']
> > prices = [1.2, 0.8]
> > for fruit, price in zip(fruits, prices):
> >     print(f'{fruit}: ${price}')
> > ```
> > **Answer.** `apple: $1.2` / `pear: $0.8` ✓

> [!example] Exercise 2 — Build a dict from two lists
> **Problem.** Turn `keys = ['a', 'b', 'c']` and `vals = [1, 2, 3]` into the dict `{'a': 1, 'b': 2, 'c': 3}` in one line.
>
> > [!success]- Click to reveal solution
> > **Solution.** `zip` the two lists, then feed the pairs to `dict()`.
> > ```python
> > keys = ['a', 'b', 'c']
> > vals = [1, 2, 3]
> > print(dict(zip(keys, vals)))
> > ```
> > **Answer.** `{'a': 1, 'b': 2, 'c': 3}` ✓

---

### Sources

| Source | Date | Type |
|---|---|---|
| Python `zip` — official built-in functions documentation | 2026 | Standard library reference |
| Verified against Python 3.14 on `E:\Python` | 2026-07-08 | Local test |
