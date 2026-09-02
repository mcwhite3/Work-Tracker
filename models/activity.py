from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from uuid import uuid4


@dataclass(slots=True)
class Activity:
    start_time: datetime
    end_time: datetime
    activity_type: str
    project: str = ""
    msm_number: str = ""
    notes: str = ""
    activity_id: str = field(default_factory=lambda: str(uuid4()))

    @property
    def duration_minutes(self) -> int:
        return int((self.end_time - self.start_time).total_seconds() // 60)

    def to_dict(self) -> dict[str, str]:
        return {
            "activity_id": self.activity_id,
            "start_time": self.start_time.isoformat(),
            "end_time": self.end_time.isoformat(),
            "activity_type": self.activity_type,
            "project": self.project,
            "msm_number": self.msm_number,
            "notes": self.notes,
        }

    @classmethod
    def from_dict(cls, data: dict[str, str]) -> Activity:
        return cls(
            activity_id=data["activity_id"],
            start_time=datetime.fromisoformat(data["start_time"]),
            end_time=datetime.fromisoformat(data["end_time"]),
            activity_type=data["activity_type"],
            project=data.get("project", ""),
            msm_number=data.get("msm_number", ""),
            notes=data.get("notes", ""),
        )

