# Lambda Functions

_Research compiled 2026-07-08 — Python's `lambda` (anonymous functions)_

> Part of the [Python Reference](<../Python Reference (Main).md>). A **lambda** is a tiny **unnamed** function written in a single line. It does the same thing as a normal `def` function, but it's small enough to write **right where you use it** — which is why it pairs so often with [`sorted`](<../Data Structures/Sorting.md>), [`map` and `filter`](<../Data Structures/Map and Filter.md>).

---

## Branch 1 — What a Lambda Is

Syntax: **`lambda arguments: expression`**. It takes some arguments, evaluates one expression, and **returns that result automatically** (no `return` keyword).

```python
square = lambda x: x * x
print(square(5))       # 25
```

That lambda is exactly equivalent to this normal function:

```python
def square(x):
    return x * x
```

Same behaviour — `lambda` is just a compact way to write a one-expression function.

---

## Branch 2 — The Forms

```python
add   = lambda a, b: a + b       # multiple arguments
print(add(3, 4))                 # 7

greet = lambda: 'hi'             # no arguments
print(greet())                   # hi

power = lambda base, exp=2: base ** exp   # default arguments work
print(power(3), power(3, 3))     # 9 27
```

You can even use a **conditional expression** in the body (but not full `if`/`for` statements):

```python
sign = lambda n: 'positive' if n > 0 else 'non-positive'
print(sign(5), sign(-1))         # positive non-positive
```

> [!warning] The body must be a single EXPRESSION
> A lambda can only hold **one expression** — no statements, no assignments, no loops, no multiple lines. If your logic needs any of those, write a normal `def` function instead. `lambda` is for *small* things.

---

## Branch 3 — Where Lambdas Actually Shine

You rarely assign a lambda to a name (if you're naming it, just use `def`). Their real purpose is to be passed **inline** to functions that take a function argument — especially `key=`.

```python
# sort a list of tuples by the 2nd item
pairs = [('a', 3), ('b', 1), ('c', 2)]
print(sorted(pairs, key=lambda p: p[1]))       # [('b', 1), ('c', 2), ('a', 3)]

# longest string
print(max(['aa', 'b', 'ccc'], key=lambda s: len(s)))   # 'ccc'

# transform / filter a list
print(list(map(lambda x: x * 10, [1, 2, 3])))          # [10, 20, 30]
print(list(filter(lambda x: x > 0, [-1, 2, -3, 4])))   # [2, 4]
```

Read `key=lambda p: p[1]` as *"for each item `p`, use `p[1]` as the sort key."* The lambda is a throwaway function you define exactly where it's needed and never reuse.

---

## Branch 4 — Lambda vs. `def`: which to use

| | `lambda` | `def` |
|---|---|---|
| Has a name? | No (anonymous) | Yes |
| Body | one **expression** only | any number of statements |
| Auto-returns? | Yes | No — needs `return` |
| Best for | a short function passed **inline** (`key=`, `map`, `filter`) | anything reusable, named, or multi-line |

> [!tip] Rule of thumb
> If you're about to write `name = lambda ...`, just use `def name(...)` instead — it's clearer and shows a real name in tracebacks. Save `lambda` for the inline `key=` / `map` / `filter` cases where a named function would be overkill.

---

## Key Takeaways

- A **lambda** is an anonymous one-line function: **`lambda args: expression`** — it auto-returns the expression's value.
- It's equivalent to a `def` that just `return`s one expression; the body must be a **single expression** (a conditional expression is allowed, but no statements/loops).
- Its real use is **inline**, passed to `key=` (in `sorted`/`max`/`min`), `map`, and `filter`.
- If you'd **name** it or it needs **multiple lines**, use **`def`** instead.

---

## Exercises

> [!example] Exercise 1 — Sort names by their last letter
> **Problem.** Sort `['Ann', 'Bob', 'Cy']` by each name's **last character**. Print the result.
>
> > [!success]- Click to reveal solution
> > **Solution.** A lambda picks the last character (`name[-1]`) as the sort key.
> > ```python
> > names = ['Ann', 'Bob', 'Cy']
> > print(sorted(names, key=lambda name: name[-1]))
> > ```
> > **Answer.** `['Bob', 'Ann', 'Cy']` ✓ (sorted by 'b', 'n', 'y')

> [!example] Exercise 2 — Double every number with map
> **Problem.** Use `map()` with a lambda to double every number in `[3, 5, 8]`, and print the result as a list.
>
> > [!success]- Click to reveal solution
> > **Solution.** The lambda `lambda x: x * 2` is applied to each item.
> > ```python
> > print(list(map(lambda x: x * 2, [3, 5, 8])))
> > ```
> > **Answer.** `[6, 10, 16]` ✓

---

### Sources

| Source | Date | Type |
|---|---|---|
| Python — official tutorial, "Lambda Expressions" | 2026 | Language reference |
| Verified against Python 3.14 on `E:\Python` | 2026-07-08 | Local test |
