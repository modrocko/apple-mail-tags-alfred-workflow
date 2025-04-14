import os
import sys
import json
import subprocess
import urllib.parse

tag = sys.argv[1].strip()

workflow_dir = os.environ["alfred_workflow_data"]
db_path = os.path.join(workflow_dir, "emails.json")

with open(db_path, "r") as f:
    emails = json.load(f)

for email in emails:
    if tag in email.get("tags", []):
        message_id = email["id"]
        encoded = urllib.parse.quote(f"<{message_id}>")
        url = f"message://{encoded}"
        subprocess.run(["open", url])