import os
import json
import subprocess
import urllib.parse
import time

message_id = os.getenv("message_id")
tag = os.getenv("tag")

workflow_dir = os.environ["alfred_workflow_data"]
data_path = os.path.join(workflow_dir, "emails.json")
title = os.environ["alfred_workflow_name"]

# 📨 Open the email in Mail
if message_id:
    encoded = urllib.parse.quote(f"<{message_id}>")
    url = f"message://{encoded}"
    subprocess.run(["open", url])

# ⏱ Add a short delay so Mail has time to open the message
time.sleep(0.5)

tag_removed = False
updated_emails = []

if os.path.exists(data_path):
    with open(data_path, "r") as f:
        emails = json.load(f)

    for email in emails:
        if email.get("id") == message_id:
            tags = email.get("tags", [])
            if tag in tags:
                tags.remove(tag)
                tag_removed = True
            if tags:
                email["tags"] = tags
                updated_emails.append(email)
            # else: don't add back (removes from file)
        else:
            updated_emails.append(email)

    with open(data_path, "w") as f:
        json.dump(updated_emails, f, indent=2)

# ✅ Show notification
if tag_removed:
    subprocess.run([
        "osascript", "-e",
        f'display notification "Removed tag \\"{tag}\\" from email." with title "{title}"'
    ])
