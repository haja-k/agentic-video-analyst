#!/usr/bin/env python3
"""Create video registry from existing uploads"""

import json
from pathlib import Path
import re

uploads_dir = Path("uploads")
videos = {}

# Pattern to extract video_id from filename: {video_id}_{original_name}
pattern = r'^([a-f0-9-]+)_(.+)$'

for video_file in uploads_dir.glob("*.mp4"):
    filename = video_file.name
    match = re.match(pattern, filename)
    
    if match:
        video_id = match.group(1)
        videos[video_id] = str(video_file.absolute())
        print(f"Added: {video_id} -> {video_file.name}")

# Save registry
registry_path = uploads_dir / "video_registry.json"
with open(registry_path, 'w') as f:
    json.dump(videos, f, indent=2)

print(f"\nCreated registry with {len(videos)} videos")
print(f"Saved to: {registry_path}")
