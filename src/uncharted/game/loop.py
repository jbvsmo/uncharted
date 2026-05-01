"""Interactive game loop: raw single-key input, in-place redraw.

Two modes (vim-style):
  NORMAL   — single keys do things (wasd/arrows move, m/c/l/g/?/x switch view, ...)
  COMMAND  — type ":word" + Enter to execute. Esc cancels back to NORMAL.
"""
from __future__ import annotations

import sys

from rich.console import Console

from ..ui import render
from ..ui.keys import Key, raw_mode, read_key
from ..world.generator import generate
from . import save as save_mod
from .state import GameState

# direction vectors for movement keys
_MOVES = {
    "w": (0, -1), "UP":    (0, -1),
    "s": (0, 1),  "DOWN":  (0, 1),
    "a": (-1, 0), "LEFT":  (-1, 0),
    "d": (1, 0),  "RIGHT": (1, 0),
}


class _LoopState:
    def __init__(self, gs: GameState) -> None:
        self.gs = gs
        self.view = render.VIEW_MAP
        self.show_examine = False
        self.mode = render.MODE_NORMAL
        self.cmd_buf = ""
        self.message: str | None = None
        self.quit = False

    def msg(self, text: str | None) -> None:
        self.message = text


# ---------------------------------------------------------------------------
# helpers
# ---------------------------------------------------------------------------

def _toggle_examine(s: _LoopState) -> None:
    if s.gs.last_feature_id is None:
        s.show_examine = False
        s.msg("nothing here to examine.")
        return
    s.show_examine = not s.show_examine


# ---------------------------------------------------------------------------
# command dispatch
# ---------------------------------------------------------------------------

def _exec_command(s: _LoopState, line: str) -> None:
    line = line.strip()
    if not line:
        return
    parts = line.split()
    cmd, args = parts[0], parts[1:]
    if cmd in ("q", "quit", "exit"):
        s.quit = True
        return
    if cmd in ("h", "help", "meta", "codex", "c", "legend", "g"):
        s.view = render.VIEW_META
        s.msg(None)
        return
    if cmd == "save":
        try:
            p = save_mod.save(s.gs)
            s.msg(f"saved to {p}")
        except OSError as e:
            s.msg(f"save failed: {e}")
        return
    if cmd == "load":
        try:
            s.gs = save_mod.load()
            s.msg(f"loaded · seed {s.gs.world.seed} · turn {s.gs.turn}")
        except (OSError, ValueError) as e:
            s.msg(f"load failed: {e}")
        return
    if cmd == "seed":
        if not args:
            s.msg("usage: :seed N")
            return
        try:
            seed = int(args[0])
        except ValueError:
            s.msg("seed must be an integer")
            return
        w = generate(seed=seed, width=s.gs.world.width, height=s.gs.world.height)
        s.gs = GameState.new(w)
        s.view = render.VIEW_MAP
        s.show_examine = False
        s.msg(f"new world · seed {seed}")
        return
    if cmd in ("look", "l", "map", "m"):
        s.view = render.VIEW_MAP
        s.msg(None)
        return
    if cmd in ("examine", "x"):
        _toggle_examine(s)
        s.view = render.VIEW_MAP
        return
    s.msg(f"unknown command: :{cmd}")


# ---------------------------------------------------------------------------
# key handling
# ---------------------------------------------------------------------------

def _handle_normal(s: _LoopState, k: Key) -> None:
    kind, val = k
    s.msg(None)
    if kind == "ESC":
        s.mode = render.MODE_COMMAND
        s.cmd_buf = ""
        return
    if kind == "ARROW":
        assert val is not None
        _try_move(s, val)
        return
    if kind == "CHAR":
        ch = val
        assert ch is not None
        if ch in _MOVES:
            _try_move(s, ch)
            return
        if ch == "m":
            s.view = render.VIEW_MAP
            return
        if ch in ("?", "/", "c", "l", "g"):
            s.view = render.VIEW_META
            return
        if ch == "x":
            _toggle_examine(s)
            return
        # ignore other keys silently — no clutter


