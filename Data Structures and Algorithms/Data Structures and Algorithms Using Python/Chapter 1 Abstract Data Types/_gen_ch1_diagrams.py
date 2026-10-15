"""Draws the four extra diagrams for Chapter 1 (Main).md.

Run from this folder:  python _gen_ch1_diagrams.py   (needs matplotlib)
"""
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Rectangle

INK = "#222222"
MUTED = "#666666"
BLUE = "#dbe8f6"
BLUE_EDGE = "#3d6fa8"
GREEN = "#dff0dc"
GREEN_EDGE = "#3f8a3a"
ORANGE = "#fde7cf"
ORANGE_EDGE = "#c06a12"
GREY = "#eeeeee"
FONT = 12


def box(ax, x, y, w, h, text, face=GREY, edge=INK, size=FONT, weight="normal", round_=True, ls="-"):
    style = "round,pad=0.02,rounding_size=0.08" if round_ else "square,pad=0"
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle=style, fc=face, ec=edge, lw=1.4, ls=ls))
    ax.text(x + w / 2, y + h / 2, text, ha="center", va="center", fontsize=size, color=INK, weight=weight)


def arrow(ax, x1, y1, x2, y2, color=INK):
    ax.annotate("", xy=(x2, y2), xytext=(x1, y1),
                arrowprops=dict(arrowstyle="-|>", color=color, lw=1.4, shrinkA=0, shrinkB=0))


def cells(ax, x, y, values, w=0.7, h=0.6, highlight=None, face="white"):
    for i, v in enumerate(values):
        fc = ORANGE if i == highlight else face
        ec = ORANGE_EDGE if i == highlight else INK
        ax.add_patch(Rectangle((x + i * w, y), w, h, fc=fc, ec=ec, lw=1.3))
        ax.text(x + i * w + w / 2, y + h / 2, str(v), ha="center", va="center", fontsize=FONT)


def finish(fig, ax, name):
    ax.set_aspect("equal")
    ax.axis("off")
    fig.savefig(name, dpi=170, bbox_inches="tight", facecolor="white")
    plt.close(fig)


# 1. Julian day number line (§1.2.4)
fig, ax = plt.subplots(figsize=(11, 3.6))
ax.set_xlim(0, 11)
ax.set_ylim(0, 3.6)
ax.plot([0.4, 2.0], [1.6, 1.6], color=INK, lw=2)
ax.plot([2.6, 10.6], [1.6, 1.6], color=INK, lw=2)
for dx in (2.05, 2.35):
    ax.plot([dx, dx + 0.2], [1.35, 1.85], color=INK, lw=1.5)
arrow(ax, 10.5, 1.6, 10.8, 1.6)
ax.text(10.75, 1.25, "days", fontsize=10, color=MUTED, ha="center")
marks = [
    (0.6, "0", "Nov 24, 4714 BC\n(day 0)"),
    (4.0, "2,446,201", "05/15/1985"),
    (6.6, "2,447,314", "06/01/1988"),
    (9.6, "2,451,545", "01/01/2000"),
]
for x, num, label in marks:
    ax.plot([x, x], [1.45, 1.75], color=INK, lw=2)
    ax.text(x, 1.95, num, ha="center", va="bottom", fontsize=FONT, weight="bold", color=BLUE_EDGE)
    ax.text(x, 1.25, label, ha="center", va="top", fontsize=10.5, color=INK)
ax.annotate("", xy=(6.6, 2.75), xytext=(4.0, 2.75),
            arrowprops=dict(arrowstyle="<->", color=GREEN_EDGE, lw=1.6))
ax.text(5.3, 2.85, "numDays = 2,447,314 − 2,446,201 = 1,113", ha="center", va="bottom",
        fontsize=FONT, color=GREEN_EDGE, weight="bold")
ax.text(5.5, 0.15, "Each Date stores ONE integer. Comparing two dates = comparing two integers; "
        "days between them = one subtraction.", ha="center", fontsize=10.5, color=MUTED)
finish(fig, ax, "Ch1 Julian Day Number Line.png")

# 2. Bag stored in a list vs in a dictionary (§1.3.2)
fig, ax = plt.subplots(figsize=(11, 3.9))
ax.set_xlim(0, 11)
ax.set_ylim(0, 3.9)
ax.text(2.1, 3.55, "List: every copy gets its own slot", ha="center", fontsize=FONT, weight="bold")
cells(ax, 0.35, 2.3, [19, 74, 23, 19, 12])
for i in range(5):
    ax.text(0.35 + i * 0.7 + 0.35, 2.05, str(i), ha="center", fontsize=10, color=MUTED)
ax.text(2.1, 1.45, "5 values stored", ha="center", fontsize=FONT, color=BLUE_EDGE)
ax.text(8.0, 3.55, "Dictionary: item → how many copies", ha="center", fontsize=FONT, weight="bold")
for r, (k, c) in enumerate([(19, 2), (74, 1), (23, 1), (12, 1)]):
    y = 2.75 - r * 0.55
    ax.add_patch(Rectangle((6.9, y), 0.9, 0.5, fc=BLUE, ec=INK, lw=1.2))
    ax.add_patch(Rectangle((8.2, y), 0.9, 0.5, fc=GREEN, ec=INK, lw=1.2))
    ax.text(7.35, y + 0.25, str(k), ha="center", va="center", fontsize=FONT)
    ax.text(8.65, y + 0.25, str(c), ha="center", va="center", fontsize=FONT)
    arrow(ax, 7.8, y + 0.25, 8.2, y + 0.25)
