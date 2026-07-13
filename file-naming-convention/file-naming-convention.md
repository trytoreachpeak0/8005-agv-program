# Project File and Folder Naming Conventions

> **Scope:** All newly created folders and files under the project root (8005 Multi-Slot AGV).
> **Goals:** ① Safe and conflict-free on both Windows and Linux; ② Consistent, predictable naming across the project; ③ Names that clearly describe content for easy search and reference.
> **Note:** This guide applies only to **newly created** files and folders. Existing files do not need to be renamed immediately, but should gradually align with these conventions during future cleanup.

---

## 1. Four Core Principles

1. **Cross-platform safety:** The same naming rules must behave identically on Windows and Linux, avoiding issues where a file works on one machine but fails or becomes garbled after syncing to another.
2. **One separator style only:** Use kebab-case (hyphen-separated names) project-wide. Do not mix underscores, spaces, and camelCase across different files.
3. **Lowercase first:** Do not rely on case to distinguish files. Windows/macOS are case-insensitive by default, while Linux is case-sensitive — the same set of files can appear identical on one system but conflict or become unreachable on another.
4. **Meaningful names:** Names should reflect what the file or folder is about. Avoid uninformative names such as `new folder`, `final version`, or `v2-revised`.

---

## 2. Hard Rules for Both Systems (Must Follow)

Based on the restrictions of both Windows and Linux, adopt the safest common subset:

### 2.1 Forbidden Characters

Do not use the following characters in file or folder names (forbidden on both platforms even if Linux allows some of them):

```
\  /  :  *  ?  "  <  >  |
```

Also avoid all invisible control characters (such as Tab).

- `/` is the path separator on Linux; `\` is the path separator on Windows. Neither may appear in a file or folder name itself.
- `: * ? " < > |` are rejected outright on Windows. Although Linux allows them, do not use them for consistency.

### 2.2 No Spaces — Use Hyphens `-` Instead

Windows and Linux both "allow" spaces in file names, but spaces cause practical problems:

- Paths with spaces must be quoted in shells and scripts, which is error-prone (the existing `requirement documents` folder in this project is an example; new folders should use `requirement-documents` instead).
- In URLs and Markdown links, spaces become `%20`, which is ugly and bug-prone.
- Git, CI tools, and some CLI utilities handle spaced paths inconsistently.

**Conclusion: Do not use spaces. Join multiple words with hyphens `-`.**

### 2.3 No Trailing Spaces or Dots

Windows does not allow file or folder names to **end with a space or a dot `.`** (the system will strip them or reject the name even if you type them manually in Explorer). Be careful not to add trailing spaces when creating new files.

### 2.4 Do Not Use Windows Reserved Device Names

The following names are reserved on Windows and **cannot be used as file or folder names, regardless of case or extension**:

```
CON, PRN, AUX, NUL,
COM0, COM1 ~ COM9,
LPT0, LPT1 ~ LPT9
```

For example, `con.md`, `COM1.json`, and a folder named `NUL` are all invalid. Even if created on Linux, they will fail or error after syncing to Windows.

### 2.5 Case: Use Lowercase Only

- Windows/macOS file systems are **case-insensitive by default** (`Report.md` and `report.md` are treated as the same file).
- Linux file systems are **case-sensitive** (`Report.md` and `report.md` are two different files).
- Consequence: If one team member creates `Report.md` on Windows and another creates `report.md` on Linux, each side thinks they have a different file — syncing to the same system causes overwrites or conflicts.

**Conclusion: Use lowercase letters for all file and folder names.** To emphasize words, use hyphens rather than capitalization (e.g. `agv-task-flow.md`, not `AGVTaskFlow.md`).

> **Exception:** Widely accepted community filenames such as `README.md`, `LICENSE`, and `CHANGELOG.md` may keep their conventional casing and do not need to be forced to lowercase.

### 2.6 Length Limits

- Windows traditionally limits total path length to 260 characters (newer versions can enable long path support, but do not rely on that setting).
- Linux (ext4, etc.) limits a single file name to 255 **bytes**, not 255 characters — one Chinese character takes 3 bytes in UTF-8, so a Chinese-only filename may exceed the limit at around 80 characters.
- **Recommendation:** Keep individual file/folder names within 30 characters (about 15 Chinese characters), and total path length within 120 characters, to avoid "path too long" errors from sync, archive, and backup tools.

---

## 3. Separator Rules (The Core Question: What to Use Between Words)

**Unified rule: Use hyphens `-` project-wide (kebab-case).**

Rationale (aligned with GitHub, npm, mainstream open-source projects, and web standards):

| Separator Style | Example | Recommended? | Reason |
| --- | --- | --- | --- |
| Hyphen `kebab-case` | `agv-task-flow.md` | ✅ Recommended — use everywhere | URL/CLI friendly, no escaping needed; no conflicts on case-insensitive platforms; default convention on GitHub, GitLab, npm, Docker images, and most open-source projects |
| Underscore `snake_case` | `agv_task_flow.md` | ⚠️ Specific scenarios only | Use only when the filename must directly serve as a code identifier or database identifier, e.g. Python module names (`.py`) or SQL table/column naming habits. This project currently has no source files that need direct import, so **do not use underscores** to avoid maintaining two parallel rules |
| Space | `agv task flow.md` | ❌ Forbidden | Requires escaping in CLI, becomes `%20` in URLs, unstable in some tools |
| CamelCase / PascalCase | `agvTaskFlow.md` | ❌ Not for file names | Confuses easily with lowercase names on case-insensitive Windows; use only for internal code variables/class names, not file system naming |

