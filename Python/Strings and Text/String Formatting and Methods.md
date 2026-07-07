# String Formatting and Methods

_Research compiled 2026-06-30 — Python string formatting + `str` methods, based on Automate the Boring Stuff Ch. 8_

> Companion to [List Methods](<../Data Structures/List Methods.md>) and [Dictionary Methods](<../Data Structures/Dictionary Methods.md>). Covers the **three ways to build formatted strings** (f-strings, `%s`, `.format()`) and the most useful **`str` methods**. Items marked **added** go beyond what Chapter 8 shows.

---

## Branch 1 — Three Ways to Insert Values Into a String

Say `name = 'Alice'` and `age = 30`. The same result, three styles:

```python
name = 'Alice'
age = 30

print(f'{name} is {age}')                    # f-string  (modern, preferred)
print('%s is %s' % (name, age))              # %s        (old style)
print('{} is {}'.format(name, age))          # .format() (middle era)
```

| Style | Looks like | Use when |
|---|---|---|
| **f-string** | `f'{name}'` | Default choice (Python 3.6+) — shortest, runs expressions inline |
| **`%s`** | `'%s' % (name,)` | Legacy code, or logging (`logging.debug('%s', x)`) |
| **`.format()`** | `'{}'.format(name)` | When the template and values are far apart, or reused by index |

---

## Branch 2 — f-strings (the modern default)

An **f-string** is any string prefixed with `f`. Anything inside `{ }` is evaluated as Python code.

```python
age = 30
print(f'In ten years I will be {age + 10}')   # expressions work inside braces
```

### Format specs — the part after a colon *(mostly added)*

Inside the braces, `{value:spec}` controls how the value is displayed. This is the powerful part the chapter barely touches.

```python
pi = 3.14159
n = 1234567
ratio = 0.827

print(f'{pi:.2f}')        # '3.14'      — 2 decimal places
print(f'{n:,}')           # '1,234,567' — thousands separator
print(f'{ratio:.1%}')     # '82.7%'     — as a percentage
print(f'{42:05d}')        # '00042'     — zero-pad to width 5
print(f'{"hi":>8}')       # '      hi'  — right-align in width 8
print(f'{"hi":<8}|')      # 'hi      |' — left-align
print(f'{"hi":^8}|')      # '   hi   |' — center
print(f'{"hi":*^8}')      # '***hi***'  — center, pad with *
```

| Spec | Meaning | Example → result |
|---|---|---|
| `.2f` | fixed decimals | `{3.14159:.2f}` → `3.14` |
| `,` | thousands separator | `{1000000:,}` → `1,000,000` |
| `.1%` | percentage | `{0.5:.1%}` → `50.0%` |
| `05d` | zero-pad integer | `{7:05d}` → `00007` |
| `>` `<` `^` | right / left / center align | `{"x":>5}` → `    x` |

> [!tip] The `=` debug form *(added)*
> `f'{value=}'` prints both the expression **and** its value — a fast debugging trick.
> ```python
> spam = 42
> print(f'{spam=}')      # spam=42
> ```

---

## Branch 3 — `%s` Old-Style Formatting

The oldest style: `%s` placeholders filled from a tuple after `%`.

```python
name = 'Alice'
print('My name is %s' % (name,))         # note the comma → single-item tuple
```

Other conversion codes *(added — the chapter mainly shows `%s`)*:

| Code | Inserts | Example → result |
|---|---|---|
| `%s` | any value as a string | `'%s' % 42` → `42` |
| `%d` | integer | `'%d' % 3.9` → `3` |
| `%f` | float (6 decimals default) | `'%f' % 3.14` → `3.140000` |
| `%.2f` | float, 2 decimals | `'%.2f' % 3.14159` → `3.14` |
| `%x` | hexadecimal | `'%x' % 255` → `ff` |

```python
print('%d' % 3.9)          # '3'         — integer (truncates the float)
print('%f' % 3.14)         # '3.140000'  — float, 6 decimals by default
print('%.2f' % 3.14159)    # '3.14'      — float, 2 decimals
print('%x' % 255)          # 'ff'        — hexadecimal
```

