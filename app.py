from flask import Flask, request, jsonify
from datetime import datetime, timedelta
import threading

app = Flask(__name__)
emails = {}

# Auto-delete emails after 3 hours
def cleanup_expired_emails():
    while True:
        now = datetime.utcnow()
        to_delete = [key for key, val in emails.items() if val["expires"] < now]
        for key in to_delete:
            del emails[key]
        threading.Event().wait(600)  # Check every 10 min

threading.Thread(target=cleanup_expired_emails, daemon=True).start()

@app.route('/api/incoming', methods=['POST'])
def receive_email():
    data = request.json
    to_address = data.get("to")
    content = data.get("content", "No content")
    if not to_address:
        return jsonify({"error": "Missing 'to'"}), 400

    emails.setdefault(to_address, {"messages": [], "expires": datetime.utcnow() + timedelta(hours=3)})
    emails[to_address]["messages"].append({
        "timestamp": datetime.utcnow().isoformat(),
        "content": content
    })
    return jsonify({"status": "stored"}), 200

@app.route('/api/inbox/<email>', methods=['GET'])
def get_inbox(email):
    inbox = emails.get(email)
    if not inbox:
        return jsonify({"messages": []})
    return jsonify(inbox["messages"])

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
