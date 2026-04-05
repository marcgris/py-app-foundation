"""Minimal desktop profile app shell for UI overlay validation."""

from __future__ import annotations

import tkinter as tk

WINDOW_TITLE = "Py App Foundation Desktop Profile"
SMOKE_MARKER_TEXT = "starter-ui-desktop-ready"


def build_window() -> tk.Tk:
    """Build the desktop window shell with deterministic marker content.

    Returns:
        Configured Tk root window instance.
    """
    root = tk.Tk()
    root.title(WINDOW_TITLE)
    root.geometry("680x420")

    marker_label = tk.Label(root, text=SMOKE_MARKER_TEXT)
    marker_label.pack(pady=24)

    return root


def run() -> None:
    """Run the desktop profile shell."""
    window = build_window()
    window.mainloop()


if __name__ == "__main__":
    run()
