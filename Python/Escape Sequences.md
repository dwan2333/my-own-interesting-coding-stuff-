# Escape Sequences

_Research compiled 2026-06-30 — Python string escape sequences, based on Automate the Boring Stuff Ch. 8_

> Companion to [String Formatting and Methods](<String Formatting and Methods.md>) and [Random Modules](<Random Modules.md>). An **escape sequence** is a backslash `\` followed by a character — it lets you put characters into a string that would otherwise be hard or impossible to type directly (quotes, tabs, newlines).

---

## Branch 1 — Why Escape Sequences Exist

Some characters can't just be typed inside a string. A quote would end the string early; a newline can't be typed on one line. The backslash `\` tells Python *"treat the next character specially."*

```python
# This breaks — the apostrophe ends the string too soon:
# print('It's a trap')          # SyntaxError

# Fix it with an escaped quote:
print('It\'s a trap')           # It's a trap
```

---

## Branch 2 — The Essential Escape Sequences

| Escape | Produces | Notes |
|---|---|---|
| `\'` | single quote | needed inside `'...'` strings |
| `\"` | double quote | needed inside `"..."` strings |
| `\\` | a literal backslash | because `\` itself is special |
| `\n` | newline (line break) | most common — moves to next line |
| `\t` | tab | aligns columns |
| `\r` | carriage return | return to line start (Windows line ends use `\r\n`) |
| `\b` | backspace | rarely used |
| `\0` | null character | code point 0 |

```python
print('Hello\nWorld')       # Hello  <newline>  World
print('Name:\tAlice')       # Name:   Alice   (tab gap)
print('Quote: \"hi\"')      # Quote: "hi"
print('Path: C:\\Users')    # Path: C:\Users

# the rarer control characters — shown with repr() so you can see them
print(repr('abc\rXY'))      # 'abc\rXY'   — \r carriage return (jumps to line start)
print(repr('ab\bc'))        # 'ab\x08c'   — \b backspace
print(repr('a\0b'))         # 'a\x00b'    — \0 null character (length is still 3)
```

> [!tip] You only escape the quote that matches your string
> Inside `'...'` you must escape `\'`, but `"` is fine as-is — and vice versa. So `"It's fine"` and `'She said "hi"'` need no escaping at all. Pick the quote style that avoids the most escaping.

---

## Branch 3 — Unicode by Code Point

You can drop any character into a string by its Unicode number (see [The ord() and chr() Functions](<The ord and chr Functions.md>)).

| Escape | Meaning | Example |
|---|---|---|
| `\xHH` | character from 2 hex digits | `'\x41'` → `'A'` |
| `\uHHHH` | character from 4 hex digits | `'é'` → `'é'` |
| `\U00HHHHHH` | character from 8 hex digits | `'\U0001F600'` → 😀 |
| `\N{NAME}` | character by its Unicode name | `'\N{BULLET}'` → `•` |

```python
print('\x41\x42\x43')            # ABC   (pure ASCII — always safe)
print('caf\xe9')                 # café  (é is in the Windows cp1252 set)
print('café')               # café  (\uHHHH — 4 hex digits give é)
```

> [!warning] Windows console encoding (cp1252) — read before printing π, •, or emoji
> Windows' default console encoding is **cp1252**, which only covers Latin-1 characters. Printing anything outside it — Greek `\N{GREEK SMALL LETTER PI}`, a bullet `\N{BULLET}`, or an emoji `\U0001F600` — raises **`UnicodeEncodeError`**. The escape sequence is fine; the *console* just can't render the glyph. Switch stdout to UTF-8 first:
> ```python
> import sys
> sys.stdout.reconfigure(encoding='utf-8')
> print('\N{GREEK SMALL LETTER PI} = 3.14')   # π = 3.14
> print('\U0001F600')                          # 😀
> ```
> (Or set the environment variable `PYTHONUTF8=1`.) This applies inside the Obsidian Execute Code plugin too.

---

## Branch 4 — Raw Strings Turn Escapes OFF

Put an `r` before the quote and Python treats every backslash **literally** — no escape processing. Essential for Windows paths and regular-expression patterns.

```python
print('C:\name\test')       # \n becomes a newline — path is broken!
print(r'C:\name\test')      # C:\name\test  — raw string keeps it literal
```

| String | `\n` means… |
|---|---|
| `'a\nb'` | a newline |
| `r'a\nb'` | a backslash then the letter `n` |

> [!warning] Where raw strings matter most
> Windows file paths (`r'C:\Users\Alice'`) and regex patterns (`r'\d+\.\d+'`) are full of backslashes. Without the `r`, Python tries to interpret each `\` as an escape — silently corrupting the string. Prefix them with `r`.

---

## Branch 5 — Multiline Strings

Triple quotes (`'''` or `"""`) let a string span several lines, keeping the line breaks literally — an alternative to scattering `\n`.

```python
message = '''Dear Alice,
Meet me at the park.
- Bob'''
print(message)
# Dear Alice,
# Meet me at the park.
# - Bob
```

Inside triple quotes you can use `'` and `"` freely without escaping. A trailing `\` at the end of a line **joins** it to the next (suppresses that one newline):

```python
print('one \
two')                       # one two   (the line break is escaped away)
```

---

## Key Takeaways

- An **escape sequence** is `\` + a character; it inserts things you can't type directly.
- Must-know: `\n` (newline), `\t` (tab), `\'` / `\"` (quotes), `\\` (literal backslash).
- Escape only the quote that **matches** your string's delimiter — or switch quote styles to avoid escaping entirely.
- Insert any character by code point with `\xHH`, `\uHHHH`, `\U…`, or by name with `\N{NAME}`.
- **Raw strings** (`r'...'`) disable escaping — use them for Windows paths and regex patterns.
- **Triple-quoted** strings span multiple lines and keep their line breaks literally.

---

### Sources

| Source | Date | Type |
|---|---|---|
| Automate the Boring Stuff, 3e — Chapter 8 (Strings) | 2026 | Book chapter |
| Python lexical analysis — string escape sequences (official docs) | 2026 | Language reference |
