# `git fetch` — Download Without Merging

`git fetch` downloads new commits, files, and refs from a remote into your local repo — **without** touching your working directory or current branch. It's the safe way to ask "what's new on the server?" before deciding how to integrate it.

> [!info] Fetch is non-destructive
> After `git fetch`, your working directory looks exactly the same as before. The only thing that changed is the `refs/remotes/` section of your `.git/` folder.

---

## Local vs Remote-Tracking Branches

Git maintains two sets of branch refs:

| Type | Location | Example | Writable? |
|---|---|---|---|
| Local | `.git/refs/heads/` | `main` | Yes — you commit to it |
| Remote-tracking | `.git/refs/remotes/` | `origin/main` | No — only `fetch` / `pull` updates it |

A `fetch` updates the remote-tracking refs. Merging them into your local branch is a separate step.

---

## Syntax

```bash
git fetch <remote>                    # fetch all branches from <remote>
git fetch <remote> <branch>           # fetch one branch only
git fetch --all                       # fetch from every registered remote
git fetch --dry-run                   # show what would be fetched, don't fetch
git fetch --prune                     # also delete local refs for deleted remote branches
```

---

## Typical Workflow

```bash
git fetch origin                      # download new refs
git log --oneline main..origin/main   # see what's new on remote
git merge origin/main                 # integrate when ready
```

Or more compactly:
```bash
git fetch origin && git merge origin/main
# ...which is the same as:
git pull origin main
```

See [[git pull]] for the one-step version.

---

## Inspecting a Fetched Branch

After `git fetch`, you can check out a remote branch without merging:

```bash
git checkout origin/feature-x         # detached HEAD — read-only
git checkout -b feature-x origin/feature-x   # create a local tracking branch
```

---

## Why Prefer `fetch` Over `pull`?

> [!tip] Rule of thumb
> If you want to **see** changes before they touch your working tree, use `fetch`. If you want the changes applied immediately, use `pull`.

Fetching first is the safer habit for shared branches — you get a chance to spot unexpected commits or conflicts before they collide with work in progress.

---

## See Also

- [[Syncing (Main)]] — the big picture
- [[git pull]] — fetch + merge in one command
- [[git remote]] — managing which remotes you fetch from
- [[Git Essential Commands]] — local-side commands
