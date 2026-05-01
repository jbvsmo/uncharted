import json
from pathlib import Path

from uncharted.game.save import from_dict, load, save, to_dict
from uncharted.game.state import GameState
from uncharted.world.features import CATALOGUE, by_id
from uncharted.world.generator import generate


def test_catalogue_is_significantly_larger():
    assert len(CATALOGUE) >= 80


def test_feature_density_stays_stable():
    for width, height in ((10, 6), (24, 12), (32, 16), (48, 20)):
        w = generate(seed=123, width=width, height=height)
        assert len(w.features) == max(8, (width * height) // 40)


def test_features_are_placed_deterministically():
    a = generate(seed=123, width=24, height=12)
    b = generate(seed=123, width=24, height=12)
    assert a.features == b.features
    assert len(a.features) > 0


def test_features_match_catalogue():
    w = generate(seed=99, width=24, height=12)
    ids = {f.id for f in CATALOGUE}
    for fi in w.features:
        assert fi.feature_id in ids


def test_codex_records_when_player_steps_on_feature():
    w = generate(seed=5, width=24, height=12)
    fi = w.features[0]
    gs = GameState(world=w, px=fi.x, py=fi.y)
    gs.reveal_around(gs.px, gs.py)
    gs._touch_feature_here()
    assert fi.feature_id in gs.codex
    assert (fi.x, fi.y) in gs.discovered_tiles
    assert gs.last_feature_id == fi.feature_id
    assert by_id(fi.feature_id) is not None


def test_revealed_but_unvisited_feature_renders_as_biome():
    """A feature tile that's only fog-revealed (not stepped on) must show the
    biome glyph, never the feature glyph — even if the same feature_id is
    already in the codex from another tile."""
    from uncharted.ui.render import _render_map
    w = generate(seed=5, width=24, height=12)
    # find an interior feature tile
    fi = next(f for f in w.features
              if 1 <= f.x < w.width - 1 and 1 <= f.y < w.height - 1)
    # stand adjacent so the feature tile is revealed but not stepped on
    gs = GameState(world=w, px=fi.x + 1, py=fi.y)
    gs.reveal_around(gs.px, gs.py)
    gs._touch_feature_here()
    # pretend we discovered the same feature_id elsewhere
    gs.codex.add(fi.feature_id)
    assert (fi.x, fi.y) in gs.revealed
    assert (fi.x, fi.y) not in gs.discovered_tiles
    feat = by_id(fi.feature_id)
    biome_glyph = w.biome_at(fi.x, fi.y).info.glyph
    rendered = _render_map(gs).plain.splitlines()
    assert rendered[fi.y][fi.x] == biome_glyph
    assert rendered[fi.y][fi.x] != feat.glyph


def test_save_and_load_roundtrip(tmp_path: Path):
    w = generate(seed=2024, width=20, height=10)
    gs = GameState.new(w)
    gs.try_move(1, 0)
    gs.try_move(0, 1)
    p = tmp_path / "save.json"
    save(gs, p)
    raw = json.loads(p.read_text())
    assert raw["seed"] == 2024
    gs2 = load(p)
    assert gs2.world.seed == gs.world.seed
    assert (gs2.px, gs2.py) == (gs.px, gs.py)
    assert gs2.revealed == gs.revealed
    assert gs2.codex == gs.codex
    assert gs2.turn == gs.turn


def test_to_dict_is_json_serialisable():
    w = generate(seed=1, width=10, height=6)
    gs = GameState.new(w)
    json.dumps(to_dict(gs))


def test_unique_features_appear_at_most_once():
    from uncharted.world.features import Rarity
    unique_ids = {f.id for f in CATALOGUE if f.rarity is Rarity.UNIQUE}
    for seed in range(1, 30):
        w = generate(seed=seed, width=40, height=20)
        seen: dict[str, int] = {}
        for fi in w.features:
            seen[fi.feature_id] = seen.get(fi.feature_id, 0) + 1
        for uid in unique_ids:
            assert seen.get(uid, 0) <= 1, f"{uid} placed multiple times on seed {seed}"


def test_from_dict_rejects_wrong_version():
    import pytest
    with pytest.raises(ValueError):
        from_dict({"version": 999})
