# Classes and Object-Oriented Programming

_Research compiled 2026-07-08 — based on Python Crash Course (3e), Chapter 9 "Classes", with added OOP essentials_

> Part of the [Python Reference](<../Python Reference (Main).md>). A **class** is a blueprint for making **objects**. You describe the general shape of a thing once (what data it holds, what it can do), then stamp out as many individual **instances** as you like — each with its own data. This is **object-oriented programming (OOP)**: modelling real-world things as objects. Sections marked **added** go beyond the book's Chapter 9.

---

## Branch 1 — The Big Idea: Blueprint vs. Instance

- A **class** is the blueprint — e.g. "a Character has a name and health, and can take damage."
- An **instance** (or object) is one specific thing built from that blueprint — e.g. "Aria, with 100 HP."
- Making an object from a class is called **instantiation**.

One class → many instances, each independent. Change one instance's data and the others are untouched.

---

## Branch 2 — Defining a Class

```python
class Character:
    """A playable game character."""       # docstring: what the class is

    def __init__(self, name, health=100):  # the initializer
        self.name = name                   # attribute
        self.health = health
        self.level = 1                      # a default attribute (not a parameter)

    def describe(self):                     # a method
        return f"{self.name} (Lv {self.level}, {self.health} HP)"
```

Three things to learn here:

