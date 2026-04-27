"""Discoverable features placed on the map at world-gen time.

Each Feature is a static definition (id, biome affinity, rarity, flavor).
A FeatureInstance is a placement of one feature at a specific tile.
"""
from __future__ import annotations

import random
from dataclasses import dataclass
from enum import Enum

from .biomes import Biome


class Rarity(Enum):
    COMMON = ("common", "white", 6)
    UNCOMMON = ("uncommon", "cyan", 3)
    RARE = ("rare", "magenta", 1)
    UNIQUE = ("unique", "bright_yellow", 1)  # placed at most once per world

    @property
    def label(self) -> str:
        return self.value[0]

    @property
    def color(self) -> str:
        return self.value[1]

    @property
    def weight(self) -> int:
        return self.value[2]


@dataclass(frozen=True)
class Feature:
    id: str
    name: str
    glyph: str
    color: str
    biome: Biome | None  # None = may appear in any biome
    rarity: Rarity
    short: str  # one-line tease shown when you arrive on the tile
    flavor: str  # longer description shown by `examine`


# ---- the catalogue -----------------------------------------------------------
# About 30 discoveries spread across biomes, plus a handful of biome-agnostic
# entries and two unique set-pieces.

CATALOGUE: tuple[Feature, ...] = (
    # FOREST
    Feature("hollow_tree", "the hollow tree", "Y", "green", Biome.FOREST, Rarity.COMMON,
            "A tree split open from the inside, its hollow lined with soft white fur.",
            "The fur is warm and breathes very slowly. You decide not to reach inside."),
    Feature("listening_grove", "the listening grove", "ψ", "green", Biome.FOREST, Rarity.UNCOMMON,
            "A clearing where the trees lean toward a single empty spot in the centre.",
            "Standing at the centre, you hear, faintly, your own thoughts spoken back to you "
            "in a voice that is almost yours."),
    Feature("paper_birch", "the paper-skin birch", "Ϋ", "bright_white", Biome.FOREST, Rarity.COMMON,
            "A birch whose bark peels away in long, written sheets.",
            "The script is in no language you know, but the handwriting is unmistakably your own."),
    Feature("moth_shrine", "the moth shrine", "✦", "magenta", Biome.FOREST, Rarity.RARE,
            "A cairn of antlers blanketed in pale, motionless moths.",
            "The moths do not stir when you approach. Each carries a single human eyelash on its back."),

    # DESERT
    Feature("salt_pillar", "the salt pillar", "‖", "yellow", Biome.DESERT, Rarity.COMMON,
            "A column of salt taller than a person, the wind has never touched.",
            "Up close, the pillar is smooth as glass and faintly warm. It hums on the same note as your bones."),
    Feature("buried_compass", "the buried compass", "✜", "yellow", Biome.DESERT, Rarity.UNCOMMON,
            "Half-uncovered by the wind: a brass compass, its needle spinning lazily.",
            "The needle ignores north. It points, slowly and definitely, at you, no matter where you stand."),
    Feature("glass_field", "the glass field", "♦", "cyan", Biome.DESERT, Rarity.UNCOMMON,
            "A patch of desert fused into pale green glass, the shape of a wide hand.",
            "Looking down through the glass, you see, very far below, something that looks back up."),
    Feature("salt_chorus", "the salt chorus", "♪", "bright_yellow", Biome.DESERT, Rarity.RARE,
            "A ring of salt formations that whistle in slight disagreement.",
            "Stand at the centre and the whistles align into a chord. The chord is the first note of a song you almost remember."),

    # TUNDRA
    Feature("frozen_lantern", "the frozen lantern", "¤", "bright_white", Biome.TUNDRA, Rarity.COMMON,
            "A lantern, still lit, encased in a teardrop of clear ice.",
            "The flame inside has no fuel and does not flicker. The ice is cold; the lantern is not."),
    Feature("breath_stones", "the breath-stones", "○", "bright_white", Biome.TUNDRA, Rarity.COMMON,
            "A ring of stones, each rimed in frost only on one side.",
            "The frost-free side of each stone is the side facing the next, as if they were exhaling at one another."),
    Feature("ice_fish", "the suspended fish", "≺", "cyan", Biome.TUNDRA, Rarity.UNCOMMON,
            "A silver fish frozen mid-leap, three feet above the ground, with no ice around it.",
            "It is not held up by anything. When you walk around it, it turns to keep facing you."),
    Feature("white_door", "the white door", "▯", "bright_white", Biome.TUNDRA, Rarity.RARE,
            "A door of pale wood, freestanding in the snow. No frame, no hinges visible.",
            "It opens. Behind it is more snow, identical, except for footprints leading away that are not yours."),

    # COAST
    Feature("tide_clock", "the tide-clock", "⊙", "cyan", Biome.COAST, Rarity.COMMON,
            "A barnacled brass dial, half-buried in wet sand, ticking against the tide.",
            "The dial has no numerals. Its hand is currently pointing at you, and slowly catching up."),
    Feature("singing_shells", "the singing shells", "⌒", "cyan", Biome.COAST, Rarity.COMMON,
            "A scatter of shells that hum faintly when the wind moves over them.",
            "Held to the ear, each shell plays a different name. None of them are yours; you remember them all."),
    Feature("drifting_boat", "the drifting boat", "⌣", "bright_white", Biome.COAST, Rarity.UNCOMMON,
            "A small wooden boat, beached, with no oars and a single dry footprint inside.",
            "The footprint is bare, child-sized, and faces the prow as though looking out to sea."),
    Feature("light_in_water", "the light in the water", "∗", "bright_cyan", Biome.COAST, Rarity.RARE,
            "Just offshore, a pale light hangs a few feet beneath the surface.",
            "It is the size and shape of a window. When you blink, it blinks back."),

    # RUINS
    Feature("counting_wall", "the counting wall", "▓", "magenta", Biome.RUINS, Rarity.COMMON,
            "A wall of fused stone marked with thousands of identical tally strokes.",
            "You count the marks and lose your place. Whatever total you arrive at, the wall has one more."),
    Feature("kneeling_statue", "the kneeling statue", "Ω", "magenta", Biome.RUINS, Rarity.UNCOMMON,
            "A statue of someone kneeling, hands cupped, eyes worn smooth by weather.",
            "The cupped hands hold a small puddle of clean water that has not evaporated in any sun."),
    Feature("locked_door", "the locked door", "‡", "magenta", Biome.RUINS, Rarity.UNCOMMON,
            "A doorway in a low ruin, sealed with a slab of unmarked metal warm to the touch.",
            "There is a keyhole at exactly your eye level. Looking through it, you see your own back."),
    Feature("library_pit", "the library pit", "▤", "magenta", Biome.RUINS, Rarity.RARE,
            "A circular pit lined with shelves, all empty, descending out of sight.",
            "Dropping a pebble in, you never hear it land. After a long while, something throws a pebble back."),

    # HILLS
    Feature("cairn", "the watchful cairn", "▲", "bright_black", Biome.HILLS, Rarity.COMMON,
            "A neat cairn of stones, balanced beyond any plausible patience.",
            "Each stone, lifted, is dry on the bottom even after rain. They have not been still as long as they look."),
    Feature("hill_eye", "the hill that opens", "◉", "bright_black", Biome.HILLS, Rarity.UNCOMMON,
            "A hill with a perfectly round, dry pond at its summit.",
            "When you turn your back to it, you feel observed. When you turn around, the pond is closed."),
    Feature("kite_string", "the kite string", "│", "bright_white", Biome.HILLS, Rarity.RARE,
            "A taut white string rises from a stake in the ground, vanishing into the sky.",
            "Following it with your eyes makes your neck hurt and your name harder to remember."),

    # ANY-BIOME
    Feature("sleeping_traveller", "the sleeping traveller", "&", "white", None, Rarity.UNCOMMON,
            "A figure curled on the ground in a long coat, breathing slowly.",
            "You cannot see their face. Their coat is identical to the one you are wearing, down to the mend on the cuff."),
    Feature("wrong_signpost", "the wrong signpost", "†", "white", None, Rarity.COMMON,
            "A weathered signpost with four arms, all pointing the same direction.",
            "Each arm names a different place. The direction they point is, very specifically, away from you."),
    Feature("paper_lantern", "the paper lantern", "¤", "yellow", None, Rarity.COMMON,
            "A paper lantern, lit, hanging from nothing at head height.",
            "The flame has no wick. The paper is warm and bears, in pencil, a date several years from now."),
    Feature("memory_stone", "the memory stone", "•", "bright_white", None, Rarity.UNCOMMON,
            "A smooth river stone resting where no river runs.",
            "Holding it, you remember a room you have never been in with great and unwelcome clarity."),
    Feature("ghost_track", "the wrong tracks", "≡", "grey50", None, Rarity.COMMON,
            "Footprints in the ground that match yours exactly, walking in a slow circle.",
            "There is one more set than there should be. They join your own a few paces back."),

    # UNIQUES (at most one per world)
    Feature("the_listener", "THE LISTENER", "Ξ", "bright_yellow", None, Rarity.UNIQUE,
            "A tall, thin shape in the middle distance that does not approach and does not leave.",
            "It has been here longer than the world. It is, you understand without being told, the reason "
            "the trees lean inward and the salt sings."),
    Feature("the_door_home", "THE DOOR HOME", "Π", "bright_yellow", None, Rarity.UNIQUE,
            "A doorframe of dark wood, standing alone, its threshold worn by long use.",
            "Through it you can see, very faintly, your own kitchen. The light is on. Someone is moving inside."),
)


