# The Enumerate Function

_Research compiled 2026-06-30 — Python built-in `enumerate()`, based on Automate the Boring Stuff Ch. 6_

> Companion to [List Methods](<List Methods.md>) and [Random Modules](<../Modules and Libraries/Random Modules.md>). **`enumerate()`** pairs each item of an iterable with its **index**, so a loop can use the position and the value at the same time.

---

## Branch 1 — What `enumerate()` Does

When you loop over a sequence, you often need **both** the item *and* its index (its position number). `enumerate()` gives you both at once: it wraps any iterable and yields `(index, value)` pairs.

```python
supplies = ['pens', 'staplers', 'binders']

for index, item in enumerate(supplies):
    print(index, item)
# 0 pens
# 1 staplers
# 2 binders
```

Compare the clumsy older way using `range(len(...))`:

```python
# Works, but harder to read — you index back into the list manually
for i in range(len(supplies)):
    print(i, supplies[i])
```

> [!tip] Prefer `enumerate()` over `range(len(...))`
> `enumerate()` is the Pythonic way to loop with a counter. It's cleaner, and you get the value directly instead of indexing back into the sequence every time.

---

## Branch 2 — Counting From a Different Number

By default the index starts at `0`. The optional second argument, **`start`**, changes where the count begins — useful for human-friendly numbering.

```python
supplies = ['pens', 'staplers', 'binders']

for number, item in enumerate(supplies, start=1):
    print(f'{number}. {item}')
# 1. pens
# 2. staplers
# 3. binders
```

`start` only changes the **counter**, not which items you get.

---

## Branch 3 — What Can Be Enumerated

`enumerate()` works on **any iterable** — anything you can loop over with a `for`. The index is always the position in iteration order (0, 1, 2, …), regardless of the data type.

| Type | Enumerable? | What the *value* is |
|---|---|---|
| `list` | Yes | each element |
| `tuple` | Yes | each element |
| `str` | Yes | each **character** |
| `range` | Yes | each number in the range |
| `dict` | Yes | each **key** (use `.items()` for key+value) |
| `set` | Yes | each element — but **order is not guaranteed** |
| file object / generator | Yes | each line / each yielded item |
| `int`, `float`, `bool` | **No** | not iterable → `TypeError` |

```python
# tuple
for i, v in enumerate(('a', 'b', 'c')):
    print(i, v)              # 0 a / 1 b / 2 c

# string → enumerates characters
for i, ch in enumerate('hi'):
    print(i, ch)             # 0 h / 1 i

# dict → enumerates the KEYS
prices = {'apple': 0.5, 'pear': 0.7}
for i, key in enumerate(prices):
    print(i, key)            # 0 apple / 1 pear
```

> [!warning] Dicts and sets
> Enumerating a **dict** gives you `(index, key)` — to get the value too, enumerate `prices.items()` and unpack `(i, (key, value))`. A **set** has no defined order, so the indexes you get are arbitrary. Numbers like `int` or `float` aren't iterable at all and raise `TypeError`.

---

## Branch 4 — It Returns a Lazy Iterator

`enumerate()` doesn't build a list immediately — it returns an **enumerate object** that produces pairs one at a time (memory-efficient for huge sequences). To see all the pairs at once, convert it with `list()`.

```python
supplies = ['pens', 'staplers']

print(enumerate(supplies))            # <enumerate object at 0x...>
print(list(enumerate(supplies)))      # [(0, 'pens'), (1, 'staplers')]
```

Each pair is a **tuple** `(index, value)` — which is exactly why `for index, item in ...` unpacking works.

---

## Key Takeaways

- **`enumerate(iterable, start=0)`** pairs every item with its index, yielding `(index, value)` tuples.
- Use it instead of **`range(len(...))`** when you need the position and the value together — it's cleaner and more Pythonic.
- The **`start`** argument changes only the counter (e.g. `start=1` for human-readable numbering), not the items.
- Works on **any iterable**: lists, tuples, strings (per character), ranges, dicts (keys), sets (unordered), files, generators. Non-iterables like `int`/`float` raise `TypeError`.
- It returns a **lazy iterator**, not a list — wrap it in **`list()`** to materialize all the `(index, value)` pairs.

---

### Sources

| Source | Date | Type |
|---|---|---|
| Automate the Boring Stuff, 3e — Chapter 6 (Lists) | 2026 | Book chapter |
| Python `enumerate` — official built-in functions documentation | 2026 | Standard library reference |
