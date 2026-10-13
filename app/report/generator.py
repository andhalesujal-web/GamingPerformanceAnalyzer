from pathlib import Path
from datetime import datetime

import matplotlib.pyplot as plt

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.units import mm
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    Image,
    PageBreak
)

from app.database.db import get_connection
from app.session.analyzer import get_session_metrics
from app.session.performance import analyze_session_performance
from app.session.scoring import calculate_performance_score


REPORTS_DIR = Path("reports")


def get_session_info(session_id):
    """Get basic information about a session."""

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
        (session_id,)
    )

    session = cursor.fetchone()

    connection.close()

    return session


def get_graph_data(session_id):
    """Get recorded metrics for graph generation."""

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
        (session_id,)
    )

    rows = cursor.fetchall()

    connection.close()

    return rows


def create_graph_image(session_id, graph_path):
    """Create performance graphs for the PDF."""

    rows = get_graph_data(session_id)

    if not rows:
        return False

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

    figure, axes = plt.subplots(
        2,
        2,
        figsize=(10, 7)
    )

    # =========================
    # CPU
    # =========================

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

    # =========================
    # GPU
    # =========================

    valid_gpu = [
        value
        for value in gpu_values
        if value is not None
    ]

    if valid_gpu:

        gpu_x = [
            timestamps[index]
            for index, value in enumerate(gpu_values)
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

    # =========================
    # RAM
    # =========================

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

    # =========================
    # GPU TEMPERATURE
    # =========================

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

    figure.tight_layout()

    figure.savefig(
        graph_path,
        dpi=150,
        bbox_inches="tight"
    )

    plt.close(
        figure
    )

    return True


def generate_session_report(session_id):
    """
    Generate a complete PDF report for a gaming session.

    Returns the generated PDF path.
    """

    session = get_session_info(
        session_id
    )

    if session is None:
        raise ValueError(
            f"Session {session_id} was not found."
        )

    game_name = session[0]
    start_time = session[1]
    end_time = session[2]
    duration = session[3]

    metrics = get_session_metrics(
        session_id
    )

    analysis = analyze_session_performance(
        session_id
    )

    score = calculate_performance_score(
        session_id
    )

    # =========================
    # REPORT DIRECTORY
    # =========================

    REPORTS_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    safe_game_name = "".join(
        character
        if character.isalnum()
        or character in (" ", "_", "-")
        else "_"
        for character in game_name
    ).strip()

    safe_game_name = (
        safe_game_name.replace(
            " ",
            "_"
        )
        or "Game"
    )

    pdf_path = (
        REPORTS_DIR
        / f"{safe_game_name}_Session_{session_id}_Report.pdf"
    )

    graph_path = (
        REPORTS_DIR
        / f"session_{session_id}_graph.png"
    )

    # =========================
    # CREATE GRAPH
    # =========================

    graph_created = create_graph_image(
        session_id,
        graph_path
    )

    # =========================
    # PDF DOCUMENT
    # =========================

    document = SimpleDocTemplate(
        str(pdf_path),
        pagesize=A4,
        rightMargin=18 * mm,
        leftMargin=18 * mm,
        topMargin=18 * mm,
        bottomMargin=18 * mm
    )

    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        "ReportTitle",
        parent=styles["Title"],
        alignment=TA_CENTER,
        fontSize=24,
        spaceAfter=10
    )

    heading_style = ParagraphStyle(
        "ReportHeading",
        parent=styles["Heading2"],
        fontSize=15,
        spaceBefore=12,
        spaceAfter=8
    )

    normal_style = ParagraphStyle(
        "ReportNormal",
        parent=styles["BodyText"],
        fontSize=10,
        leading=15
    )

    story = []

    # =========================
    # TITLE
    # =========================

    story.append(
        Paragraph(
            "Gaming Performance Analyzer",
            title_style
        )
    )

    story.append(
        Paragraph(
            "Session Performance Report",
            ParagraphStyle(
                "Subtitle",
                parent=normal_style,
                alignment=TA_CENTER,
                fontSize=13
            )
        )
    )

    story.append(
        Spacer(
            1,
            15
        )
    )

    # =========================
    # SESSION INFORMATION
    # =========================

    story.append(
        Paragraph(
            "Session Information",
            heading_style
        )
    )

    duration_text = (
        f"{duration:.1f} seconds"
        if duration is not None
        else "Active"
    )

    session_data = [
        ["Game", game_name],
        ["Session ID", str(session_id)],
        ["Start Time", str(start_time)],
        ["End Time", str(end_time)],
        ["Duration", duration_text],
    ]

    session_table = Table(
        session_data,
        colWidths=[
            45 * mm,
            115 * mm
        ]
    )

    session_table.setStyle(
        TableStyle(
            [
                (
                    "BACKGROUND",
                    (0, 0),
                    (0, -1),
                    colors.lightgrey
                ),
                (
                    "GRID",
                    (0, 0),
                    (-1, -1),
                    0.5,
                    colors.grey
                ),
                (
                    "FONTNAME",
                    (0, 0),
                    (0, -1),
                    "Helvetica-Bold"
                ),
                (
                    "FONTNAME",
                    (1, 0),
                    (1, -1),
                    "Helvetica"
                ),
                (
                    "VALIGN",
                    (0, 0),
                    (-1, -1),
                    "MIDDLE"
                ),
                (
                    "LEFTPADDING",
                    (0, 0),
                    (-1, -1),
                    8
                ),
                (
                    "RIGHTPADDING",
                    (0, 0),
                    (-1, -1),
                    8
                ),
                (
                    "TOPPADDING",
                    (0, 0),
                    (-1, -1),
                    6
                ),
                (
                    "BOTTOMPADDING",
                    (0, 0),
                    (-1, -1),
                    6
                ),
            ]
        )
    )

    story.append(
        session_table
    )

    # =========================
    # PERFORMANCE METRICS
    # =========================

    story.append(
        Paragraph(
            "Performance Metrics",
            heading_style
        )
    )

    def format_value(value, suffix=""):
        if value is None:
            return "N/A"

        return f"{value:.1f}{suffix}"

    metrics_data = [
        [
            "Metric",
            "Average",
            "Peak"
        ],
        [
            "CPU Usage",
            format_value(
                metrics["avg_cpu"],
                "%"
            ),
            format_value(
                metrics["peak_cpu"],
                "%"
            )
        ],
        [
            "GPU Usage",
            format_value(
                metrics["avg_gpu"],
                "%"
            ),
            format_value(
                metrics["peak_gpu"],
                "%"
            )
        ],
        [
            "RAM Usage",
            format_value(
                metrics["avg_ram"],
                "%"
            ),
            format_value(
                metrics["peak_ram"],
                "%"
            )
        ],
        [
            "GPU Temperature",
            format_value(
                metrics["avg_gpu_temperature"],
                "°C"
            ),
            format_value(
                metrics["peak_gpu_temperature"],
                "°C"
            )
        ],
        [
            "GPU Memory",
            format_value(
                metrics["avg_gpu_memory"],
                " MB"
            ),
            format_value(
                metrics["peak_gpu_memory"],
                " MB"
            )
        ],
    ]

    metrics_table = Table(
        metrics_data,
        colWidths=[
            70 * mm,
            45 * mm,
            45 * mm
        ]
    )

    metrics_table.setStyle(
        TableStyle(
            [
                (
                    "BACKGROUND",
                    (0, 0),
                    (-1, 0),
                    colors.lightgrey
                ),
                (
                    "GRID",
                    (0, 0),
                    (-1, -1),
                    0.5,
                    colors.grey
                ),
                (
                    "FONTNAME",
                    (0, 0),
                    (-1, 0),
                    "Helvetica-Bold"
                ),
                (
                    "ALIGN",
                    (1, 1),
                    (-1, -1),
                    "CENTER"
                ),
                (
                    "VALIGN",
                    (0, 0),
                    (-1, -1),
                    "MIDDLE"
                ),
                (
                    "TOPPADDING",
                    (0, 0),
                    (-1, -1),
                    7
                ),
                (
                    "BOTTOMPADDING",
                    (0, 0),
                    (-1, -1),
                    7
                ),
            ]
        )
    )

    story.append(
        metrics_table
    )

    # =========================
    # SCORE
    # =========================

    story.append(
        Paragraph(
            "Performance Score",
            heading_style
        )
    )

    score_data = [
        [
            "Session Condition Score",
            f"{score:.0f} / 100"
        ]
    ]

    score_table = Table(
        score_data,
        colWidths=[
            110 * mm,
            50 * mm
        ]
    )

    score_table.setStyle(
        TableStyle(
            [
                (
                    "BACKGROUND",
                    (0, 0),
                    (0, 0),
                    colors.lightgrey
                ),
                (
                    "BACKGROUND",
                    (1, 0),
                    (1, 0),
                    colors.whitesmoke
                ),
                (
                    "GRID",
                    (0, 0),
                    (-1, -1),
                    0.5,
                    colors.grey
                ),
                (
                    "FONTNAME",
                    (0, 0),
                    (-1, -1),
                    "Helvetica-Bold"
                ),
                (
                    "ALIGN",
                    (1, 0),
                    (1, 0),
                    "CENTER"
                ),
                (
                    "FONTSIZE",
                    (1, 0),
                    (1, 0),
                    15
                ),
                (
                    "TOPPADDING",
                    (0, 0),
                    (-1, -1),
                    8
                ),
                (
                    "BOTTOMPADDING",
                    (0, 0),
                    (-1, -1),
                    8
                ),
            ]
        )
    )

    story.append(
        score_table
    )

    # =========================
    # FINDINGS
    # =========================

    story.append(
        Paragraph(
            "Performance Findings",
            heading_style
        )
    )

    for finding in analysis["findings"]:

        story.append(
            Paragraph(
                f"• {finding}",
                normal_style
            )
        )

        story.append(
            Spacer(
                1,
                4
            )
        )

    # =========================
    # RECOMMENDATIONS
    # =========================

    story.append(
        Paragraph(
            "Performance Recommendations",
            heading_style
        )
    )

    for recommendation in analysis[
        "recommendations"
    ]:

        story.append(
            Paragraph(
                f"• {recommendation}",
                normal_style
            )
        )

        story.append(
            Spacer(
                1,
                4
            )
        )

    # =========================
    # GRAPH
    # =========================

    if graph_created:

        story.append(
            PageBreak()
        )

        story.append(
            Paragraph(
                "Performance Graphs",
                heading_style
            )
        )

        story.append(
            Image(
                str(graph_path),
                width=175 * mm,
                height=122 * mm
            )
        )

    # =========================
    # FOOTER
    # =========================

    story.append(
        Spacer(
            1,
            15
        )
    )

    generated_time = datetime.now().strftime(
        "%Y-%m-%d %H:%M:%S"
    )

    story.append(
        Paragraph(
            f"Report generated on {generated_time}",
            ParagraphStyle(
                "Footer",
                parent=normal_style,
                fontSize=8,
                textColor=colors.grey
            )
        )
    )

    # =========================
    # BUILD PDF
    # =========================

    document.build(
        story
    )

    # Remove temporary graph image

    try:

        graph_path.unlink()

    except Exception:
        pass

    return pdf_path