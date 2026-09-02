from __future__ import annotations

import tkinter as tk
from collections.abc import Callable
from tkinter import ttk


class Sidebar(ttk.Frame):
    ACTIVITY_TYPES = [
        "Team Meeting",
        "Personal Development",
        "Research & Technology",
        "PWM",
        "Jira: Category Review",
        "Jira: Maintenance",
        "EVT: Product Prep",
        "EVT: Product Return",
    ]

    def __init__(self, parent: tk.Widget, on_activity_selected: Callable[[str], None]) -> None:
        super().__init__(parent, style="Panel.TFrame", padding=16)
        self.on_activity_selected = on_activity_selected
        self._build()

    def _build(self) -> None:
        ttk.Label(self, text="Activities", style="Title.TLabel").pack(anchor="w")
        ttk.Label(
            self,
            text="Starter categories",
            style="Muted.TLabel",
        ).pack(anchor="w", pady=(4, 16))

        for activity_type in self.ACTIVITY_TYPES:
            ttk.Button(
                self,
                text=activity_type,
                style="Sidebar.TButton",
                command=lambda selected=activity_type: self.on_activity_selected(selected),
            ).pack(fill=tk.X, pady=3)
