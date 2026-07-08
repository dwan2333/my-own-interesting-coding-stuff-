# Star Parameters — `*args` and `**kwargs`

_Research compiled 2026-07-07 — Python `*` / `**` in function parameters and calls_

> Part of the [Python Reference](<../Python Reference (Main).md>). The `*` and `**` symbols do **three different jobs** depending on where they appear — collecting arguments in a function definition, unpacking a collection at a call, or forcing keyword-only arguments. The names `args`/`kwargs` are just convention; the `*` and `**` are what matter.

---

## Branch 1 — In a Definition: Collect Extra Arguments

### `*args` — gather extra *positional* arguments into a **tuple**

Lets a function accept **any number** of positional arguments without listing them.

```python
def total(*args):
    return sum(args)          # args is a tuple, e.g. (1, 2, 3, 4)

print(total(1, 2, 3, 4))     # 10
print(total(5, 5))           # 10
```

### `**kwargs` — gather extra *keyword* arguments into a **dict**

```python
def show(**kwargs):
    return kwargs             # kwargs is a dict, e.g. {'a': 1, 'b': 2}

print(show(a=1, b=2))        # {'a': 1, 'b': 2}
```

---

## Branch 2 — In a Call: Unpack a Collection

The **same symbols** do the reverse at the call site — they spread a collection *into* separate arguments.

```python
def total(*args):
    return sum(args)

nums = [10, 20, 30]
print(total(*nums))          # same as total(10, 20, 30) → 60

def show(**kwargs):
    return kwargs

info = {'a': 9, 'b': 8}
print(show(**info))          # same as show(a=9, b=8)
```

- `*` spreads a **list/tuple** into positional arguments.
- `**` spreads a **dict** into keyword arguments (keys become argument names).

> [!tip] Definition collects, call spreads
> Think of it as a funnel that works both ways: in a **definition**, `*`/`**` *pack* many arguments into one variable; in a **call**, they *unpack* one collection back into many arguments.

---

## Branch 3 — A Bare `*`: Force Keyword-Only Arguments

A `*` on its own (not attached to a name) means *"everything after me must be passed **by name**."*

```python
def make(name, *, color='red'):
    return f'{name}/{color}'

print(make('car', color='blue'))   # OK — passed by name
# make('car', 'blue')              # TypeError: color is keyword-only
```

This is a readability guard: it stops callers from writing mystery positional values like `make('car', 'blue', True)` and forces the clearer `color='blue'`.

---

## Branch 4 — Putting Them Together

The full order in a definition is: **normal parameters → `*args` → `**kwargs`.**

```python
def describe(label, *args, **kwargs):
    return f'{label} | args={args} | kwargs={kwargs}'

print(describe('x', 1, 2, a=3, b=4))
# x | args=(1, 2) | kwargs={'a': 3, 'b': 4}
```

The classic real-world use is a **wrapper** that accepts anything and forwards it unchanged — you collect with `*args, **kwargs`, then pass them on by unpacking with `*args, **kwargs`:

```python
def logged(func):
    def inner(*args, **kwargs):          # collect whatever was passed
        print('calling with', args, kwargs)
        return func(*args, **kwargs)     # forward it unchanged
    return inner

@logged
def add(a, b):
    return a + b

print(add(2, 3))
# calling with (2, 3) {}
# 5
```

---

## Quick Reference

| Where it appears | `*` | `**` |
|---|---|---|
| **Definition** | collect extra **positional** args → tuple (`*args`) | collect extra **keyword** args → dict (`**kwargs`) |
| **Call** | unpack a list/tuple into positional args (`f(*nums)`) | unpack a dict into keyword args (`f(**d)`) |
| **Bare `*`** | everything after it is **keyword-only** | — |

---

## Exercises

Try each first, then reveal the solution.

> [!example] Exercise 1 — Average of any number of values
> **Problem.** Write a function `average(*nums)` that returns the mean of however many numbers are passed. `average(2, 4, 6)` should give `4.0`.
>
> > [!success]- Click to reveal solution
> > **Solution.** `*nums` collects all positional arguments into a tuple; divide the sum by the count.
> > ```python
> > def average(*nums):
> >     return sum(nums) / len(nums)
> > print(average(2, 4, 6))
> > ```
> > **Answer.** `4.0` ✓

> [!example] Exercise 2 — Unpack a list into a function
> **Problem.** You have `point = [3, 4]` and a function `def dist(x, y): return (x**2 + y**2) ** 0.5`. Call `dist` using the list without writing `point[0]`, `point[1]`.
>
> > [!success]- Click to reveal solution
> > **Solution.** Spread the list into positional arguments with `*`.
> > ```python
> > def dist(x, y):
> >     return (x**2 + y**2) ** 0.5
> > point = [3, 4]
> > print(dist(*point))
> > ```
> > **Answer.** `5.0` ✓

> [!example] Exercise 3 — Collect keyword arguments
> **Problem.** Write `tag(**attrs)` that turns keyword arguments into an HTML-ish string. `tag(id='x', cls='big')` should give `id="x" cls="big"`.
>
> > [!success]- Click to reveal solution
> > **Solution.** `**attrs` collects the keyword arguments into a dict; loop its `.items()`.
> > ```python
> > def tag(**attrs):
> >     return ' '.join(f'{k}="{v}"' for k, v in attrs.items())
> > print(tag(id='x', cls='big'))
> > ```
> > **Answer.** `id="x" cls="big"` ✓

---

### Sources

| Source | Date | Type |
|---|---|---|
| Python — official tutorial, "More on Defining Functions" | 2026 | Language reference |
| Verified against Python 3.14 on `E:\Python` | 2026-07-07 | Local test |
