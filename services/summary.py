from __future__ import annotations

from collections import defaultdict

from models import DaySchedule


def format_minutes(minutes: int) -> str:
    hours, remainder = divmod(minutes, 60)
    return f"{hours}h {remainder:02d}m"


def total_minutes(schedule: DaySchedule) -> int:
    return sum(activity.duration_minutes for activity in schedule.activities)


def summarize_by_activity_type(schedule: DaySchedule) -> dict[str, int]:
    totals: dict[str, int] = defaultdict(int)

    for activity in schedule.activities:
        totals[activity.activity_type] += activity.duration_minutes

    return dict(totals)


def build_submission_text(schedule: DaySchedule) -> str:
    rows = [
        [
            "Date",
            "Start",
            "End",
            "Duration",
            "Activity Type",
            "Project",
            "MSM Number",
            "Notes",
        ]
    ]

    for activity in sorted(schedule.activities, key=lambda item: item.start_time):
        rows.append(
            [
                schedule.schedule_date.isoformat(),
                activity.start_time.strftime("%I:%M %p").lstrip("0"),
                activity.end_time.strftime("%I:%M %p").lstrip("0"),
                format_minutes(activity.duration_minutes),
                activity.activity_type,
                activity.project,
                activity.msm_number,
                activity.notes.replace("\n", " "),
            ]
        )

    return "\n".join("\t".join(row) for row in rows)
