# Airflow Project

## Overview
This project demonstrates an Apache Airflow workflow with data asset management and inter-DAG dependencies. It implements a modern Airflow architecture using decorators and asset-based scheduling.

## Project Structure
```
Airflow_Project/
├── dags/
│   ├── data_fetch.py      # Producer DAG that fetches and materializes weather data
│   └── data_report.py     # Consumer DAG that reads and analyzes the materialized data
└── README.md              # This file
```

## DAGs Overview

### 1. **data_fetch** (`dags/data_fetch.py`)
**Purpose:** Fetches raw weather data from an API, transforms it, and materializes it as a data asset.

**Tasks:**
- `prepare_storage()` - Creates the storage directory at `/opt/airflow/data`
- `fetch_api_data()` - Simulates an API call to retrieve weather data (city, temperature, unit)
- `transform_data()` - Cleans and enriches the data by adding metadata (processing timestamp, status)
- `materialize_asset()` - Writes the processed data to `weather_report.json` and marks it as an outlet asset

**Output Asset:**
- `weather_data_asset` - File-based asset at `file:///opt/airflow/data/weather_report.json`

**Execution Flow:**
```
prepare_storage() → fetch_api_data() → transform_data() → materialize_asset()
```

---

### 2. **data_report** (`dags/data_report.py`)
**Purpose:** Consumes the weather data asset produced by the `data_fetch` DAG and generates analysis/reports.

**Tasks:**
- `read_asset()` - Reads the materialized `weather_report.json` file and prints analysis

**Trigger:**
- Scheduled based on the `weather_data_asset` produced by `data_fetch`
- Uses asset-based scheduling: only runs when the asset is updated

**Execution Flow:**
```
read_asset()
```

---

## Key Concepts

### Asset-Based Dependencies
This project uses Apache Airflow's **Asset-Based Scheduling** for inter-DAG communication:
- `data_fetch` **produces** the `weather_data_asset`
- `data_report` **consumes** the same asset
- When `data_fetch` completes and materializes the asset, `data_report` is automatically triggered

This decouples DAGs and allows for data-driven workflows without hardcoded task dependencies.

---

## Setup & Configuration

### Prerequisites
- Apache Airflow 2.7+ (supports decorators and asset scheduling)
- Python 3.8+
- Storage directory accessible at `/opt/airflow/data/`

### Installation
1. Ensure your Airflow environment is configured
2. Place the `dags/` folder in your Airflow `DAGS_FOLDER`
3. Trigger the `data_fetch` DAG to initialize the workflow

### Running the DAGs
1. **Manually trigger `data_fetch`:**
   - Airflow UI → DAGs → `data_fetch` → Trigger
   - This fetches data and materializes the asset

2. **`data_report` will auto-trigger:**
   - Once `data_fetch` completes, `data_report` automatically runs
   - Reads the asset and performs analysis

---

## Data Flow

```
External API
    ↓
data_fetch DAG
    ├── prepare_storage
    ├── fetch_api_data
    ├── transform_data
    └── materialize_asset → weather_report.json (Asset)
                              ↓
                        data_report DAG
                              ↓
                          read_asset
                              ↓
                          Analysis Output
```

---

## Example Output

When `data_fetch` completes:
```json
{
  "city": "New York",
  "temp": 22,
  "unit": "C",
  "processed_at": "2024-01-15T10:30:45.123456",
  "status": "cleansed"
}
```

`data_report` then reads this and prints:
```
Analyzing data for New York: 22°C
```

---

## Future Enhancements
- Replace simulated API calls with real weather APIs (e.g., OpenWeatherMap)
- Add data validation and error handling
- Implement multiple asset producers for data fusion workflows
- Add alerting based on temperature thresholds
- Store processed data in a database instead of JSON files

---

## Contributing
Follow the project standards defined in `.claude/CLAUDE.md`:
- Use PEP 8 for Python code style
- Add type hints and docstrings
- Maintain clear commit messages
- Keep the main branch stable

---

## Notes
- All file paths are absolute (`/opt/airflow/data/`) and should be adjusted based on your Airflow installation
- The API data fetch is simulated; replace with actual API calls as needed
- Asset-based scheduling requires Airflow 2.7+
