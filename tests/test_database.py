from app.database.db import (
    initialize_database,
    get_all_sessions,
    get_all_game_profiles,
    add_game_profile,
    delete_game_profile,
)


def test_database_initialization():
    initialize_database()

    sessions = get_all_sessions()
    profiles = get_all_game_profiles()

    assert isinstance(sessions, list)
    assert isinstance(profiles, list)


def test_default_game_profiles_exist():
    initialize_database()

    profiles = get_all_game_profiles()

    game_names = [profile[1] for profile in profiles]

    assert "Valorant" in game_names
    assert "GTA V" in game_names
    assert "Minecraft" in game_names
    assert "Roblox" in game_names


def test_add_and_delete_game_profile():
    initialize_database()

    add_game_profile(
        "Test Game",
        "1920x1080",
        "Low",
        "Automated test profile"
    )

    profiles = get_all_game_profiles()

    test_profiles = [
        profile for profile in profiles
        if profile[1] == "Test Game"
    ]

    assert len(test_profiles) >= 1

    profile_id = test_profiles[-1][0]

    delete_game_profile(profile_id)

    profiles_after_delete = get_all_game_profiles()

    remaining = [
        profile for profile in profiles_after_delete
        if profile[0] == profile_id
    ]

    assert len(remaining) == 0