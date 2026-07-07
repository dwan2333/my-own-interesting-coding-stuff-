# The Assert Statement

_Research compiled 2026-06-30 — Python built-in `assert` statement, based on Automate the Boring Stuff Ch. 5_

> Companion to [The Logging Module](<The Logging Module.md>) — the other debugging tool from the same chapter. **`assert` is a statement, not a module or function**, so there's nothing to import and no parentheses around it.

---

## Branch 1 — What `assert` Does

An **assertion** is a sanity check that says *"I'm certain this is true at this point in my program."* You write a condition you believe must hold; if you're right, nothing happens and the program continues. If you're **wrong**, Python raises an `AssertionError` and crashes immediately — right at the spot where your assumption broke, instead of letting a bad value travel deeper and cause a confusing error later.

Think of it as a tripwire for *"this should never happen"* situations.

```python
ages = [25, 30, 42]
assert len(ages) > 0          # true → nothing happens, program continues
print("Passed the check, list is not empty")
```

If the condition is **False**, it stops the program:

```python
total = -5
assert total >= 0             # False → raises AssertionError and crashes here
print("This line never runs")
```

> [!note] Syntax
> `assert <condition>` — checks the condition.
> `assert <condition>, <message>` — same, but shows your message in the error if it fails.

---

## Branch 2 — Adding a Helpful Message

On its own, a failed assertion just says `AssertionError` with no explanation. Add a comma and a message to say **what** went wrong — and include the bad value so you can see it.

```python
age = -3
assert age >= 0, f'age should never be negative, but got {age}'
```

The crash then reads:

```text
AssertionError: age should never be negative, but got -3
```

That message turns a mystery crash into an immediate diagnosis.

---

## Branch 3 — When to Use It (and When Not To)

Assertions are for **catching your own bugs during development** — checking assumptions that should *always* be true if your code is correct.

| Use `assert` for… | Use `if` / `raise` for… |
|---|---|
| Internal sanity checks ("this list is never empty here") | Validating **user input** or external data |
| Catching programmer mistakes early | Errors you expect to happen sometimes |
| Documenting an assumption in code | Anything that must run in production |

```python
def apply_discount(price, percent):
    assert 0 <= percent <= 100, f'percent out of range: {percent}'   # my own bug check
    return price * (1 - percent / 100)

print(apply_discount(50, 20))    # 40.0
```

> [!warning] Do NOT use `assert` for user input or security checks
> Assertions can be switched off (see Branch 4). If you rely on one to validate a password, a file, or form data, that check vanishes when assertions are disabled. For data that *might legitimately be bad*, use a real `if` test that raises an exception instead.

---

## Branch 4 — Assertions Can Be Turned Off

Running Python with the **`-O`** (optimize) flag disables **every** assertion in the program:

```text
python -O myprogram.py      # all assert statements are skipped
```

This is why assertions are a **development-time** tool: they're meant to be cheap safety nets you can strip out for a production run, *not* guarantees you depend on. If a check must always run, it can't be an `assert`.

---

## Branch 5 — The Tuple Gotcha

Because `assert` is a statement (not a function), **never wrap the condition and message in parentheses** — that creates a tuple, and a non-empty tuple is always truthy, so the assertion can *never* fail.

```python
# WRONG — always passes, the check is silently dead
assert (2 + 2 == 5, 'math is broken')

# RIGHT — no parentheses around the pair
assert 2 + 2 == 5, 'math is broken'
```

The first version never raises anything, even though `2 + 2 == 5` is false. This is a classic silent bug.

---

## Key Takeaways

- **`assert`** is a built-in statement that checks a condition you believe is true; if it's **False**, it raises `AssertionError` and stops the program at that exact line.
- Syntax: `assert condition` or `assert condition, 'message'` — add a message (with the bad value) to make failures self-explanatory.
- Use it for **internal sanity checks and catching your own bugs**, not for validating user input or security-critical data.
- Assertions can be **disabled** with `python -O`, so never rely on them for checks that must always run.
- **Gotcha:** `assert (cond, 'msg')` with parentheses is always true — drop the parentheses.

---

### Sources

| Source | Date | Type |
|---|---|---|
| Automate the Boring Stuff, 3e — Chapter 5 (Assertions) | 2026 | Book chapter |
| Python `assert` — official language reference | 2026 | Language reference |
