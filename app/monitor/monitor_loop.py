import time
from datetime import datetime

from app.monitor.collector import collect_metrics


def start_monitoring(interval=2, duration=10):
    """Collect system metrics repeatedly for a fixed duration."""

    print("=== Monitoring Started ===")
    print(f"Sampling every {interval} seconds")
    print()

    start_time = time.time()

    while time.time() - start_time < duration:
        timestamp = datetime.now().strftime("%H:%M:%S")

        metrics = collect_metrics()

        cpu = metrics["cpu"]["usage_percent"]
        memory = metrics["memory"]["usage_percent"]

        if "error" not in metrics["gpu"]:
            gpu = metrics["gpu"]["gpu_usage"]
            temperature = metrics["gpu"]["temperature"]
        else:
            gpu = None
            temperature = None

        print(
            f"[{timestamp}] "
            f"CPU: {cpu:5.1f}% | "
            f"GPU: {gpu if gpu is not None else 'N/A':>5}% | "
            f"RAM: {memory:5.1f}% | "
            f"GPU Temp: {temperature if temperature is not None else 'N/A'}°C"
        )

        time.sleep(interval)

    print()
    print("=== Monitoring Finished ===")