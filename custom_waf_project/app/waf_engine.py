import re
import json
import time
import os

BLOCK_DURATION = 300
BLOCKED_IPS = {}

rules_path = os.path.join(os.path.dirname(__file__), 'rules.json')
with open(rules_path) as file:
    RULES = json.load(file)

def is_malicious_request(data):
    content = f"{data['params']} {data['body']} {data['headers']}"
    for pattern in RULES.get("patterns", []):
        if re.search(pattern, content, re.IGNORECASE):
            return True
    return False

def add_blocked_ip(ip):
    BLOCKED_IPS[ip] = time.time()

def is_blocked_ip(ip):
    if ip in BLOCKED_IPS and (time.time() - BLOCKED_IPS[ip]) < BLOCK_DURATION:
        return True
    elif ip in BLOCKED_IPS:
        del BLOCKED_IPS[ip]
    return False