# Chapter 1 — Abstract Data Types

_Notes compiled 2026-06-21 — Rance D. Necaise, *Data Structures and Algorithms Using Python*, Ch. 1, with NotebookLM-assisted summaries (written for a first-time reader) and main-agent verification of the technical claims._

> [!tip] Companion notes in this vault
> This chapter's **Bag** is built on a Python **[List](<../Python/Data Structures/List Methods.md>)**; its **iterators** are the machinery that `for` loops and **[The Enumerate Function](<../Python/Data Structures/The Enumerate Function.md>)** rely on; and §1.2 weighs a list against a **[Dictionary](<../Python/Data Structures/Dictionary Methods.md>)** for storage.

---

> [!info] Chapter Essence — in one breath
> This chapter is about a single, powerful idea: **separate *what* something does from *how* it works.** An **abstract data type (ADT)** is a "black box" — you're told which operations it offers (its *interface*), but not the messy internals. A **data structure** is one particular way of building those internals. Keeping the two apart lets you use tools without understanding their wiring, and lets the wiring be swapped for something better without breaking anything that relies on it. The chapter makes this concrete with three examples: a **Date**, a **Bag**, and a small **student-records** program.

> [!tip] Never coded before? Three words to anchor everything
> - **Algorithm** — a precise, step-by-step recipe for solving a problem (like a recipe for a cake).
> - **Data type** — a *category* of data (whole numbers, text, …) bundled with the operations you're allowed to do to it (add, compare, …). It's what gives meaning to the raw 0s and 1s a computer actually stores.
> - **Abstraction** — deliberately *hiding* detail so you can focus only on what matters. You use a calculator's √ button without knowing how it computes the root — that's abstraction.

---

## 1.1 Introduction — The "What" vs. the "How"

A computer, at the bottom, only stores **0s and 1s** — and the same string of bits could mean a number, a letter, or a pixel. Meaning is layered *on top* through **abstraction**. Each layer hides the one beneath it:

![Figure 1.1 — Levels of abstraction: hardware at the bottom, and each layer above hides the details of the one below it](dsa_fig_1.1_levels_of_abstraction.png)

> [!definition] The two kinds of abstraction
> The book splits abstraction into two flavours — one about **actions**, one about **data**:
> - **Procedural (functional) abstraction** — using a **function or method** knowing *what* it does but **ignoring *how*** it does it. You call the square-root function `sqrt(x)` and trust it returns the root; you don't need to know the algorithm inside. The *action* is a black box.
> - **Data abstraction** — separating a **data type's** properties (its values and the operations on them) from **how that type is implemented**. You use Python strings constantly without knowing how the characters are stored in memory or how `.upper()` works internally. The *data* is a black box.
>
> An **ADT combines both**: it bundles data (data abstraction) with a set of operations you call without seeing their internals (procedural abstraction).

> [!tip] How does high-level code turn into those assembly instructions? A translator.
> The CPU only understands **machine code** — raw binary instructions (assembly language is just a human-readable spelling of those). The processor has no idea what `x = a + b - 5` means. Sitting **between** the high-level language and the hardware is a **translator** that converts your code into the low-level instructions the machine actually runs:
> - A **compiler** translates the *whole* program into machine code **ahead of time**; you then run the finished result. (C, C++, and Rust work this way.)
> - An **interpreter** translates and runs the code **as it goes**, roughly line by line. (Python works this way — it first turns your code into compact **bytecode**, which the Python runtime then executes.)
>
> Either way, **you never hand-write the load/add/store steps** — the translator generates them for you from your one-line expression. It has a ready-made low-level pattern for **each operation**: `+` becomes an **add** instruction, a test like `a > b` becomes **compare-and-jump** instructions — the translator just fills in *your* specific variables and emits the pattern. That translator *is* the bridge between the high-level layer and the assembly layer in Figure 1.1.

> [!example] Abstraction in layers — the same sum, from Python down to the hardware
> Figure 1.1 shows abstraction stacked in **layers**, each one hiding the messy layer beneath it. The book illustrates this with a simple calculation, `x = a + b − 5`:
> - **High-level language** (Python, etc.) — you just write `x = a + b - 5`. Clean, familiar, one line.
> - **Assembly language** — the processor can't do that in one go. The expression has to be broken into individual instructions that shuttle values between **memory** (where variables like `a`, `b`, `x` live) and **registers** (tiny, super-fast storage slots inside the CPU), performing **one operation at a time**:
> ```text
> loadFromMem(R1, 'a')    # copy a from memory into register R1
> loadFromMem(R2, 'b')    # copy b into register R2
> add R0, R1, R2          # R0 = R1 + R2   (this is a + b)
> sub R0, R0, 5           # R0 = R0 − 5
> storeToMem(R0, 'x')     # copy the result back to memory as x
> ```
> - **Hardware** — at the very bottom, even those instructions become binary values and logic circuits flipping 0s and 1s.
>
> Each higher layer **hides** the one below. Writing `x = a + b - 5` is an *abstraction* over all those load/add/store steps — you get to think about the **math**, while the language quietly picks the right hardware instructions for you. That's the payoff of abstraction: you utilize the machine's hardware **without** hand-writing hardware instructions.

