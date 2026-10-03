from app.session.performance import analyze_performance


def main():
    session_id = 2

    result = analyze_performance(session_id)

    print("=== PERFORMANCE ANALYSIS ===")
    print()

    for finding in result["findings"]:
        print(f"- {finding}")


if __name__ == "__main__":
    main()