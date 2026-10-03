import sqlite3
from pathlib import Path


DATABASE_PATH = Path("data/gaming_performance.db")


def get_connection():
    """Create and return a database connection."""

    DATABASE_PATH.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    return sqlite3.connect(
        DATABASE_PATH
    )


def initialize_database():
    """Create all required database tables."""

    connection = get_connection()
    cursor = connection.cursor()

    # =========================================================
    # SESSIONS TABLE
    # =========================================================

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS sessions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            game_name TEXT NOT NULL,
            start_time TEXT NOT NULL,
            end_time TEXT,
            duration_seconds REAL
        )
        """
    )

    # =========================================================
    # METRICS TABLE
    # =========================================================

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS metrics (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            session_id INTEGER NOT NULL,
            timestamp TEXT NOT NULL,
            cpu_usage REAL,
            gpu_usage REAL,
            ram_usage REAL,
            gpu_temperature REAL,
            gpu_memory_used REAL,
            FOREIGN KEY (session_id)
                REFERENCES sessions(id)
        )
        """
    )

    # =========================================================
    # GAME PROFILES TABLE
    # =========================================================

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS game_profiles (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            game_name TEXT NOT NULL UNIQUE,
            resolution TEXT,
            graphics_quality TEXT,
            notes TEXT
        )
        """
    )

    connection.commit()

    # =========================================================
    # DEFAULT GAME PROFILES
    # =========================================================

    default_profiles = [
        (
            "Roblox",
            "1920x1080",
            "High",
            "Default Roblox profile"
        ),
        (
            "Valorant",
            "1920x1080",
            "Medium",
            "Competitive settings profile"
        ),
        (
            "GTA V",
            "1920x1080",
            "Medium",
            "Default GTA V profile"
        ),
        (
            "Minecraft",
            "1920x1080",
            "High",
            "Default Minecraft profile"
        )
    ]

    for profile in default_profiles:

        cursor.execute(
            """
            INSERT OR IGNORE INTO game_profiles (
                game_name,
                resolution,
                graphics_quality,
                notes
            )
            VALUES (?, ?, ?, ?)
            """,
            profile
        )

    connection.commit()
    connection.close()


def get_all_sessions():
    """Return all recorded gaming sessions."""

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT
            id,
            game_name,
            start_time,
            end_time,
            duration_seconds
        FROM sessions
        ORDER BY id DESC
        """
    )

    sessions = cursor.fetchall()

    connection.close()

    return sessions


def get_all_game_profiles():
    """Return all game profiles."""

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT
            id,
            game_name,
            resolution,
            graphics_quality,
            notes
        FROM game_profiles
        ORDER BY game_name ASC
        """
    )

    profiles = cursor.fetchall()

    connection.close()

    return profiles


def add_game_profile(
    game_name,
    resolution,
    graphics_quality,
    notes
):
    """Add a new game profile."""

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT INTO game_profiles (
            game_name,
            resolution,
            graphics_quality,
            notes
        )
        VALUES (?, ?, ?, ?)
        """,
        (
            game_name,
            resolution,
            graphics_quality,
            notes
        )
    )

    connection.commit()
    connection.close()


def delete_game_profile(profile_id):
    """Delete a game profile."""

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        DELETE FROM game_profiles
        WHERE id = ?
        """,
        (profile_id,)
    )

    connection.commit()
    connection.close()