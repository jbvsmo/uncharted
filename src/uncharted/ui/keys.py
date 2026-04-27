"""Raw single-key input for terminals.

Returns small (kind, value) tuples so the game loop can dispatch on key
identity without dealing with escape sequences directly.

Supports POSIX (termios + os.read on stdin fd) and Windows (msvcrt).
"""
from __future__ import annotations

import sys
from contextlib import contextmanager
from typing import Iterator

_IS_WINDOWS = sys.platform == "win32"

# (kind, value)
#   kind: "CHAR" | "ARROW" | "ESC" | "ENTER" | "BACKSPACE"
#   value: the character (CHAR) or "UP"/"DOWN"/"LEFT"/"RIGHT" (ARROW), else None
Key = tuple[str, str | None]


# ---------------------------------------------------------------------------
# POSIX implementation
# ---------------------------------------------------------------------------

if not _IS_WINDOWS:
    import os
    import select
    import termios
    import tty

    @contextmanager
    def raw_mode(fd: int) -> Iterator[None]:
        old = termios.tcgetattr(fd)
        try:
            tty.setcbreak(fd)
            yield
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old)

    _ARROWS = {"A": "UP", "B": "DOWN", "C": "RIGHT", "D": "LEFT"}

    def _read_byte(fd: int, timeout: float | None) -> str | None:
        """Read one byte from `fd` directly, bypassing Python's buffered stdin.

        With `sys.stdin.read(1)` Python's text-mode buffer would slurp the
        entire `\\x1b[A` arrow sequence on the first call, leaving `select()`
        to report "no data" on the kernel fd — which made the loop see a bare
        ESC followed by literal `[A` characters. Using os.read on the raw fd
        avoids that.
        """
        if timeout is not None:
            r, _, _ = select.select([fd], [], [], timeout)
            if not r:
                return None
        try:
            b = os.read(fd, 1)
        except OSError:
            return None
        if not b:
            return None
        try:
            return b.decode("utf-8", errors="replace")
        except Exception:
            return None

    def read_key() -> Key:
        """Block until a key is available; return a (kind, value) tuple."""
        fd = sys.stdin.fileno()
        ch = _read_byte(fd, None)
        if ch is None:
            raise EOFError
        if ch == "\x1b":
            # lone Esc, or the start of an escape sequence (arrows etc).
            ch2 = _read_byte(fd, 0.05)
            if ch2 is None:
                return ("ESC", None)
            # Both "\x1b[A" (normal) and "\x1bOA" (application cursor mode,
            # used by some terminals / tmux setups) encode arrow keys.
            if ch2 in ("[", "O"):
                ch3 = _read_byte(fd, 0.05)
                if ch3 is None:
                    return ("ESC", None)
                if ch3 in _ARROWS:
                    return ("ARROW", _ARROWS[ch3])
                # swallow any remaining bytes of an unknown CSI sequence
                # (e.g. "\x1b[1;5A") so they don't leak into the command buffer.
                while ch3 is not None and not ("@" <= ch3 <= "~"):
                    ch3 = _read_byte(fd, 0.005)
                return ("ESC", None)
            return ("ESC", None)
        if ch in ("\r", "\n"):
            return ("ENTER", None)
        if ch in ("\x7f", "\b"):
            return ("BACKSPACE", None)
        if ch == "\x03":
            raise KeyboardInterrupt
        if ch == "\x04":
            raise EOFError
        return ("CHAR", ch)


# ---------------------------------------------------------------------------
# Windows implementation
# ---------------------------------------------------------------------------

else:
    import msvcrt

    @contextmanager
    def raw_mode(fd: int) -> Iterator[None]:
        # msvcrt.getwch() already bypasses line buffering; nothing to toggle.
        # We still try to enable ANSI escape processing so Rich's redraw works.
        try:
            import ctypes
            from ctypes import wintypes

            kernel32 = ctypes.windll.kernel32
            ENABLE_VT = 0x0004
            STD_OUTPUT = -11
            handle = kernel32.GetStdHandle(STD_OUTPUT)
            mode = wintypes.DWORD()
            if kernel32.GetConsoleMode(handle, ctypes.byref(mode)):
                kernel32.SetConsoleMode(handle, mode.value | ENABLE_VT)
        except Exception:
            pass
        yield

    # Windows console returns arrow keys as a two-step sequence starting with
    # either '\x00' or '\xe0', followed by a code byte.
    _WIN_ARROWS = {"H": "UP", "P": "DOWN", "K": "LEFT", "M": "RIGHT"}

    def read_key() -> Key:
        """Block until a key is available; return a (kind, value) tuple."""
        ch = msvcrt.getwch()
        if ch in ("\x00", "\xe0"):
            ch2 = msvcrt.getwch()
            if ch2 in _WIN_ARROWS:
                return ("ARROW", _WIN_ARROWS[ch2])
            return ("ESC", None)
        if ch == "\x1b":
            return ("ESC", None)
        if ch in ("\r", "\n"):
            return ("ENTER", None)
        if ch in ("\x08", "\x7f"):
            return ("BACKSPACE", None)
        if ch == "\x03":
            raise KeyboardInterrupt
        if ch == "\x04":
            raise EOFError
        return ("CHAR", ch)
