# Multi-Dimensional Arrays (§3.3)

_Notes compiled 2026-07-08 — Rance D. Necaise, *Data Structures and Algorithms Using Python*, §3.3, written for a first-time reader with main-agent verification of the storage math._

> [!tip] Where this fits
> Chapter 3 is **"Sets and Maps"**, but §3.3 is a self-contained detour into **multi-dimensional arrays** — grids, cubes, and higher. It builds on the 2-D array from Chapter 2 and connects directly to how Python's **[tuple](<../Python/Data Structures/Tuples.md>)** carries multi-part subscripts like `x[i, j]`.

---

> [!info] Section essence — in one breath
> A **multi-dimensional array** is a grid of more than one dimension: a 2-D array is a **table** (rows × columns), a 3-D array is a **box of tables**, and you can go higher. You reach an element with **one index per dimension** — `x[i, j]` or `y[i, j, k]`. The twist the section reveals: the computer has no real "2-D memory," so a multi-D array is secretly stored as **one long 1-D array**, and a small **formula** converts your `(i, j)` coordinates into a single position in that line.

---

## 1. The Picture: grids, boxes, and beyond

- **2-D array** — a **table**: pick a row and a column. Element `x[i, j]`.
- **3-D array** — a **box of tables**: pick a table, then a row, then a column. Element `y[i, j, k]`.
- **n-D array** — any number of dimensions; harder to picture, but the idea is the same: one index per dimension.

Every index **starts at 0**, and you must supply **all** of them to reach an element.

---

## 2. The MultiArray ADT (the "remote control")

Just like Chapter 1's Date and Bag, the book defines an **abstract data type** — the buttons you press, hiding the machinery inside. Python has no built-in array of any dimension, so the ADT builds one.

| Button (operation) | What it does |
|---|---|
| `MultiArray(d1, d2, … dn)` | **constructor** — make an array with those dimension lengths (needs 2+ dimensions); every element starts as `None` |
| `dims()` | how many dimensions the array has |
| `length(dim)` | the length of one dimension (dimensions numbered from 1 = highest) |
| `clear(value)` | set **every** element to `value` |
| `x[i, j, …]` | **get** the element at that coordinate (via `__getitem__`) |
| `x[i, j, …] = v` | **set** that element to `v` (via `__setitem__`) |

> [!tip] The coordinate is a tuple
> When you write `x[1, 2]`, Python packs `1, 2` into the **tuple** `(1, 2)` and hands it to the array's `__getitem__` as a single argument. That's why a multi-component subscript is called an **n-tuple subscript** — see [Tuples §7](<../Python/Data Structures/Tuples.md>).

---

## 3. The Big Idea: a multi-D array is really a 1-D array

Computer memory is **one long line** of slots — there's no physical "grid." So a 2-D (or n-D) array is an **abstract view** laid on top of a single **1-D array**. The language (or the ADT) does the bookkeeping to make it *feel* like a grid.

The question this raises: if a 3×5 table lives in one 1-D line of 15 slots, **in what order** do the elements go? There are two standard answers.

### Row-major vs. column-major order

| Order | How it lays the grid into the line | Used by |
|---|---|---|
| **Row-major** | one **row** at a time — all of row 0, then all of row 1, … | most languages (C, Python's NumPy default) |
| **Column-major** | one **column** at a time — all of column 0, then column 1, … | FORTRAN, MATLAB, R |

For this 3×5 grid (3 rows, 5 columns):

```
grid:
 0  1  2  3  4
 5  6  7  8  9
10 11 12 13 14

row-major line:  0  1  2  3  4  5  6  7  8  9 10 11 12 13 14   (rows in order)
col-major line:  0  5 10  1  6 11  2  7 12  3  8 13  4  9 14   (columns in order)
```

---

## 4. The Index Formula (coordinates → position)

To read `x[i, j]`, the language must compute **which slot** of the 1-D line holds it. For an `m × n` grid (m rows, n columns) stored **row-major**:

$$\text{index}(i, j) = i \times n + j$$

Why it works: to reach row `i`, you skip `i` whole rows — that's `i × n` elements (each row has `n` columns). Then `+ j` steps across to the right column.

> [!example] Find element (2, 3) in the 3×5 grid
> **Given.** `m = 3` rows, `n = 5` columns, target coordinate `(2, 3)`.
> **Compute.** `index(2, 3) = 2 × 5 + 3 = 13`.
> **Check.** Slot 13 of the row-major line above holds `13` — the value at grid position (2, 3). ✓
> **Column-major** would instead be `index(i, j) = j × m + i = 3 × 3 + 2 = 11`.

The same idea scales up: a 3-D array skips whole *tables*, then whole *rows*, then columns; each extra dimension just adds another "skip this many complete blocks" term.

---

## 5. Seeing It in Real Python (NumPy)

You don't build this by hand in practice — **NumPy** arrays *are* multi-dimensional arrays stored exactly this way, and let you choose the order (`'C'` = row-major, `'F'` = column-major):

```python
import numpy as np

a = np.arange(15).reshape(3, 5)     # the 3×5 grid
print(a[2, 3])                       # 13   — tuple subscript (2, 3)

print(a.flatten('C').tolist())       # row-major:  [0,1,2,...,14]
print(a.flatten('F').tolist())       # col-major:  [0,5,10,1,6,11,...]
```

`a[2, 3]` uses the exact tuple-subscript mechanism from §2 — and `flatten('C')` / `flatten('F')` show the two storage orders from §3.

---

## Key Ideas

- A **multi-dimensional array** stores elements reached by **one index per dimension** (`x[i, j]`, `y[i, j, k]`); indices start at 0 and all must be given.
- The **MultiArray ADT** wraps this behind buttons — `dims()`, `length(dim)`, `clear(value)`, and `x[…]` get/set — because Python has no built-in array.
- A multi-D array is **physically one 1-D array**; the grid is an abstraction over that line.
- Two storage orders: **row-major** (rows in sequence — C/NumPy) and **column-major** (columns in sequence — FORTRAN).
- The **row-major index formula** is `i × n + j` for an `m × n` grid — skip `i` full rows, then step `j` columns. Higher dimensions add more "skip whole blocks" terms.
- **NumPy** is this concept made real: `a[i, j]` (tuple subscript) with `'C'`/`'F'` order.

---

### Sources

| Source | Detail | Type |
|---|---|---|
| Rance D. Necaise, *Data Structures and Algorithms Using Python* | §3.3 Multi-Dimensional Arrays | Textbook |
| Main-agent verification | Row/column-major storage and the `i·n + j` index formula checked against NumPy `'C'`/`'F'` order | — |
