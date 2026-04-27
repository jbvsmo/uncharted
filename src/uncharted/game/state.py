"""Mutable game state: player position, fog of war, codex of discoveries."""
from __future__ import annotations

from dataclasses import dataclass, field

from ..world.generator import World


@dataclass
class GameState:
    world: World
    px: int
    py: int
    revealed: set[tuple[int, int]] = field(default_factory=set)
    codex: set[str] = field(default_factory=set)  # discovered feature ids
    # specific feature instances (tiles) the player has stepped on
    discovered_tiles: set[tuple[int, int]] = field(default_factory=set)
    turn: int = 0
    # last discovery on the current tile, for `examine`
    last_feature_id: str | None = None

    @classmethod
    def new(cls, world: World) -> "GameState":
        gs = cls(world=world, px=world.spawn[0], py=world.spawn[1])
        gs.reveal_around(gs.px, gs.py)
        gs._touch_feature_here()
        return gs

    def reveal_around(self, x: int, y: int, radius: int = 1) -> None:
        for dy in range(-radius, radius + 1):
            for dx in range(-radius, radius + 1):
                nx, ny = x + dx, y + dy
                if self.world.in_bounds(nx, ny):
                    self.revealed.add((nx, ny))

    def try_move(self, dx: int, dy: int) -> bool:
        nx, ny = self.px + dx, self.py + dy
        if not self.world.in_bounds(nx, ny):
            return False
        self.px, self.py = nx, ny
        self.turn += 1
        self.reveal_around(nx, ny)
        self._touch_feature_here()
        return True

    def _touch_feature_here(self) -> None:
        fi = self.world.feature_at(self.px, self.py)
        if fi is None:
            self.last_feature_id = None
            return
        self.last_feature_id = fi.feature_id
        self.codex.add(fi.feature_id)
        self.discovered_tiles.add((self.px, self.py))

    @property
    def total_features(self) -> int:
        return len(self.world.features)
