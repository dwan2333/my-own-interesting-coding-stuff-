# Writing Good Commit Messages

A good commit message tells future-you (or a teammate, or an automated changelog tool) **what changed and why** in 50 characters or less, with optional details below. The diff already shows *how*; the message exists to provide the context the diff can't.

This note covers the universally-agreed-on rules and the modern **Conventional Commits** standard that codifies them.

---

## The Three Parts of a Commit Message

| Part             | Required? | Length             | Purpose                                             |
| ---------------- | --------- | ------------------ | --------------------------------------------------- |
| **Subject line** | Yes       | ≤ 50 chars         | Imperative-mood headline of the change              |
| **Body**         | No        | Wrap at 72 chars   | Explain *what* and *why* (never *how*)              |
| **Footer**       | No        | One line per token | Metadata: `BREAKING CHANGE`, issue refs, co-authors |

Separate each part with a blank line. Most editors will do this automatically when you run `git commit` without `-m`.

---

## The Seven Rules of a Great Commit Message

The canonical rules, formalized by Chris Beams and adopted across the industry:

1. **Separate subject from body with a blank line.**
2. **Limit the subject line to 50 characters.**
3. **Capitalize the subject line.**
4. **Don't end the subject line with a period.**
5. **Use the imperative mood in the subject line.** Write "Add login button," *not* "Added login button" or "Adds login button."
6. **Wrap the body at 72 characters.**
7. **Use the body to explain *what* and *why*, not *how*.** The diff shows how.

> [!tip] The imperative-mood test
> A good subject line completes the sentence *"If applied, this commit will ___."* "If applied, this commit will *add login button*" reads correctly. "If applied, this commit will *added login button*" does not.

---

## Conventional Commits — The Modern Standard

A small disciplined dialect of the seven rules that adds machine-parseable structure:

```
<type>[optional scope]: <description>

[optional body]

[optional footer(s)]
```

Example:

```
feat(auth): add JWT login

Replace session cookies with stateless JWT to support
mobile clients that can't share browser cookies.

Closes #142
```

The point isn't decoration — tools like `semantic-release`, `conventional-changelog`, and `commitlint` parse these messages to auto-bump SemVer versions and generate changelogs.

### The Standard Type Keywords

| Type | When to use | SemVer effect |
|---|---|---|
| **`feat`** | New feature | MINOR bump |
| **`fix`** | Bug fix | PATCH bump |
| **`docs`** | Documentation only | None |
| **`style`** | Formatting, whitespace, no code change | None |
| **`refactor`** | Code change without feature/fix | None |
| **`perf`** | Performance improvement | PATCH (sometimes MINOR) |
| **`test`** | Adding/fixing tests | None |
| **`chore`** | Maintenance, deps, build tools | None |
| **`build`** | Build system changes | None |
| **`ci`** | CI/CD pipeline changes | None |
| **`revert`** | Reverts a previous commit | Depends on what's reverted |

Only `feat` and `fix` are formally part of the spec — the others are conventional but widely accepted.

### Breaking Changes

A breaking change triggers a SemVer **MAJOR** bump. Two equivalent ways to mark one:

```
feat!: remove deprecated /v1 API endpoint
```

Or via a footer:

```
feat(api): remove /v1 endpoint

BREAKING CHANGE: the /v1 endpoint has been removed. Migrate to /v2.
```

`!` alone is sufficient if the description is clear; the footer is for longer migration notes.

---

## Anti-Patterns

| Anti-pattern | What's wrong | Better |
|---|---|---|
| `fix a bug` | Vague — which bug? | `fix(auth): handle null session token on logout` |
| `Fixed login` | Past tense | `Fix login` (imperative) |
| `Update.` | Period + no detail | `chore(deps): update lodash to 4.17.21` |
| `oops`, `wip`, `saved` | Lazy / meaningless | A meaningful subject |
| `Add margin` | Missing the *why* | `Add margin to nav items to prevent overlap with logo` |
| `Add login feature.` | Period at end of subject | `Add login feature` |

---

## A Worked Example

**Bad:**

```
fix bug
```

**Good:**

```
fix(auth): handle null session token on logout

Logging out without an active session was throwing
TypeError: Cannot read property 'userId' of null. Now
checks for null and redirects to /login regardless.

Closes #287
```

The good version answers the three questions a reader actually has:

- *What changed?* → null session tokens now handled gracefully on logout
- *Why?* → the null was crashing a benign user action
- *Where's more context?* → issue #287

---

## Related Documents

- **[[Git Essential Commands]]** — `git commit` and the rest of the daily-driver commands
- **[[GitHub pull request]]** — PR titles typically follow Conventional Commits format too

---

## Sources

| Source | Type |
|---|---|
| [Conventional Commits 1.0.0 specification](https://www.conventionalcommits.org/en/v1.0.0/#summary) | Standard |
| [How to Write Better Git Commit Messages — freeCodeCamp](https://www.freecodecamp.org/news/how-to-write-better-git-commit-messages/) | Tutorial |
| [How to Write Good Git Commit Messages Like a Pro — Front End Weekly](https://medium.com/front-end-weekly/how-to-write-good-git-commit-messages-like-a-pro-2c12f01569d9) | Tutorial |
| [Commit Messages — The Odin Project](https://www.theodinproject.com/lessons/foundations-commit-messages) | Lesson |
