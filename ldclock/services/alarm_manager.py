from __future__ import annotations

from datetime import datetime
from typing import Dict, List

from ldclock.data_structures.circular_doubly_linked_list import CircularDoublyLinkedList
from ldclock.models.alarm import Alarm


class AlarmManager:
    """Service that manages alarms using a circular doubly linked list."""

    def __init__(self) -> None:
        self._alarms = CircularDoublyLinkedList[Alarm]()
        self._next_id = 1
        self._last_trigger_by_alarm: Dict[int, str] = {}

    def add_alarm(self, hour: int, minute: int, second: int, label: str) -> Alarm:
        clean_label = label.strip()
        if not clean_label:
            raise ValueError("Alarm label is required.")

        self._validate_time(hour, minute, second)
        alarm = Alarm(
            alarm_id=self._next_id,
            hour=hour,
            minute=minute,
            second=second,
            label=clean_label,
        )
        self._alarms.insert_end(alarm)
        self._next_id += 1
        return alarm

    def remove_alarm(self, alarm_id: int) -> bool:
        removed = self._alarms.delete_by(lambda alarm: alarm.alarm_id == alarm_id)
        if removed and alarm_id in self._last_trigger_by_alarm:
            del self._last_trigger_by_alarm[alarm_id]
        return removed

    def get_alarms_forward(self) -> List[Alarm]:
        return self._alarms.traverse_forward()

    def get_alarms_backward(self) -> List[Alarm]:
        return self._alarms.traverse_backward()

    def is_empty(self) -> bool:
        return self._alarms.is_empty()

    def check_due_alarms(self, current_time: datetime) -> List[Alarm]:
        triggered: List[Alarm] = []
        current_second_key = current_time.strftime("%Y-%m-%d %H:%M:%S")

        for alarm in self._alarms.traverse_forward():
            if not alarm.matches_time(current_time):
                continue

            last_trigger_key = self._last_trigger_by_alarm.get(alarm.alarm_id)
            if last_trigger_key == current_second_key:
                continue

            self._last_trigger_by_alarm[alarm.alarm_id] = current_second_key
            triggered.append(alarm)

        return triggered

    @staticmethod
    def _validate_time(hour: int, minute: int, second: int) -> None:
        if not (0 <= hour <= 23):
            raise ValueError("Hour must be between 0 and 23.")
        if not (0 <= minute <= 59):
            raise ValueError("Minute must be between 0 and 59.")
        if not (0 <= second <= 59):
            raise ValueError("Second must be between 0 and 59.")
