from __future__ import annotations

import tkinter as tk
from datetime import date
from tkinter import ttk

from models import DaySchedule
from ui.sidebar import Sidebar
from ui.summary import SummaryPanel


class PlannerApp:
    def __init__(self) -> None:
        self.root = tk.Tk()
        self.root.title("Work Tracker")
        self.root.geometry("1000x720")
        self.root.minsize(860, 560)

        self.schedule = DaySchedule(schedule_date=date.today())

        self._configure_styles()
        self._build_layout()
        self._draw_timeline()

    def run(self) -> None:
        self.root.mainloop()

    def _configure_styles(self) -> None:
        style = ttk.Style(self.root)
        style.theme_use("clam")
        style.configure("App.TFrame", background="#f6f7f9")
        style.configure("Panel.TFrame", background="#ffffff")
        style.configure("Title.TLabel", background="#ffffff", font=("Segoe UI", 16, "bold"))
        style.configure("Muted.TLabel", background="#ffffff", foreground="#5f6673")
        style.configure("Sidebar.TButton", padding=(10, 8))

    def _build_layout(self) -> None:
        self.root.configure(background="#f6f7f9")

        shell = ttk.Frame(self.root, style="App.TFrame", padding=16)
        shell.pack(fill=tk.BOTH, expand=True)
        shell.columnconfigure(1, weight=1)
        shell.rowconfigure(0, weight=1)

        self.sidebar = Sidebar(shell)
        self.sidebar.grid(row=0, column=0, sticky="nsw", padx=(0, 12))

        center = ttk.Frame(shell, style="Panel.TFrame", padding=16)
        center.grid(row=0, column=1, sticky="nsew")
        center.columnconfigure(0, weight=1)
        center.rowconfigure(1, weight=1)

        header = ttk.Frame(center, style="Panel.TFrame")
        header.grid(row=0, column=0, sticky="ew", pady=(0, 12))
        header.columnconfigure(0, weight=1)

        ttk.Label(header, text="Today", style="Title.TLabel").grid(row=0, column=0, sticky="w")
        ttk.Label(
            header,
            text="Placeholder timeline view for the first MVP milestone",
            style="Muted.TLabel",
        ).grid(row=1, column=0, sticky="w", pady=(4, 0))

        self.timeline_canvas = tk.Canvas(
            center,
            background="#ffffff",
            highlightthickness=1,
            highlightbackground="#d9dde5",
        )
        self.timeline_canvas.grid(row=1, column=0, sticky="nsew")

        self.summary = SummaryPanel(shell)
        self.summary.grid(row=0, column=2, sticky="nse", padx=(12, 0))

    def _draw_timeline(self) -> None:
        self.timeline_canvas.delete("all")

        hour_height = 72
        start_hour = 8
        end_hour = 17
        left_margin = 72
        top_margin = 24
        right_edge = 820

        for index, hour in enumerate(range(start_hour, end_hour + 1)):
            y = top_margin + index * hour_height
            label = self._format_hour(hour)
            self.timeline_canvas.create_text(
                24,
                y,
                text=label,
                anchor="w",
                fill="#3d4552",
                font=("Segoe UI", 10),
            )
            self.timeline_canvas.create_line(
                left_margin,
                y,
                right_edge,
                y,
                fill="#edf0f4",
            )

        self.timeline_canvas.create_rectangle(
            left_margin,
            top_margin + hour_height,
            right_edge - 24,
            top_margin + hour_height * 2,
            fill="#d8ebff",
            outline="#7bb4ea",
            width=1,
        )
        self.timeline_canvas.create_text(
            left_margin + 16,
            top_margin + hour_height + 16,
            text="Sample activity block",
            anchor="nw",
            fill="#16446d",
            font=("Segoe UI", 11, "bold"),
        )
        self.timeline_canvas.create_text(
            left_margin + 16,
            top_margin + hour_height + 42,
            text="Drag, resize, and editing behavior will come next",
            anchor="nw",
            fill="#385d7c",
            font=("Segoe UI", 9),
        )

    @staticmethod
    def _format_hour(hour: int) -> str:
        suffix = "AM" if hour < 12 else "PM"
        display_hour = hour if hour <= 12 else hour - 12
        return f"{display_hour}:00 {suffix}"