> [!note] Where `%s` still matters
> The `logging` module uses this style: `logging.debug('x is %s', x)`. It's worth recognizing even though f-strings are preferred elsewhere. See [The Logging Module](<../Debugging/The Logging Module.md>).

---

## Branch 4 — the `.format()` Method

Placeholders are `{}`; values come from `.format(...)`. Placeholders can be **numbered** (reuse/reorder) or **named**.

```python
print('{} is {}'.format('Alice', 30))              # positional
print('{1} then {0}'.format('second', 'first'))    # by index → 'first then second'
print('{name} is {age}'.format(name='Bob', age=25))# by name

# format specs work here too, after a colon:
print('{:.2f}'.format(3.14159))                    # '3.14'
print('{:,}'.format(1000000))                      # '1,000,000'
```

---

## Branch 5 — Case Methods

| Method | Returns | Note |
|---|---|---|
| `upper()` | all uppercase | |
| `lower()` | all lowercase | |
| `title()` | Each Word Capitalized | *added* |
| `capitalize()` | First char up, rest low | *added* |
| `swapcase()` | invert each letter's case | *added* |
| `casefold()` | aggressive lowercase for comparisons | *added* |

```python
s = 'hELLo WoRLD'
print(s.upper())        # 'HELLO WORLD'
print(s.lower())        # 'hello world'
print(s.title())        # 'Hello World'
print(s.capitalize())   # 'Hello world'
print(s.swapcase())     # 'HellO wOrld'
print('STRASSE'.casefold())  # 'strasse' — aggressive lowercase for comparisons
```

> [!warning] String methods return a **new** string
> Strings are **immutable** — `s.upper()` doesn't change `s`, it returns a new string. You must capture it: `s = s.upper()`.

---

## Branch 6 — Inspection (`isX`) Methods

Each returns `True`/`False`. All require the string to be **non-empty** to return `True`.

| Method | True when the string… |
|---|---|
| `isupper()` / `islower()` | is all upper / all lower case (has letters) |
| `isalpha()` | is only letters |
| `isalnum()` | is only letters and digits |
| `isdecimal()` | is only digit characters |
| `isspace()` | is only whitespace (spaces, tabs, newlines) |
| `istitle()` | Has Every Word Starting Uppercase |

```python
print('Hello'.isalpha())     # True
print('Hello123'.isalnum())  # True
print('42'.isdecimal())      # True
print('   '.isspace())       # True
print('Hello World'.istitle())  # True
print('HELLO'.isupper())     # True
print('hello'.islower())     # True
```

Common use — validating input in a loop until it's a number:

```python
age = '30'
if age.isdecimal():
    print('valid number:', int(age))
```

---

## Branch 7 — Searching & Replacing

| Method | What it does | Missing value → |
|---|---|---|
| `in` / `not in` | membership test (an operator, not a method) | `False` |
| `startswith(p)` / `endswith(s)` | prefix / suffix test | `False` |
| `find(sub)` | index of first match | `-1` *(added)* |
| `index(sub)` | index of first match | raises `ValueError` *(added)* |
| `count(sub)` | number of occurrences | `0` *(added)* |
| `replace(old, new)` | swap all occurrences | *(added)* |

```python
s = 'hello world'
print('world' in s)             # True
print(s.startswith('hello'))    # True
print(s.find('o'))              # 4   (first 'o')
print(s.endswith('world'))      # True
print(s.index('world'))         # 6   (like find, but raises ValueError if absent)
print(s.count('o'))             # 2
print(s.replace('world', 'there'))  # 'hello there'
```

> [!tip] `find()` vs `index()`
> Both return the position of a substring, but `find()` returns **-1** when it's not there while `index()` **crashes** with `ValueError`. Use `find()` when a miss is expected.

---

## Branch 8 — Splitting & Joining

