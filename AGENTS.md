# AGENTS.md

Instructions for AI coding agents working in this repository.

## The project

**Uncharted** is a small text-based terminal discovery game written in Python.
The player wanders a procedurally generated world, reveals the map, and adds
discovered features to a Codex.

- Package name: `uncharted` (see `pyproject.toml`)
- Python is managed via `uv`
- Source layout:
  ```
  src/uncharted/
    __init__.py        # entry point + CLI args
    world/             # biomes, features, world generator
    game/              # state, REPL loop, save/load
    ui/                # rendering (Rich), raw key input
  tests/               # pytest suite
  ```
- Entry point: `uv run uncharted` (random seed) or `uv run uncharted --seed N`
- Tests: `uv run pytest -q` — they must pass before any change is considered done.

## Coding conventions

- Keep changes minimal and focused on what the user asked for.
- Match existing style (type hints, small focused helpers, comments only 
  where they explain *why*).
- No new dependencies without being asked.
- The game runs in a real terminal in raw mode. When touching `ui/keys.py`
  or `game/loop.py`, remember that `sys.stdin.read()` is buffered — read
  bytes from the fd directly with `os.read` for escape sequences.


## ⚠️ Commit & push policy — READ THIS

**You MUST NOT run `git commit` or `git push` unless the user has explicitly
asked you to, in that very message, for that very change.**

This rule applies to **every single commit and every single push**, with no
exceptions. In particular:

- Finishing a task is **not** permission to commit.
- Tests passing is **not** permission to commit.
- A previous request to "commit and push" does **not** carry over to the next
  change. Each commit and each push needs its own explicit request.
- "Save my work", "wrap it up", "we're done", "looks good", or similar are
  **not** requests to commit or push.
- Do not commit "just in case" or to "checkpoint" progress.
- Do not amend, rebase, force-push, tag, or otherwise rewrite history unless
  explicitly told to.
- Do not create branches or stash changes unless explicitly told to.

What you **may** do without being asked:
- `git status`, `git diff`, `git log`, `git show`, `git branch` (read-only)
- `git add` is allowed only as part of a commit the user just requested.

When in doubt: leave the working tree dirty and let the user decide. The user
will say something like "commit this" or "commit and push" when they want it.
Anything less explicit than that — don't.
