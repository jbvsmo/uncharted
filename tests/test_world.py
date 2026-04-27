from uncharted.game.state import GameState
from uncharted.world.generator import generate


def test_generation_is_deterministic():
    a = generate(seed=42, width=20, height=10)
    b = generate(seed=42, width=20, height=10)
    assert a.tiles == b.tiles
    assert a.spawn == b.spawn


def test_different_seeds_differ():
    a = generate(seed=1, width=20, height=10)
    b = generate(seed=2, width=20, height=10)
    assert a.tiles != b.tiles


def test_movement_and_reveal():
    w = generate(seed=7, width=10, height=10)
    gs = GameState.new(w)
    start = (gs.px, gs.py)
    assert (gs.px, gs.py) in gs.revealed
    assert gs.try_move(1, 0) is True
    assert (gs.px, gs.py) == (start[0] + 1, start[1])
    assert gs.turn == 1


def test_movement_bounds():
    w = generate(seed=7, width=4, height=4)
    gs = GameState.new(w)
    # walk off the east edge
    moved = 0
    for _ in range(10):
        if gs.try_move(1, 0):
            moved += 1
    assert gs.px == w.width - 1
    assert moved < 10
