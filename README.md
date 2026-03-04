# Shared JSON Settings

This repository now uses a single `settings.json` file as the source of truth for runtime settings.

## Files

- `settings_manager.py` – helper for reading and writing `settings.json`.
- `gui_settings.py` – Tkinter GUI that updates the JSON file.
- `script_a.py`, `script_b.py` – example scripts that read the same settings.

## Usage

```bash
python gui_settings.py
python script_a.py
python script_b.py
```

Any save action from the GUI updates `settings.json`, and all scripts read current values from that same file.
