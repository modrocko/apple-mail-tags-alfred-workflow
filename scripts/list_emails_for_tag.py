import os
import sys
import json

tag = sys.argv[1].strip()
workflow_dir = os.environ["alfred_workflow_data"]
db_path = os.path.join(workflow_dir, "emails.json")

if not os.path.exists(db_path):
    print('{"items": []}')
    exit()

with open(db_path, "r") as f:
    emails = json.load(f)

items = []
for email in emails:
    if tag in email.get("tags", []):
        subject = email["subject"]
        sender = email["sender"]
        date = email["date"]
        message_id = email.get("id", "")
        items.append({
            "title": subject,
            "subtitle": f"{sender} — {date}",
            "arg": message_id,
            "mods": {
                "cmd": {
                    "arg": f"{message_id}||{tag}",
                    "subtitle": f"⌘↵ to remove tag '{tag}' from this email"
                },
                "alt": {
                    "arg": message_id,
                    "subtitle": f"⌥↵ to open & remove tag '{tag}'",
                    "variables": {
                        "tag": tag
                    }
                },
                "ctrl": {
                    "arg": "reassign",
                    "subtitle": f"⌃↵ to reassign tag from '{tag}'",
                    "variables": {
                        "id": message_id,
                        "old_tag": tag
                    }
                }
            }
        })

print(json.dumps({"items": items}))
