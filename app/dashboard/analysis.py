import customtkinter as ctk
import matplotlib.pyplot as plt

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from app.database.db import get_connection
from app.session.analyzer import get_session_metrics
from app.session.performance import analyze_performance
from app.session.scoring import calculate_performance_score


class SessionAnalysis(ctk.CTkToplevel):

    def __init__(self, parent, session_id):
        super().__init__(parent)

        self.parent = parent
        self.session_id = session_id

        self.title("Session Analysis")
        self.geometry("1100x950")
        self.minsize(900, 750)

        self.create_interface()
        self.load_analysis()

    # =========================================================
    # INTERFACE
    # =========================================================

    def create_interface(self):

        title = ctk.CTkLabel(
            self,
            text="SESSION ANALYSIS",
            font=ctk.CTkFont(
                size=28,
                weight="bold"
            )
        )

        title.pack(
            pady=(20, 5)
        )

        self.game_label = ctk.CTkLabel(
            self,
            text="Game: Loading...",
            font=ctk.CTkFont(size=16)
        )

        self.game_label.pack(
            pady=(0, 15)
        )

        # =====================================================
        # SCROLLABLE CONTENT
        # =====================================================

        self.content_frame = ctk.CTkScrollableFrame(
            self
        )

        self.content_frame.pack(
            padx=25,
            pady=5,
            fill="both",
            expand=True
        )

        # =====================================================
        # SUMMARY
        # =====================================================

        self.summary_frame = ctk.CTkFrame(
            self.content_frame
        )

        self.summary_frame.pack(
            fill="x",
            pady=10
        )

        self.avg_cpu_label = self.create_metric(
            self.summary_frame,
            "Average CPU",
            0,
            0
        )

        self.peak_cpu_label = self.create_metric(
            self.summary_frame,
            "Peak CPU",
            0,
            1
        )

        self.avg_gpu_label = self.create_metric(
            self.summary_frame,
            "Average GPU",
            0,
            2
        )

        self.peak_gpu_label = self.create_metric(
            self.summary_frame,
            "Peak GPU",
            1,
            0
        )

        self.avg_ram_label = self.create_metric(
            self.summary_frame,
            "Average RAM",
            1,
            1
        )

        self.peak_ram_label = self.create_metric(
            self.summary_frame,
            "Peak RAM",
            1,
            2
        )

        self.avg_temp_label = self.create_metric(
            self.summary_frame,
            "Average GPU Temp",
            2,
            0
        )

        self.peak_temp_label = self.create_metric(
            self.summary_frame,
            "Peak GPU Temp",
            2,
            1
        )

        self.avg_vram_label = self.create_metric(
            self.summary_frame,
            "Average VRAM",
            2,
            2
        )

        # =====================================================
        # PERFORMANCE SCORE
        # =====================================================

        score_frame = ctk.CTkFrame(
            self.content_frame
        )

        score_frame.pack(
            fill="x",
            pady=10
        )

        score_title = ctk.CTkLabel(
            score_frame,
            text="PERFORMANCE SCORE",
            font=ctk.CTkFont(
                size=16,
                weight="bold"
            )
        )

        score_title.pack(
            pady=(15, 5)
        )

        self.score_label = ctk.CTkLabel(
            score_frame,
            text="-- / 100",
            font=ctk.CTkFont(
                size=32,
                weight="bold"
            )
        )

        self.score_label.pack(
            pady=(0, 15)
        )

        # =====================================================
        # GRAPH SECTION
        # =====================================================

        graph_title = ctk.CTkLabel(
            self.content_frame,
            text="PERFORMANCE GRAPH",
            font=ctk.CTkFont(
                size=20,
                weight="bold"
            )
        )

        graph_title.pack(
            pady=(20, 10)
        )

        self.graph_frame = ctk.CTkFrame(
            self.content_frame
        )

        self.graph_frame.pack(
            fill="both",
            expand=True,
            pady=10
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
            )
        )

        findings_title.pack(
            pady=(20, 5)
        )

        self.findings_box = ctk.CTkTextbox(
            self.content_frame,
            height=130
        )

        self.findings_box.pack(
            fill="x",
            pady=(5, 15)
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
            )
        )

        recommendations_title.pack(
            pady=(10, 5)
        )

        self.recommendations_box = ctk.CTkTextbox(
            self.content_frame,
            height=150
        )

        self.recommendations_box.pack(
            fill="x",
            pady=(5, 15)
        )

        self.recommendations_box.configure(
            state="disabled"
        )

        # =====================================================
        # PDF REPORT BUTTON
        # =====================================================

        self.report_button = ctk.CTkButton(
            self.content_frame,
            text="GENERATE PDF REPORT",
            command=self.generate_pdf_report,
            height=40
        )

        self.report_button.pack(
            pady=(5, 25)
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
            parent
        )

        card.grid(
            row=row,
            column=column,
            padx=8,
            pady=8,
            sticky="nsew"
        )

        parent.grid_columnconfigure(
            column,
            weight=1
        )

        title_label = ctk.CTkLabel(
            card,
            text=title,
            font=ctk.CTkFont(
                size=13,
                weight="bold"
            )
        )

        title_label.pack(
            pady=(12, 5)
        )

        value_label = ctk.CTkLabel(
            card,
            text="--",
            font=ctk.CTkFont(
                size=22,
                weight="bold"
            )
        )

        value_label.pack(
            pady=(0, 12)
        )

        return value_label

    # =========================================================
    # GET SESSION INFORMATION
    # =========================================================

    def get_session_info(self):

        connection = get_connection()

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

        session = cursor.fetchone()

        connection.close()

        return session

    # =========================================================
    # GET GRAPH DATA
    # =========================================================

    def get_graph_data(self):

        connection = get_connection()

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

        rows = cursor.fetchall()

        connection.close()

        return rows

    # =========================================================
    # LOAD ANALYSIS
    # =========================================================

    def load_analysis(self):

        try:

            session = self.get_session_info()

            if session is None:

                self.game_label.configure(
                    text="Session not found."
                )

                return

            game_name = session[0]
            duration = session[3]

            duration_text = (
                f"{duration:.1f} seconds"
                if duration is not None
                else "Active"
            )

            self.game_label.configure(
                text=(
                    f"Game: {game_name}  |  "
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
                text=f"{metrics['avg_cpu']:.1f}%"
            )

            self.peak_cpu_label.configure(
                text=f"{metrics['peak_cpu']:.1f}%"
            )

            # GPU

            if metrics["avg_gpu"] is not None:

                self.avg_gpu_label.configure(
                    text=f"{metrics['avg_gpu']:.1f}%"
                )

                self.peak_gpu_label.configure(
                    text=f"{metrics['peak_gpu']:.1f}%"
                )

            else:

                self.avg_gpu_label.configure(
                    text="N/A"
                )

                self.peak_gpu_label.configure(
                    text="N/A"
                )

            # RAM

            self.avg_ram_label.configure(
                text=f"{metrics['avg_ram']:.1f}%"
            )

            self.peak_ram_label.configure(
                text=f"{metrics['peak_ram']:.1f}%"
            )

            # GPU TEMPERATURE

            if metrics["avg_gpu_temperature"] is not None:

                self.avg_temp_label.configure(
                    text=(
                        f"{metrics['avg_gpu_temperature']:.1f}°C"
                    )
                )

                self.peak_temp_label.configure(
                    text=(
                        f"{metrics['peak_gpu_temperature']:.1f}°C"
                    )
                )

            else:

                self.avg_temp_label.configure(
                    text="N/A"
                )

                self.peak_temp_label.configure(
                    text="N/A"
                )

            # VRAM

            if metrics["avg_gpu_memory"] is not None:

                self.avg_vram_label.configure(
                    text=(
                        f"{metrics['avg_gpu_memory']:.0f} MB"
                    )
                )

            else:

                self.avg_vram_label.configure(
                    text="N/A"
                )

            # =================================================
            # PERFORMANCE SCORE
            # =================================================

            score = calculate_performance_score(
                self.session_id
            )

            self.score_label.configure(
                text=f"{score:.0f} / 100"
            )

            # =================================================
            # SMART ANALYSIS
            # =================================================

            analysis = analyze_performance(
                self.session_id
            )

            # =================================================
            # FINDINGS
            # =================================================

            self.findings_box.configure(
                state="normal"
            )

            self.findings_box.delete(
                "1.0",
                "end"
            )

            for finding in analysis["findings"]:

                self.findings_box.insert(
                    "end",
                    f"• {finding}\n\n"
                )

            self.findings_box.configure(
                state="disabled"
            )

            # =================================================
            # RECOMMENDATIONS
            # =================================================

            self.recommendations_box.configure(
                state="normal"
            )

            self.recommendations_box.delete(
                "1.0",
                "end"
            )

            for recommendation in analysis[
                "recommendations"
            ]:

                self.recommendations_box.insert(
                    "end",
                    f"• {recommendation}\n\n"
                )

            self.recommendations_box.configure(
                state="disabled"
            )

            # =================================================
            # GRAPH
            # =================================================

            self.create_graph()

        except Exception as error:

            self.game_label.configure(
                text=f"Analysis error: {error}"
            )

    # =========================================================
    # GENERATE PDF REPORT
    # =========================================================

    def generate_pdf_report(self):
        """Generate a PDF report for the current session."""

        try:

            from app.report.generator import (
                generate_session_report
            )

            pdf_path = generate_session_report(
                self.session_id
            )

            self.report_button.configure(
                text="PDF REPORT CREATED",
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
    # CREATE PERFORMANCE GRAPH
    # =========================================================

    def create_graph(self):

        rows = self.get_graph_data()

        if not rows:

            no_data_label = ctk.CTkLabel(
                self.graph_frame,
                text="No graph data available."
            )

            no_data_label.pack(
                pady=30
            )

            return

        # =====================================================
        # PREPARE DATA
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
        # CREATE FIGURE
        # =====================================================

        figure, axes = plt.subplots(
            2,
            2,
            figsize=(10, 7)
        )

        # =====================================================
        # CPU
        # =====================================================

        axes[0, 0].plot(
            timestamps,
            cpu_values,
            marker="o",
            markersize=3
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

        axes[0, 0].grid(
            True,
            alpha=0.3
        )

        # =====================================================
        # GPU
        # =====================================================

        valid_gpu = [
            value
            for value in gpu_values
            if value is not None
        ]

        if valid_gpu:

            gpu_x = [
                timestamps[index]
                for index, value in enumerate(
                    gpu_values
                )
                if value is not None
            ]

            axes[0, 1].plot(
                gpu_x,
                valid_gpu,
                marker="o",
                markersize=3
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

        axes[0, 1].grid(
            True,
            alpha=0.3
        )

        # =====================================================
        # RAM
        # =====================================================

        axes[1, 0].plot(
            timestamps,
            ram_values,
            marker="o",
            markersize=3
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

        axes[1, 0].grid(
            True,
            alpha=0.3
        )

        # =====================================================
        # TEMPERATURE
        # =====================================================

        valid_temperature = [
            value
            for value in temperature_values
            if value is not None
        ]

        if valid_temperature:

            temp_x = [
                timestamps[index]
                for index, value in enumerate(
                    temperature_values
                )
                if value is not None
            ]

            axes[1, 1].plot(
                temp_x,
                valid_temperature,
                marker="o",
                markersize=3
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

        axes[1, 1].grid(
            True,
            alpha=0.3
        )

        # =====================================================
        # LAYOUT
        # =====================================================

        figure.tight_layout(
            pad=2.0
        )

        # =====================================================
        # EMBED GRAPH
        # =====================================================

        canvas = FigureCanvasTkAgg(
            figure,
            master=self.graph_frame
        )

        canvas.draw()

        canvas_widget = canvas.get_tk_widget()

        canvas_widget.pack(
            fill="both",
            expand=True,
            padx=10,
            pady=10
        )