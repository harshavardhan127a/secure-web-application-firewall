from flask import Flask, request, Response
import requests
from waf_engine import is_malicious_request, is_blocked_ip, add_blocked_ip
from logger import log_request

app = Flask(__name__)
BACKEND_URL = "http://127.0.0.1:5001"

@app.route('/', defaults={'path': ''}, methods=["GET", "POST"])
@app.route('/<path:path>', methods=["GET", "POST"])
def proxy(path):
    client_ip = request.remote_addr
    full_url = f"{BACKEND_URL}/{path}"
    
    request_data = {
        "headers": dict(request.headers),
        "params": request.args.to_dict(),
        "body": request.get_data(as_text=True)
    }

    if is_blocked_ip(client_ip):
        log_request(request, blocked=True, reason="IP Blocked")
        return Response("403 Forbidden - IP Blocked", status=403)

    if is_malicious_request(request_data):
        add_blocked_ip(client_ip)
        log_request(request, blocked=True, reason="Malicious Payload")
        return Response("Blocked by WAF", status=403)

    log_request(request, blocked=False)
    try:
        if request.method == "POST":
            response = requests.post(full_url, data=request.form, headers={k: v for k, v in request.headers if k.lower() != 'host'})
        else:
            response = requests.get(full_url, headers={k: v for k, v in request.headers if k.lower() != 'host'})
        return Response(response.content, status=response.status_code)
    except requests.RequestException:
        return Response("502 Bad Gateway", status=502)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)