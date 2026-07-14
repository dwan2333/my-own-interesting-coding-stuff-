# The NumPy Module

_Research compiled 2026-07-14 — Wes McKinney, *Python for Data Analysis* (3e), Ch. 4 "NumPy Basics: Arrays and Vectorized Computation", read directly from the book text with main-agent verification: every example below was executed against NumPy 2.5.1 and the outputs shown are real. Items marked **added** go beyond the chapter._

> Part of the [Python Reference](<../Python Reference (Main).md>). **NumPy** ("Numerical Python") is the foundation of scientific Python — an **ndarray** is a grid of same-typed values that you operate on *all at once* instead of looping. Everything pandas does is built on these ideas. Install with `pip install numpy`; the universal convention is:
>
> ```python
> import numpy as np
> ```
> (Don't use `from numpy import *` — NumPy has functions like `min`/`max` that would shadow Python's built-ins.)

---

## Branch 1 — Why NumPy? Vectorization and Speed

A NumPy array stores its data in **one contiguous block of memory** and runs its math in compiled **C** — no per-item type checking, no Python loop overhead. Operating on a whole array at once instead of looping is called **vectorization**.

```python
import numpy as np
import time

my_arr = np.arange(1_000_000)
my_list = list(range(1_000_000))

t = time.perf_counter(); my_arr2 = my_arr * 2;              t_arr  = time.perf_counter() - t
t = time.perf_counter(); my_list2 = [x * 2 for x in my_list]; t_list = time.perf_counter() - t
print(f'array: {t_arr*1000:.1f} ms   list: {t_list*1000:.1f} ms')
# array: 1.4 ms   list: 32.0 ms      — ~23× faster here; the book cites 10–100×
```

> [!tip] The mental shift
> Stop thinking "for each element, do X." Start thinking "do X to the whole array." Nearly every branch below is a variation on that single idea.

---

## Branch 2 — Creating Arrays

`np.array()` converts any sequence (list, tuple, another array) into an ndarray. Nested lists of equal length become a **2-dimensional** array:

```python
data = np.array([[1.5, -0.1, 3], [0, -3, 6.5]])
print(data)
# [[ 1.5 -0.1  3. ]
#  [ 0.  -3.   6.5]]
```

Every array carries three key **attributes**:

```python
print(data.shape)   # (2, 3)     — size of each dimension (2 rows, 3 columns)
print(data.dtype)   # float64    — the type ALL elements share
print(data.ndim)    # 2          — number of dimensions
```

The other creation functions, each with a verified example:

| Function | What it makes | Example → result |
|---|---|---|
| `np.array(seq)` | array from a sequence | `np.array([6, 7.5, 8])` → `[6. , 7.5, 8. ]` |
| `np.zeros(shape)` | all 0s | `np.zeros((2, 3))` → 2×3 of `0.` |
| `np.ones(shape)` | all 1s | `np.ones((2, 2))` → 2×2 of `1.` |
| `np.full(shape, v)` | all set to `v` | `np.full((2, 3), 7)` → 2×3 of `7` |
| `np.arange(n)` | array-version of `range` | `np.arange(8)` → `[0 1 2 3 4 5 6 7]` |
| `np.eye(n)` | n×n identity matrix | `np.eye(3)` → 1s on the diagonal |
| `np.empty(shape)` | **uninitialized** memory | garbage values — see warning |
| `np.linspace(a, b, n)` | `n` evenly spaced points from `a` to `b` **inclusive** *(added — not in the chapter but essential)* | `np.linspace(0, 1, 5)` → `[0.  , 0.25, 0.5 , 0.75, 1.  ]` |
| `*_like(arr)` variants | same shape/dtype as `arr` | `np.zeros_like(data)` → 2×3 of `0.` |

> [!warning] `np.empty` does NOT mean "empty"
> It allocates memory **without clearing it** — the array may contain nonzero garbage. Use it only when you'll overwrite every value anyway.

---

## Branch 3 — Data Types (`dtype`) and `astype()`

All elements of an ndarray share one **dtype** — that's what makes the C-speed math possible. Names are `type` + `bits`: `int32`, `float64` (= a Python `float`, 8 bytes), `bool`, etc.

```python
a = np.array([1, 2, 3], dtype=np.float64)   # choose the type at creation
b = np.array([1, 2, 3], dtype=np.int32)
print(a.dtype, b.dtype)     # float64 int32
print(np.array([1, 2, 3]).dtype)   # int64   — inferred when you don't specify
```

