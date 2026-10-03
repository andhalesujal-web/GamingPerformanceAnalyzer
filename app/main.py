from app.database.db import initialize_database
from app.dashboard.window import Dashboard


def main():
    initialize_database()

    app = Dashboard()
    app.mainloop()


if __name__ == "__main__":
    main()