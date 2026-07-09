# Tuples

_Research compiled 2026-07-08 — Python's built-in `tuple`, with usage notes from Necaise, *Data Structures and Algorithms Using Python*_

> Companion to [List Methods](<List Methods.md>) and [Dictionary Methods](<Dictionary Methods.md>). A **tuple** is an **ordered, immutable** sequence — like a list you can read and slice, but **cannot change** after it's built. Use it for a fixed group of values that belong together (a coordinate, a row, a "record").

> [!note] A note on the source
> In *Data Structures and Algorithms Using Python* (Necaise), **Chapter 3 is "Sets and Maps"** — it has no dedicated tuple section. The book *uses* tuples as **multi-component array subscripts** in §2.3 (2-D arrays) and §3.3 (multi-dimensional arrays); that specific use is covered in Branch 6 below. The rest of this note is a general tuple reference with verified examples.

---

## Branch 1 — What a Tuple Is

- **Ordered** — items keep their position, and you index them like a list (`t[0]`).
- **Immutable** — once created, you can't add, remove, or replace items.
- Written with **commas**, usually wrapped in **parentheses**: `(1, 2, 3)`.

```python
t = (1, 2, 3)
print(t)              # (1, 2, 3)
print(type(t))        # <class 'tuple'>
```

> [!tip] It's the commas, not the parentheses
> A tuple is really defined by the **commas**; the parentheses just group them. `1, 2, 3` is already a tuple. But always writing the parentheses makes code clearer.

---

## Branch 2 — Creating Tuples

```python
empty = ()                 # empty tuple
point = (3, 4)             # two items
mixed = (1, 'hi', 3.5)     # types can differ
from_list = tuple([1, 2, 3])   # build from any iterable
```

> [!warning] The single-item tuple trap
> A one-item tuple **needs a trailing comma** — the parentheses alone don't make it a tuple:
> ```python
> print(type((5,)))     # <class 'tuple'>   ← comma makes it a tuple
> print(type((5)))      # <class 'int'>     ← just a number in parentheses!
> ```

---

## Branch 3 — Reading a Tuple (same as a list)

Everything you do to *read* a list works on a tuple — index, negative index, slice, loop, `len`, `in`.

```python
t = ('a', 'b', 'c', 'd')
print(t[0])       # 'a'
print(t[-1])      # 'd'
print(t[1:3])     # ('b', 'c')   — a slice is a new tuple
print(len(t))     # 4
print('b' in t)   # True
for item in t:
    print(item)   # a / b / c / d
```

---

## Branch 4 — Immutability (the whole point)

You **cannot** change a tuple after building it — assigning to an index raises `TypeError`.

```python
t = (1, 2, 3)
t[0] = 99          # TypeError: 'tuple' object does not support item assignment
```

