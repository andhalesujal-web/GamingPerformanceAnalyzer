from app.database.db import get_connection


def check_database():
    connection = get_connection()
    cursor = connection.cursor()

    print("=== Sessions ===")

    cursor.execute("""
        SELECT id, game_name, start_time, end_time, duration_seconds
        FROM sessions
    """)

    sessions = cursor.fetchall()

    for session in sessions:
        print(session)

    print()
    print("=== Metrics ===")

    cursor.execute("""
        SELECT
            session_id,
            timestamp,
            cpu_usage,
            gpu_usage,
            ram_usage,
            gpu_temperature,
            gpu_memory_used
        FROM metrics
    """)

    metrics = cursor.fetchall()

    for metric in metrics:
        print(metric)

    connection.close()


if __name__ == "__main__":
    check_database()