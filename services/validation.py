from __future__ import annotations

from models import DaySchedule


def validate_schedule(schedule: DaySchedule) -> list[str]:
    messages: list[str] = []

    sorted_activities = sorted(schedule.activities, key=lambda item: item.start_time)

    for activity in sorted_activities:
        if activity.end_time <= activity.start_time:
            messages.append(f"{activity.activity_type} must end after it starts.")

        if "Product" in activity.activity_type and not activity.msm_number.strip():
            messages.append(f"{activity.activity_type} should include an MSM number.")

    for previous, current in zip(sorted_activities, sorted_activities[1:]):
        if current.start_time < previous.end_time:
            messages.append(
                f"{current.activity_type} overlaps with {previous.activity_type}."
            )

    return messages
