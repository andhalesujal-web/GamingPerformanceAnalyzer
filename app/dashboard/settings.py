import customtkinter as ctk

from app.config.settings import (
    load_settings,
    save_settings
)


class SettingsWindow(ctk.CTkToplevel):

    def __init__(self, parent):
        super().__init__(parent)

        self.parent = parent

        self.title("Settings")
        self.geometry("600x500")
        self.minsize(500, 450)

        self.settings = load_settings()

        self.create_interface()
        self.load_current_settings()

    # =========================================================
    # INTERFACE
    # =========================================================

    def create_interface(self):

        title = ctk.CTkLabel(
            self,
            text="SETTINGS",
            font=ctk.CTkFont(
                size=28,
                weight="bold"
            )
        )

        title.pack(
            pady=(30, 25)
        )

        # =====================================================
        # MONITORING SETTINGS
        # =====================================================

        monitoring_frame = ctk.CTkFrame(
            self
        )

        monitoring_frame.pack(
            padx=30,
            pady=10,
            fill="x"
        )

        monitoring_title = ctk.CTkLabel(
            monitoring_frame,
            text="MONITORING",
            font=ctk.CTkFont(
                size=17,
                weight="bold"
            )
        )

        monitoring_title.pack(
            pady=(20, 10)
        )

        interval_label = ctk.CTkLabel(
            monitoring_frame,
            text="Monitoring interval"
        )

        interval_label.pack(
            pady=(5, 5)
        )

        self.interval_combo = ctk.CTkComboBox(
            monitoring_frame,
            values=[
                "1 second",
                "2 seconds",
                "3 seconds",
                "5 seconds",
                "10 seconds"
            ],
            width=220,
            state="readonly"
        )

        self.interval_combo.pack(
            pady=(0, 20)
        )

        # =====================================================
        # APPEARANCE SETTINGS
        # =====================================================

        appearance_frame = ctk.CTkFrame(
            self
        )

        appearance_frame.pack(
            padx=30,
            pady=10,
            fill="x"
        )

        appearance_title = ctk.CTkLabel(
            appearance_frame,
            text="APPEARANCE",
            font=ctk.CTkFont(
                size=17,
                weight="bold"
            )
        )

        appearance_title.pack(
            pady=(20, 10)
        )

        appearance_label = ctk.CTkLabel(
            appearance_frame,
            text="Appearance mode"
        )

        appearance_label.pack(
            pady=(5, 5)
        )

        self.appearance_combo = ctk.CTkComboBox(
            appearance_frame,
            values=[
                "Dark",
                "Light",
                "System"
            ],
            width=220,
            state="readonly"
        )

        self.appearance_combo.pack(
            pady=(0, 20)
        )

        # =====================================================
        # STATUS
        # =====================================================

        self.status_label = ctk.CTkLabel(
            self,
            text=""
        )

        self.status_label.pack(
            pady=(10, 5)
        )

        # =====================================================
        # SAVE BUTTON
        # =====================================================

        self.save_button = ctk.CTkButton(
            self,
            text="SAVE SETTINGS",
            command=self.save
        )

        self.save_button.pack(
            pady=(10, 20)
        )

    # =========================================================
    # LOAD CURRENT SETTINGS
    # =========================================================

    def load_current_settings(self):

        interval = self.settings.get(
            "monitoring_interval",
            2
        )

        appearance = self.settings.get(
            "appearance_mode",
            "dark"
        )

        # Interval

        interval_text = (
            f"{interval} second"
            if interval == 1
            else f"{interval} seconds"
        )

        self.interval_combo.set(
            interval_text
        )

        # Appearance

        self.appearance_combo.set(
            appearance.capitalize()
        )

    # =========================================================
    # SAVE SETTINGS
    # =========================================================

    def save(self):

        # =========================
        # INTERVAL
        # =========================

        interval_text = (
            self.interval_combo.get()
        )

        interval = int(
            interval_text.split()[0]
        )

        # =========================
        # APPEARANCE
        # =========================

        appearance = (
            self.appearance_combo.get()
            .lower()
        )

        # =========================
        # SAVE
        # =========================

        self.settings = {
            "monitoring_interval": interval,
            "appearance_mode": appearance
        }

        save_settings(
            self.settings
        )

        # Apply appearance immediately

        ctk.set_appearance_mode(
            appearance
        )

        # Tell dashboard about new interval

        if hasattr(
            self.parent,
            "apply_settings"
        ):

            self.parent.apply_settings()

        self.status_label.configure(
            text="Settings saved successfully."
        )