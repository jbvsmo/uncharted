"""Procedural world generation.

The world is built in layers:

1. A deterministic elevation map creates landmasses, seas, and a few islands.
2. Moisture / temperature / roughness fields classify natural biomes.
3. Rare overlays add sparse specialised biomes such as volcanoes, fjords,
   ruins, farmland, rural settlements, and cities.
4. Features are placed afterwards, keeping per-world feature count stable.
"""
from __future__ import annotations

import random
from collections import deque
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


def _value_field(seed: int, width: int, height: int, count: int,
                 low: int = 0, high: int = 100) -> tuple[tuple[int, ...], ...]:
    """Voronoi-style value field: each tile takes the value of its nearest seed."""
    rng = random.Random(seed)
    points: list[tuple[int, int, int]] = []
    for _ in range(max(1, count)):
        points.append((
            rng.randrange(width),
            rng.randrange(height),
            rng.randint(low, high),
        ))

    rows: list[tuple[int, ...]] = []
    for y in range(height):
        row: list[int] = []
        for x in range(width):
            best_d = 1 << 60
            best_v = low
            for px, py, v in points:
                d = (px - x) ** 2 + (py - y) ** 2
                if d < best_d:
                    best_d = d
                    best_v = v
            row.append(best_v)
        rows.append(tuple(row))
    return tuple(rows)


def _neighbors(x: int, y: int, width: int, height: int):
    if x > 0:
        yield x - 1, y
    if x < width - 1:
        yield x + 1, y
    if y > 0:
        yield x, y - 1
    if y < height - 1:
        yield x, y + 1


def _distance_field(width: int, height: int,
                    sources: list[tuple[int, int]]) -> list[list[int]]:
    dist = [[-1 for _ in range(width)] for _ in range(height)]
    q: deque[tuple[int, int]] = deque()
    for x, y in sources:
        dist[y][x] = 0
        q.append((x, y))
    while q:
        x, y = q.popleft()
        for nx, ny in _neighbors(x, y, width, height):
            if dist[ny][nx] != -1:
                continue
            dist[ny][nx] = dist[y][x] + 1
            q.append((nx, ny))
    return dist


def _component_sizes(mask: list[list[bool]]) -> list[list[int]]:
    height = len(mask)
    width = len(mask[0]) if height else 0
    seen = [[False for _ in range(width)] for _ in range(height)]
    sizes = [[0 for _ in range(width)] for _ in range(height)]

    for y in range(height):
        for x in range(width):
            if seen[y][x] or not mask[y][x]:
                continue
            q = deque([(x, y)])
            seen[y][x] = True
            cells: list[tuple[int, int]] = []
            while q:
                cx, cy = q.popleft()
                cells.append((cx, cy))
                for nx, ny in _neighbors(cx, cy, width, height):
                    if seen[ny][nx] or not mask[ny][nx]:
                        continue
                    seen[ny][nx] = True
                    q.append((nx, ny))
            size = len(cells)
            for cx, cy in cells:
                sizes[cy][cx] = size
    return sizes


def _pick_spaced_sites(rng: random.Random, candidates: list[tuple[int, int]],
                       count: int, min_dist: int) -> list[tuple[int, int]]:
    if count <= 0 or not candidates:
        return []
    rng.shuffle(candidates)
    chosen: list[tuple[int, int]] = []
    min_sq = min_dist * min_dist
    for x, y in candidates:
        if all((x - sx) ** 2 + (y - sy) ** 2 >= min_sq for sx, sy in chosen):
            chosen.append((x, y))
            if len(chosen) >= count:
                break
    return chosen


