# Conda Environment Basics

_Research compiled 2026-07-07 — Conda package & environment manager (setup commands from Python for Data Analysis, 3e)_

> **Conda** is a tool that does two jobs: it **installs packages** (like `pip`, but also non-Python things like compilers and libraries) and it manages **environments** — isolated, self-contained Python setups so each project can have its own versions without clashing. This note walks through the four setup commands line by line.

---

## Branch 1 — The `(base)` Prompt

Before any command, notice the prompt:

```bash
(base) $
```

The `(base)` in parentheses is **conda telling you which environment is currently active**. `base` is the default environment that comes with a conda install. Once you activate your own environment, this label changes — that's your visual confirmation of where packages will install.

---

## Branch 2 — Configuring Channels

```bash
(base) $ conda config --add channels conda-forge
(base) $ conda config --set channel_priority strict
```

A **channel** is a *source* conda downloads packages from — like an app store. `conda config` edits conda's settings file (`.condarc`).

| Command                                      | What it does                                                                            |
| -------------------------------------------- | --------------------------------------------------------------------------------------- |
| `conda config --add channels conda-forge`    | Adds **conda-forge** to your list of package sources, at the **top** (highest priority) |
| `conda config --set channel_priority strict` | Turns on **strict** channel priority                                                    |

- **`conda-forge`** is a large, community-maintained channel with more packages and fresher versions than conda's default channel. Adding it means "look here first."
- **`channel_priority strict`** tells conda: *always* prefer the higher-priority channel (conda-forge), even if a lower channel has a newer version. This keeps all your packages coming from **one consistent source**, which avoids the mix-and-match conflicts that cause broken environments. It also makes installs resolve faster.

> [!tip] Why this matters
> Mixing packages from different channels is a top cause of "it won't install" / "it imports but crashes" problems. Setting conda-forge first + strict priority is the standard recommended baseline for a clean, reliable setup.

---

## Branch 3 — Creating an Environment

```bash
(base) $ conda create -y -n pydata-book python=3.10
```

`conda create` builds a **brand-new, isolated environment**. Breaking down the flags:

| Piece | Meaning |
|---|---|
| `conda create` | make a new environment |
| `-y` | **y**es to all prompts — don't stop to ask "Proceed? [y/n]", just do it |
| `-n pydata-book` | **n**ame the environment `pydata-book` |
| `python=3.10` | install **Python 3.10** into it (and its core dependencies) |

The result is a self-contained Python 3.10 setup living under your conda folder. Anything you install while it's active goes **only** into this environment — it can't break your `base` install or any other project.

> [!note] Why pin `python=3.10`?
> Specifying an exact version means the project runs on a known, tested interpreter. Different projects can have different Python versions side by side — one env on 3.10, another on 3.12 — with no conflict. (`-n` names it; the alternative `-p /path` puts an env at a specific folder instead.)

---

## Branch 4 — Activating the Environment

```bash
(base) $ conda activate pydata-book
(pydata-book) $
```

`conda activate pydata-book` **switches into** the environment you just made. Notice the prompt changed from `(base)` to `(pydata-book)` — that's the confirmation it worked. From now on:

- `python` runs **this environment's** Python 3.10.
- `conda install ...` or `pip install ...` puts packages **here**, isolated from everything else.

To leave and return to `base`:

```bash
(pydata-book) $ conda deactivate
(base) $
```

---

## Branch 5 — Other Everyday Commands

Once you understand the four above, these round out day-to-day use:

| Command                              | What it does                                            |
| ------------------------------------ | ------------------------------------------------------- |
| `conda env list`                     | list all your environments (a `*` marks the active one) |
| `conda install <pkg>`                | install a package into the active environment           |
| `conda install numpy pandas jupyter` | install several at once                                 |
| `conda list`                         | show every package installed in the active environment  |
| `conda remove -n <name> --all`       | delete an entire environment                            |
| `conda deactivate`                   | leave the current environment                           |

---

## Key Takeaways

- **Conda** manages both **packages** and isolated **environments**; the `(name)` in your prompt shows which environment is active.
- `conda config --add channels conda-forge` + `--set channel_priority strict` sets **conda-forge** as the primary, consistent package source — the recommended clean baseline.
- `conda create -y -n NAME python=X.Y` builds a new isolated environment: `-y` skips prompts, `-n` names it, `python=X.Y` pins the version.
- `conda activate NAME` switches into it (prompt changes); `conda deactivate` returns to `base`.
- Everyday helpers: `conda env list`, `conda install`, `conda list`, `conda remove -n NAME --all`.

---

## Related

- **[Conda vs Pip](<Conda vs Pip.md>)** — how `conda install` differs from `pip install`, and how to safely use both.

---

### Sources

| Source | Date | Type |
|---|---|---|
| Python for Data Analysis, 3e (Wes McKinney) — setup instructions | 2026 | Book |
| Conda — official documentation | 2026 | Tool reference |