Why is that *useful*?
- **Safety** — a tuple you pass around can't be modified by accident.
- **It can be a dictionary key or a set member** (a list can't — see Branch 5).
- **Signals intent** — "this group of values is fixed."

> [!warning] "Immutable" means the tuple's *slots* are fixed — not what's inside them
> If a tuple holds a **mutable** object (like a list), that inner object can still change. The tuple just can't swap it for a different object.
> ```python
> t = (1, [2, 3])
> t[1].append(4)      # allowed — we mutate the inner list, not the tuple
> print(t)            # (1, [2, 3, 4])
> ```

---

## Branch 5 — Packing and Unpacking (tuples' superpower)

**Packing** — commas bundle several values into one tuple. **Unpacking** — spread a tuple back into separate variables.

```python
# unpack into matching variables
a, b, c = (10, 20, 30)
print(a, b, c)          # 10 20 30

# swap two variables with no temp variable
x, y = 1, 2
x, y = y, x
print(x, y)             # 2 1

# grab the first, collect the rest with *
first, *rest = (1, 2, 3, 4)
print(first, rest)      # 1 [2, 3, 4]
```

This is also **how a function returns several values** — it really returns one tuple, which you unpack:

```python
def min_max(nums):
    return min(nums), max(nums)     # packs into a tuple

lo, hi = min_max([4, 1, 7, 3])      # unpacks it
print(lo, hi)                        # 1 7
```

---

## Branch 6 — The Two Methods, + Tuples as Keys

A tuple has only **two** methods (because it can't be modified):

| Method | What it does |
|---|---|
| `.count(x)` | how many times `x` appears |
| `.index(x)` | position of the first `x` (`ValueError` if absent) |

```python
t = (1, 2, 2, 3, 2)
print(t.count(2))    # 3
print(t.index(3))    # 3
```

Because tuples are immutable, they are **hashable**, so they can be **dictionary keys** or **set members** — a common way to key data by a coordinate or pair:

```python
grid = {(0, 0): 'origin', (1, 2): 'treasure'}
print(grid[(1, 2)])          # 'treasure'
```

---

## Branch 7 — How the Book Uses Tuples: multi-dimensional subscripts

This is the tuple usage in Necaise's array chapters. When you index with **more than one value** — `x[i, j]` — Python automatically **packs those values into a tuple** and hands it to the object's `__getitem__` method as a single argument.

```python
class Grid:
    def __getitem__(self, ndx):
        return f"received a {type(ndx).__name__}: {ndx}"

g = Grid()
print(g[2, 3])       # received a tuple: (2, 3)
```

So the book's 2-D and multi-dimensional array classes define `__getitem__(self, ndxTuple)` and read `ndxTuple[0]`, `ndxTuple[1]` as the row and column. The tuple is the perfect carrier here precisely *because* it's an immutable, fixed-size group of coordinates. (This is why writing `matrix[r, c]` works in libraries like NumPy too.)

---

## Branch 8 — Tuple vs. List: which to use?

| | **tuple** | **list** |
|---|---|---|
| Changeable? | No (immutable) | Yes (mutable) |
| Syntax | `(1, 2, 3)` | `[1, 2, 3]` |
| Methods | 2 (`count`, `index`) | ~11 (`append`, `sort`, …) |
| Dict key / set member? | Yes | No |
| Use for | a **fixed record** — a coordinate, a returned pair, a row that won't change | a **collection you'll edit** — add/remove/sort items |

Rule of thumb: **reach for a list by default; choose a tuple when the group is fixed** or needs to be a dict key.

---

## Key Takeaways

- A **tuple** is an **ordered, immutable** sequence: `(1, 2, 3)`. It's the **commas** that make it — and a single-item tuple needs a trailing comma: `(5,)`.
- You **read** tuples exactly like lists (index, slice, loop, `in`, `len`), but you **can't change** them — assignment raises `TypeError`. (Mutable objects *inside* a tuple can still change.)
- **Packing/unpacking** is the killer feature: `a, b = b, a` swaps; `lo, hi = min_max(x)` returns multiple values; `first, *rest = t` splits.
- Only **two methods**: `count()` and `index()`. Being immutable makes tuples **hashable**, so they work as **dict keys / set members**.
- The DSA book uses tuples as **multi-component subscripts**: `x[i, j]` packs `(i, j)` into a tuple passed to `__getitem__`.
- Use a **tuple for fixed records**, a **list for collections you'll edit**.

---

## Exercises

> [!example] Exercise 1 — Swap without a temp variable
> **Problem.** Given `a = 5` and `b = 9`, swap their values using tuple unpacking (no third variable), then print `a, b`.
>
> > [!success]- Click to reveal solution
> > **Solution.** The right side packs `(b, a)` into a tuple; the left side unpacks it.
> > ```python
> > a, b = 5, 9
> > a, b = b, a
> > print(a, b)
> > ```
> > **Answer.** `9 5` ✓

> [!example] Exercise 2 — Return two values from a function
> **Problem.** Write `stats(nums)` that returns both the smallest and largest of a list, then unpack the result into `lo, hi`. Test on `[4, 1, 7, 3]`.
>
> > [!success]- Click to reveal solution
> > **Solution.** Returning `min(nums), max(nums)` packs a tuple; unpack it at the call site.
> > ```python
> > def stats(nums):
> >     return min(nums), max(nums)
> > lo, hi = stats([4, 1, 7, 3])
> > print(lo, hi)
> > ```
> > **Answer.** `1 7` ✓

---

### Sources

| Source | Date | Type |
|---|---|---|
| Python `tuple` — official data-structures documentation | 2026 | Standard library reference |
| Rance D. Necaise, *Data Structures and Algorithms Using Python* — §2.3, §3.3 (tuples as array subscripts) | 2026 | Textbook |
| Verified against Python 3.14 on `E:\Python` | 2026-07-08 | Local test |
