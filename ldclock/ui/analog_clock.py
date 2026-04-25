from __future__ import annotations

import math
import tkinter as tk
from datetime import datetime


class AnalogClock(tk.Frame):
    """Tkinter analog clock widget."""

    def __init__(self, master: tk.Misc, size: int = 360) -> None:
        super().__init__(master, bg="#f4f6fb")
        self.size = size
        self.center = size // 2
        self.radius = int(size * 0.42)

        self.canvas = tk.Canvas(
            self,
            width=size,
            height=size,
            bg="#fefefe",
            highlightthickness=1,
            highlightbackground="#d6dbe8",
        )
        self.canvas.pack(padx=12, pady=12)

        self._draw_clock_face()
        self._second_hand_id = None
        self._minute_hand_id = None
        self._hour_hand_id = None
        self._center_dot_id = None

    def update_time(self, current_time: datetime) -> None:
        second = current_time.second + current_time.microsecond / 1_000_000
        minute = current_time.minute + second / 60
        hour = (current_time.hour % 12) + minute / 60

        second_angle = second * 6
        minute_angle = minute * 6
        hour_angle = hour * 30

        self._draw_hands(hour_angle, minute_angle, second_angle)

    def _draw_clock_face(self) -> None:
        margin = 18
        self.canvas.create_oval(
            margin,
            margin,
            self.size - margin,
            self.size - margin,
            fill="#ffffff",
            outline="#2d3a59",
            width=3,
        )

        # Draw hour marks and minute marks around the full circle.
        for marker in range(60):
            angle = math.radians(marker * 6 - 90)
            is_hour_marker = marker % 5 == 0

            outer_x = self.center + math.cos(angle) * (self.radius - 2)
            outer_y = self.center + math.sin(angle) * (self.radius - 2)

            inner_distance = self.radius - (20 if is_hour_marker else 10)
            inner_x = self.center + math.cos(angle) * inner_distance
            inner_y = self.center + math.sin(angle) * inner_distance

            self.canvas.create_line(
                inner_x,
                inner_y,
                outer_x,
                outer_y,
                fill="#2d3a59" if is_hour_marker else "#7c879f",
                width=3 if is_hour_marker else 1,
            )

    def _draw_hands(self, hour_angle: float, minute_angle: float, second_angle: float) -> None:
        if self._hour_hand_id is not None:
            self.canvas.delete(self._hour_hand_id)
        if self._minute_hand_id is not None:
            self.canvas.delete(self._minute_hand_id)
        if self._second_hand_id is not None:
            self.canvas.delete(self._second_hand_id)
        if self._center_dot_id is not None:
            self.canvas.delete(self._center_dot_id)

        hour_end = self._calculate_hand_end(hour_angle, self.radius * 0.52)
        minute_end = self._calculate_hand_end(minute_angle, self.radius * 0.74)
        second_end = self._calculate_hand_end(second_angle, self.radius * 0.82)

        self._hour_hand_id = self.canvas.create_line(
            self.center,
            self.center,
            hour_end[0],
            hour_end[1],
            fill="#2a334d",
            width=7,
            capstyle=tk.ROUND,
        )
        self._minute_hand_id = self.canvas.create_line(
            self.center,
            self.center,
            minute_end[0],
            minute_end[1],
            fill="#3c4d79",
            width=5,
            capstyle=tk.ROUND,
        )
        self._second_hand_id = self.canvas.create_line(
            self.center,
            self.center,
            second_end[0],
            second_end[1],
            fill="#e14d2a",
            width=2,
            capstyle=tk.ROUND,
        )
        self._center_dot_id = self.canvas.create_oval(
            self.center - 6,
            self.center - 6,
            self.center + 6,
            self.center + 6,
            fill="#e14d2a",
            outline="#e14d2a",
        )

    def _calculate_hand_end(self, angle_degrees: float, length: float) -> tuple[float, float]:
        radians_angle = math.radians(angle_degrees - 90)
        end_x = self.center + math.cos(radians_angle) * length
        end_y = self.center + math.sin(radians_angle) * length
        return end_x, end_y
