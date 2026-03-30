"""
List, pause, resume, and delete monitors.

Shows all lifecycle operations for managing monitors.
"""

import json

from scrapegraph_py import Client

client = Client()  # uses SGAI_API_KEY env var

# List all monitors
monitors = client.monitor.list()
print("All monitors:", json.dumps(monitors, indent=2))

# If you have a monitor ID, you can manage it:
# monitor_id = "your-monitor-id"

# Get details
# details = client.monitor.get(monitor_id)
# print("Details:", json.dumps(details, indent=2))

# Pause a monitor
# paused = client.monitor.pause(monitor_id)
# print("Paused:", json.dumps(paused, indent=2))

# Resume a paused monitor
# resumed = client.monitor.resume(monitor_id)
# print("Resumed:", json.dumps(resumed, indent=2))

# Delete a monitor
# deleted = client.monitor.delete(monitor_id)
# print("Deleted:", json.dumps(deleted, indent=2))

client.close()
