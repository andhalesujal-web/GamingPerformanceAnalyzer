from app.session.analyzer import get_session_metrics


def calculate_performance_score(session_id):
    """
    Calculate a performance score from recorded system metrics.

    The score is based on:
    - GPU utilization
    - CPU utilization
    - RAM usage
    - GPU temperature
    """

    metrics = get_session_metrics(session_id)

    score = 100.0

    # GPU utilization
    # High GPU utilization is not inherently bad,
    # so this component only penalizes extremely low
    # utilization when CPU utilization is also high.
    if (
        metrics["avg_gpu"] is not None
        and metrics["avg_cpu"] > 80
        and metrics["avg_gpu"] < 50
    ):
        score -= 15

    # RAM pressure
    if metrics["avg_ram"] >= 80:
        score -= 10

    if metrics["avg_ram"] >= 90:
        score -= 10

    # GPU temperature
    if (
        metrics["avg_gpu_temperature"] is not None
        and metrics["avg_gpu_temperature"] >= 80
    ):
        score -= 10

    if (
        metrics["peak_gpu_temperature"] is not None
        and metrics["peak_gpu_temperature"] >= 85
    ):
        score -= 10

    # Keep score within 0–100
    score = max(0, min(100, score))

    return round(score, 2)