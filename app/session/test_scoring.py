from app.session.scoring import calculate_performance_score


def main():
    session_id = 2

    score = calculate_performance_score(session_id)

    print("=== PERFORMANCE SCORE ===")
    print()
    print(f"Score: {score}/100")


if __name__ == "__main__":
    main()