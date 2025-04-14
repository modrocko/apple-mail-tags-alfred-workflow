import os
import sys
import json
import subprocess

# Get new tag from input
new_tag = sys.argv[1].strip().replace("!", "❗")

# Get metadata from environment
message_id = os.environ.get("id", "").strip()
old_tag = os.environ.get("old_tag", "").strip()
workflow_dir = os.environ["alfred_workflow_data"]
db_path = os.path.join(workflow_dir, "emails.json")
notif_title = os.environ["alfred_workflow_name"]

# Make sure data file exists
if not os.path.exists(db_path):
    print("Data file not found")
    sys.exit(1)

# Load emails
with open(db_path, "r") as f:
    emails = json.load(f)

# Try to find the matching email by ID & reassign the tag
changed = False
for email in emails:
    if email.get("id", "") == message_id:
        tags = email.get("tags", [])
        if old_tag in tags:
            tags.remove(old_tag)
        if new_tag not in tags:
            tags.append(new_tag)
        email["tags"] = tags
        changed = True
        break

# Save changes and show notification
if changed:
    with open(db_path, "w") as f:
        json.dump(emails, f, indent=2)

    print(f"✅ Reassigned tag '{old_tag}' → '{new_tag}'")

    notif_text = f"Email reassigned from '{old_tag}' to '{new_tag}'"
    subprocess.run([
        "osascript", "-e",
        f'display notification "{notif_text}" with title "{notif_title}"'
    ])
else:
    print("❌ Email not found or tag not changed")