import os
import sys
import json

query = sys.argv[1].strip().lower()
workflow_dir = os.environ["alfred_workflow_data"]
db_path = os.path.join(workflow_dir, "emails.json")

if not os.path.exists(db_path):
    print('{"items": []}')
    exit()

with open(db_path, "r") as f:
    emails = json.load(f)

results = []
for email in emails:
    subject = email.get("subject", "")
    sender = email.get("sender", "")
    date = email.get("date", "")
    tags_list = email.get("tags", [])
    tag = tags_list[0] if tags_list else ""
    message_id = email.get("id", "")

    if query in subject.lower() or query in sender.lower():
        results.append({
            "title": subject,
            "subtitle": f"[{tag}] • {sender} — {date}",
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

if not results:
    results.append({
        "title": "No matches found",
        "subtitle": f"No emails found for: {query}",
        "valid": False
    })

print(json.dumps({"items": results}))
