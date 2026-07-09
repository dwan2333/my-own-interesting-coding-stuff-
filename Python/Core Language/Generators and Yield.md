# Generators and `yield`

_Research compiled 2026-07-08 — Python generators and the `yield` keyword_

> Part of the [Python Reference](<../Python Reference (Main).md>). A **generator** is a function that produces a **stream of values one at a time**, instead of building them all and returning a list. The magic word is **`yield`**: it hands back a value and **pauses** the function, resuming right where it left off on the next request. This makes generators **lazy** and **memory-light** — the same trait behind [`enumerate`](<../Data Structures/The Enumerate Function.md>), [`zip`](<../Data Structures/The Zip Function.md>), and [`map`](<../Data Structures/Map and Filter.md>).

---

## Branch 1 — `yield` Turns a Function Into a Generator

Any function that contains `yield` becomes a **generator function**. Calling it doesn't run the body — it hands you a **generator object** that runs on demand.

```python
def count_up_to(n):
    i = 1
    while i <= n:
        yield i        # hand back i, then PAUSE here until asked again
        i += 1

gen = count_up_to(3)
print(type(gen).__name__)   # generator   — nothing has run yet
print(list(gen))            # [1, 2, 3]    — now it runs, producing values
```

**`yield` vs `return`:** `return` ends the function and gives back **one** value. `yield` gives back a value but **freezes** the function in place; the next request thaws it and continues after the `yield`.

---

## Branch 2 — Getting Values Out

You pull values with `next()`, or (far more common) just **loop** over it.

```python
def count_up_to(n):
    i = 1
    while i <= n:
        yield i
        i += 1

# one at a time with next()
g = count_up_to(3)
print(next(g))   # 1
print(next(g))   # 2

# the normal way — a for loop
for x in count_up_to(3):
    print(x)     # 1 / 2 / 3
```

When the function ends, the generator is **exhausted** and raises **`StopIteration`** — which a `for` loop catches automatically to stop cleanly (the same signal you saw in the DSA iterator note).

```python
def two():
    yield 'a'
    yield 'b'

t = two()
next(t); next(t)
next(t)          # StopIteration — nothing left
```

> [!warning] Generators are single-use
> Once you loop through a generator (or call `list()` on it), it's **used up** — looping again yields nothing. Call the generator function again to get a fresh one.

---

## Branch 3 — Why Bother? Laziness Saves Memory

A generator produces values **on demand**, so it never has to hold them all at once. This lets you work with huge — even infinite — sequences.

```python
def big():
    for i in range(1_000_000_000):
        yield i          # a billion values, but only ONE exists at a time

g = big()
print(next(g), next(g), next(g))   # 0 1 2  — instant; no billion-item list built
```

A **list** version (`return [i for i in range(1_000_000_000)]`) would try to build the whole billion-item list in memory first — slow and likely to crash. The generator just streams.

> [!tip] The rule of thumb
> If you're going to loop over results **once** and don't need them all in memory, a generator is the efficient choice — especially for big files, large ranges, or pipelines. If you need the full collection (to index it, sort it, reuse it), build a list.

---

## Branch 4 — Generator Expressions (the one-liner form)

For simple cases you don't even need a function. A **generator expression** looks like a [list comprehension](<../Data Structures/Map and Filter.md>) but with **parentheses** instead of brackets — and it's lazy.

```python
squares = (x * x for x in range(5))   # () not []  → a generator, not a list
print(type(squares).__name__)         # generator
print(list(squares))                  # [0, 1, 4, 9, 16]
```

The big win is feeding one straight into a function like `sum()`, `max()`, or `any()` — no intermediate list is built:

```python
print(sum(x * x for x in range(1000)))   # 332833500  — memory-light
```

| Form | Syntax | Result |
|---|---|---|
| List comprehension | `[x*x for x in xs]` | a **list** (all values in memory) |
| Generator expression | `(x*x for x in xs)` | a **lazy generator** (one at a time) |

---

## Key Takeaways

- A function with **`yield`** is a **generator**: `yield` returns a value **and pauses**, resuming where it left off on the next request.
- Get values with **`next()`** or a **`for` loop**; a finished generator raises **`StopIteration`** (loops handle this for you). Generators are **single-use**.
- Generators are **lazy** — they produce values one at a time, so they use little memory and can handle huge/infinite sequences.
- A **generator expression** `(expr for x in xs)` is the one-line form — like a list comprehension with `()`; great fed directly into `sum`/`max`/`any`.
- Use a **generator** to stream results once; use a **list** when you need them all at once (to index, sort, or reuse).

---

## Exercises

> [!example] Exercise 1 — Yield the even numbers
> **Problem.** Write a generator function `evens(n)` that yields the even numbers from 0 up to (not including) `n`. Print `list(evens(10))`.
>
> > [!success]- Click to reveal solution
> > **Solution.** Loop and `yield` only when the number is even.
> > ```python
> > def evens(n):
> >     for i in range(n):
> >         if i % 2 == 0:
> >             yield i
> > print(list(evens(10)))
> > ```
> > **Answer.** `[0, 2, 4, 6, 8]` ✓

> [!example] Exercise 2 — Sum of squares without a list
> **Problem.** Using a **generator expression**, compute the sum of the squares of 1 through 5 (i.e. 1+4+9+16+25) in one line.
>
> > [!success]- Click to reveal solution
> > **Solution.** Feed a generator expression straight into `sum()` — no list built.
> > ```python
> > print(sum(x * x for x in range(1, 6)))
> > ```
> > **Answer.** `55` ✓

---

### Sources

| Source | Date | Type |
|---|---|---|
| Python — official tutorial, "Generators" & "Generator Expressions" | 2026 | Language reference |
| Verified against Python 3.14 on `E:\Python` | 2026-07-08 | Local test |
