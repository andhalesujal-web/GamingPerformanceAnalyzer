from app.database.db import get_connection


def get_session_metrics(session_id):
    """Calculate summary statistics for a gaming session."""

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT
            cpu_usage,
            gpu_usage,
            ram_usage,
            gpu_temperature,
            gpu_memory_used
        FROM metrics
        WHERE session_id = ?
        """,
        (session_id,)
    )

    rows = cursor.fetchall()
    connection.close()

    if not rows:
        raise ValueError(f"No metrics found for session {session_id}")

    cpu_values = [row[0] for row in rows]
    gpu_values = [row[1] for row in rows if row[1] is not None]
    ram_values = [row[2] for row in rows]
    temperature_values = [
        row[3] for row in rows
        if row[3] is not None
    ]
    memory_values = [
        row[4] for row in rows
        if row[4] is not None
    ]

    return {
        "sample_count": len(rows),

        "avg_cpu": sum(cpu_values) / len(cpu_values),
        "peak_cpu": max(cpu_values),

        "avg_gpu": (
            sum(gpu_values) / len(gpu_values)
            if gpu_values else None
        ),
        "peak_gpu": (
            max(gpu_values)
            if gpu_values else None
        ),

        "avg_ram": sum(ram_values) / len(ram_values),
        "peak_ram": max(ram_values),

        "avg_gpu_temperature": (
            sum(temperature_values) / len(temperature_values)
            if temperature_values else None
        ),
        "peak_gpu_temperature": (
            max(temperature_values)
            if temperature_values else None
        ),

        "avg_gpu_memory": (
            sum(memory_values) / len(memory_values)
            if memory_values else None
        ),
        "peak_gpu_memory": (
            max(memory_values)
            if memory_values else None
        ),
    }