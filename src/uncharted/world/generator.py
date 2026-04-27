"""Procedural world generation.

Strategy: scatter N biome seed points across the grid, each tile takes the
biome of its nearest seed (squared euclidean distance). Cheap, deterministic
per seed, and produces organic-looking regions. Then place features.
"""
from __future__ import annotations

import random
from dataclasses import dataclass

from .biomes import Biome
from .features import FeatureInstance, place


@dataclass(frozen=True)
class World:
    width: int
    height: int
    seed: int
    tiles: tuple[tuple[Biome, ...], ...]
    spawn: tuple[int, int]
    features: tuple[FeatureInstance, ...]

    def biome_at(self, x: int, y: int) -> Biome:
        return self.tiles[y][x]

    def in_bounds(self, x: int, y: int) -> bool:
        return 0 <= x < self.width and 0 <= y < self.height

    def feature_at(self, x: int, y: int) -> FeatureInstance | None:
        for fi in self.features:
            if fi.x == x and fi.y == y:
                return fi
        return None


def generate(seed: int, width: int = 32, height: int = 16) -> World:
    rng = random.Random(seed)
    biomes = list(Biome)
    n_seeds = max(8, (width * height) // 40)

    seed_points: list[tuple[int, int, Biome]] = []
    for _ in range(n_seeds):
        b = rng.choice(biomes)
        if b is Biome.COAST:
            edge = rng.choice(["n", "s", "e", "w"])
            if edge == "n":
                x, y = rng.randrange(width), rng.randrange(0, max(1, height // 4))
            elif edge == "s":
                x, y = rng.randrange(width), rng.randrange(3 * height // 4, height)
            elif edge == "w":
                x, y = rng.randrange(0, max(1, width // 4)), rng.randrange(height)
            else:
                x, y = rng.randrange(3 * width // 4, width), rng.randrange(height)
        else:
            x, y = rng.randrange(width), rng.randrange(height)
        seed_points.append((x, y, b))

    tiles: list[tuple[Biome, ...]] = []
    for y in range(height):
        row: list[Biome] = []
        for x in range(width):
            best: tuple[int, Biome] | None = None
            for sx, sy, sb in seed_points:
                d = (sx - x) ** 2 + (sy - y) ** 2
                if best is None or d < best[0]:
                    best = (d, sb)
            assert best is not None
            row.append(best[1])
        tiles.append(tuple(row))

    tiles_t = tuple(tiles)
    spawn = (width // 2, height // 2)
    features = place(seed=seed, width=width, height=height, tiles=tiles_t)
    return World(
        width=width,
        height=height,
        seed=seed,
        tiles=tiles_t,
        spawn=spawn,
        features=features,
    )
