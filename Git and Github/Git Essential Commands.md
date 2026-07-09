# Git Commands

## `git init`

Initializes a new Git repository in the current folder. Creates the hidden `.git/` directory where all version history and configuration is stored.

```bash
git init
```

## `git add`

Moves file changes from your working directory into the index (staging area), marking them to be included in the next commit.

```bash
git add filename.md      # stage a specific file
git add .               # stage all changes in current directory
```

## `git commit -m 'message'`

Takes everything currently in the index and saves it as a permanent snapshot in the object store. The `-m` flag lets you write the commit message inline.

```bash
git commit -m "Add treasury bonds guide"
```

## `git mv <file> <new-name>`

Renames or moves a file and automatically stages the change — equivalent to renaming the file manually and running `git add`. Keeps Git's history intact.

```bash
git mv old_name.md new_name.md
```

## `git rm -f <file>`

Removes a file from both your working directory **and** the index. The deletion is staged and will be recorded in the next commit.

```bash
git rm -f filename.md
```

## `git rm --cached <file>`

Removes a file from the index (stops tracking it) **without** deleting it from your working directory. Useful when you accidentally staged a file you don't want Git to track (e.g., a `.env` file).

```bash
git rm --cached secret.env
```

## `git status`

Shows the current state of your working directory and index. It reports three zones:

| Section                           | What it means                                                     |
| --------------------------------- | ----------------------------------------------------------------- |
| **Changes to be committed**       | Files in the index, staged and ready for the next commit          |
| **Changes not staged for commit** | Files Git tracks but that have been modified since the last stage |
| **Untracked files**               | Files Git has never seen before — not in the index or history     |

```bash
git status
```

---

## `git config` — Configuration Levels & Files

Git stores configuration in three files, each scoped to a different level. Narrower scope overrides broader scope:

| Level | Flag | File Location | Scope |
|---|---|---|---|
| **System** | `--system` | `C:\ProgramData\Git\config` (Windows) | All users, all repos on the machine |
| **Global** | `--global` | `C:\Users\<username>\.gitconfig` | All repos for the current OS user |
| **Local** | `--local` (default) | `<repo>/.git/config` | Only the current repository |

**Precedence: local > global > system** — Git starts at local and bubbles up. The most specific value wins.

### Configure Your Identity

Every commit permanently embeds your name and email. Set them globally so they apply to all repos:

```bash
git config --global user.name "Your Name"
git config --global user.email "you@example.com"
```

To override for a single repo, run the same commands without `--global` (defaults to `--local`):

```bash
git config user.name "Work Name"
git config user.email "work@company.com"
```

### Configure the Default Branch

Since Git 2.28, you can change the default branch name created by `git init` (previously always `master`):

```bash
git config --global init.defaultBranch main
```

### Remove Config Properties

**Unset a single key:**
```bash
git config --global --unset user.name
```

**Unset all values for a key** (if a key has multiple entries):
```bash
git config --global --unset-all user.name
```

**Remove an entire section:**
```bash
git config --global --remove-section user
```

### View Config

```bash
git config --list            # list all active config values
git config --global --edit   # open global config in your default editor
```

---

## `git log`

Shows the commit history of the current branch — each commit's hash, author, date, and message, with the newest at the top. Useful for reviewing what's been done and finding the commit hash you need for other commands.

```bash
git log                       # full history with author, date, message
git log --oneline             # condensed — one commit per line
git log --graph --oneline     # visual branch graph
git log -n 5                  # show only the last 5 commits
git log -- filename.md        # history filtered to one file
```

## `git show`

Displays everything about a single commit — the commit metadata (hash, author, date, message) **and** the full diff of what that commit changed. If you don't pass a hash, it shows the most recent commit (`HEAD`).

```bash
git show                      # show the most recent commit
git show a1b2c3d              # show a specific commit by hash
git show HEAD~2               # show the commit 2 steps before HEAD
git show a1b2c3d -- file.md   # show only one file's changes in that commit
```

## `git diff`

Shows the differences between two states of your files. By default, it compares your **working directory** against the **index** — in other words, changes you've made but haven't staged yet.

