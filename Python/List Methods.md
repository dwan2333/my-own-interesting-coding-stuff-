# List Methods

_Research compiled 2026-06-30 — Python built-in `list` methods, based on Automate the Boring Stuff Ch. 6_

> Companion to [Random Modules](<Random Modules.md>). The `list` class has **11 methods**. Chapter 6 covers 6 of them; the other 5 (marked **added**) are just as worth knowing. Most list methods change the list **in place** and return `None` — don't assign their result back to a variable.

---

## Branch 1 — Adding Items

### `append(x)` — add one item to the end

```python
spam = ['cat', 'dog', 'bat']
spam.append('moose')
print(spam)              # ['cat', 'dog', 'bat', 'moose']
```

### `insert(i, x)` — add an item at a specific index

```python
spam = ['cat', 'dog', 'bat']
spam.insert(1, 'chicken')
print(spam)              # ['cat', 'chicken', 'dog', 'bat']
```

### `extend(iterable)` — add **all** items from another iterable *(added)*

The key difference from `append`: `extend` unpacks the other iterable into separate items, while `append` would add it as one nested item.

```python
spam = ['a', 'b']
spam.extend([1, 2, 3])
print(spam)              # ['a', 'b', 1, 2, 3]

spam2 = ['a', 'b']
spam2.append([1, 2, 3])
print(spam2)             # ['a', 'b', [1, 2, 3]]  <-- one nested list!
```

> [!warning] `append` vs `extend`
> `append([4, 5])` adds the list as a **single item**; `extend([4, 5])` adds `4` and `5` as **separate items**. Mixing these up is one of the most common list bugs.

---

## Branch 2 — Removing Items

### `remove(x)` — remove the first item equal to a value

Deletes by **value**. Raises `ValueError` if the value isn't present.

```python
spam = ['cat', 'bat', 'rat', 'elephant']
spam.remove('bat')
print(spam)              # ['cat', 'rat', 'elephant']
```

### `pop(i=-1)` — remove **and return** the item at an index *(added)*

Deletes by **index** and hands the item back. With no argument it removes the last item — handy for using a list as a stack.

```python
spam = ['cat', 'rat', 'elephant']
last = spam.pop()        # no index → removes the last item
print(last)              # 'elephant'
print(spam)              # ['cat', 'rat']

first = spam.pop(0)      # remove by index
print(first)             # 'cat'
```

### `clear()` — remove every item *(added)*

```python
spam = [1, 2, 3]
spam.clear()
print(spam)              # []
```

> [!tip] `remove` vs `pop`
> `remove(x)` deletes by **value** and returns nothing. `pop(i)` deletes by **index** and **returns** the removed item. Use `pop` when you still need the value you're taking out.

---

## Branch 3 — Finding & Counting

### `index(x)` — find the index of the first matching value

Returns the position. Raises `ValueError` if the value isn't present.

```python
spam = ['hello', 'hi', 'howdy']
print(spam.index('hi'))   # 1
```

### `count(x)` — count how many times a value appears *(added)*

```python
spam = ['cat', 'dog', 'cat', 'cat']
print(spam.count('cat'))  # 3
print(spam.count('fish')) # 0  (not found → just zero, no error)
```

---

## Branch 4 — Reordering

### `sort(key=None, reverse=False)` — sort the list in place

Sorts numbers numerically and strings in **ASCIIbetical** order (all uppercase before all lowercase). Use `key=str.lower` for true case-insensitive alphabetical order, and `reverse=True` for descending.

```python
nums = [2, 5, 3.14, 1, -7]
nums.sort()
print(nums)               # [-7, 1, 2, 3.14, 5]

words = ['banana', 'Apple', 'cherry']
words.sort(key=str.lower)         # ignore case
print(words)              # ['Apple', 'banana', 'cherry']

nums.sort(reverse=True)
print(nums)               # [5, 3.14, 2, 1, -7]
```

> [!warning] `sort()` returns `None`
> `spam = spam.sort()` is a classic bug — it sets `spam` to `None`. Call `spam.sort()` on its own line, then use `spam`. (For a sorted **copy** that leaves the original alone, use the built-in `sorted(spam)` instead.)

### `reverse()` — reverse the order in place

```python
spam = ['cat', 'dog', 'moose']
spam.reverse()
print(spam)               # ['moose', 'dog', 'cat']
```

---

## Branch 5 — Copying

### `copy()` — make a shallow copy *(added)*

Returns a **new** list, so changes to the copy don't touch the original. (Method form of the `spam[:]` slice trick.)

```python
spam = ['cat', 'dog']
backup = spam.copy()
backup.append('rat')
print(spam)               # ['cat', 'dog']        (unchanged)
print(backup)             # ['cat', 'dog', 'rat']
```

> [!note] "Shallow" copy
> `copy()` duplicates the outer list, but **nested lists inside it are still shared**. To copy nested lists too, use `copy.deepcopy()` from the `copy` module.

---

## Reference Table — All 11 Methods

| Method | Source | What it does | Returns |
|---|---|---|---|
| `append(x)` | Ch. 6 | Add one item to the end | `None` |
| `insert(i, x)` | Ch. 6 | Insert `x` at index `i` | `None` |
| `extend(iterable)` | **added** | Add all items from an iterable | `None` |
| `remove(x)` | Ch. 6 | Remove first item equal to `x` | `None` |
| `pop(i=-1)` | **added** | Remove and return item at index `i` | the item |
| `clear()` | **added** | Remove all items | `None` |
| `index(x)` | Ch. 6 | Index of first `x` | `int` |
| `count(x)` | **added** | Number of times `x` appears | `int` |
| `sort(key, reverse)` | Ch. 6 | Sort in place | `None` |
| `reverse()` | Ch. 6 | Reverse in place | `None` |
| `copy()` | **added** | Shallow copy | new `list` |

---

## Key Takeaways

- Most list methods mutate the list **in place** and return `None` — never write `spam = spam.sort()` or `spam = spam.reverse()`.
- **`append`** adds one item; **`extend`** adds many. **`remove`** deletes by value; **`pop`** deletes by index and returns the item.
- **`index`** and **`remove`** raise `ValueError` when the value is missing; **`count`** just returns `0`.
- For a sorted/duplicated result *without* changing the original, reach for the built-ins **`sorted(spam)`** and slicing **`spam[:]`** / **`spam.copy()`**.
- `copy()` is **shallow** — nested lists stay shared; use `copy.deepcopy()` for those.

---

### Sources

| Source | Date | Type |
|---|---|---|
| Automate the Boring Stuff, 3e — Chapter 6 (Lists) | 2026 | Book chapter |
| Python `list` — official data structures documentation | 2026 | Standard library reference |
