"""
Extract data with custom LLM configuration.

Use LlmConfig to control the model, temperature, and other LLM parameters.
"""

import json

from scrapegraph_py import Client, LlmConfig

client = Client()  # uses SGAI_API_KEY env var

result = client.extract(
    url="https://example.com",
    prompt="Extract a detailed summary of the page content",
    llm_config=LlmConfig(
        temperature=0.3,
        max_tokens=1000,
    ),
)
print(json.dumps(result, indent=2))

client.close()
