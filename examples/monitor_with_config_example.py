"""
Create a monitor with custom fetch and LLM configuration.
"""

import json

from scrapegraph_py import Client, FetchConfig, LlmConfig

client = Client()  # uses SGAI_API_KEY env var

monitor = client.monitor.create(
    name="Stealth News Monitor",
    url="https://example.com/news",
    prompt="Extract the top 5 news headlines with their dates",
    cron="0 */6 * * *",  # Every 6 hours
    fetch_config=FetchConfig(
        mode="js+stealth",
        wait=2000,
    ),
    llm_config=LlmConfig(
        temperature=0.1,
    ),
)
print("Monitor created:", json.dumps(monitor, indent=2))

client.close()
