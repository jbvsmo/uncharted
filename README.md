# Uncharted

A text-based discovery game for the terminal. You are an explorer dropped into
a procedurally generated world. Wander, reveal the map, and find strange
things to add to your Codex.

> Pure text. No TUI, no full-screen takeover — just a prompt and printed
> output. Rich is used for color and tables only.

## Install & run

From a checkout:

```sh
uv run uncharted              # random seed
uv run uncharted --seed 42    # reproducible world (shareable)
uv run uncharted --width 48 --height 20
```

System-wide:

```sh
uv build
pipx install dist/uncharted-0.1.0-py3-none-any.whl
uncharted --seed 42
```

## How to play

The screen has three regions and refreshes in place:

```
┌─ view (map | meta: codex / legend / help) ─┐
│  ...                                        │
└─────────────────────────────────────────────┘
┌─ examine (only on map, when toggled with x) ┐
│  ...                                        │
└─────────────────────────────────────────────┘
description of where you stand (and what's here)
[ MODE ]   hints, or :command-line buffer
```

There are only two top-level views: **map** and **meta**. The meta view shows
codex, legend, and help all together side-by-side in a single panel — any of
`?`, `/`, `c`, `l`, `g` opens it. `m` returns to the map.

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

## Sharing worlds

Worlds are deterministic from `--seed`. If you find something good, share the
seed:

> "There's a singing salt chorus due east on `--seed 1729 --width 40 --height 18`."

## Status

- [x] **M1** — project scaffold (`uv`, package layout)
- [x] **M2** — procedural Voronoi map gen + ASCII render with fog
- [x] **M3** — REPL game loop, movement, look/map
- [x] **M4** — feature placement, discovery on entry, `examine` + `codex`
- [x] **M5** — Rich polish (panels, codex table, legend, color)
- [x] **M6** — save / load to XDG data dir, deterministic from seed
- [x] **M7** — content pass: ~30 discoveries across all 6 biomes incl. 2 uniques
- [x] **M8** — packaged as a wheel, installable via `pipx`

## Develop

```sh
uv sync
uv run pytest -q
```

## Layout

```
src/uncharted/
  __init__.py        # entry point + CLI args
  world/
    biomes.py        # 6 biomes: glyph, color, flavor
    features.py      # ~30 discoveries + placement
    generator.py     # Voronoi-style world gen
  game/
    state.py         # player, fog, codex
    loop.py          # REPL command dispatch
    save.py          # JSON persistence
  ui/
    render.py        # Rich-formatted output
tests/
```
