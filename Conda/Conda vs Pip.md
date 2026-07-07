# Conda vs Pip

_Research compiled 2026-07-07 — comparing the two Python package installers_

> Companion to [Conda Environment Basics](<Conda Environment Basics.md>). Both `conda install` and `pip install` add packages to your environment, but they pull from different places and solve dependencies differently. Knowing when to use which avoids broken setups.

---

## Branch 1 — The Core Difference

| | `conda install` | `pip install` |
|---|---|---|
| **Installs from** | conda **channels** (conda-forge, defaults) | **PyPI** (Python Package Index) |
| **Can install** | Python packages **+ non-Python** (C/C++ libraries, compilers, CUDA, R, Python itself) | **Python packages only** |
| **Dependency handling** | a real **solver** — finds one mutually compatible set for the whole environment | installs a package + its requirements one at a time; may overwrite existing versions |
| **Package format** | pre-built **binaries** for your OS | **wheels** (pre-built) or source you compile locally |
| **Environments** | also **creates/manages** them | just installs — needs `venv`/`virtualenv` separately |

---

## Branch 2 — Why Conda Installs More Than Python

Many scientific packages (NumPy, SciPy, pandas) are Python wrappers around **compiled libraries** written in C or Fortran (e.g. the BLAS/LAPACK math libraries).

- **conda** installs the Python part **and** the compiled library underneath, guaranteeing the versions match. This is why data-science stacks "just work" through conda.
- **pip** installs only the Python part and assumes the compiled pieces are already on your system. Historically this made scientific packages painful to `pip install` on Windows (though modern wheels have improved it a lot).

> [!tip] This is conda's main advantage
> Conda manages the *whole stack* — Python, native libraries, and even non-Python tools — as one coherent set. Pip only knows about Python packages on PyPI.

---

## Branch 3 — Why Conda's Solver Is Stricter

- **conda** looks at **every** package in the environment at once and refuses a combination that would conflict. Safer, but the solve can be slower.
- **pip** installs what you asked for and its stated requirements, right now. Faster, but it can **silently replace** a version that another package depended on, quietly breaking it.

---

## Branch 4 — Using Both Together (the golden rule)

You can — and often must — use pip inside a conda environment, because many packages live **only** on PyPI. The safe order:

1. **`conda install` first** for everything available on conda — especially the big packages (NumPy, pandas, SciPy, Jupyter).
2. **`pip install` last**, only for what conda doesn't have.

```bash
(pydata-book) $ conda install numpy pandas jupyter   # heavy lifting via conda
(pydata-book) $ pip install some-pypi-only-package   # then top up with pip
```

> [!warning] Don't ping-pong between them
> Conda doesn't track what pip changed. If you `pip install` something and **then** run `conda install`, conda may overwrite or conflict with pip's work. Do all your conda installs first, add pip packages on top, and avoid going back and forth. Always do this **inside an activated environment**, never in `base`.

---

## Branch 5 — Which Should I Reach For?

| Situation | Use |
|---|---|
| Scientific / data stack (NumPy, pandas, SciPy, Jupyter) | **conda** |
| A package that needs compiled/native libraries | **conda** |
| Creating or managing environments | **conda** |
| A package that's on PyPI but not on conda | **pip** (inside the env) |
| Pure-Python package, quick install | either — **pip** is fine |

---

## Key Takeaways

- **`conda`** installs from channels, can install **non-Python** software, solves the whole environment together, and manages environments. **`pip`** installs Python-only packages from **PyPI**, one request at a time.
- Conda's edge is the **full stack** (Python + compiled libraries matched) — why data-science tools install cleanly through it.
- Conda's solver is **stricter** (safer but slower); pip is **faster** but can silently overwrite versions.
- Use **both** when needed: **conda first**, **pip last**, always inside an **activated environment** — and don't ping-pong between them.

---

### Sources

| Source | Date | Type |
|---|---|---|
| Conda — official documentation ("Using pip in a conda environment") | 2026 | Tool reference |
| pip / PyPI — official documentation | 2026 | Tool reference |
