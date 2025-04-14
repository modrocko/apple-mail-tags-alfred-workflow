import os
import sys
import json

query = sys.argv[1].replace("!", "❗").lower() if len(sys.argv) > 1 else ""

workflow_dir = os.environ["alfred_workflow_data"]
db_path = os.path.join(workflow_dir, "emails.json")
default_tags_path = os.path.join(workflow_dir, "default-tags.json")

# Load emails
if not os.path.exists(db_path):
    print('{"items": []}')
    exit()

with open(db_path, "r") as f:
    emails = json.load(f)

# Load default tags
default_tags = []
if os.path.exists(default_tags_path):
    with open(default_tags_path, "r") as f:
        default_tags = json.load(f)

# Collect tags from emails + defaults
tag_set = set(default_tags)
for email in emails:
    tag_set.update(email.get("tags", []))

# Filter
filtered = sorted(t for t in tag_set if query in t.lower())

# Always include the typed input as a new tag option
if query and query not in [t.lower() for t in tag_set]:
    filtered.insert(0, query)

# Build results
items = []
for tag in filtered:
    items.append({
        "title": tag,
        "subtitle": "↵ to tag selected Mail message",
        "arg": tag
    })

print(json.dumps({"items": items}))
