# The map() and filter() Functions

_Research compiled 2026-07-08 — Python built-ins `map()` and `filter()`_

> Companion to [The Zip Function](<The Zip Function.md>) and [Sorting](<Sorting.md>). **`map()`** transforms every item in an iterable; **`filter()`** keeps only the items that pass a test. Together they're the "apply a function across a whole collection" pair — a loop-free way to reshape data.

---

## Branch 1 — `map()` — transform every item

`map(function, iterable)` runs `function` on each item and yields the results.

```python
nums = [1, 2, 3, 4]
print(list(map(str, nums)))            # ['1', '2', '3', '4']  — str() on each
print(list(map(lambda x: x * x, nums)))# [1, 4, 9, 16]         — square each
```

Read `map(f, items)` as *"give me `f(item)` for every item."* The function can be a built-in (`str`, `int`, `abs`), a named function, or a `lambda`.

### The most common use — text → numbers

```python
lines = ['10', '20', '30']
print(list(map(int, lines)))           # [10, 20, 30]
```

### Multiple iterables

Pass more than one iterable and the function takes **one item from each**, in parallel (it stops at the shortest, like [`zip`](<The Zip Function.md>)):

```python
print(list(map(lambda a, b: a + b, [1, 2, 3], [10, 20, 30])))
# [11, 22, 33]
```

---

## Branch 2 — `filter()` — keep only what passes a test

`filter(function, iterable)` keeps each item for which `function(item)` is **truthy**, dropping the rest.

```python
nums = [1, 2, 3, 4, 5, 6]
print(list(filter(lambda x: x % 2 == 0, nums)))   # [2, 4, 6]  — keep the evens
print(list(filter(str.isalpha, ['ab', 'a1', 'cd']))) # ['ab', 'cd']  — keep pure-letter strings
```

> [!tip] `filter(None, ...)` drops falsy items
> Passing `None` as the function keeps only the **truthy** items — a quick way to strip out `0`, `''`, `None`, `[]`, etc.
> ```python
> print(list(filter(None, [0, 1, '', 'hi', [], [1]])))   # [1, 'hi', [1]]
> ```

---

## Branch 3 — Both Are Lazy Iterators

Like `zip` and `enumerate`, `map()` and `filter()` return **lazy, single-use iterators** — not lists. Wrap in `list()` to see the values, or feed them straight into `sum()`, `sorted()`, a `for` loop, etc.

```python
print(map(str, [1, 2]))                 # <map object at 0x...>
print(sum(map(len, ['a', 'bb', 'ccc']))) # 6   — total length, no intermediate list
```

---

## Branch 4 — Comprehensions Often Read Better

Every `map`/`filter` has an equivalent **comprehension**, which many find clearer — especially when you'd otherwise need a `lambda`.

| Goal | `map`/`filter` | Comprehension |
|---|---|---|
| Transform | `list(map(str, nums))` | `[str(n) for n in nums]` |
| Keep some | `list(filter(lambda x: x%2==0, nums))` | `[x for x in nums if x % 2 == 0]` |
| Both | `list(map(f, filter(g, xs)))` | `[f(x) for x in xs if g(x)]` |

> [!tip] When to use which
> Reach for **`map`/`filter`** when you already have a **named function** to apply — `map(int, lines)` and `filter(str.isalpha, words)` are crisp. Reach for a **comprehension** when the logic would need a `lambda` — `[x*x for x in nums]` beats `map(lambda x: x*x, nums)`.

---

## Key Takeaways

- **`map(func, iterable)`** applies `func` to every item → new items (e.g. `map(int, lines)` turns text into numbers). With several iterables, `func` gets one item from each.
- **`filter(func, iterable)`** keeps only items where `func(item)` is truthy; **`filter(None, x)`** keeps just the truthy items.
- Both return **lazy, single-use iterators** — wrap in `list()` or feed to `sum`/`sorted`/a loop.
- A **comprehension** is the common, often clearer alternative: `[f(x) for x in xs if g(x)]`. Use `map`/`filter` with a **named function**, a comprehension when you'd need a `lambda`.

---

## Exercises

> [!example] Exercise 1 — Uppercase every word
> **Problem.** Given `words = ['cat', 'dog', 'bird']`, use `map()` to produce `['CAT', 'DOG', 'BIRD']`.
>
> > [!success]- Click to reveal solution
> > **Solution.** `str.upper` is a named function — `map` applies it to each word.
> > ```python
> > words = ['cat', 'dog', 'bird']
> > print(list(map(str.upper, words)))
> > ```
> > **Answer.** `['CAT', 'DOG', 'BIRD']` ✓

> [!example] Exercise 2 — Keep the positive numbers
> **Problem.** Given `nums = [-3, 5, -1, 8, 0, 2]`, use `filter()` to keep only the numbers greater than 0.
>
> > [!success]- Click to reveal solution
> > **Solution.** The test `lambda x: x > 0` returns `True` for positives, which `filter` keeps.
> > ```python
> > nums = [-3, 5, -1, 8, 0, 2]
> > print(list(filter(lambda x: x > 0, nums)))
> > ```
> > **Answer.** `[5, 8, 2]` ✓

---

### Sources

| Source | Date | Type |
|---|---|---|
| Python `map` / `filter` — official built-in functions documentation | 2026 | Standard library reference |
| Verified against Python 3.14 on `E:\Python` | 2026-07-08 | Local test |
