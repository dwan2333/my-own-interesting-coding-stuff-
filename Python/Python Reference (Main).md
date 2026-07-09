# Python Reference

_A growing, example-driven reference on Python — every method and function has a runnable, verified example (tested against `E:\Python`). Built alongside Automate the Boring Stuff (3e) and Python for Data Analysis._

> This is the **index**. Notes are grouped into folders by theme. Each note runs directly in the Obsidian Execute Code plugin.

---

## Core Language

- **[Star Parameters - args and kwargs](<Core Language/Star Parameters - args and kwargs.md>)** — what `*` and `**` do in function parameters and calls.
- **[Classes and OOP](<Core Language/Classes and OOP.md>)** — classes, instances, `__init__`/`self`, inheritance, composition, `__str__`.
- **[Any and All](<Core Language/Any and All.md>)** — the `any()` / `all()` built-ins for testing a condition across a collection.
- **[Lambda Functions](<Core Language/Lambda Functions.md>)** — one-line anonymous functions for inline use with `key=`/`map`/`filter`.
- **[Generators and Yield](<Core Language/Generators and Yield.md>)** — `yield` for lazy, memory-light streams of values.

---

## Data Structures

- **[List Methods](<Data Structures/List Methods.md>)** — all 11 `list` methods (`append`, `extend`, `pop`, `sort`, …).
- **[Dictionary Methods](<Data Structures/Dictionary Methods.md>)** — all 11 `dict` methods (`get`, `setdefault`, `update`, `pop`, …).
- **[The Enumerate Function](<Data Structures/The Enumerate Function.md>)** — pairing items with their index in a loop; what's iterable.
- **[Tuples](<Data Structures/Tuples.md>)** — the immutable sequence: packing/unpacking, when to use vs. a list.
- **[Sorting](<Data Structures/Sorting.md>)** — the `sorted()` function and `.sort()` method: `key`, `reverse`, stability.
- **[The Zip Function](<Data Structures/The Zip Function.md>)** — pairing several iterables together to loop over them at once.
- **[Sets](<Data Structures/Sets.md>)** — unordered collection of unique items: dedup, membership, and set math.
- **[Map and Filter](<Data Structures/Map and Filter.md>)** — the `map()` / `filter()` built-ins for transforming and filtering iterables.

---

## Strings and Text

- **[String Formatting and Methods](<Strings and Text/String Formatting and Methods.md>)** — f-strings, `%s`, `.format()`, and the `str` methods.
- **[Escape Sequences](<Strings and Text/Escape Sequences.md>)** — `\n`, `\t`, quotes, raw strings, Unicode escapes.
- **[The ord and chr Functions](<Strings and Text/The ord and chr Functions.md>)** — characters ↔ Unicode code points.
- **[The Regex Module](<Strings and Text/The Regex Module.md>)** — `re`: search methods, groups, `\d`/`\w`/`\s`, lookaround, flags.

---

## Files and Paths

- **[Pathlib - Building and Inspecting Paths](<Files and Paths/Pathlib - Building and Inspecting Paths.md>)** — constructing paths and reading their parts.
- **[Pathlib - File System Operations](<Files and Paths/Pathlib - File System Operations.md>)** — reading, writing, listing, creating, deleting files.
- **[File Open Modes](<Files and Paths/File Open Modes.md>)** — `open()` modes: `r`/`w`/`a`/`x`/`b`/`+` and `'w'` vs `'a'`.

---

## Debugging

- **[The Assert Statement](<Debugging/The Assert Statement.md>)** — sanity-check tripwires for catching bugs early.
- **[The Logging Module](<Debugging/The Logging Module.md>)** — recording timestamped messages about what your program does.
- **[Exceptions - try except finally](<Debugging/Exceptions - try except finally.md>)** — catching errors with `try`/`except`, and guaranteed cleanup with `finally`.

---

## Modules and Libraries

- **[Random Modules](<Modules and Libraries/Random Modules.md>)** — the `random` module: floats, ints, sequences, distributions.
- **[The Datetime Module](<Modules and Libraries/The Datetime Module.md>)** — dates, times, durations, and text ↔ date conversion.
- **[The Itertools Module](<Modules and Libraries/The Itertools Module.md>)** — lazy iterator tools: chain, islice, groupby, combinations, product.
- **[The Collections Module](<Modules and Libraries/The Collections Module.md>)** — `Counter`, `defaultdict`, `namedtuple`, `deque`, `OrderedDict`.
- **[The Pyperclip Module](<Modules and Libraries/The Pyperclip Module.md>)** — reading and writing the system clipboard.
- **[The Yfinance Library](<Modules and Libraries/The Yfinance Library.md>)** — downloading Yahoo Finance market data into pandas.

---

## Related folders

- **Conda** — environment and package management (`Conda Environment Basics`, `Conda vs Pip`).
