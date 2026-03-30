"""Check remaining API credits."""

from scrapegraph_py import Client

client = Client()  # uses SGAI_API_KEY env var

credits = client.credits()
print(f"Remaining credits: {credits['remaining_credits']}")
print(f"Total used: {credits['total_credits_used']}")

client.close()
