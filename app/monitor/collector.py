from app.monitor.cpu import get_cpu_usage, get_cpu_count
from app.monitor.gpu import initialize_gpu, shutdown_gpu, get_gpu_info
from app.monitor.memory import get_memory_info
from app.monitor.disk import get_disk_info
from app.monitor.network import get_network_info


def collect_metrics():
    """Collect a complete snapshot of system performance."""

    metrics = {
        "cpu": {},
        "gpu": {},
        "memory": {},
        "disk": {},
        "network": {},
    }

    # CPU
    metrics["cpu"] = {
        "usage_percent": get_cpu_usage(),
        "core_count": get_cpu_count(),
    }

    # GPU
    try:
        initialize_gpu()
        metrics["gpu"] = get_gpu_info()

    except Exception as error:
        metrics["gpu"] = {
            "error": str(error)
        }

    finally:
        try:
            shutdown_gpu()
        except Exception:
            pass

    # RAM
    metrics["memory"] = get_memory_info()

    # Disk
    metrics["disk"] = get_disk_info()

    # Network
    metrics["network"] = get_network_info()

    return metrics