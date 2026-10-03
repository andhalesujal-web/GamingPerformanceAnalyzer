# Gaming Performance Analyzer

A Python-based desktop application for monitoring, recording, analyzing, and evaluating gaming PC performance.

The Gaming Performance Analyzer collects system performance data such as CPU usage, GPU usage, RAM usage, GPU temperature, GPU memory usage, disk information, and network statistics during gaming sessions.

It also provides session history, performance analysis, performance scoring, game profiles, graphical visualization, and PDF reports.

---

## Features

### 1. Live System Monitoring

The application provides real-time monitoring of:

- CPU usage
- CPU core count
- GPU usage
- GPU temperature
- GPU memory usage
- RAM usage
- RAM availability
- Disk usage
- Network statistics

---

### 2. Gaming Session Recording

Users can start and stop gaming sessions.

During a session, the application records performance metrics at regular intervals and stores them in an SQLite database.

Each session contains:

- Game name
- Start time
- End time
- Session duration
- CPU usage
- GPU usage
- RAM usage
- GPU temperature
- GPU memory usage

---

### 3. Session History

Previously recorded gaming sessions can be viewed from the Session History section.

The history displays:

- Game name
- Session duration
- Start time
- Analysis option

---

### 4. Performance Analysis

After a gaming session, the application analyzes the collected data.

It calculates:

- Average CPU usage
- Peak CPU usage
- Average GPU usage
- Peak GPU usage
- Average RAM usage
- Peak RAM usage
- Average GPU temperature
- Peak GPU temperature
- Average GPU memory usage
- Peak GPU memory usage

The application also generates findings and recommendations based on the recorded performance.

---

### 5. Performance Score

Each analyzed session receives a performance score between 0 and 100.

The score considers factors such as:

- CPU utilization
- RAM utilization
- GPU temperature
- GPU workload

---

### 6. Graphical Analysis

Performance data is visualized using graphs.

The analysis dashboard can display:

- CPU usage graph
- GPU usage graph
- RAM usage graph
- GPU temperature graph

This makes it easier to understand performance changes during a gaming session.

---

### 7. PDF Reports

The application can generate a PDF report for a gaming session.

The report contains:

- Session information
- Performance metrics
- Performance score
- Findings
- Recommendations
- Performance graphs

Generated reports are stored inside the `reports` directory.

---

### 8. Game Profiles

Users can create and manage game profiles.

A profile contains:

- Game name
- Resolution
- Graphics quality
- Notes

The project also includes default profiles for:

- Valorant
- GTA V
- Minecraft
- Roblox

---

### 9. Settings

The application provides configurable settings for:

- Monitoring interval
- Application appearance

Available monitoring intervals include:

- 1 second
- 2 seconds
- 3 seconds
- 5 seconds
- 10 seconds

Appearance modes:

- Dark
- Light
- System

Settings are saved locally and persist after restarting the application.

---

## Technology Stack

| Technology | Purpose |
|---|---|
| Python | Main programming language |
| CustomTkinter | Desktop graphical user interface |
| psutil | CPU, RAM, disk and network monitoring |
| NVIDIA ML | NVIDIA GPU monitoring |
| SQLite | Local database |
| Pandas | Data processing |
| Matplotlib | Performance graphs |
| ReportLab | PDF report generation |
| Pytest | Automated testing |
| Git | Version control |

---

## System Requirements

### Hardware

Recommended:

- Modern multi-core CPU
- 8 GB RAM or more
- NVIDIA GPU for GPU monitoring features
- At least 1 GB available storage

### Software

- Windows 10/11
- Python 3.13 or compatible Python version
- NVIDIA drivers for NVIDIA GPU monitoring

---

## Project Structure

```text
GamingPerformanceAnalyzer/
│
├── app/
│   ├── __init__.py
│   ├── main.py
│   │
│   ├── config/
│   │   ├── __init__.py
│   │   └── settings.py
│   │
│   ├── monitor/
│   │   ├── __init__.py
│   │   ├── cpu.py
│   │   ├── gpu.py
│   │   ├── memory.py
│   │   ├── disk.py
│   │   ├── network.py
│   │   ├── collector.py
│   │   └── monitor_loop.py
│   │
│   ├── database/
│   │   ├── __init__.py
│   │   ├── db.py
│   │   └── check_db.py
│   │
│   ├── session/
│   │   ├── __init__.py
│   │   ├── recorder.py
│   │   ├── analyzer.py
│   │   ├── performance.py
│   │   └── scoring.py
│   │
│   ├── dashboard/
│   │   ├── __init__.py
│   │   ├── window.py
│   │   ├── history.py
│   │   ├── analysis.py
│   │   ├── profiles.py
│   │   └── settings.py
│   │
│   └── report/
│       ├── __init__.py
│       └── generator.py
│
├── data/
│   ├── gaming_performance.db
│   └── settings.json
│
├── reports/
│
├── tests/
│   ├── test_database.py
│   ├── test_analyzer.py
│   ├── test_performance.py
│   └── test_scoring.py
│
├── .venv/
├── pytest.ini
├── requirements.txt
└── README.md