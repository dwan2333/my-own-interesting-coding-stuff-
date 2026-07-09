# `git remote` — Managing Remote Connections

`git remote` is the command for managing the list of remote repositories your local repo knows about. Each remote is a name (like `origin`) mapped to a URL.

> [!info] Remotes are bookmarks, not branches
> A remote doesn't contain code — it's just a pointer to another repository. The code you fetch from it lives in `refs/remotes/<name>/` inside your `.git/` directory.

---

## Viewing Remotes

```bash
git remote          # list remote names
git remote -v       # list names + URLs (fetch and push)
```

A freshly cloned repo shows one:
```
origin  https://github.com/user/repo.git (fetch)
origin  https://github.com/user/repo.git (push)
```

---

## Subcommands

| Subcommand                        | Purpose                                                          |
| --------------------------------- | ---------------------------------------------------------------- |
| `git remote add <name> <url>`     | Register a new remote                                            |
| `git remote rename <old> <new>`   | Rename an existing remote                                        |
| `git remote rm <name>`            | Remove a remote                                                  |
| `git remote show <name>`          | Show fetch/push URLs and tracked branches                        |
| `git remote set-url <name> <url>` | Change the URL for an existing remote                            |
| `git remote get-url <name>`       | Print the URL for a remote                                       |
| `git remote prune <name>`         | Delete local refs to branches that no longer exist on the remote |
|                                   |                                                                  |

---

## Examples

### Add a teammate's fork

```bash
git remote add john https://github.com/john/repo.git
git fetch john
git checkout john/feature-x
```

### Rename `origin` to `upstream`

```bash
git remote rename origin upstream
```

Git rewrites `.git/config` and updates all remote-tracking branches (e.g., `origin/main` becomes `upstream/main`).

### Change a URL (e.g., switch from HTTPS to SSH)

```bash
git remote set-url origin git@github.com:user/repo.git
```

### Clean up stale remote-tracking branches

```bash
git remote prune origin --dry-run   # preview
git remote prune origin             # actually delete
```

---

## The `origin` Convention

When you `git clone <url>`, Git automatically registers the clone source as a remote named `origin`. Nothing is special about the name — it's just a default. You can rename or remove it.

> [!tip] `origin` is a convention, not a keyword
> Every other Git command that mentions `origin` (like `git push origin main`) is just referencing the bookmark. You could rename it to `home` and everything still works, provided you use the new name.

---

## See Also

- [[Syncing (Main)]] — overview of remote controls
- [[git fetch]] — download from a remote
- [[git push]] — upload to a remote
- [[git pull]] — fetch + merge in one step
- [[Git Essential Commands]] — local-side commands
