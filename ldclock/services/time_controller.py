from __future__ import annotations

import time
from datetime import datetime, timedelta


class TimeController:
    """Controls system time mode and manually programmed time mode."""

    def __init__(self) -> None:
        self._use_system_time = True
        self._custom_base_time = datetime.now()
        self._custom_set_timestamp = time.time()

    @property
    def is_system_time_enabled(self) -> bool:
        return self._use_system_time

    def get_current_time(self) -> datetime:
        if self._use_system_time:
            return datetime.now()

        elapsed_seconds = time.time() - self._custom_set_timestamp
        return self._custom_base_time + timedelta(seconds=elapsed_seconds)

    def set_custom_time(self, hour: int, minute: int, second: int) -> None:
        now = datetime.now()
        self._custom_base_time = now.replace(
            hour=hour,
            minute=minute,
            second=second,
            microsecond=0,
        )
        self._custom_set_timestamp = time.time()
        self._use_system_time = False

    def use_system_time(self) -> None:
        self._use_system_time = True

    def shift_minutes(self, delta_minutes: int) -> datetime:
        current_time = self.get_current_time()
        shifted_time = current_time + timedelta(minutes=delta_minutes)

        self._custom_base_time = shifted_time.replace(microsecond=0)
        self._custom_set_timestamp = time.time()
        self._use_system_time = False

        return self._custom_base_time