def _handle_command(s: _LoopState, k: Key) -> None:
    kind, val = k
    if kind == "ESC":
        s.mode = render.MODE_NORMAL
        s.cmd_buf = ""
        s.msg(None)
        return
    if kind == "ENTER":
        line = s.cmd_buf
        s.cmd_buf = ""
        s.mode = render.MODE_NORMAL
        _exec_command(s, line)
        return
    if kind == "BACKSPACE":
        s.cmd_buf = s.cmd_buf[:-1]
        return
    if kind == "CHAR":
        assert val is not None
        # don't echo a leading ':' — the renderer prints one
        if not s.cmd_buf and val == ":":
            return
        s.cmd_buf += val


def _try_move(s: _LoopState, key: str) -> None:
    dx, dy = _MOVES[key]
    if not s.gs.try_move(dx, dy):
        s.msg("the world ends here.")
        return
    # leaving a tile closes the examine panel; user must re-toggle on the next
    s.show_examine = False
    if s.gs.last_feature_id is not None:
        s.view = render.VIEW_MAP  # ensure map is visible on new discovery


def _screen(s: _LoopState):
    return render.render_screen(
        s.gs, s.view, s.mode, s.cmd_buf, s.message,
        show_examine=s.show_examine,
    )


# ---------------------------------------------------------------------------
# entrypoint
# ---------------------------------------------------------------------------

def run(console: Console, gs: GameState) -> None:
    s = _LoopState(gs)
    s.msg(f"world seed {gs.world.seed} · {gs.total_features} things to find · "
          "press ? for help")

    if not sys.stdin.isatty():
        # one-shot render: preserve any prior terminal output, no Live, no raw_mode
        console.print(_screen(s))
        return

    with raw_mode(sys.stdin.fileno()):
        # Per-line diff state. We will redraw only lines that changed.
        prev_lines: list[str] = []
        cur_row = [0]

        def draw() -> None:
            with console.capture() as cap:
                console.print(_screen(s))
            text = cap.get()
            if text.endswith("\n"):
                text = text[:-1]
            new_lines = text.split("\n")

            buf: list[str] = []

            if not prev_lines:
                # first frame: just print it
                buf.append(text)
                cur = len(new_lines) - 1
            else:
                # move cursor to top of previous frame (row 0, col 1)
                if cur_row[0] > 0:
                    buf.append(f"\x1b[{cur_row[0]}F")
                else:
                    buf.append("\r")
                cur = 0
                total = max(len(prev_lines), len(new_lines))
                for i in range(total):
                    new = new_lines[i] if i < len(new_lines) else ""
                    old = prev_lines[i] if i < len(prev_lines) else None
                    if i < len(new_lines) and new == old:
                        continue  # unchanged, leave it alone
                    # navigate to row i, column 1
                    if i > cur:
                        buf.append(f"\x1b[{i - cur}E")  # cursor next line
                    elif i < cur:
                        buf.append(f"\x1b[{cur - i}F")  # cursor prev line
                    else:
                        buf.append("\r")
                    buf.append("\x1b[2K")  # erase entire current line
                    if i < len(new_lines):
                        buf.append(new)
                    cur = i
                # if previous frame was taller, clear any leftover lines below
                if len(prev_lines) > len(new_lines):
                    last = len(new_lines) - 1
                    if cur != last:
                        if last > cur:
                            buf.append(f"\x1b[{last - cur}E")
                        else:
                            buf.append(f"\x1b[{cur - last}F")
                        cur = last
                    # move just past the last new line and erase to end
                    buf.append("\x1b[1E\x1b[J\x1b[1F")
                    cur = last

            sys.stdout.write("".join(buf))
            sys.stdout.flush()

            prev_lines[:] = new_lines
            cur_row[0] = cur

        sys.stdout.write("\x1b[?25l")  # hide cursor for the whole session
        sys.stdout.flush()
        draw()
        while not s.quit:
            try:
                k = read_key()
            except (KeyboardInterrupt, EOFError):
                break
            if s.mode == render.MODE_NORMAL:
                _handle_normal(s, k)
            else:
                _handle_command(s, k)
            draw()
        # Move cursor to the bottom of the last frame so the newline lands
        # cleanly below it instead of splitting a line mid-frame.
        bottom = len(prev_lines) - 1
        if cur_row[0] < bottom:
            sys.stdout.write(f"\x1b[{bottom - cur_row[0]}E")
        sys.stdout.write("\x1b[?25h\n")  # restore cursor, then newline
        sys.stdout.flush()

    console.print("[grey50]you fade from the world.[/grey50]")