| Method | What it does |
|---|---|
| `split(sep=None)` | string → list (default splits on any whitespace) |
| `splitlines()` | split on line breaks → list of lines *(added)* |
| `partition(sep)` | split into `(before, sep, after)` — exactly 3 parts *(added)* |
| `sep.join(list)` | list → string, `sep` between items |

```python
print('a,b,c'.split(','))            # ['a', 'b', 'c']
print('one two  three'.split())      # ['one', 'two', 'three']
print('line1\nline2'.splitlines())   # ['line1', 'line2']
print('user@example.com'.partition('@'))  # ('user', '@', 'example.com')
print('-'.join(['a', 'b', 'c']))     # 'a-b-c'
```

**`maxsplit` — limit how many splits happen** *(added)*. A second argument caps the number of splits; `rsplit` does the same but works from the **right**:

```python
print('a,b,c,d'.split(',', 2))       # ['a', 'b', 'c,d']   — only 2 splits
print('a,b,c,d'.rsplit(',', 1))      # ['a,b,c', 'd']      — 1 split, from the right
```

> [!note] `join()` reads backwards
> You call `join()` on the **separator**, passing the list: `'-'.join(items)`, not `items.join('-')`.

---

## Branch 9 — Padding & Stripping

| Method | What it does |
|---|---|
| `rjust(w, fill=' ')` | right-justify to width `w` |
| `ljust(w, fill=' ')` | left-justify to width `w` |
| `center(w, fill=' ')` | center to width `w` |
| `zfill(w)` | pad with leading zeros to width `w` *(added)* |
| `strip(chars=None)` | remove chars from both ends (default whitespace) |
| `lstrip()` / `rstrip()` | remove from left / right end only |

```python
print('Hi'.rjust(5))         # '   Hi'
print('Hi'.ljust(5) + '|')   # 'Hi   |'
print('Hi'.center(6, '=') )  # '==Hi=='
print('42'.zfill(5))         # '00042'
print('  hello  '.strip())   # 'hello'
print('xxhixx'.strip('x'))   # 'hi'
print(repr('  hi  '.lstrip()))  # 'hi  '  — left end only
print(repr('  hi  '.rstrip()))  # '  hi'  — right end only
```

> [!warning] `strip('chars')` removes a **set of characters**, not a substring
> The argument is treated as a *bag of individual characters* to strip from each end — **not** a prefix/suffix to match. So it can eat more than you expect:
> ```python
> print('commit.com'.strip('.com'))   # 'it'  — leading 'com' AND trailing '.com' stripped!
> ```
> To remove an exact prefix/suffix, use **`removeprefix()`** / **`removesuffix()`** (Python 3.9+):
> ```python
> print('commit.com'.removesuffix('.com'))   # 'commit'  — only the exact suffix
> ```

`rjust`/`ljust`/`center` are handy for lining up columns in a table printed to the screen.

---

## Related

- **[The ord() and chr() Functions](<The ord and chr Functions.md>)** — converting between a character and its Unicode code-point number (split out into its own note).

---

## Key Takeaways

- Prefer **f-strings**: `f'{value}'`. Add a **format spec** after a colon — `{x:.2f}` (decimals), `{x:,}` (thousands), `{x:>10}` (align/pad), `{x:.1%}` (percent), `{x=}` (debug).
- **`%s`** is legacy but lives on in `logging`; **`.format()`** shines when placeholders are numbered/named or reused.
- Strings are **immutable** — every string method returns a **new** string; capture it (`s = s.upper()`).
- Search/replace with `in`, `startswith`/`endswith`, `find` (returns `-1`) vs `index` (raises), `count`, `replace`.
- Reshape text with `split` / `splitlines` / `partition` and `sep.join(list)`; align with `rjust`/`ljust`/`center`/`zfill`; trim with `strip`/`lstrip`/`rstrip`.

---

### Sources

| Source | Date | Type |
|---|---|---|
| Automate the Boring Stuff, 3e — Chapter 8 (Strings) | 2026 | Book chapter |
| Python `str` — official text-sequence documentation | 2026 | Standard library reference |
| Python format spec mini-language — official documentation | 2026 | Standard library reference |
