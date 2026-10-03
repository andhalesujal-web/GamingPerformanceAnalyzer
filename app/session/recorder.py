from datetime import datetime

from app.database.db import get_connection


class SessionRecorder:

    def __init__(self, game_name):
        self.game_name = game_name
        self.session_id = None
        self.start_time = None

    def start_session(self):
        """Create a new gaming session."""

        self.start_time = datetime.now()

        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute(
            """
            INSERT INTO sessions (
                game_name,
                start_time
            )
            VALUES (?, ?)
            """,
            (
                self.game_name,
                self.start_time.isoformat()
            )
        )

        self.session_id = cursor.lastrowid

        connection.commit()
        connection.close()

        print(f"Session started: {self.game_name}")
        print(f"Session ID: {self.session_id}")

    def record_sample(self, metrics):
        """Store one already-collected performance sample."""

        if self.session_id is None:
            raise RuntimeError("Session has not been started.")

        timestamp = datetime.now().isoformat()

        cpu_usage = metrics["cpu"]["usage_percent"]
        ram_usage = metrics["memory"]["usage_percent"]

        gpu_usage = None
        gpu_temperature = None
        gpu_memory_used = None

        if "error" not in metrics["gpu"]:
            gpu_usage = metrics["gpu"]["gpu_usage"]
            gpu_temperature = metrics["gpu"]["temperature"]
            gpu_memory_used = metrics["gpu"]["memory_used_mb"]

        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute(
            """
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
            """,
            (
                self.session_id,
                timestamp,
                cpu_usage,
                gpu_usage,
                ram_usage,
                gpu_temperature,
                gpu_memory_used
            )
        )

        connection.commit()
        connection.close()

        print(
            f"[{timestamp}] "
            f"CPU: {cpu_usage:.1f}% | "
            f"GPU: {gpu_usage if gpu_usage is not None else 'N/A'}% | "
            f"RAM: {ram_usage:.1f}%"
        )

    def end_session(self):
        """Finish the current gaming session."""

        if self.session_id is None:
            raise RuntimeError("Session has not been started.")

        end_time = datetime.now()

        duration = (
            end_time - self.start_time
        ).total_seconds()

        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute(
            """
            UPDATE sessions
            SET end_time = ?,
                duration_seconds = ?
            WHERE id = ?
            """,
            (
                end_time.isoformat(),
                duration,
                self.session_id
            )
        )

        connection.commit()
        connection.close()

        print()
        print("Session finished.")
        print(f"Duration: {duration:.1f} seconds")