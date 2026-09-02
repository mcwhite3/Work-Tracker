from __future__ import annotations

from collections import defaultdict

from models import DaySchedule


def summarize_by_activity_type(schedule: DaySchedule) -> dict[str, int]:
    totals: dict[str, int] = defaultdict(int)

    for activity in schedule.activities:
        totals[activity.activity_type] += activity.duration_minutes

    return dict(totals)

