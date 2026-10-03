import psutil


def get_disk_info():
    """Return current disk usage information."""
    disk = psutil.disk_usage("/")

    return {
        "total_gb": disk.total / (1024 ** 3),
        "used_gb": disk.used / (1024 ** 3),
        "free_gb": disk.free / (1024 ** 3),
        "usage_percent": disk.percent,
    }