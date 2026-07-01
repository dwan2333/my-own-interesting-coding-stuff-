# The Regex Module (`re`)

_Research compiled 2026-06-30 — Python standard library `re`, based on Automate the Boring Stuff Ch. 12_

> Companion to [String Formatting and Methods](<String Formatting and Methods.md>) and [Random Modules](<Random Modules.md>). A **regular expression** (regex) is a pattern for matching text. The `re` module compiles these patterns and searches, extracts, and replaces text with them — far more powerful than `str.find()` or `in`.

---

## Branch 1 — The Basic Workflow

1. `import re`
2. Build a pattern, ideally as a **raw string** (`r'...'`) so backslashes stay literal.
3. Search text with it and read the **match object**.

```python
import re

pattern = re.compile(r'\d\d\d-\d\d\d-\d\d\d\d')     # a phone number shape
match = pattern.search('Call me at 415-555-1234 today.')
print(match.group())        # 415-555-1234
```

> [!tip] Always use raw strings for patterns
> Regex uses backslashes constantly (`\d`, `\w`, `\.`). In a normal string `\d` risks being mangled; in a raw string `r'\d'` it stays literal. See [Escape Sequences](<Escape Sequences.md>). Always write patterns as `r'...'`.

---

## Branch 2 — The Search Methods

You can call these on a compiled pattern (`pattern.search(text)`) **or** on the module directly (`re.search(pattern, text)`).

| Method | Returns | Finds |
|---|---|---|
| `search(text)` | Match object, or `None` | the **first** match anywhere |
| `match(text)` | Match object, or `None` | a match **only at the start** of the string |
| `fullmatch(text)` | Match object, or `None` | a match only if the **whole** string matches |
| `findall(text)` | **list** of strings (or tuples) | **every** non-overlapping match |
| `finditer(text)` | iterator of **match objects** | every match, one at a time |
| `sub(repl, text)` | new **string** | replaces every match with `repl` |
| `split(text)` | **list** of strings | splits the string on every match |

```python
import re

text = 'cat hat sat mat'
print(re.search(r'[chm]at', text).group())   # 'cat'  (first match)
print(re.findall(r'[chm]at', text))          # ['cat', 'hat', 'mat']  ('sat' excluded)
print(re.sub(r'[chm]at', 'DOG', text))       # 'DOG DOG sat DOG'
print(re.split(r'\s', text))                 # ['cat', 'hat', 'sat', 'mat']
```

> [!warning] Check for `None` before `.group()`
> `search()` / `match()` return `None` when nothing matches. Calling `.group()` on `None` raises `AttributeError`. Guard it: `m = re.search(...); if m: ...`.

### `match()` — only at the **start** of the string

Unlike `search` (which looks anywhere), `match` only succeeds if the pattern is found right at the beginning.

```python
import re

print(bool(re.match(r'\d+', '123 abc')))     # True  — starts with digits
print(bool(re.match(r'\d+', 'abc 123')))     # False — digits aren't at the start
print(re.match(r'\d+', '123 abc').group())   # '123'
```

### `fullmatch()` — the **whole** string must match

Succeeds only if the pattern covers the entire string end to end — ideal for **validation** (is this string *exactly* a phone number?).

```python
import re

print(bool(re.fullmatch(r'\d{3}-\d{4}', '555-1234')))      # True
print(bool(re.fullmatch(r'\d{3}-\d{4}', '555-1234 ext')))  # False — extra text
```

### `finditer()` — every match as a match **object**

Like `findall`, but yields match **objects** (not strings), so you also get each match's position via `.start()` / `.end()`.

```python
import re

for m in re.finditer(r'\d+', 'a1 bb22 ccc333'):
    print(m.group(), 'at', m.start(), '-', m.end())
# 1 at 1 - 2
# 22 at 5 - 7
# 333 at 11 - 14
```

> [!tip] `findall` vs `finditer`
> `findall` gives you a quick **list of strings**. `finditer` gives you match **objects** — reach for it when you also need each match's **position** or groups.

---

## Branch 3 — Groups With Parentheses

Wrapping part of a pattern in `()` creates a **group** you can pull out separately. `group(0)` (or `group()`) is the whole match; `group(1)`, `group(2)`, … are the parenthesised parts, left to right.

```python
import re

pattern = re.compile(r'(\d\d\d)-(\d\d\d-\d\d\d\d)')
m = pattern.search('My number is 415-555-1234.')
print(m.group())     # 415-555-1234   (the whole match)
print(m.group(1))    # 415            (first group — area code)
print(m.group(2))    # 555-1234       (second group)
print(m.groups())    # ('415', '555-1234')   (all groups as a tuple)
```

### Named groups

Name a group with `(?P<name>...)` and read it by name — clearer than counting positions.

```python
import re

m = re.search(r'(?P<area>\d{3})-(?P<rest>\d{3}-\d{4})', '415-555-1234')
print(m.group('area'))    # 415
print(m.group('rest'))    # 555-1234
```

### `findall` and groups

With **one** group, `findall` returns that group's text; with **multiple** groups it returns **tuples**.

```python
import re

print(re.findall(r'(\d\d\d)-(\d\d\d\d)', '555-1234, 999-8888'))
# [('555', '1234'), ('999', '8888')]
```

---

## Branch 4 — Character Classes (`\d`, `\w`, `\s`, …)

These shorthand classes are the workhorses — they match *kinds* of characters. Each has an **uppercase = NOT** version.

| Shorthand | Matches | Opposite | Matches |
|---|---|---|---|
| `\d` | a digit `0–9` | `\D` | any **non**-digit |
| `\w` | a "word" char: letter, digit, or `_` | `\W` | any **non**-word char |
| `\s` | whitespace (space, tab, newline) | `\S` | any **non**-whitespace |

