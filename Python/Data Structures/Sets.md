# Sets

_Research compiled 2026-07-08 — Python's built-in `set` type and `set()` function_

> Companion to [List Methods](<List Methods.md>), [Dictionary Methods](<Dictionary Methods.md>), and [Tuples](<Tuples.md>). A **set** is an **unordered** collection of **unique** items — no duplicates, no positions. Two things it's great at: removing duplicates, and doing fast **membership tests** and **set math** (union, intersection, difference).

---

## Branch 1 — What a Set Is

- **Unique** — duplicates are automatically dropped.
- **Unordered** — no indexing (`s[0]` is an error); order isn't kept.
- Written with **curly braces** `{1, 2, 3}` or the **`set()`** function.

```python
s = {1, 2, 3, 2, 1}
print(s)              # {1, 2, 3}   — duplicates removed

print(set([1, 1, 2, 3, 3]))   # {1, 2, 3}   — build from any iterable
```

> [!warning] The empty-set trap
> `{}` is an **empty dict**, not an empty set. For an empty set you **must** use `set()`:
> ```python
> print(type({}))       # <class 'dict'>
> print(type(set()))    # <class 'set'>
> ```

---

## Branch 2 — Adding, Removing, Testing

```python
s = {1, 2}
s.add(3)            # add one item
s.discard(9)        # remove if present — NO error if it's absent
s.remove(2)         # remove — RAISES KeyError if absent
print(s)            # {1, 3}

print(2 in {1, 2, 3})   # True   — membership test
```

| Method | What it does |
|---|---|
| `.add(x)` | add an item |
| `.discard(x)` | remove `x`; **no error** if it's not there |
| `.remove(x)` | remove `x`; **`KeyError`** if it's not there |
| `.pop()` | remove and return an arbitrary item |
| `.clear()` | empty the set |
| `x in s` | membership test — **very fast** |

> [!tip] Sets make membership checks fast
> Checking `x in a_list` scans every item; checking `x in a_set` is near-instant regardless of size. If you repeatedly test "is this in my collection?", store the collection as a set.

---

## Branch 3 — Set Math (the real power)

Sets support the mathematical set operations directly, with operators or method names.

```python
a = {1, 2, 3, 4}
b = {3, 4, 5, 6}

print(a | b)    # {1, 2, 3, 4, 5, 6}   union — everything in either
print(a & b)    # {3, 4}               intersection — in BOTH
print(a - b)    # {1, 2}               difference — in a but not b
print(a ^ b)    # {1, 2, 5, 6}         symmetric difference — in one but not both
```

| Operation | Operator | Method | Meaning |
|---|---|---|---|
| Union | `a \| b` | `a.union(b)` | in **either** set |
| Intersection | `a & b` | `a.intersection(b)` | in **both** sets |
| Difference | `a - b` | `a.difference(b)` | in `a` but **not** `b` |
| Symmetric difference | `a ^ b` | `a.symmetric_difference(b)` | in exactly **one** |
| Subset | `a <= b` | `a.issubset(b)` | every item of `a` is in `b` |

```python
print({1, 2} <= {1, 2, 3})   # True   — {1,2} is a subset
```

---

## Branch 4 — The Most Common Use: Remove Duplicates

Wrapping a list in `set()` drops duplicates instantly. If you need a list back, wrap it again in `list()` — but note **order is lost**.

```python
nums = [3, 1, 2, 3, 1]
print(set(nums))          # {1, 2, 3}
print(list(set(nums)))    # [1, 2, 3]   — deduped (order NOT guaranteed)

# to dedupe AND keep first-seen order, use dict.fromkeys instead:
print(list(dict.fromkeys(nums)))   # [3, 1, 2]
```

> [!note] Sets don't keep order
> If order matters, `list(set(x))` is the wrong tool — use `list(dict.fromkeys(x))` (dicts keep insertion order). Reach for a set only when uniqueness matters and order doesn't.

---

## Branch 5 — What Can Go In a Set

Set items must be **hashable** — basically **immutable**: numbers, strings, and **tuples** are fine; **lists and dicts are not** (they'd raise `TypeError`).

```python
ok = {1, 'hi', (2, 3)}       # numbers, strings, tuples — fine
# bad = {[1, 2]}             # TypeError: unhashable type: 'list'
```

A **`frozenset`** is an **immutable** set — since it's hashable, it can itself be a set member or a dict key:

```python
fs = frozenset([1, 2, 3])
print({fs: 'group A'}[fs])   # 'group A'   — frozenset as a dict key
```

---

## Key Takeaways

- A **set** is an **unordered collection of unique items**: `{1, 2, 3}` or `set(iterable)`. Use **`set()`** for an empty one — `{}` is a dict.
- **`.add`** / **`.discard`** (safe) / **`.remove`** (errors if absent); `x in s` is a **fast** membership test.
- **Set math:** `|` union, `&` intersection, `-` difference, `^` symmetric difference, `<=` subset.
- **`list(set(x))`** removes duplicates but **loses order**; use `list(dict.fromkeys(x))` to dedupe *and* keep order.
- Items must be **hashable** (numbers/strings/tuples — not lists/dicts); a **`frozenset`** is an immutable set usable as a dict key or set member.

---

## Exercises

> [!example] Exercise 1 — Remove duplicates
> **Problem.** Given `nums = [4, 2, 4, 1, 2, 4]`, produce a collection of just the unique numbers.
>
> > [!success]- Click to reveal solution
> > **Solution.** Wrapping the list in `set()` drops duplicates.
> > ```python
> > nums = [4, 2, 4, 1, 2, 4]
> > print(set(nums))
> > ```
> > **Answer.** `{1, 2, 4}` ✓ (order not guaranteed)

> [!example] Exercise 2 — What's in both lists?
> **Problem.** Given `a = ['apple', 'pear', 'kiwi']` and `b = ['kiwi', 'plum', 'apple']`, find the items that appear in **both** lists.
>
> > [!success]- Click to reveal solution
> > **Solution.** Turn both into sets and take the intersection with `&`.
> > ```python
> > a = ['apple', 'pear', 'kiwi']
> > b = ['kiwi', 'plum', 'apple']
> > print(set(a) & set(b))
> > ```
> > **Answer.** `{'apple', 'kiwi'}` ✓

---

### Sources

| Source | Date | Type |
|---|---|---|
| Python `set` / `frozenset` — official data-structures documentation | 2026 | Standard library reference |
| Verified against Python 3.14 on `E:\Python` | 2026-07-08 | Local test |