@dataclass(frozen=True)
class FeatureInstance:
    feature_id: str
    x: int
    y: int


def by_id(fid: str) -> Feature:
    for f in CATALOGUE:
        if f.id == fid:
            return f
    raise KeyError(fid)


def place(seed: int, width: int, height: int, tiles: tuple[tuple[Biome, ...], ...]
          ) -> tuple[FeatureInstance, ...]:
    """Place ~width*height/40 feature instances. Deterministic per seed."""
    rng = random.Random(seed ^ 0xFEA7)
    n = max(8, (width * height) // 40)
    placed: list[FeatureInstance] = []
    used_tiles: set[tuple[int, int]] = set()
    used_uniques: set[str] = set()

    # build weighted pools: per biome + any-biome
    biome_pool: dict[Biome | None, list[Feature]] = {}
    for f in CATALOGUE:
        biome_pool.setdefault(f.biome, []).extend([f] * f.rarity.weight)

    attempts = 0
    while len(placed) < n and attempts < n * 20:
        attempts += 1
        x, y = rng.randrange(width), rng.randrange(height)
        if (x, y) in used_tiles:
            continue
        b = tiles[y][x]
        # 70% chance to draw from biome-specific, else any-biome
        pool: list[Feature] = []
        if rng.random() < 0.7:
            pool = biome_pool.get(b, [])
        if not pool:
            pool = biome_pool.get(None, [])
        if not pool:
            continue
        feat = rng.choice(pool)
        if feat.rarity is Rarity.UNIQUE:
            if feat.id in used_uniques:
                continue
            used_uniques.add(feat.id)
        used_tiles.add((x, y))
        placed.append(FeatureInstance(feat.id, x, y))

    return tuple(placed)
