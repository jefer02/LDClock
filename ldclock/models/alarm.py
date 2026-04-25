from dataclasses import dataclass
from datetime import datetime


@dataclass
class Alarm:
    """Alarm entity stored in the circular doubly linked list."""

    alarm_id: int
    hour: int
    minute: int
    second: int
    label: str = "Alarma"

    def matches_time(self, current_time: datetime) -> bool:
        return (
            self.hour == current_time.hour
            and self.minute == current_time.minute
            and self.second == current_time.second
        )

    def to_display_text(self) -> str:
        return f"ID {self.alarm_id:02d} - {self.hour:02d}:{self.minute:02d}:{self.second:02d} - {self.label}"
