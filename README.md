# Uncharted

A text-based discovery game for the terminal. You are an explorer dropped into
a procedurally generated world. Wander, reveal the map, and find strange
things to add to your Codex.

## Install & run

From a checkout:

```sh
uv run uncharted              # random seed
uv run uncharted --seed 42    # reproducible world (shareable)
uv run uncharted --width 48 --height 20
```

Try it straight from GitHub:

```sh
uvx --from git+https://github.com/jbvsmo/uncharted uncharted --seed 42
```

## How to play

The screen has three regions and refreshes in place:

```
┌─ view (map | meta: codex / legend / help) ───┐
│  ...                                         │
└──────────────────────────────────────────────┘
┌─ examine (only on map, when toggled with x) ─┐
│  ...                                         │
└──────────────────────────────────────────────┘
description of where you stand (and what's here)
[ MODE ]   hints, or :command-line buffer
```

Two modes, vim-style:

### NORMAL — single keys, no Enter
| key | action |
|---|---|
| `w` `a` `s` `d` / `↑` `←` `↓` `→` | move one tile |
| `m` | map view |
| `?` / `/` / `c` / `l` / `g` | meta view (codex + legend + help, side by side) |
| `x` | toggle examine panel below the map (status hint if no feature here) |
| `Esc` | enter COMMAND mode |

### COMMAND — vim-style, type then Enter
| command | what it does |
|---|---|
| `:q` / `:quit` | leave the world |
| `:save` | save the game |
| `:load` | reload the saved game |
| `:seed N` | restart in a new world with seed `N` |
| `:help` | help view |
| `Esc` | cancel back to NORMAL |

## Saves

Saved to `$XDG_DATA_HOME/uncharted/save.json` (default
`~/.local/share/uncharted/save.json`). The save only stores your seed,
position, revealed tiles, and codex — the world itself regenerates from the
seed, so saves are tiny and human-readable.

## Develop

```sh
uv sync
uv run pytest -q
```
