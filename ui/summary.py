from __future__ import annotations

import tkinter as tk
from tkinter import ttk


class SummaryPanel(ttk.Frame):
    def __init__(self, parent: tk.Widget) -> None:
        super().__init__(parent, style="Panel.TFrame", padding=16)
        self._build()

    def _build(self) -> None:
        ttk.Label(self, text="Summary", style="Title.TLabel").pack(anchor="w")
        ttk.Label(
            self,
            text="Daily totals will appear here.",
            style="Muted.TLabel",
            wraplength=180,
        ).pack(anchor="w", pady=(4, 16))

        ttk.Label(self, text="Total: 0h 00m", style="Muted.TLabel").pack(anchor="w")
        ttk.Label(self, text="Blocks: 0", style="Muted.TLabel").pack(anchor="w", pady=(6, 0))

