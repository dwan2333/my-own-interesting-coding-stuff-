# Git Index & Object Store (Core Internals)

## The Object Store

The object store is Git's permanent database, stored in `.git/objects/`. Every piece of data Git tracks is stored as one of four object types:

- **Blob** — the raw content of a file (no filename, just data)
- **Tree** — a snapshot of a directory, mapping filenames to blobs
- **Commit** — a pointer to a tree + metadata (author, message, parent commit)
- **Tag** — a named pointer to a specific commit

Once an object is written, it is **immutable** — it can never be changed. This is what makes Git's history tamper-proof.

## The Index (Staging Area)

The index is a binary file at `.git/index` — a middle layer between your working directory and the object store.

```
Working Directory  →  git add  →  Index (Staging)  →  git commit  →  Object Store
```

## Why Does the Index Exist? Why Not Commit Directly?

Without the index, every commit would capture *everything* in your working directory — every half-finished change, every experimental edit, every file you touched but didn't mean to include. You would lose the ability to shape your commits.

The index exists to give you **control over what goes into each commit:**

- **Selective staging** — you might have changed 5 files, but only 2 are related to the bug fix you're committing. The index lets you stage just those 2 and commit them cleanly, while the other 3 stay in your working directory for a separate commit later.
- **Reviewing before committing** — the index acts as a checkpoint. You stage changes, inspect them with `git diff --cached`, and only commit when you're satisfied. Without this step, mistakes go straight into history.
- **Building commits incrementally** — you can stage parts of your work over time, assembling a coherent commit piece by piece, rather than being forced to commit everything at once.
- **Separating "save" from "record"** — saving a file to disk (working directory) is not the same as recording it in history (object store). The index is the deliberate act in between — your declaration that "this specific set of changes is ready to become permanent."

**In short:** the object store is permanent and immutable. Committing directly to it with no staging step would be like publishing a book with no editing phase — every draft mistake becomes permanent history. The index is your editing desk.
