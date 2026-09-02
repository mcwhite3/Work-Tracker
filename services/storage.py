from __future__ import annotations

import json
from pathlib import Path

from models import DaySchedule


def save_schedule(schedule: DaySchedule, folder: Path) -> Path:
    folder.mkdir(parents=True, exist_ok=True)
    output_path = folder / f"{schedule.schedule_date.isoformat()}.json"
    output_path.write_text(json.dumps(schedule.to_dict(), indent=2), encoding="utf-8")
    return output_path


def load_schedule(path: Path) -> DaySchedule:
    data = json.loads(path.read_text(encoding="utf-8"))
    return DaySchedule.from_dict(data)

