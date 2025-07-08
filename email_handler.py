from flask import request
from datetime import datetime, timedelta
import os, json

INBOX_DIR = "inboxes"

if not os.path.exists(INBOX_DIR):
    os.makedirs(INBOX_DIR)

def save_email_to_inbox(data):
    to_address = data.get("to", "")
    email_user = to_address.split("@")[0].lower()

    inbox_file = os.path.join(INBOX_DIR, f"{email_user}.json")
    
    inbox = []
    if os.path.exists(inbox_file):
        with open(inbox_file, "r") as f:
            inbox = json.load(f)

    email_obj = {
        "from": data.get("from"),
        "subject": data.get("subject", "No subject"),
        "body": data.get("text", ""),
        "time": datetime.utcnow().isoformat()
    }

    inbox.append(email_obj)

    with open(inbox_file, "w") as f:
        json.dump(inbox, f, indent=2)

    return True
