# The Logging Module

_Research compiled 2026-06-30 — Python standard library (`logging` module), based on Automate the Boring Stuff Ch. 5_

> Companion to [Random Modules](<Random Modules.md>). **`logging`** is Python's built-in way to record timestamped messages about what your program is doing — a smarter replacement for scattering `print()` calls when you're debugging.

---

## Branch 1 — What `logging` Does

As a program runs, you often want to know *what it's doing and when* — which values it computed, which branch it took, where it failed. You could use `print()`, but those messages clutter your real output and have to be deleted by hand afterward.

The `logging` module solves this. It lets you record **log messages** that:

- carry a **timestamp** automatically,
- are tagged with a **severity level** (so you can filter by importance),
- can be **turned off with a single line** instead of deleting code,
- can be **redirected to a file** without changing the rest of your program.

```python
import logging

logging.basicConfig(level=logging.DEBUG,
                    format=' %(asctime)s - %(levelname)s - %(message)s',
                    force=True)

logging.debug('Program started')        # a log message
logging.debug('Still running fine')
```

> [!tip] Why logging beats `print()` for debugging
> Fill your program with as many log messages as you like — then disable them all at once when you're done. They never have to be hunted down and deleted, and they stay out of your program's real output.

| | `print()` | `logging` |
|---|---|---|
| Timestamps | No | Yes, automatic |
| Severity levels | No | Five levels |
| Turn off easily | Delete each one | One line |
| Send to a file | Manual | `filename=` argument |

---

## Branch 2 — Setting It Up With `basicConfig()`

Put this near the top of your program. `basicConfig()` decides **what to show** and **how to format it**.

```python
import logging

logging.basicConfig(level=logging.DEBUG,
                    format=' %(asctime)s - %(levelname)s - %(message)s',
                    force=True)
```

- **`level=logging.DEBUG`** — show messages of this level *and above*. DEBUG is the lowest, so this shows everything.
- **`format=...`** — the layout of each line, built from these placeholders:

| Placeholder | Shows |
|---|---|
| `%(asctime)s` | Date and time the message was logged |
| `%(levelname)s` | The level (DEBUG, INFO, …) |
| `%(message)s` | The text you passed in |

A logged line then looks like:

```text
 2026-06-30 19:50:48,650 - DEBUG - Program started
```

> [!warning] Call `basicConfig()` only once
> `basicConfig()` configures logging a single time — a second call is normally **ignored**. The Obsidian Execute Code plugin reuses one Python process per note, so each runnable block here adds **`force=True`** to reconfigure cleanly. In a normal program you call `basicConfig()` once at the top and can drop `force=True`.

---

## Branch 3 — The Five Logging Levels

Every message has a level. From least to most severe:

| Level | Function | When to use it |
|---|---|---|
| **DEBUG** | `logging.debug()` | Small details, only interesting when diagnosing a problem |
| **INFO** | `logging.info()` | General events — confirming the program is working at a given point |
| **WARNING** | `logging.warning()` | A potential problem that doesn't stop the program *yet* |
| **ERROR** | `logging.error()` | An error that caused the program to fail at something |
| **CRITICAL** | `logging.critical()` | A fatal error that has stopped, or is about to stop, the program |

```python
import logging
logging.basicConfig(level=logging.DEBUG,
                    format=' %(asctime)s - %(levelname)s - %(message)s',
                    force=True)

logging.debug('Detailed value: x = 5')
logging.info('Halfway through the file')
logging.warning('Disk is 90% full')
logging.error('Could not open config.txt')
logging.critical('Out of memory — shutting down')
```

### Levels act as a filter

The `level=` you set in `basicConfig()` is a **threshold** — anything *below* it is silently ignored. Raise the threshold to hide the noisy low-level messages.

```python
import logging
logging.basicConfig(level=logging.WARNING,   # only WARNING and above
                    format=' %(levelname)s - %(message)s',
                    force=True)

logging.debug('You will NOT see this')      # below the threshold
logging.info('You will NOT see this either')
logging.warning('But you WILL see this')    # WARNING and up get through
```

---

## Branch 4 — Logging to a File

To save log messages to a file instead of showing them on screen, add the **`filename`** argument. Everything else works the same.

```python
import logging
logging.basicConfig(filename='myProgramLog.txt',
                    level=logging.DEBUG,
                    format=' %(asctime)s - %(levelname)s - %(message)s',
                    force=True)

logging.debug('This line goes into myProgramLog.txt, not the screen')
```

This is ideal for programs that run unattended — you can read the log file afterward to see exactly what happened.

---

## Branch 5 — Disabling Logging

When you're done debugging, you don't delete your log calls — you **switch them off**. `logging.disable()` suppresses every message at the given level *and below*. Passing `CRITICAL` (the highest) silences everything.

```python
import logging
logging.basicConfig(level=logging.DEBUG,
                    format=' %(levelname)s - %(message)s',
                    force=True)

logging.disable(logging.CRITICAL)   # silence ALL log messages

logging.critical('Even this is hidden now')   # nothing prints
```

Put this line just after your `import logging` so it's easy to comment out and back in.

---

## Key Takeaways

- **`logging`** records timestamped, severity-tagged messages about what your program is doing — a cleaner, switch-off-able replacement for `print()` debugging.
- Configure it once with **`logging.basicConfig(level=..., format=...)`**; the format string uses `%(asctime)s`, `%(levelname)s`, and `%(message)s`.
- Five levels, low to high: **DEBUG → INFO → WARNING → ERROR → CRITICAL**. The `level=` you set is a threshold — anything below it is hidden.
- Add **`filename='...'`** to send logs to a file instead of the screen.
- **`logging.disable(logging.CRITICAL)`** switches off all logging in one line — no need to delete your log calls.
- In Obsidian's runner, add **`force=True`** to `basicConfig()` so each block reconfigures.

---

### Sources

| Source | Date | Type |
|---|---|---|
| Automate the Boring Stuff, 3e — Chapter 5 (Logging) | 2026 | Book chapter |
| Python `logging` — official CPython documentation | 2026 | Standard library reference |