def _make_land_mask(seed: int, width: int, height: int) -> list[list[bool]]:
    area = width * height
    elevation = _value_field(seed ^ 0xA11E, width, height,
                             max(6, area // 90), 28, 92)
    jitter = _value_field(seed ^ 0xB44F, width, height,
                          max(8, area // 70), 0, 100)

    land = [[False for _ in range(width)] for _ in range(height)]
    centre_span = max(1, min(width, height) // 2)
    for y in range(height):
        for x in range(width):
            edge = min(x, y, width - 1 - x, height - 1 - y)
            continentality = int(24 * (edge / centre_span))
            noise = (jitter[y][x] - 50) // 4
            score = elevation[y][x] + continentality + noise
            land[y][x] = score >= 68

    # sprinkle a few tiny islands, biased toward the outer bands of the map
    rng = random.Random(seed ^ 0x1A11)
    island_count = max(1, min(4, area // 240 + 1))
    for _ in range(island_count):
        side = rng.choice(("n", "s", "e", "w"))
        if side == "n":
            cx, cy = rng.randrange(width), rng.randrange(max(1, height // 4))
        elif side == "s":
            cx, cy = rng.randrange(width), rng.randrange(max(1, 3 * height // 4), height)
        elif side == "w":
            cx, cy = rng.randrange(max(1, width // 4)), rng.randrange(height)
        else:
            cx, cy = rng.randrange(max(1, 3 * width // 4), width), rng.randrange(height)
        if land[cy][cx]:
            continue
        rx = rng.randint(1, max(1, width // 12))
        ry = rng.randint(1, max(1, height // 10))
        for y in range(max(0, cy - ry - 1), min(height, cy + ry + 2)):
            for x in range(max(0, cx - rx - 1), min(width, cx + rx + 2)):
                dx = (x - cx) / max(1, rx)
                dy = (y - cy) / max(1, ry)
                if dx * dx + dy * dy <= 1.15:
                    land[y][x] = True

    return land


def generate(seed: int, width: int = 32, height: int = 16) -> World:
    area = width * height

    land = _make_land_mask(seed, width, height)
    moisture = _value_field(seed ^ 0xC31F, width, height,
                            max(6, area // 85), 0, 100)
    roughness = _value_field(seed ^ 0xD05A, width, height,
                             max(6, area // 95), 0, 100)
    warmth = _value_field(seed ^ 0xE771, width, height,
                          max(6, area // 90), 15, 100)
    oddity = _value_field(seed ^ 0xF90D, width, height,
                          max(6, area // 90), 0, 100)

    land_tiles = [(x, y) for y in range(height) for x in range(width) if land[y][x]]
    water_tiles = [(x, y) for y in range(height) for x in range(width) if not land[y][x]]
    if not land_tiles:
        # pathological edge case on tiny maps: force the centre to exist as land
        cx, cy = width // 2, height // 2
        land[cy][cx] = True
        land_tiles = [(cx, cy)]
        water_tiles = [(x, y) for y in range(height) for x in range(width)
                       if not land[y][x]]

    dist_to_land = _distance_field(width, height, land_tiles)
    dist_to_water = _distance_field(width, height, water_tiles or land_tiles)
    land_component_size = _component_sizes(land)
    island_limit = max(4, area // 80)

    natural: list[list[Biome]] = [[Biome.PLAINS for _ in range(width)]
                                  for _ in range(height)]

    for y in range(height):
        for x in range(width):
            m = moisture[y][x]
            r = roughness[y][x]
            lat_bias = int((y / max(1, height - 1)) * 24) - 12
            t = max(0, min(100, warmth[y][x] + lat_bias - r // 8))

            if not land[y][x]:
                north_land = y > 0 and land[y - 1][x]
                south_land = y < height - 1 and land[y + 1][x]
                west_land = x > 0 and land[y][x - 1]
                east_land = x < width - 1 and land[y][x + 1]
                narrow = (north_land and south_land) or (west_land and east_land)
                if (dist_to_land[y][x] <= 1 and narrow and t < 44 and r > 60
                        and oddity[y][x] > 58):
                    natural[y][x] = Biome.FJORD
                elif dist_to_land[y][x] >= 6:
                    natural[y][x] = Biome.DEEP_SEA
                elif dist_to_land[y][x] >= 3:
                    natural[y][x] = Biome.OCEAN
                else:
                    natural[y][x] = Biome.SEA
                continue

            coast = dist_to_water[y][x] == 1
            island = land_component_size[y][x] <= island_limit

            if island:
                natural[y][x] = Biome.BEACH if coast and land_component_size[y][x] > 2 else Biome.ISLAND
                continue
            if coast and 35 <= t <= 80 and r < 42 and m < 75:
                natural[y][x] = Biome.BEACH
                continue
            if coast and m > 72 and r < 40 and t > 30:
                natural[y][x] = Biome.MARSH
                continue

            if t < 18:
                natural[y][x] = Biome.ICEFIELD if (m > 40 or r < 45) else Biome.TUNDRA
            elif t < 35:
                natural[y][x] = Biome.TAIGA if m > 52 else Biome.TUNDRA
            elif t > 80:
                if m < 28:
                    natural[y][x] = Biome.DESERT
                elif m < 60:
                    natural[y][x] = Biome.SAVANNAH
                else:
                    natural[y][x] = Biome.RAINFOREST
            elif t > 62:
                if m < 20 and r > 50:
                    natural[y][x] = Biome.BADLANDS
                elif m < 35:
                    natural[y][x] = Biome.SAVANNAH
                elif m > 76:
                    natural[y][x] = Biome.RAINFOREST
                elif r > 72:
                    natural[y][x] = Biome.HILLS
                else:
                    natural[y][x] = Biome.FOREST
            else:
                if m > 78 and r < 36:
                    natural[y][x] = Biome.MARSH
                elif m < 22 and r > 55:
                    natural[y][x] = Biome.BADLANDS
                elif r > 75:
                    natural[y][x] = Biome.HILLS
                elif m < 35:
                    natural[y][x] = Biome.PLAINS
                elif m > 65:
                    natural[y][x] = Biome.FOREST
                else:
                    natural[y][x] = Biome.PLAINS if r < 40 else Biome.FOREST

    tiles = [row[:] for row in natural]

    # ----- cohesion pass -----------------------------------------------
    # The combination of moisture/temperature/roughness fields can leave
    # isolated single-tile pockets of an unrelated biome inside an otherwise
    # uniform region. Sweep twice and assimilate any land tile whose climate
    # disagrees with at least three of its four cardinal neighbours, so
    # regions read as coherent zones rather than confetti. Beach/island are
    # exempt because they exist precisely as transitional fringes.
    _SMOOTH_SKIP = {Biome.BEACH, Biome.ISLAND}
    for _ in range(2):
        nxt = [row[:] for row in tiles]
        for y in range(height):
            for x in range(width):
                if not land[y][x] or tiles[y][x] in _SMOOTH_SKIP:
                    continue
                tally: dict[Biome, int] = {}
                for nx, ny in _neighbors(x, y, width, height):
                    if not land[ny][nx]:
                        continue
                    nb = tiles[ny][nx]
                    if nb in _SMOOTH_SKIP:
                        continue
                    tally[nb] = tally.get(nb, 0) + 1
                if not tally:
                    continue
                top, count = max(tally.items(), key=lambda kv: kv[1])
                if count >= 3 and top is not tiles[y][x]:
                    nxt[y][x] = top
        tiles = nxt
        natural = [row[:] for row in tiles]

    def can_overlay(x: int, y: int) -> bool:
        b = tiles[y][x]
        return (not b.is_water and b not in {
            Biome.BEACH,
            Biome.ISLAND,
            Biome.FJORD,
            Biome.VOLCANO,
            Biome.RUINS,
        })

    # Volcanoes: very sparse, only on hot rough interiors.
    volcano_candidates = [
        (x, y)
        for y in range(height)
        for x in range(width)
        if natural[y][x] in {Biome.HILLS, Biome.BADLANDS, Biome.DESERT, Biome.SAVANNAH}
        and roughness[y][x] > 72
        and warmth[y][x] > 62
        and dist_to_water[y][x] > 1
    ]
    volcano_rng = random.Random(seed ^ 0x51C0)
    volcano_count = 0
    if volcano_candidates and area >= 140 and volcano_rng.random() < 0.7:
        volcano_count = 1
        if area >= 700 and volcano_rng.random() < 0.35:
            volcano_count += 1
    for vx, vy in _pick_spaced_sites(volcano_rng, volcano_candidates, volcano_count, 7):
        tiles[vy][vx] = Biome.VOLCANO
        for nx, ny in _neighbors(vx, vy, width, height):
            if can_overlay(nx, ny) and natural[ny][nx] in {Biome.PLAINS, Biome.FOREST, Biome.HILLS, Biome.SAVANNAH}:
                tiles[ny][nx] = Biome.BADLANDS

    # Ruins: sparse scars of older habitation.
    ruin_candidates = [
        (x, y)
        for y in range(height)
        for x in range(width)
        if natural[y][x] in {
            Biome.PLAINS,
            Biome.FOREST,
            Biome.HILLS,
            Biome.DESERT,
            Biome.TUNDRA,
            Biome.TAIGA,
            Biome.SAVANNAH,
        }
        and dist_to_water[y][x] <= 6
        and tiles[y][x] is not Biome.VOLCANO
    ]
    ruin_rng = random.Random(seed ^ 0x5227)
    ruin_count = 0
    if ruin_candidates and area >= 160 and ruin_rng.random() < 0.55:
        ruin_count = 1
        if area >= 800 and ruin_rng.random() < 0.25:
            ruin_count += 1
    for rx, ry in _pick_spaced_sites(ruin_rng, ruin_candidates, ruin_count, 6):
        tiles[ry][rx] = Biome.RUINS
        for nx, ny in _neighbors(rx, ry, width, height):
            if can_overlay(nx, ny) and oddity[ny][nx] > 52:
                tiles[ny][nx] = Biome.RUINS

    # Settlements: rare urban centres with rural / farmland halos.
    settlement_candidates = [
        (x, y)
        for y in range(height)
        for x in range(width)
        if natural[y][x] in {Biome.PLAINS, Biome.FOREST, Biome.TAIGA, Biome.SAVANNAH}
        and dist_to_water[y][x] <= 5
        and land_component_size[y][x] > island_limit
        and tiles[y][x] not in {Biome.RUINS, Biome.VOLCANO}
    ]
    settlement_rng = random.Random(seed ^ 0x5E77)
    settlement_count = 0
    if settlement_candidates and area >= 160 and settlement_rng.random() < 0.55:
        settlement_count = 1
        if area >= 700 and settlement_rng.random() < 0.2:
            settlement_count += 1
    for sx, sy in _pick_spaced_sites(settlement_rng, settlement_candidates, settlement_count, 7):
        if not can_overlay(sx, sy):
            continue
        tiles[sy][sx] = Biome.CITY
        for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            nx, ny = sx + dx, sy + dy
            if 0 <= nx < width and 0 <= ny < height and can_overlay(nx, ny):
                if natural[ny][nx] in {Biome.PLAINS, Biome.FOREST, Biome.TAIGA, Biome.SAVANNAH}:
                    tiles[ny][nx] = Biome.RURAL
        for dy in range(-2, 3):
            for dx in range(-2, 3):
                if abs(dx) + abs(dy) != 2:
                    continue
                nx, ny = sx + dx, sy + dy
                if 0 <= nx < width and 0 <= ny < height and can_overlay(nx, ny):
                    if natural[ny][nx] in {Biome.PLAINS, Biome.FOREST, Biome.SAVANNAH}:
                        tiles[ny][nx] = Biome.FARMLAND

    tiles_t = tuple(tuple(row) for row in tiles)

    # Spawn near the middle, but prefer non-water, non-volcano, non-city tiles.
    cx, cy = width // 2, height // 2
    preferred = [
        (x, y)
        for y in range(height)
        for x in range(width)
        if not tiles_t[y][x].is_water and tiles_t[y][x] not in {Biome.VOLCANO, Biome.CITY}
    ]
    fallback = [
        (x, y)
        for y in range(height)
        for x in range(width)
        if not tiles_t[y][x].is_water
    ]
    pool = preferred or fallback or [(cx, cy)]
    spawn = min(
        pool,
        key=lambda p: (
            (p[0] - cx) ** 2 + (p[1] - cy) ** 2,
            tiles_t[p[1]][p[0]].is_rare,
            p[1],
            p[0],
        ),
    )

    features = place(seed=seed, width=width, height=height, tiles=tiles_t)
    return World(
        width=width,
        height=height,
        seed=seed,
        tiles=tiles_t,
        spawn=spawn,
        features=features,
    )
