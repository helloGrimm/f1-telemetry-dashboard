# 📊 F1 Data Analytics Dashboard

This project is a Formula 1 data visualization and analysis tool that fetches data from the Ergast/Jolpica API and provides structured race insights, including results, lap times, pit stops, and circuit layouts. The Python layer is integrated with LabVIEW 2026 and is executed directly from LabVIEW (no manual run required).

# 📂 Repository Structure

f1_api.py – Python API layer for fetching and processing F1 data (seasons, races, results, lap times, pit stops, circuits).  
f1.vi – LabVIEW 2026 main interface for data visualization and user interaction.  
circuits/ – Local GeoJSON files containing F1 track layouts used for circuit rendering.

# 🛠️ Features

- Season and race calendar retrieval (1950–present)
- Detailed race results (drivers, teams, positions, points)
- Lap-by-lap analysis per driver
- Pit stop tracking
- Circuit geometry visualization using GeoJSON
- Integration with LabVIEW dashboards

# 🔗 Data Source

Ergast / Jolpica F1 API: https://api.jolpi.ca/ergast/

# ⚙️ Requirements

- Python 3.12
- LabVIEW 2026

Note: The Python code is executed and managed directly by LabVIEW, so manual execution is not required.

# 🧠 How It Works

LabVIEW calls Python functions from `f1_api.py` to dynamically fetch and process F1 data. The processed results are then used for visualization inside the LabVIEW interface.
