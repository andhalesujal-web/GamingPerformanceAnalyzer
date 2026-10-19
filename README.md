# Gaming Performance Analyzer

A Python desktop application that monitors computer performance during gaming sessions, records performance data, and presents session analysis through graphs and PDF reports.

## Features

- **Live system monitoring:** CPU usage, CPU core count, RAM usage and availability, GPU usage, GPU temperature, GPU memory, disk usage, and network statistics.
- **Gaming session recording:** Start and stop sessions and save collected metrics in a local SQLite database.
- **Session history:** Review recorded sessions and open their analysis.
- **Performance analysis:** View average and peak CPU, GPU, RAM, GPU temperature, and GPU memory values, along with findings and recommendations.
- **Performance score:** Calculate a session score from 0 to 100 using the application's scoring logic.
- **Graphs:** Visualize CPU, GPU, RAM, and GPU temperature during a session.
- **PDF reports:** Export session details, metrics, score, findings, recommendations, and graphs.
- **Game profiles:** Create and manage profiles with game name, resolution, graphics quality, and notes. Default profiles include Valorant, GTA V, Minecraft, and Roblox.
- **Settings:** Configure the monitoring interval and application appearance.

## Technology Stack

| Technology | Purpose |
|---|---|
| Python | Main programming language |
| CustomTkinter | Desktop user interface |
| psutil | CPU, memory, disk, and network monitoring |
| NVIDIA Management Library (`nvidia-ml-py`) | NVIDIA GPU metrics |
| SQLite | Local session and profile database |
| Pandas | Data handling and analysis |
| Matplotlib | Performance graphs |
| ReportLab | PDF report generation |
| Pytest | Automated tests |
| Git | Version control |

## Requirements

- Windows 10 or Windows 11
- Python 3.13 (the project has been tested with Python 3.13)
- NVIDIA drivers and a supported NVIDIA GPU for NVIDIA GPU metrics
- Internet access to install dependencies

CPU and memory monitoring can be useful without an NVIDIA GPU, but GPU-specific readings depend on supported NVIDIA hardware and drivers.

## Setup and Installation

Run these commands in PowerShell from the project directory.

### 1. Create a virtual environment

```powershell
python -m venv .venv
```

### 2. Activate it

```powershell
.\.venv\Scripts\Activate.ps1
```

If PowerShell blocks activation, use Command Prompt to activate the environment, or review your system's PowerShell execution-policy settings.

### 3. Install dependencies

```powershell
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Run the application

```powershell
python -m app.main
```

## Run Automated Tests

With the virtual environment activated, run:

```powershell
python -m pytest -v
```

The project currently includes tests for session analysis, database initialization, game profiles, performance analysis, and scoring.

## Project Structure

```text
GamingPerformanceAnalyzer/
├── app/
│   ├── main.py
│   ├── config/
│   │   └── settings.py
│   ├── monitor/
│   │   ├── cpu.py
│   │   ├── gpu.py
│   │   ├── memory.py
│   │   ├── disk.py
│   │   ├── network.py
│   │   ├── collector.py
│   │   └── monitor_loop.py
│   ├── database/
│   │   ├── db.py
│   │   └── check_db.py
│   ├── session/
│   │   ├── recorder.py
│   │   ├── analyzer.py
│   │   ├── performance.py
│   │   └── scoring.py
│   ├── dashboard/
│   │   ├── window.py
│   │   ├── history.py
│   │   ├── analysis.py
│   │   ├── profiles.py
│   │   └── settings.py
│   └── report/
│       └── generator.py
├── tests/
├── reports/
├── requirements.txt
├── pytest.ini
└── README.md
```

The `data/` directory is created/used locally for the SQLite database and settings. Generated PDF reports are saved in `reports/`.

## How to Use

1. Start the application.
2. Open the monitoring dashboard and review the available system metrics.
3. Start a gaming session and select/enter the game as prompted by the application.
4. Stop the session after playing.
5. Open session history and view the session analysis.
6. Review the graphs and performance findings.
7. Generate a PDF report if needed.

Exact controls and available metrics may depend on the application version and the hardware supported by the computer.

## Notes and Limitations

- GPU metrics are dependent on supported NVIDIA hardware, drivers, and the NVIDIA Management Library.
- The performance score is an application-generated indicator based on collected metrics; it is not a standardized benchmark and should not be treated as a direct measurement of FPS or game quality.
- The application records the metrics it supports; it does not claim to measure FPS or 1% low FPS unless those features are added separately.
- The SQLite database and settings are stored locally.

## Academic Project

This project demonstrates desktop GUI development, system monitoring, database operations, data analysis, visualization, report generation, and automated testing using Python.
