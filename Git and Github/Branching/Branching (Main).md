# Branching — Independent Lines of Development

A **branch** in Git is a lightweight pointer to a specific commit. Branches let you work on features, experiments, or bug fixes in isolation from the main codebase, then merge the results back when they're ready.

> [!info] Branches are pointers, not copies
> Unlike older version-control systems that duplicate files or folders, Git branches are just a reference stored in `.git/refs/heads/<branch-name>` — a single file containing a commit hash. Creating a branch is nearly instant and costs almost no disk space.

---

## The Core Commands

| Command                        | Purpose                                                           |
| ------------------------------ | ----------------------------------------------------------------- |
| `git branch` *(covered below)* | Create, list, rename, delete branches                             |
| [[git checkout]]               | Switch between branches (or restore files)                        |
| [[git merge]]                  | Integrate one branch into another (adds a merge commit)           |
| [[git rebase]]                 | Integrate by replaying commits onto a new base (rewrites history) |
| [[git cherry-pick]]            | Copy **individual commits** between branches without merging      |

Conflicts that arise during merging, rebasing, or cherry-picking are covered separately in [[Merge Conflicts]].

---

## How a Branch Works

```mermaid
gitGraph
    commit id: "A"
    commit id: "B"
    branch feature
    commit id: "C"
    commit id: "D"
    checkout main
    commit id: "E"
```

- `main` points at commit `E`
- `feature` points at commit `D`
- Both branches share history up to commit `B`
- Switching branches moves `HEAD` — the "you are here" marker — between these pointers

---

## `git branch` — Managing Branches

```bash
git branch                       # list local branches (current marked with *)
git branch -a                    # list local + remote-tracking branches
git branch feature-x             # create a new branch from current HEAD (doesn't switch)
git branch -d feature-x          # delete a merged branch
git branch -D feature-x          # force-delete an unmerged branch
git branch -m old-name new-name  # rename
```

> [!tip] `-d` refuses to delete unmerged work
> Use `-D` (capital) only when you're intentionally discarding commits. Lowercase `-d` is the safety-checked version.

---

## Typical Branching Workflow

```mermaid
sequenceDiagram
    participant You
    participant Main as main
    participant Feature as feature-x
    You->>Feature: git checkout -b feature-x
    You->>Feature: commit, commit, commit
    You->>Main: git checkout main
    You->>Main: git merge feature-x
    You->>Feature: git branch -d feature-x
```

1. Branch off main — `git checkout -b feature-x`
2. Work in isolation, committing freely
3. Switch back to main — `git checkout main`
4. Integrate — `git merge feature-x` (see [[git merge]])
5. Delete the branch — `git branch -d feature-x`

---

## Release Branches and Backporting

Some branches aren't short-lived feature work — they're **long-lived release branches** that hang around for months or years, receiving patches for customers still on older versions. A team might carry `main`, `release-2.0`, and `release-1.0` simultaneously.

```mermaid
gitGraph
    commit id: "v1.0"
    branch release-1.0
    checkout main
    commit id: "dev"
    commit id: "v2.0"
    branch release-2.0
    checkout main
    commit id: "feat"
    commit id: "fix"
```

When a fix lands on `main`, it often has to be **backported** to one or more release branches — the same change, re-applied on a different line of history.

### Three ways to backport

| Situation                                        | Tool                                                  |
| ------------------------------------------------ | ----------------------------------------------------- |
| The original commits are known, standalone       | `git cherry-pick <sha1> <sha2> <sha3>`                |
| The feature branch still exists                  | `git merge <branch>` directly onto the release branch |
| Only a **merge commit** remains (branch deleted) | `git cherry-pick -m 1 <merge-sha>`                    |

The third case — lumping a deleted feature branch's contents into one commit on a release branch — is the canonical use of [[git cherry-pick]]'s `-m` flag. See [[git cherry-pick#Cherry-Picking a Merge Commit]] for the full walkthrough.

> [!tip] Keep release branches short on commits
> Many teams enforce "one commit per release patch" to keep release-branch history auditable. Cherry-picking a merge with `-m 1` delivers exactly that: the whole fix as a single commit, with the cost that granular messages and bisectability are lost.

---

## Local vs Remote Branches

| Type                       | Where it lives              | Who updates it           |
| -------------------------- | --------------------------- | ------------------------ |
| **Local branch**           | `.git/refs/heads/`          | Your local commits       |
| **Remote-tracking branch** | `.git/refs/remotes/origin/` | `git fetch` / `git pull` |

A local branch can *track* a remote one so `git push` / `git pull` work without arguments. Set tracking with `-u`:

```bash
git push -u origin feature-x
```

See [[Syncing (Main)]] for the full remote-sync story.

---

## Related Notes

- [[git checkout]] — switch branches, restore files
- [[git merge]] — combine branches
- [[git rebase]] — replay commits on a new base
- [[git cherry-pick]] — copy single commits across branches
- [[Squashing Commits]] — collapse multiple commits into one
- [[Merge Conflicts]] — what to do when Git can't auto-combine
- [[Syncing (Main)]] — pushing branches to remotes
- [[GitHub pull request]] — the review layer that sits on top of branch merges
- [[Git Essential Commands]] — local-side basics
