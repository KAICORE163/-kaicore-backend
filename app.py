from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime
import threading

app = Flask(__name__)
CORS(app)   # ← Enable CORS on all routes

inboxes = {}

@app.route("/")
def home():
    return "✅ KAICORE Inbox API is live"

@app.route("/api/incoming", methods=["POST"])
def receive_email():
    to_email = request.form.get("recipient")
    sender   = request.form.get("sender")
    subject  = request.form.get("subject", "(No Subject)")
    body     = request.form.get("body-plain", "")

    if not to_email:
        return "❌ Missing recipient", 400

    inbox = inboxes.setdefault(to_email, [])
    inbox.append({
        "from":    sender,
        "subject": subject,
        "body":    body,
        "time":    datetime.utcnow().isoformat()
    })

    # Schedule deletion after 3 hours
    threading.Timer(3 * 3600, lambda: inboxes.pop(to_email, None)).start()

    return "✅ Email received", 200

@app.route("/api/inbox", methods=["GET"])
def get_inbox():
    email = request.args.get("email")
    if not email:
        return "❌ Missing email", 400

    return jsonify(inboxes.get(email, []))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
