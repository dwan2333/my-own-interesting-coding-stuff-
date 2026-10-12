# AGENTS.md: rules for Daniel's Coding core vault

This is Daniel's **reading vault for coding and algorithms**. Everything here is for him to read: neat, clear, easy to follow. It is published as a public website, so treat every note as public.

Read this whole file before changing anything here.

## 1. Daniel's three vaults

| Vault | Folder | What it's for |
|---|---|---|
| **Coding core** (this one) | `E:\Coding core` | Coding and algorithms notes he reads. Public website: https://dwan2333.github.io/my-own-interesting-coding-stuff-/ |
| **Knowledge core** | `E:\Knowledge core` | Math and finance notes he reads. Also a public website |
| **Brain** | `E:\AI Brain\Big Brain\Brain` | The agent's private memory of Daniel: his profile, preferences, every question, progress data. Private GitHub repo. Never copy Brain data into this vault |

- **Study questions:** best asked in a session opened in the Brain folder, which logs and files them automatically. If he asks one in a session opened here, answer it, save it as a question note (§5), and record it in the Brain by following `E:\AI Brain\Big Brain\Brain\AGENTS.md` §3.
- **Outdated skill:** don't use the `vault-note-creator` skill. Daniel retired it; it conflicts with these rules.

## 2. Layout

- **Topic folders:** notes live in topic folders at the top of the repo: `Conda`, `Data Structure and Algorithm`, `Git and Github`, `Python`, `Quant coding project`, `Small Coding Projects`. Subfolders group related notes, e.g. `Git and Github\Branching\`.
- **Overview notes:** a topic's overview note is named `<Title> (Main).md`.
- **Series notes:** number them in reading order: `1 - Short Title.md`, …
- **Code files:** working code (`.py`) sits next to the note that explains it, mostly in `Small Coding Projects`.
- **What gets published:** the website build (`.github\workflows\deploy-quartz.yml`) copies the **whole repo** into the site. It skips only the folders and files listed in its `rsync --exclude` lines. If you add a file at the top of the repo that shouldn't be published, add an exclude for it there.

## 3. Writing rules (they keep Obsidian and the website both working)

- **File names:** readable words, because his sidebar shows file names; command names stay as typed, e.g. `git rebase.md`. Never use underscores or snake_case for notes.
  - No `\ / : * ? " < > | # %`, and no dots except before the extension.
  - Every file name must be unique across the vault.
- **Links:** use the bare file name, `[text](<File Name.md>)`, with angle brackets when it has spaces. Add `#Heading` to link to a section.
  - **Never** use `../` or folder paths: the website resolves links by unique file name, and folder paths give "page not found".
- **Code:** in fenced blocks with a language tag (` ```python `, ` ```bash `, ` ```powershell `). Commands he types go in their own block.
- **Math:** LaTeX: `$…$` inline, and display math on its own lines between `$$` lines.
- **Money:** write the dollar sign as `&#36;`. A bare `$` is read as the start of math. Shell variables inside code blocks are fine.
- **Changing existing notes:** don't move, rename or delete his notes unless he asks. If you rename a file, update every link to it in the same change.

## 4. Git and publishing

- **Asking first:** the GitHub repo is `dwan2333/my-own-interesting-coding-stuff-`, and pushing to `main` publishes the website. Commit or push only when Daniel asks.
- **Commits:** commit only the files you changed. Never sweep in unrelated `.obsidian/` state.
- **Network:** GitHub needs his local proxy, `HTTPS_PROXY=http://127.0.0.1:7897`. Don't bypass the proxy; that fails. There is no `gh` command on this PC.
- **His backup:** his Obsidian Git plugin also commits and pushes ("vault backup: …").
- **Python on Windows:** run `python`, not `py`. The `py` launcher is broken in some of his terminals.

## 5. Question notes ("Questions I Had While Studying")

Each coding question Daniel asks gets one readable note, filed in the matching topic folder:
`<Topic>\Questions I Had While Studying\YYYY-MM-DD - Short Title.md`

If he sent a screenshot, save it next to the note under the same name. Use `python "E:\AI Brain\Big Brain\Brain\system\save_screenshot.py" --dest "<folder>" --name "<note name>"`, then look at the image to confirm it's his.

**One note per question, kept compact.** Follow-up questions about the same question or topic do **not** get a new note. Update the existing note so it captures the whole question, including every sub-question he asked, as one well-compacted summary:
- add only what's new, merged where it belongs (a new case, example, or a short "Follow-up" callout);
- update the Question Essence to cover it;
- never repeat what the note already says.

Start a new note only for a genuinely new question.

**Format: match his other notes here** (house style; see `git rebase.md` in `Git and Github\Branching` for a model).

```
# `<command or concept>` — <Title in Title Case>

_Question I had while studying · <topic> · asked YYYY-MM-DD_

<one or two plain sentences framing the question>

> [!info] Question Essence
> <3–5 sentences: what was asked (every sub-question) and the core idea of the answer>

---

## The Question
![<what it shows>](<YYYY-MM-DD - Short Title.png>)    ← if there is no screenshot, quote the code or error here

---

## <What's Going On / How It Works>     ← one section per sub-question
<explanation, with fenced code blocks (language tag) and Mermaid diagrams where they help>

> [!example] <runnable example>      > [!tip] <better way or rule of thumb>      > [!warning] <common mistake>

---

> [!tip] Key Takeaway
> <one or two lines>

---

## Related Documents
- **[Note Title](<File Name.md>)** — one line on how it connects.
```

- **Sections:** skip any section that doesn't apply. Use separators (`---`) between sections, as his notes do.
- **No repetition:** each idea appears exactly once.
