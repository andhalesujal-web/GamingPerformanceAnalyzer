import customtkinter as ctk

from app.monitor.collector import collect_metrics
from app.session.recorder import SessionRecorder
from app.database.db import get_all_game_profiles
from app.config.settings import load_settings


class Dashboard(ctk.CTk):

    def __init__(self):
        super().__init__()

        self.title("Gaming Performance Analyzer")
        self.geometry("1000x700")
        self.minsize(900, 650)

        # =====================================================
        # APPLICATION STATE
        # =====================================================

        self.recorder = None
        self.session_active = False
        self.update_job = None
        self.closing = False

        # =====================================================
        # LOAD SETTINGS
        # =====================================================

        self.settings = load_settings()

        self.monitoring_interval = self.settings.get(
            "monitoring_interval",
            2
        )

        ctk.set_appearance_mode(
            self.settings.get(
                "appearance_mode",
                "dark"
            )
        )

        ctk.set_default_color_theme(
            "blue"
        )

        # =====================================================
        # CREATE APPLICATION
        # =====================================================

        self.create_interface()

        self.load_game_profiles()

        self.update_metrics()

        self.protocol(
            "WM_DELETE_WINDOW",
            self.close_application
        )

    # =========================================================
    # INTERFACE
    # =========================================================

    def create_interface(self):

        # =====================================================
        # TITLE
        # =====================================================

        title = ctk.CTkLabel(
            self,
            text="GAMING PERFORMANCE ANALYZER",
            font=ctk.CTkFont(
                size=28,
                weight="bold"
            )
        )

        title.pack(
            pady=(25, 5)
        )

        subtitle = ctk.CTkLabel(
            self,
            text="Live Hardware Monitor",
            font=ctk.CTkFont(
                size=15
            )
        )

        subtitle.pack(
            pady=(0, 20)
        )

        # =====================================================
        # METRICS FRAME
        # =====================================================

        self.metrics_frame = ctk.CTkFrame(
            self
        )

        self.metrics_frame.pack(
            padx=30,
            pady=10,
            fill="both",
            expand=True
        )

        # CPU

        self.cpu_label = self.create_metric(
            self.metrics_frame,
            "CPU",
            0,
            0
        )

        # GPU

        self.gpu_label = self.create_metric(
            self.metrics_frame,
            "GPU",
            0,
            1
        )

        # RAM

        self.ram_label = self.create_metric(
            self.metrics_frame,
            "RAM",
            0,
            2
        )

        # GPU Temperature

        self.temp_label = self.create_metric(
            self.metrics_frame,
            "GPU TEMP",
            1,
            0
        )

        # VRAM

        self.vram_label = self.create_metric(
            self.metrics_frame,
            "VRAM",
            1,
            1
        )

        # Disk

        self.disk_label = self.create_metric(
            self.metrics_frame,
            "DISK",
            1,
            2
        )

        # =====================================================
        # SESSION FRAME
        # =====================================================

        self.session_frame = ctk.CTkFrame(
            self
        )

        self.session_frame.pack(
            padx=30,
            pady=(10, 5),
            fill="x"
        )

        # =====================================================
        # GAME PROFILE DROPDOWN
        # =====================================================

        self.game_combo = ctk.CTkComboBox(
            self.session_frame,
            values=[
                "No profiles available"
            ],
            width=250,
            state="readonly"
        )

        self.game_combo.grid(
            row=0,
            column=0,
            padx=15,
            pady=15
        )

        # =====================================================
        # START SESSION
        # =====================================================

        self.start_button = ctk.CTkButton(
            self.session_frame,
            text="START SESSION",
            command=self.start_session
        )

        self.start_button.grid(
            row=0,
            column=1,
            padx=10,
            pady=15
        )

        # =====================================================
        # STOP SESSION
        # =====================================================

        self.stop_button = ctk.CTkButton(
            self.session_frame,
            text="STOP SESSION",
            command=self.stop_session,
            state="disabled"
        )

        self.stop_button.grid(
            row=0,
            column=2,
            padx=10,
            pady=15
        )

        # =====================================================
        # SESSION HISTORY
        # =====================================================

        self.history_button = ctk.CTkButton(
            self,
            text="SESSION HISTORY",
            command=self.open_history
        )

        self.history_button.pack(
            pady=(5, 8)
        )

        # =====================================================
        # GAME PROFILES
        # =====================================================

        self.profile_button = ctk.CTkButton(
            self,
            text="GAME PROFILES",
            command=self.open_game_profiles
        )

        self.profile_button.pack(
            pady=(0, 8)
        )

        # =====================================================
        # SETTINGS
        # =====================================================

        self.settings_button = ctk.CTkButton(
            self,
            text="SETTINGS",
            command=self.open_settings
        )

        self.settings_button.pack(
            pady=(0, 10)
        )

        # =====================================================
        # STATUS
        # =====================================================

        self.status_label = ctk.CTkLabel(
            self,
            text="● Monitoring",
            font=ctk.CTkFont(
                size=14
            )
        )

        self.status_label.pack(
            pady=(5, 20)
        )

    # =========================================================
    # LOAD GAME PROFILES
    # =========================================================

    def load_game_profiles(self):

        try:

            profiles = get_all_game_profiles()

            if profiles:

                game_names = [
                    profile[1]
                    for profile in profiles
                ]

                self.game_combo.configure(
                    values=game_names
                )

                current_game = self.game_combo.get()

                if current_game in game_names:

                    self.game_combo.set(
                        current_game
                    )

                else:

                    self.game_combo.set(
                        game_names[0]
                    )

            else:

                self.game_combo.configure(
                    values=[
                        "No profiles available"
                    ]
                )

                self.game_combo.set(
                    "No profiles available"
                )

        except Exception as error:

            self.game_combo.configure(
                values=[
                    "Database error"
                ]
            )

            self.game_combo.set(
                "Database error"
            )

            if hasattr(
                self,
                "status_label"
            ):

                self.status_label.configure(
                    text=f"Profile error: {error}"
                )

    # =========================================================
    # REFRESH GAME PROFILES
    # =========================================================

    def refresh_game_profiles(self):

        self.load_game_profiles()

    # =========================================================
    # CREATE METRIC CARD
    # =========================================================

    def create_metric(
        self,
        parent,
        name,
        row,
        column
    ):

        card = ctk.CTkFrame(
            parent
        )

        card.grid(
            row=row,
            column=column,
            padx=15,
            pady=15,
            sticky="nsew"
        )

        parent.grid_columnconfigure(
            column,
            weight=1
        )

        parent.grid_rowconfigure(
            row,
            weight=1
        )

        title = ctk.CTkLabel(
            card,
            text=name,
            font=ctk.CTkFont(
                size=16,
                weight="bold"
            )
        )

        title.pack(
            pady=(25, 10)
        )

        value = ctk.CTkLabel(
            card,
            text="--",
            font=ctk.CTkFont(
                size=30,
                weight="bold"
            )
        )

        value.pack(
            pady=(0, 25)
        )

        return value

    # =========================================================
    # START SESSION
    # =========================================================

    def start_session(self):

        game_name = self.game_combo.get().strip()

        if not game_name:

            self.status_label.configure(
                text="Select a game first."
            )

            return

        if game_name in (
            "No profiles available",
            "Database error"
        ):

            self.status_label.configure(
                text="Create a game profile first."
            )

            return

        if self.session_active:
            return

        try:

            self.recorder = SessionRecorder(
                game_name
            )

            self.recorder.start_session()

            self.session_active = True

            self.start_button.configure(
                state="disabled"
            )

            self.stop_button.configure(
                state="normal"
            )

            self.game_combo.configure(
                state="disabled"
            )

            self.status_label.configure(
                text=f"● Recording: {game_name}"
            )

        except Exception as error:

            self.status_label.configure(
                text=f"Session error: {error}"
            )

    # =========================================================
    # STOP SESSION
    # =========================================================

    def stop_session(self):

        if not self.session_active:
            return

        try:

            self.recorder.end_session()

            self.session_active = False
            self.recorder = None

            self.start_button.configure(
                state="normal"
            )

            self.stop_button.configure(
                state="disabled"
            )

            self.game_combo.configure(
                state="readonly"
            )

            self.status_label.configure(
                text="● Monitoring"
            )

        except Exception as error:

            self.status_label.configure(
                text=f"Session error: {error}"
            )

    # =========================================================
    # LIVE MONITORING
    # =========================================================

    def update_metrics(self):

        if self.closing:
            return

        try:

            metrics = collect_metrics()

            cpu = metrics["cpu"]
            memory = metrics["memory"]
            disk = metrics["disk"]
            gpu = metrics["gpu"]

            # =================================================
            # CPU
            # =================================================

            self.cpu_label.configure(
                text=f"{cpu['usage_percent']:.1f}%"
            )

            # =================================================
            # RAM
            # =================================================

            self.ram_label.configure(
                text=f"{memory['usage_percent']:.1f}%"
            )

            # =================================================
            # DISK
            # =================================================

            self.disk_label.configure(
                text=f"{disk['usage_percent']:.1f}%"
            )

            # =================================================
            # GPU
            # =================================================

            if "error" not in gpu:

                self.gpu_label.configure(
                    text=f"{gpu['gpu_usage']}%"
                )

                self.temp_label.configure(
                    text=f"{gpu['temperature']}°C"
                )

                self.vram_label.configure(
                    text=(
                        f"{gpu['memory_used_mb']:.0f} / "
                        f"{gpu['memory_total_mb']:.0f} MB"
                    )
                )

            else:

                self.gpu_label.configure(
                    text="N/A"
                )

                self.temp_label.configure(
                    text="N/A"
                )

                self.vram_label.configure(
                    text="N/A"
                )

            # =================================================
            # RECORD SESSION SAMPLE
            # =================================================

            if (
                self.session_active
                and self.recorder
            ):

                self.recorder.record_sample(
                    metrics
                )

        except Exception as error:

            if not self.closing:

                try:

                    self.status_label.configure(
                        text=f"Monitoring error: {error}"
                    )

                except Exception:
                    pass

        # =====================================================
        # NEXT UPDATE
        # =====================================================

        if not self.closing:

            try:

                self.update_job = self.after(
                    self.monitoring_interval * 1000,
                    self.update_metrics
                )

            except Exception:

                self.update_job = None

    # =========================================================
    # SESSION HISTORY
    # =========================================================

    def open_history(self):

        from app.dashboard.history import SessionHistory

        SessionHistory(
            self
        )

    # =========================================================
    # GAME PROFILES
    # =========================================================

    def open_game_profiles(self):

        from app.dashboard.profiles import GameProfiles

        profile_window = GameProfiles(
            self
        )

        profile_window.protocol(
            "WM_DELETE_WINDOW",
            lambda: self.close_profiles_window(
                profile_window
            )
        )

    # =========================================================
    # CLOSE PROFILE WINDOW
    # =========================================================

    def close_profiles_window(
        self,
        profile_window
    ):

        try:

            profile_window.destroy()

        except Exception:
            pass

        self.refresh_game_profiles()

    # =========================================================
    # SETTINGS
    # =========================================================

    def open_settings(self):

        from app.dashboard.settings import SettingsWindow

        settings_window = SettingsWindow(
            self
        )

        settings_window.protocol(
            "WM_DELETE_WINDOW",
            lambda: settings_window.destroy()
        )

    # =========================================================
    # APPLY SETTINGS
    # =========================================================

    def apply_settings(self):

        self.settings = load_settings()

        self.monitoring_interval = (
            self.settings.get(
                "monitoring_interval",
                2
            )
        )

        ctk.set_appearance_mode(
            self.settings.get(
                "appearance_mode",
                "dark"
            )
        )

    # =========================================================
    # SESSION ANALYSIS
    # =========================================================

    def open_session_analysis(
        self,
        session_id
    ):

        from app.dashboard.analysis import SessionAnalysis

        SessionAnalysis(
            self,
            session_id
        )

    # =========================================================
    # CANCEL CALLBACKS
    # =========================================================

    def cancel_all_callbacks(self):

        try:

            callback_ids = self.tk.call(
                "after",
                "info"
            )

            if not callback_ids:
                return

            for callback_id in callback_ids:

                try:

                    self.after_cancel(
                        callback_id
                    )

                except Exception:
                    pass

        except Exception:
            pass

        self.update_job = None

    # =========================================================
    # CLOSE APPLICATION
    # =========================================================

    def close_application(self):

        if self.closing:
            return

        self.closing = True

        # =====================================================
        # CANCEL MONITORING CALLBACK
        # =====================================================

        if self.update_job is not None:

            try:

                self.after_cancel(
                    self.update_job
                )

            except Exception:
                pass

            self.update_job = None

        # =====================================================
        # FINISH ACTIVE SESSION
        # =====================================================

        if (
            self.session_active
            and self.recorder
        ):

            try:

                self.recorder.end_session()

            except Exception:
                pass

            self.session_active = False
            self.recorder = None

        # =====================================================
        # CANCEL REMAINING CALLBACKS
        # =====================================================

        self.cancel_all_callbacks()

        # =====================================================
        # STOP MAIN LOOP
        # =====================================================

        try:

            self.quit()

        except Exception:
            pass

        # =====================================================
        # DESTROY WINDOW
        # =====================================================

        try:

            self.destroy()

        except Exception:
            pass