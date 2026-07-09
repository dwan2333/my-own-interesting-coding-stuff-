# The Collections Module

_Research compiled 2026-07-08 — Python standard library `collections`_

> Part of the [Python Reference](<../Python Reference (Main).md>). The **`collections`** module provides upgraded container types — smarter versions of the built-in `list`, `dict`, and `tuple` for common jobs. It's built in (`import collections`), and the five most useful members are **`Counter`**, **`defaultdict`**, **`namedtuple`**, **`deque`**, and **`OrderedDict`**.

---

## Branch 1 — `Counter` — tally things automatically

`Counter` counts how many times each item appears. Give it any iterable and it returns a dict-like object of `{item: count}`.

```python
from collections import Counter

c = Counter('banana')
print(c)                    # Counter({'a': 3, 'n': 2, 'b': 1})
print(c['a'])               # 3    (missing items return 0, not KeyError)

votes = Counter(['yes', 'no', 'yes', 'yes', 'no'])
print(votes.most_common(1)) # [('yes', 3)]   — the top item(s)
```

| Feature | What it does |
|---|---|
| `Counter(iterable)` | tally every item into `{item: count}` |
| `c[item]` | the count (missing → `0`, no error) |
| `.most_common(n)` | the `n` highest-count items as `(item, count)` pairs |

> [!tip] The go-to for "what's the most frequent…?"
> Word frequencies, vote tallies, most-common characters — `Counter(...).most_common(n)` answers these in one line.

---

## Branch 2 — `defaultdict` — a dict that never raises `KeyError`

A normal dict raises `KeyError` when you read a missing key. A `defaultdict` instead **creates a default value automatically** the first time a key is touched. You give it a *factory* — `list`, `int`, `set`, etc.

```python
from collections import defaultdict

# group items into lists — no need to check "if key exists" first
groups = defaultdict(list)
groups['fruit'].append('apple')     # key missing → auto-creates []
groups['fruit'].append('pear')
print(dict(groups))                 # {'fruit': ['apple', 'pear']}

# count with int (default 0) — like a mini Counter
tally = defaultdict(int)
for ch in 'banana':
    tally[ch] += 1                  # missing → starts at 0
print(dict(tally))                  # {'b': 1, 'a': 3, 'n': 2}
```

| Factory | Missing key becomes | Good for |
|---|---|---|
| `defaultdict(list)` | `[]` | grouping items into lists |
| `defaultdict(int)` | `0` | counting |
| `defaultdict(set)` | `set()` | collecting unique items per key |

> [!note] `defaultdict(list)` vs `dict.setdefault`
> Both avoid the "check if the key exists" dance. `defaultdict` is cleaner when *every* access should have a default; `setdefault` (see [Dictionary Methods](<Dictionary Methods.md>)) is fine for a one-off.

---

## Branch 3 — `namedtuple` — a tuple with named fields

A [tuple](<../Data Structures/Tuples.md>) is fixed and lightweight, but `t[0]`, `t[1]` is cryptic. A `namedtuple` gives each position a **name**, so you can write `p.x` instead of `p[0]` — readable *and* still a real tuple.

```python
from collections import namedtuple

Point = namedtuple('Point', ['x', 'y'])   # define the type once
p = Point(3, 4)

print(p)        # Point(x=3, y=4)
print(p.x, p.y) # 3 4     — access by name
print(p[0])     # 3       — still works like a tuple
```

Great for small fixed "records" (a point, a color, a row) where a full class is overkill but bare tuples are unclear.

---

## Branch 4 — `deque` — fast adds/removes at **both** ends

A `deque` ("deck", double-ended queue) is like a list, but adding or removing at the **front** is fast (a list's `insert(0, …)` / `pop(0)` is slow). Perfect for queues and sliding windows.

```python
from collections import deque

d = deque([1, 2, 3])
d.appendleft(0)     # add to the FRONT
d.append(4)         # add to the back
print(d)            # deque([0, 1, 2, 3, 4])
print(d.popleft())  # 0   — remove from the front
```

With **`maxlen`**, a deque auto-drops old items as new ones arrive — a ready-made "last N things" buffer:

```python
last3 = deque(maxlen=3)
for i in range(5):
    last3.append(i)
print(last3)        # deque([2, 3, 4], maxlen=3)  — only the last 3 kept
```

---

## Branch 5 — `OrderedDict` (mostly historical now)

Since Python 3.7, **regular dicts already keep insertion order**, so you rarely need `OrderedDict` just for ordering. It's still useful for its extra method **`move_to_end()`** (handy for LRU-cache-style logic):

```python
from collections import OrderedDict

od = OrderedDict([('a', 1), ('b', 2)])
od.move_to_end('a')          # push 'a' to the end
print(list(od.items()))      # [('b', 2), ('a', 1)]
```

---

## Key Takeaways

- **`Counter(iterable)`** tallies items; `.most_common(n)` gives the top `n`. Missing items count as `0`.
- **`defaultdict(factory)`** auto-creates a default (`list`→`[]`, `int`→`0`, `set`→`set()`) so missing keys never raise `KeyError` — ideal for grouping and counting.
- **`namedtuple('Name', [fields])`** is a tuple with **named fields** (`p.x`) — a lightweight readable record.
- **`deque`** gives fast `appendleft`/`popleft` at the front; `deque(maxlen=n)` is an auto-trimming "last N" buffer.
- **`OrderedDict`** is mostly legacy now (plain dicts keep order since 3.7); reach for it only for `move_to_end()`.

---

## Exercises

> [!example] Exercise 1 — Most common word
> **Problem.** Given `words = ['a', 'b', 'a', 'c', 'a', 'b']`, use `Counter` to find the single most common word and how many times it appears.
>
> > [!success]- Click to reveal solution
> > **Solution.** `most_common(1)` returns a list with one `(item, count)` pair.
> > ```python
> > from collections import Counter
> > words = ['a', 'b', 'a', 'c', 'a', 'b']
> > print(Counter(words).most_common(1))
> > ```
> > **Answer.** `[('a', 3)]` ✓

> [!example] Exercise 2 — Group names by first letter
> **Problem.** Given `names = ['Ann', 'Bo', 'Amy', 'Ben']`, build a dict mapping each first letter to the list of names starting with it, using `defaultdict`.
>
> > [!success]- Click to reveal solution
> > **Solution.** `defaultdict(list)` lets you `.append` without pre-creating each list.
> > ```python
> > from collections import defaultdict
> > names = ['Ann', 'Bo', 'Amy', 'Ben']
> > groups = defaultdict(list)
> > for name in names:
> >     groups[name[0]].append(name)
> > print(dict(groups))
> > ```
> > **Answer.** `{'A': ['Ann', 'Amy'], 'B': ['Bo', 'Ben']}` ✓

---

### Sources

| Source | Date | Type |
|---|---|---|
| Python `collections` — official documentation | 2026 | Standard library reference |
| Verified against Python 3.14 on `E:\Python` | 2026-07-08 | Local test |
