# The ord() and chr() Functions

_Research compiled 2026-06-30 — Python built-ins `ord()` and `chr()`, based on Automate the Boring Stuff Ch. 8_

> Companion to [String Formatting and Methods](<String Formatting and Methods.md>) and [Random Modules](<Random Modules.md>). These two built-ins convert between a **character** and its **Unicode code-point number** — they're inverses of each other.

---

## Branch 1 — What They Do

Every character has a unique **code point**: an integer the computer uses to represent it (Unicode, which starts with the older ASCII numbers). `ord()` and `chr()` translate between the character and that number.

| Function | Takes | Returns |
|---|---|---|
| `ord(char)` | a **single character** | its code-point **integer** |
| `chr(number)` | an **integer** | the **character** at that code point |

```python
print(ord('A'))    # 65   — character → number
print(chr(65))     # 'A'  — number → character
```

They undo each other:

```python
print(chr(ord('A')))   # 'A'
print(ord(chr(97)))    # 97
```

> [!warning] `ord()` needs exactly one character
> `ord('A')` works; `ord('AB')` raises `TypeError` — it wants a string of length 1. `chr()` takes any valid code-point integer.

---

## Branch 2 — Useful Because Code Points Are Ordered

Letters and digits sit in **consecutive** blocks, so you can do arithmetic on them.

```python
# Uppercase A–Z are 65–90, lowercase a–z are 97–122
print(ord('A'), ord('Z'))   # 65 90
print(ord('a'), ord('z'))   # 97 122
print(ord('0'), ord('9'))   # 48 57
```

### Next / previous letter

```python
print(chr(ord('A') + 1))    # 'B'  — shift one letter forward
print(chr(ord('z') - 1))    # 'y'  — one letter back
```

### The whole alphabet in a loop

```python
alphabet = ''.join(chr(code) for code in range(ord('a'), ord('z') + 1))
print(alphabet)             # 'abcdefghijklmnopqrstuvwxyz'
```

### Uppercase → lowercase by the numbers

Lowercase letters are exactly **32** higher than their uppercase versions:

```python
print(ord('a') - ord('A'))  # 32
print(chr(ord('H') + 32))   # 'h'
```

(In real code use `str.lower()` — this just shows *why* the gap works.)

---

## Branch 3 — A Tiny Caesar Cipher

The classic use: shift each letter by a fixed amount, wrapping around with `%`. This is what `ord()`/`chr()` are for.

```python
def shift(text, key):
    result = ''
    for ch in text:
        if ch.isupper():
            result += chr((ord(ch) - ord('A') + key) % 26 + ord('A'))
        elif ch.islower():
            result += chr((ord(ch) - ord('a') + key) % 26 + ord('a'))
        else:
            result += ch            # leave spaces/punctuation alone
    return result

secret = shift('Hello, World!', 3)
print(secret)                       # 'Khoor, Zruog!'
print(shift(secret, -3))            # 'Hello, World!'  (shift back to decrypt)
```

- `ord(ch) - ord('A')` maps `A–Z` to `0–25`.
- `+ key` shifts, `% 26` wraps `Z` back around to `A`.
- `+ ord('A')` maps back to a letter, and `chr(...)` turns it into the character.

---

## Key Takeaways

- **`ord(char)`** → the character's Unicode code-point integer; **`chr(number)`** → the character for that code point. They're inverses.
- `ord()` needs a **single** character or it raises `TypeError`.
- Because code points are **consecutive** (`A–Z` = 65–90, `a–z` = 97–122, `0–9` = 48–57), you can do letter arithmetic — next/previous letter, case shifts, ciphers.
- For everyday case changes prefer `str.lower()` / `str.upper()`; reach for `ord`/`chr` when you need the **numeric** relationship (ciphers, encoding, character ranges).

---

### Sources

| Source | Date | Type |
|---|---|---|
| Automate the Boring Stuff, 3e — Chapter 8 (Strings) | 2026 | Book chapter |
| Python `ord` / `chr` — official built-in functions documentation | 2026 | Standard library reference |
