import json
from pathlib import Path


SETTINGS_PATH = Path("data/settings.json")


DEFAULT_SETTINGS = {
    "monitoring_interval": 2,
    "appearance_mode": "dark"
}


def ensure_settings_file():
    """Create the settings file if it does not exist."""

    SETTINGS_PATH.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    if not SETTINGS_PATH.exists():

        save_settings(
            DEFAULT_SETTINGS.copy()
        )


def load_settings():
    """Load application settings."""

    ensure_settings_file()

    try:

        with open(
            SETTINGS_PATH,
            "r",
            encoding="utf-8"
        ) as file:

            settings = json.load(file)

        # Make sure missing settings get defaults

        for key, value in DEFAULT_SETTINGS.items():

            if key not in settings:
                settings[key] = value

        return settings

    except (
        json.JSONDecodeError,
        OSError
    ):

        return DEFAULT_SETTINGS.copy()


def save_settings(settings):
    """Save application settings."""

    SETTINGS_PATH.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    with open(
        SETTINGS_PATH,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            settings,
            file,
            indent=4
        )


def update_setting(
    key,
    value
):
    """Update one setting."""

    settings = load_settings()

    settings[key] = value

    save_settings(
        settings
    )


def get_setting(
    key,
    default=None
):
    """Return one setting."""

    settings = load_settings()

    return settings.get(
        key,
        default
    )