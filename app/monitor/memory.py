import psutil


def get_memory_info():
    """Return current RAM usage information."""
    memory = psutil.virtual_memory()

    return {
        "total_gb": memory.total / (1024 ** 3),
        "used_gb": memory.used / (1024 ** 3),
        "available_gb": memory.available / (1024 ** 3),
        "usage_percent": memory.percent,
    }