from uncharted.game.loop import (
    _LoopState, _exec_command, _handle_command, _handle_normal,
)
from uncharted.game.state import GameState
from uncharted.ui import render
from uncharted.world.generator import generate


def _state(seed=11):
    gs = GameState.new(generate(seed=seed, width=20, height=10))
    return _LoopState(gs)


def test_normal_mode_wasd_moves():
    s = _state()
    sx, sy = s.gs.px, s.gs.py
    _handle_normal(s, ("CHAR", "d"))
    assert (s.gs.px, s.gs.py) == (sx + 1, sy)
    _handle_normal(s, ("CHAR", "s"))
    assert (s.gs.px, s.gs.py) == (sx + 1, sy + 1)


def test_normal_mode_arrows_move():
    s = _state()
    sx, sy = s.gs.px, s.gs.py
    _handle_normal(s, ("ARROW", "UP"))
    assert (s.gs.px, s.gs.py) == (sx, sy - 1)


def test_view_switching_keys():
    s = _state()
    for ch in ("c", "?", "/", "l", "g"):
        s.view = render.VIEW_MAP
        _handle_normal(s, ("CHAR", ch))
        assert s.view == render.VIEW_META, f"{ch!r} should enter META"
    _handle_normal(s, ("CHAR", "m"))
    assert s.view == render.VIEW_MAP


def test_examine_toggle_with_feature():
    s = _state()
    # find a feature tile and put player on it
    fi = s.gs.world.features[0]
    s.gs.px, s.gs.py = fi.x, fi.y
    s.gs._touch_feature_here()
    assert s.show_examine is False
    _handle_normal(s, ("CHAR", "x"))
    assert s.show_examine is True
    _handle_normal(s, ("CHAR", "x"))
    assert s.show_examine is False


def test_examine_resets_on_move():
    s = _state()
    # find a feature that is not at the right edge so 'd' can move
    fi = next(f for f in s.gs.world.features if f.x < s.gs.world.width - 1)
    s.gs.px, s.gs.py = fi.x, fi.y
    s.gs._touch_feature_here()
    _handle_normal(s, ("CHAR", "x"))
    assert s.show_examine is True
    _handle_normal(s, ("CHAR", "d"))
    assert s.show_examine is False


def test_examine_no_feature_sets_status_message():
    s = _state()
    # ensure not on a feature tile
    feature_tiles = {(fi.x, fi.y) for fi in s.gs.world.features}
    if (s.gs.px, s.gs.py) in feature_tiles:
        # nudge off
        s.gs.last_feature_id = None
    s.gs.last_feature_id = None
    _handle_normal(s, ("CHAR", "x"))
    assert s.show_examine is False
    assert s.message and "nothing" in s.message.lower()


def test_esc_enters_command_mode():
    s = _state()
    _handle_normal(s, ("ESC", None))
    assert s.mode == render.MODE_COMMAND
    assert s.cmd_buf == ""


def test_command_typing_and_backspace():
    s = _state()
    s.mode = render.MODE_COMMAND
    _handle_command(s, ("CHAR", ":"))
    assert s.cmd_buf == ""
    for ch in "save":
        _handle_command(s, ("CHAR", ch))
    assert s.cmd_buf == "save"
    _handle_command(s, ("BACKSPACE", None))
    assert s.cmd_buf == "sav"


def test_command_esc_cancels():
    s = _state()
    s.mode = render.MODE_COMMAND
    s.cmd_buf = "qui"
    _handle_command(s, ("ESC", None))
    assert s.mode == render.MODE_NORMAL
    assert s.cmd_buf == ""


def test_command_quit():
    s = _state()
    _exec_command(s, "q")
    assert s.quit is True


def test_command_seed_replaces_world():
    s = _state(seed=11)
    _exec_command(s, "seed 99")
    assert s.gs.world.seed == 99


def test_command_help_codex_legend_all_open_meta():
    for c in ("help", "codex", "legend", "meta"):
        s = _state()
        _exec_command(s, c)
        assert s.view == render.VIEW_META, f":{c} should open META"
    s = _state()
    s.view = render.VIEW_META
    _exec_command(s, "map")
    assert s.view == render.VIEW_MAP


def test_unknown_command_sets_message():
    s = _state()
    _exec_command(s, "fhqwhgads")
    assert s.message and "unknown" in s.message