```python
import re

print(re.findall(r'\d+', 'Order 12 costs $34'))      # ['12', '34']
print(re.findall(r'\w+', 'hi_there, world!'))         # ['hi_there', 'world']
print(re.split(r'\s+', 'split   these\twords'))       # ['split', 'these', 'words']
```

### Related escape-based tokens

| Token | Meaning |
|---|---|
| `\n` `\t` | a literal newline / tab inside the pattern |
| `\b` | a **word boundary** (between `\w` and non-`\w`) — great for whole-word matches |
| `\.` `\$` `\(` | a **literal** `.` `$` `(` — backslash escapes a special character |

```python
import re

print(re.findall(r'\bcat\b', 'the cat scattered'))   # ['cat']  (not 'cat' in 'scattered')
print(re.findall(r'\$\d+', 'costs $5 and $40'))       # ['$5', '$40']  (escaped $)
```

### Custom classes with `[ ]`

Make your own set with square brackets; `^` inside negates it; `-` gives a range.

```python
import re

print(re.findall(r'[aeiou]', 'Robocop eats baby food'))   # all vowels
print(re.findall(r'[^aeiou ]', 'hello'))                  # ['h','l','l'] (non-vowels)
print(re.findall(r'[A-Z][a-z]+', 'Alice met Bob'))        # ['Alice', 'Bob']
```

---

## Branch 5 — Repetition (Quantifiers)

How **many** times the preceding piece must match.

| Quantifier | Meaning |
|---|---|
| `?` | 0 or 1 (optional) |
| `*` | 0 or more |
| `+` | 1 or more |
| `{n}` | exactly `n` |
| `{n,m}` | between `n` and `m` |
| `{n,}` | `n` or more |

```python
import re

print(re.findall(r'\d{3}-\d{4}', 'call 555-1234'))    # ['555-1234']
print(re.findall(r'go*d', 'gd god good goood'))       # ['gd','god','good','goood']
print(re.search(r'colou?r', 'color').group())         # 'color'  (u optional)
```

> [!warning] Greedy vs non-greedy
> Quantifiers are **greedy** by default — they grab as much as possible. Add `?` after a quantifier to make it **non-greedy** (as little as possible).
> ```python
> print(re.search(r'<.*>', '<a><b>').group())    # '<a><b>'  (greedy)
> print(re.search(r'<.*?>', '<a><b>').group())   # '<a>'     (non-greedy)
> ```

---

## Branch 6 — Anchors and Flags

**Anchors** pin a match to a position (they match a *place*, not a character):

| Anchor | Matches |
|---|---|
| `^` | start of the string |
| `$` | end of the string |
| `.` | any single character **except** newline |

```python
import re

print(bool(re.search(r'^Hello', 'Hello world')))    # True  (starts with Hello)
print(bool(re.search(r'world$', 'Hello world')))     # True  (ends with world)
```

**Flags** change how the whole pattern behaves — pass them as the third argument:

| Flag | Effect |
|---|---|
| `re.IGNORECASE` (`re.I`) | case-insensitive matching |
| `re.DOTALL` (`re.S`) | let `.` also match newlines |
| `re.MULTILINE` (`re.M`) | `^` and `$` match at each line, not just string ends |

**`re.IGNORECASE`** — match regardless of upper/lower case:

```python
import re

print(re.findall(r'cat', 'Cat CAT cat', re.IGNORECASE))   # ['Cat', 'CAT', 'cat']
```

**`re.DOTALL`** — let `.` also match newline characters (normally it stops at `\n`):

```python
import re

text = 'first line\nsecond line'
print(re.search(r'first.*second', text))                    # None  — . won't cross \n
print(re.search(r'first.*second', text, re.DOTALL).group()) # 'first line\nsecond'
```

**`re.MULTILINE`** — make `^` and `$` match at the start/end of **each line**, not just the whole string:

```python
import re

log = 'ERROR disk\nok cpu\nERROR ram'
print(re.findall(r'^ERROR', log))                 # ['ERROR']          (only the very start)
print(re.findall(r'^ERROR', log, re.MULTILINE))   # ['ERROR', 'ERROR'] (start of each line)
```

> [!tip] Combining flags
> Combine flags with the `|` operator: `re.search(pattern, text, re.IGNORECASE | re.DOTALL)`.

---

## Key Takeaways

- Workflow: `import re` → write a **raw-string** pattern → `search`/`findall`/`sub` → read the **match object**.
- **Search methods:** `search` (first), `match` (at start), `fullmatch` (whole string), `findall` (list of all), `finditer` (match objects), `sub` (replace), `split`.
- **Groups** with `()` — `group(0)` is the whole match, `group(1)`, `group(2)`, … are the parts; name them with `(?P<name>...)`.
- **Character classes:** `\d` digit, `\w` word char, `\s` whitespace — uppercase negates. `\b` = word boundary; backslash escapes literals like `\.` `\$`.
- **Quantifiers:** `?` `*` `+` `{n}` `{n,m}`; greedy by default — add `?` for non-greedy.
- **Anchors** `^` `$` `.`; **flags** `re.IGNORECASE`, `re.DOTALL`, `re.MULTILINE`. Always check a match isn't `None` before `.group()`.

---

### Sources

| Source | Date | Type |
|---|---|---|
| Automate the Boring Stuff, 3e — Chapter 12 (Regular Expressions) | 2026 | Book chapter |
| Python `re` — official regular-expression documentation | 2026 | Standard library reference |
