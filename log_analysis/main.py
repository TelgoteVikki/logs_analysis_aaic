from fastapi_pagination import Page, add_pagination, paginate
from fastapi import FastAPI, HTTPException, Query

from typing import Optional, Dict
from datetime import datetime

from utils import read_all_logs, clear_cache
from serializers import LogEntry

app = FastAPI(title="Log File Data Access and Analysis API")

# --- API ENDPOINTS ---
@app.get("/logs", response_model=Page[LogEntry])
def get_logs(
    level: Optional[str] = Query(None),
    component: Optional[str] = Query(None),
    start_time: Optional[datetime] = Query(None),
    end_time: Optional[datetime] = Query(None)
):
    try:
        logs = read_all_logs()
       
        # Filtering Based on query parameters
        if level:
            logs = [log for log in logs if log.level == level]
        if component:
            logs = [log for log in logs if log.component == component]
        if start_time:
            logs = [log for log in logs if log.timestamp >= start_time]
        if end_time:
            logs = [log for log in logs if log.timestamp <= end_time]

        return paginate(logs)
    
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

@app.post("/cleare/logs-cache")
def cleare_log_cache():
    clear_cache()
    return {"message": "Log cache cleared successfully."}


add_pagination(app)
