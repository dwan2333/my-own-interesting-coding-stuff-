# Sorting — sorted() and .sort()

_Research compiled 2026-07-08 — Python's built-in sorting: the `sorted()` function and the `list.sort()` method_

> Companion to [List Methods](<List Methods.md>) and [Tuples](<Tuples.md>). Python gives you **two ways to sort**: the built-in **`sorted()`** function (returns a *new* sorted list, works on *any* iterable) and the **`.sort()`** method (sorts a list *in place*). Both share the same two powerful options — **`key`** and **`reverse`**.

---

## Branch 1 — Two Ways to Sort

### `sorted(iterable)` — returns a NEW sorted list

Works on **any** iterable (list, tuple, string, dict-keys…) and leaves the original untouched — it hands back a brand-new list.

```python
print(sorted([3, 1, 2]))       # [1, 2, 3]
print(sorted((3, 1, 2)))       # [1, 2, 3]   — tuple in, LIST out
print(sorted('dbca'))          # ['a', 'b', 'c', 'd']  — string → list of chars

nums = [3, 1, 2]
print(sorted(nums))            # [1, 2, 3]
print(nums)                    # [3, 1, 2]   — original is unchanged
```

### `list.sort()` — sorts the list IN PLACE

A method on lists only. It rearranges the list itself and returns **`None`**.

```python
lst = [3, 1, 2]
lst.sort()
print(lst)                     # [1, 2, 3]
```

> [!warning] `.sort()` returns `None` — don't assign it
> `lst = lst.sort()` is a classic bug: it sets `lst` to `None`. Call `lst.sort()` on its own line, or use `sorted(lst)` when you want a value back.

---

## Branch 2 — `reverse=` for Descending Order

Add `reverse=True` (works on both) to sort largest-to-smallest.

```python
print(sorted([3, 1, 2], reverse=True))   # [3, 2, 1]

lst = [3, 1, 2]
lst.sort(reverse=True)
print(lst)                                # [3, 2, 1]
```

---

## Branch 3 — `key=` : Sort by a Computed Value (the powerful part)

`key` takes a **function** applied to each item; Python sorts by the *result* of that function instead of the item itself. This is what makes sorting flexible.

### Sort by a built-in property

```python
words = ['banana', 'kiwi', 'cherry']
print(sorted(words, key=len))          # ['kiwi', 'banana', 'cherry']  — by length

print(sorted(['B', 'a', 'C', 'b'], key=str.lower))   # ['a', 'B', 'b', 'C']  — case-insensitive
```

### Sort by part of each item — with a `lambda`

A `lambda` is a tiny inline function (see [Star Parameters](<../Core Language/Star Parameters - args and kwargs.md>) for related function syntax). Use it to pick *which* value to sort on.

```python
# a list of tuples — sort by the SECOND element
pairs = [('a', 3), ('b', 1), ('c', 2)]
print(sorted(pairs, key=lambda p: p[1]))
# [('b', 1), ('c', 2), ('a', 3)]

# sort a dict's items by VALUE (highest last)
scores = {'x': 5, 'y': 2, 'z': 8}
print(sorted(scores.items(), key=lambda kv: kv[1]))
# [('y', 2), ('x', 5), ('z', 8)]
```

> [!tip] `key` is called once per item
> Read `key=lambda p: p[1]` as *"for each item `p`, sort by `p[1]`."* The function receives one item and returns the thing to compare. Combine with `reverse=True` to get, say, the highest scores first.

---

## Branch 4 — Sorting Is Stable

Python's sort is **stable**: items that compare **equal keep their original order**. So you can sort by one thing, then another, and ties from the second sort preserve the first ordering.

```python
data = [('a', 2), ('b', 1), ('c', 2), ('d', 1)]
print(sorted(data, key=lambda p: p[1]))
# [('b', 1), ('d', 1), ('a', 2), ('c', 2)]
#  b before d (both 1) and a before c (both 2) — original order kept within ties
```

---

## `sorted()` vs `.sort()` — quick reference

| | `sorted(iterable)` | `list.sort()` |
|---|---|---|
| Returns | a **new** sorted list | **`None`** (sorts in place) |
| Works on | **any** iterable (list, tuple, str, dict…) | **lists only** |
| Original | unchanged | modified |
| Options | `key=`, `reverse=` | `key=`, `reverse=` |
| Use when | you need a sorted copy, or the source isn't a list | you own the list and don't need the original order |

---

## Key Takeaways

- **`sorted(iterable)`** returns a **new** sorted list from any iterable; **`list.sort()`** sorts a list **in place** and returns **`None`** (never assign its result).
- **`reverse=True`** sorts descending (both).
- **`key=func`** sorts by a computed value — `key=len`, `key=str.lower`, or `key=lambda p: p[1]` to sort by part of each item (tuples, dict `.items()`, objects).
- Python's sort is **stable** — equal keys keep their original order.
- Numbers sort numerically; strings sort in Unicode order (uppercase before lowercase — use `key=str.lower` for true alphabetical).

---

## Exercises

> [!example] Exercise 1 — Sort words by length
> **Problem.** Sort `['pear', 'fig', 'banana', 'kiwi']` from shortest to longest word. Print the result.
>
> > [!success]- Click to reveal solution
> > **Solution.** Use `key=len` so items are compared by their length.
> > ```python
> > fruits = ['pear', 'fig', 'banana', 'kiwi']
> > print(sorted(fruits, key=len))
> > ```
> > **Answer.** `['fig', 'pear', 'kiwi', 'banana']` ✓ (pear before kiwi — both length 4, original order kept)

> [!example] Exercise 2 — Sort a scoreboard, highest first
> **Problem.** Given `scores = {'Ann': 12, 'Bo': 20, 'Cy': 7}`, produce a list of `(name, score)` pairs sorted from **highest** score to lowest.
>
> > [!success]- Click to reveal solution
> > **Solution.** Sort `scores.items()` by the value with a lambda, and `reverse=True` for descending.
> > ```python
> > scores = {'Ann': 12, 'Bo': 20, 'Cy': 7}
> > print(sorted(scores.items(), key=lambda kv: kv[1], reverse=True))
> > ```
> > **Answer.** `[('Bo', 20), ('Ann', 12), ('Cy', 7)]` ✓

---

### Sources

| Source | Date | Type |
|---|---|---|
| Python `sorted` / `list.sort` — official documentation & Sorting HOW TO | 2026 | Standard library reference |
| Verified against Python 3.14 on `E:\Python` | 2026-07-08 | Local test |