> **Simple rule of thumb:** For folders and file names, always use **lowercase letters/digits + hyphens only**. If the project later introduces Python, JS, or other source code, follow each language's community conventions for source files (Python uses `snake_case.py`, React components use `PascalCase.tsx`), but that belongs to "code style" and is separate from the document/asset naming covered here.

---

## 4. Handling Chinese and English Names

This project's documentation is primarily in Chinese business semantics. Chinese names are allowed, but apply them consistently:

1. **Pure Chinese titles:** A complete Chinese phrase may be used directly as a file name. Do not force translation to English or insert hyphens between Chinese characters.
   Example: `焊线氮气柜送关卡任务说明.md` ✅
2. **Mixed Chinese + English/digits:** Separate Chinese from English and digits with hyphens. Do not use spaces or concatenate directly.
   Example: `rcs-接口清单.md`, `sql-脚本-送烘箱.sql` (not `rcs接口清单.md` or `rcs 接口清单.md`)
3. **No full-width punctuation:** Do not use Chinese punctuation in file names, such as `，。《》：？！、（）`. Use ASCII half-width `-`, `_` (if needed), `.`, and `()` instead.
4. **Consistent language within a category:** Files of the same type in the same directory should use either Chinese or English consistently — not a mix (e.g. both `装片完工送烘箱.sql` and `wire-bonding-finish.sql` in the same folder), to keep sorting and search predictable.
5. For cross-team collaboration or documents that may be shared with international vendors (e.g. RIOT, Standard Robots), prefer English kebab-case names for easier search and reference.

---

## 5. Dates and Version Numbers

- Dates must use **ISO 8601** format: `YYYY-MM-DD`, e.g. `2026-07-07`.
  - Do not use `07-07-2026`, `26-7-7`, or `0707` — the first is ambiguous across US/China date order; the last cannot sort correctly.
  - When a date is part of the file name, place it at the **beginning** so alphabetical sort equals chronological sort: `2026-07-07-需求评审纪要.md`.
- Version numbers use `v` + digits, hyphen-separated: `agv-interface-spec-v1.2.md`.
  - Do not use labels like "final version", "ultimate version", or "cannot revise anymore" — they cannot be sorted or compared.

---

## 6. Naming Suggestions by File Type (Based on Current Project)

| Type | Suggested Pattern | Example |
| --- | --- | --- |
| Requirements / docs (Markdown) | Chinese semantic phrase, or `number-title` | `01-vision-scope.md`, `简易需求文档.md` |
| Interface / protocol (JSON, SQL, TSL) | English kebab-case, reflecting source system and purpose | `riot-swagger-device.json`, `sql-send-to-oven.sql` |
| Legacy scripts grouped by business scenario | `action-object`, hyphen-separated | `get-eqp-list-by-material.sql` |
| Images / screenshots | Content + date (if needed), hyphen-separated | `agv-cabin-layout-2026-07-07.png` |
| Meeting notes / review records | Date first + topic | `2026-07-07-需求评审纪要.md` |
| Descriptive README | Fixed uppercase `README.md` | `README.md` |

---

## 7. Folder Hierarchy Naming

- Top-level folders are organized by business module, using short lowercase English words: `mes`, `rcs`, `requirements` (replacing the existing `requirement documents`, which contains a space).
- Subfolders are organized by function or scenario. Chinese or English kebab-case is acceptable, but sibling directories should use a consistent language style.
- Avoid nesting deeper than 4–5 levels. Deeper hierarchies make paths longer and harder to maintain.

---

## 8. Cheat Sheet

| Rule | Requirement |
| --- | --- |
| Separator | Hyphen `-` only; no spaces, underscores, or camelCase |
| Case | Lowercase only (except conventional names like `README.md`) |
| Forbidden characters | `\ / : * ? " < > \|` and control characters |
| Forbidden endings | No trailing space or `.` |
| Forbidden names | `CON PRN AUX NUL COM0-9 LPT0-9` (case-insensitive) |
| Date format | `YYYY-MM-DD`, placed at the start of the file name |
| Version number | Sortable, comparable format such as `v1.0`, `v1.2` |
| Length | Single name ≤ 30 characters recommended; full path ≤ 120 characters recommended |
| Mixed languages | Separate Chinese/English and Chinese/digits with hyphens, no spaces |
| Semantics | Name should describe what the content is; avoid meaningless labels like "new folder" or "final version" |

---

## 9. Existing Names → Suggested Names (Reference Examples)

These examples illustrate how the rules apply in practice. **They do not require immediate renaming of existing files:**

| Existing Name | Issue | Suggested Name |
| --- | --- | --- |
| `requirement documents/` | Contains a space | `requirements/` |
| `IT提供的SQL语句/` | Chinese punctuation; can be kept but should be unified | `it-sql-scripts/` (or keep Chinese without punctuation) |
| `根据sublot进行核验/` | Mixed Chinese/English without separator | `sublot-verification/` or `按sublot核验/` |
| `UpZP_Finish_TAG_BySublots.sql` | Mixed camelCase and underscores; inconsistent case | `up-zp-finish-tag-by-sublots.sql` |
| `旧程序sql访问代码/` | Chinese and English concatenated without separator | `legacy-sql-scripts/` or `旧程序-sql访问代码/` |

---

If naming conventions for source code files (e.g. future Python or frontend code) are needed, add a separate "Code Naming Conventions" section based on this document.
