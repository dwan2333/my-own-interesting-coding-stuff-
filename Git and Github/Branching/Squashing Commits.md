# Squashing Commits — Combining Many into One

**Squashing** means combining multiple Git commits into a single commit. It's not a standalone command — it's a *technique* you apply using `git rebase -i`, `git merge --squash`, or `git reset --soft`. The goal is always the same: take N messy commits, produce 1 clean commit with the same code.

> [!info] Squash is about the story, not the code
> The final code is identical whether you squash or not. What changes is the **history** — how the work is narrated in the git log.

---

## Why Squash?

A typical branch after a day of work looks like this:

```
a1b2c3d  fix typo
b2c3d4e  wip
c3d4e5f  oh wait that was wrong
d4e5f6g  add validation
e5f6g7h  login form
```

A reviewer doesn't care about your bumbling — they want to see **the one logical change** you added. Squashing gives you:

| Benefit                 | Reason                                                     |
| ----------------------- | ---------------------------------------------------------- |
| **Clean history**       | Main reads as feature-by-feature, not WIP-by-WIP           |
| **Easier `git bisect`** | Each commit is a complete, testable unit                   |
| **Better `git blame`**  | Blame points to the real reason for a line, not a typo fix |
| **Simpler reverts**     | One `git revert` undoes the whole feature                  |

---

## Method 1 — Interactive Rebase (most flexible)

The standard approach when you want control over which commits combine and how.

```bash
git rebase -i HEAD~5        # edit the last 5 commits
```

Git opens an editor:

```
pick a1b2c3d  login form
pick b2c3d4e  add validation
pick c3d4e5f  oh wait that was wrong
pick d4e5f6g  wip
pick e5f6g7h  fix typo
```

Change every `pick` except the first to `squash` (or `s`):

```
pick   a1b2c3d  login form
squash b2c3d4e  add validation
squash c3d4e5f  oh wait that was wrong
squash d4e5f6g  wip
squash e5f6g7h  fix typo
```

Save and close. Git then opens a second editor with all five messages concatenated, inviting you to write one combined message. Delete the noise, write something clean, save. Result:

```
x1y2z3a  Add login form with validation
```

Five commits → one commit. Same code.

> [!tip] `fixup` is `squash` without the message  juprompt
> If the extra commits werest typo fixes you want to discard, use `fixup` instead of `squash`. Git silently combines them and keeps only the first commit's message.

See [[git rebase]] for the full interactive-rebase guide.

---

## Method 2 — `git merge --squash` (whole branch, one commit)

When you want to merge an entire feature branch but turn the whole thing into a single commit on main:

```bash
git checkout main
git merge --squash feature-login
# All feature-login's changes are now staged in your working tree
git commit -m "Add login feature"
```

Key differences from interactive rebase:
- You don't pick *which* commits to combine — it's all of them
- The feature branch itself is **not modified** (no history rewrite on your branch)
- You must manually `git commit` afterward — the merge doesn't auto-commit

This is what GitHub's **"Squash and merge"** PR button does under the hood.

> [!warning] Don't keep working on a squash-merged branch
> If you add more commits to a branch after it's been squash-merged, your next PR re-includes the "already merged" changes (with new SHAs), causing duplicate-conflict pain. After a squash-merge: **delete the branch.**

---

## Method 3 — `git reset --soft` (quick & dirty)

A shortcut when you just want to flatten the last N commits into one, no editor dance:

```bash
git reset --soft HEAD~5     # rewind 5 commits, keep all changes staged --mixed (changes the index) and --hard (changes your working directory and index )
git commit -m "Your combined message"
```

What happens:
1. `--soft` moves the branch pointer back 5 commits **without touching the working directory or index**
2. All changes from those 5 commits are now staged
3. A new `git commit` captures all of it as one

Fast. But all-or-nothing — you lose the ability to keep some commits and squash others.

---

## Method Comparison

| Method | Control | Rewrites feature history? | Best for |
|---|---|---|---|
| `rebase -i` + `squash`/`fixup` | Fine-grained per commit | Yes | Selectively cleaning up noisy commits |
| `merge --squash` | Whole branch only | No (feature untouched) | Collapsing a finished feature into one commit on main |
| `reset --soft` + `commit` | Whole range only | Yes | Quick flatten in one command |
| GitHub "Squash and merge" | Whole PR only | No (server-side on main) | Reviewers who want one commit per PR |

---

## The Golden Rule (again)

Squashing via `rebase -i` or `reset --soft` **rewrites history** — old commits are replaced by new ones with different SHA-1s.

> [!warning] Never squash commits that have been pushed and shared
> If others have your old commits, squashing causes duplicate-history pain when they sync. Squash only on local, unshared branches.
>
> `git merge --squash` and the GitHub button are exceptions — they don't rewrite your feature branch, they produce a new squashed commit on main.

See [[git rebase]] for the full rules on rewriting history.

---

## Recovering from a Bad Squash

Squashed commits aren't gone — they're still reachable via reflog for ~90 days:

```bash
git reflog
# Find the entry just before the rebase/squash
git reset --hard HEAD@{N}
```

---

## When NOT to Squash

| Situation                                      | Why keep the commits                                                     |
| ---------------------------------------------- | ------------------------------------------------------------------------ |
| Each commit is a **separate logical change**   | Reviewer benefits from seeing them step-by-step                          |
| You want accurate `git blame` for sub-features | A collapsed commit blurs authorship                                      |
| The branch is already shared                   | Don't rewrite public history                                             |
| You're using `git bisect`                      | Bisecting through small commits narrows bugs faster than one huge commit |

Squashing is a tool for **story-telling**, not automation. If each commit already tells a clean story, leave them alone.

---

## See Also

- [[git rebase]] — the mechanism behind interactive squashing
- [[git merge]] — the `--squash` flag variant
- [[Branching (Main)]] — overview of branch workflows
- [[Git Essential Commands]] — `git reset` quick-reference
