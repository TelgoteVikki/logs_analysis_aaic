from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import JSONResponse

from typing import List, Optional, Dict
from datetime import datetime

from utils import generate_log_id, parse_log_line, read_all_logs, clear_cache
from serializers import LogEntry


app = FastAPI(title="Log File Data Access and Analysis API")


# --- API ENDPOINTS ---
@app.get("/logs", response_model=List[LogEntry])
def get_logs(
    level: Optional[str] = Query(None),
    component: Optional[str] = Query(None),
    start_time: Optional[datetime] = Query(None),
    end_time: Optional[datetime] = Query(None),
    skip: int = 0,
    limit: int = 10
):
    try:
        logs = read_all_logs()

        if skip < 0 or limit < 1:
            raise HTTPException(status_code=400, detail="Invalid pagination parameters: start must be >= 0 and limit must be >= 1")


        # Filtering Based on query parameters
        if level:
            logs = [log for log in logs if log.level == level]
        if component:
            logs = [log for log in logs if log.component == component]
        if start_time:
            logs = [log for log in logs if log.timestamp >= start_time]
        if end_time:
            logs = [log for log in logs if log.timestamp <= end_time]

        return logs[skip:skip + limit]  #With page limit
    
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=f"Value error: {str(ve)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail="An unexpected error occurred while fetching logs.")

@app.get("/logs/stats")
def get_stats():
    logs = read_all_logs()
    total = len(logs)
    level_counts: Dict[str, int] = {}
    component_counts: Dict[str, int] = {}

    try:
        for log in logs:
            level_counts[log.level] = level_counts.get(log.level, 0) + 1
            component_counts[log.component] = component_counts.get(log.component, 0) + 1

        return {
            "total_logs": total,
            "by_level": level_counts,
            "by_component": component_counts
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail="An unexpected error occurred while fetching stats.")

@app.get("/logs/{log_id}", response_model=LogEntry)
def get_log_by_id(log_id: str):
    logs = read_all_logs()
    for log in logs:
        if log.log_id == log_id:
            return log
    raise HTTPException(status_code=404, detail="Log entry not found")

@app.post("/refresh/logs")
def refresh_log_cache():
    clear_cache()
    return {"message": "Log cache cleared successfully."}

