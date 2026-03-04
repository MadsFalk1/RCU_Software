from pathlib import Path
import sys

sys.path.append(str(Path(__file__).resolve().parents[1]))

from settings_manager import DEFAULT_SETTINGS, load_settings, save_settings


def test_load_settings_uses_defaults_for_missing_keys(tmp_path, monkeypatch):
    test_path = tmp_path / "settings.json"
    monkeypatch.setattr("settings_manager.SETTINGS_PATH", test_path)
    save_settings({"theme": "dark"})

    data = load_settings()

    assert data["theme"] == "dark"
    assert data["refresh_interval"] == DEFAULT_SETTINGS["refresh_interval"]
    assert data["auto_start"] == DEFAULT_SETTINGS["auto_start"]


def test_save_and_load_round_trip(tmp_path, monkeypatch):
    test_path = tmp_path / "settings.json"
    monkeypatch.setattr("settings_manager.SETTINGS_PATH", test_path)
    original = {
        "theme": "dark",
        "refresh_interval": 5,
        "auto_start": True,
        "output_directory": "./tmp",
    }

    save_settings(original)
    loaded = load_settings()

    assert loaded == original
