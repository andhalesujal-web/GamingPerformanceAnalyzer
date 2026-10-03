from app.session.analyzer import get_session_metrics


def main():
    session_id = 2

    results = get_session_metrics(session_id)

    print("=== SESSION ANALYSIS ===")
    print()

    print(f"Samples           : {results['sample_count']}")

    print(f"Average CPU       : {results['avg_cpu']:.2f}%")
    print(f"Peak CPU          : {results['peak_cpu']:.2f}%")

    print(f"Average GPU       : {results['avg_gpu']:.2f}%")
    print(f"Peak GPU          : {results['peak_gpu']:.2f}%")

    print(f"Average RAM       : {results['avg_ram']:.2f}%")
    print(f"Peak RAM          : {results['peak_ram']:.2f}%")

    print(
        f"Average GPU Temp  : "
        f"{results['avg_gpu_temperature']:.2f}°C"
    )

    print(
        f"Peak GPU Temp     : "
        f"{results['peak_gpu_temperature']:.2f}°C"
    )

    print(
        f"Average VRAM      : "
        f"{results['avg_gpu_memory']:.2f} MB"
    )

    print(
        f"Peak VRAM         : "
        f"{results['peak_gpu_memory']:.2f} MB"
    )


if __name__ == "__main__":
    main()