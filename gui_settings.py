"""Simple GUI editor backed by settings.json."""

from __future__ import annotations

import tkinter as tk
from tkinter import ttk

from settings_manager import load_settings, save_settings


class SettingsGUI(tk.Tk):
    def __init__(self) -> None:
        super().__init__()
        self.title("Application Settings")
        self.geometry("380x260")

        self._settings = load_settings()

        self.theme_var = tk.StringVar(value=self._settings["theme"])
        self.refresh_var = tk.IntVar(value=self._settings["refresh_interval"])
        self.auto_start_var = tk.BooleanVar(value=self._settings["auto_start"])
        self.output_var = tk.StringVar(value=self._settings["output_directory"])

        self._build_form()

    def _build_form(self) -> None:
        wrapper = ttk.Frame(self, padding=12)
        wrapper.pack(fill="both", expand=True)

        ttk.Label(wrapper, text="Theme").grid(row=0, column=0, sticky="w", pady=4)
        theme_combo = ttk.Combobox(
            wrapper,
            textvariable=self.theme_var,
            values=["light", "dark"],
            state="readonly",
        )
        theme_combo.grid(row=0, column=1, sticky="ew", pady=4)

        ttk.Label(wrapper, text="Refresh Interval (sec)").grid(
            row=1, column=0, sticky="w", pady=4
        )
        ttk.Spinbox(wrapper, from_=1, to=3600, textvariable=self.refresh_var).grid(
            row=1, column=1, sticky="ew", pady=4
        )

        ttk.Checkbutton(
            wrapper, text="Auto start", variable=self.auto_start_var
        ).grid(row=2, column=0, columnspan=2, sticky="w", pady=4)

        ttk.Label(wrapper, text="Output Directory").grid(
            row=3, column=0, sticky="w", pady=4
        )
        ttk.Entry(wrapper, textvariable=self.output_var).grid(
            row=3, column=1, sticky="ew", pady=4
        )

        button_frame = ttk.Frame(wrapper)
        button_frame.grid(row=4, column=0, columnspan=2, pady=12, sticky="e")

        ttk.Button(button_frame, text="Save", command=self.save).pack(side="left", padx=4)
        ttk.Button(button_frame, text="Reload", command=self.reload).pack(side="left")

        self.status_label = ttk.Label(wrapper, text="")
        self.status_label.grid(row=5, column=0, columnspan=2, sticky="w")

        wrapper.columnconfigure(1, weight=1)

    def _current_form_settings(self):
        return {
            "theme": self.theme_var.get(),
            "refresh_interval": self.refresh_var.get(),
            "auto_start": self.auto_start_var.get(),
            "output_directory": self.output_var.get(),
        }

    def save(self) -> None:
        save_settings(self._current_form_settings())
        self.status_label.configure(text="Saved to settings.json")

    def reload(self) -> None:
        current = load_settings()
        self.theme_var.set(current["theme"])
        self.refresh_var.set(current["refresh_interval"])
        self.auto_start_var.set(current["auto_start"])
        self.output_var.set(current["output_directory"])
        self.status_label.configure(text="Reloaded from settings.json")


if __name__ == "__main__":
    app = SettingsGUI()
    app.mainloop()
