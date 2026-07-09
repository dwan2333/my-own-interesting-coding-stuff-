# Merge Conflicts — When Git Can't Auto-Combine

A **merge conflict** happens when two branches make incompatible changes to the same region of a file — or when one branch deletes a file the other modified. Git refuses to guess; it stops the merge and hands you the conflicted files to resolve manually.

> [!info] Conflicts aren't errors, they're decisions
> Git is telling you it doesn't have enough information to pick a winner. Your job is to decide what the final content should be.

---

## Two Moments a Conflict Can Hit

| Timing             | Cause                                             | Error message                                          |
| ------------------ | ------------------------------------------------- | ------------------------------------------------------ |
| **At merge start** | Uncommitted changes in your working tree or index | `error: Entry '<file>' not uptodate. Cannot merge.`    |
| **During merge**   | Branches edited the same lines differently        | `error: Entry '<file>' would be overwritten by merge.` |

The first kind is fixed by committing or stashing first. The second kind is the "classic" merge conflict.

---

## What a Conflict Looks Like in a File

Git rewrites the conflicted region with three marker lines:

```
<<<<<<< HEAD
content from the current branch (where you ran merge)
=======
content from the branch being merged in
>>>>>>> feature-x
```

- **`<<<<<<< HEAD`** — everything between this line and `=======` is *your* side
- **`=======`** — separator
- **`>>>>>>> feature-x`** — everything above this and below `=======` is *their* side

---

## Identifying Conflicts

```bash
git status                   # lists 'Unmerged paths:'
git diff                     # shows the conflict markers in context
git log --merge              # shows commits unique to each side — useful for context
git diff --name-only --diff-filter=U   # just the conflicted filenames
```

---

## Resolving — The Manual Way

1. Open each conflicted file
2. Find every `<<<<<<<` block
3. Edit the region down to whatever the correct final content should be (some mix of both sides, one side only, or something new)
4. Delete all three marker lines
5. Save, stage, commit:

```bash
git add <resolved-files>
git commit               # Git prefills a merge commit message
```

---

## Resolving — Shortcuts

### Take one side wholesale

```bash
git checkout --ours   path/to/file       # keep the current branch's version
git checkout --theirs path/to/file       # take the incoming branch's version
git add path/to/file
```

### Abort and try again

```bash
git merge --abort                        # return to the pre-merge state
```

### Nuke and restart

```bash
git reset --merge                        # reset to pre-merge, clearing index and working tree of conflict state
```

---

## Preventive Habits

> [!tip] Merge conflicts get exponentially worse with branch age
> - Pull from `main` into your feature branch regularly (`git pull origin main`) so conflicts stay small
> - Keep feature branches short-lived
> - Commit frequently on your feature branch so Git has fine-grained common ancestors to reason about
> - Communicate on shared files — if two people touch the same module, coordinate

---

## Example End-to-End

```bash
$ git merge feature-x
Auto-merging app.py
CONFLICT (content): Merge conflict in app.py
Automatic merge failed; fix conflicts and then commit the result.

$ git status
On branch main
You have unmerged paths.
  Unmerged paths:
    both modified:   app.py

# ...edit app.py in your editor, remove <<<, ===, >>> markers, save...

$ git add app.py
$ git commit -m "Merge feature-x into main"
```

---

## See Also

- [[git merge]] — the command that triggers conflicts
- [[git rebase]] — conflicts during rebase resolve the same way (per-commit)
- [[git cherry-pick]] — same 3-way merge, same markers, same `--continue` / `--abort` flow
- [[git checkout]] — `--ours` and `--theirs` shortcuts
- [[Branching (Main)]] — why we have branches in the first place
- [[git pull]] — pull conflicts resolve the same way
