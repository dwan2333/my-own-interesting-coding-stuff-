# Pathlib — File System Operations

_Research compiled 2026-06-30 — Python standard library `pathlib`, based on Automate the Boring Stuff Ch. 10_

> Companion to [Pathlib - Building and Inspecting Paths](<Pathlib - Building and Inspecting Paths.md>) and [Random Modules](<../Modules and Libraries/Random Modules.md>). Where the sibling note builds and dissects paths (pure string math), **this note actually touches the disk** — checking, reading, writing, listing, creating, and deleting real files. Methods marked **added** go beyond what Chapter 10 shows.

---

## Branch 1 — Checking What's There

| Method                    | Returns `True` when…                                |
| ------------------------- | --------------------------------------------------- |
| `.exists()`               | the path exists at all                              |
| `.is_file()`              | it's a file                                         |
| `.is_dir()`               | it's a directory                                    |
| `.is_symlink()` *(added)* | it's a symbolic link                                |
| `.stat()`                 | (not bool) returns metadata: `.st_size`, timestamps |

```python
from pathlib import Path

folder = Path('.')
p = Path('notes.txt')

print(folder.is_dir())      # True  — a directory
print(p.is_file())          # True  — a regular file (if it exists)
print(p.is_symlink())       # False — not a symbolic link
if p.exists() and p.is_file():
    print('size in bytes:', p.stat().st_size)
```

> [!tip] `.exists()` before you read
> Reading a missing file raises `FileNotFoundError`. A quick `if p.exists():` (or a `try`/`except`) avoids the crash.

---

## Branch 2 — Reading and Writing

`pathlib` can read or write a whole file in **one call** — no `open()`/`close()` needed for simple cases.

| Method | What it does |
|---|---|
| `.read_text(encoding=...)` | return the whole file as a **string** |
| `.write_text(s)` | create/overwrite the file with string `s` |
| `.read_bytes()` *(added)* | read the file as **bytes** (images, binary) |
| `.write_bytes(b)` *(added)* | write raw bytes |
| `.open(mode)` *(added)* | get a normal file handle (for line-by-line or appending) |
| `.touch()` *(added)* | create an empty file (or update its timestamp) |

```python
from pathlib import Path

p = Path('demo.txt')
p.write_text('line1\nline2')          # creates/overwrites the file
print(repr(p.read_text()))            # 'line1\nline2'

# open() when you need modes like append or line-by-line
with p.open('a', encoding='utf-8') as f:
    f.write('\nline3')
```

> [!note] What does `'a'` mean here? See [File Open Modes](<File Open Modes.md>)
> `Path.open()` takes the exact same mode strings as the built-in `open()` — `'r'` read, `'w'` write (wipes), `'a'` append, `'x'` create-only, plus `'b'`/`'+'`. The dedicated **[File Open Modes](<File Open Modes.md>)** note breaks down every mode and the `'w'` vs `'a'` difference.

**`read_bytes()` / `write_bytes()`** — the binary equivalents, for non-text files (images, audio, `.zip`). They take and return `bytes`, not `str`:

```python
from pathlib import Path

b = Path('data.bin')
b.write_bytes(b'\x00\x01\x02ABC')     # write raw bytes
print(b.read_bytes())                 # b'\x00\x01\x02ABC'
```

**`touch()`** — create an empty file (or, if it already exists, just update its modified-time):

```python
from pathlib import Path

t = Path('empty.txt')
t.touch()
print(t.exists(), t.stat().st_size)   # True 0   (exists, zero bytes)
```

> [!warning] `write_text()` overwrites without warning
> It replaces the entire file — there's no "append" mode. To add to a file, use `.open('a')`. To specify a UTF-8 encoding (recommended on Windows, given the cp1252 default), pass `encoding='utf-8'`.

---

## Branch 3 — Listing a Folder's Contents

| Method | What it does |
|---|---|
| `.iterdir()` *(added)* | yield every item **directly inside** a folder |
| `.glob(pattern)` | yield items matching a wildcard pattern (one level, unless `**`) |
| `.rglob(pattern)` *(added)* | **recursive** glob — search all subfolders |

```python
from pathlib import Path

folder = Path('.')

# everything directly inside
for item in folder.iterdir():
    print(item.name)

# only Python files in this folder
for py in folder.glob('*.py'):
    print(py.name)

# every .txt anywhere below this folder (recursive)
for txt in folder.rglob('*.txt'):
    print(txt)
```

> [!tip] `glob` wildcards
> `*` = any run of characters, `?` = **one** character, `**` = this folder and all subfolders. `folder.glob('**/*.py')` is the same as `folder.rglob('*.py')`.

Given a folder with `a.txt`, `b.txt`, `c.py`, and `sub/deep.txt`, `sub/e.py`:

```python
from pathlib import Path
base = Path('.')

print(sorted(p.name for p in base.glob('*.txt')))    # ['a.txt', 'b.txt']
print(sorted(p.name for p in base.glob('?.py')))     # ['c.py']   (? = one char)
print(sorted(p.name for p in base.rglob('*.txt')))   # ['a.txt', 'b.txt', 'deep.txt']
print(sorted(p.name for p in base.glob('**/*.py')))  # ['c.py', 'e.py']  (recursive)
```

