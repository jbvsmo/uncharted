"""Uncharted — a text-based discovery game."""
from __future__ import annotations

import argparse
import random

from rich.console import Console

from .game.loop import run
from .game.state import GameState
from .world.generator import generate


def main() -> None:
    parser = argparse.ArgumentParser(prog="uncharted", description=__doc__)
    parser.add_argument("--seed", type=int, default=None, help="world seed")
    parser.add_argument("--width", type=int, default=32)
    parser.add_argument("--height", type=int, default=16)
    args = parser.parse_args()

    seed = args.seed if args.seed is not None else random.randint(1, 2**31 - 1)
    world = generate(seed=seed, width=args.width, height=args.height)
    gs = GameState.new(world)
    run(Console(), gs)
