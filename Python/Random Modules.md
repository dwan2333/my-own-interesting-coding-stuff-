# Random Modules

_Research compiled 2026-06-27 — Python standard library (`random` module)_

> First entry in a growing reference on Python's most useful built-in modules. This note covers **`random`** — pseudo-random number generation for floats, integers, sequences, and statistical distributions.
>
> **Related notes:** [The Logging Module](<The Logging Module.md>) — recording timestamped messages about what your program does · [The Assert Statement](<The Assert Statement.md>) — sanity-check tripwires for catching bugs early · [List Methods](<List Methods.md>) — the 11 methods of the `list` class · [The Enumerate Function](<The Enumerate Function.md>) — pairing items with their index in a loop · [Dictionary Methods](<Dictionary Methods.md>) — the 11 methods of the `dict` class · [String Formatting and Methods](<String Formatting and Methods.md>) — f-strings, `%s`, `.format()`, and the `str` methods · [The ord() and chr() Functions](<The ord and chr Functions.md>) — characters ↔ Unicode code points · [Escape Sequences](<Escape Sequences.md>) — `\n`, `\t`, quotes, raw strings, and Unicode escapes.

---

## Branch 1 — Getting Started

### What the module is

- **`random`** is part of Python's standard library — no install needed, just `import random`.
- It generates **pseudo-random** numbers using the **Mersenne Twister** algorithm: deterministic under the hood, but statistically random enough for simulations, games, sampling, and shuffling.
- **Not cryptographically secure.** For passwords, tokens, or security-sensitive randomness, use the [`secrets`](#branch-6--when-not-to-use-random) module instead.

```python
import random

print(random.random())   # e.g. 0.37444887175646646
```

### Seeding for reproducibility

`random.seed()` fixes the starting point of the generator so you get the **same sequence every run** — essential for debugging and reproducible experiments.

```python
random.seed(42)
print(random.random())   # 0.6394267984578837  (same every time)
print(random.random())   # 0.025010755222666936

random.seed(42)          # reset to the same seed
print(random.random())   # 0.6394267984578837  (repeats!)
```

---

## Branch 2 — Random Floats

| Function | Returns | Range |
|---|---|---|
| `random.random()` | float | `[0.0, 1.0)` — includes 0, excludes 1 |
| `random.uniform(a, b)` | float | `[a, b]` — any two bounds, order-independent |

```python
import random

print(random.random())           # 0.0 <= x < 1.0
print(random.uniform(1, 10))     # e.g. 7.34 — a float between 1 and 10
print(random.uniform(10, 1))     # works too; bounds can be reversed
```

> [!tip] Scaling `random()`
> `random.random() * n` gives a float in `[0, n)` — a quick way to scale without `uniform`.

---

## Branch 3 — Random Integers

| Function | Returns | Notes |
|---|---|---|
| `random.randint(a, b)` | int in `[a, b]` | **Both endpoints included** |
| `random.randrange(stop)` | int in `[0, stop)` | Stop **excluded**, like `range()` |
| `random.randrange(start, stop[, step])` | int | Respects a step |

```python
import random

print(random.randint(1, 6))         # simulate a die roll: 1..6 inclusive
print(random.randrange(10))         # 0..9
print(random.randrange(0, 100, 5))  # 0, 5, 10, ... 95 (multiples of 5)
```

> [!warning] `randint` vs `randrange`
> `randint(1, 6)` **can** return 6. `randrange(1, 6)` **cannot** — it stops at 5. This off-by-one trips people up constantly.

---

## Branch 4 — Working With Sequences

This is where `random` is most useful day-to-day — picking from and reordering lists.

### Pick one item — `random.choice()`

```python
import random

colors = ["red", "green", "blue"]
print(random.choice(colors))     # e.g. "green"
```

### Pick several items

| Function | Replacement? | Duplicates? | Key argument |
|---|---|---|---|
| `random.choices(seq, k=n)` | **with** replacement | yes | `weights`, `k` |
| `random.sample(seq, k=n)` | **without** replacement | no | `k` |

```python
import random

# choices: same item can appear more than once
print(random.choices(["a", "b", "c"], k=5))        # e.g. ['a', 'c', 'c', 'a', 'b']

# weighted choices — 'win' is 10x more likely than 'lose'
print(random.choices(["win", "lose"], weights=[10, 1], k=3))

# sample: unique items, like dealing cards
print(random.sample(range(1, 50), k=6))            # 6 distinct lottery numbers
```

### Shuffle in place — `random.shuffle()`

Reorders a **mutable** sequence (like a list) directly; returns `None`.

```python
import random

deck = list(range(1, 53))
random.shuffle(deck)             # deck is now reordered
print(deck[:5])                  # e.g. [27, 3, 51, 14, 40]
```

> [!warning] `shuffle` mutates and returns `None`
> `deck = random.shuffle(deck)` is a common bug — it sets `deck` to `None`. Shuffle the list, then use it; don't assign the result. For a shuffled **copy**, use `random.sample(deck, k=len(deck))`.

---

## Branch 5 — Statistical Distributions

When you need numbers that follow a real-world distribution rather than uniform randomness.

| Function | Distribution | Common use |
|---|---|---|
| `random.gauss(mu, sigma)` | Normal (Gaussian) | Heights, measurement noise |
| `random.normalvariate(mu, sigma)` | Normal (thread-safe variant) | Same, safer in threads |
| `random.triangular(low, high, mode)` | Triangular | Rough estimates with a "most likely" value |
| `random.expovariate(lambd)` | Exponential | Time between events (arrivals, decay) |

```python
import random

print(random.gauss(0, 1))         # standard normal: mean 0, std-dev 1
print(random.gauss(170, 10))      # heights around 170 cm
print(random.triangular(1, 10, 3))  # between 1 and 10, peaking near 3
print(random.expovariate(1/5))    # wait times averaging 5 units
```

---

## Branch 6 — When *Not* to Use `random`

`random` is predictable: anyone who learns the internal state can reproduce its output. **Never use it for security.**

```python
import secrets

print(secrets.choice(["a", "b", "c"]))  # cryptographically secure pick
print(secrets.randbelow(100))           # secure int in [0, 100)
print(secrets.token_hex(16))            # secure random token, e.g. for API keys
```

| Need | Use |
|---|---|
| Games, simulations, sampling, shuffling | `random` |
| Passwords, tokens, secrets, crypto keys | `secrets` |

---

## Key Takeaways

- `import random` — built-in, **pseudo-random**, based on the Mersenne Twister.
- **`random()`** → float `[0,1)`; **`uniform(a,b)`** → float in a range; **`randint(a,b)`** → int **inclusive** of both ends.
- Watch the boundary: `randint` includes the top end, `randrange` excludes it.
- For sequences: **`choice`** (one), **`choices`** (many, with replacement + weights), **`sample`** (many, unique), **`shuffle`** (reorder in place — returns `None`).
- **`seed()`** makes runs reproducible; distribution functions (`gauss`, `expovariate`, …) model real-world randomness.
- For anything security-related, switch to **`secrets`**, not `random`.

---

### Sources

| Source | Date | Type |
|---|---|---|
| Python `random` — official CPython documentation | 2026 | Standard library reference |
| Python `secrets` — official CPython documentation | 2026 | Standard library reference |
