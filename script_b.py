"""Another script using the same shared settings file."""

from settings_manager import load_settings


def main() -> None:
    settings = load_settings()
    print(
        f"[script_b] auto_start={settings['auto_start']}, "
        f"output_directory={settings['output_directory']}"
    )


if __name__ == "__main__":
    main()
