from dotenv import load_dotenv
load_dotenv()

import json
import signal
import time
from scrapegraph_py import ScrapeGraphAI, MonitorCreateRequest, JsonFormatConfig

sgai = ScrapeGraphAI()

res = sgai.monitor.create(MonitorCreateRequest(
    url="https://time.is/",
    name="Time Monitor",
    interval="*/10 * * * *",
    formats=[JsonFormatConfig(
        prompt="Extract the current time",
        schema={
            "type": "object",
            "properties": {
                "time": {"type": "string"},
            },
            "required": ["time"],
        },
    )],
))

if res.status != "success" or not res.data:
    print("Failed to create monitor:", res.error)
    exit(1)

monitor_id = res.data.cron_id
print(f"Monitor created: {monitor_id}")
print(f"Interval: {res.data.interval}")
print("\nPolling for activity (Ctrl+C to stop)...\n")

def cleanup(_sig, _frame):
    print("\nStopping monitor...")
    sgai.monitor.delete(monitor_id)
    print("Monitor deleted")
    exit(0)

signal.signal(signal.SIGINT, cleanup)

seen_ids = set()

while True:
    activity = sgai.monitor.activity(monitor_id)
    if activity.status == "success" and activity.data:
        for tick in activity.data.ticks:
            if tick.id in seen_ids:
                continue
            seen_ids.add(tick.id)

            changes = "CHANGED" if tick.changed else "no change"
            print(f"[{tick.created_at}] {tick.status} - {changes} ({tick.elapsed_ms}ms)")
            diffs = tick.diffs.model_dump(exclude_none=True)
            if diffs:
                print(f"  Diffs: {json.dumps(diffs, indent=2)}")
            elif tick.changed:
                print("  (no diffs data)")
    time.sleep(30)
