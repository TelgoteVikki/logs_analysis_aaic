from pydantic import BaseModel
from datetime import datetime

class LogEntry(BaseModel):
    log_id: str
    timestamp: datetime
    level: str
    component: str
    message: str