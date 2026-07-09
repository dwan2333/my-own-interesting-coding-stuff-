# The Itertools Module

_Research compiled 2026-07-08 — Python standard library `itertools`_

> Part of the [Python Reference](<../Python Reference (Main).md>). **`itertools`** is a built-in module of fast, memory-light tools for working with **iterables** — combining them, slicing them, accumulating over them, and generating combinations. Everything it returns is a **lazy iterator** (like [generators](<../Core Language/Generators and Yield.md>), [`zip`](<../Data Structures/The Zip Function.md>), [`map`](<../Data Structures/Map and Filter.md>)), so wrap results in `list()` to see them.

```python
import itertools as it   # common alias
```

---

## Branch 1 — Infinite Iterators (bound them with `islice`)

These produce values **forever** — so you pair them with `islice` (Branch 2) or `break` to stop.

| Function | Produces |
|---|---|
| `count(start, step)` | `start, start+step, …` forever |
| `cycle(iterable)` | loops the iterable endlessly |
| `repeat(value, times)` | `value` repeated (forever, or `times` times) |

```python
import itertools as it

print(list(it.islice(it.count(10, 2), 4)))    # [10, 12, 14, 16]  — from 10, step 2, take 4
print(list(it.islice(it.cycle('AB'), 5)))     # ['A', 'B', 'A', 'B', 'A']
print(list(it.repeat(9, 3)))                  # [9, 9, 9]
```

> [!warning] `count` and `cycle` never stop on their own
> `list(it.count(1))` would run forever and hang. Always bound an infinite iterator with `islice(..., n)` or a `break` in your loop.

---

## Branch 2 — Combining & Slicing Iterables

| Function | What it does |
|---|---|
| `chain(a, b, …)` | glue several iterables into one long stream |
| `islice(iterable, stop)` / `islice(it, start, stop, step)` | slice an iterator (you can't use `[ : ]` on a generator) |
| `zip_longest(a, b, fillvalue=…)` | like `zip`, but pads the short one instead of truncating |

```python
import itertools as it

print(list(it.chain([1, 2], [3, 4], [5])))          # [1, 2, 3, 4, 5]
print(list(it.islice(range(100), 2, 8, 2)))         # [2, 4, 6]
print(list(it.zip_longest([1, 2, 3], ['a', 'b'], fillvalue='-')))
# [(1, 'a'), (2, 'b'), (3, '-')]      — 3 keeps its partner as '-'
```

> [!tip] `zip_longest` fixes `zip`'s truncation
> Plain [`zip`](<../Data Structures/The Zip Function.md>) stops at the shortest iterable and silently drops the rest. When you need to keep **all** items and pad the gaps, use `it.zip_longest(..., fillvalue=...)`.

---

## Branch 3 — Accumulating & Grouping

| Function | What it does |
|---|---|
| `accumulate(iterable)` | running totals (a cumulative sum by default) |
| `groupby(iterable, key)` | group **consecutive** items sharing a key |

```python
import itertools as it

print(list(it.accumulate([1, 2, 3, 4])))      # [1, 3, 6, 10]  — running sum

data = [('a', 1), ('a', 2), ('b', 3)]
grouped = {k: [v for _, v in g] for k, g in it.groupby(data, key=lambda x: x[0])}
print(grouped)                                # {'a': [1, 2], 'b': [3]}
```

> [!warning] `groupby` only groups **adjacent** items
> It starts a new group whenever the key changes, so items with the same key must already be **next to each other**. If they're scattered, **`sorted(...)` by the same key first**, then `groupby`.

`accumulate` also takes a function — e.g. a running maximum or product:

```python
import itertools as it
print(list(it.accumulate([3, 1, 4, 1, 5], max)))   # [3, 3, 4, 4, 5]  — running max
```

---

## Branch 4 — Combinatorics (the most-loved part)

Generate combinations and orderings without hand-written nested loops.

| Function | Gives you | Order matters? | Repeats? |
|---|---|---|---|
| `product(a, b)` | every pairing across iterables (like nested loops) | — | — |
| `permutations(it, r)` | all **ordered** arrangements of length `r` | **Yes** | no |
| `combinations(it, r)` | all **unordered** selections of length `r` | No | no |

```python
import itertools as it

print(list(it.product([1, 2], ['a', 'b'])))
# [(1, 'a'), (1, 'b'), (2, 'a'), (2, 'b')]

print(list(it.permutations([1, 2, 3], 2)))
# [(1, 2), (1, 3), (2, 1), (2, 3), (3, 1), (3, 2)]   — (1,2) and (2,1) both appear

print(list(it.combinations([1, 2, 3], 2)))
# [(1, 2), (1, 3), (2, 3)]                           — order ignored, no (2,1)
```

The difference in one line: **permutations** count `(1,2)` and `(2,1)` as different; **combinations** treat them as the same.

---

## Key Takeaways

- **`import itertools as it`** — a toolbox of **lazy** iterator helpers; wrap results in `list()` to view.
- **Infinite:** `count`, `cycle`, `repeat` — always bound them with `islice` or `break`.
- **Combine/slice:** `chain` (join streams), `islice` (slice an iterator), `zip_longest` (pad instead of truncate).
- **Aggregate:** `accumulate` (running totals / custom running op), `groupby` (group **adjacent** equal-key items — `sorted` first if scattered).
- **Combinatorics:** `product` (nested-loop pairings), `permutations` (ordered), `combinations` (unordered).

---

## Exercises

> [!example] Exercise 1 — All 2-item combinations
> **Problem.** Use `itertools` to list every 2-item combination (order doesn't matter) of `['red', 'green', 'blue']`.
>
> > [!success]- Click to reveal solution
> > **Solution.** `combinations(iterable, 2)` gives unordered pairs.
> > ```python
> > import itertools as it
> > print(list(it.combinations(['red', 'green', 'blue'], 2)))
> > ```
> > **Answer.** `[('red', 'green'), ('red', 'blue'), ('green', 'blue')]` ✓

> [!example] Exercise 2 — Running total
> **Problem.** Given daily earnings `[10, 5, 20, 5]`, produce the running (cumulative) total after each day.
>
> > [!success]- Click to reveal solution
> > **Solution.** `accumulate` produces a running sum by default.
> > ```python
> > import itertools as it
> > print(list(it.accumulate([10, 5, 20, 5])))
> > ```
> > **Answer.** `[10, 15, 35, 40]` ✓

---

### Sources

| Source | Date | Type |
|---|---|---|
| Python `itertools` — official documentation | 2026 | Standard library reference |
| Verified against Python 3.14 on `E:\Python` | 2026-07-08 | Local test |
