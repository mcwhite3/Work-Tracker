from __future__ import annotations

from models import DaySchedule


def validate_schedule(schedule: DaySchedule) -> list[str]:
    messages: list[str] = []

    for activity in schedule.activities:
        if activity.end_time <= activity.start_time:
            messages.append(f"{activity.activity_type} must end after it starts.")

    return messages

