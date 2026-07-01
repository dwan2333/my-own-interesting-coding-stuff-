# Pathlib — File System Operations

_Research compiled 2026-06-30 — Python standard library `pathlib`, based on Automate the Boring Stuff Ch. 10_

> Companion to [Pathlib - Building and Inspecting Paths](<Pathlib - Building and Inspecting Paths.md>) and [Random Modules](<Random Modules.md>). Where the sibling note builds and dissects paths (pure string math), **this note actually touches the disk** — checking, reading, writing, listing, creating, and deleting real files. Methods marked **added** go beyond what Chapter 10 shows.

---

## Branch 1 — Checking What's There

| Method | Returns `True` when… |
|---|---|
| `.exists()` | the path exists at all |
| `.is_file()` | it's a file |
| `.is_dir()` | it's a directory |
| `.is_symlink()` *(added)* | it's a symbolic link |
| `.stat()` | (not bool) returns metadata: `.st_size`, timestamps |

```python
from pathlib import Path

p = Path('notes.txt')
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
> `*` = any run of characters, `?` = one character, `**` = this folder and all subfolders. `folder.glob('**/*.py')` is the same as `folder.rglob('*.py')`.

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

> [!warning] `pathlib` deletes are limited on purpose
> `.unlink()` only removes a **file**; `.rmdir()` only removes an **empty** folder. To delete a folder that still has contents, use **`shutil.rmtree(path)`** from the `shutil` module — `pathlib` deliberately has no recursive-delete, to avoid accidents.

---

## Key Takeaways

- **Check first:** `.exists()`, `.is_file()`, `.is_dir()` (`.is_symlink()` added); `.stat().st_size` for the byte size.
- **Read/write in one call:** `.read_text()` / `.write_text()` for strings, `.read_bytes()` / `.write_bytes()` for binary; `.open('a')` for appending; `.touch()` to make an empty file. `write_text()` **overwrites**.
- **List folders:** `.iterdir()` (direct children), `.glob(pattern)` (wildcards), `.rglob(pattern)` (recursive).
- **Create/delete:** `.mkdir(parents=True, exist_ok=True)`, `.rename()` / `.replace()` to move, `.unlink(missing_ok=True)` for files, `.rmdir()` for empty folders.
- For **recursive deletion**, reach outside pathlib to **`shutil.rmtree()`**.
- Path *building* and inspection live in the sibling note: [Pathlib - Building and Inspecting Paths](<Pathlib - Building and Inspecting Paths.md>).

---

### Sources

| Source | Date | Type |
|---|---|---|
| Automate the Boring Stuff, 3e — Chapter 10 (Files & Paths) | 2026 | Book chapter |
| Python `pathlib` — official documentation | 2026 | Standard library reference |
