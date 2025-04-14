import os
import json
import sys

# Get typed input from Alfred
query = sys.argv[1].lower() if len(sys.argv) > 1 else ""

# Get workflow directory path
workflow_dir = os.environ["alfred_workflow_data"]
db_path = os.path.join(workflow_dir, "emails.json")

# Return nothing if file doesn't exist
if not os.path.exists(db_path):
    print('{"items": []}')
    exit()

# Load email data
with open(db_path, "r") as f:
    emails = json.load(f)

# Count how many times each tag appears
tag_counts = {}
for email in emails:
    for tag in email.get("tags", []):
        tag_counts[tag] = tag_counts.get(tag, 0) + 1

# Filter & sort tags
filtered_tags = sorted(tag for tag in tag_counts if query in tag.lower()) if query else sorted(tag_counts)

# Build Alfred results
items = []
for tag in filtered_tags:
    count = tag_counts[tag]
    items.append({
        "title": tag,
        "subtitle": f"{count} email{'s' if count != 1 else ''} • ↵ view • ⌘ remove • ⌥ rename • ⌃ tag • ⇧ view all",
        "arg": tag,
        "mods": {
            "cmd": {
                "arg": tag,
                "subtitle": f"Remove tag: {tag}"
            },
            "alt": {
                "arg": tag,
                "subtitle": f"Rename tag: {tag}",
                "variables": {
                    "old_tag": tag
                }
            },
            "ctrl": {
                "arg": tag,
                "subtitle": f"Tag mail with: {tag}"
            },
            "shift": {
                "arg": tag,
                "subtitle": "Open all emails with: {tag}"
            }
        }
    })

# Output to Alfred
print(json.dumps({"items": items}))
