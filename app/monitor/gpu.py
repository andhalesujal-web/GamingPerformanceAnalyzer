import pynvml


def initialize_gpu():
    """Initialize NVIDIA Management Library."""
    pynvml.nvmlInit()


def shutdown_gpu():
    """Shutdown NVIDIA Management Library."""
    pynvml.nvmlShutdown()


def get_gpu_info():
    """Return basic information about the first NVIDIA GPU."""
    handle = pynvml.nvmlDeviceGetHandleByIndex(0)

    name = pynvml.nvmlDeviceGetName(handle)

    if isinstance(name, bytes):
        name = name.decode("utf-8")

    utilization = pynvml.nvmlDeviceGetUtilizationRates(handle)
    memory = pynvml.nvmlDeviceGetMemoryInfo(handle)
    temperature = pynvml.nvmlDeviceGetTemperature(
        handle,
        pynvml.NVML_TEMPERATURE_GPU
    )

    return {
        "name": name,
        "gpu_usage": utilization.gpu,
        "memory_used_mb": memory.used / (1024 ** 2),
        "memory_total_mb": memory.total / (1024 ** 2),
        "temperature": temperature,
    }