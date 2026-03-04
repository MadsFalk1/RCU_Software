"""Example worker script reading shared settings."""

from settings_manager import load_settings


def main() -> None:
    settings = load_settings()
    print(
        f"[script_a] Running with theme={settings['theme']}, "
        f"refresh_interval={settings['refresh_interval']}"
    )


if __name__ == "__main__":
    main()
