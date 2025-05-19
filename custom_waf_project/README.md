# Secure Web Application Firewall (WAF)

## 📌 How to Run

1. Install Python and Flask
2. Start your real backend server (on port 5001)
3. Run the WAF:

```bash
pip install flask requests
python app/main.py
```

4. Access through `http://localhost:8080`

## 🧠 Features

- Detects basic XSS, SQLi, command injections
- Temporarily blocks IPs on detection
- Logs requests with reasons

## 📄 Customize Rules

Edit `app/rules.json` to add/remove patterns.