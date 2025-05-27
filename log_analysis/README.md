# logs_analysis_aaic

# Log File Data Access and Analysis API

This project provides a RESTful API using FastAPI that reads log files from a local directory and allows you to query and analyze log entries.

---
Project Structure

.
├── log_analysis/
│   ├── __pycache__/
│   ├── logs/                # Folder containing log files (e.g., sample.log)
│   ├── main.py              # FastAPI application entry point
│   ├── serializers.py       # Pydantic models and response schemas
│   ├── utils.py             # Helper functions for reading and filtering logs
│   ├── requirements.txt     # Python dependencies
│   └── README.md            # Project documentation

## Log File Format

Log files must be placed inside the `logs/` directory and should follow this format:

Timestamp\tLevel\tComponent\tMessage

Create log file with below sample data.

Sample Test File
You can create a sample log file inside the logs/ directory:

logs/sample.log
With content:

2025-05-07 10:00:00\tINFO\tUserAuth\tUser 'john.doe' logged in successfully.
2025-05-07 10:00:20\tERROR\tPayment\tTransaction failed for user 'jane.doe'.

Sample:

2025-05-07 10:00:00\tINFO\tUserAuth\tUser 'john.doe' logged in successfully.
2025-05-07 10:00:15\tWARNING\tGeoIP\tCould not resolve IP address '192.168.1.100'.
2025-05-07 10:00:20\tERROR\tPayment\tTransaction failed for user 'jane.doe'.
2025-05-07 10:00:25\tINFO\tUserAuth\tUser 'alice.smith' logged out.


> Each line must use tabs (`\t`) between fields — not spaces.


## Features

- Read and parse log entries from all `.log` files in the `logs/` directory.
- Filter logs by:
  - Log level (e.g., `ERROR`)
  - Component (e.g., `UserAuth`)
  - Time range (`start_time`, `end_time`)
- Retrieve individual logs by unique ID.
- Get summary statistics:
  - Total logs
  - Logs per level
  - Logs per component

---

## Installation

### 1. Clone the repo

```bash
git clone https://github.com/TelgoteVikki/logs_analysis_aaic.git
cd log_analysis
2. Create virtual environment

python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
3. Install dependencies

pip install -r requirements.txt
Run the API

uvicorn main:app --reload
This will start the server at: http://127.0.0.1:8000

API Endpoints
GET /logs

#Pagination
GET logs?page=1&size=10

Retrieve all logs (optionally filtered).

Query Parameters:

level: e.g., ERROR

component: e.g., UserAuth

start_time: e.g., 2025-05-07 10:00:00

end_time: e.g., 2025-05-07 10:00:30

Example:


GET /logs?level=ERROR&component=Payment
GET /logs/{log_id}
Get a single log entry by its ID.

GET /logs/stats

Returns:

json
{
  "total_logs": 100,
  "logs_per_level": {
    "INFO": 60,
    "ERROR": 20,
    "WARNING": 20
  },
  "logs_per_component": {
    "UserAuth": 40,
    "Payment": 30,
    "GeoIP": 30
  }
}

POST /cleare/logs-cache

NOTE: To optimize performance, the application uses caching to avoid re-reading and re-parsing log files on every request. This significantly improves response times for log retrieval APIs

You can clear the log cache to ensure updated logs are reloaded. However, instead of exposing a manual "Clear Cache" API, we can use a scheduled cron job to periodically clear the cache at defined intervals.

This approach ensures the cache stays up-to-date while keeping the system efficient and secure.
