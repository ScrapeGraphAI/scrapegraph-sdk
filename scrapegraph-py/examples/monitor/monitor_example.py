"""Create and manage monitors for recurring extraction."""

from scrapegraph_py import Client

client = Client()  # uses SGAI_API_KEY env var

# Create a monitor
monitor = client.monitor.create(
    name="Price Tracker",
    url="https://example.com/products",
    prompt="Extract all product prices",
    cron="0 9 * * 1",  # Every Monday at 9am
)
print("Monitor created:", monitor)

# List all monitors
monitors = client.monitor.list()
print("All monitors:", monitors)

# Pause/resume/delete
# client.monitor.pause(monitor["id"])
# client.monitor.resume(monitor["id"])
# client.monitor.delete(monitor["id"])

client.close()
