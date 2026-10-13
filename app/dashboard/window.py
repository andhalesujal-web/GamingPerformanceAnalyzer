import customtkinter as ctk

from app.monitor.collector import collect_metrics
from app.session.recorder import SessionRecorder
from app.database.db import get_all_game_profiles
from app.config.settings import load_settings


class Dashboard(ctk.CTk):

    # =========================================================
    # COLORS
    # =========================================================

    BG = "#0B0F14"
    SIDEBAR = "#0F141B"
    CARD = "#141A22"
    CARD_HOVER = "#1B2430"
    BORDER = "#252E3A"

    TEXT = "#F5F7FA"
    MUTED = "#8B96A5"

    BLUE = "#3B82F6"
    GREEN = "#22C55E"
    RED = "#EF4444"
    ORANGE = "#F59E0B"
    PURPLE = "#8B5CF6"

    # =========================================================
    # INITIALIZATION
    # =========================================================

    def __init__(self):
        super().__init__()

        self.title("Gaming Performance Analyzer")
        self.geometry("1250x780")
        self.minsize(1100, 700)

        # -----------------------------------------------------
        # APPLICATION STATE
        # -----------------------------------------------------

        self.recorder = None
        self.session_active = False
        self.update_job = None
        self.closing = False

        self.current_game = "No Game Selected"

        # Graph history
        self.cpu_history = []
        self.gpu_history = []
        self.ram_history = []

        self.max_graph_points = 40

        # -----------------------------------------------------
        # SETTINGS
        # -----------------------------------------------------

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

        ctk.set_default_color_theme("blue")

        # -----------------------------------------------------
        # CREATE UI
        # -----------------------------------------------------

        self.create_interface()

        self.load_game_profiles()

        self.update_metrics()

        self.protocol(
            "WM_DELETE_WINDOW",
            self.close_application
        )

    # =========================================================
    # MAIN INTERFACE
    # =========================================================

    def create_interface(self):

        # -----------------------------------------------------
        # ROOT GRID
        # -----------------------------------------------------

        self.grid_columnconfigure(
            0,
            weight=0
        )

        self.grid_columnconfigure(
            1,
            weight=1
        )

        self.grid_rowconfigure(
            0,
            weight=1
        )

        # -----------------------------------------------------
        # SIDEBAR
        # -----------------------------------------------------

        self.create_sidebar()

        # -----------------------------------------------------
        # MAIN CONTENT
        # -----------------------------------------------------

        self.main_frame = ctk.CTkFrame(
            self,
            fg_color=self.BG,
            corner_radius=0
        )

        self.main_frame.grid(
            row=0,
            column=1,
            sticky="nsew"
        )

        self.main_frame.grid_columnconfigure(
            0,
            weight=1
        )

        self.main_frame.grid_rowconfigure(
            3,
            weight=1
        )

        self.create_header()
        self.create_game_profile()
        self.create_metric_cards()
        self.create_bottom_area()

    # =========================================================
    # SIDEBAR
    # =========================================================

    def create_sidebar(self):

        self.sidebar = ctk.CTkFrame(
            self,
            width=220,
            corner_radius=0,
            fg_color=self.SIDEBAR
        )

        self.sidebar.grid(
            row=0,
            column=0,
            sticky="nsew"
        )

        self.sidebar.grid_propagate(False)

        # -----------------------------------------------------
        # LOGO
        # -----------------------------------------------------

        logo_frame = ctk.CTkFrame(
            self.sidebar,
            fg_color="transparent"
        )

        logo_frame.pack(
            fill="x",
            padx=20,
            pady=(25, 30)
        )

        logo_icon = ctk.CTkLabel(
            logo_frame,
            text="◈",
            text_color=self.BLUE,
            font=ctk.CTkFont(
                size=30,
                weight="bold"
            )
        )

        logo_icon.pack(
            side="left"
        )

        logo_text_frame = ctk.CTkFrame(
            logo_frame,
            fg_color="transparent"
        )

        logo_text_frame.pack(
            side="left",
            padx=8
        )

        ctk.CTkLabel(
            logo_text_frame,
            text="GPA",
            text_color=self.TEXT,
            font=ctk.CTkFont(
                size=20,
                weight="bold"
            )
        ).pack(
            anchor="w"
        )

        ctk.CTkLabel(
            logo_text_frame,
            text="Performance Analyzer",
            text_color=self.MUTED,
            font=ctk.CTkFont(
                size=9
            )
        ).pack(
            anchor="w"
        )

        # -----------------------------------------------------
        # NAVIGATION TITLE
        # -----------------------------------------------------

        ctk.CTkLabel(
            self.sidebar,
            text="MAIN MENU",
            text_color="#5F6B7A",
            font=ctk.CTkFont(
                size=10,
                weight="bold"
            )
        ).pack(
            anchor="w",
            padx=22,
            pady=(0, 10)
        )

        # -----------------------------------------------------
        # NAVIGATION BUTTONS
        # -----------------------------------------------------

        self.dashboard_button = self.create_nav_button(
            "▣   Dashboard",
            self.show_dashboard,
            active=True
        )

        self.history_button = self.create_nav_button(
            "◷   Session History",
            self.open_history
        )

        self.profile_button = self.create_nav_button(
            "▤   Game Profiles",
            self.open_game_profiles
        )

        self.settings_button = self.create_nav_button(
            "⚙   Settings",
            self.open_settings
        )

        # -----------------------------------------------------
        # SIDEBAR BOTTOM
        # -----------------------------------------------------

        bottom_frame = ctk.CTkFrame(
            self.sidebar,
            fg_color="transparent"
        )

        bottom_frame.pack(
            side="bottom",
            fill="x",
            padx=18,
            pady=20
        )

        ctk.CTkFrame(
            bottom_frame,
            height=1,
            fg_color=self.BORDER
        ).pack(
            fill="x",
            pady=(0, 15)
        )

        ctk.CTkLabel(
            bottom_frame,
            text="SYSTEM",
            text_color="#5F6B7A",
            font=ctk.CTkFont(
                size=9,
                weight="bold"
            )
        ).pack(
            anchor="w"
        )

        self.sidebar_status = ctk.CTkLabel(
            bottom_frame,
            text="●  Monitoring",
            text_color=self.GREEN,
            font=ctk.CTkFont(
                size=12,
                weight="bold"
            )
        )

        self.sidebar_status.pack(
            anchor="w",
            pady=(5, 0)
        )

    # =========================================================
    # NAV BUTTON
    # =========================================================

    def create_nav_button(
        self,
        text,
        command,
        active=False
    ):

        button = ctk.CTkButton(
            self.sidebar,
            text=text,
            command=command,
            anchor="w",
            height=42,
            corner_radius=8,
            fg_color=(
                self.BLUE
                if active
                else "transparent"
            ),
            hover_color=(
                "#2563EB"
                if active
                else self.CARD_HOVER
            ),
            text_color=self.TEXT,
            font=ctk.CTkFont(
                size=13,
                weight="bold"
                if active
                else "normal"
            )
        )

        button.pack(
            fill="x",
            padx=14,
            pady=3
        )

        return button

    # =========================================================
    # HEADER
    # =========================================================

    def create_header(self):

        self.header = ctk.CTkFrame(
            self.main_frame,
            fg_color="transparent"
        )

        self.header.grid(
            row=0,
            column=0,
            sticky="ew",
            padx=28,
            pady=(24, 10)
        )

        self.header.grid_columnconfigure(
            0,
            weight=1
        )

        # Title

        title_frame = ctk.CTkFrame(
            self.header,
            fg_color="transparent"
        )

        title_frame.grid(
            row=0,
            column=0,
            sticky="w"
        )

        ctk.CTkLabel(
            title_frame,
            text="GAMING PERFORMANCE ANALYZER",
            text_color=self.TEXT,
            font=ctk.CTkFont(
                size=25,
                weight="bold"
            )
        ).pack(
            anchor="w"
        )

        ctk.CTkLabel(
            title_frame,
            text="Real-time hardware monitoring & performance analysis",
            text_color=self.MUTED,
            font=ctk.CTkFont(
                size=12
            )
        ).pack(
            anchor="w",
            pady=(3, 0)
        )

        # Online status

        status_frame = ctk.CTkFrame(
            self.header,
            fg_color=self.CARD,
            corner_radius=20,
            border_width=1,
            border_color=self.BORDER
        )

        status_frame.grid(
            row=0,
            column=1,
            sticky="e",
            padx=(20, 0)
        )

        self.online_label = ctk.CTkLabel(
            status_frame,
            text="●  SYSTEM ONLINE",
            text_color=self.GREEN,
            font=ctk.CTkFont(
                size=11,
                weight="bold"
            )
        )

        self.online_label.pack(
            padx=16,
            pady=9
        )

    # =========================================================
    # CURRENT GAME PROFILE
    # =========================================================

    def create_game_profile(self):

        self.profile_card = ctk.CTkFrame(
            self.main_frame,
            fg_color=self.CARD,
            corner_radius=14,
            border_width=1,
            border_color=self.BORDER
        )

        self.profile_card.grid(
            row=1,
            column=0,
            sticky="ew",
            padx=28,
            pady=10
        )

        self.profile_card.grid_columnconfigure(
            1,
            weight=1
        )

        # Game icon

        icon_frame = ctk.CTkFrame(
            self.profile_card,
            width=70,
            height=70,
            corner_radius=12,
            fg_color="#1D4ED8"
        )

        icon_frame.grid(
            row=0,
            column=0,
            padx=16,
            pady=14
        )

        icon_frame.grid_propagate(False)

        ctk.CTkLabel(
            icon_frame,
            text="🎮",
            font=ctk.CTkFont(
                size=28
            )
        ).place(
            relx=0.5,
            rely=0.5,
            anchor="center"
        )

        # Game information

        info_frame = ctk.CTkFrame(
            self.profile_card,
            fg_color="transparent"
        )

        info_frame.grid(
            row=0,
            column=1,
            sticky="w",
            pady=12
        )

        ctk.CTkLabel(
            info_frame,
            text="CURRENT GAME PROFILE",
            text_color=self.MUTED,
            font=ctk.CTkFont(
                size=9,
                weight="bold"
            )
        ).pack(
            anchor="w"
        )

        self.game_name_label = ctk.CTkLabel(
            info_frame,
            text="No Game Selected",
            text_color=self.TEXT,
            font=ctk.CTkFont(
                size=18,
                weight="bold"
            )
        )

        self.game_name_label.pack(
            anchor="w",
            pady=(3, 2)
        )

        self.game_details_label = ctk.CTkLabel(
            info_frame,
            text="Select a profile to begin",
            text_color=self.MUTED,
            font=ctk.CTkFont(
                size=11
            )
        )

        self.game_details_label.pack(
            anchor="w"
        )

        # Profile dropdown

        self.game_combo = ctk.CTkComboBox(
            self.profile_card,
            values=["No profiles available"],
            width=210,
            height=38,
            corner_radius=8,
            fg_color=self.SIDEBAR,
            border_color=self.BORDER,
            button_color=self.BLUE,
            button_hover_color="#2563EB",
            dropdown_fg_color=self.CARD,
            dropdown_hover_color=self.CARD_HOVER,
            dropdown_text_color=self.TEXT,
            command=self.profile_selected
        )

        self.game_combo.grid(
            row=0,
            column=2,
            padx=16,
            pady=14
        )

    # =========================================================
    # METRIC CARDS
    # =========================================================

    def create_metric_cards(self):

        self.metrics_frame = ctk.CTkFrame(
            self.main_frame,
            fg_color="transparent"
        )

        self.metrics_frame.grid(
            row=2,
            column=0,
            sticky="ew",
            padx=28,
            pady=10
        )

        for column in range(4):

            self.metrics_frame.grid_columnconfigure(
                column,
                weight=1
            )

        self.cpu_label = self.create_metric_card(
            self.metrics_frame,
            0,
            "CPU",
            "Processor Usage",
            self.BLUE
        )

        self.gpu_label = self.create_metric_card(
            self.metrics_frame,
            1,
            "GPU",
            "Graphics Usage",
            self.PURPLE
        )

        self.ram_label = self.create_metric_card(
            self.metrics_frame,
            2,
            "RAM",
            "Memory Usage",
            self.GREEN
        )

        self.temp_label = self.create_metric_card(
            self.metrics_frame,
            3,
            "GPU TEMP",
            "Graphics Temperature",
            self.ORANGE
        )

    # =========================================================
    # METRIC CARD
    # =========================================================

    def create_metric_card(
        self,
        parent,
        column,
        title,
        subtitle,
        accent
    ):

        card = ctk.CTkFrame(
            parent,
            fg_color=self.CARD,
            corner_radius=14,
            border_width=1,
            border_color=self.BORDER
        )

        card.grid(
            row=0,
            column=column,
            sticky="ew",
            padx=5
        )

        # Top line

        top = ctk.CTkFrame(
            card,
            fg_color="transparent"
        )

        top.pack(
            fill="x",
            padx=15,
            pady=(13, 0)
        )

        ctk.CTkLabel(
            top,
            text=title,
            text_color=self.TEXT,
            font=ctk.CTkFont(
                size=13,
                weight="bold"
            )
        ).pack(
            side="left"
        )

        # Value

        value = ctk.CTkLabel(
            card,
            text="--",
            text_color=self.TEXT,
            font=ctk.CTkFont(
                size=28,
                weight="bold"
            )
        )

        value.pack(
            anchor="w",
            padx=15,
            pady=(8, 0)
        )

        # Subtitle

        ctk.CTkLabel(
            card,
            text=subtitle,
            text_color=self.MUTED,
            font=ctk.CTkFont(
                size=9
            )
        ).pack(
            anchor="w",
            padx=15,
            pady=(0, 10)
        )

        # Progress bar

        progress = ctk.CTkProgressBar(
            card,
            height=5,
            corner_radius=3,
            progress_color=accent,
            fg_color="#242B35"
        )

        progress.set(0)

        progress.pack(
            fill="x",
            padx=15,
            pady=(0, 14)
        )

        return {
            "value": value,
            "progress": progress
        }

    # =========================================================
    # BOTTOM AREA
    # =========================================================

    def create_bottom_area(self):

        self.bottom_frame = ctk.CTkFrame(
            self.main_frame,
            fg_color="transparent"
        )

        self.bottom_frame.grid(
            row=3,
            column=0,
            sticky="nsew",
            padx=28,
            pady=(5, 20)
        )

        self.bottom_frame.grid_columnconfigure(
            0,
            weight=3
        )

        self.bottom_frame.grid_columnconfigure(
            1,
            weight=2
        )

        self.bottom_frame.grid_rowconfigure(
            0,
            weight=1
        )

        self.create_graph_panel()

        self.create_session_panel()

    # =========================================================
    # GRAPH PANEL
    # =========================================================

    def create_graph_panel(self):

        self.graph_card = ctk.CTkFrame(
            self.bottom_frame,
            fg_color=self.CARD,
            corner_radius=14,
            border_width=1,
            border_color=self.BORDER
        )

        self.graph_card.grid(
            row=0,
            column=0,
            sticky="nsew",
            padx=(0, 6)
        )

        # Header

        graph_header = ctk.CTkFrame(
            self.graph_card,
            fg_color="transparent"
        )

        graph_header.pack(
            fill="x",
            padx=18,
            pady=(14, 5)
        )

        ctk.CTkLabel(
            graph_header,
            text="LIVE PERFORMANCE",
            text_color=self.TEXT,
            font=ctk.CTkFont(
                size=13,
                weight="bold"
            )
        ).pack(
            side="left"
        )

        ctk.CTkLabel(
            graph_header,
            text="CPU   GPU   RAM",
            text_color=self.MUTED,
            font=ctk.CTkFont(
                size=9
            )
        ).pack(
            side="right"
        )

        # Canvas

        self.graph_canvas = ctk.CTkCanvas(
            self.graph_card,
            bg=self.CARD,
            highlightthickness=0
        )

        self.graph_canvas.pack(
            fill="both",
            expand=True,
            padx=12,
            pady=(0, 12)
        )

        self.graph_canvas.bind(
            "<Configure>",
            lambda event: self.draw_graph()
        )

    # =========================================================
    # SESSION PANEL
    # =========================================================

    def create_session_panel(self):

        self.session_card = ctk.CTkFrame(
            self.bottom_frame,
            fg_color=self.CARD,
            corner_radius=14,
            border_width=1,
            border_color=self.BORDER
        )

        self.session_card.grid(
            row=0,
            column=1,
            sticky="nsew",
            padx=(6, 0)
        )

        # Header

        ctk.CTkLabel(
            self.session_card,
            text="SESSION CONTROL",
            text_color=self.TEXT,
            font=ctk.CTkFont(
                size=13,
                weight="bold"
            )
        ).pack(
            anchor="w",
            padx=18,
            pady=(15, 12)
        )

        # Status

        self.session_status = ctk.CTkLabel(
            self.session_card,
            text="Ready to record",
            text_color=self.MUTED,
            font=ctk.CTkFont(
                size=11
            )
        )

        self.session_status.pack(
            anchor="w",
            padx=18
        )

        # Start button

        self.start_button = ctk.CTkButton(
            self.session_card,
            text="▶  START SESSION",
            command=self.start_session,
            height=40,
            corner_radius=8,
            fg_color=self.GREEN,
            hover_color="#16A34A",
            text_color="#07100A",
            font=ctk.CTkFont(
                size=12,
                weight="bold"
            )
        )

        self.start_button.pack(
            fill="x",
            padx=18,
            pady=(15, 8)
        )

        # Stop button

        self.stop_button = ctk.CTkButton(
            self.session_card,
            text="■  STOP SESSION",
            command=self.stop_session,
            state="disabled",
            height=40,
            corner_radius=8,
            fg_color="#242B35",
            hover_color="#303946",
            text_color=self.TEXT,
            font=ctk.CTkFont(
                size=12,
                weight="bold"
            )
        )

        self.stop_button.pack(
            fill="x",
            padx=18,
            pady=(0, 15)
        )

        # Separator

        ctk.CTkFrame(
            self.session_card,
            height=1,
            fg_color=self.BORDER
        ).pack(
            fill="x",
            padx=18
        )

        # Session info

        ctk.CTkLabel(
            self.session_card,
            text="SESSION INFORMATION",
            text_color=self.MUTED,
            font=ctk.CTkFont(
                size=9,
                weight="bold"
            )
        ).pack(
            anchor="w",
            padx=18,
            pady=(15, 8)
        )

        self.session_game_label = self.create_info_row(
            "Game",
            "—"
        )

        self.session_state_label = self.create_info_row(
            "Status",
            "Idle"
        )

        self.session_monitor_label = self.create_info_row(
            "Monitor",
            "Active"
        )

    # =========================================================
    # INFO ROW
    # =========================================================

    def create_info_row(
        self,
        title,
        value
    ):

        frame = ctk.CTkFrame(
            self.session_card,
            fg_color="transparent"
        )

        frame.pack(
            fill="x",
            padx=18,
            pady=2
        )

        ctk.CTkLabel(
            frame,
            text=title,
            text_color=self.MUTED,
            font=ctk.CTkFont(
                size=10
            )
        ).pack(
            side="left"
        )

        label = ctk.CTkLabel(
            frame,
            text=value,
            text_color=self.TEXT,
            font=ctk.CTkFont(
                size=10,
                weight="bold"
            )
        )

        label.pack(
            side="right"
        )

        return label

    # =========================================================
    # LOAD GAME PROFILES
    # =========================================================

    def load_game_profiles(self):

        try:

            profiles = get_all_game_profiles()

            self.profile_data = profiles

            if profiles:

                game_names = [
                    profile[1]
                    for profile in profiles
                ]

                self.game_combo.configure(
                    values=game_names
                )

                self.game_combo.set(
                    game_names[0]
                )

                self.update_profile_display(
                    profiles[0]
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

                self.update_profile_display(
                    None
                )

        except Exception as error:

            self.profile_data = []

            self.game_combo.configure(
                values=[
                    "Database error"
                ]
            )

            self.game_combo.set(
                "Database error"
            )

            self.game_name_label.configure(
                text="Database Error"
            )

            self.game_details_label.configure(
                text=str(error)
            )

    # =========================================================
    # PROFILE SELECTED
    # =========================================================

    def profile_selected(self, selected):

        if not hasattr(
            self,
            "profile_data"
        ):
            return

        for profile in self.profile_data:

            if profile[1] == selected:

                self.update_profile_display(
                    profile
                )

                break

    # =========================================================
    # UPDATE PROFILE DISPLAY
    # =========================================================

    def update_profile_display(
        self,
        profile
    ):

        if not profile:

            self.current_game = "No Game Selected"

            self.game_name_label.configure(
                text="No Game Selected"
            )

            self.game_details_label.configure(
                text="Create a game profile to begin"
            )

            return

        self.current_game = profile[1]

        game_name = profile[1]
        resolution = profile[2]
        quality = profile[3]

        self.game_name_label.configure(
            text=game_name
        )

        self.game_details_label.configure(
            text=f"{resolution}   •   {quality} Quality"
        )

        self.session_game_label.configure(
            text=game_name
        )

    # =========================================================
    # REFRESH GAME PROFILES
    # =========================================================

    def refresh_game_profiles(self):

        self.load_game_profiles()

    # =========================================================
    # START SESSION
    # =========================================================

    def start_session(self):

        game_name = self.game_combo.get().strip()

        if not game_name:

            self.set_status(
                "Select a game first.",
                self.RED
            )

            return

        if game_name in (
            "No profiles available",
            "Database error"
        ):

            self.set_status(
                "Create a game profile first.",
                self.RED
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
                state="normal",
                fg_color=self.RED,
                hover_color="#DC2626"
            )

            self.game_combo.configure(
                state="disabled"
            )

            self.session_status.configure(
                text="Recording performance data",
                text_color=self.GREEN
            )

            self.session_state_label.configure(
                text="Recording",
                text_color=self.GREEN
            )

            self.sidebar_status.configure(
                text="●  Recording",
                text_color=self.RED
            )

            self.set_status(
                f"Recording: {game_name}",
                self.RED
            )

        except Exception as error:

            self.set_status(
                f"Session error: {error}",
                self.RED
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
                state="disabled",
                fg_color="#242B35",
                hover_color="#303946"
            )

            self.game_combo.configure(
                state="readonly"
            )

            self.session_status.configure(
                text="Session completed",
                text_color=self.GREEN
            )

            self.session_state_label.configure(
                text="Completed",
                text_color=self.GREEN
            )

            self.sidebar_status.configure(
                text="●  Monitoring",
                text_color=self.GREEN
            )

            self.set_status(
                "Session completed",
                self.GREEN
            )

        except Exception as error:

            self.set_status(
                f"Session error: {error}",
                self.RED
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

            cpu_usage = float(
                cpu["usage_percent"]
            )

            ram_usage = float(
                memory["usage_percent"]
            )

            disk_usage = float(
                disk["usage_percent"]
            )

            # -------------------------------------------------
            # CPU
            # -------------------------------------------------

            self.cpu_label["value"].configure(
                text=f"{cpu_usage:.1f}%"
            )

            self.cpu_label["progress"].set(
                min(cpu_usage / 100, 1)
            )

            # -------------------------------------------------
            # RAM
            # -------------------------------------------------

            self.ram_label["value"].configure(
                text=f"{ram_usage:.1f}%"
            )

            self.ram_label["progress"].set(
                min(ram_usage / 100, 1)
            )

            # -------------------------------------------------
            # DISK
            # -------------------------------------------------

            if hasattr(
                self,
                "disk_value_label"
            ):

                self.disk_value_label.configure(
                    text=f"{disk_usage:.1f}%"
                )

            # -------------------------------------------------
            # GPU
            # -------------------------------------------------

            if "error" not in gpu:

                gpu_usage = float(
                    gpu["gpu_usage"]
                )

                temperature = float(
                    gpu["temperature"]
                )

                vram_used = float(
                    gpu["memory_used_mb"]
                )

                vram_total = float(
                    gpu["memory_total_mb"]
                )

                self.gpu_label["value"].configure(
                    text=f"{gpu_usage:.1f}%"
                )

                self.gpu_label["progress"].set(
                    min(gpu_usage / 100, 1)
                )

                self.temp_label["value"].configure(
                    text=f"{temperature:.0f}°C"
                )

                self.temp_label["progress"].set(
                    min(temperature / 100, 1)
                )

                self.update_secondary_info(
                    vram_used,
                    vram_total,
                    disk_usage
                )

                self.gpu_history.append(
                    gpu_usage
                )

            else:

                gpu_usage = 0

                self.gpu_label["value"].configure(
                    text="N/A"
                )

                self.gpu_label["progress"].set(0)

                self.temp_label["value"].configure(
                    text="N/A"
                )

                self.temp_label["progress"].set(0)

                self.update_secondary_info(
                    None,
                    None,
                    disk_usage
                )

            # -------------------------------------------------
            # GRAPH HISTORY
            # -------------------------------------------------

            self.cpu_history.append(
                cpu_usage
            )

            self.ram_history.append(
                ram_usage
            )

            self.cpu_history = (
                self.cpu_history[
                    -self.max_graph_points:
                ]
            )

            self.gpu_history = (
                self.gpu_history[
                    -self.max_graph_points:
                ]
            )

            self.ram_history = (
                self.ram_history[
                    -self.max_graph_points:
                ]
            )

            self.draw_graph()

            # -------------------------------------------------
            # RECORD SESSION
            # -------------------------------------------------

            if (
                self.session_active
                and self.recorder
            ):

                self.recorder.record_sample(
                    metrics
                )

        except Exception as error:

            if not self.closing:

                self.set_status(
                    f"Monitoring error: {error}",
                    self.RED
                )

        # -----------------------------------------------------
        # NEXT UPDATE
        # -----------------------------------------------------

        if not self.closing:

            try:

                self.update_job = self.after(
                    self.monitoring_interval * 1000,
                    self.update_metrics
                )

            except Exception:

                self.update_job = None

    # =========================================================
    # SECONDARY INFORMATION
    # =========================================================

    def update_secondary_info(
        self,
        vram_used,
        vram_total,
        disk_usage
    ):

        if vram_used is not None:

            self.session_monitor_label.configure(
                text=f"VRAM {vram_used:.0f}/{vram_total:.0f} MB"
            )

        else:

            self.session_monitor_label.configure(
                text=f"Disk {disk_usage:.1f}%"
            )

    # =========================================================
    # LIVE GRAPH
    # =========================================================

    def draw_graph(self):

        if not hasattr(
            self,
            "graph_canvas"
        ):
            return

        canvas = self.graph_canvas

        try:

            width = canvas.winfo_width()
            height = canvas.winfo_height()

            if width < 50 or height < 50:
                return

            canvas.delete("all")

            # -------------------------------------------------
            # GRID
            # -------------------------------------------------

            for i in range(1, 5):

                y = (
                    height
                    - (height * i / 5)
                )

                canvas.create_line(
                    0,
                    y,
                    width,
                    y,
                    fill="#202833"
                )

            # -------------------------------------------------
            # DATA
            # -------------------------------------------------

            datasets = [
                (
                    self.cpu_history,
                    self.BLUE
                ),
                (
                    self.gpu_history,
                    self.PURPLE
                ),
                (
                    self.ram_history,
                    self.GREEN
                )
            ]

            for data, color in datasets:

                if len(data) < 2:
                    continue

                points = []

                for index, value in enumerate(data):

                    x = (
                        index
                        / max(
                            len(data) - 1,
                            1
                        )
                        * width
                    )

                    y = (
                        height
                        - (
                            min(
                                max(value, 0),
                                100
                            )
                            / 100
                            * height
                        )
                    )

                    points.extend(
                        [x, y]
                    )

                canvas.create_line(
                    *points,
                    fill=color,
                    width=2,
                    smooth=True
                )

        except Exception:
            pass

    # =========================================================
    # STATUS
    # =========================================================

    def set_status(
        self,
        text,
        color=None
    ):

        if color is None:
            color = self.TEXT

        try:

            self.online_label.configure(
                text="●  SYSTEM ONLINE",
                text_color=self.GREEN
            )

            self.session_status.configure(
                text=text,
                text_color=color
            )

        except Exception:
            pass

    # =========================================================
    # DASHBOARD
    # =========================================================

    def show_dashboard(self):

        self.dashboard_button.configure(
            fg_color=self.BLUE
        )

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

        # -----------------------------------------------------
        # CANCEL MONITORING
        # -----------------------------------------------------

        if self.update_job is not None:

            try:

                self.after_cancel(
                    self.update_job
                )

            except Exception:
                pass

            self.update_job = None

        # -----------------------------------------------------
        # FINISH ACTIVE SESSION
        # -----------------------------------------------------

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

        # -----------------------------------------------------
        # CANCEL CALLBACKS
        # -----------------------------------------------------

        self.cancel_all_callbacks()

        # -----------------------------------------------------
        # CLOSE
        # -----------------------------------------------------

        try:

            self.quit()

        except Exception:
            pass

        try:

            self.destroy()

        except Exception:
            pass