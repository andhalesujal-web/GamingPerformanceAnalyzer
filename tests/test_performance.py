from app.database.db import get_connection
from app.session.performance import analyze_session_performance


def create_performance_test_session():
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
        "Performance Test Game",
        "2026-01-01T11:00:00",
        "2026-01-01T11:10:00",
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
        "2026-01-01T11:05:00",
        95.0,
        60.0,
        85.0,
        90.0,
        3000.0
    ))

    connection.commit()
    connection.close()

    return session_id


def test_performance_analysis():
    session_id = create_performance_test_session()

    result = analyze_session_performance(session_id)

    assert "findings" in result
    assert "recommendations" in result

    assert isinstance(result["findings"], list)
    assert isinstance(result["recommendations"], list)

    assert len(result["findings"]) > 0
    assert len(result["recommendations"]) > 0