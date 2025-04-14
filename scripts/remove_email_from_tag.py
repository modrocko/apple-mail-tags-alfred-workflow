import os
import sys
import json
import subprocess

# Input is something like: message_id||tag
parts = sys.argv[1].split("||")
if len(parts) != 2:
    sys.exit()

message_id = parts[0].strip()
tag_to_remove = parts[1].strip()

workflow_dir = os.environ["alfred_workflow_data"]
db_path = os.path.join(workflow_dir, "emails.json")
title = os.environ["alfred_workflow_name"]

if not os.path.exists(db_path):
    sys.exit()

with open(db_path, "r") as f:
    emails = json.load(f)

# Build new list, excluding emails that end up with no tags
updated = []
tag_removed = False

for email in emails:
    if email.get("id") == message_id:
        tags = email.get("tags", [])
        if tag_to_remove in tags:
            tags.remove(tag_to_remove)
            tag_removed = True
        if tags:
            email["tags"] = tags
            updated.append(email)
    else:
        updated.append(email)

with open(db_path, "w") as f:
    json.dump(updated, f, indent=2)

# ✅ Notification if tag was removed
if tag_removed:
    subprocess.run([
        "osascript", "-e",
        f'display notification "Email removed from \\"{tag_to_remove}\\"" with title "{title}"'
    ])