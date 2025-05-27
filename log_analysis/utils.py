from serializers import LogEntry
from typing import List, Optional, Dict
from datetime import datetime
import hashlib
import os


LOG_DIRECTORY = "logs"

def generate_log_id(entry: str) -> str:
    """Generate a unique log ID using SHA-1 hash."""
    return hashlib.sha1(entry.encode()).hexdigest()

def parse_log_line(line: str) -> Optional[LogEntry]:
    line = line.replace("\\t", "\t")
    parts = line.split("\t")

    if len(parts) != 4:
        return None  # Malformed line
    timestamp_str, level, component, message = parts
    try:
        timestamp = datetime.strptime(timestamp_str, "%Y-%m-%d %H:%M:%S")
    except ValueError:
        return None
    log_id = generate_log_id(line)
    return LogEntry(
        log_id=log_id,
        timestamp=timestamp,
        level=level,
        component=component,
        message=message
    )

def read_all_logs() -> List[LogEntry]:
    logs = []
    for filename in os.listdir(LOG_DIRECTORY):
        filepath = os.path.join(LOG_DIRECTORY, filename)
        
        if os.path.isfile(filepath):
            with open(filepath, "r") as f:
                for line in f:
                    entry = parse_log_line(line)
                    if entry:
                        logs.append(entry)
        else:
            print("no file")
    return logs