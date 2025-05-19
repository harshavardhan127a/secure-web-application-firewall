from datetime import datetime
import os

log_file_path = os.path.join(os.path.dirname(__file__), '../logs/waf_logs.txt')

def log_request(request, blocked, reason="Allowed"):
    log_entry = f"[{datetime.now()}] {request.remote_addr} - {request.method} {request.full_path} - {'BLOCKED' if blocked else 'ALLOWED'} - Reason: {reason}\n"
    os.makedirs(os.path.dirname(log_file_path), exist_ok=True)
    with open(log_file_path, "a") as f:
        f.write(log_entry)