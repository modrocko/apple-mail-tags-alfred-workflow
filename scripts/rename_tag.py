import json
import os
import sys
import subprocess

new_tag = sys.argv[1].strip().replace("!", "❗")
old_tag = os.getenv("old_tag")
workflow_dir = os.environ["alfred_workflow_data"]
db_path = os.path.join(workflow_dir, "emails.json")
title = os.environ["alfred_workflow_name"]

# Load data
with open(db_path, "r") as f:
    emails = json.load(f)

# Replace old tag with new one
for email in emails:
    if "tags" in email and old_tag in email["tags"]:
        email["tags"] = [new_tag if t == old_tag else t for t in email["tags"]]

# Save updated data
with open(db_path, "w") as f:
    json.dump(emails, f, indent=2)

# ✅ Notification
subprocess.run([
    "osascript", "-e",
    f'display notification "Tag renamed from {old_tag} to {new_tag}." with title "{title}"'
])