> [!tip] The mind-blowing part: even data types are an illusion over raw numbers
> It's not just math. The CPU has **no concept** of a string, a list, or a boolean — it only understands **binary numbers**. High-level languages *fake* those data types using **encoding rules**, then translate every operation on them down into "move and add these numbers in memory." This is **data abstraction** at the deepest level:
> - **Strings** — each character is stored as its **Unicode/ASCII number**. `"CAT"` is really `67, 65, 84` sitting in three consecutive memory slots; printing it just decodes the numbers back into letters.
> - **Lists** — the values go into consecutive memory slots, and the language remembers the **starting address** so it can find them again.
> - **Booleans** — `True` is simply the number `1`; `False` is `0`.
>
> So *every* high-level feature — arithmetic **and** data types — ultimately reduces to **adding, subtracting, and moving numbers around in memory**. Data abstraction is what lets you think "a string of letters" while the hardware only ever sees a row of numbers.

> [!definition] The two central words
> - An **Abstract Data Type (ADT)** specifies a set of data values **and** the operations allowed on them — describing *what* it does while **hiding** how it does it. The approved list of operations it exposes is its **interface**.
> - A **data structure** is the concrete way the data is actually *organized and stored* inside memory — the *how*.
> - The code that makes the interface actually work, using some data structure, is the **implementation**.
> - A **client** (the book says "user program") is whatever code *uses* the ADT through its interface.

![Figure 1.2 — A "string ADT" as a black box: the user program touches only the interface (str, upper, lower, …); the implementation details are sealed inside](dsa_fig_1.2_adt_vs_implementation.png)

