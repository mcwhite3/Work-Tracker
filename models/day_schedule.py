from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date

from .activity import Activity


@dataclass(slots=True)
class DaySchedule:
    schedule_date: date
    activities: list[Activity] = field(default_factory=list)

    def add_activity(self, activity: Activity) -> None:
        self.activities.append(activity)
        self.activities.sort(key=lambda item: item.start_time)

    def remove_activity(self, activity_id: str) -> None:
        self.activities = [
            activity for activity in self.activities if activity.activity_id != activity_id
        ]

    def to_dict(self) -> dict[str, object]:
        return {
            "schedule_date": self.schedule_date.isoformat(),
            "activities": [activity.to_dict() for activity in self.activities],
        }

    @classmethod
    def from_dict(cls, data: dict[str, object]) -> DaySchedule:
        activities = [
            Activity.from_dict(activity)
            for activity in data.get("activities", [])
            if isinstance(activity, dict)
        ]
        return cls(
            schedule_date=date.fromisoformat(str(data["schedule_date"])),
            activities=activities,
        )

