from scrapegraph_py import SyncClient
from scrapegraph_py.logger import get_logger

get_logger(level="DEBUG")

# Initialize the client
sgai_client = SyncClient(api_key="your-api-key-here")

# Check remaining credits
credits = sgai_client.get_credits()
print(f"Credits Info: {credits}")

sgai_client.close()
