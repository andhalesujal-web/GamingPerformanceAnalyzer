import customtkinter as ctk

from app.database.db import get_all_sessions


class SessionHistory(ctk.CTkToplevel):

    def __init__(self, parent):
        super().__init__(parent)

        self.title("Session History")
        self.geometry("850x550")
        self.minsize(750, 450)

        self.parent = parent

        self.create_interface()
        self.load_sessions()

    def create_interface(self):
        title = ctk.CTkLabel(
            self,
            text="SESSION HISTORY",
            font=ctk.CTkFont(
                size=26,
                weight="bold"
            )
        )

        title.pack(pady=(25, 15))

        self.scroll_frame = ctk.CTkScrollableFrame(
            self
        )

        self.scroll_frame.pack(
            padx=25,
            pady=10,
            fill="both",
            expand=True
        )

    def load_sessions(self):

        sessions = get_all_sessions()

        if not sessions:

            label = ctk.CTkLabel(
                self.scroll_frame,
                text="No gaming sessions recorded."
            )

            label.pack(pady=30)

            return

        headers = [
            "Game",
            "Duration",
            "Start Time"
        ]

        for column, header in enumerate(headers):

            label = ctk.CTkLabel(
                self.scroll_frame,
                text=header,
                font=ctk.CTkFont(
                    size=15,
                    weight="bold"
                )
            )

            label.grid(
                row=0,
                column=column,
                padx=20,
                pady=15,
                sticky="w"
            )

        for row_index, session in enumerate(
            sessions,
            start=1
        ):

            session_id = session[0]
            game_name = session[1]
            start_time = session[2]
            duration = session[4]

            duration_text = (
                f"{duration:.1f} sec"
                if duration is not None
                else "Active"
            )

            start_text = start_time.replace("T", " ")[:19]

            values = [
                game_name,
                duration_text,
                start_text
            ]

            for column, value in enumerate(values):

                label = ctk.CTkLabel(
                    self.scroll_frame,
                    text=str(value)
                )

                label.grid(
                    row=row_index,
                    column=column,
                    padx=20,
                    pady=10,
                    sticky="w"
                )

            view_button = ctk.CTkButton(
                self.scroll_frame,
                text="View",
                width=80,
                command=lambda sid=session_id:
                    self.view_session(sid)
            )

            view_button.grid(
                row=row_index,
                column=3,
                padx=20,
                pady=10
            )

    def view_session(self, session_id):

        self.parent.open_session_analysis(
            session_id
        )