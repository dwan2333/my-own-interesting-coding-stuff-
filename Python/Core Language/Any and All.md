# The any() and all() Functions

_Research compiled 2026-07-08 — Python built-in functions `any()` and `all()`_

> Part of the [Python Reference](<../Python Reference (Main).md>). **`any()`** and **`all()`** are a pair of built-in functions that answer yes/no questions about a whole collection at once: *"is **any** item true?"* and *"are **all** items true?"* They're the clean way to replace a loop that just checks a condition across items.

---

## Branch 1 — `any()` — is at least one item truthy?

Returns **`True` if *at least one*** item in the iterable is truthy, and `False` only if **every** item is falsy.

```python
print(any([False, False, True]))     # True   — one truthy item is enough
print(any([0, '', None]))            # False  — all falsy
print(any([]))                       # False  — empty: nothing is truthy
```

---

## Branch 2 — `all()` — is every item truthy?

Returns **`True` only if *every*** item is truthy. One falsy item makes it `False`.

```python
print(all([True, True, True]))       # True   — all truthy
print(all([True, 0, True]))          # False  — the 0 breaks it
print(all([]))                       # True   — empty: "nothing fails the test"
```

> [!warning] The empty-iterable cases are opposite (and easy to forget)
> `any([])` is **`False`** (there's nothing truthy), but `all([])` is **`True`** (there's nothing that fails). This "empty `all()` is True" surprises people — guard with a length check if an empty collection should count as failure.

---

## Branch 3 — The Real Pattern: a condition over items

You rarely pass a plain list of booleans. The everyday use is **`any(condition for item in iterable)`** — a generator that produces `True`/`False` per item. It reads almost like English.

```python
nums = [2, 4, 7, 8]
print(any(n % 2 == 1 for n in nums))   # True   — is ANY number odd?  (7 is)
print(all(n % 2 == 0 for n in nums))   # False  — are they ALL even?  (7 isn't)

words = ['cat', 'elephant', 'dog']
print(any(len(w) > 5 for w in words))  # True   — is ANY word long?  (elephant)
print(all(len(w) >= 3 for w in words)) # True   — are ALL words >= 3 letters?
```

This replaces a manual loop-with-a-flag:

```python
# the long way any() replaces:
found = False
for n in nums:
    if n % 2 == 1:
        found = True
        break
# ...is just:  found = any(n % 2 == 1 for n in nums)
```

---

## Branch 4 — Two Things to Remember

### They test *truthiness*, not literal `True`

`any()`/`all()` check whether each item is **truthy**, not whether it equals `True`. Python's **falsy** values are: `False`, `0`, `0.0`, `''`, `[]`, `{}`, `()`, and `None`. Everything else is truthy.

```python
print(any(['', 'hello', '']))   # True  — 'hello' is a non-empty (truthy) string
print(all([1, 2, 3]))           # True  — all non-zero numbers are truthy
```

### They short-circuit (stop early)

`any()` stops at the **first truthy** item; `all()` stops at the **first falsy** item. It doesn't examine the rest — efficient on big or lazy sequences.

---

## `any()` vs `all()` — quick reference

| | `any(iterable)` | `all(iterable)` |
|---|---|---|
| Returns `True` when | **at least one** item is truthy | **every** item is truthy |
| Returns `False` when | **all** items are falsy | **at least one** item is falsy |
| Empty iterable | `False` | `True` |
| Stops early at | first **truthy** item | first **falsy** item |

Think of them as the "OR across a collection" (`any`) and "AND across a collection" (`all`).

---

## Key Takeaways

- **`any(iterable)`** → `True` if *at least one* item is truthy; **`all(iterable)`** → `True` only if *every* item is truthy.
- The everyday form is **`any(cond for x in items)`** / **`all(cond for x in items)`** — a readable replacement for a loop-with-a-flag.
- They test **truthiness** (falsy = `False`/`0`/`''`/`[]`/`{}`/`None`), not literal `True`, and they **short-circuit**.
- Watch the empty case: **`any([])` is `False`**, but **`all([])` is `True`**.

---

## Exercises

> [!example] Exercise 1 — Is any word "long"?
> **Problem.** Given `words = ['cat', 'elephant', 'dog']`, use `any()` to check whether **any** word is longer than 5 letters. Print the result.
>
> > [!success]- Click to reveal solution
> > **Solution.** A generator produces `len(w) > 5` for each word; `any()` reports if even one is `True`.
> > ```python
> > words = ['cat', 'elephant', 'dog']
> > print(any(len(w) > 5 for w in words))
> > ```
> > **Answer.** `True` ✓ ('elephant' has 8 letters)

> [!example] Exercise 2 — Are all numbers positive?
> **Problem.** Given `nums = [3, 8, 1, 6]`, use `all()` to check whether **every** number is greater than 0. Print the result.
>
> > [!success]- Click to reveal solution
> > **Solution.** `all()` is `True` only if the condition holds for every item.
> > ```python
> > nums = [3, 8, 1, 6]
> > print(all(n > 0 for n in nums))
> > ```
> > **Answer.** `True` ✓ (all four are positive; if any were `0` or negative it would be `False`)

---

### Sources

| Source | Date | Type |
|---|---|---|
| Python `any` / `all` — official built-in functions documentation | 2026 | Standard library reference |
| Verified against Python 3.14 on `E:\Python` | 2026-07-08 | Local test |
