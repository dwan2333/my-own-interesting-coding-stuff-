# Dictionary Methods

_Research compiled 2026-06-30 — Python built-in `dict` methods, based on Automate the Boring Stuff Ch. 7_

> Companion to [List Methods](<List Methods.md>) and [Random Modules](<../Modules and Libraries/Random Modules.md>). A dictionary stores **key → value** pairs. The `dict` class has **11 methods**; Chapter 7 covers 5, and the other 6 (marked **added**) are essential day-to-day tools.

---

## Branch 1 — Viewing Keys, Values, and Pairs

These three return live **view objects** that reflect the dictionary and can be looped over or converted with `list()`.

### `keys()` — the keys

```python
spam = {'color': 'red', 'age': 42}
print(list(spam.keys()))      # ['color', 'age']
```

### `values()` — the values

```python
spam = {'color': 'red', 'age': 42}
print(list(spam.values()))    # ['red', 42]
```

### `items()` — key–value pairs as tuples

Each pair comes out as a `(key, value)` tuple, so you can unpack them directly in a loop.

```python
spam = {'color': 'red', 'age': 42}
for k, v in spam.items():
    print(k, '->', v)
# color -> red
# age -> 42
```

> [!note] View objects, not lists
> `keys()`, `values()`, and `items()` return `dict_keys` / `dict_values` / `dict_items` views — they update live if the dict changes. Wrap them in `list()` when you need an actual list to index or store.

---

## Branch 2 — Safe Access Without Errors

Reading a missing key with `spam['missing']` raises a **`KeyError`** and crashes. These two methods avoid that.

### `get(key, default=None)` — read with a fallback

Returns the value if the key exists, otherwise the fallback — **without** adding anything to the dict.

```python
picnic = {'apples': 5, 'cups': 2}
print(picnic.get('eggs', 0))    # 0   (key missing → fallback)
print(picnic.get('apples', 0))  # 5   (key present → its value)
print(picnic)                   # {'apples': 5, 'cups': 2}  (unchanged)
```

### `setdefault(key, default)` — read, or insert if missing

Like `get()`, but if the key is **absent** it also **inserts** it with the default. Great for initializing.

```python
spam = {'name': 'Pooka'}
spam.setdefault('color', 'black')   # 'color' missing → added
spam.setdefault('name', 'Zophie')   # 'name' present → left alone
print(spam)                         # {'name': 'Pooka', 'color': 'black'}
```

A classic use — counting characters without a `KeyError`:

```python
message = 'hello'
counts = {}
for ch in message:
    counts.setdefault(ch, 0)
    counts[ch] += 1
print(counts)                       # {'h': 1, 'e': 1, 'l': 2, 'o': 1}
```

---

## Branch 3 — Adding & Merging *(added)*

### `update(other)` — add/overwrite from another dict

Copies another dict's pairs in. Existing keys are **overwritten**; new keys are added.

```python
spam = {'a': 1, 'b': 2}
spam.update({'b': 20, 'c': 3})
print(spam)                     # {'a': 1, 'b': 20, 'c': 3}
```

---

## Branch 4 — Removing Items *(added)*

### `pop(key, default)` — remove a key and return its value

Deletes `key` and hands back its value. Supply a default to avoid a `KeyError` when the key is missing.

```python
spam = {'a': 1, 'b': 2}
print(spam.pop('a'))            # 1
print(spam)                     # {'b': 2}
print(spam.pop('z', 'n/a'))     # 'n/a'  (missing key → default, no crash)
```

### `popitem()` — remove and return the last-inserted pair

Returns a `(key, value)` tuple. Handy for draining a dict; raises `KeyError` if it's empty.

```python
spam = {'a': 1, 'b': 2}
print(spam.popitem())           # ('b', 2)
print(spam)                     # {'a': 1}
```

### `clear()` — remove everything

```python
spam = {'a': 1, 'b': 2}
spam.clear()
print(spam)                     # {}
```

---

## Branch 5 — Copying & Creating *(added)*

### `copy()` — a shallow copy

Returns a **new** dict, so changes to the copy don't affect the original (nested objects are still shared — use `copy.deepcopy()` for those).

```python
spam = {'a': 1}
backup = spam.copy()
backup['b'] = 2
print(spam)                     # {'a': 1}        (unchanged)
print(backup)                   # {'a': 1, 'b': 2}
```

### `fromkeys(keys, value)` — build a dict from a list of keys

A **class method** — call it on `dict`. Every key gets the same starting value.

```python
new = dict.fromkeys(['a', 'b', 'c'], 0)
print(new)                      # {'a': 0, 'b': 0, 'c': 0}
```

---

## Branch 6 — Key Operations (not methods)

- **Square brackets** — read `spam['color']`, or assign `spam['color'] = 'red'` (adds the key if new). Keys can be strings, numbers, or other immutable types — **not lists**.
- **`in` / `not in`** — test for a **key**: `'color' in spam` → `True/False`. Checking `in spam` looks at keys, not values (use `value in spam.values()` for values).

```python
spam = {'color': 'red'}
print('color' in spam)            # True
print('red' in spam)              # False  (that's a value, not a key)
print('red' in spam.values())     # True
```

---

## Reference Table — All 11 Methods

| Method | Source | What it does | Returns |
|---|---|---|---|
| `keys()` | Ch. 7 | View of the keys | `dict_keys` |
| `values()` | Ch. 7 | View of the values | `dict_values` |
| `items()` | Ch. 7 | View of `(key, value)` pairs | `dict_items` |
| `get(key, default)` | Ch. 7 | Value, or fallback if missing (no insert) | value |
| `setdefault(key, default)` | Ch. 7 | Value, inserting the default if missing | value |
| `update(other)` | **added** | Merge in another dict (overwrites) | `None` |
| `pop(key, default)` | **added** | Remove key, return its value | value |
| `popitem()` | **added** | Remove and return the last pair | `(k, v)` tuple |
| `clear()` | **added** | Remove all pairs | `None` |
| `copy()` | **added** | Shallow copy | new `dict` |
| `fromkeys(keys, value)` | **added** | Build a dict from keys, all set to `value` | new `dict` |

---

## Key Takeaways

- Read safely with **`get(key, default)`** (never inserts) or **`setdefault(key, default)`** (inserts the default if the key is missing) — both dodge `KeyError`.
- **`keys()` / `values()` / `items()`** return live **views**; wrap in `list()` to materialize. Loop `items()` with `for k, v in ...`.
- **`update()`** merges dicts (overwriting duplicates); **`pop(key, default)`** removes and returns a value safely; **`clear()`** empties the dict.
- **`copy()`** is a shallow copy; **`dict.fromkeys(keys, value)`** builds a fresh dict with every key set to the same value.
- **`in`** tests for a **key**, not a value — use `x in spam.values()` to search values.

---

### Sources

| Source | Date | Type |
|---|---|---|
| Automate the Boring Stuff, 3e — Chapter 7 (Dictionaries) | 2026 | Book chapter |
| Python `dict` — official data structures documentation | 2026 | Standard library reference |
