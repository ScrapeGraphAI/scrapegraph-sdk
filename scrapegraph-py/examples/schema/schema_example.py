"""Generate a JSON schema from a natural language prompt."""

from scrapegraph_py import Client

client = Client()  # uses SGAI_API_KEY env var

result = client.schema("Product with name, price, description, and rating")
print(result)

client.close()
