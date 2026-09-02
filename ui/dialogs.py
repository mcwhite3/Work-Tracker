from __future__ import annotations

import tkinter as tk
from datetime import date, datetime, timedelta
from tkinter import messagebox, ttk

from models import Activity
from ui.sidebar import Sidebar


def show_not_ready(parent: tk.Widget, feature_name: str) -> None:
    messagebox.showinfo(
        title="Coming Soon",
        message=f"{feature_name} is planned for a future MVP milestone.",
        parent=parent,
    )


class ActivityDialog(tk.Toplevel):
    def __init__(
        self,
        parent: tk.Widget,
        schedule_date: date,
        activity: Activity | None = None,
        default_activity_type: str = "",
        default_start: datetime | None = None,
        default_end: datetime | None = None,
    ) -> None:
        super().__init__(parent)
        self.title("Activity")
        self.resizable(False, False)
        self.result: Activity | None = None
        self.schedule_date = schedule_date
        self.activity = activity

        start_value = activity.start_time if activity else default_start
        end_value = activity.end_time if activity else default_end
        self.start_var = tk.StringVar(value=self._time_value(start_value, "09:00"))
        self.end_var = tk.StringVar(value=self._time_value(end_value, "10:00"))
        self.type_var = tk.StringVar(
            value=activity.activity_type if activity else default_activity_type or Sidebar.ACTIVITY_TYPES[0]
        )
        self.project_var = tk.StringVar(value=activity.project if activity else "")
        self.msm_var = tk.StringVar(value=activity.msm_number if activity else "")

        self._build()
        self.transient(parent)
        self.grab_set()
        self.wait_window()

    def _build(self) -> None:
        frame = ttk.Frame(self, padding=16)
        frame.grid(row=0, column=0, sticky="nsew")

        self._add_labeled_entry(frame, "Start", self.start_var, 0)
        self._add_labeled_entry(frame, "End", self.end_var, 1)

        ttk.Label(frame, text="Type").grid(row=2, column=0, sticky="w", pady=(0, 8))
        ttk.Combobox(
            frame,
            textvariable=self.type_var,
            values=Sidebar.ACTIVITY_TYPES,
            state="readonly",
            width=30,
        ).grid(row=2, column=1, sticky="ew", pady=(0, 8))

        self._add_labeled_entry(frame, "Project", self.project_var, 3)
        self._add_labeled_entry(frame, "MSM Number", self.msm_var, 4)

        ttk.Label(frame, text="Notes").grid(row=5, column=0, sticky="nw", pady=(0, 8))
        self.notes_text = tk.Text(frame, width=32, height=5, wrap=tk.WORD)
        self.notes_text.grid(row=5, column=1, sticky="ew", pady=(0, 8))
        if self.activity:
            self.notes_text.insert("1.0", self.activity.notes)

        actions = ttk.Frame(frame)
        actions.grid(row=6, column=0, columnspan=2, sticky="e", pady=(8, 0))
        ttk.Button(actions, text="Cancel", command=self.destroy).pack(side=tk.RIGHT)
        ttk.Button(actions, text="Save", command=self._save).pack(side=tk.RIGHT, padx=(0, 8))

    @staticmethod
    def _add_labeled_entry(
        parent: ttk.Frame,
        label: str,
        variable: tk.StringVar,
        row: int,
    ) -> None:
        ttk.Label(parent, text=label).grid(row=row, column=0, sticky="w", pady=(0, 8))
        ttk.Entry(parent, textvariable=variable, width=32).grid(
            row=row,
            column=1,
            sticky="ew",
            pady=(0, 8),
        )

    def _save(self) -> None:
        try:
            start_time = self._parse_time(self.start_var.get())
            end_time = self._parse_time(self.end_var.get())
        except ValueError:
            messagebox.showerror(
                "Invalid Time",
                "Use a time like 9:00, 09:00, or 2:30 PM.",
                parent=self,
            )
            return

        activity_data = {
            "start_time": start_time,
            "end_time": end_time,
            "activity_type": self.type_var.get(),
            "project": self.project_var.get().strip(),
            "msm_number": self.msm_var.get().strip(),
            "notes": self.notes_text.get("1.0", tk.END).strip(),
        }
        if self.activity:
            activity_data["activity_id"] = self.activity.activity_id

        self.result = Activity(**activity_data)
        self.destroy()

    def _parse_time(self, value: str) -> datetime:
        cleaned = value.strip().upper().replace(".", "")
        formats = ("%H:%M", "%I:%M %p", "%I %p")

        for time_format in formats:
            try:
                parsed = datetime.strptime(cleaned, time_format)
                if "AM" not in cleaned and "PM" not in cleaned and 1 <= parsed.hour <= 7:
                    parsed += timedelta(hours=12)
                return datetime.combine(self.schedule_date, parsed.time())
            except ValueError:
                pass

        raise ValueError(value)

    @staticmethod
    def _time_value(value: datetime | None, fallback: str) -> str:
        return value.strftime("%H:%M") if value else fallback
