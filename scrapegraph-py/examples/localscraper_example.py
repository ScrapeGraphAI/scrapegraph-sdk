from scrapegraph_py import Client
from scrapegraph_py.logger import sgai_logger

sgai_logger.set_logging(level="INFO")

# Initialize the client
sgai_client = Client(api_key="your-api-key-here")

# Example HTML content
html_content = """
<html>
    <body>
        <h1>Company Name</h1>
        <p>We are a technology company focused on AI solutions.</p>
        <div class="contact">
            <p>Email: contact@example.com</p>
            <p>Phone: (555) 123-4567</p>
        </div>
    </body>
</html>
"""

# LocalScraper request
response = sgai_client.localscraper(
    user_prompt="Extract the company description and contact information",
    website_html=html_content,
)

# Print the response
print(f"Request ID: {response['request_id']}")
print(f"Result: {response['result']}")
