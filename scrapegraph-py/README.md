# ScrapeGraph API Python SDK

The official Python SDK for interacting with the ScrapeGraphAI API - a powerful web scraping and data extraction service.

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

### Basic Web Scraping

```python
import os
from scrapegraph_py import ScrapeGraphClient, smart_scraper
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("SCRAPEGRAPH_API_KEY")
client = ScrapeGraphClient(api_key)

url = "https://scrapegraphai.com/"
prompt = "What does the company do?"

result = smart_scraper(client, url, prompt)
print(result)
```

### Local HTML Scraping

You can also scrape content from local HTML files:

```python
from scrapegraph_py import ScrapeGraphClient, scrape_text
from bs4 import BeautifulSoup
import os

# Load environment variables
from dotenv import load_dotenv
load_dotenv()
api_key = os.getenv("SCRAPEGRAPH_API_KEY")

client = ScrapeGraphClient(api_key)

def scrape_local_html(client: ScrapeGraphClient, file_path: str, prompt: str):
    with open(file_path, 'r', encoding='utf-8') as file:
        html_content = file.read()
    
    # Use BeautifulSoup to extract text content
    soup = BeautifulSoup(html_content, 'html.parser')
    text_content = soup.get_text(separator='\n', strip=True)
    
    # Use ScrapeGraph AI to analyze the text
    return scrape_text(client, text_content, prompt)

# Usage
result = scrape_local_html(
    client,
    'sample.html',
    "Extract main content and important information"
)
print("Extracted Data:", result)
```

### Structured Data Extraction

For more structured data extraction, you can define a Pydantic schema:

```python
from pydantic import BaseModel, Field
from scrapegraph_py import scrape
import os

# Load environment variables
from dotenv import load_dotenv
load_dotenv()
api_key = os.getenv("SCRAPEGRAPH_API_KEY")

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
import os

# Load environment variables
from dotenv import load_dotenv
load_dotenv()
api_key = os.getenv("SCRAPEGRAPH_API_KEY")

response = credits(api_key)
print(response)
```

### Provide Feedback and Check Status

You can provide feedback on scraping results and check the API status:

```python
from scrapegraph_py import feedback, status
import os

# Load environment variables
from dotenv import load_dotenv
load_dotenv()
api_key = os.getenv("SCRAPEGRAPH_API_KEY")

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

## Expected Output Example

The following is an example of the expected output when scraping articles from a webpage:

```json
{
  "articles": [
    {
      "title": "Thousands of People Are Cloning Their Dead Pets. This Is the Woman They Call First",
      "url": "https://www.wired.com/story/your-next-job-pet-cloner/"
    },
    {
      "title": "The Quantum Geometry That Exists Outside of Space and Time",
      "url": "https://www.wired.com/story/physicists-reveal-a-quantum-geometry-that-exists-outside-of-space-and-time/"
    },
    {
      "title": "How a PhD Student Discovered a Lost Mayan City From Hundreds of Miles Away",
      "url": "https://www.wired.com/story/lost-maya-city-valeriana-interview/"
    },
    {
      "title": "The Maker of Ozempic Is Trying to Block Compounded Versions of Its Blockbuster Drug",
      "url": "https://www.wired.com/story/novo-nordisk-ozempic-compounded-fda-block-pharmacies/"
    }
  ]
}
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


