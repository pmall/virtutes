# Instructions for AI assistants

What the project is: `README.md`, then the documents it lists. This file says how to work here.

## At the start and the end of a session

1. Read `WIP.md`: it says where the work stands and what to do next.
2. Read the instruction file for the task at hand, and the documents it names. Nothing else is needed up front.
3. Before stopping: commit, then **rewrite** `WIP.md` (replace its content, do not append) and commit it.

## Instruction files (read only the one you need)

| Task | File |
|---|---|
| Convert one version to the unified text format | `instructions/convert_version.md` |
| Map every version of a new work | `instructions/map_editions.md` |
| Choose the versions of a work, download them, write their note | `instructions/select_and_download.md` |

## Where each kind of information goes (one place only)

| Information | Place |
|---|---|
| What the project is, a definition, a method, an open question | `docs/` (one topic, one file) |
| How an assistant must act | This file, or `instructions/` for a task |
| Where the work stands, what is next, hints for the next session | `WIP.md`, rewritten each session, kept under one page |
| What a script does and why | The comment at the top of the script |
| What was done and when | The git commit message |
| What a version's files are and why it was chosen | Its `metadata/note.txt` |

Never state the same thing in two places: link to it. Do not write dates, progress or history in `docs/` or `instructions/`. If a task changes a definition, change the document in the same commit.

## Rules

- **Never download anything without the user's explicit go-ahead.** Give the list, the total size and the expected duration first, then wait.
- **Never install anything without asking.** Python: standard library only.
- **`source/` is read-only.** Never modify, rename, unpack in place or delete what a library delivered.
- **`text/` is never edited by hand.** It is the output of the version's `convert/convert.py`.
- `data/Pilot_works_all_versions.csv` is not modified.
- Bulky files stay out of git (`.gitignore`); never force-add them.
- Commit on the current branch; do not create branches.
- **Checked or assumed.** Say which, every time. Never state an unverified fact as verified. A proposal is not a decision: mark it as a proposal.
- **When a point is not settled by the documents, ask the user**; do not decide silently.
- Documents are for researchers from other fields: plain language, short, not addressed to the user. Present works as one table, one row per version, counting versions as defined in `docs/Edition_mapping_method.md`, section 1.
- Deliverables are local files in this folder; nothing online unless asked.
- Libraries: at most one request every two seconds, generic client name, no personal or project details in requests.
- Paths contain spaces and accents: quote them.
