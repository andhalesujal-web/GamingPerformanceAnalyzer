import customtkinter as ctk
import matplotlib.pyplot as plt

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from app.database.db import get_connection
from app.session.analyzer import get_session_metrics
from app.session.performance import analyze_session_performance
from app.session.scoring import calculate_performance_score


class SessionAnalysis(ctk.CTkToplevel):

    def __init__(self, parent, session_id):

        super().__init__(parent)

        # =====================================================
        # WINDOW
        # =====================================================

        self.parent = parent
        self.session_id = session_id
        self.figure = None
        self.canvas = None

        self.title("Session Analysis")
        self.geometry("1150x900")
        self.minsize(950, 700)

        self.configure(
            fg_color="#080B12"
        )

        # =====================================================
        # CREATE UI
        # =====================================================

        self.create_interface()
        self.load_analysis()

    # =========================================================
    # MAIN INTERFACE
    # =========================================================

    def create_interface(self):

        # =====================================================
        # HEADER
        # =====================================================

        header = ctk.CTkFrame(
            self,
            fg_color="#0D111A",
            corner_radius=0
        )

        header.pack(
            fill="x"
        )

        # Title

        title = ctk.CTkLabel(
            header,
            text="SESSION ANALYSIS",
            font=ctk.CTkFont(
                size=26,
                weight="bold"
            ),
            text_color="#FFFFFF"
        )

        title.pack(
            side="left",
            padx=30,
            pady=(20, 4)
        )

        # Close button

        close_button = ctk.CTkButton(
            header,
            text="✕",
            width=38,
            height=32,
            corner_radius=8,
            fg_color="#151C2A",
            hover_color="#2A3548",
            command=self.destroy
        )

        close_button.pack(
            side="right",
            padx=25,
            pady=18
        )

        # Game information

        self.game_label = ctk.CTkLabel(
            self,
            text="Loading session...",
            font=ctk.CTkFont(
                size=14
            ),
            text_color="#7F8CA3"
        )

        self.game_label.pack(
            anchor="w",
            padx=30,
            pady=(12, 15)
        )

        # =====================================================
        # SCROLLABLE CONTENT
        # =====================================================

        self.content_frame = ctk.CTkScrollableFrame(
            self,
            fg_color="#080B12",
            corner_radius=0
        )

        self.content_frame.pack(
            padx=20,
            pady=(0, 20),
            fill="both",
            expand=True
        )

        # =====================================================
        # PERFORMANCE SUMMARY
        # =====================================================

        summary_title = ctk.CTkLabel(
            self.content_frame,
            text="PERFORMANCE SUMMARY",
            font=ctk.CTkFont(
                size=18,
                weight="bold"
            ),
            text_color="#FFFFFF"
        )

        summary_title.pack(
            anchor="w",
            padx=5,
            pady=(5, 10)
        )

        self.summary_frame = ctk.CTkFrame(
            self.content_frame,
            fg_color="#0F141E",
            corner_radius=14,
            border_width=1,
            border_color="#1B2433"
        )

        self.summary_frame.pack(
            fill="x",
            padx=5,
            pady=(0, 15)
        )

        # Configure columns

        for column in range(3):

            self.summary_frame.grid_columnconfigure(
                column,
                weight=1
            )

        # Row 1

        self.avg_cpu_label = self.create_metric(
            self.summary_frame,
            "AVG CPU",
            0,
            0
        )

        self.peak_cpu_label = self.create_metric(
            self.summary_frame,
            "PEAK CPU",
            0,
            1
        )

        self.avg_gpu_label = self.create_metric(
            self.summary_frame,
            "AVG GPU",
            0,
            2
        )

        # Row 2

        self.peak_gpu_label = self.create_metric(
            self.summary_frame,
            "PEAK GPU",
            1,
            0
        )

        self.avg_ram_label = self.create_metric(
            self.summary_frame,
            "AVG RAM",
            1,
            1
        )

        self.peak_ram_label = self.create_metric(
            self.summary_frame,
            "PEAK RAM",
            1,
            2
        )

        # Row 3

        self.avg_temp_label = self.create_metric(
            self.summary_frame,
            "AVG GPU TEMP",
            2,
            0
        )

        self.peak_temp_label = self.create_metric(
            self.summary_frame,
            "PEAK GPU TEMP",
            2,
            1
        )

        self.avg_vram_label = self.create_metric(
            self.summary_frame,
            "AVG VRAM",
            2,
            2
        )

        # =====================================================
        # SCORE SECTION
        # =====================================================

        score_frame = ctk.CTkFrame(
            self.content_frame,
            fg_color="#0F141E",
            corner_radius=14,
            border_width=1,
            border_color="#1B2433"
        )

        score_frame.pack(
            fill="x",
            padx=5,
            pady=10
        )

        score_title = ctk.CTkLabel(
            score_frame,
            text="PERFORMANCE SCORE",
            font=ctk.CTkFont(
                size=13,
                weight="bold"
            ),
            text_color="#7F8CA3"
        )

        score_title.pack(
            pady=(18, 2)
        )

        self.score_label = ctk.CTkLabel(
            score_frame,
            text="-- / 100",
            font=ctk.CTkFont(
                size=40,
                weight="bold"
            ),
            text_color="#FFFFFF"
        )

        self.score_label.pack(
            pady=(0, 5)
        )

        self.score_status_label = ctk.CTkLabel(
            score_frame,
            text="Calculating...",
            font=ctk.CTkFont(
                size=12
            ),
            text_color="#7F8CA3"
        )

        self.score_status_label.pack(
            pady=(0, 18)
        )

        # =====================================================
        # GRAPH TITLE
        # =====================================================

        graph_title = ctk.CTkLabel(
            self.content_frame,
            text="PERFORMANCE GRAPH",
            font=ctk.CTkFont(
                size=18,
                weight="bold"
            ),
            text_color="#FFFFFF"
        )

        graph_title.pack(
            anchor="w",
            padx=5,
            pady=(20, 10)
        )

        # =====================================================
        # GRAPH FRAME
        # =====================================================

        self.graph_frame = ctk.CTkFrame(
            self.content_frame,
            fg_color="#0F141E",
            corner_radius=14,
            border_width=1,
            border_color="#1B2433"
        )

        self.graph_frame.pack(
            fill="x",
            padx=5,
            pady=(0, 15)
        )

        # =====================================================
        # FINDINGS
        # =====================================================

        findings_title = ctk.CTkLabel(
            self.content_frame,
            text="PERFORMANCE FINDINGS",
            font=ctk.CTkFont(
                size=18,
                weight="bold"
            ),
            text_color="#FFFFFF"
        )

        findings_title.pack(
            anchor="w",
            padx=5,
            pady=(15, 8)
        )

        self.findings_box = ctk.CTkTextbox(
            self.content_frame,
            height=150,
            fg_color="#0F141E",
            border_width=1,
            border_color="#1B2433",
            corner_radius=12,
            text_color="#DCE3EF"
        )

        self.findings_box.pack(
            fill="x",
            padx=5,
            pady=(0, 15)
        )

        self.findings_box.configure(
            state="disabled"
        )

        # =====================================================
        # RECOMMENDATIONS
        # =====================================================

        recommendations_title = ctk.CTkLabel(
            self.content_frame,
            text="PERFORMANCE RECOMMENDATIONS",
            font=ctk.CTkFont(
                size=18,
                weight="bold"
            ),
            text_color="#FFFFFF"
        )

        recommendations_title.pack(
            anchor="w",
            padx=5,
            pady=(5, 8)
        )

        self.recommendations_box = ctk.CTkTextbox(
            self.content_frame,
            height=160,
            fg_color="#0F141E",
            border_width=1,
            border_color="#1B2433",
            corner_radius=12,
            text_color="#DCE3EF"
        )

        self.recommendations_box.pack(
            fill="x",
            padx=5,
            pady=(0, 20)
        )

        self.recommendations_box.configure(
            state="disabled"
        )

        # =====================================================
        # PDF REPORT
        # =====================================================

        self.report_button = ctk.CTkButton(
            self.content_frame,
            text="GENERATE PDF REPORT",
            height=42,
            corner_radius=10,
            fg_color="#151F31",
            hover_color="#24344F",
            font=ctk.CTkFont(
                size=13,
                weight="bold"
            ),
            command=self.generate_pdf_report
        )

        self.report_button.pack(
            padx=5,
            pady=(0, 25)
        )

    # =========================================================
    # METRIC CARD
    # =========================================================

    def create_metric(
        self,
        parent,
        title,
        row,
        column
    ):

        card = ctk.CTkFrame(
            parent,
            fg_color="#111722",
            corner_radius=10
        )

        card.grid(
            row=row,
            column=column,
            padx=7,
            pady=7,
            sticky="nsew"
        )

        title_label = ctk.CTkLabel(
            card,
            text=title,
            font=ctk.CTkFont(
                size=11,
                weight="bold"
            ),
            text_color="#69778E"
        )

        title_label.pack(
            pady=(12, 3)
        )

        value_label = ctk.CTkLabel(
            card,
            text="--",
            font=ctk.CTkFont(
                size=22,
                weight="bold"
            ),
            text_color="#FFFFFF"
        )

        value_label.pack(
            pady=(0, 12)
        )

        return value_label

    # =========================================================
    # DATABASE - SESSION INFO
    # =========================================================

    def get_session_info(self):

        connection = get_connection()

        try:

            cursor = connection.cursor()

            cursor.execute(
                """
                SELECT
                    game_name,
                    start_time,
                    end_time,
                    duration_seconds
                FROM sessions
                WHERE id = ?
                """,
                (self.session_id,)
            )

            return cursor.fetchone()

        finally:

            connection.close()

    # =========================================================
    # DATABASE - GRAPH DATA
    # =========================================================

    def get_graph_data(self):

        connection = get_connection()

        try:

            cursor = connection.cursor()

            cursor.execute(
                """
                SELECT
                    timestamp,
                    cpu_usage,
                    gpu_usage,
                    ram_usage,
                    gpu_temperature
                FROM metrics
                WHERE session_id = ?
                ORDER BY timestamp ASC
                """,
                (self.session_id,)
            )

            return cursor.fetchall()

        finally:

            connection.close()

    # =========================================================
    # LOAD ANALYSIS
    # =========================================================

    def load_analysis(self):

        try:

            # =================================================
            # SESSION
            # =================================================

            session = self.get_session_info()

            if session is None:

                self.game_label.configure(
                    text="Session not found."
                )

                return

            game_name = session[0]
            start_time = session[1]
            duration = session[3]

            duration_text = self.format_duration(
                duration
            )

            start_text = self.format_datetime(
                start_time
            )

            self.game_label.configure(
                text=(
                    f"🎮 {game_name}    •    "
                    f"{start_text}    •    "
                    f"Duration: {duration_text}"
                )
            )

            # =================================================
            # METRICS
            # =================================================

            metrics = get_session_metrics(
                self.session_id
            )

            # CPU

            self.avg_cpu_label.configure(
                text=self.format_percent(
                    metrics.get("avg_cpu")
                )
            )

            self.peak_cpu_label.configure(
                text=self.format_percent(
                    metrics.get("peak_cpu")
                )
            )

            # GPU

            self.avg_gpu_label.configure(
                text=self.format_percent(
                    metrics.get("avg_gpu")
                )
            )

            self.peak_gpu_label.configure(
                text=self.format_percent(
                    metrics.get("peak_gpu")
                )
            )

            # RAM

            self.avg_ram_label.configure(
                text=self.format_percent(
                    metrics.get("avg_ram")
                )
            )

            self.peak_ram_label.configure(
                text=self.format_percent(
                    metrics.get("peak_ram")
                )
            )

            # GPU TEMP

            self.avg_temp_label.configure(
                text=self.format_temperature(
                    metrics.get(
                        "avg_gpu_temperature"
                    )
                )
            )

            self.peak_temp_label.configure(
                text=self.format_temperature(
                    metrics.get(
                        "peak_gpu_temperature"
                    )
                )
            )

            # VRAM

            self.avg_vram_label.configure(
                text=self.format_vram(
                    metrics.get(
                        "avg_gpu_memory"
                    )
                )
            )

            # =================================================
            # SCORE
            # =================================================

            score = calculate_performance_score(
                self.session_id
            )

            self.score_label.configure(
                text=f"{score:.0f} / 100",
                text_color=self.get_score_color(
                    score
                )
            )

            self.score_status_label.configure(
                text=self.get_score_status(
                    score
                )
            )

            # =================================================
            # PERFORMANCE ANALYSIS
            # =================================================

            analysis = analyze_session_performance(
                self.session_id
            )

            # =================================================
            # FINDINGS
            # =================================================

            findings = analysis.get(
                "findings",
                []
            )

            self.set_textbox_content(
                self.findings_box,
                findings,
                "No major performance issues detected."
            )

            # =================================================
            # RECOMMENDATIONS
            # =================================================

            recommendations = analysis.get(
                "recommendations",
                []
            )

            self.set_textbox_content(
                self.recommendations_box,
                recommendations,
                "Keep monitoring your sessions for optimization opportunities."
            )

            # =================================================
            # GRAPH
            # =================================================

            self.create_graph()

        except Exception as error:

            self.game_label.configure(
                text=f"Analysis error: {error}"
            )

            self.show_error(
                error
            )

    # =========================================================
    # TEXTBOX HELPER
    # =========================================================

    def set_textbox_content(
        self,
        textbox,
        items,
        fallback
    ):

        textbox.configure(
            state="normal"
        )

        textbox.delete(
            "1.0",
            "end"
        )

        if items:

            for item in items:

                textbox.insert(
                    "end",
                    f"• {item}\n\n"
                )

        else:

            textbox.insert(
                "end",
                fallback
            )

        textbox.configure(
            state="disabled"
        )

    # =========================================================
    # GRAPH
    # =========================================================

    def create_graph(self):

        rows = self.get_graph_data()

        if not rows:

            label = ctk.CTkLabel(
                self.graph_frame,
                text="No graph data available for this session.",
                text_color="#7F8CA3",
                font=ctk.CTkFont(
                    size=13
                )
            )

            label.pack(
                pady=50
            )

            return

        # =====================================================
        # CLOSE PREVIOUS GRAPH
        # =====================================================

        if self.canvas is not None:

            try:
                self.canvas.get_tk_widget().destroy()
            except Exception:
                pass

        if self.figure is not None:

            try:
                plt.close(
                    self.figure
                )
            except Exception:
                pass

        # =====================================================
        # DATA
        # =====================================================

        timestamps = list(
            range(
                1,
                len(rows) + 1
            )
        )

        cpu_values = [
            row[1]
            for row in rows
        ]

        gpu_values = [
            row[2]
            for row in rows
        ]

        ram_values = [
            row[3]
            for row in rows
        ]

        temperature_values = [
            row[4]
            for row in rows
        ]

        # =====================================================
        # MATPLOTLIB DARK THEME
        # =====================================================

        self.figure, axes = plt.subplots(
            2,
            2,
            figsize=(10, 7)
        )

        self.figure.patch.set_facecolor(
            "#0F141E"
        )

        for axis in axes.flat:

            axis.set_facecolor(
                "#0F141E"
            )

            axis.tick_params(
                colors="#AAB4C5"
            )

            axis.xaxis.label.set_color(
                "#7F8CA3"
            )

            axis.yaxis.label.set_color(
                "#7F8CA3"
            )

            axis.title.set_color(
                "#FFFFFF"
            )

            for spine in axis.spines.values():

                spine.set_color(
                    "#273246"
                )

            axis.grid(
                True,
                alpha=0.18
            )

        # =====================================================
        # CPU
        # =====================================================

        axes[0, 0].plot(
            timestamps,
            cpu_values,
            linewidth=2
        )

        axes[0, 0].set_title(
            "CPU Usage"
        )

        axes[0, 0].set_xlabel(
            "Sample"
        )

        axes[0, 0].set_ylabel(
            "Usage (%)"
        )

        # =====================================================
        # GPU
        # =====================================================

        gpu_points = [
            (timestamps[index], value)
            for index, value in enumerate(
                gpu_values
            )
            if value is not None
        ]

        if gpu_points:

            gpu_x = [
                point[0]
                for point in gpu_points
            ]

            gpu_y = [
                point[1]
                for point in gpu_points
            ]

            axes[0, 1].plot(
                gpu_x,
                gpu_y,
                linewidth=2
            )

        else:

            axes[0, 1].text(
                0.5,
                0.5,
                "GPU data unavailable",
                ha="center",
                va="center",
                transform=axes[0, 1].transAxes,
                color="#7F8CA3"
            )

        axes[0, 1].set_title(
            "GPU Usage"
        )

        axes[0, 1].set_xlabel(
            "Sample"
        )

        axes[0, 1].set_ylabel(
            "Usage (%)"
        )

        # =====================================================
        # RAM
        # =====================================================

        axes[1, 0].plot(
            timestamps,
            ram_values,
            linewidth=2
        )

        axes[1, 0].set_title(
            "RAM Usage"
        )

        axes[1, 0].set_xlabel(
            "Sample"
        )

        axes[1, 0].set_ylabel(
            "Usage (%)"
        )

        # =====================================================
        # TEMPERATURE
        # =====================================================

        temp_points = [
            (timestamps[index], value)
            for index, value in enumerate(
                temperature_values
            )
            if value is not None
        ]

        if temp_points:

            temp_x = [
                point[0]
                for point in temp_points
            ]

            temp_y = [
                point[1]
                for point in temp_points
            ]

            axes[1, 1].plot(
                temp_x,
                temp_y,
                linewidth=2
            )

        else:

            axes[1, 1].text(
                0.5,
                0.5,
                "Temperature data unavailable",
                ha="center",
                va="center",
                transform=axes[1, 1].transAxes,
                color="#7F8CA3"
            )

        axes[1, 1].set_title(
            "GPU Temperature"
        )

        axes[1, 1].set_xlabel(
            "Sample"
        )

        axes[1, 1].set_ylabel(
            "Temperature (°C)"
        )

        # =====================================================
        # Y AXIS LIMITS
        # =====================================================

        axes[0, 0].set_ylim(
            0,
            100
        )

        axes[0, 1].set_ylim(
            0,
            100
        )

        axes[1, 0].set_ylim(
            0,
            100
        )

        # =====================================================
        # LAYOUT
        # =====================================================

        self.figure.tight_layout(
            pad=2.5
        )

        # =====================================================
        # EMBED
        # =====================================================

        self.canvas = FigureCanvasTkAgg(
            self.figure,
            master=self.graph_frame
        )

        self.canvas.draw()

        canvas_widget = (
            self.canvas.get_tk_widget()
        )

        canvas_widget.pack(
            fill="both",
            expand=True,
            padx=10,
            pady=10
        )

    # =========================================================
    # PDF REPORT
    # =========================================================

    def generate_pdf_report(self):

        try:

            from app.report.generator import (
                generate_session_report
            )

            pdf_path = generate_session_report(
                self.session_id
            )

            self.report_button.configure(
                text="✓ PDF REPORT CREATED",
                state="disabled"
            )

            print(
                f"PDF report created: {pdf_path}"
            )

        except Exception as error:

            self.report_button.configure(
                text="REPORT GENERATION FAILED"
            )

            print(
                f"PDF report error: {error}"
            )

    # =========================================================
    # FORMATTING
    # =========================================================

    def format_percent(
        self,
        value
    ):

        if value is None:
            return "N/A"

        try:
            return f"{float(value):.1f}%"
        except (TypeError, ValueError):
            return "N/A"

    # ---------------------------------------------------------

    def format_temperature(
        self,
        value
    ):

        if value is None:
            return "N/A"

        try:
            return f"{float(value):.1f}°C"
        except (TypeError, ValueError):
            return "N/A"

    # ---------------------------------------------------------

    def format_vram(
        self,
        value
    ):

        if value is None:
            return "N/A"

        try:
            return f"{float(value):.0f} MB"
        except (TypeError, ValueError):
            return "N/A"

    # ---------------------------------------------------------

    def format_duration(
        self,
        duration
    ):

        if duration is None:
            return "Active"

        try:

            duration = float(
                duration
            )

        except (TypeError, ValueError):

            return "Unknown"

        if duration < 60:

            return f"{duration:.0f}s"

        minutes = int(
            duration // 60
        )

        seconds = int(
            duration % 60
        )

        if minutes < 60:

            return (
                f"{minutes}m "
                f"{seconds}s"
            )

        hours = minutes // 60

        remaining_minutes = (
            minutes % 60
        )

        return (
            f"{hours}h "
            f"{remaining_minutes}m"
        )

    # ---------------------------------------------------------

    def format_datetime(
        self,
        value
    ):

        if not value:
            return "Unknown"

        try:

            return value.replace(
                "T",
                " "
            )[:19]

        except Exception:

            return str(value)

    # =========================================================
    # SCORE HELPERS
    # =========================================================

    def get_score_color(
        self,
        score
    ):

        if score >= 80:
            return "#3DDC97"

        if score >= 60:
            return "#F5C451"

        if score >= 40:
            return "#FF9F43"

        return "#FF5C5C"

    # ---------------------------------------------------------

    def get_score_status(
        self,
        score
    ):

        if score >= 80:
            return "Excellent performance"

        if score >= 60:
            return "Good performance"

        if score >= 40:
            return "Performance can be improved"

        return "Performance needs attention"

    # =========================================================
    # ERROR DISPLAY
    # =========================================================

    def show_error(
        self,
        error
    ):

        error_label = ctk.CTkLabel(
            self.content_frame,
            text=f"⚠ Analysis error: {error}",
            text_color="#FF5C5C",
            font=ctk.CTkFont(
                size=12
            )
        )

        error_label.pack(
            padx=10,
            pady=(0, 20)
        )

    # =========================================================
    # CLOSE
    # =========================================================

    def destroy(self):

        if self.figure is not None:

            try:
                plt.close(
                    self.figure
                )
            except Exception:
                pass

        super().destroy()