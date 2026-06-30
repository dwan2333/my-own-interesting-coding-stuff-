# The Traceback Module

_Research compiled 2026-06-30 — Python standard library (`traceback` module)_

> Companion to [Random Modules](<Random Modules.md>). Where `logging` records *that* something went wrong, **`traceback`** records the *full story* of how — the chain of calls and the exact line that raised the error.

---

## Branch 1 — The Problem It Solves

When you catch an exception with `try`/`except`, Python normally prints a **traceback** (the error report) and stops. But once *you* catch it, that detailed report disappears — you only get whatever message you wrote.

```python
try:
    result = 10 / 0
except ZeroDivisionError:
    print("Something broke")   # but WHERE? WHY? we lost the details
```

Output: just `Something broke`. You've thrown away the most useful debugging info — the line number and the exception chain. `traceback` (and logging's built-in support for it) gets it back.

---

## Branch 2 — Core Syntax

| Function | What it does | Returns |
|---|---|---|
| `traceback.print_exc()` | Prints the current exception's traceback to the screen (stderr) | `None` |
| `traceback.format_exc()` | Returns the traceback as a **string** — so you can log it or save it | `str` |
| `traceback.print_exception(e)` | Prints the traceback for a specific exception object | `None` |

### `traceback.print_exc()` — see the full error without crashing

```python
import traceback

try:
    eggs = [1, 2, 3]
    print(eggs[10])              # IndexError
except IndexError:
    print("Caught it — here is the full traceback:")
    traceback.print_exc()        # prints file, line number, and the error
```

### `traceback.format_exc()` — capture the traceback as text

This is the key one: it gives you the traceback as a **string**, so you can write it to a log file or a variable instead of just the screen.

```python
import traceback

try:
    10 / 0
except ZeroDivisionError:
    error_text = traceback.format_exc()   # the whole traceback, as a string
    print("Saved this to a variable:")
    print(error_text)
```

> [!tip] Why `format_exc()` matters
> `print_exc()` only *shows* the error. `format_exc()` *hands it to you* as data — which is exactly what you need to feed into a log file, an email alert, or a crash report.

---

## Branch 3 — Where It Meets `logging`

This is the payoff. Instead of stitching `traceback` and `logging` together by hand, the `logging` module has built-in ways to attach a full traceback to a log message.

### Option A — `logging.exception()` (the easy way)

Call it **inside an `except` block**. It logs at **ERROR** level *and* automatically appends the full traceback. No `traceback` import needed.

```python
import logging
logging.basicConfig(level=logging.DEBUG,
                    format=' %(asctime)s - %(levelname)s - %(message)s',
                    force=True)

try:
    10 / 0
except ZeroDivisionError:
    logging.exception("Division failed")   # logs message + full traceback
```

### Option B — `exc_info=True` (works with any level)

Add `exc_info=True` to any logging call to attach the traceback. Useful when you want it at, say, **CRITICAL** instead of ERROR.

```python
import logging
logging.basicConfig(level=logging.DEBUG,
                    format=' %(asctime)s - %(levelname)s - %(message)s',
                    force=True)

try:
    10 / 0
except ZeroDivisionError:
    logging.critical("Fatal math error", exc_info=True)
```

### Option C — feed `format_exc()` in manually

When you want full control over the text (e.g. combine it with other info before logging):

```python
import logging, traceback
logging.basicConfig(filename='errors.log', level=logging.ERROR,
                    format=' %(asctime)s - %(levelname)s - %(message)s',
                    force=True)

try:
    10 / 0
except ZeroDivisionError:
    logging.error("Math broke:\n%s", traceback.format_exc())
```

| Approach | Best when |
|---|---|
| `logging.exception("msg")` | You're in an `except` block and want the default ERROR level — simplest |
| `logging.error("msg", exc_info=True)` | You want a traceback at a specific level |
| `traceback.format_exc()` | You need the traceback as a string to reshape, store, or send |

> [!warning] `force=True` in `basicConfig`
> `basicConfig()` only configures logging **once** — a second call is silently ignored. The Execute Code plugin reuses one Python process per note, so without `force=True` your later blocks would keep the first block's settings. `force=True` (Python 3.8+) makes each block reconfigure cleanly. Outside Obsidian you usually call `basicConfig()` just once at the top of your program and can drop `force=True`.

---

## Branch 4 — How to Read a Traceback

A traceback is read **bottom-up**: the last line is the actual error; the lines above trace the calls that led there.

```text
Traceback (most recent call last):
  File "demo.py", line 9, in <module>
    main()
  File "demo.py", line 5, in main
    return 10 / divisor
ZeroDivisionError: division by zero        <-- the real error is here
```

- **Bottom line** = the exception type and message (`ZeroDivisionError: division by zero`).
- **Lines above** = the call chain (`main()` was called, which ran `10 / divisor`).
- **Line numbers** point you straight to the code to fix.

---

## Key Takeaways

- **`logging`** tells you *something* failed; **`traceback`** tells you *exactly what and where*.
- **`traceback.print_exc()`** shows the full error without crashing; **`traceback.format_exc()`** returns it as a **string** you can log or save.
- The cleanest combo is **`logging.exception("msg")`** inside an `except` block — message + full traceback in one call.
- Use **`exc_info=True`** to attach a traceback to any level (e.g. `logging.critical(..., exc_info=True)`).
- Read tracebacks **bottom-up**: the last line is the real error.
- In Obsidian's runner, add **`force=True`** to `basicConfig()` so each block reconfigures.

---

### Sources

| Source | Date | Type |
|---|---|---|
| Automate the Boring Stuff, 3e — Chapter 5 (Logging) | 2026 | Book chapter |
| Python `traceback` — official CPython documentation | 2026 | Standard library reference |
| Python `logging` — official CPython documentation | 2026 | Standard library reference |
