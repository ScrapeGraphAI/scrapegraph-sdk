# ScrapeGraph Python SDK

The official Python SDK for interacting with the ScrapeGraph AI API - a powerful web scraping and data extraction service.

## Installation

Install the package using pip:
```bash
pip install scrapegraph-py
```

## Authentication

To use the ScrapeGraph API, you'll need an API key. You can manage this in two ways:

1. Environment variable:
```bash
export SCRAPEGRAPH_API_KEY="your-api-key-here"
```

2. `.env` file:
```plaintext
SCRAPEGRAPH_API_KEY="your-api-key-here"
```

## Features

The SDK provides four main functionalities:

1. Web Scraping (basic and structured)
2. Credits checking
3. Feedback submission
4. API status checking

## Usage


### Structured Data Extraction

For more structured data extraction, you can define a Pydantic schema:

```python
from pydantic import BaseModel, Field
from scrapegraph_py import scrape

class CompanyInfoSchema(BaseModel):
    company_name: str = Field(description="The name of the company")
    description: str = Field(description="A description of the company")
    main_products: list[str] = Field(description="The main products of the company")

# Scrape with schema
result = scrape(
    api_key=api_key,
    url="https://scrapegraphai.com/",
    prompt="What does the company do?",
    schema=CompanyInfoSchema
)
print(result)
```

### Check Credits

Monitor your API usage:

```python
from scrapegraph_py import credits

response = credits(api_key)
print(response)
```

### Provide Feedback and Check Status

You can provide feedback on scraping results and check the API status:

```python
from scrapegraph_py import feedback, status

# Check API status
status_response = status(api_key)
print(f"API Status: {status_response}")

# Submit feedback
feedback_response = feedback(
    api_key=api_key,
    request_id="your-request-id",  # UUID from your scraping request
    rating=5,  # Rating from 1-5
    message="Great results!"
)
print(f"Feedback Response: {feedback_response}")
```

## Development

### Requirements

- Python 3.9+
- [Rye](https://rye-up.com/) for dependency management (optional)

### Project Structure

```
scrapegraph_py/
├── __init__.py
├── credits.py      # Credits checking functionality
├── scrape.py      # Core scraping functionality
└── feedback.py    # Feedback submission functionality

examples/
├── credits_example.py
├── feedback_example.py
├── scrape_example.py
└── scrape_schema_example.py

tests/
├── test_credits.py
├── test_feedback.py
└── test_scrape.py
```

### Setting up the Development Environment

1. Clone the repository:
```bash
git clone https://github.com/yourusername/scrapegraph-py.git
cd scrapegraph-py
```

2. Install dependencies:
```bash
# If using Rye
rye sync

# If using pip
pip install -r requirements-dev.lock
```

3. Create a `.env` file in the root directory:
```plaintext
SCRAPEGRAPH_API_KEY="your-api-key-here"
```

## License

This project is licensed under the MIT License.

## Support

For support:
- Visit [ScrapeGraph AI](https://scrapegraphai.com/)
- Contact our support team
- Check the examples in the `examples/` directory

