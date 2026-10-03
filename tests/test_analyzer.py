from app.database.db import get_connection
from app.session.analyzer import get_session_metrics


def create_test_session():
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
        "Automated Test Game",
        "2026-01-01T10:00:00",
        "2026-01-01T10:10:00",
        600
    ))

    session_id = cursor.lastrowid

    test_metrics = [
        (50.0, 70.0, 60.0, 60.0, 1000.0),
        (80.0, 90.0, 75.0, 70.0, 2000.0),
        (60.0, 80.0, 65.0, 65.0, 1500.0),
    ]

    for cpu, gpu, ram, temperature, gpu_memory in test_metrics:
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
            "2026-01-01T10:00:00",
            cpu,
            gpu,
            ram,
            temperature,
            gpu_memory
        ))

    connection.commit()
    connection.close()

    return session_id


def test_session_metrics_analysis():
    session_id = create_test_session()

    result = get_session_metrics(session_id)

    assert result["sample_count"] == 3

    assert result["avg_cpu"] == 190 / 3
    assert result["peak_cpu"] == 80.0

    assert result["avg_gpu"] == 80.0
    assert result["peak_gpu"] == 90.0

    assert result["avg_ram"] == 200 / 3
    assert result["peak_ram"] == 75.0

    assert result["avg_gpu_temperature"] == 65.0
    assert result["peak_gpu_temperature"] == 70.0

    assert result["avg_gpu_memory"] == 1500.0
    assert result["peak_gpu_memory"] == 2000.0