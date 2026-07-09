# `git checkout` — Switch Branches & Restore Files

`git checkout` is Git's Swiss-army navigation command. It moves `HEAD` — either to a different branch, a specific commit, or a previous version of a file.

> [!info] Two jobs, one command
> Historically `git checkout` handled both branch switching **and** file restoration. This dual role confused many users, so modern Git added two replacements:
> - `git switch` — for changing branches
> - `git restore` — for restoring files
>
> `git checkout` still works for both and remains widespread.

---

## Switching Branches

```bash
git checkout main                # switch to main
git checkout feature-x           # switch to feature-x
git checkout -b feature-y        # create feature-y and switch to it
git checkout -b hotfix main      # create hotfix off main (not current HEAD)
```

> [!warning] Uncommitted changes can block a checkout
> If your working tree has modifications that would be overwritten by the target branch, Git refuses. Either commit, stash (`git stash`), or discard them first.

---

## Checking Out Remote Branches

```bash
git fetch --all
git checkout feature-x                       # modern: creates local branch tracking origin/feature-x
git checkout -b feature-x origin/feature-x   # older syntax, still works
```

---

## Checking Out Files

Restore a file from the index (or a past commit) without changing branches:

```bash
git checkout -- file.md                      # discard unstaged changes in file.md
git checkout HEAD~2 -- file.md               # grab file.md from 2 commits ago
git checkout abc1234 -- src/app.py           # grab file from a specific commit
```

The `--` disambiguates the filename from a branch name in case they collide.

---

## Detached HEAD State

Checking out a raw commit hash — instead of a branch — detaches `HEAD`:

```bash
git checkout abc1234
# You are in 'detached HEAD' state...
```

> [!warning] Commits in detached HEAD can be lost
> Any new commits you make aren't anchored to a branch. If you switch away without creating one, those commits become unreachable and eventually get garbage-collected. To save work from a detached HEAD:
>
> ```bash
> git checkout -b rescue-branch
> ```

---

## Related Commands

| Command | What it does |
|---|---|
| `git switch <branch>` | Modern equivalent for branch switching only |
| `git switch -c <new-branch>` | Modern equivalent of `checkout -b` |
| `git restore <file>` | Modern equivalent for file restoration |
| `git branch` | Create branches without switching |

---

## Typical Workflow

```bash
git checkout -b feature-login       # start a feature branch
# ...work, commit...
git checkout main                   # back to main
git merge feature-login             # integrate
git branch -d feature-login         # cleanup
```

---

## See Also

- [[Branching (Main)]] — overview of branches
- [[git merge]] — combine branches after checking out
- [[Merge Conflicts]] — when a checkout would clash
- [[Git Essential Commands]] — related local commands
