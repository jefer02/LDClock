from __future__ import annotations

import tkinter as tk
from tkinter import messagebox

from ldclock.models.alarm import Alarm
from ldclock.services.alarm_manager import AlarmManager
from ldclock.services.time_controller import TimeController
from ldclock.ui.analog_clock import AnalogClock


class MainApp:
    """Main application controller for LDClock."""

    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.root.title("LDClock - Reloj Analógico")
        self.root.configure(bg="#f4f6fb")
        self.root.geometry("980x560")
        self.root.minsize(900, 540)

        self.time_controller = TimeController()
        self.alarm_manager = AlarmManager()

        self._current_alarm_view = "forward"
        self._alarm_index_map: list[int] = []
        self._last_checked_second = -1

        self._build_layout()
        self._start_update_loop()

    def _build_layout(self) -> None:
        self.root.grid_columnconfigure(0, weight=3)
        self.root.grid_columnconfigure(1, weight=2)
        self.root.grid_rowconfigure(0, weight=1)

        clock_container = tk.Frame(self.root, bg="#f4f6fb")
        clock_container.grid(row=0, column=0, sticky="nsew", padx=(16, 8), pady=16)

        title_label = tk.Label(
            clock_container,
            text="Reloj Analógico",
            font=("Segoe UI", 20, "bold"),
            bg="#f4f6fb",
            fg="#2a334d",
        )
        title_label.pack(pady=(0, 12))

        self.clock_widget = AnalogClock(clock_container, size=400)
        self.clock_widget.pack()

        self.mode_label = tk.Label(
            clock_container,
            text="Modo: Hora del sistema",
            font=("Segoe UI", 11, "bold"),
            bg="#f4f6fb",
            fg="#2d3a59",
        )
        self.mode_label.pack(pady=(12, 0))

        controls_container = tk.Frame(self.root, bg="#edf1f9", highlightthickness=1, highlightbackground="#d7deee")
        controls_container.grid(row=0, column=1, sticky="nsew", padx=(8, 16), pady=16)

        self._build_time_controls(controls_container)
        self._build_alarm_controls(controls_container)

    def _build_time_controls(self, parent: tk.Frame) -> None:
        section = tk.LabelFrame(
            parent,
            text="Control de hora",
            bg="#edf1f9",
            fg="#2d3a59",
            font=("Segoe UI", 11, "bold"),
            padx=10,
            pady=10,
        )
        section.pack(fill="x", padx=10, pady=(10, 8))

        tk.Label(section, text="Hora", bg="#edf1f9", font=("Segoe UI", 9)).grid(row=0, column=0, padx=4, pady=4)
        tk.Label(section, text="Min", bg="#edf1f9", font=("Segoe UI", 9)).grid(row=0, column=1, padx=4, pady=4)
        tk.Label(section, text="Seg", bg="#edf1f9", font=("Segoe UI", 9)).grid(row=0, column=2, padx=4, pady=4)

        self.time_hour_entry = tk.Entry(section, width=5, justify="center")
        self.time_minute_entry = tk.Entry(section, width=5, justify="center")
        self.time_second_entry = tk.Entry(section, width=5, justify="center")

        self.time_hour_entry.grid(row=1, column=0, padx=4, pady=4)
        self.time_minute_entry.grid(row=1, column=1, padx=4, pady=4)
        self.time_second_entry.grid(row=1, column=2, padx=4, pady=4)

        program_button = tk.Button(
            section,
            text="Programar hora",
            command=self._on_program_time,
            bg="#2f5fb3",
            fg="white",
            relief=tk.FLAT,
            padx=10,
            pady=4,
        )
        program_button.grid(row=2, column=0, columnspan=3, sticky="ew", padx=4, pady=(8, 4))

        system_button = tk.Button(
            section,
            text="Usar hora actual",
            command=self._on_use_system_time,
            bg="#5f6b85",
            fg="white",
            relief=tk.FLAT,
            padx=10,
            pady=4,
        )
        system_button.grid(row=3, column=0, columnspan=3, sticky="ew", padx=4, pady=(2, 0))

        advance_button = tk.Button(
            section,
            text="Adelantar +5 min",
            command=self._on_advance_5_minutes,
            bg="#2f8f61",
            fg="white",
            relief=tk.FLAT,
            padx=10,
            pady=4,
        )
        advance_button.grid(row=4, column=0, columnspan=3, sticky="ew", padx=4, pady=(8, 2))

        delay_button = tk.Button(
            section,
            text="Atrasar -5 min",
            command=self._on_delay_5_minutes,
            bg="#8a6a3f",
            fg="white",
            relief=tk.FLAT,
            padx=10,
            pady=4,
        )
        delay_button.grid(row=5, column=0, columnspan=3, sticky="ew", padx=4, pady=(2, 0))

    def _build_alarm_controls(self, parent: tk.Frame) -> None:
        section = tk.LabelFrame(
            parent,
            text="Alarmas",
            bg="#edf1f9",
            fg="#2d3a59",
            font=("Segoe UI", 11, "bold"),
            padx=10,
            pady=10,
        )
        section.pack(fill="both", expand=True, padx=10, pady=(8, 10))

        tk.Label(section, text="Hora", bg="#edf1f9").grid(row=0, column=0, padx=4, pady=3)
        tk.Label(section, text="Min", bg="#edf1f9").grid(row=0, column=1, padx=4, pady=3)
        tk.Label(section, text="Seg", bg="#edf1f9").grid(row=0, column=2, padx=4, pady=3)

        self.alarm_hour_entry = tk.Entry(section, width=5, justify="center")
        self.alarm_minute_entry = tk.Entry(section, width=5, justify="center")
        self.alarm_second_entry = tk.Entry(section, width=5, justify="center")

        self.alarm_hour_entry.grid(row=1, column=0, padx=4, pady=3)
        self.alarm_minute_entry.grid(row=1, column=1, padx=4, pady=3)
        self.alarm_second_entry.grid(row=1, column=2, padx=4, pady=3)

        tk.Label(section, text="Etiqueta", bg="#edf1f9").grid(row=2, column=0, columnspan=4, sticky="w", padx=4, pady=(8, 2))
        self.alarm_label_entry = tk.Entry(section)
        self.alarm_label_entry.grid(row=3, column=0, columnspan=4, sticky="ew", padx=4, pady=(0, 6))

        add_button = tk.Button(
            section,
            text="Agregar alarma",
            command=self._on_add_alarm,
            bg="#2f8f61",
            fg="white",
            relief=tk.FLAT,
            padx=8,
            pady=4,
        )
        add_button.grid(row=4, column=0, columnspan=2, sticky="ew", padx=4, pady=4)

        remove_button = tk.Button(
            section,
            text="Eliminar seleccionada",
            command=self._on_remove_selected_alarm,
            bg="#b34040",
            fg="white",
            relief=tk.FLAT,
            padx=8,
            pady=4,
        )
        remove_button.grid(row=4, column=2, columnspan=2, sticky="ew", padx=4, pady=4)

        forward_button = tk.Button(
            section,
            text="Recorrido hacia adelante",
            command=self._on_show_forward,
            bg="#4a6fa5",
            fg="white",
            relief=tk.FLAT,
            padx=8,
            pady=4,
        )
        forward_button.grid(row=5, column=0, columnspan=2, sticky="ew", padx=4, pady=(2, 4))

        backward_button = tk.Button(
            section,
            text="Recorrido hacia atrás",
            command=self._on_show_backward,
            bg="#6a5da8",
            fg="white",
            relief=tk.FLAT,
            padx=8,
            pady=4,
        )
        backward_button.grid(row=5, column=2, columnspan=2, sticky="ew", padx=4, pady=(2, 4))

        self.alarm_listbox = tk.Listbox(section, height=10)
        self.alarm_listbox.grid(row=6, column=0, columnspan=4, sticky="nsew", padx=4, pady=6)

        section.grid_columnconfigure(0, weight=1)
        section.grid_columnconfigure(1, weight=1)
        section.grid_columnconfigure(2, weight=1)
        section.grid_columnconfigure(3, weight=1)
        section.grid_rowconfigure(6, weight=1)

    def _start_update_loop(self) -> None:
        self._update_clock_and_alarms()

    def _update_clock_and_alarms(self) -> None:
        current_time = self.time_controller.get_current_time()
        self.clock_widget.update_time(current_time)

        if current_time.second != self._last_checked_second:
            self._last_checked_second = current_time.second
            due_alarms = self.alarm_manager.check_due_alarms(current_time)
            for alarm in due_alarms:
                self._show_alarm_notification(alarm)

        self.root.after(120, self._update_clock_and_alarms)

    def _show_alarm_notification(self, alarm: Alarm) -> None:
        messagebox.showinfo(
            "Alarma",
            f"Son las {alarm.hour:02d}:{alarm.minute:02d}:{alarm.second:02d}\n\n{alarm.label}",
        )

    def _on_program_time(self) -> None:
        try:
            hour = int(self.time_hour_entry.get())
            minute = int(self.time_minute_entry.get())
            second = int(self.time_second_entry.get())
        except ValueError:
            messagebox.showerror("Entrada inválida", "Ingresa números válidos para hora, minuto y segundo.")
            return

        if not (0 <= hour <= 23 and 0 <= minute <= 59 and 0 <= second <= 59):
            messagebox.showerror("Entrada inválida", "La hora debe estar en formato 24 horas válido.")
            return

        self.time_controller.set_custom_time(hour, minute, second)
        self.mode_label.config(text="Modo: Hora programada manualmente")

    def _on_use_system_time(self) -> None:
        self.time_controller.use_system_time()
        self.mode_label.config(text="Modo: Hora del sistema")

    def _on_advance_5_minutes(self) -> None:
        self.time_controller.shift_minutes(5)
        self.mode_label.config(text="Modo: Hora programada manualmente")

    def _on_delay_5_minutes(self) -> None:
        self.time_controller.shift_minutes(-5)
        self.mode_label.config(text="Modo: Hora programada manualmente")

    def _on_add_alarm(self) -> None:
        try:
            hour = int(self.alarm_hour_entry.get())
            minute = int(self.alarm_minute_entry.get())
            second = int(self.alarm_second_entry.get())
        except ValueError:
            messagebox.showerror("Entrada inválida", "Ingresa números válidos para la alarma.")
            return

        label = self.alarm_label_entry.get().strip()
        if not label:
            messagebox.showerror("Entrada inválida", "La etiqueta de la alarma es obligatoria.")
            return

        try:
            self.alarm_manager.add_alarm(hour, minute, second, label)
        except ValueError:
            messagebox.showerror("Entrada inválida", "Hora de alarma fuera de rango.")
            return

        self._refresh_alarm_list()
        self._clear_alarm_inputs()

    def _on_remove_selected_alarm(self) -> None:
        selected_indices = self.alarm_listbox.curselection()
        if not selected_indices:
            messagebox.showwarning("Sin selección", "Selecciona una alarma para eliminar.")
            return

        selected_index = selected_indices[0]
        alarm_id = self._alarm_index_map[selected_index]
        removed = self.alarm_manager.remove_alarm(alarm_id)

        if removed:
            self._refresh_alarm_list()
        else:
            messagebox.showerror("Error", "No fue posible eliminar la alarma seleccionada.")

    def _on_show_forward(self) -> None:
        self._current_alarm_view = "forward"
        self._refresh_alarm_list()

    def _on_show_backward(self) -> None:
        self._current_alarm_view = "backward"
        self._refresh_alarm_list()

    def _refresh_alarm_list(self) -> None:
        self.alarm_listbox.delete(0, tk.END)
        self._alarm_index_map.clear()

        alarms = (
            self.alarm_manager.get_alarms_forward()
            if self._current_alarm_view == "forward"
            else self.alarm_manager.get_alarms_backward()
        )

        if not alarms:
            self.alarm_listbox.insert(tk.END, "No hay alarmas registradas")
            return

        for alarm in alarms:
            self._alarm_index_map.append(alarm.alarm_id)
            self.alarm_listbox.insert(tk.END, alarm.to_display_text())

    def _clear_alarm_inputs(self) -> None:
        self.alarm_hour_entry.delete(0, tk.END)
        self.alarm_minute_entry.delete(0, tk.END)
        self.alarm_second_entry.delete(0, tk.END)
        self.alarm_label_entry.delete(0, tk.END)
