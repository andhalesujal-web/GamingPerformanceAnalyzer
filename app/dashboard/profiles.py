import customtkinter as ctk

from app.database.db import (
    get_all_game_profiles,
    add_game_profile,
    delete_game_profile
)


class GameProfiles(ctk.CTkToplevel):

    def __init__(self, parent):
        super().__init__(parent)

        self.parent = parent

        self.title("Game Profiles")
        self.geometry("900x650")
        self.minsize(800, 550)

        self.create_interface()
        self.load_profiles()

    # =========================================================
    # INTERFACE
    # =========================================================

    def create_interface(self):

        title = ctk.CTkLabel(
            self,
            text="GAME PROFILES",
            font=ctk.CTkFont(
                size=28,
                weight="bold"
            )
        )

        title.pack(
            pady=(25, 15)
        )

        # =====================================================
        # ADD PROFILE FORM
        # =====================================================

        self.form_frame = ctk.CTkFrame(
            self
        )

        self.form_frame.pack(
            padx=25,
            pady=10,
            fill="x"
        )

        # Game name

        self.game_entry = ctk.CTkEntry(
            self.form_frame,
            placeholder_text="Game name",
            width=180
        )

        self.game_entry.grid(
            row=0,
            column=0,
            padx=10,
            pady=15
        )

        # Resolution

        self.resolution_entry = ctk.CTkEntry(
            self.form_frame,
            placeholder_text="Resolution",
            width=160
        )

        self.resolution_entry.grid(
            row=0,
            column=1,
            padx=10,
            pady=15
        )

        # Graphics quality

        self.graphics_entry = ctk.CTkEntry(
            self.form_frame,
            placeholder_text="Graphics quality",
            width=160
        )

        self.graphics_entry.grid(
            row=0,
            column=2,
            padx=10,
            pady=15
        )

        # Add button

        self.add_button = ctk.CTkButton(
            self.form_frame,
            text="ADD PROFILE",
            command=self.add_profile,
            width=130
        )

        self.add_button.grid(
            row=0,
            column=3,
            padx=10,
            pady=15
        )

        # =====================================================
        # STATUS
        # =====================================================

        self.status_label = ctk.CTkLabel(
            self,
            text="Create or manage your game profiles."
        )

        self.status_label.pack(
            pady=(5, 10)
        )

        # =====================================================
        # PROFILE LIST
        # =====================================================

        self.profile_frame = ctk.CTkScrollableFrame(
            self
        )

        self.profile_frame.pack(
            padx=25,
            pady=10,
            fill="both",
            expand=True
        )

    # =========================================================
    # LOAD PROFILES
    # =========================================================

    def load_profiles(self):

        # Clear old widgets

        for widget in self.profile_frame.winfo_children():
            widget.destroy()

        try:

            profiles = get_all_game_profiles()

        except Exception as error:

            self.status_label.configure(
                text=f"Database error: {error}"
            )

            return

        if not profiles:

            label = ctk.CTkLabel(
                self.profile_frame,
                text="No game profiles found."
            )

            label.pack(
                pady=30
            )

            return

        # =====================================================
        # HEADERS
        # =====================================================

        headers = [
            "Game",
            "Resolution",
            "Graphics",
            "Notes",
            "Action"
        ]

        for column, header in enumerate(headers):

            label = ctk.CTkLabel(
                self.profile_frame,
                text=header,
                font=ctk.CTkFont(
                    size=14,
                    weight="bold"
                )
            )

            label.grid(
                row=0,
                column=column,
                padx=10,
                pady=12,
                sticky="w"
            )

        # =====================================================
        # PROFILE ROWS
        # =====================================================

        for row_index, profile in enumerate(
            profiles,
            start=1
        ):

            profile_id = profile[0]
            game_name = profile[1]
            resolution = profile[2]
            graphics_quality = profile[3]
            notes = profile[4]

            values = [
                game_name,
                resolution or "N/A",
                graphics_quality or "N/A",
                notes or "N/A"
            ]

            for column, value in enumerate(values):

                label = ctk.CTkLabel(
                    self.profile_frame,
                    text=str(value)
                )

                label.grid(
                    row=row_index,
                    column=column,
                    padx=10,
                    pady=10,
                    sticky="w"
                )

            delete_button = ctk.CTkButton(
                self.profile_frame,
                text="Delete",
                width=75,
                command=lambda pid=profile_id:
                    self.delete_profile(pid)
            )

            delete_button.grid(
                row=row_index,
                column=4,
                padx=10,
                pady=10
            )

    # =========================================================
    # ADD PROFILE
    # =========================================================

    def add_profile(self):

        game_name = self.game_entry.get().strip()
        resolution = self.resolution_entry.get().strip()
        graphics_quality = self.graphics_entry.get().strip()

        if not game_name:

            self.status_label.configure(
                text="Enter a game name."
            )

            return

        if not resolution:
            resolution = "Not specified"

        if not graphics_quality:
            graphics_quality = "Not specified"

        try:

            add_game_profile(
                game_name,
                resolution,
                graphics_quality,
                "Custom game profile"
            )

            # Clear form

            self.game_entry.delete(
                0,
                "end"
            )

            self.resolution_entry.delete(
                0,
                "end"
            )

            self.graphics_entry.delete(
                0,
                "end"
            )

            self.status_label.configure(
                text=f"Profile added: {game_name}"
            )

            self.load_profiles()

            if hasattr(self.parent, "refresh_game_profiles"):
                 self.parent.refresh_game_profiles()

        except Exception as error:

            self.status_label.configure(
                text=f"Profile error: {error}"
            )

    # =========================================================
    # DELETE PROFILE
    # =========================================================

    def delete_profile(
        self,
        profile_id
    ):

        try:

            delete_game_profile(
                profile_id
            )

            self.status_label.configure(
                text="Profile deleted."
            )

            self.load_profiles()

            if hasattr(self.parent, "refresh_game_profiles"):
                self.parent.refresh_game_profiles()

        except Exception as error:

            self.status_label.configure(
                text=f"Delete error: {error}"
            )