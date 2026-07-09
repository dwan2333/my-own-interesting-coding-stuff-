# File Open Modes

_Research compiled 2026-06-30 — Python's built-in `open()` and file modes, based on Automate the Boring Stuff Ch. 10_

> Companion to [Pathlib - File System Operations](<Pathlib - File System Operations.md>) and [Random Modules](<../Modules and Libraries/Random Modules.md>). When you open a file with `open(path, mode)` (or `Path.open(mode)`), the **mode string** decides three things: whether you're **reading or writing**, whether existing content is **kept or wiped**, and whether you're working in **text or bytes**. Getting the mode wrong is how people accidentally erase files — so this note covers every mode in detail.

---

## Branch 1 — The Shape of `open()`

```python
with open('testfile.txt', 'r', encoding='utf-8') as f:
    contents = f.read()
```

- **1st argument** — the file path (string or `Path`).
- **2nd argument** — the **mode** (default `'r'`).
- **`encoding=`** — how text is decoded/encoded (use `'utf-8'`; see the warning in Branch 5).
- **`with`** — a *context manager* that **auto-closes** the file when the block ends, even if an error happens. Always use `with`.

> [!tip] Always use `with`
> Without `with` you must call `f.close()` yourself, and a crash before that line leaks the open file (and can lose un-flushed writes). `with open(...) as f:` closes it for you, guaranteed.

---

## Branch 2 — The Core Modes

| Mode | Name | If the file **exists** | If it **doesn't** | Position |
|---|---|---|---|---|
| `'r'` | read (default) | opens for reading | **`FileNotFoundError`** | start |
| `'w'` | write | **erases all content** | creates it | start |
| `'a'` | append | keeps content, adds to end | creates it | **end** |
| `'x'` | exclusive create | **`FileExistsError`** | creates it | start |

```python
# 'w' — WIPES the file first, then writes
with open('test.txt', 'w', encoding='utf-8') as f:
    f.write('first\n')
with open('test.txt', 'w', encoding='utf-8') as f:
    f.write('second\n')     # 'first' is gone
# file now contains: 'second\n'
```

---

## Branch 3 — `'w'` vs `'a'` (the one everybody asks about)

Both **write** and both **create the file if it's missing**. The difference is what happens to content that's *already there*:

- **`'w'` (write)** — **truncates** the file to empty the moment you open it, then writes. Anything that was in the file is **gone**.
- **`'a'` (append)** — leaves existing content untouched and moves the write position to the **end**, so new text is added *after* what's already there.

```python
# start fresh
with open('log.txt', 'w', encoding='utf-8') as f:
    f.write('second\n')

# 'a' keeps 'second' and adds after it
with open('log.txt', 'a', encoding='utf-8') as f:
    f.write('third\n')

# file now contains:
# second
# third
```

> [!warning] `'w'` erases the whole file on open — even if you write nothing
> The truncation happens when the file is *opened* in `'w'`, not when you write. `open('important.txt', 'w')` and then closing it immediately leaves the file **empty**. Use `'a'` to add to a file, and `'w'` only when you truly want to replace it. Use `'x'` if you want to *avoid* overwriting an existing file (it errors instead).

---

## Branch 4 — Text vs Binary, and the `+` Modifier

Two modifiers combine with the letters above:

| Modifier | Meaning |
|---|---|
| `'t'` | **text** mode (default) — reads/writes `str`, handles encoding and line endings |
| `'b'` | **binary** mode — reads/writes `bytes`, no encoding (images, audio, `.zip`) |
| `'+'` | open for **both reading and writing** |

```python
# binary read → returns bytes, not str
with open('test.txt', 'rb') as f:
    print(f.read()[:6])      # b'second'
```

Common combined modes you'll actually see:

| Mode | Meaning |
|---|---|
| `'rb'` | read bytes | 
| `'wb'` | write bytes (wipes first) |
| `'r+'` | read **and** write, file must exist, position at start |
| `'w+'` | read **and** write, but **wipes** the file first |
| `'a+'` | read **and** write, position at end, keeps content |

> [!note] `'b'` never takes an `encoding`
> Encoding only applies to text. In binary mode you pass and receive `bytes` directly — passing `encoding=` with `'b'` is an error.

---

## Branch 5 — Reading Methods

Once a file is open in a read mode, these pull the text out:

| Method | Returns |
|---|---|
| `f.read()` | the **entire** file as one string |
| `f.read(n)` | the next `n` characters |
| `f.readline()` | the next **single line** (including its `\n`) |
| `f.readlines()` | a **list** of all lines |
| iterating `for line in f:` | one line at a time — memory-friendly for big files |

```python
# given a file containing 'second\nthird\n'
with open('test.txt', encoding='utf-8') as f:
    print(f.read())          # 'second\nthird\n'

with open('test.txt', encoding='utf-8') as f:
    print(f.readlines())     # ['second\n', 'third\n']

with open('test.txt', encoding='utf-8') as f:
    for line in f:           # best for large files — reads lazily
        print(line.rstrip('\n'))
```

> [!warning] Always pass `encoding='utf-8'` on Windows
> Without it, Python uses the OS default — on your machine that's **cp1252**, which mis-reads or crashes on non-Latin text (see [Escape Sequences](<../Strings and Text/Escape Sequences.md>)). Passing `encoding='utf-8'` makes files read/write consistently across systems. The same applies to `Path.read_text()` / `write_text()`.

