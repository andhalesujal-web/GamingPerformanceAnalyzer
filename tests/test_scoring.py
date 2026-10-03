from app.database.db import get_connection
from app.session.scoring import calculate_performance_score


def create_scoring_test_session():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO sessions (
            game_name,
            start_time,
            end_time,
            duration_seconds
        )
        VALUES (?, ?, ?, ?)
    """, (
        "Scoring Test Game",
        "2026-01-01T12:00:00",
        "2026-01-01T12:10:00",
        600
    ))

    session_id = cursor.lastrowid

    cursor.execute("""
        INSERT INTO metrics (
            session_id,
            timestamp,
            cpu_usage,
            gpu_usage,
            ram_usage,
            gpu_temperature,
            gpu_memory_used
        )
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        session_id,
        "2026-01-01T12:05:00",
        90.0,
        70.0,
        85.0,
        85.0,
        3000.0
    ))

    connection.commit()
    connection.close()

    return session_id


def test_performance_score():
    session_id = create_scoring_test_session()

    score = calculate_performance_score(session_id)

    assert isinstance(score, (int, float))
    assert 0 <= score <= 100