- **`class Character:`** — the `class` keyword plus a name in **CamelCase** (capital first letter, no underscores). The docstring on the next line describes it.
- **`__init__(self, ...)`** — a special method Python runs **automatically** every time you create an instance. It sets up the starting data. (Two underscores on each side — `_init_` with one underscore each side won't run automatically.)
- **`self`** — the first parameter of every method. It refers to *"this particular instance."* You never pass it yourself; Python fills it in. Anything stored as `self.something` becomes an **attribute** available to the whole instance.

> [!note] Attributes vs. methods
> An **attribute** is a piece of *data* an instance holds (`self.name`). A **method** is a *function defined inside a class* — a thing the instance can *do* (`describe()`). Everything you know about functions applies to methods; the only difference is that first `self` parameter.

---

## Branch 3 — Making and Using Instances

Create an instance by calling the class like a function; access its parts with **dot notation**.

```python
hero = Character("Aria")        # __init__ runs with name="Aria"

print(hero.name)                # Aria          — read an attribute
print(hero.describe())          # Aria (Lv 1, 100 HP)  — call a method

villain = Character("Mordak", health=150)   # a second, independent instance
print(villain.health)           # 150
```

- `hero.name` reads the attribute; `hero.describe()` calls the method.
- `hero` and `villain` are separate — each has its own `name`, `health`, `level`.

---

## Branch 4 — Changing an Instance's Data

There are **three** ways to change an attribute's value.

```python
class Character:
    def __init__(self, name):
        self.name = name
        self.health = 100
    def take_damage(self, amount):
        self.health = max(0, self.health - amount)   # method with a rule
    def gain_level(self):
        self.health += 20                            # increment inside a method

c = Character("Bo")

c.health = 80          # 1. DIRECTLY through the instance
c.take_damage(30)      # 2. THROUGH A METHOD (which can enforce rules)
print(c.health)        # 50
c.take_damage(999)     # the max(0, ...) rule stops it going below 0
print(c.health)        # 0
c.gain_level()         # 3. INCREMENT through a method
print(c.health)        # 20
```

- **Directly** — simplest, but no validation: `c.health = 80`.
- **Through a method** — lets you enforce rules (here, health can't drop below 0). This is usually the better habit.
- **Incrementing** — a method that *adds to* the current value instead of replacing it.

> [!warning] Methods guard your data, but don't *secure* it
> A method like `take_damage` can enforce rules, but anyone can still bypass it by setting `c.health = -999` directly. Methods are for *convenience and correctness*, not security.

---

## Branch 5 — Inheritance (building on an existing class)

If a new class is a **specialized version** of an existing one, it can **inherit** from it — taking on all the parent's attributes and methods, then adding or changing its own. The original is the **parent** (superclass); the new one is the **child** (subclass).

```python
class Mage(Character):                     # Mage inherits from Character
    """A character that can cast spells."""

    def __init__(self, name, health=100, mana=50):
        super().__init__(name, health)     # run the PARENT's __init__ first
        self.mana = mana                   # then add a child-specific attribute

    def cast_spell(self):                  # a brand-new method
        self.mana -= 10
        return f"{self.name} casts a spell! (mana {self.mana})"

    def describe(self):                    # OVERRIDE the parent's method
        return f"{self.name} the Mage ({self.health} HP, {self.mana} MP)"

m = Mage("Merlin")
print(m.describe())        # Merlin the Mage (100 HP, 50 MP)  — child's version
print(m.cast_spell())      # Merlin casts a spell! (mana 40)
print(m.take_damage)       # inherited from Character — still available
```

The key pieces:

- **`class Mage(Character):`** — put the parent's name in parentheses.
- **`super().__init__(...)`** — calls the parent's `__init__` so all the parent's setup still happens. Do this **first**, then add child-specific attributes. (`super` = "superclass".)
- **Adding** — the child freely defines new attributes (`self.mana`) and methods (`cast_spell`).
- **Overriding** — define a method with the **same name** as one in the parent, and the child's version wins. Use this when the parent's behaviour doesn't fit the child.

---

## Branch 6 — Composition (instances as attributes)

When a class grows too big, move part of it into a **separate class** and store an instance of that class as an attribute. This is **composition** — building a complex object out of simpler ones ("has-a" instead of inheritance's "is-a").

```python
class Inventory:
    def __init__(self):
        self.items = []
    def add(self, item):
        self.items.append(item)

class Hero:
    def __init__(self, name):
        self.name = name
        self.inventory = Inventory()       # a Hero HAS an Inventory

h = Hero("Zed")
h.inventory.add("sword")                   # reach through the attribute
h.inventory.add("shield")
print(h.inventory.items)                   # ['sword', 'shield']
```

- A `Hero` **has an** `Inventory` (composition); a `Mage` **is a** `Character` (inheritance). Choosing between them is a big part of "thinking like a programmer."
- You reach the inner object's methods by chaining dots: `h.inventory.add(...)`.

---

## Branch 7 — Class Attributes vs. Instance Attributes *(added)*

Everything in `__init__` with `self.` is an **instance attribute** — unique per object. An attribute defined **directly in the class body** is a **class attribute** — **shared by every instance**.

```python
class Player:
    game_title = "PyQuest"           # CLASS attribute — one copy, shared by all
    def __init__(self, name):
        self.name = name             # INSTANCE attribute — one per player

p1 = Player("A")
p2 = Player("B")
print(p1.game_title, p2.game_title)  # PyQuest PyQuest  (both share it)

Player.game_title = "PyQuest II"     # change it once...
print(p1.game_title, p2.game_title)  # PyQuest II PyQuest II  (...all see it)
```

Use a **class attribute** for something every instance shares (a constant, a shared counter, a default). Use an **instance attribute** for data unique to each object.

---

## Branch 8 — `__str__` and `__repr__` *(added)*

By default, printing an object shows something ugly like `<__main__.Point object at 0x...>`. Define **`__str__`** to control what `print()` shows, and **`__repr__`** for the developer-facing/debugging form.

```python
class Point:
    def __init__(self, x, y):
        self.x, self.y = x, y
    def __str__(self):
        return f"({self.x}, {self.y})"       # friendly — used by print()
    def __repr__(self):
        return f"Point({self.x}, {self.y})"  # unambiguous — used in the REPL / lists

pt = Point(3, 4)
print(pt)          # (3, 4)          — __str__
print(repr(pt))    # Point(3, 4)     — __repr__
print([pt])        # [Point(3, 4)]   — containers use __repr__ for their items
```

Both are **dunder** ("double-underscore") methods, like `__init__` — special names Python calls automatically in certain situations.

---

## Branch 9 — Storing Classes in Modules (importing)

As files grow, move classes into their own `.py` **module** and import what you need — same idea as importing functions. If `characters.py` contains `Character` and `Mage`:

```python
# one class
from characters import Character

# several classes
from characters import Character, Mage

# the whole module — then use module.ClassName
import characters
hero = characters.Character("Aria")

# with an alias
from characters import Character as Char
import characters as ch
```

- **`from module import Name`** is the common form.
- **`import module`** then `module.ClassName` keeps it obvious where each class comes from and avoids name clashes.
- **`from module import *`** (import everything) is **discouraged** — it hides which names you're using and invites naming conflicts.
- A class in one module can import a class from another (e.g. a `Mage` module doing `from characters import Character` to inherit from it).

---

## Branch 10 — Checking Types *(added)*

```python
m = Mage("Merlin")
print(isinstance(m, Mage))        # True
print(isinstance(m, Character))   # True  — a Mage IS a Character (inheritance)
print(type(m).__name__)           # 'Mage'  — the exact class
```

- **`isinstance(obj, Class)`** — `True` if `obj` is that class **or a subclass** of it (respects inheritance). Prefer this for type checks.
- **`type(obj)`** — the object's exact class, no inheritance leniency.

---

## Branch 11 — Styling Classes (PEP 8)

- **Class names** in **CamelCase** (`ElectricCar`); **instances and modules** in `lower_snake_case` (`my_car`).
- Give **every class a docstring** right after the `class` line; give **every module** a docstring too.
- **One blank line** between methods inside a class; **two blank lines** between classes in a module.
- With mixed imports, put **standard-library** imports first, then a blank line, then **your own** modules.

---

## Key Takeaways

- A **class** is a blueprint; an **instance** is one object built from it. `__init__(self, …)` sets up each instance's starting **attributes**; **methods** are its behaviours.
- **`self`** means "this instance" and is passed automatically; store data as `self.x`.
- Change attributes **directly**, **through a method** (which can enforce rules), or by **incrementing** in a method.
- **Inheritance** (`class Child(Parent)`, `super().__init__(...)`) reuses a parent class; add new methods, or **override** to replace one. **Composition** stores an instance as an attribute ("has-a").
- **Class attributes** are shared by all instances; **instance attributes** are per-object.
- Add **`__str__`** / **`__repr__`** for readable printing; check types with **`isinstance()`**.
- Store classes in **modules** and import them; follow **CamelCase / docstring / blank-line** style.

---

## Exercises

Try each first, then reveal the solution. All solutions verified against Python 3.14.

> [!example] Exercise 1 — A Rectangle class
> **Problem.** Write a class `Rectangle` whose `__init__` takes `width` and `height`. Add a method `area()` and a method `perimeter()`. Make a `Rectangle(3, 4)` and print both.
>
> > [!success]- Click to reveal solution
> > **Solution.** Store the two values as attributes; each method computes from `self`.
> > ```python
> > class Rectangle:
> >     def __init__(self, width, height):
> >         self.width = width
> >         self.height = height
> >     def area(self):
> >         return self.width * self.height
> >     def perimeter(self):
> >         return 2 * (self.width + self.height)
> > r = Rectangle(3, 4)
> > print(r.area(), r.perimeter())
> > ```
> > **Answer.** `12 14` ✓

> [!example] Exercise 2 — A Counter with default + methods
> **Problem.** Write a class `Counter` that starts with `count = 0` (no parameter). Add `increment()` (adds 1) and `reset()` (back to 0). Increment twice, print, reset, print.
>
> > [!success]- Click to reveal solution
> > **Solution.** Give `count` a default in `__init__`; the methods modify `self.count`.
> > ```python
> > class Counter:
> >     def __init__(self):
> >         self.count = 0
> >     def increment(self):
> >         self.count += 1
> >     def reset(self):
> >         self.count = 0
> > c = Counter()
> > c.increment(); c.increment()
> > print(c.count)      # 2
> > c.reset()
> > print(c.count)      # 0
> > ```
> > **Answer.** `2` then `0` ✓

> [!example] Exercise 3 — Inheritance: Square from Rectangle
> **Problem.** Using your `Rectangle` from Exercise 1, write `Square` that inherits from it. A square only needs **one** side length — its `__init__` takes `side` and passes it as both width and height to the parent. Print the area of a `Square(5)`.
>
> > [!success]- Click to reveal solution
> > **Solution.** Call `super().__init__(side, side)` so both dimensions equal the side.
> > ```python
> > class Square(Rectangle):
> >     def __init__(self, side):
> >         super().__init__(side, side)
> > print(Square(5).area())
> > ```
> > **Answer.** `25` ✓ (`area()` is inherited from `Rectangle` — no need to rewrite it)

> [!example] Exercise 4 — Add a readable `__str__`
> **Problem.** Add a `__str__` method to `Rectangle` so that `print(Rectangle(2, 6))` shows `Rectangle 2x6`.
>
> > [!success]- Click to reveal solution
> > **Solution.** `__str__` must **return** the string (not print it); `print()` calls it automatically.
> > ```python
> > class Rectangle:
> >     def __init__(self, width, height):
> >         self.width = width
> >         self.height = height
> >     def __str__(self):
> >         return f'Rectangle {self.width}x{self.height}'
> > print(Rectangle(2, 6))
> > ```
> > **Answer.** `Rectangle 2x6` ✓

---

### Sources

| Source | Date | Type |
|---|---|---|
| Python Crash Course, 3e (Eric Matthes) — Chapter 9 "Classes" | 2026 | Book chapter |
| Python data model (`__init__`, `__str__`, `__repr__`) — official docs | 2026 | Language reference |
| Verified against Python 3.14 on `E:\Python` | 2026-07-08 | Local test |
