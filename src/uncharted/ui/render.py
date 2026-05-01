"""Rich-based renderers. Composes the persistent screen:

  ┌── view (map or meta) ──┐
  │  ...                   │
  └────────────────────────┘
  (optional examine panel, only on map view when toggled on)
  description (one or two lines about your tile)
  status line (mode, hints, command-line buffer)
"""
from __future__ import annotations

from rich.columns import Columns
from rich.console import Group, RenderableType
from rich.panel import Panel
from rich.table import Table
from rich.text import Text

from ..game.state import GameState
from ..world.biomes import Biome
from ..world.features import CATALOGUE, by_id

# ---- view enum (string constants, simpler) ---------------------------------
VIEW_MAP = "map"
VIEW_META = "meta"

MODE_NORMAL = "normal"
MODE_COMMAND = "command"


# ---- map -------------------------------------------------------------------

def _render_map(gs: GameState) -> Text:
    w = gs.world
    out = Text()
    for y in range(w.height):
        for x in range(w.width):
            if x == gs.px and y == gs.py:
                out.append("@", style="bold white on grey15")
            elif (x, y) in gs.revealed:
                fi = w.feature_at(x, y)
                if fi is not None and (x, y) in gs.discovered_tiles:
                    f = by_id(fi.feature_id)
                    out.append(f.glyph, style=f"bold {f.color}")
                else:
                    b = w.biome_at(x, y).info
                    out.append(b.glyph, style=b.color)
            else:
                out.append("·", style="grey23")
        if y < w.height - 1:
            out.append("\n")
    return out


def _map_panel(gs: GameState) -> Panel:
    title = (
        f"map · seed={gs.world.seed} · pos=({gs.px},{gs.py}) · turn={gs.turn} "
        f"· codex={len(gs.codex)}/{gs.total_features}"
    )
    return Panel(_render_map(gs), title=title, border_style="grey39")


# ---- codex -----------------------------------------------------------------

def _codex_panel(gs: GameState) -> Panel:
    table = Table(border_style="grey39", show_header=True, expand=False)
    table.add_column("", justify="center", width=2)
    table.add_column("name")
    table.add_column("rarity")
    table.add_column("biome")
    present_ids = {fi.feature_id for fi in gs.world.features}
    for f in CATALOGUE:
        if f.id not in present_ids:
            continue
        if f.id in gs.codex:
            glyph = Text(f.glyph, style=f"bold {f.color}")
            name = Text(f.name, style=f.color)
        else:
            glyph = Text("?", style="grey39")
            name = Text("???", style="grey39")
        table.add_row(
            glyph,
            name,
            Text(f.rarity.label, style=f.rarity.color),
            f.biome.info.name if f.biome else "anywhere",
        )
    title = f"codex · {len(gs.codex)}/{gs.total_features} discovered (seed {gs.world.seed})"
    return Panel(table, title=title, border_style="grey39")


# ---- help ------------------------------------------------------------------

def _help_panel() -> Panel:
    body = Text.from_markup(
        "[bold]NORMAL mode[/bold]  (single keys, no return)\n"
        "  [cyan]w a s d[/cyan] / [cyan]↑ ← ↓ →[/cyan]   move\n"
        "  [cyan]m[/cyan]   map view\n"
        "  [cyan]?[/cyan] / [cyan]/[/cyan] / [cyan]c[/cyan] / [cyan]l[/cyan] / [cyan]g[/cyan]   meta view (codex + legend + help)\n"
        "  [cyan]x[/cyan]   toggle examine panel (below the map)\n"
        "  [cyan]Esc[/cyan]  →  COMMAND mode\n"
        "\n"
        "[bold]COMMAND mode[/bold]  (vim-style, type then Enter)\n"
        "  [cyan]:q[/cyan]  / [cyan]:quit[/cyan]      leave the world\n"
        "  [cyan]:save[/cyan]              save the game\n"
        "  [cyan]:load[/cyan]              reload the saved game\n"
        "  [cyan]:seed N[/cyan]            restart in a new world with seed N\n"
        "  [cyan]:help[/cyan]              this help\n"
        "  [cyan]Esc[/cyan]                cancel back to NORMAL"
    )
    return Panel(body, title="help", border_style="grey39")


# ---- legend ----------------------------------------------------------------

def _legend_panel(gs: GameState) -> Panel:
    revealed_biomes = {gs.world.biome_at(x, y) for x, y in gs.revealed}
    table = Table(border_style="grey39", show_header=True, expand=False)
    table.add_column("glyph", justify="center")
    table.add_column("biome")
    for b in Biome:
        if b not in revealed_biomes:
            continue
        i = b.info
        table.add_row(Text(i.glyph, style=i.color), i.name)
    table.add_row(Text("@", style="bold white"), "you")
    table.add_row(Text("·", style="grey23"), "unexplored")
    return Panel(table, title="legend", border_style="grey39")


# ---- meta (codex + legend + help side by side) -----------------------------

def _meta_panel(gs: GameState) -> Panel:
    cols = Columns(
        [_codex_panel(gs), _legend_panel(gs), _help_panel()],
        equal=False, expand=False, padding=(0, 1),
    )
    return Panel(cols, title="meta · codex · legend · help",
                 border_style="grey39")


# ---- examine ---------------------------------------------------------------

def _examine_panel(gs: GameState) -> Panel:
    f = by_id(gs.last_feature_id) if gs.last_feature_id else None
    assert f is not None
    body = Text()
    body.append(f.short + "\n\n", style=f.color)
    body.append(f.flavor, style="italic")
    return Panel(body, title=f"examine · {f.name} · {f.rarity.label}",
                 border_style=f.color)


# ---- description -----------------------------------------------------------

def _description(gs: GameState) -> RenderableType:
    b = gs.world.biome_at(gs.px, gs.py).info
    out = Text()
    out.append(f"You stand in {b.short}. ", style=f"bold {b.color}")
    out.append(b.flavor, style="italic")
    if gs.last_feature_id is not None:
        f = by_id(gs.last_feature_id)
        out.append("\n  ✺ Here: ", style="bold bright_yellow")
        out.append(f"{f.name} — ", style=f"bold {f.color}")
        out.append(f.short, style="italic")
        out.append("   (press x to examine)", style="grey50")
    return out


# ---- status / command-line -------------------------------------------------

def _status(mode: str, cmd_buf: str, message: str | None) -> RenderableType:
    if mode == MODE_COMMAND:
        line = Text()
        line.append(" COMMAND ", style="bold black on bright_yellow")
        line.append(" :", style="bright_yellow")
        line.append(cmd_buf, style="bright_white")
        line.append("_", style="blink bright_white")
        return line
    line = Text()
    line.append(" NORMAL  ", style="bold black on bright_green")
    line.append(
        "  wasd/arrows move · m map · ? meta · x examine · Esc :command",
        style="grey50",
    )
    if message:
        line.append("\n")
        line.append(message, style="bright_yellow")
    return line


# ---- top-level screen ------------------------------------------------------

def render_screen(gs: GameState, view: str, mode: str,
                  cmd_buf: str = "", message: str | None = None,
                  show_examine: bool = False) -> RenderableType:
    if view == VIEW_META:
        top: RenderableType = _meta_panel(gs)
    else:
        top = _map_panel(gs)
    parts: list[RenderableType] = [top]
    if view == VIEW_MAP and show_examine and gs.last_feature_id is not None:
        parts.append(_examine_panel(gs))
    parts.append(_description(gs))
    parts.append(_status(mode, cmd_buf, message))
    return Group(*parts)
