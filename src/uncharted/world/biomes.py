"""Biome definitions: glyph, color, flavor text, and coarse tags."""
from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


@dataclass(frozen=True)
class BiomeInfo:
    name: str
    glyph: str
    color: str
    short: str
    flavor: str
    water: bool = False
    rare: bool = False


class Biome(Enum):
    FOREST = BiomeInfo(
        name="forest",
        glyph="♣",
        color="green",
        short="a hush of pale-leaved trees",
        flavor=(
            "The trees here lean inward as if listening. Their leaves are the "
            "colour of old paper and they do not move when you do."
        ),
    )
    RAINFOREST = BiomeInfo(
        name="rainforest",
        glyph="Ψ",
        color="bright_green",
        short="a wet green vault of tangled leaves",
        flavor=(
            "Everything grows over everything else. Water falls in patient "
            "threads from vines thick as rope, and the air tastes of sap and "
            "forgotten altars."
        ),
        rare=True,
    )
    TAIGA = BiomeInfo(
        name="taiga",
        glyph="♤",
        color="green",
        short="a dark belt of resin-heavy pines",
        flavor=(
            "The conifers stand in rank upon rank, black at the trunk and silver "
            "at the needle tips. The wind moves through them like distant surf."
        ),
        rare=True,
    )
    PLAINS = BiomeInfo(
        name="plains",
        glyph="˷",
        color="bright_yellow",
        short="open plains under an extravagant sky",
        flavor=(
            "Long grasses lie in brushed bands, all of them leaning one way as "
            "though the day itself had passed over here in a hurry."
        ),
    )
    SAVANNAH = BiomeInfo(
        name="savannah",
        glyph="∻",
        color="yellow",
        short="amber grassland dotted with lonely trees",
        flavor=(
            "Heat shimmers low over the ground. Every tree appears placed rather "
            "than grown, as if the plain were once arranged for an audience."
        ),
        rare=True,
    )
    DESERT = BiomeInfo(
        name="desert",
        glyph="∴",
        color="yellow",
        short="cracked salt flats",
        flavor=(
            "Wind has scoured the ground into long, parallel grooves. The salt "
            "tastes faintly of iron when it touches your lips."
        ),
    )
    BADLANDS = BiomeInfo(
        name="badlands",
        glyph="∷",
        color="bright_red",
        short="a red maze of gullies and dry scars",
        flavor=(
            "Clay walls rise in blistered folds and collapse into one another. "
            "Even your echo sounds thirsty here."
        ),
        rare=True,
    )
    TUNDRA = BiomeInfo(
        name="tundra",
        glyph="∗",
        color="bright_white",
        short="a grey-blue tundra",
        flavor=(
            "The cold here is patient. Frost rimes every stone in concentric "
            "rings, like something has been breathing slowly for a long time."
        ),
    )
    ICEFIELD = BiomeInfo(
        name="icefield",
        glyph="✶",
        color="bright_cyan",
        short="a hard plain of blue ice",
        flavor=(
            "The ice is old enough to remember weight. Bubbles trapped inside it "
            "hang like punctuation from sentences the world no longer speaks."
        ),
        rare=True,
    )
    HILLS = BiomeInfo(
        name="hills",
        glyph="∩",
        color="bright_black",
        short="a low range of grey hills",
        flavor=(
            "The hills crest in even waves, as though the land itself were "
            "frozen mid-breath."
        ),
    )
    MARSH = BiomeInfo(
        name="marsh",
        glyph="≋",
        color="green",
        short="a reed-choked marsh of black water and peat",
        flavor=(
            "Every tuft of grass grows from something drowned. The mud keeps its "
            "own counsel and releases it in bubbles when you step too near."
        ),
        rare=True,
    )
    BEACH = BiomeInfo(
        name="beach",
        glyph="⋯",
        color="bright_yellow",
        short="a pale strand where the land gives up gently",
        flavor=(
            "The sand is fine as sifted bone. The tideline is marked not by foam "
            "but by a careful sorting of shells, glass, and impossible teeth."
        ),
        rare=True,
    )
    ISLAND = BiomeInfo(
        name="island",
        glyph="◌",
        color="bright_yellow",
        short="a small island holding itself apart from the world",
        flavor=(
            "This patch of land feels accidental, as though it surfaced only long "
            "enough to remember it was supposed to be elsewhere."
        ),
        rare=True,
    )
    FJORD = BiomeInfo(
        name="fjord",
        glyph="ǁ",
        color="cyan",
        short="a narrow fjord of black, deliberate water",
        flavor=(
            "Water has cut far into the land here, straight and deep beneath "
            "watching cliffs. Sound travels down it and seldom returns."
        ),
        water=True,
        rare=True,
    )
    FARMLAND = BiomeInfo(
        name="farmland",
        glyph="⌗",
        color="yellow",
        short="measured fields under old labour",
        flavor=(
            "Rows and furrows keep a discipline the farmers themselves may have "
            "forgotten. Even the crows cross above them in straight lines."
        ),
        rare=True,
    )
    RURAL = BiomeInfo(
        name="rural",
        glyph="⌂",
        color="white",
        short="scattered lanes and weather-beaten homesteads",
        flavor=(
            "Tracks between houses have been walked smooth by lives too ordinary "
            "to be remembered and too persistent to be erased."
        ),
        rare=True,
    )
    CITY = BiomeInfo(
        name="city",
        glyph="▦",
        color="bright_white",
        short="a dense knot of streets and stone",
        flavor=(
            "The city does not ruin so much as pause. Windows still hold shapes "
            "of habitation, and alleys seem confident someone will soon return."
        ),
        rare=True,
    )
    RUINS = BiomeInfo(
        name="ruins",
        glyph="▒",
        color="magenta",
        short="weathered ruins of something deliberate",
        flavor=(
            "Low walls of fused stone form patterns too regular to be natural. "
            "Whatever lived here measured its world in straight lines."
        ),
        rare=True,
    )
    VOLCANO = BiomeInfo(
        name="volcano",
        glyph="Λ",
        color="bright_red",
        short="a hot slope of ash and half-cooled fire",
        flavor=(
            "The ground has not decided whether it is stone or memory. Heat lifts "
            "from cracks in the rock in slow, resentful breaths."
        ),
        rare=True,
    )
    SEA = BiomeInfo(
        name="sea",
        glyph="≈",
        color="cyan",
        short="a green-blue sea within sight of land",
        flavor=(
            "The water rolls with a coastal patience, carrying drift, rumours, "
            "and the occasional thing that should have stayed sunk."
        ),
        water=True,
    )
    OCEAN = BiomeInfo(
        name="ocean",
        glyph="≊",
        color="bright_blue",
        short="the open ocean, broad and unsympathetic",
        flavor=(
            "Beyond the last familiar shallows the water darkens into thought. "
            "Waves rise and fall with the calm of something too large to hurry."
        ),
        water=True,
        rare=True,
    )
    DEEP_SEA = BiomeInfo(
        name="deep sea",
        glyph="≀",
        color="blue",
        short="trench-dark water where light loses interest",
        flavor=(
            "Depth gathers here like a second sky turned upside down. What moves "
            "below does so with the unearned confidence of the ancient."
        ),
        water=True,
        rare=True,
    )

    @property
    def info(self) -> BiomeInfo:
        return self.value

    @property
    def is_water(self) -> bool:
        return self.info.water

    @property
    def is_rare(self) -> bool:
        return self.info.rare