### The standalone `glob` module

Before `pathlib`, Python's separate **`glob` module** did the same wildcard matching but returned **strings** instead of `Path` objects. You'll still see it in lots of code, so it's worth knowing.

| Function | What it does | Returns |
|---|---|---|
| `glob.glob(pattern)` | list paths matching the pattern | **list** of strings |
| `glob.glob(pattern, recursive=True)` | let `**` descend into subfolders | list of strings |
| `glob.iglob(pattern)` | same, but as a lazy **iterator** | generator |
| `glob.escape(text)` | escape `*`, `?`, `[` so they match literally | string |

```python
import glob

print(glob.glob('*.txt'))                        # ['a.txt', 'b.txt']
print(glob.glob('**/*.txt', recursive=True))     # ['a.txt', 'b.txt', 'sub\\deep.txt']
print(list(glob.iglob('*.txt')))                 # ['a.txt', 'b.txt']  (iglob = lazy iterator)
print(glob.escape('file[1].txt'))                # 'file[[]1].txt'  (brackets escaped)
```

> [!tip] `glob` module vs `Path.glob()`
> They use the **same wildcard syntax**. The difference: `glob.glob()` returns plain **strings** and needs `recursive=True` to make `**` descend; `Path.glob()` returns **`Path` objects** and `**` is always recursive. In new code prefer **`Path.glob()`** / **`.rglob()`** — you get `Path` objects you can immediately `.read_text()`, `.rename()`, etc. Reach for the `glob` module only when you specifically want strings or are matching a bare pattern without a starting `Path`.

---

## Branch 4 — Creating and Deleting

| Method | What it does |
|---|---|
| `.mkdir()` | create a directory |
| `.mkdir(parents=True, exist_ok=True)` *(added args)* | also create missing parent folders; don't error if it already exists |
| `.rename(target)` *(added)* | move/rename to `target` |
| `.replace(target)` *(added)* | like rename, but overwrites an existing target |
| `.unlink()` *(added)* | delete a **file** |
| `.unlink(missing_ok=True)` *(added)* | delete, but don't error if it's already gone |
| `.rmdir()` *(added)* | delete an **empty** directory |

```python
from pathlib import Path

Path('output/logs').mkdir(parents=True, exist_ok=True)   # whole tree at once

p = Path('output/draft.txt')
p.write_text('temp')
p2 = p.rename('output/final.txt')      # move/rename → returns the new Path
p2.unlink(missing_ok=True)             # delete the file safely
Path('output/logs').rmdir()           # remove the (now empty) folder
```

**`rename()` vs `replace()`** — both move a file, but they differ when the target already exists:

```python
from pathlib import Path

a = Path('a.txt'); a.write_text('AAA')
b = Path('b.txt'); b.write_text('BBB')

a.replace(b)                 # move a → b, OVERWRITING the existing b
print(b.read_text())         # 'AAA'
print(a.exists())            # False
```

- **`replace(target)`** always overwrites `target` if it exists (cross-platform, predictable).
- **`rename(target)`** may **error or silently overwrite** depending on the OS when `target` exists — use `replace()` when the destination might already be there.

> [!warning] `pathlib` deletes are limited on purpose
> `.unlink()` only removes a **file**; `.rmdir()` only removes an **empty** folder. To delete a folder that still has contents, use **`shutil.rmtree(path)`** from the `shutil` module — `pathlib` deliberately has no recursive-delete, to avoid accidents.

---

## Key Takeaways

- **Check first:** `.exists()`, `.is_file()`, `.is_dir()` (`.is_symlink()` added); `.stat().st_size` for the byte size.
- **Read/write in one call:** `.read_text()` / `.write_text()` for strings, `.read_bytes()` / `.write_bytes()` for binary; `.open('a')` for appending; `.touch()` to make an empty file. `write_text()` **overwrites**.
- **List folders:** `.iterdir()` (direct children), `.glob(pattern)` (wildcards: `*`, `?`, `**`), `.rglob(pattern)` (recursive). The older standalone **`glob` module** (`glob.glob()`, `recursive=True` for `**`) does the same but returns **strings** — prefer `Path.glob()` in new code.
- **Create/delete:** `.mkdir(parents=True, exist_ok=True)`, `.rename()` / `.replace()` to move, `.unlink(missing_ok=True)` for files, `.rmdir()` for empty folders.
- For **recursive deletion**, reach outside pathlib to **`shutil.rmtree()`**.
- Path *building* and inspection live in the sibling note: [Pathlib - Building and Inspecting Paths](<Pathlib - Building and Inspecting Paths.md>).

---

### Sources

| Source | Date | Type |
|---|---|---|
| Automate the Boring Stuff, 3e — Chapter 10 (Files & Paths) | 2026 | Book chapter |
| Python `pathlib` — official documentation | 2026 | Standard library reference |