```bash
git diff                     # unstaged changes (working dir vs index)
git diff filename.md         # diff for a specific file only
git diff HEAD                # everything different from the last commit (staged + unstaged)
git diff branch1..branch2    # compare two branches
```

### `git diff --cached` (same as `--staged`)

Shows the differences between the **index** and the **last commit** — what will be included in your next commit if you ran `git commit` right now. This is the counterpart to plain `git diff`, which only shows unstaged changes.

| Command | Compares | Answers the question |
|---|---|---|
| `git diff` | Working dir ↔ Index | What have I changed but not staged? |
| `git diff --cached` | Index ↔ Last commit | What have I staged for the next commit? |
| `git diff HEAD` | Working dir ↔ Last commit | What's different from the last commit in total? |

```bash
git diff --cached             # staged changes only
git diff --staged             # identical — same command, different flag name
```

## `git restore --staged <file>`

Removes a file from the index (unstages it) **without** changing the file's contents in your working directory. Useful when you ran `git add` on something by mistake — the changes are still there, just no longer lined up for the next commit.

```bash
git restore --staged file.md   # unstage a single file
git restore --staged .         # unstage everything currently staged
```

Compare to `git rm --cached`, which stops tracking the file entirely. `git restore --staged` only undoes the most recent `git add` — the file remains tracked.

---

## `git clone`

Copies an entire existing repository from a remote source (usually GitHub) onto your local machine. Downloads the full history, all branches, and all files, and automatically sets up the remote connection so you can `git pull` and `git push` later. This is typically the first command you run when starting work on someone else's project or setting up an existing repo on a new computer.

```bash
git clone https://github.com/user/repo.git              # clone into a folder named "repo"
git clone https://github.com/user/repo.git my-folder    # clone into a custom folder name
git clone --depth 1 https://github.com/user/repo.git    # shallow clone — only latest commit (faster, smaller)
git clone -b dev https://github.com/user/repo.git       # clone and check out a specific branch
git clone git@github.com:user/repo.git                  # clone via SSH (needs SSH key set up)
```

### HTTPS vs SSH

| Protocol | URL format | When to use |
|---|---|---|
| **HTTPS** | `https://github.com/user/repo.git` | Simpler — works anywhere, asks for username/password (or token) |
| **SSH** | `git@github.com:user/repo.git` | Requires SSH key setup, but no password prompts after that |

### What `git clone` Actually Does Under the Hood

It runs several steps in one: creates a new folder, runs `git init` inside it, adds the remote URL as `origin`, and then fetches and checks out the default branch. So cloning is equivalent to:

```bash
mkdir repo && cd repo
git init
git remote add origin <url>
git fetch origin
git switch main
```

You almost never need to do it that way — `git clone` exists precisely to collapse all those steps into one.

---

## Syncing with Remotes

These four commands connect your local repo to remote repositories. Brief summaries here — see [[Syncing (Main)]] for the full overview and the linked deep-dive notes for each command.

### `git remote`

Manages the list of remote repositories your local repo knows about. Each remote is a name (like `origin`) mapped to a URL.

```bash
git remote -v                               # list remotes with URLs
git remote add upstream <url>               # register a new remote
git remote rename origin upstream           # rename
git remote set-url origin <new-url>         # change a remote's URL
git remote rm <name>                        # delete a remote
```

See [[git remote]] for every subcommand and examples.

### `git fetch`

Downloads new commits and refs from a remote **without** modifying your working directory. The safe way to preview what's upstream before integrating.

```bash
git fetch origin                            # download all branches from origin
git fetch origin main                       # just one branch
git fetch --all                             # every registered remote
git fetch --prune                           # also delete stale remote-tracking refs
```

After fetching, remote commits live under `refs/remotes/origin/` — inspect with `git log origin/main` before merging. See [[git fetch]].

### `git push`

Uploads local commits to a remote branch. Only pushes what's already committed.

```bash
git push origin main                        # push main to origin
git push -u origin feature-x                # first push — set upstream
git push --tags                             # include tags (not pushed by default)
git push origin --delete feature-x          # delete remote branch
git push --force-with-lease origin main     # safer force push
```

> [!warning] `--force` overwrites remote history
> Use `--force-with-lease` instead — it aborts if someone else pushed since your last fetch. See [[git push]] for full detail.

