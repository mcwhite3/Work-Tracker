from __future__ import annotations

from models import DaySchedule


class SmartsheetClient:
    def submit_schedule(self, schedule: DaySchedule) -> None:
        raise NotImplementedError("Smartsheet integration is intentionally not implemented yet.")