ax.text(7.35, 3.3, "key", ha="center", fontsize=10, color=MUTED)
ax.text(8.65, 3.3, "count", ha="center", fontsize=10, color=MUTED)
ax.text(8.0, 0.75, "4 keys + 4 counters stored", ha="center", fontsize=FONT, color=BLUE_EDGE)
ax.text(5.5, 0.1, "Mostly unique items → the dictionary stores about twice as much. "
        "Simple bag: list. Counting bag: dictionary.", ha="center", fontsize=10.5, color=MUTED)
finish(fig, ax, "Ch1 Bag List vs Dictionary.png")

# 3. The iterator walking the bag's list (§1.4.2)
items = [19, 74, 23, 19, 12]
fig, ax = plt.subplots(figsize=(10.5, 5.6))
ax.set_xlim(0, 10.5)
ax.set_ylim(-0.4, 6.0)
ax.text(5.25, 5.7, "for item in bag:  Python calls bag.__iter__() once, then __next__() again and again",
        ha="center", fontsize=FONT, weight="bold")
ax.text(0.2, 5.05, "call", fontsize=10, color=MUTED)
ax.text(1.35, 5.05, "_curItem before the call", fontsize=10, color=MUTED)
ax.text(6.0, 5.05, "what __next__() does", fontsize=10, color=MUTED)
for k in range(6):
    y = 4.3 - k * 0.8
    ax.text(0.35, y + 0.3, f"#{k + 1}", fontsize=FONT, ha="center", va="center")
    cells(ax, 1.3, y, items, w=0.7, h=0.6, highlight=k if k < 5 else None)
    ax.text(5.0, y + 0.3, str(k), fontsize=FONT, ha="center", va="center", color=ORANGE_EDGE, weight="bold")
    if k < 5:
        msg = f"returns {items[k]},  _curItem → {k + 1}"
        col = INK
    else:
        msg = "5 == len(list) → raise StopIteration → loop ends"
        col = "#b02a2a"
    ax.text(6.0, y + 0.3, msg, fontsize=FONT, va="center", color=col)
ax.text(5.25, -0.3, "The iterator never copies the list: _bagItems is an alias to the bag's own list "
        "(Figure 1.4). Its only memory is one integer.", ha="center", fontsize=10.5, color=MUTED)
finish(fig, ax, "Ch1 Iterator Walk.png")

# 4. Student report pipeline (§1.5)
fig, ax = plt.subplots(figsize=(12, 4.6))
ax.set_xlim(0, 12)
ax.set_ylim(0, 4.6)
box(ax, 0.2, 2.55, 2.0, 1.2, "students.txt\n5 lines per record", face=GREY)
ax.add_patch(FancyBboxPatch((2.75, 2.15), 4.9, 2.1, boxstyle="round,pad=0.02,rounding_size=0.1",
                            fc="white", ec=BLUE_EDGE, lw=1.6, ls="--"))
ax.text(5.2, 3.92, "StudentFileReader", ha="center", fontsize=11, color=BLUE_EDGE, weight="bold")
ax.text(5.2, 3.6, "the only code that knows the file format", ha="center", fontsize=10, color=BLUE_EDGE)
box(ax, 2.95, 2.35, 1.2, 0.9, "open()", face=BLUE, edge=BLUE_EDGE)
box(ax, 4.45, 2.35, 1.55, 0.9, "fetchAll()\nloops\nfetchRecord()", face=BLUE, edge=BLUE_EDGE, size=10.5)
box(ax, 6.3, 2.35, 1.2, 0.9, "close()", face=BLUE, edge=BLUE_EDGE)
arrow(ax, 2.2, 3.0, 2.95, 2.8)
arrow(ax, 4.15, 2.8, 4.45, 2.8)
arrow(ax, 6.0, 2.8, 6.3, 2.8)
box(ax, 8.2, 2.55, 3.5, 1.2, "list of StudentRecord objects\n(idNum, firstName, lastName,\nclassCode, gpa)",
    face=GREEN, edge=GREEN_EDGE, size=10.5)
arrow(ax, 7.65, 3.15, 8.2, 3.15)
box(ax, 8.2, 0.55, 3.5, 1.1, "sort(key=lambda rec: rec.idNum)", face=ORANGE, edge=ORANGE_EDGE, size=10.5)
arrow(ax, 9.95, 2.55, 9.95, 1.65)
box(ax, 4.45, 0.55, 3.0, 1.1, "printReport()\nheader · rows · footer", face=ORANGE, edge=ORANGE_EDGE, size=10.5)
arrow(ax, 8.2, 1.1, 7.45, 1.1)
box(ax, 0.2, 0.55, 3.4, 1.1, "LIST OF STUDENTS\n10015  Smith, John  …", face=GREY, size=10.5)
arrow(ax, 4.45, 1.1, 3.6, 1.1)
ax.text(6.0, 0.05, "New file format?  Swap the reader module (and maybe the file name). "
        "Everything outside the dashed box stays the same.", ha="center", fontsize=10.5, color=MUTED)
finish(fig, ax, "Ch1 Student Report Pipeline.png")

print("wrote 4 diagrams")
