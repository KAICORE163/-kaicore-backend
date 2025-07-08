import os
import json
from flask import Blueprint, request
from datetime import datetime, timedelta

email_handler = Blueprint('email_handler', __name__)

# In-memory store for email inboxes
INBOXES = {}

@email_handler.route("/api/incoming", methods=["POST"])
def receive_email():
    data = request.form

    to_address = data.get("to", "").strip().lower()
    subject = data.get("subject", "")
    sender = data.get("from", "")
    text = data.get("text", "")
    timestamp = datetime.utcnow()

    if "@kaicore.ai" not in to_address:
        return "Invalid address", 400

    if to_address not in INBOXES:
        INBOXES[to_address] = []

    INBOXES[to_address].append({
        "from": sender,
        "subject": subject,
        "text": text,
        "time": timestamp.isoformat()
    })

    return "Email received", 200

# Auto-expiry cleanup (to be called periodically)
def cleanup_expired():
    now = datetime.utcnow()
    expired = now - timedelta(hours=3)
    for addr in list(INBOXES.keys()):
        INBOXES[addr] = [msg for msg in INBOXES[addr] if datetime.fromisoformat(msg["time"]) > expired]
        if not INBOXES[addr]:
            del INBOXES[addr]
