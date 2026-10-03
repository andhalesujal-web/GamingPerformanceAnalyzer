import psutil


def initialize_cpu_monitor():
    """Initialize CPU monitoring."""
    psutil.cpu_percent(interval=None)


def get_cpu_usage():
    """Return current CPU usage percentage."""
    return psutil.cpu_percent(interval=None)


def get_cpu_count():
    """Return the number of logical CPU cores."""
    return psutil.cpu_count(logical=True)