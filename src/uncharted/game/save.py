"""Save/load. Worlds are reproducible from seed+dimensions, so we only need to
persist the player's situation: seed, size, position, revealed tiles, codex,
turn count.
"""
from __future__ import annotations

import json
import os
from pathlib import Path

from ..world.generator import generate
from .state import GameState

SAVE_VERSION = 1


def default_save_path() -> Path:
    base = os.environ.get("XDG_DATA_HOME") or str(Path.home() / ".local" / "share")
    p = Path(base) / "uncharted"
    p.mkdir(parents=True, exist_ok=True)
    return p / "save.json"


def to_dict(gs: GameState) -> dict:
    return {
        "version": SAVE_VERSION,
        "seed": gs.world.seed,
        "width": gs.world.width,
        "height": gs.world.height,
        "px": gs.px,
        "py": gs.py,
        "turn": gs.turn,
        "revealed": sorted([list(t) for t in gs.revealed]),
        "codex": sorted(gs.codex),
        "discovered_tiles": sorted([list(t) for t in gs.discovered_tiles]),
    }


def from_dict(d: dict) -> GameState:
    if d.get("version") != SAVE_VERSION:
        raise ValueError(f"unsupported save version: {d.get('version')!r}")
    world = generate(seed=int(d["seed"]), width=int(d["width"]), height=int(d["height"]))
    gs = GameState(
        world=world,
        px=int(d["px"]),
        py=int(d["py"]),
        revealed={(int(x), int(y)) for x, y in d.get("revealed", [])},
        codex=set(d.get("codex", [])),
        discovered_tiles={(int(x), int(y)) for x, y in d.get("discovered_tiles", [])},
        turn=int(d.get("turn", 0)),
    )
    gs._touch_feature_here()
    return gs


def save(gs: GameState, path: Path | None = None) -> Path:
    p = path or default_save_path()
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(to_dict(gs), indent=2))
    return p


def load(path: Path | None = None) -> GameState:
    p = path or default_save_path()
    return from_dict(json.loads(p.read_text()))
