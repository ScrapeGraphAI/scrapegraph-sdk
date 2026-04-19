from dotenv import load_dotenv
load_dotenv()

import asyncio
import json
from scrapegraph_py import AsyncScrapeGraphAI, MonitorCreateRequest, JsonFormatConfig

async def main():
    async with AsyncScrapeGraphAI() as sgai:
        res = await sgai.monitor.create(MonitorCreateRequest(
            url="https://time.is/",
            name="Time Monitor with Webhook",
            interval="*/10 * * * *",
            webhook_url="https://your-webhook-endpoint.com/hook",
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
            return

        monitor_id = res.data.cron_id
        print(f"Monitor created: {monitor_id}")
        print(f"Interval: {res.data.interval}")
        print("Webhook configured")
        print("\nPolling for activity (Ctrl+C to stop)...\n")

        seen_ids = set()

        try:
            while True:
                activity = await sgai.monitor.activity(monitor_id)
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
                await asyncio.sleep(30)
        except asyncio.CancelledError:
            pass

        print("\nStopping monitor...")
        await sgai.monitor.delete(monitor_id)
        print("Monitor deleted")

asyncio.run(main())