---

## Branch 6 — Writing, and the Full Method Set

`write()` writes one string; **`writelines()`** writes a whole **sequence** of strings (it does *not* add newlines — include your own `\n`).

```python
with open('out.txt', 'w', encoding='utf-8') as f:
    f.write('one line\n')
    f.writelines(['a\n', 'b\n', 'c\n'])   # write several strings at once
```

The most useful file methods and attributes:

| Method / attribute | What it does |
|---|---|
| `read([n])` | read all, or `n` characters (text) / bytes (binary) |
| `readline()` / `readlines()` | one line / a list of all lines |
| `write(s)` / `writelines(seq)` | write a string / a sequence of strings |
| `seek(pos)` | jump to byte position `pos` (see Branch 7) |
| `tell()` | current position, as a byte offset |
| `flush()` | force buffered writes out to disk now |
| `close()` | close it (`with` does this for you) |
| `readable()` / `writable()` / `seekable()` | `True`/`False` — what this file supports |
| `closed` | `True` once the file is closed |
| `encoding` | the encoding in use (e.g. `'utf-8'`) |

---

## Branch 7 — File Position: `seek()` and `tell()`

A file has a **position** — where the next read/write happens. Reading advances it; **`tell()`** reports it (as a **byte** offset) and **`seek(pos)`** jumps to a byte.

```python
with open('poem.txt', encoding='utf-8') as f:
    print(f.read(5))    # read 5 characters
    print(f.tell())     # current position (in bytes)
    f.seek(0)           # jump back to the start
    print(f.read(3))    # read from the beginning again
```

This is **random access** — handy for re-reading, or jumping around a large file without reading everything.

---

## Branch 8 — Characters vs. Bytes (the encoding subtlety)

This is the part that trips people up. In **text mode**, `read(n)` returns **`n` characters**; in **binary mode** (`'rb'`), it returns **`n` bytes**. Those aren't the same, because UTF-8 is a **variable-length** encoding — one character can be 1–4 bytes.

```python
# the file starts with "Sueña..." — the 'ñ' takes 2 bytes in UTF-8
with open('poem.txt', encoding='utf-8') as f:
    chars = f.read(10)
    print(len(chars))     # 10   — ten CHARACTERS
    print(f.tell())       # 11   — but ELEVEN bytes (ñ counted as 2)

with open('poem.txt', 'rb') as f:
    data = f.read(10)
    print(len(data))      # 10   — exactly ten BYTES
    print(data[:5])       # b'Sue\xc3\xb1'  — the ñ shows as two raw bytes
```

Check the platform's default encoding (why you should always pass `encoding=` explicitly):

```python
import sys
print(sys.getdefaultencoding())   # 'utf-8'  — but the *file* default varies by OS
```

> [!warning] Don't `seek()` into the middle of a character in text mode
> Because a character can span several bytes, seeking to a byte that lands **inside** a multi-byte character makes the next read fail with **`UnicodeDecodeError`** — Python can't decode half a character.
> ```python
> with open('poem.txt', encoding='utf-8') as f:
>     f.seek(4)      # byte 4 is the 2nd half of 'ñ'
>     f.read(1)      # UnicodeDecodeError!
> ```
> `seek()` is only truly safe in **binary** mode. In text mode, seek to `0` or to positions you got from `tell()`.

---

## Key Takeaways

- `open(path, mode, encoding='utf-8')` inside a **`with`** block (auto-closes). Default mode is `'r'`.
- **Core modes:** `'r'` read (errors if missing), `'w'` write (**erases first**), `'a'` append (keeps + adds at end), `'x'` create-only (errors if it exists).
- **`'w'` vs `'a'`:** both write and both create the file; `'w'` **wipes** existing content on open, `'a'` **preserves** it and writes at the end. `'w'` empties the file the instant it opens, even with no write.
- **Modifiers:** `'t'` text (default, `str`), `'b'` binary (`bytes`, no encoding), `'+'` read-and-write — combine as `'rb'`, `'w+'`, `'a+'`, etc.
- **Reading:** `read()` (all), `read(n)` (n chars), `readline()` (one line), `readlines()` (list), or iterate `for line in f:` (lazy, best for big files).
- **Writing:** `write(s)` (one string), `writelines(seq)` (several — no auto-newlines). `flush()` forces buffered writes to disk.
- **Position:** `tell()` reports the byte offset; `seek(pos)` jumps to a byte (random access).
- **Characters ≠ bytes:** in text mode `read(n)` = `n` **characters**; in binary mode = `n` **bytes**. UTF-8 is variable-length, so one character can be several bytes — which is why `seek()` into a multi-byte char errors in text mode.
- **Always pass `encoding='utf-8'`** on Windows to avoid cp1252 problems; `sys.getdefaultencoding()` shows the default.

---

### Sources

| Source | Date | Type |
|---|---|---|
| Automate the Boring Stuff, 3e — Chapter 10 (Files & Paths) | 2026 | Book chapter |
| Python for Data Analysis, 3e (Wes McKinney) — §3.3 Files and the Operating System | 2026 | Book section |
| Python `open()` — official built-in functions documentation | 2026 | Standard library reference |
| Verified against Python 3.14 on `E:\Python` | 2026-07-09 | Local test |
