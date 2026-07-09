# Exceptions — try / except / else / finally

_Research compiled 2026-07-08 — Python exception handling, focused on `finally`_

> Part of the [Python Reference](<../Python Reference (Main).md>). Companion to [The Assert Statement](<The Assert Statement.md>) and [The Logging Module](<The Logging Module.md>). When code hits an error it normally **crashes**. A **`try`/`except`** block lets you **catch** the error and keep running; **`finally`** adds cleanup that runs **no matter what**.

---

## Branch 1 — `try` / `except`: catch an error

Put risky code in `try`; handle the failure in `except`. If the risky line raises an error, Python jumps straight to the matching `except` instead of crashing.

```python
try:
    x = 10 / 0
except ZeroDivisionError:
    print("caught division by zero")
# program keeps running instead of crashing
```

### Catch a specific error and read it

Name the exception type, and grab the error object with `as e`:

```python
try:
    int("hello")
except ValueError as e:
    print("ValueError:", e)   # invalid literal for int() with base 10: 'hello'
```

> [!warning] Catch specific exceptions, not everything
> A bare `except:` (or `except Exception:`) swallows *every* error — including typos and bugs you'd want to see. Catch the **specific** type you expect (`ValueError`, `FileNotFoundError`, …) so real problems still surface.

---

## Branch 2 — Multiple `except` blocks

List several handlers; Python runs the **first one that matches** the error type.

```python
def parse(v):
    try:
        return 10 / int(v)
    except ValueError:
        return "not a number"
    except ZeroDivisionError:
        return "cannot divide by zero"

print(parse("5"))   # 2.0
print(parse("x"))   # not a number
print(parse("0"))   # cannot divide by zero
```

---

## Branch 3 — `else`: runs only if there was NO error

The optional `else` block runs **when the `try` succeeded** (no exception). It keeps the "success path" out of the `try`, so you're not accidentally catching errors from it.

```python
try:
    n = int("42")
except ValueError:
    print("bad input")
else:
    print("parsed fine, n =", n)   # else ran, n = 42
```

---

## Branch 4 — `finally`: runs NO MATTER WHAT

The `finally` block **always** runs when the `try` finishes — whether it succeeded, raised a caught error, raised an *uncaught* error, or even hit a `return`. It's for **cleanup** that must happen either way (closing a file, releasing a lock, disconnecting).

```python
def demo(x):
    try:
        return 10 / x
    except ZeroDivisionError:
        return "div0"
    finally:
        print("  finally ran (cleanup)")   # prints on BOTH paths

print(demo(2))    # finally ran (cleanup)  →  5.0
print(demo(0))    # finally ran (cleanup)  →  div0
```

### It even runs before a `return`

If the `try` (or `except`) hits a `return`, Python **still runs `finally` first**, then returns:

```python
def f():
    try:
        return "from try"
    finally:
        print("  finally runs before the return happens")

print(f())
#   finally runs before the return happens
# from try
```

> [!tip] What `finally` is for — guaranteed cleanup
> Use `finally` for the "always do this" step: `file.close()`, releasing a resource, resetting state. Because it runs even when an error propagates uncaught, your cleanup never gets skipped by a crash.
>
> **But for files, prefer [`with`](<../Files and Paths/File Open Modes.md>)** — a `with` block closes the file for you automatically, which is `try`/`finally` done for you behind the scenes.

---

## Branch 5 — Raising Exceptions Yourself

Use `raise` to signal an error on purpose — e.g. to reject bad input:

```python
def check_age(age):
    if age < 0:
        raise ValueError("age cannot be negative")
    return age

try:
    check_age(-5)
except ValueError as e:
    print("raised:", e)   # raised: age cannot be negative
```

- `raise ValueError("message")` — raise a specific exception with a message.
- Inside an `except`, a bare `raise` **re-raises** the current error (handle it partly, then let it propagate).
- Pair this with [logging](<The Logging Module.md>): `logging.exception("...")` inside an `except` records the full traceback.

---

## The full shape

```python
try:
    ...        # risky code
except SomeError as e:
    ...        # runs if that error happened
else:
    ...        # runs if NO error happened
finally:
    ...        # ALWAYS runs (cleanup)
```

Order is fixed: `try` → `except`(s) → `else` → `finally`. Only `try` plus **one** of `except`/`finally` is required; `else` and extra `except`s are optional.

---

## Key Takeaways

- **`try`/`except`** catches an error so the program keeps running; catch a **specific** exception type and read it with **`as e`**.
- Multiple **`except`** blocks handle different error types; the first matching one runs.
- **`else`** runs only when the `try` raised **no** error (keeps the success path uncaught).
- **`finally` always runs** — success, handled error, uncaught error, or `return` — making it the place for guaranteed **cleanup**. (For files, prefer **`with`**.)
- **`raise SomeError("msg")`** signals an error yourself; a bare **`raise`** inside `except` re-raises the current one.

---

## Exercises

> [!example] Exercise 1 — Safe division
> **Problem.** Write `safe_div(a, b)` that returns `a / b`, but returns the string `"undefined"` if `b` is 0. Test it on `(10, 2)` and `(10, 0)`.
>
> > [!success]- Click to reveal solution
> > **Solution.** Catch `ZeroDivisionError` and return the fallback.
> > ```python
> > def safe_div(a, b):
> >     try:
> >         return a / b
> >     except ZeroDivisionError:
> >         return "undefined"
> > print(safe_div(10, 2), safe_div(10, 0))
> > ```
> > **Answer.** `5.0 undefined` ✓

> [!example] Exercise 2 — Guaranteed cleanup message
> **Problem.** Write a function that tries to convert a value with `int(value)` and returns it, catches `ValueError` returning `-1`, and **always** prints `"done"` at the end (even on the error path). Test on `"42"` and `"oops"`.
>
> > [!success]- Click to reveal solution
> > **Solution.** Put the "always" step in `finally`.
> > ```python
> > def to_int(value):
> >     try:
> >         return int(value)
> >     except ValueError:
> >         return -1
> >     finally:
> >         print("done")
> > print(to_int("42"))     # done → 42
> > print(to_int("oops"))   # done → -1
> > ```
> > **Answer.** prints `done` both times; returns `42` then `-1` ✓

---

### Sources

| Source | Date | Type |
|---|---|---|
| Python — official tutorial, "Errors and Exceptions" | 2026 | Language reference |
| Verified against Python 3.14 on `E:\Python` | 2026-07-08 | Local test |
