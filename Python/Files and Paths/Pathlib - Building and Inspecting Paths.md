# Pathlib — Building and Inspecting Paths

_Research compiled 2026-06-30 — Python standard library `pathlib`, based on Automate the Boring Stuff Ch. 10_

> Companion to [Pathlib - File System Operations](<Pathlib - File System Operations.md>) and [Random Modules](<../Modules and Libraries/Random Modules.md>). `pathlib` represents a file path as a **`Path` object** instead of a plain string, giving you clean methods for building paths and pulling them apart. This note covers **construction and the path components**; the sibling note covers reading, writing, and changing files. Methods marked **added** go beyond what Chapter 10 shows.

---

## Branch 1 — Creating Path Objects

```python
from pathlib import Path

p = Path('spam') / 'bacon' / 'eggs.txt'   # the / operator joins path parts
print(p)                                   # spam\bacon\eggs.txt  (on Windows)
print(str(p))                              # convert to a plain string
```

- **`Path('...')`** — build a path from strings.
- **`/`** — join parts with the correct separator for the OS (no manual `\` or `/`).
- **`Path.cwd()`** — the current working directory.
- **`Path.home()`** — your home folder.
- **`.joinpath('a', 'b')`** *(added)* — join like `/` but as a method call.

```python
from pathlib import Path

print(Path.cwd())                          # current directory
print(Path.home())                         # e.g. C:\Users\dwan0
print(Path('a').joinpath('b', 'c'))        # a\b\c
print(Path('~/notes').expanduser())        # (added) expands ~ to your home folder
```

> [!tip] Why not just use strings?
> String paths force you to handle `\` vs `/`, trailing slashes, and joining by hand. `Path` objects do all of that correctly per-OS, and give you the inspection methods below for free.

---

## Branch 2 — Taking a Path Apart

Every `Path` exposes its pieces as attributes. Using `C:\Users\dwan0\report.final.txt`:

| Attribute                    | Value                                            | Meaning                                  |
| ---------------------------- | ------------------------------------------------ | ---------------------------------------- |
| `.parts`                     | `('C:\\', 'Users', 'dwan0', 'report.final.txt')` | every component as a tuple               |
| `.name`                      | `report.final.txt`                               | the full filename                        |
| `.stem`s                     | `report.final`                                   | filename **without** the final extension |
| `.suffix`                    | `.txt`                                           | the final extension                      |
| `.suffixes` *(added)*        | `['.final', '.txt']`                             | **all** extensions as a list             |
| `.parent`                    | `C:\Users\dwan0`                                 | the containing folder                    |
| `.parents[0]`, `.parents[1]` | `C:\Users\dwan0`, `C:\Users`                     | ancestor folders by index                |
| `.anchor`                    | `C:\`                                            | the root                                 |
| `.drive`                     | `C:`                                             | the drive (Windows)                      |

```python
from pathlib import Path

p = Path('C:/Users/dwan0/report.final.txt')
print(p.name)        # report.final.txt
print(p.stem)        # report.final
print(p.suffix)      # .txt
print(p.suffixes)    # ['.final', '.txt']   (added)
print(p.parent)      # C:\Users\dwan0
print(p.parts)       # ('C:\\', 'Users', 'dwan0', 'report.final.txt')
print(p.anchor)      # C:\\
print(p.drive)       # C:
print(p.parents[0])  # C:\Users\dwan0   (immediate parent)
print(p.parents[1])  # C:\Users         (grandparent — index up the tree)
```

---

## Branch 3 — Deriving New Paths *(mostly added)*

These return a **new** `Path` based on an existing one — great for renaming or changing extensions without string surgery.

| Method | What it does | Example result |
|---|---|---|
| `.with_suffix('.md')` | swap the extension | `...\report.final.md` |
| `.with_name('summary.txt')` | replace the whole filename | `...\summary.txt` |
| `.with_stem('draft')` | replace just the stem | `...\draft.txt` |

```python
from pathlib import Path

p = Path('C:/Users/dwan0/report.final.txt')
print(p.with_suffix('.md'))       # C:\Users\dwan0\report.final.md
print(p.with_name('summary.txt')) # C:\Users\dwan0\summary.txt
print(p.with_stem('draft'))       # C:\Users\dwan0\draft.txt
```

> [!note] `with_stem()` needs Python 3.9+
> `with_suffix()` and `with_name()` have been around longer; `with_stem()` was added in Python 3.9 (you're on 3.14, so all three work).

---

## Branch 4 — Absolute, Relative, and Resolved Paths

| Method                          | What it does                                                          |
| ------------------------------- | --------------------------------------------------------------------- |
| `.is_absolute()`                | `True` if the path starts from a root/drive                           |
| `.absolute()`                   | turn a relative path into an absolute one (does **not** resolve `..`) |
| `.resolve()` *(added)*          | the **canonical** absolute path — resolves `..` and symlinks          |
| `.relative_to(other)` *(added)* | the part of this path **below** `other`                               |
| `.match(pattern)` *(added)*     | test the path against a glob pattern → `True/False`                   |

```python
from pathlib import Path

print(Path('notes/todo.txt').is_absolute())          # False
print(Path('C:/a/b/../c').resolve())                 # C:\a\c   (.. collapsed)
print(Path('C:/Users/dwan0/report.txt')
        .relative_to('C:/Users'))                    # dwan0\report.txt
print(Path('C:/Users/dwan0/report.txt').match('*.txt'))  # True
print(Path('notes.txt').absolute())                  # e.g. C:\Users\dwan0\notes.txt (cwd + name)
```

> [!warning] `relative_to()` must actually be a sub-path
> `relative_to(other)` raises `ValueError` if the path isn't inside `other`. It's pure string math — it doesn't check the disk.

---

## Key Takeaways

- Build paths with **`Path('...')`** and the **`/`** operator (or `.joinpath()`); get key folders with **`Path.cwd()`** / **`Path.home()`**, and expand `~` with **`.expanduser()`**.
- Pull a path apart with **`.name`**, **`.stem`**, **`.suffix`** (`.suffixes` for all), **`.parent`** / **`.parents[i]`**, **`.parts`**, **`.anchor`**, **`.drive`**.
- Derive new paths with **`.with_suffix()`**, **`.with_name()`**, **`.with_stem()`** — no string hacking.
- **`.resolve()`** gives the canonical absolute path (collapses `..`); **`.relative_to()`** strips a leading folder; **`.match()`** tests a glob pattern.
- These are all **pure path math** — none of them touch the disk. For that, see [Pathlib - File System Operations](<Pathlib - File System Operations.md>).

---

### Sources

| Source | Date | Type |
|---|---|---|
| Automate the Boring Stuff, 3e — Chapter 10 (Files & Paths) | 2026 | Book chapter |
| Python `pathlib` — official documentation | 2026 | Standard library reference |
