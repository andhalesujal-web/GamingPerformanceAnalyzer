import customtkinter as ctk

from app.database.db import get_all_sessions
from app.session.scoring import calculate_performance_score


class SessionHistory(ctk.CTkToplevel):
    """Display recorded gaming sessions and open their analysis."""

    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent

        self.title("Session History")
        self.geometry("1000x650")
        self.minsize(850, 500)
        self.configure(fg_color="#080B12")

        self.create_interface()
        self.load_sessions()

    def create_interface(self):
        header = ctk.CTkFrame(self, fg_color="#0D111A", corner_radius=0)
        header.pack(fill="x")

        title = ctk.CTkLabel(
            header,
            text="SESSION HISTORY",
            font=ctk.CTkFont(size=26, weight="bold"),
            text_color="#FFFFFF",
        )
        title.pack(side="left", padx=30, pady=(22, 5))

        refresh_button = ctk.CTkButton(
            header,
            text="⟳  Refresh",
            width=110,
            height=34,
            corner_radius=8,
            fg_color="#151C2A",
            hover_color="#202A3D",
            command=self.refresh_sessions,
        )
        refresh_button.pack(side="right", padx=30, pady=20)

        subtitle = ctk.CTkLabel(
            self,
            text="Review your previous gaming sessions and performance",
            font=ctk.CTkFont(size=13),
            text_color="#7F8CA3",
        )
        subtitle.pack(anchor="w", padx=30, pady=(12, 15))

        self.scroll_frame = ctk.CTkScrollableFrame(
            self, fg_color="#080B12", corner_radius=0
        )
        self.scroll_frame.pack(
            padx=20, pady=(0, 20), fill="both", expand=True
        )

    def load_sessions(self):
        for widget in self.scroll_frame.winfo_children():
            widget.destroy()

        sessions = get_all_sessions()
        if not sessions:
            empty_frame = ctk.CTkFrame(
                self.scroll_frame, fg_color="#10151F", corner_radius=14
            )
            empty_frame.pack(fill="x", padx=10, pady=30)
            ctk.CTkLabel(
                empty_frame,
                text="No gaming sessions recorded yet.",
                font=ctk.CTkFont(size=16, weight="bold"),
                text_color="#FFFFFF",
            ).pack(pady=(25, 5))
            ctk.CTkLabel(
                empty_frame,
                text="Start a gaming session from the dashboard.",
                font=ctk.CTkFont(size=13),
                text_color="#7F8CA3",
            ).pack(pady=(0, 25))
            return

        header = ctk.CTkFrame(
            self.scroll_frame, fg_color="#111722", corner_radius=10, height=45
        )
        header.pack(fill="x", padx=5, pady=(0, 10))
        for column, weight in enumerate((2, 2, 1, 1, 1)):
            header.grid_columnconfigure(column, weight=weight)

        for column, label in enumerate(
            ("GAME", "DATE & TIME", "DURATION", "SCORE", "ACTION")
        ):
            self.create_header_label(header, label, column)

        for session in sessions:
            # get_all_sessions() rows: id, game_name, start_time, end_time, duration
            session_id, game_name, start_time = session[0], session[1], session[2]
            duration = session[4] if len(session) > 4 else None
            duration_text = self.format_duration(duration)
            start_text = self.format_datetime(start_time)

            # calculate_performance_score returns a numeric score, not a dict.
            try:
                score = calculate_performance_score(session_id)
                score = float(score) if score is not None else None
            except Exception as error:
                print(f"Performance score error for session {session_id}: {error}")
                score = None

            card = ctk.CTkFrame(
                self.scroll_frame,
                fg_color="#0F141E",
                corner_radius=12,
                border_width=1,
                border_color="#1B2433",
            )
            card.pack(fill="x", padx=5, pady=5)
            for column, weight in enumerate((2, 2, 1, 1, 1)):
                card.grid_columnconfigure(column, weight=weight)

            ctk.CTkLabel(
                card,
                text=f"🎮  {game_name}",
                font=ctk.CTkFont(size=14, weight="bold"),
                text_color="#FFFFFF",
                anchor="w",
            ).grid(row=0, column=0, padx=18, pady=16, sticky="w")

            ctk.CTkLabel(
                card,
                text=start_text,
                font=ctk.CTkFont(size=12),
                text_color="#AAB4C5",
                anchor="w",
            ).grid(row=0, column=1, padx=10, pady=16, sticky="w")

            ctk.CTkLabel(
                card,
                text=duration_text,
                font=ctk.CTkFont(size=12, weight="bold"),
                text_color="#AAB4C5",
            ).grid(row=0, column=2, padx=10, pady=16)

            score_text = f"{score:.0f}/100" if score is not None else "N/A"
            ctk.CTkLabel(
                card,
                text=score_text,
                font=ctk.CTkFont(size=13, weight="bold"),
                text_color=self.get_score_color(score) if score is not None else "#7F8CA3",
            ).grid(row=0, column=3, padx=10, pady=16)

            ctk.CTkButton(
                card,
                text="View Analysis",
                width=115,
                height=32,
                corner_radius=8,
                fg_color="#151F31",
                hover_color="#24344F",
                command=lambda sid=session_id: self.view_session(sid),
            ).grid(row=0, column=4, padx=12, pady=12)

    def create_header_label(self, parent, text, column):
        ctk.CTkLabel(
            parent,
            text=text,
            font=ctk.CTkFont(size=11, weight="bold"),
            text_color="#69778E",
            anchor="w",
        ).grid(row=0, column=column, padx=18, pady=12, sticky="w")

    @staticmethod
    def format_duration(duration):
        if duration is None:
            return "Active"
        try:
            duration = float(duration)
        except (TypeError, ValueError):
            return "Unknown"
        if duration < 60:
            return f"{duration:.0f}s"
        minutes, seconds = int(duration // 60), int(duration % 60)
        if minutes < 60:
            return f"{minutes}m {seconds}s"
        return f"{minutes // 60}h {minutes % 60}m"

    @staticmethod
    def format_datetime(start_time):
        if not start_time:
            return "Unknown"
        try:
            return start_time.replace("T", " ")[:19]
        except (AttributeError, TypeError):
            return str(start_time)

    @staticmethod
    def get_score_color(score):
        if score >= 80:
            return "#3DDC97"
        if score >= 60:
            return "#F5C451"
        if score >= 40:
            return "#FF9F43"
        return "#FF5C5C"

    def refresh_sessions(self):
        self.load_sessions()

    def view_session(self, session_id):
        try:
            self.parent.open_session_analysis(session_id)
        except Exception as error:
            print(f"Unable to open session analysis: {error}")
