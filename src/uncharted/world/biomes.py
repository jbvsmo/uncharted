"""Biome definitions: glyph, color, and flavor text."""
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
    COAST = BiomeInfo(
        name="coast",
        glyph="≈",
        color="cyan",
        short="a slow, glassy shore",
        flavor=(
            "The water does not so much lap as consider. Smooth black pebbles "
            "rearrange themselves when you look away."
        ),
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

    @property
    def info(self) -> BiomeInfo:
        return self.value
