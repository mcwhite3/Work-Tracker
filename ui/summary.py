from __future__ import annotations

import tkinter as tk
from tkinter import ttk

from models import DaySchedule
from services.summary import format_minutes, summarize_by_activity_type, total_minutes


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

        self.total_label = ttk.Label(self, text="Total: 0h 00m", style="Muted.TLabel")
        self.total_label.pack(anchor="w")

        self.blocks_label = ttk.Label(self, text="Blocks: 0", style="Muted.TLabel")
        self.blocks_label.pack(anchor="w", pady=(6, 16))

        self.breakdown_frame = ttk.Frame(self, style="Panel.TFrame")
        self.breakdown_frame.pack(fill=tk.X, anchor="w")

    def update_schedule(self, schedule: DaySchedule) -> None:
        self.total_label.configure(text=f"Total: {format_minutes(total_minutes(schedule))}")
        self.blocks_label.configure(text=f"Blocks: {len(schedule.activities)}")

        for child in self.breakdown_frame.winfo_children():
            child.destroy()

        for activity_type, minutes in sorted(summarize_by_activity_type(schedule).items()):
            ttk.Label(
                self.breakdown_frame,
                text=f"{activity_type}: {format_minutes(minutes)}",
                style="Muted.TLabel",
                wraplength=190,
            ).pack(anchor="w", pady=(0, 6))
