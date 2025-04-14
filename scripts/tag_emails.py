import os
import sys
import json
import subprocess

tag = sys.argv[1].strip().replace("!", "❗")
if not tag:
    sys.exit(0)

workflow_dir = os.environ["alfred_workflow_data"]
db_path = os.path.join(workflow_dir, "emails.json")
title = os.environ["alfred_workflow_name"]

# AppleScript: get subject, sender, date, id
applescript = """
tell application "Mail"
	set selectedMessages to selection
	set output to ""
	repeat with msg in selectedMessages
		set theSubject to subject of msg
		set theSender to sender of msg
		set theDate to date received of msg
		set theID to message id of msg
		set output to output & theSubject & "||" & theSender & "||" & theDate & "||" & theID & "%%"
	end repeat
	return output
end tell
"""

result = subprocess.run(["osascript", "-e", applescript], capture_output=True, text=True)
raw_output = result.stdout.strip()

# If nothing selected
if not raw_output:
    subprocess.run([
        "osascript",
        "-e",
        f'display notification "No mail(s) selected. Select mail(s) to tag." with title "{title}"'
    ])
    sys.exit(0)

# Parse AppleScript result
emails = []
for item in raw_output.split("%%"):
    if not item.strip():
        continue
    parts = item.strip().split("||")
    if len(parts) == 4:
        emails.append({
            "subject": parts[0].strip(),
            "sender": parts[1].strip(),
            "date": parts[2].strip(),
            "id": parts[3].strip()
        })

# Load or create database
if os.path.exists(db_path):
    with open(db_path, "r") as f:
        db = json.load(f)
else:
    db = []

# Tag emails - add new entry only if same ID+tag combo doesn't exist
added = 0
for email in emails:
    already_tagged = any(
        entry["id"] == email["id"] and tag in entry.get("tags", [])
        for entry in db
    )
    if not already_tagged:
        email["tags"] = [tag]
        db.append(email)
        added += 1

# Save updated file
with open(db_path, "w") as f:
    json.dump(db, f, indent=2)

# Show notification
subprocess.run([
    "osascript", "-e",
    f'display notification "Tagged {added} email(s) with \\"{tag}\\"" with title "{title}"'
])