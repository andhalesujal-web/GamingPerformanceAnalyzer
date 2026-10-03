from app.session.analyzer import get_session_metrics


def analyze_session_performance(session_id):
    metrics = get_session_metrics(session_id)

    findings = []
    recommendations = []

    # CPU analysis
    if metrics["avg_cpu"] >= 85:
        findings.append(
            f"High CPU utilization detected. "
            f"Average CPU usage was {metrics['avg_cpu']:.1f}%."
        )
        recommendations.append(
            "Close unnecessary background applications to reduce CPU load."
        )

    elif metrics["peak_cpu"] >= 90:
        findings.append(
            f"CPU usage reached a high peak of {metrics['peak_cpu']:.1f}%."
        )
        recommendations.append(
            "Monitor background processes if high CPU peaks occur frequently."
        )

    # GPU analysis
    if metrics["avg_gpu"] is not None:
        if metrics["avg_gpu"] >= 85:
            findings.append(
                f"High GPU utilization detected. "
                f"Average GPU usage was {metrics['avg_gpu']:.1f}%."
            )
            recommendations.append(
                "High GPU utilization can be normal during gaming. "
                "Check temperatures and performance stability."
            )

        elif metrics["avg_gpu"] < 50 and metrics["avg_cpu"] < 50:
            findings.append(
                "Both CPU and GPU utilization were relatively low."
            )
            recommendations.append(
                "The recorded workload appears light. "
                "Check whether the game was actively running during the session."
            )

    # RAM analysis
    if metrics["peak_ram"] >= 90:
        findings.append(
            f"Very high RAM usage detected. "
            f"Peak RAM usage was {metrics['peak_ram']:.1f}%."
        )
        recommendations.append(
            "Close unnecessary applications or consider increasing system RAM."
        )

    elif metrics["peak_ram"] >= 80:
        findings.append(
            f"High RAM usage detected. "
            f"Peak RAM usage was {metrics['peak_ram']:.1f}%."
        )
        recommendations.append(
            "Close unnecessary background applications to free RAM."
        )

    # GPU temperature analysis
    if metrics["peak_gpu_temperature"] is not None:
        temperature = metrics["peak_gpu_temperature"]

        if temperature >= 90:
            findings.append(
                f"Very high GPU temperature detected. "
                f"Peak temperature was {temperature:.1f}°C."
            )
            recommendations.append(
                "Improve GPU cooling, clean dust from the system, "
                "and check airflow."
            )

        elif temperature >= 85:
            findings.append(
                f"High GPU temperature detected. "
                f"Peak temperature was {temperature:.1f}°C."
            )
            recommendations.append(
                "Monitor GPU temperature and improve airflow if necessary."
            )

        elif temperature >= 80:
            findings.append(
                f"Elevated GPU temperature detected. "
                f"Peak temperature was {temperature:.1f}°C."
            )
            recommendations.append(
                "Keep the laptop or PC well ventilated during gaming."
            )

    # Balanced workload
    if (
        metrics["avg_cpu"] < 80
        and (metrics["avg_gpu"] is None or metrics["avg_gpu"] < 80)
        and metrics["peak_ram"] < 85
        and (
            metrics["peak_gpu_temperature"] is None
            or metrics["peak_gpu_temperature"] < 85
        )
    ):
        findings.append(
            "Overall system utilization remained within a balanced range."
        )

        recommendations.append(
            "Continue monitoring performance during longer gaming sessions."
        )

    # Fallback
    if not findings:
        findings.append(
            "No major performance issues were detected during this session."
        )

    if not recommendations:
        recommendations.append(
            "System performance appears stable based on the recorded metrics."
        )

    return {
        "findings": findings,
        "recommendations": recommendations,
    }