**`astype()` converts** (casts) an array to another dtype — it **always returns a new copy**:

```python
arr = np.array([1, 2, 3, 4, 5])
floats = arr.astype(np.float64)
print(floats)                       # [1. 2. 3. 4. 5.]

# float → int TRUNCATES toward zero (does not round!)
arr = np.array([3.7, -1.2, -2.6, 0.5, 12.9, 10.1])
print(arr.astype(np.int32))         # [ 3 -1 -2  0 12 10]

# strings of numbers → numeric
ns = np.array(["1.25", "-9.6", "42"])
print(ns.astype(float))             # [ 1.25 -9.6  42.  ]
```

> [!warning] Book vs. modern NumPy *(added)*
> The book (2022) uses `np.string_` for fixed-size strings — **NumPy 2.0 removed that name** (it's `np.bytes_` now, and fixed-size strings silently truncate, so prefer plain Python strings or pandas for text anyway). If a cast can't work (e.g. `"abc"` → float), you get a `ValueError`.

> [!note] Integer overflow is silent *(added)*
> Small integer dtypes wrap around instead of erroring: `np.array([255], dtype=np.uint8) + 1` → `[0]`. If your numbers might grow, stay with the default `int64`/`float64`.

---

## Branch 4 — Vectorized Arithmetic

Arithmetic between **equal-size arrays** applies element-by-element; arithmetic with a **scalar** applies to every element ("propagates"):

```python
arr = np.array([[1., 2., 3.], [4., 5., 6.]])

print(arr * arr)      # [[ 1.  4.  9.]     — element-wise, NOT matrix multiply
                      #  [16. 25. 36.]]
print(1 / arr)        # [[1.     0.5    0.3333]
                      #  [0.25   0.2    0.1667]]
print(arr ** 2)       # [[ 1.  4.  9.]
                      #  [16. 25. 36.]]
```

Comparisons are vectorized too — they return **Boolean arrays** (the fuel for Branch 6):

```python
arr2 = np.array([[0., 4., 1.], [7., 2., 12.]])
print(arr2 > arr)
# [[False  True False]
#  [ True False  True]]
```

Operations between *different-sized* arrays follow rules called **broadcasting** (the book defers this to its Appendix A — the short version: a scalar, and more generally any compatible smaller shape, is "stretched" to fit).

---

## Branch 5 — Indexing and Slicing: Slices Are **Views**!

1-D arrays index and slice like lists — with one huge difference: **a slice is a *view* into the original array, not a copy.** Modify the view and you modify the source.

```python
arr = np.arange(10)
print(arr[5], arr[5:8])         # 5 [5 6 7]

arr[5:8] = 12                   # assigning a scalar to a slice broadcasts it
print(arr)                      # [ 0  1  2  3  4 12 12 12  8  9]

arr_slice = arr[5:8]            # NO data copied — this is a window onto arr
arr_slice[1] = 12345
print(arr)                      # [    0     1     2     3     4    12 12345    12     8     9]

arr_slice[:] = 64               # bare [:] assigns into every slot of the view
print(arr)                      # [ 0  1  2  3  4 64 64 64  8  9]
```

```python
# want an independent copy? say so explicitly:
c = np.arange(10)
chunk = c[5:8].copy()
chunk[0] = 99
print(c)        # [0 1 2 3 4 5 6 7 8 9]   — untouched
```

**Higher dimensions** — separate indices with commas; `arr2d[0, 2]` beats `arr2d[0][2]`:

```python
arr2d = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
print(arr2d[2])        # [7 8 9]       — one index → whole row (a 1-D array)
print(arr2d[0, 2])     # 3             — row 0, column 2

print(arr2d[:2])       # first two ROWS       [[1 2 3]
                       #                       [4 5 6]]
print(arr2d[:2, 1:])   # rows 0–1, columns 1+  [[2 3]
                       #                       [5 6]]
print(arr2d[1, :2])    # [4 5]  — mixing an integer with a slice DROPS a dimension
print(arr2d[:, :1])    # every row, first column — still 2-D: [[1] [4] [7]]

arr2d[:2, 1:] = 0      # assignment hits the whole selected region
print(arr2d)           # [[1 0 0] [4 0 0] [7 8 9]]
```

> [!tip] The axis mental model *(added)*
> For 2-D arrays: **axis 0 runs down the rows; axis 1 runs across the columns.** `arr2d[:2]` slices along axis 0 ("first two rows"); `arr2d[:, :1]` says "all of axis 0, first slot of axis 1." Every `axis=` argument in Branch 11 uses the same numbering.

---

## Branch 6 — Boolean Indexing: Filter With a Mask

Index an array with a **Boolean array of matching length** and you keep only the `True` positions. This is NumPy's version of a `WHERE` clause:

```python
names = np.array(["Bob", "Joe", "Will", "Bob", "Will", "Joe", "Joe"])
data = np.array([[4, 7], [0, 2], [-5, 6], [0, 0], [1, 2], [-12, -4], [3, 4]])

print(names == "Bob")            # [ True False False  True False False False]
print(data[names == "Bob"])      # rows 0 and 3:  [[4 7]
                                 #                 [0 0]]
print(data[names == "Bob", 1])   # …and just column 1 of those rows: [7 0]
```

Invert with `~`, combine with `&` (and) / `|` (or):

```python
print(data[~(names == "Bob")])                    # everything EXCEPT Bob's rows
mask = (names == "Bob") | (names == "Will")
print(data[mask])                                 # Bob's and Will's rows
```

> [!warning] `and` / `or` do NOT work on arrays
> Use `&` and `|` (and wrap each comparison in parentheses — `&` binds tighter than `==`). Python's `and`/`or` raise an error on arrays.

**Setting values through a mask** is the idiomatic "clean the data" move:

```python
data[data < 0] = 0               # zero out every negative value, in place
data[names != "Joe"] = 7         # set entire rows via a 1-D mask
```

Unlike slicing, **Boolean selection always copies** the data when you assign it to a new variable.

---

## Branch 7 — Fancy Indexing: Select With Integer Lists

"Fancy indexing" = indexing with **arrays of integers**. Pass a list of row numbers to grab rows **in any order you like** (negative counts from the end):

```python
arr = np.zeros((8, 4))
for i in range(8):
    arr[i] = i                   # row i filled with the value i

print(arr[[4, 3, 0, 6]])         # rows 4, 3, 0, 6 — in exactly that order
print(arr[[-3, -5, -7]])         # rows 5, 3, 1 counted from the end
```

**Two index arrays** select individual *elements* by coordinate pairs — the result is 1-D:

```python
arr = np.arange(32).reshape((8, 4))
print(arr[[1, 5, 7, 2], [0, 3, 1, 2]])
# [ 4 23 29 10]    — elements (1,0), (5,3), (7,1), (2,2)

# want the rectangular block instead? select rows first, then reorder columns:
print(arr[[1, 5, 7, 2]][:, [0, 3, 1, 2]])
# [[ 4  7  5  6]
#  [20 23 21 22]
#  [28 31 29 30]
#  [ 8 11  9 10]]
```

Fancy indexing, unlike slicing, **always copies** into a new array (though assigning *into* `arr[rows, cols] = value` still modifies the original).

> [!note] The three selection styles side by side *(added)*
>
> | Style | Example | Returns |
> |---|---|---|
> | Slice | `arr[2:5]` | **view** — edits hit the original |
> | Boolean mask | `arr[arr > 0]` | **copy** |
> | Fancy (integer lists) | `arr[[4, 0, 2]]` | **copy** |

---

## Branch 8 — Transposing, `@`, and `reshape`

```python
arr = np.arange(15).reshape((3, 5))   # reshape: same data, new dimensions
print(arr.T)                          # .T flips rows↔columns (a VIEW, no copy)
# [[ 0  5 10]
#  [ 1  6 11]
#  [ 2  7 12]
#  [ 3  8 13]
#  [ 4  9 14]]
```

`*` is element-wise; **matrix multiplication** is the `@` operator (or `np.dot`):

```python
x = np.array([[0, 1, 0], [1, 2, -2], [6, 3, 2], [-1, 0, -1], [1, 0, 1]])
print(x.T @ x)               # (3×5) @ (5×3) → 3×3 matrix product
# [[39 20 12]
#  [20 14  2]
#  [12  2 10]]
```

`arr.swapaxes(0, 1)` generalizes `.T` to any pair of axes (also a view).

> [!tip] `reshape(-1)` — let NumPy do the math *(added)*
> One dimension may be `-1`, meaning "whatever fits": `np.arange(12).reshape(2, -1)` → shape `(2, 6)`. And `arr.ravel()` flattens back to 1-D. The chapter leans on `reshape` constantly but defers explaining it — these two idioms cover 90% of real use.

---

## Branch 9 — Pseudorandom Numbers: `default_rng`

`numpy.random` generates **whole arrays** of random values at once (the book measures it ~40× faster than looping Python's `random` — see [Random Modules](<Random Modules.md>) for the built-in). Modern code creates an explicit **generator** with an optional **seed** for reproducibility:

```python
rng = np.random.default_rng(seed=12345)
print(rng.standard_normal((2, 3)))
# [[-1.4238  1.2637 -0.8707]
#  [-0.2592 -0.0753 -0.7409]]     — same seed → same numbers, every run
```

| Generator method | What it draws | Example |
|---|---|---|
| `rng.integers(lo, hi, size=…)` | random ints in `[lo, hi)` | `rng.integers(0, 10, size=5)` → `[5 5 2 1 2]` |
| `rng.uniform(size=…)` | floats in `[0, 1)` | `rng.uniform(size=3)` → `[0.9418 0.2482 0.9489]` |
| `rng.standard_normal(shape)` | normal, mean 0, std 1 | see above |
| `rng.normal(mu, sigma, size=…)` | normal with your mean/std | — |
| `rng.permutation(seq)` | shuffled **copy** | `rng.permutation(np.arange(5))` → `[2 0 4 1 3]` |
| `rng.shuffle(seq)` | shuffle **in place** | — |
| `rng.binomial / beta / gamma / chisquare` | other distributions | — |

> [!note] Why a generator object instead of `np.random.xxx()`? *(added)*
> The older global functions (`np.random.seed`, `np.random.randn`, …) still exist but share hidden global state — any library call can disturb your sequence. A `rng` object is **isolated**: your results stay reproducible no matter what other code does.

---

## Branch 10 — Universal Functions (ufuncs): Element-Wise Math

A **ufunc** applies a fast element-wise operation to a whole array. **Unary** ufuncs take one array:

```python
arr = np.arange(10)
print(np.sqrt(arr))
# [0.     1.     1.4142 1.7321 2.     2.2361 2.4495 2.6458 2.8284 3.    ]
print(np.exp(np.arange(4)))
# [ 1.      2.7183  7.3891 20.0855]
```

**Binary** ufuncs take two arrays — e.g. `np.maximum` keeps the element-wise larger value:

```python
rng = np.random.default_rng(seed=42)
x = rng.standard_normal(5)    # [ 0.3047 -1.04    0.7505  0.9406 -1.951 ]
y = rng.standard_normal(5)    # [-1.3022  0.1278 -0.3162 -0.0168 -0.853 ]
print(np.maximum(x, y))       # [ 0.3047  0.1278  0.7505  0.9406 -0.853 ]
```

The ufunc toolbox, each verified:

| ufunc | What it does | Example → result |
|---|---|---|
| `np.abs(a)` | absolute value | `np.abs([-2, 3, -5])` → `[2 3 5]` |
| `np.sqrt(a)` / `np.square(a)` | `a ** 0.5` / `a ** 2` | above |
| `np.exp(a)` / `np.log(a)` | eˣ / natural log (`log10`, `log2` too) | above |
| `np.floor(a)` / `np.ceil(a)` | round down / up | `np.floor([3.7, -1.2])` → `[ 3. -2.]`, `ceil` → `[ 4. -1.]` |
| `np.rint(a)` | round to nearest int | — |
| `np.sign(a)` | −1, 0, or 1 per element | `np.sign([-5, 0, 9])` → `[-1  0  1]` |
| `np.isnan(a)` / `np.isfinite(a)` | NaN / finite test | `np.isnan([1.0, np.nan])` → `[False  True]` |
| `np.modf(a)` | fractional & whole parts, **two** outputs | `np.modf([4.51, -8.11])` → `[0.51 -0.11]`, `[4. -8.]` |
| `np.add / subtract / multiply / divide` | arithmetic as functions | — |
| `np.maximum / minimum` | element-wise max/min (`fmax`/`fmin` ignore NaN) | above |
| `np.power(a, b)` / `np.mod(a, b)` | aᵇ / remainder | — |
| `np.sin / cos / tan` (+ `arc…`, `…h`) | trigonometry | — |
| `np.greater / less / equal …` | the comparison operators as functions | — |

Ufuncs accept an **`out=`** argument to write results into an existing array instead of allocating a new one:

```python
arr = np.array([4.51, -8.11, 2.25])
out = np.zeros(3)
np.add(arr, 1, out=out)
print(out)          # [ 5.51 -7.11  3.25]
```

---

## Branch 11 — Array-Oriented Programming

The payoff branch: replacing loops *and* conditionals with array expressions.

### `np.where` — vectorized if/else

`np.where(condition, A, B)` picks from `A` where the condition is `True`, else from `B`:

```python
xarr = np.array([1.1, 1.2, 1.3, 1.4, 1.5])
yarr = np.array([2.1, 2.2, 2.3, 2.4, 2.5])
cond = np.array([True, False, True, True, False])

print(np.where(cond, xarr, yarr))    # [1.1 2.2 1.3 1.4 2.5]
```

`A`/`B` can be scalars or mix scalar-with-array — the classic clean-up patterns:

```python
arr = np.array([[2.6, 0.8, -0.9], [-1.2, 0.5, 0.7]])
print(np.where(arr > 0, 2, -2))     # all positives→2, negatives→-2
# [[ 2  2 -2]
#  [-2  2  2]]
print(np.where(arr > 0, 2, arr))    # only replace positives, keep the rest
# [[ 2.   2.  -0.9]
#  [-1.2  2.   2. ]]
```

### Statistical methods — and the `axis` argument

Aggregations exist as both methods (`arr.mean()`) and functions (`np.mean(arr)`). `axis=0` collapses **down the rows** (one result per column); `axis=1` collapses **across the columns** (one result per row):

```python
arr = np.array([[0., 1., 2.], [3., 4., 5.], [6., 7., 8.]])

print(arr.mean())          # 4.0        — whole array
print(arr.sum())           # 36.0
print(arr.mean(axis=1))    # [1. 4. 7.]     — mean of each ROW
print(arr.sum(axis=0))     # [ 9. 12. 15.]  — sum of each COLUMN
```

| Method | Returns | Example (on `arr` above) |
|---|---|---|
| `sum` / `mean` | total / average | `36.0` / `4.0` |
| `std` / `var` | standard deviation / variance | `2.582` / `6.667` |
| `min` / `max` | extremes | `0.0` / `8.0` |
| `argmin` / `argmax` | **index** of the extreme | `0` / `8` |
| `cumsum` / `cumprod` | running total / product (not an aggregation — full-size result) | below |

```python
print(np.arange(8).cumsum())     # [ 0  1  3  6 10 15 21 28]
print(arr.cumsum(axis=0))        # running total down each column
# [[ 0.  1.  2.]
#  [ 3.  5.  7.]
#  [ 9. 12. 15.]]
```

### Boolean arrays: count and test

`True` counts as 1, `False` as 0 — so `.sum()` **counts hits**, and `.any()`/`.all()` test them (see [Any and All](<../Core Language/Any and All.md>) for the plain-Python versions):

```python
rng = np.random.default_rng(seed=12345)
arr = rng.standard_normal(100)
print((arr > 0).sum())      # 50    — how many positive values
print((arr <= 0).sum())     # 50

bools = np.array([False, False, True, False])
print(bools.any(), bools.all())    # True False
```

### Sorting

`arr.sort()` sorts **in place** (along an axis if given); `np.sort(arr)` returns a sorted **copy** — same split as list `.sort()` vs `sorted()` in [Sorting](<../Data Structures/Sorting.md>):

```python
m = np.array([[3., 1., 2.], [6., 5., 4.]])
m.sort(axis=1)                   # sort within each row, in place
print(m)                         # [[1. 2. 3.] [4. 5. 6.]]

arr2 = np.array([5, -10, 7, 1, 0, -3])
print(np.sort(arr2))             # [-10  -3   0   1   5   7]  — copy
print(arr2)                      # [  5 -10   7   1   0  -3]  — original intact
```

### Unique values and set logic

```python
names = np.array(["Bob", "Will", "Joe", "Bob", "Will", "Joe", "Joe"])
print(np.unique(names))          # ['Bob' 'Joe' 'Will']   — sorted, deduplicated

values = np.array([6, 0, 0, 3, 2, 5, 6])
print(np.isin(values, [2, 3, 6]))   # [ True False False  True  True False  True]
```

| Function | What it does | Example → result |
|---|---|---|
| `np.unique(x)` | sorted unique elements | above |
| `np.isin(x, y)` | is each element of `x` in `y`? | above — **the book's `np.in1d` was removed in NumPy 2.0; `isin` is its replacement** *(added)* |
| `np.intersect1d(x, y)` | sorted common elements | `intersect1d([1,3,4], [3,4,5])` → `[3 4]` |
| `np.union1d(x, y)` | sorted union | `union1d([1,3], [2,3])` → `[1 2 3]` |
| `np.setdiff1d(x, y)` | in `x` but not `y` | `setdiff1d([1,2,3,4], [2,4])` → `[1 3]` |
| `np.setxor1d(x, y)` | in exactly one of the two | `setxor1d([1,2,3], [2,3,4])` → `[1 4]` |

---

## Branch 12 — Saving and Loading Arrays

NumPy's own binary format (`.npy` / `.npz`) round-trips arrays exactly:

```python
arr = np.arange(10)
np.save("some_array", arr)             # writes some_array.npy (extension auto-added)
print(np.load("some_array.npy"))       # [0 1 2 3 4 5 6 7 8 9]

np.savez("archive.npz", a=arr, b=arr * 2)    # several arrays, by keyword
arch = np.load("archive.npz")                # lazy, dict-like access
print(arch["b"])                             # [ 0  2  4  6  8 10 12 14 16 18]

np.savez_compressed("small.npz", a=arr)      # same, compressed
```

(For CSV/tabular data you'll normally reach for pandas instead.)

---

## Branch 13 — Linear Algebra

`*` multiplies element-wise — **matrix** multiplication is `@` / `np.dot`, and `numpy.linalg` holds the matrix toolbox:

```python
x = np.array([[1., 2., 3.], [4., 5., 6.]])
y = np.array([[6., 23.], [-1, 7], [8, 9]])
print(x @ y)              # (2×3) @ (3×2) → 2×2
# [[ 28.  64.]
#  [ 67. 181.]]
print(x @ np.ones(3))     # 2-D @ 1-D → 1-D:  [ 6. 15.]
```

```python
from numpy.linalg import inv, det, solve

m = np.array([[2., 1.], [1., 3.]])
print(inv(m))               # [[ 0.6 -0.2]
                            #  [-0.2  0.4]]
print(m @ inv(m))           # identity (within rounding): [[1. 0.] [-0. 1.]]
print(det(m))               # 5.000000000000001
print(solve(m, [3., 5.]))   # solves m @ x = [3, 5]  →  [0.8 1.4]
print(np.trace(m))          # 5.0  — sum of the diagonal
print(np.diag(m))           # [2. 3.]
```

| `numpy.linalg` | Computes |
|---|---|
| `inv` / `pinv` | inverse / pseudoinverse |
| `det` | determinant |
| `solve(A, b)` | solution of `A @ x = b` |
| `lstsq` | least-squares solution |
| `eig` | eigenvalues & eigenvectors |
| `qr` / `svd` | QR / singular value decomposition |
| `np.trace` / `np.diag` | diagonal sum / diagonal extraction |

---

## Branch 14 — Worked Example: Random Walks

The chapter's capstone — everything above in one exercise.

> [!example] Example — 5,000 random walks at once
> **Problem.** A walker starts at 0 and repeatedly steps +1 or −1 with equal probability. Simulate 1,000 steps; then simulate 5,000 *separate* walkers and answer: how many ever reach ±30, and how long does that take on average?
> **Setup.** Coin flips → `rng.integers(0, 2)`; flips → ±1 steps via `np.where`; positions = running total via `cumsum`.
> **Solution.**
> ```python
> nsteps = 1000
> rng = np.random.default_rng(seed=12345)
> draws = rng.integers(0, 2, size=nsteps)      # 1,000 coin flips
> steps = np.where(draws == 0, 1, -1)          # heads→+1, tails→−1
> walk = steps.cumsum()                        # position after each step
> print(walk.min(), walk.max())                # -8 50
>
> # first time the walker is 10 away from 0, in either direction:
> print((np.abs(walk) >= 10).argmax())         # 155
> # argmax returns the FIRST index of the max value — in a Boolean array
> # the max is True, so this finds the first True. (Full-scan caveat: it
> # doesn't stop early, but it's vectorized and simple.)
>
> # --- now 5,000 walks in ONE shot: a (5000, 1000) array, no loop ---
> nwalks = 5000
> rng = np.random.default_rng(seed=12345)
> draws = rng.integers(0, 2, size=(nwalks, nsteps))
> steps = np.where(draws > 0, 1, -1)
> walks = steps.cumsum(axis=1)                 # each ROW is one walker
> print(walks.max(), walks.min())              # 114 -120
>
> hits30 = (np.abs(walks) >= 30).any(axis=1)   # per row: did it ever hit ±30?
> print(hits30.sum())                          # 3395  — walkers that did
>
> crossing_times = (np.abs(walks[hits30]) >= 30).argmax(axis=1)
> print(round(crossing_times.mean(), 2))       # 500.62 steps on average
> ```
> **Answer.** With this seed: 3,395 of 5,000 walkers reach ±30, taking ≈ 500.6 steps on average to get there.
> **Insight.** The whole simulation is four array expressions — no `for` loop touches the 5,000,000 simulated steps. `where` builds the steps, `cumsum(axis=1)` walks every row at once, `any(axis=1)` filters the rows, and Boolean-`argmax` finds each row's first crossing. That is array-oriented thinking.

---

## Key Takeaways

- **Vectorize**: operate on whole arrays (`arr * 2`, `arr > 0`, `np.sqrt(arr)`) instead of looping — 10–100× faster because the work happens in C.
- Every array has a **`shape`**, a **`dtype`** (one type for all elements — convert with **`astype`**, which copies; float→int truncates), and an **`ndim`**.
- **Slices are views** — edits propagate to the original; `.copy()` when you need independence. Boolean and fancy indexing return **copies**.
- Filter with **Boolean masks** (`data[names == "Bob"]`, `arr[arr < 0] = 0`) using `&` `|` `~` — never `and`/`or`.
- **`axis=0` works down the rows, `axis=1` across the columns** — the same rule for `mean`, `sum`, `sort`, `cumsum`, `any`…
- **`np.where(cond, a, b)`** is the vectorized if/else; `(bools).sum()` counts; `any`/`all` test.
- Reproducible randomness: `rng = np.random.default_rng(seed=…)`, then `rng.integers` / `rng.standard_normal` / …
- `@` is matrix multiplication (`*` is element-wise); `numpy.linalg` has `inv`, `det`, `solve`, `eig`, `svd`.
- NumPy 2.0 renamed things the book still uses: `np.string_` → `np.bytes_`, `np.in1d` → **`np.isin`**.

---

## Exercises

Try each before expanding the solution — every answer below was verified by running the code.

> [!example] Exercise 1 — Creation and dtypes
> **Problem.** (a) Build the array `[10, 20, 30, 40, 50, 60]` and report its dtype. (b) Convert it to `float64` and compute its mean. (c) Predict the output of `np.array([9.9, -2.7, 3.5]).astype(np.int32)` — then check.
>
> > [!success]- Click to reveal solution
> > ```python
> > t = np.array([10, 20, 30, 40, 50, 60])
> > print(t.dtype)                          # int64  (inferred from the ints)
> > print(t.astype(np.float64).mean())      # 35.0
> > print(np.array([9.9, -2.7, 3.5]).astype(np.int32))   # [ 9 -2  3]
> > ```
> > **Answer.** dtype `int64`; mean `35.0`; the cast gives `[ 9 -2  3]` — `astype` **truncates toward zero** (9.9→9, −2.7→−2), it never rounds. ✓

> [!example] Exercise 2 — The view trap
> **Problem.** Without running it, predict what `a` prints:
> ```python
> a = np.arange(10)
> v = a[2:5]
> v[:] = 0
> print(a)
> ```
>
> > [!success]- Click to reveal solution
> > **Answer.** `[0 1 0 0 0 5 6 7 8 9]` ✓ — `v` is a **view** onto `a[2:5]`, so zeroing `v` zeroes positions 2–4 of `a` itself. To leave `a` alone you'd write `v = a[2:5].copy()`.

> [!example] Exercise 3 — Boolean indexing on real-ish data
> **Problem.** Given
> ```python
> names  = np.array(["Ana", "Ben", "Cai", "Dee"])
> scores = np.array([[72, 95], [51, 60], [88, 40], [65, 82]])   # [midterm, final]
> ```
> (a) Select the rows of students whose midterm ≥ 65. (b) Which *names* scored above 90 on **any** exam? (c) Produce a copy where every score below 60 is raised to 60.
>
> > [!success]- Click to reveal solution
> > ```python
> > print(scores[scores[:, 0] >= 65])        # (a) rows of Ana, Cai, Dee
> > # [[72 95]
> > #  [88 40]
> > #  [65 82]]
> > print(names[(scores > 90).any(axis=1)])  # (b) ['Ana']
> > fixed = scores.copy()
> > fixed[fixed < 60] = 60                   # (c) mask assignment
> > print(fixed)
> > # [[72 95]
> > #  [60 60]
> > #  [88 60]
> > #  [65 82]]
> > ```
> > **Answer.** (a) the three rows shown; (b) only `Ana` (her 95); (c) Ben's 51 and Cai's 40 become 60. Note `(scores > 90).any(axis=1)` — "across the columns, per row." ✓

> [!example] Exercise 4 — Fancy indexing
> **Problem.** For `g = np.arange(16).reshape(4, 4)`: (a) grab the four corner elements in one expression; (b) return the array with its first and last **rows swapped** (just those two rows, in one expression).
>
> > [!success]- Click to reveal solution
> > ```python
> > g = np.arange(16).reshape(4, 4)
> > print(g[[0, 0, -1, -1], [0, -1, 0, -1]])   # (a) [ 0  3 12 15]
> > print(g[[3, 0]])                           # (b) rows in the order 3, 0
> > # [[12 13 14 15]
> > #  [ 0  1  2  3]]
> > ```
> > **Answer.** (a) `[ 0 3 12 15]` — paired row/column index lists pick coordinates (0,0), (0,−1), (−1,0), (−1,−1). (b) passing `[3, 0]` reorders rows — fancy indexing returns rows in exactly the order you list them. ✓

> [!example] Exercise 5 — ufuncs, where, and axis statistics
> **Problem.** For `m = np.array([[4., 9., 16.], [25., 36., 49.]])`: (a) take the square root of every element; (b) replace the roots that are **even** with −1 (keep odd roots); (c) compute the column sums, the row means, and the running row-wise cumulative sum of `m`.
>
> > [!success]- Click to reveal solution
> > ```python
> > r = np.sqrt(m)
> > print(r)                                   # (a) [[2. 3. 4.] [5. 6. 7.]]
> > print(np.where(r % 2 == 0, -1, r))         # (b) [[-1.  3. -1.] [ 5. -1.  7.]]
> > print(m.sum(axis=0))                       # (c) [29. 45. 65.]     — down the columns
> > print(m.mean(axis=1))                      #     [ 9.6667 36.6667] — across each row
> > print(m.cumsum(axis=1))                    #     [[  4.  13.  29.]
> > #                                                 [ 25.  61. 110.]]
> > ```
> > **Answer.** As printed above — (b) chains a ufunc into `np.where`, and (c) is pure `axis` discipline: 0 collapses rows away, 1 collapses columns away. ✓

> [!example] Exercise 6 — Mini random-walk study
> **Problem.** Simulate **2,000 walks of 500 steps** (±1, fair coin) with `np.random.default_rng(seed=7)`. What percentage of walkers ever reach ±20, and what is the average first-crossing time among those who do?
>
> > [!success]- Click to reveal solution
> > ```python
> > rng = np.random.default_rng(seed=7)
> > steps = np.where(rng.integers(0, 2, size=(2000, 500)) == 0, 1, -1)
> > w = steps.cumsum(axis=1)
> > hit20 = (np.abs(w) >= 20).any(axis=1)
> > print(hit20.sum())                                    # 1445 walkers
> > print(round(hit20.mean() * 100, 1))                   # 72.2 %
> > print(round((np.abs(w[hit20]) >= 20).argmax(axis=1).mean(), 1))   # 237.2
> > ```
> > **Answer.** 1,445 of 2,000 walkers (**72.2%**) reach ±20, and on average they first get there after **≈237 steps**. Same four-move recipe as Branch 14: `integers` → `where` → `cumsum(axis=1)` → Boolean `any`/`argmax`. ✓

---

## Related

- **[Random Modules](<Random Modules.md>)** — Python's built-in `random`; NumPy's `default_rng` is its array-scale, reproducible cousin.
- **[Sorting](<../Data Structures/Sorting.md>)** — `list.sort()` vs `sorted()` mirrors `arr.sort()` vs `np.sort(arr)`.
- **[Any and All](<../Core Language/Any and All.md>)** — the built-in `any()`/`all()`; NumPy's are the per-axis versions.
- **[List Methods](<../Data Structures/List Methods.md>)** — where list slices *copy*, array slices are *views*: the single biggest behavioral difference.
- **[Map and Filter](<../Data Structures/Map and Filter.md>)** — ufuncs and Boolean masks are the vectorized replacements for map/filter loops.

---

### Sources

| Source | Detail | Type |
|---|---|---|
| Wes McKinney, *Python for Data Analysis*, 3rd ed. | Chapter 4 — NumPy Basics: Arrays and Vectorized Computation (pp. 83–121) | Book chapter |
| NumPy official documentation | ndarray, ufuncs, `numpy.random.Generator`, `numpy.linalg` | Library reference |
| Main-agent verification | Every code example executed on NumPy 2.5.1 / Python 3.14; outputs shown are actual; NumPy 2.0 renames (`string_`→`bytes_`, `in1d`→`isin`) flagged | — |