> [!definition] The four kinds of buttons — every ADT operation falls into one of these categories
> The book sorts everything an interface can offer into **four categories** (added here — presented right alongside Figure 1.2 in the text):
>
> | Category | What it does | Date ADT (§1.2) | Bag ADT (§1.3) | Python types you already use |
> |---|---|---|---|---|
> | **Constructor** | creates and initializes a new instance | `Date(10, 31, 2023)` | `Bag()` | `list()`, `dict()`, `int("42")` |
> | **Accessor** | returns data from the instance **without modifying it** | `day()`, `monthName()`, `isLeapYear()` | `length()`, `contains(item)` | `len(nums)`, `x in d`, `s.upper()` |
> | **Mutator** | **modifies** the contents of the instance | `advanceBy(days)` | `add(item)`, `remove(item)` | `nums.append(x)`, `nums.sort()`, `d.update(…)` |
> | **Iterator** | hands out the components **one at a time**, sequentially | — (a single date has no items to walk) | `iterator()` — the whole of §1.4 | what a `for` loop drives |
>
> Why the sorting habit is worth building:
> - **Reading a new ADT**: bin its buttons into these four and you instantly know which calls are *safe anywhere* (accessors — they can't change anything) and which ones *change state* (mutators — handle with care).
> - **Spotting immutability**: a type with **no mutators can never change** after construction. That's why `s.upper()` is an *accessor returning a new string* rather than a mutator — Python strings ship with zero mutators (the "returns a **new** string" warning in [String Formatting and Methods](<../Python/Strings and Text/String Formatting and Methods.md>) is this exact idea). The partial `Date` class in §1.2 is the same: after the constructor, every implemented method only *reads* `_julianDay`.
> - **Designing your own**: the Bag is mutator-heavy because a container's whole job is changing contents; a Date is accessor-heavy because a date *is* a fixed value. What you're building dictates the mix.

> [!tip] The analogy that makes it click — a television
> - The **ADT** is the *idea* of a TV: a box that shows moving pictures and plays sound.
> - The **interface** is the **remote control** — a fixed set of buttons: Power, Volume Up, Change Channel. *You* are the **client** pressing them.
> - The **implementation / data structure** is the wires, chips, and screen inside — the *how*.
>
> You only need the remote (interface) to know *what* the TV does. And if you buy a TV with a better screen (a new implementation), the **same remote still works** — that's exactly why separating "what" from "how" is so useful.

**Why bother separating them?** Three payoffs:
1. **Focus** — you solve your problem without drowning in internal detail.
2. **Safety** — the client can only touch the interface, so it can't accidentally corrupt the internals.
3. **Swappability** — you can replace the internal data structure with a faster one later, and no client code breaks.

> [!definition] Words for "groups of things"
> - **Collection** — a group of values with no particular organization.
> - **Container** — any ADT/structure that holds a collection.
> - **Sequence** — a container whose items sit in a strict front-to-back order (like people in a line).

---

## 1.2 The Date ADT — A First Example

The book's first ADT represents **one calendar day**. It's chosen because it's familiar, yet it shows off **encapsulation** (a synonym for *information hiding*): interact only through clean buttons; never touch the internals.

### Defining the ADT — the "remote control"

Each button is a **method** (a named operation attached to the type). A special button, the **constructor**, creates a fresh **instance** — one specific value of the type (e.g. "Oct 31 2023" is one Date *instance*; "Jan 1 2024" is a different one).

| Button (operation) | What it does |
|---|---|
| `Date(month, day, year)` | **constructor** — brings a new Date instance into existence |
| `day()` / `month()` / `year()` | report the day / month / year |
| `monthName()` | the month's name, e.g. "November" |
| `dayOfWeek()` | day of week as a number (0 = Monday … 6 = Sunday) |
| `numDays(other)` | how many days lie between this date and another |
| `isLeapYear()` | true/false — is this a leap year? |
| `advanceBy(days)` | move the date forward (or back) by some days |
| `comparable(other)` | which date comes first (lets you use `<`, `>`) |
| `toString()` | a tidy text form, e.g. "10/31/2023" |

### Using the ADT — a worked example

> [!example] "Are you at least 21?" — a digital bouncer
> **Problem.** Ask people for their birth dates and report who is at least 21 years old.
> **Setup.** Create one **target** Date via the constructor — the latest birth date that still counts as 21 (in the book's example, `June 1, 1988`). Anyone born *on or before* it is old enough.
> **Solution.** Repeatedly read a birth month/day/year, build a Date instance from it, and use `comparable` to ask: *is this birth date ≤ the target?* Keep going until the user types `0` for the month to stop.
> **Answer.** For each qualifying date the program prints "Is at least 21 years of age."
> **Insight.** The program **never** does leap-year or month-length math itself — it just presses interface buttons. It has no idea *how* a Date works inside, and doesn't need to.

#### The actual code — Listing 1.1, `checkdates.py` *(added 2026-07-15; behavior verified by simulated runs)*

```python
# Extracts a collection of birth dates from the user and determines
# if each individual is at least 21 years of age.
from date import Date

def main():
    # Date before which a person must have been born to be 21 or older.
    bornBefore = Date(6, 1, 1988)

    # Extract birth dates from the user and determine if 21 or older.
    date = promptAndExtractDate()
    while date is not None :
        if date <= bornBefore :
            print( "Is at least 21 years of age: ", date )
        date = promptAndExtractDate()

# Prompts for and extracts the Gregorian date components. Returns a
# Date object or None when the user has finished entering dates.
def promptAndExtractDate():
    print( "Enter a birth date." )
    month = int( input("month (0 to quit): ") )
    if month == 0 :
        return None
    else :
        day = int( input("day: ") )
        year = int( input("year: ") )
        return Date( month, day, year )

# Call the main routine.
main()
```

> [!tip] The trick: an age check that never computes an age
> Notice what the program does **not** do: it never subtracts dates, never counts years, never touches "today." Computing someone's age directly is messy (leap years, month lengths, has-the-birthday-happened-yet). The book **inverts the question**:
> - The book's "today" is June 1, 2009. Anyone 21 or older must have been born **on or before June 1, 1988** — today minus 21 years, computed *once, by a human*, and baked in as `bornBefore = Date(6, 1, 1988)`.
> - Now "is this person at least 21?" collapses to **one comparison**: `date <= bornBefore`.
>
> Remember that for birth dates, **earlier = older** — so *less-or-equal* means *old enough*. The boundary is inclusive: someone born exactly on 06/01/1988 turns 21 exactly on the target day and qualifies (verified: the simulated run prints `Is at least 21 years of age:  06/01/1988`).

> [!note] Where the Date ADT is doing the work — button by button
> Every line of this program that touches a date goes through the **interface**, never the internals:
> - **Constructor** — `Date(6, 1, 1988)` builds the target; `Date(month, day, year)` builds one instance per person. Validation is the constructor's job (its `assert` precondition rejects nonsense like month 13) — the loop code doesn't validate anything.
> - **Comparable** — `date <= bornBefore` is the ADT's `comparable()` operation, which Python lets us spell as an operator via `__le__`. Under the hood (Listing 1.2 below) this is **one integer comparison** of Julian day numbers — all the calendar complexity was paid once, at construction.
> - **toString** — `print(..., date)` triggers `__str__`, printing `05/15/1985` — the program never formats a date by hand.
> - The loop itself is a classic **sentinel pattern**: `promptAndExtractDate()` returns a `Date` *or* `None` (when the user types `0` for the month), and `while date is not None` runs until the sentinel appears.
>
> The ADT payoff, stated with this example: `checkdates.py` would run **unchanged** if the Date implementation switched from Julian-day storage to three stored fields — the client depends on the *contract*, not the wiring. And in the four-categories language of §1.1: this client uses only the **constructor** and (comparison) **accessors** — it never mutates a date and never iterates, because its job needs neither.

### Implementing the ADT — the clever internal trick

> [!tip] How is a date actually stored?
> The obvious idea — keep month, day, year as three separate numbers — makes "days between two dates" painful (months differ in length; leap years shift everything). So the book stores each date as **one single running integer**, a **Julian day number**: the total count of days since a fixed far-past starting point.
>
> - **Days between two dates?** Just **subtract** the two integers — plain arithmetic.
> - **Which date is earlier?** Compare the two integers.
> - **Press `month()` or `year()`?** A hidden formula converts that big integer *back* into a normal calendar month/year right before answering — and the client never knows the translation happened.
>
> (Inside the implementation, the word **`self`** simply means "the specific instance I'm working on right now.")

### The actual code — Listing 1.2, `date.py` *(added 2026-07-14; previously summarized only)*

The book's partial implementation, faithful to the text (every line below was executed and verified — see the checks after the code):

```python
# Implements a proleptic Gregorian calendar date as a Julian day number.

class Date :
    # Creates an object instance for the specified Gregorian date.
    def __init__( self, month, day, year ):
        self._julianDay = 0
        assert self._isValidGregorian( month, day, year ), \
               "Invalid Gregorian date."

        # The formula's first line, T = (M - 14) / 12, had to be changed
        # because Python's integer division differs from the mathematical
        # definition — see the warning below.
        tmp = 0
        if month < 3 :
            tmp = -1
        self._julianDay = day - 32075 + \
                          (1461 * (year + 4800 + tmp) // 4) + \
                          (367 * (month - 2 - tmp * 12) // 12) - \
                          (3 * ((year + 4900 + tmp) // 100) // 4)

    # Extracts the appropriate Gregorian date component.
    def month( self ):
        return (self._toGregorian())[0]     # M from (M, d, y)

    def day( self ):
        return (self._toGregorian())[1]     # D from (m, D, y)

    def year( self ):
        return (self._toGregorian())[2]     # Y from (m, d, Y)

    # Returns day of the week as an int between 0 (Mon) and 6 (Sun).
    def dayOfWeek( self ):
        month, day, year = self._toGregorian()
        if month < 3 :
            month = month + 12
            year = year - 1
        return ((13 * month + 3) // 5 + day + \
                year + year // 4 - year // 100 + year // 400) % 7

    # Returns the date as a string in Gregorian format.
    def __str__( self ):
        month, day, year = self._toGregorian()
        return "%02d/%02d/%04d" % (month, day, year)

    # Logically compares the two dates.
    def __eq__( self, otherDate ):
        return self._julianDay == otherDate._julianDay

    def __lt__( self, otherDate ):
        return self._julianDay < otherDate._julianDay

    def __le__( self, otherDate ):
        return self._julianDay <= otherDate._julianDay

    # ... the remaining methods (numDays, advanceBy, monthName, isLeapYear,
    #     _isValidGregorian) are left as exercises by the book ...

    # Returns the Gregorian date as a tuple: (month, day, year).
    def _toGregorian( self ):
        A = self._julianDay + 68569
        B = 4 * A // 146097
        A = A - (146097 * B + 3) // 4
        year = 4000 * (A + 1) // 1461001
        A = A - (1461 * year // 4) + 31
        month = 80 * A // 2447
        day = A - (2447 * month // 80)
        A = month // 11
        month = month + 2 - (12 * A)
        year = 100 * (B - 49) + year + A
        return month, day, year
```

(To actually run it you need the one method the book leaves as an exercise — a minimal `_isValidGregorian` checking `1 ≤ month ≤ 12` and `day` against that month's length, with 29 for February in leap years.)

> [!example] Walking through the constructor — how a Gregorian date becomes ONE number
> **Problem.** Store `Date(10, 31, 2023)` as a single Julian day integer.
> **Setup.** The book uses a published astronomy formula (Seidelmann, *Explanatory Supplement to the Astronomical Almanac*), where day 0 = November 24, 4713 BC and **all divisions are integer divisions**:
> ```text
> T    = (M - 14) / 12
> jday = D - 32075 + (1461 * (Y + 4800 + T) / 4)
>                  + (367 * (M - 2 - T*12) / 12)
>                  - (3 * ((Y + 4900 + T) / 100) / 4)
> ```
> **Solution.** First the `assert` guards the **precondition** ("the supplied date must be valid" — see the note below); only then does the constructor apply the formula and store the result in the one attribute `self._julianDay`. Nothing else is ever stored — month, day, and year are *recomputed on demand*.
> **Answer.** Verified by execution: `Date(1, 1, 2000)._julianDay` → **2451545**, the textbook Julian day number for Jan 1, 2000. ✓
> **Insight.** `T` is a trick playing on the formula's view that **January and February are months 13 and 14 of the *previous* year** — that shift parks the leap day (Feb 29) at the *end* of the counting year, so leap-year corrections never disturb the months after February.

> [!warning] The `tmp` variable — the "why is it written that way" part
> The book could not copy the formula's first line into Python, because **Python's integer division is not the mathematical definition the formula assumes**:
> - The formula (and languages like C) **truncate toward zero**: `(10 − 14) / 12` = `−4/12` → **0**.
> - Python's `//` **floors toward negative infinity**: `(10 - 14) // 12` → **−1**.
> ```python
> print((10 - 14) // 12)    # -1  ← Python; the formula needs 0 here
> ```
> For any month ≥ 3 that off-by-one would silently corrupt the Julian day. Since `T` can only ever be **−1 (for Jan/Feb) or 0 (for Mar–Dec)**, the book replaces the formula line with an explicit branch — `tmp = -1 if month < 3 else 0` — which is exactly what lines with `tmp` in the constructor do. Same math, Python-proof.
> This is the chapter's quiet real-world lesson: **porting a formula between languages means checking what its operators actually do**, not just transcribing symbols.

> [!tip] Why `_toGregorian()` exists — and why the accessors look so lazy
> Several operations (`month()`, `day()`, `year()`, `dayOfWeek()`, `__str__`) all need the reverse conversion (Julian → Gregorian). Rather than duplicating that hairy formula in each method, the book writes it **once** as a helper that returns a `(month, day, year)` **tuple**, and every accessor just picks its slot — `self._toGregorian()[0]` and done.
> The **leading underscore** in `_toGregorian` and `_julianDay` is Python's "protected by convention" flag: nothing *stops* outside code from touching them, but the name warns "internal wiring — clients use the interface buttons instead." That's encapsulation enforced by discipline, not by the language.

> [!note] The remaining design choices, each in one breath
> - **`assert` = the precondition check.** §1.2.3 defines a **precondition** (what must be true *before* an operation runs) and a **postcondition** (what's guaranteed *after*). The book tests preconditions with `assert` throughout — fail fast, let the caller decide. See [The Assert Statement](<../Python/Debugging/The Assert Statement.md>).
> - **`__str__` overload** — `print(firstDay)` "just works" because Python calls `__str__` automatically. The `"%02d/%02d/%04d"` template is old-style `%` formatting (zero-padded 2- and 4-digit numbers) — see [String Formatting and Methods](<../Python/Strings and Text/String Formatting and Methods.md>).
> - **Only `==`, `<`, `<=` are implemented — on purpose.** Python 3 auto-derives the rest: `a > b` is answered by swapping into `b < a` (a *reflected* operator), and `!=` by inverting `==`. Three methods buy all six comparisons. Verified: `a > b` and `a != b` work on the class above with no `__gt__`/`__ne__` defined. ✓
> - **Comparisons and "days between" are trivial** precisely *because* of the Julian-day storage choice: both reduce to integer `==`/`<`/`−` on `_julianDay`. Verified: `Date(6,1,1988)` vs `Date(5,15,1985)` → 1,113 days apart, matching the real calendar. ✓
> - **`dayOfWeek()`** reuses the same Jan/Feb-belong-to-last-year shift, then a Zeller-style congruence mod 7 (0 = Monday). Verified: it returns **4 (Friday)** for October 15, 1582 — history records the Gregorian calendar's first official day as a Friday. ✓

---

## 1.3 Bags — An Unordered Collection

> [!definition] What is a Bag?
> A **Bag** is an ADT modeling a real bag of stuff (marbles, groceries): an **unordered** collection where **duplicates are allowed**. Throw in three identical red marbles and it holds all three. (Contrast a **set**, which keeps only *unique* items.)

> [!definition] A few code words, in plain English
> - **Class** — the *blueprint* a programmer writes to define a new type (the blueprint for "Bag").
> - **Instance** — one actual object built from that blueprint (the one specific bag you made).
> - **Method** — a button (operation) attached to the class.

**The Bag's buttons:** `Bag()` (make an empty bag) · `length()` (count the items) · `contains` (is item X inside? true/false) · `add` (toss an item in) · `remove` (take one copy out; complains with an error if it isn't there) · `iterator` (hand out every item, one by one — see §1.4).

> [!tip] Why a Bag at all, when Python has lists and dicts? — the book's own answer *(added 2026-07-15)*
> The book raises exactly this question ("why do we need the Bag ADT when we could simply use the list?") and concedes that **for a small program, a plain list is fine**. The four advantages appear when programs and teams grow. Working through the bag *abstraction* lets you:
> **(a)** focus on the problem instead of container mechanics, **(b)** avoid errors from *misusing* a list's extra powers (indexing, sorting — operations a bag shouldn't allow), **(c)** coordinate better between modules and teammates (the interface is the agreement), and **(d)** swap in a different, possibly faster implementation later without breaking anything.

### Selecting a Data Structure — the book's three-question checklist *(§1.3.2, added 2026-07-15)*

Implementing an ADT means picking a **data structure** to power it — and there are always several candidates. The book evaluates suitability with **three questions**:

> [!definition] The three suitability questions
> 1. **Can it store the domain?** The structure must be able to hold *every* value the ADT's definition allows (for a Bag: any comparable items, **including duplicates**).
> 2. **Can it implement every operation — without breaking the abstraction?** All the ADT's buttons must be buildable from the structure's own operations, with the internals staying hidden from the user.
> 3. **Is it efficient?** When several structures pass questions 1–2, efficiency picks the winner. The book *postpones* this question — judging efficiency needs **complexity analysis (Big-O)**, which is exactly what the "Necaise 4" chapter on your schedule teaches. In Chapter 1, only questions 1 and 2 are used.
>
> There's rarely one "right" answer — the best structure depends on **context**, which is why real libraries ship *several* implementations of the same ADT and let you choose.

**The audition — list vs. dictionary for the Bag.** Both candidates can pass question 1, but differently:

| Candidate | How it would store the bag | Verdict |
|---|---|---|
| **List** | each item in its own slot — duplicates simply occupy separate slots (`[19, 74, 23, 19, 12]`) | ✅ **chosen** — natural fit, no wasted space |
| **Dictionary** | duplicates clash with unique keys, so: item as the **key**, an occurrence **counter** as the value (`{19: 2, 74: 1, …}`); add a duplicate → increment, remove one → decrement | works, but for a simple bag it costs **≈2× the space** when most items are unique (a counter stored per item for nothing) |

The dictionary isn't wrong — the book notes it's an **excellent** choice for the *counting bag* variant, whose whole job is tracking occurrence counts. (That counting-bag-on-a-dict is essentially `collections.Counter` from [The Collections Module](<../Python/Modules and Libraries/The Collections Module.md>) — the standard library made the same selection for the same reason.)

**Question 2, verified operation by operation.** Before committing, the book confirms every Bag button maps onto something the list already provides:

| Bag operation | Implemented with the list's own machinery |
|---|---|
| `Bag()` — empty bag | an empty list |
| `length()` | the list's length (`len`) |
| `contains(item)` | the list's membership test (`in`) |
| `add(item)` | **append to the end** — a bag has no ordering, so the cheapest spot is fine |
| `remove(item)` | find the item's slot, pull it out (`index` + `pop`) |
| `iterator()` | a `for` loop + a custom iterator class — the subject of §1.4 |

Every operation maps cleanly, so the list passes both questions — **the list is suitable**. (A list keeps a strict order and a bag doesn't care about order; that mismatch is harmless — the Bag simply never *promises* any order through its interface.)

![Figure 1.3 — A Bag stored as a list: the internal "theItems" list holds [19, 74, 23, 19, 12] in slots 0–4 (note the repeated 19 — bags allow duplicates)](dsa_fig_1.3_bag_as_list.png)

**How the buttons work on that row of slots:**
- **add** — since order doesn't matter, just **tack a new slot onto the end** and drop the item in (fast and simple).
- **contains** — **scan** the slots one by one, checking each.
- **remove** — scan to **find** the item, pull it out, and **shift** the rest to close the gap so no empty slot is left behind.

### The actual code — Listing 1.3, `linearbag.py` *(§1.3.3, added 2026-07-15; behavior verified by execution)*

```python
# Implements the Bag ADT container using a Python list.

class Bag :
    # Constructs an empty bag.
    def __init__( self ):
        self._theItems = list()

    # Returns the number of items in the bag.
    def __len__( self ):
        return len( self._theItems )

    # Determines if an item is contained in the bag.
    def __contains__( self, item ):
        return item in self._theItems

    # Adds a new item to the bag.
    def add( self, item ):
        self._theItems.append( item )

    # Removes and returns an instance of the item from the bag.
    def remove( self, item ):
        assert item in self._theItems, "The item must be in the bag."
        ndx = self._theItems.index( item )
        return self._theItems.pop( ndx )

    # Returns an iterator for traversing the list of items.
    def __iter__( self ):
        return _BagIterator( self._theItems )   # the iterator class lives in §1.4
```

(The book's printed listing leaves `__iter__` as dots and completes it in §1.4 — shown here already wired up. The print run also has a small typo there, `def __iter__( self, item ):`; the correct signature, used above, takes only `self`.)

> [!note] Reading the implementation — three things to notice
> - **One field is the whole state.** `self._theItems = list()` — an empty bag *is* an empty list, exactly as the operation-mapping table promised. The underscore marks it protected-by-convention, same as `_julianDay` in the Date class.
> - **The dunder names are deliberate.** The ADT's `length()` and `contains()` are implemented as `__len__` and `__contains__`, so clients write natural Python — `len(myBag)` and `value in myBag` — per the ADT-operations-as-operators convention from §1.2. Sorted into the four categories of §1.1: constructor (`__init__`), accessors (`__len__`, `__contains__`), mutators (`add`, `remove`), iterator (`__iter__`).
> - **`remove` guards its precondition** with `assert item in self._theItems` before touching anything — the same fail-fast pattern as the Date constructor. And because duplicates occupy separate slots, `remove` takes out exactly **one** occurrence: verified — after `add`ing `19, 74, 23, 19, 12` and calling `remove(19)`, the bag still contains the second `19` and `len` drops 5 → 4. ✓

---

## 1.4 Iterators — Visiting Every Item

> [!definition] Traversal and the problem it solves
> A **traversal** (to **iterate**) means visiting *every* item in a container, one at a time, to do something with each (search it, print it, …). But if we let outsiders reach *directly* into a Bag to look, we'd expose its hidden internals — breaking the whole point of an ADT.

> [!tip] The fix — an iterator (a conveyor belt)
> An **iterator** is a small helper built into the ADT that walks the collection *for* you without revealing the internals. Think of a **supermarket checkout belt**: instead of climbing into the stockroom, you let the belt feed items past you **one at a time**. (Or: a cursor stepping down a list.)

An iterator offers two operations:
- **Give me the next item** — return the item it's currently pointing at, then advance its placeholder by one.
- **Know when to stop** — when there's nothing left, it raises a signal called **`StopIteration`** (a formal "I'm out of items!" alarm; an *exception* is just such a signal).

![Figure 1.4 — The iterator tracks a position: the _BagIterator holds a pointer into the Bag's list plus curItem = 0 (the slot it will hand out next)](dsa_fig_1.4_bag_iterator.png)

### The actual code — Listing 1.4, `_BagIterator` *(added 2026-07-15; verified by execution)*

This class completes the `linearbag.py` module from §1.3 — it's what the Bag's `__iter__` hands back:

```python
# An iterator for the Bag ADT implemented as a Python list.
class _BagIterator :
    def __init__( self, theList ):
        self._bagItems = theList     # an ALIAS to the bag's list (no copy)
        self._curItem = 0            # the slot it will hand out next

    def __iter__( self ):
        return self                  # an iterator's __iter__ always returns itself

    def __next__( self ):
        if self._curItem < len( self._bagItems ) :
            item = self._bagItems[ self._curItem ]
            self._curItem += 1
            return item
        else :
            raise StopIteration
```

Two details worth noticing: `_bagItems` is a **reference to the same list** the Bag holds (Figure 1.4 draws exactly this — no data is copied), and all the iterator's "memory" is one integer, `_curItem`. Each `__next__` call hands out the current slot and advances; running off the end raises the `StopIteration` alarm.

> [!tip] What a `for` loop is really doing
> When you write "for each item in the bag, do …", the loop **automatically**: sets up the iterator, keeps pressing *give-me-the-next-item*, processes whatever comes back, and — the moment the `StopIteration` alarm fires — stops cleanly. You never press the buttons yourself.
> The book shows the machinery spelled out — this is the exact equivalent of `for item in myBag: print(item)`, and it runs (verified):
> ```python
> # Create a _BagIterator object for myBag.
> iterator = myBag.__iter__()
> while True :
>     try :
>         item = iterator.__next__()   # next item, please
>         print( item )                # the body of the for loop
>     except StopIteration :           # the "I'm out of items!" alarm
>         break
> ```

Re-running the bouncer example (§1.2) is now trivial: store the birth dates in a Bag, `for` each date the belt hands out, check "born on/before the target?", and print the ones who qualify — all **without knowing how the Bag stores anything.**

---

## 1.5 Application: Student Records — Putting It Together

> [!example] The real-world task
> **Problem.** Read a collection of **student records** from an external file and print a tidy report, **sorted by ID number**. The catch: you're *not told* how the file is formatted (plain text? binary? a database?).
> **Solution — lean on abstraction.**
> - **What to store per student:** an **ID** (whole number), **first & last name** (text), a **classification code** (1–4 = freshman→senior), and a **GPA** (a decimal number, i.e. a *floating-point* value).
> - **Bundle it:** a tiny **storage class** `StudentRecord` groups those five fields under *readable names* (`firstName`, `gpa`, …). Better than an unnamed **tuple**, where you'd have to remember which slot is which.
> - **Hide the file mess:** a **Student File Reader** ADT — a *reader* is an object whose job is to pull data *in* from outside. As a black box, the main program just presses its buttons; opening files and parsing text is the reader's private business.
> **The steps.**
> 1. **Setup** — make a reader, tell it the file name (e.g. `students.txt`).
> 2. **Connect** — `open()` the file.
> 3. **Extract** — `fetchAll()`: the reader loops the file, builds a `StudentRecord` per student, and returns a ready-made **list** of them.
> 4. **Disconnect** — `close()` the file.
> 5. **Sort** — order the list by student ID.
> 6. **Report** — loop the sorted list, translate class codes (1 → "Freshman", …) into words, and print the formatted report.
> **Insight.** Every hard part (unknown file format, parsing, iterating) is sealed inside an ADT, so the top-level program reads like a short to-do list.

---

## Key Ideas & a Beginner's Glossary

- **The one big idea:** an **ADT** is the *interface* (what you can do); a **data structure** is the *implementation* (how it's built). Separating them buys focus, safety, and the freedom to swap internals.
- **Abstraction** = focusing only on what's relevant and hiding the rest. Two kinds: **procedural abstraction** (use a *function* knowing what it does, not how — e.g. `sqrt`) and **data abstraction** (use a *data type* without knowing how it's stored — e.g. a Python string). An ADT combines both.
- **Encapsulation / information hiding** — sealing internals behind an interface (the "black box").
- **Class** = blueprint · **instance/object** = one thing built from it · **method** = a button · **constructor** = the button that builds a new instance · **self** = "this particular instance."
- **The four operation categories:** **constructor** (creates the instance) · **accessor** (reads without changing — safe anywhere) · **mutator** (changes the contents) · **iterator** (hands out items one at a time). No mutators ⇒ the type is immutable.
- **Collection** = a group of values · **container** = holds a collection · **sequence** = a container in strict order.
- **Bag** = unordered collection, duplicates allowed (built here from a **list** = a growable row of numbered slots).
- **Iterator** = a helper that hands you items one at a time (a conveyor belt); a **for-loop** drives it and stops on the **StopIteration** signal.
- **Nice trick to remember:** storing a Date as **one Julian day-number** turns "days between dates" into simple subtraction — a great example of a smart data structure making operations easy.

> [!note] About the chapter's exercises
> The chapter ends with **Exercises** and **Programming Projects** — but these are hands-on *coding* assignments (finish the `Date` class, write a `printCalendar()`, build a click-counter, etc.), meant to be implemented in Python. They're a great next step *once you start coding*, but they're outside the scope of this plain-language summary, so they aren't reproduced here.

---

### Sources

| Source | Detail | Type |
|---|---|---|
| Rance D. Necaise, *Data Structures and Algorithms Using Python* | Chapter 1 — Abstract Data Types | Textbook |
| NotebookLM | Per-section summaries (prompted for a first-time reader) from the Ch. 1 PDF | LLM tool |
| Main-agent verification | Checked the ADT/data-structure claims, the Date/Bag/iterator behavior, and the Julian-day trick against the text | — |
| Book text, §1.2.4 (added 2026-07-14) | Listing 1.2 `date.py` code + explanations extracted directly from the PDF; all code executed and verified (JDN 2451545 for 2000-01-01; Friday for 1582-10-15; 1,113-day span check) | Direct extraction |
