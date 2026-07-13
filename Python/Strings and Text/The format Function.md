# The format() Function

_Research compiled 2026-07-13 — the `format()` built-in and the `__format__` protocol it shares with f-strings_

> Companion to [String Formatting and Methods](<String Formatting and Methods.md>). That note covers the **three formatting styles** (f-strings, `%s`, `.format()`); this one covers the **`format()` built-in function** — and the key insight that f-strings, `str.format()`, and `format()` are all front-ends for the **same machinery**: the value's `__format__` method.

---

## Branch 1 — What format() Does

`format(value, spec)` takes **one value** and a **format spec string**, and returns the formatted text:

```python
print(format(3.14159, '.2f'))    # '3.14'      — 2 decimal places
print(format(1234567, ','))      # '1,234,567' — thousands separator
print(format(255, 'x'))          # 'ff'        — hexadecimal
print(format(42, '05d'))         # '00042'     — zero-pad to width 5
print(format('hi', '^10'))       # '    hi    '— center in width 10
print(format(0.256, '.1%'))      # '25.6%'     — as a percentage
```

With no spec, it behaves like `str()`:

```python
print(format(42))       # '42'
print(format(3.14))     # '3.14'
```

The `spec` is the **same mini-language** that goes after the `:` in an f-string — these are equivalent:

```python
pi = 3.14159
print(f'{pi:.2f}')           # '3.14'  — f-string
print(format(pi, '.2f'))     # '3.14'  — format() built-in
print('{:.2f}'.format(pi))   # '3.14'  — str.format() method
```

| Front-end | Looks like | One value or many? |
|---|---|---|
| **f-string** | `f'{pi:.2f}'` | many, inline in a template |
| **`str.format()`** | `'{:.2f}'.format(pi)` | many, template separate from values |
| **`format()`** | `format(pi, '.2f')` | exactly **one** value, no template |

---

## Branch 2 — Under the Hood: the `__format__` Protocol

All three front-ends resolve to the **same call**: `value.__format__(spec)`.

```python
pi = 3.14159
print(format(pi, '.2f'))         # '3.14'
print(pi.__format__('.2f'))      # '3.14'  — what format() actually calls
```

When Python sees `f'{pi:.2f}'`, it:

1. Evaluates the expression (`pi`)
2. Takes the text after the colon as the spec (`'.2f'`)
3. Calls `type(pi).__format__(pi, '.2f')` — exactly what `format()` does

So the f-string is **syntax sugar** over the same protocol. Each built-in type supplies its own `__format__` that understands the spec mini-language — `float` knows `.2f`, `int` knows `x` and `,`, `str` knows `^10`. That's why the same specs work everywhere: it's one engine with three doors.

> [!tip] Where the spec language is defined
> The spec grammar — `[fill][align][sign][width][,][.precision][type]` — is the **Format Specification Mini-Language** in the `string` module docs. It belongs to the *types*, not to f-strings: any object can define what a spec means for itself (see Branch 4).

---

## Branch 3 — When to Use format() Over an f-string

Day to day, **f-strings win**. `format()` earns its place when the **spec itself is a variable** or you're formatting programmatically:

```python
precise = False
spec = '.3f' if precise else '.1f'
x = 3.14159

print(format(x, spec))       # '3.1' — spec chosen at runtime
print(f'{x:{spec}}')         # '3.1' — f-strings can nest a spec variable too
```

Other spots where `format()` reads better:

```python
# as a function you can pass around (e.g. to map)
prices = [3.5, 10, 7.25]
print(list(map(lambda p: format(p, '.2f'), prices)))   # ['3.50', '10.00', '7.25']

# formatting one value with no surrounding text — no template noise
print(format(1_000_000, ','))    # '1,000,000'
```

---

## Branch 4 — Custom Classes Can Join In

Because everything routes through `__format__`, your own classes can respond to format specs — and then **f-strings automatically understand them too**:

```python
class Temperature:
    def __init__(self, celsius):
        self.celsius = celsius

    def __format__(self, spec):
        if spec == 'F':
            return f'{self.celsius * 9/5 + 32:.1f}°F'
        return f'{self.celsius:.1f}°C'

t = Temperature(21.5)
print(format(t))         # '21.5°C'
print(format(t, 'F'))    # '70.7°F'
print(f'{t:F}')          # '70.7°F' — the f-string hits the same __format__
```

This is the same pattern as `__str__` giving your class a `print()` representation — see [Classes and OOP](<../Core Language/Classes and OOP.md>). A real-world example: `datetime` objects define `__format__` to accept `strftime` codes, which is why `f'{now:%Y-%m-%d}'` works — see [The Datetime Module](<../Modules and Libraries/The Datetime Module.md>).

---

## Related

- **[String Formatting and Methods](<String Formatting and Methods.md>)** — the three formatting styles and the full format-spec table; this note is the "under the hood" companion.
- **[Classes and OOP](<../Core Language/Classes and OOP.md>)** — dunder methods like `__str__`; `__format__` is the same idea for format specs.
- **[The Datetime Module](<../Modules and Libraries/The Datetime Module.md>)** — `datetime.__format__` accepts `strftime` codes inside f-strings.

---

## Key Takeaways

- `format(value, spec)` formats **one value** with a spec string; with no spec it acts like `str()`.
- The spec is the **same mini-language** used after `:` in f-strings and in `str.format()` placeholders — one engine, three doors.
- All three routes call **`value.__format__(spec)`** — f-strings are syntax sugar over the same protocol.
- Reach for `format()` when the **spec is a runtime variable** or you need formatting as a passable function; otherwise prefer f-strings.
- Define `__format__` on your own classes to make them respond to custom specs in f-strings.

---

### Sources

| Source | Date | Type |
|---|---|---|
| Python built-in functions — `format()` official documentation | 2026 | Standard library reference |
| Python `string` module — Format Specification Mini-Language | 2026 | Standard library reference |
| Python data model — `object.__format__` | 2026 | Language reference |
