from __future__ import annotations

import tkinter as tk
from datetime import date, datetime, timedelta
from pathlib import Path
from tkinter import filedialog, messagebox, ttk

from app_info import APP_DISPLAY_NAME, APP_NAME, APP_VERSION
from models import Activity, DaySchedule
from services.storage import load_schedule, save_schedule
from services.summary import build_submission_text
from services.validation import validate_schedule
from ui.dialogs import ActivityDialog
from ui.sidebar import Sidebar
from ui.summary import SummaryPanel


SCHEDULE_FOLDER = Path(__file__).resolve().parents[1] / "data" / "schedules"
TIMELINE_START_HOUR = 8
TIMELINE_END_HOUR = 17
HOUR_HEIGHT = 72
LEFT_MARGIN = 72
TOP_MARGIN = 24
SNAP_MINUTES = 15


class PlannerApp:
    def __init__(self) -> None:
        self.root = tk.Tk()
        self.root.title(APP_DISPLAY_NAME)
        self.root.geometry("1000x720")
        self.root.minsize(860, 560)

        self.schedule = DaySchedule(schedule_date=date.today())
        self.activity_canvas_items: dict[int, str] = {}
        self.activity_rectangles: dict[str, int] = {}
        self.activity_handles: dict[str, int] = {}
        self.drag_state: dict[str, object] | None = None

        self._configure_styles()
        self._build_layout()
        self.refresh()

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

        self.sidebar = Sidebar(shell, on_activity_selected=self.add_activity)
        self.sidebar.grid(row=0, column=0, sticky="nsw", padx=(0, 12))

        center = ttk.Frame(shell, style="Panel.TFrame", padding=16)
        center.grid(row=0, column=1, sticky="nsew")
        center.columnconfigure(0, weight=1)
        center.rowconfigure(1, weight=1)

        header = ttk.Frame(center, style="Panel.TFrame")
        header.grid(row=0, column=0, sticky="ew", pady=(0, 12))
        header.columnconfigure(0, weight=1)

        self.title_label = ttk.Label(header, text=APP_NAME, style="Title.TLabel")
        self.title_label.grid(row=0, column=0, sticky="w")
        self.date_label = ttk.Label(header, text="", style="Muted.TLabel")
        self.date_label.grid(row=1, column=0, sticky="w", pady=(4, 0))
        self.status_label = ttk.Label(
            header,
            text="Add activity blocks, save them for later, or copy a paste-ready summary.",
            style="Muted.TLabel",
        )
        self.status_label.grid(row=2, column=0, sticky="w", pady=(4, 0))

        actions = ttk.Frame(header, style="Panel.TFrame")
        actions.grid(row=0, column=1, rowspan=3, sticky="e")
        ttk.Button(actions, text="Add Activity", command=self.add_activity).pack(side=tk.LEFT, padx=(0, 6))
        ttk.Button(actions, text="Load", command=self.load_for_later).pack(side=tk.LEFT, padx=(0, 6))
        ttk.Button(actions, text="Save", command=self.save_for_later).pack(side=tk.LEFT, padx=(0, 6))
        ttk.Button(actions, text="Save & Copy", command=self.save_and_copy).pack(side=tk.LEFT)

        self.timeline_canvas = tk.Canvas(
            center,
            background="#ffffff",
            highlightthickness=1,
            highlightbackground="#d9dde5",
        )
        self.timeline_canvas.grid(row=1, column=0, sticky="nsew")
        self.timeline_canvas.bind("<ButtonPress-1>", self._on_timeline_press)
        self.timeline_canvas.bind("<B1-Motion>", self._on_timeline_drag)
        self.timeline_canvas.bind("<ButtonRelease-1>", self._on_timeline_release)
        self.timeline_canvas.bind("<Configure>", lambda _event: self.refresh())

        self.summary = SummaryPanel(shell)
        self.summary.grid(row=0, column=2, sticky="nse", padx=(12, 0))

    def refresh(self) -> None:
        self.date_label.configure(
            text=f"{self.schedule.schedule_date.strftime('%A, %B %d, %Y')} | v{APP_VERSION}"
        )
        self._draw_timeline()
        self.summary.update_schedule(self.schedule)

    def add_activity(self, activity_type: str = "") -> None:
        dialog = ActivityDialog(
            self.root,
            schedule_date=self.schedule.schedule_date,
            default_activity_type=activity_type,
        )

        if dialog.result:
            self.schedule.add_activity(dialog.result)
            self.refresh()

    def add_activity_from_times(
        self,
        start_time: datetime,
        end_time: datetime,
        activity_type: str = "",
    ) -> None:
        dialog = ActivityDialog(
            self.root,
            schedule_date=self.schedule.schedule_date,
            default_activity_type=activity_type,
            default_start=start_time,
            default_end=end_time,
        )

        if dialog.result:
            self.schedule.add_activity(dialog.result)
            self.refresh()

    def edit_activity(self, activity_id: str) -> None:
        activity = self._find_activity(activity_id)
        if not activity:
            return

        dialog = ActivityDialog(
            self.root,
            schedule_date=self.schedule.schedule_date,
            activity=activity,
        )

        if dialog.result:
            self.schedule.replace_activity(dialog.result)
            self.refresh()

    def save_for_later(self) -> None:
        messages = validate_schedule(self.schedule)
        if messages and not messagebox.askyesno(
            "Validation Warnings",
            "Some items need attention:\n\n"
            + "\n".join(messages)
            + "\n\nSave anyway?",
            parent=self.root,
        ):
            return

        output_path = save_schedule(self.schedule, SCHEDULE_FOLDER)
        self.status_label.configure(text=f"Saved for later: {output_path.name}")

    def load_for_later(self) -> None:
        SCHEDULE_FOLDER.mkdir(parents=True, exist_ok=True)
        selected_path = filedialog.askopenfilename(
            title="Open Schedule",
            initialdir=SCHEDULE_FOLDER,
            filetypes=[("Schedule files", "*.json"), ("All files", "*.*")],
            parent=self.root,
        )
        if not selected_path:
            return

        self.schedule = load_schedule(Path(selected_path))
        self.status_label.configure(text=f"Loaded: {Path(selected_path).name}")
        self.refresh()

    def save_and_copy(self) -> None:
        messages = validate_schedule(self.schedule)
        if messages:
            messagebox.showwarning(
                "Validation Warnings",
                "Review these before submitting:\n\n" + "\n".join(messages),
                parent=self.root,
            )

        save_schedule(self.schedule, SCHEDULE_FOLDER)
        submission_text = build_submission_text(self.schedule)
        self.root.clipboard_clear()
        self.root.clipboard_append(submission_text)
        self.root.update()
        self.status_label.configure(text="Saved and copied paste-ready rows to clipboard.")
        messagebox.showinfo(
            "Ready to Paste",
            "Your schedule was saved and copied as tab-separated rows.",
            parent=self.root,
        )

    def _draw_timeline(self) -> None:
        self.timeline_canvas.delete("all")
        self.activity_canvas_items.clear()
        self.activity_rectangles.clear()
        self.activity_handles.clear()

        right_edge = max(self.timeline_canvas.winfo_width() - 24, 760)

        for index, hour in enumerate(range(TIMELINE_START_HOUR, TIMELINE_END_HOUR + 1)):
            y = TOP_MARGIN + index * HOUR_HEIGHT
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
                LEFT_MARGIN,
                y,
                right_edge,
                y,
                fill="#edf0f4",
            )

            if hour < TIMELINE_END_HOUR:
                half_hour_y = y + HOUR_HEIGHT / 2
                self.timeline_canvas.create_line(
                    LEFT_MARGIN,
                    half_hour_y,
                    right_edge,
                    half_hour_y,
                    fill="#dfe4ec",
                    dash=(2, 4),
                )
                self.timeline_canvas.create_text(
                    42,
                    half_hour_y,
                    text=":30",
                    anchor="w",
                    fill="#8a93a3",
                    font=("Segoe UI", 8),
                )

        if not self.schedule.activities:
            self.timeline_canvas.create_text(
                LEFT_MARGIN + 16,
                TOP_MARGIN + 32,
                text="Add your first activity to start building today's schedule.",
                anchor="nw",
                fill="#5f6673",
                font=("Segoe UI", 11),
            )

        for activity in self.schedule.activities:
            self._draw_activity(activity, right_edge)

    def _draw_activity(
        self,
        activity: Activity,
        right_edge: int,
    ) -> None:
        start_minutes = self._time_to_timeline_minutes(activity.start_time)
        end_minutes = self._time_to_timeline_minutes(activity.end_time)

        y1 = self._minutes_to_y(max(start_minutes, 0))
        y2 = self._minutes_to_y(max(end_minutes, SNAP_MINUTES))
        y2 = max(y2, y1 + 28)

        rectangle = self.timeline_canvas.create_rectangle(
            LEFT_MARGIN,
            y1,
            right_edge - 24,
            y2,
            fill="#d8ebff",
            outline="#7bb4ea",
            width=1,
            tags=(activity.activity_id, "activity"),
        )
        title = self.timeline_canvas.create_text(
            LEFT_MARGIN + 12,
            y1 + 8,
            text=f"{activity.activity_type}  {activity.start_time.strftime('%I:%M %p').lstrip('0')}",
            anchor="nw",
            fill="#16446d",
            font=("Segoe UI", 10, "bold"),
            tags=(activity.activity_id, "activity"),
        )
        details = self.timeline_canvas.create_text(
            LEFT_MARGIN + 12,
            y1 + 30,
            text=self._activity_detail_text(activity),
            anchor="nw",
            fill="#385d7c",
            font=("Segoe UI", 9),
            tags=(activity.activity_id, "activity"),
        )
        handle = self.timeline_canvas.create_rectangle(
            LEFT_MARGIN,
            y2 - 6,
            right_edge - 24,
            y2,
            fill="#7bb4ea",
            outline="#7bb4ea",
            tags=(activity.activity_id, "resize_handle"),
        )

        self.activity_rectangles[activity.activity_id] = rectangle
        self.activity_handles[activity.activity_id] = handle

        for item_id in (rectangle, title, details, handle):
            self.activity_canvas_items[item_id] = activity.activity_id
            self.timeline_canvas.tag_bind(
                item_id,
                "<Double-Button-1>",
                lambda _event, selected=activity.activity_id: self.edit_activity(selected),
            )

    def _on_timeline_press(self, event: tk.Event) -> None:
        item_id = self._canvas_item_at(event.x, event.y)
        activity_id = self.activity_canvas_items.get(item_id) if item_id else None
        timeline_bottom = self._minutes_to_y(self._timeline_total_minutes())

        if activity_id and item_id in self.activity_handles.values():
            activity = self._find_activity(activity_id)
            if not activity:
                return
            self.drag_state = {
                "mode": "resize",
                "activity_id": activity_id,
                "start_y": event.y,
                "last_y": event.y,
                "original_start": activity.start_time,
                "original_end": activity.end_time,
            }
            return

        if activity_id:
            activity = self._find_activity(activity_id)
            if not activity:
                return
            self.drag_state = {
                "mode": "move",
                "activity_id": activity_id,
                "start_y": event.y,
                "last_y": event.y,
                "original_start": activity.start_time,
                "original_end": activity.end_time,
            }
            return

        if LEFT_MARGIN <= event.x and TOP_MARGIN <= event.y <= timeline_bottom:
            start_y = self._snap_y(event.y)
            draft = self.timeline_canvas.create_rectangle(
                LEFT_MARGIN,
                start_y,
                max(self.timeline_canvas.winfo_width() - 48, 736),
                start_y + self._minutes_to_pixels(30),
                fill="#eef6ff",
                outline="#7bb4ea",
                dash=(4, 3),
            )
            self.drag_state = {
                "mode": "draw",
                "start_y": start_y,
                "last_y": start_y,
                "draft": draft,
            }

    def _on_timeline_drag(self, event: tk.Event) -> None:
        if not self.drag_state:
            return

        mode = self.drag_state["mode"]

        if mode == "move":
            activity_id = str(self.drag_state["activity_id"])
            last_y = int(self.drag_state["last_y"])
            dy = event.y - last_y
            self.timeline_canvas.move(activity_id, 0, dy)
            self.drag_state["last_y"] = event.y
            return

        if mode == "resize":
            activity_id = str(self.drag_state["activity_id"])
            rectangle = self.activity_rectangles.get(activity_id)
            handle = self.activity_handles.get(activity_id)
            if not rectangle or not handle:
                return

            y2 = self._snap_y(event.y)
            original_start = self.drag_state["original_start"]
            if not isinstance(original_start, datetime):
                return
            min_y2 = self._minutes_to_y(
                self._time_to_timeline_minutes(original_start) + SNAP_MINUTES
            )
            y2 = max(y2, min_y2)
            y2 = min(y2, self._minutes_to_y(self._timeline_total_minutes()))

            x1, y1, x2, _old_y2 = self.timeline_canvas.coords(rectangle)
            self.timeline_canvas.coords(rectangle, x1, y1, x2, y2)
            self.timeline_canvas.coords(handle, x1, y2 - 6, x2, y2)
            return

        if mode == "draw":
            draft = self.drag_state.get("draft")
            if not isinstance(draft, int):
                return
            start_y = float(self.drag_state["start_y"])
            current_y = self._snap_y(event.y)
            top = min(start_y, current_y)
            bottom = max(start_y, current_y)
            if bottom - top < self._minutes_to_pixels(SNAP_MINUTES):
                bottom = top + self._minutes_to_pixels(SNAP_MINUTES)
            bottom = min(bottom, self._minutes_to_y(self._timeline_total_minutes()))
            self.timeline_canvas.coords(
                draft,
                LEFT_MARGIN,
                top,
                max(self.timeline_canvas.winfo_width() - 48, 736),
                bottom,
            )

    def _on_timeline_release(self, event: tk.Event) -> None:
        if not self.drag_state:
            return

        mode = self.drag_state["mode"]

        if mode == "move":
            self._finish_move(event.y)
        elif mode == "resize":
            self._finish_resize(event.y)
        elif mode == "draw":
            self._finish_draw()

        self.drag_state = None

    def _finish_move(self, y: int) -> None:
        if not self.drag_state:
            return

        activity_id = str(self.drag_state["activity_id"])
        activity = self._find_activity(activity_id)
        original_start = self.drag_state["original_start"]
        original_end = self.drag_state["original_end"]
        start_y = int(self.drag_state["start_y"])
        if not activity or not isinstance(original_start, datetime) or not isinstance(original_end, datetime):
            self.refresh()
            return

        delta_minutes = self._pixels_to_minutes(self._snap_y(y) - self._snap_y(start_y))
        duration_minutes = int((original_end - original_start).total_seconds() // 60)
        new_start_minutes = self._time_to_timeline_minutes(original_start) + delta_minutes
        new_start_minutes = max(0, min(new_start_minutes, self._timeline_total_minutes() - duration_minutes))
        new_end_minutes = new_start_minutes + duration_minutes

        updated_activity = Activity(
            activity_id=activity.activity_id,
            start_time=self._timeline_minutes_to_datetime(new_start_minutes),
            end_time=self._timeline_minutes_to_datetime(new_end_minutes),
            activity_type=activity.activity_type,
            project=activity.project,
            msm_number=activity.msm_number,
            notes=activity.notes,
        )
        self.schedule.replace_activity(updated_activity)
        self.refresh()

    def _finish_resize(self, y: int) -> None:
        if not self.drag_state:
            return

        activity_id = str(self.drag_state["activity_id"])
        activity = self._find_activity(activity_id)
        original_start = self.drag_state["original_start"]
        if not activity or not isinstance(original_start, datetime):
            self.refresh()
            return

        start_minutes = self._time_to_timeline_minutes(original_start)
        end_minutes = self._y_to_minutes(y)
        end_minutes = max(end_minutes, start_minutes + SNAP_MINUTES)
        end_minutes = min(end_minutes, self._timeline_total_minutes())

        updated_activity = Activity(
            activity_id=activity.activity_id,
            start_time=original_start,
            end_time=self._timeline_minutes_to_datetime(end_minutes),
            activity_type=activity.activity_type,
            project=activity.project,
            msm_number=activity.msm_number,
            notes=activity.notes,
        )
        self.schedule.replace_activity(updated_activity)
        self.refresh()

    def _finish_draw(self) -> None:
        if not self.drag_state:
            return

        draft = self.drag_state.get("draft")
        if isinstance(draft, int):
            coords = self.timeline_canvas.coords(draft)
            self.timeline_canvas.delete(draft)
        else:
            coords = []

        if len(coords) != 4:
            return

        y1, y2 = sorted((coords[1], coords[3]))
        start_minutes = self._y_to_minutes(y1)
        end_minutes = self._y_to_minutes(y2)
        if end_minutes <= start_minutes:
            end_minutes = start_minutes + 30

        end_minutes = min(end_minutes, self._timeline_total_minutes())
        self.add_activity_from_times(
            self._timeline_minutes_to_datetime(start_minutes),
            self._timeline_minutes_to_datetime(end_minutes),
        )

    @staticmethod
    def _format_hour(hour: int) -> str:
        suffix = "AM" if hour < 12 else "PM"
        display_hour = hour if hour <= 12 else hour - 12
        return f"{display_hour}:00 {suffix}"

    @staticmethod
    def _activity_detail_text(activity: Activity) -> str:
        pieces = []
        if activity.msm_number:
            pieces.append(f"MSM {activity.msm_number}")
        if activity.project:
            pieces.append(activity.project)
        if activity.notes:
            pieces.append(activity.notes)
        return " | ".join(pieces) or "Double-click to edit"

    def _find_activity(self, activity_id: str) -> Activity | None:
        return next(
            (
                activity
                for activity in self.schedule.activities
                if activity.activity_id == activity_id
            ),
            None,
        )

    def _canvas_item_at(self, x: int, y: int) -> int | None:
        item_ids = self.timeline_canvas.find_overlapping(x, y, x, y)
        return item_ids[-1] if item_ids else None

    @staticmethod
    def _timeline_total_minutes() -> int:
        return (TIMELINE_END_HOUR - TIMELINE_START_HOUR) * 60

    @staticmethod
    def _minutes_to_pixels(minutes: int) -> float:
        return minutes * HOUR_HEIGHT / 60

    @staticmethod
    def _pixels_to_minutes(pixels: float) -> int:
        return round(pixels * 60 / HOUR_HEIGHT / SNAP_MINUTES) * SNAP_MINUTES

    def _minutes_to_y(self, minutes: int) -> float:
        return TOP_MARGIN + self._minutes_to_pixels(minutes)

    def _y_to_minutes(self, y: float) -> int:
        raw_minutes = int(round((y - TOP_MARGIN) * 60 / HOUR_HEIGHT))
        snapped = round(raw_minutes / SNAP_MINUTES) * SNAP_MINUTES
        return max(0, min(snapped, self._timeline_total_minutes()))

    def _snap_y(self, y: float) -> float:
        return self._minutes_to_y(self._y_to_minutes(y))

    @staticmethod
    def _time_to_timeline_minutes(value: datetime) -> int:
        return (value.hour - TIMELINE_START_HOUR) * 60 + value.minute

    def _timeline_minutes_to_datetime(self, minutes: int) -> datetime:
        start_of_day = datetime.combine(self.schedule.schedule_date, datetime.min.time())
        return start_of_day + timedelta(hours=TIMELINE_START_HOUR, minutes=minutes)
