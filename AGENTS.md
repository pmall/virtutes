# Instructions for AI assistants

What the project is: `README.md`, then the documents it lists. This file says how to work here.

## Why this file is strict

Projects die when their context piles up: notes on notes, the same fact in three files, history mixed with rules. Here every piece of information has one place, and what is no longer needed is deleted, not kept "just in case".

## WIP.md

`WIP.md` is the list of what remains to do, in order; the first item is what to do next. Read it first. Every commit leaves it true: remove what is done, add what was discovered.

## Skills (one per task)

Each task has its procedure in `skills/<name>/SKILL.md`; the first lines of that file say when to use it. `.claude/skills/` holds one link per skill. Current skills: `convert-version`, `map-editions`, `select-and-download`.

A new skill is a new folder in `skills/` plus its link: `ln -s ../../skills/<name> .claude/skills/<name>`.

## Where each kind of information goes (one place only)

| Information | Place |
|---|---|
| What the project is, a definition, a method, an open question | `docs/` (one topic, one file) |
| How an assistant must act | This file for rules that always apply; a skill for the procedure of one task |
| What remains to do | `WIP.md` |
| What a script does and why | The comment at the top of the script |
| What was done and when | The git commit message |
| What a version's files are and why it was chosen | Its `metadata/note.txt` |

Never state the same thing in two places: link to it. Do not write dates, progress or history in `docs/` or `skills/`. If a task changes a definition, change the document in the same commit.

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