### `git pull`

Fetches from a remote and immediately merges into your current branch. Equivalent to `git fetch` + `git merge`.

```bash
git pull                                    # pull current branch from its upstream
git pull origin main                        # explicit remote + branch
git pull --rebase origin main               # rebase instead of merge for linear history
```

See [[git pull]] for the merge-vs-rebase trade-off and safety notes.

---

## Branching & Merging

Four commands for working with independent lines of development. See [[Branching (Main)]] for the overview.

### `git branch`

Creates, lists, renames, or deletes branches — without switching to them.

```bash
git branch                       # list local branches
git branch -a                    # list local + remote
git branch feature-x             # create (doesn't switch)
git branch -d feature-x          # delete merged branch
git branch -D feature-x          # force-delete unmerged branch
git branch -m old new            # rename
```

Covered in [[Branching (Main)]].

### `git checkout`

Switches branches or restores files.

```bash
git checkout feature-x           # switch branches
git checkout -b feature-y        # create + switch
git checkout -- file.md          # discard unstaged changes in file.md
git checkout HEAD~2 -- file.md   # grab file from 2 commits ago
```

> [!warning] Checking out a commit hash creates a detached HEAD
> Commits made there aren't anchored to a branch — save them with `git checkout -b rescue-branch` before switching away. See [[git checkout]].

### `git merge`

Combines another branch into the current one.

```bash
git merge feature-x              # merge feature-x into current branch
git merge --no-ff feature-x      # force a merge commit (preserve branch history)
git merge --squash feature-x     # flatten feature into one commit
git merge --abort                # cancel a merge in progress
```

See [[git merge]] for fast-forward vs three-way merge.

### `git rebase`

Replays your branch's commits on top of a new base — producing a linear history instead of a merge commit. Use on local branches only.

```bash
git rebase main                  # replay current branch onto latest main
git rebase -i HEAD~3             # interactive — squash, reword, reorder last 3
git rebase --continue            # after resolving conflicts
git rebase --abort               # cancel and restore pre-rebase state
git pull --rebase                # pull that rebases instead of merging
```

> [!warning] The golden rule — never rebase public history
> Rebasing rewrites commits with new SHA-1s. If others have based work on those commits, rebasing forces them to reconcile duplicate histories. Safe on private branches only. See [[git rebase]] for the full rules and recipes.

### `git cherry-pick`

Copies one or more existing commits by SHA and replays them onto your current branch as new commits. Use for hotfixes, backports, or rescuing a commit from the wrong branch — not as a substitute for merge or rebase.

```bash
git cherry-pick <sha>                    # apply one commit to current branch
git cherry-pick <sha1> <sha2>            # apply multiple commits in order
git cherry-pick <sha1>..<sha5>           # range (sha1 exclusive → sha5 inclusive)
git cherry-pick -x <sha>                 # append "(cherry picked from ...)" to message
git cherry-pick -n <sha>                 # stage changes without committing
git cherry-pick -m 1 <merge-sha>         # cherry-pick a merge commit (mainline = parent 1)
git cherry-pick --continue               # after resolving conflicts
git cherry-pick --abort                  # cancel and restore pre-pick state
```

> [!warning] Cherry-pick creates duplicate commits with new hashes
> Great for one-off transplants (hotfixes, backports). Overusing it fragments history and causes phantom conflicts when the source branch is later merged. See [[git cherry-pick]] for full pitfalls.

### Squashing Commits

Combining multiple commits into one. Not a standalone command — done via rebase, merge, or reset:

```bash
git rebase -i HEAD~5             # interactive: pick one, mark others 'squash' or 'fixup'
git merge --squash feature-x     # merge a whole branch as one unstaged change
git reset --soft HEAD~5          # flatten last 5 commits, then git commit
```

See [[Squashing Commits]] for method comparison and when to use each.

### Merge Conflicts

When the same lines change in both branches, Git halts and marks the conflict with `<<<<<<<`, `=======`, `>>>>>>>` in the affected files. Resolve by editing, then:

```bash
git add <resolved-file>
git commit
# or to bail out entirely:
git merge --abort
```

Full resolution guide: [[Merge Conflicts]].

---




