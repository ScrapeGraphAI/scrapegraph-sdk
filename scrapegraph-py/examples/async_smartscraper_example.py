import asyncio
from scrapegraph_py import AsyncClient
from scrapegraph_py.exceptions import APIError

async def main():
    sgai_client = AsyncClient(api_key="sgai-your-api-key-here")
    
    try:
        # Concurrent scraping requests
        urls = [
            "https://scrapegraphai.com/",
            "https://github.com/ScrapeGraphAI/Scrapegraph-ai"
        ]
        
        tasks = [
            sgai_client.smartscraper(
                website_url=url,
                user_prompt="Summarize the main content"
            ) for url in urls
        ]
        
        # Execute requests concurrently
        responses = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Process results
        for i, response in enumerate(responses):
            if isinstance(response, Exception):
                print(f"\nError for {urls[i]}: {response}")
            else:
                print(f"\nPage {i+1} Summary:")
                print(f"URL: {urls[i]}")
                print(f"Result: {response['result']}")
            
        # Check credits
        credits = await sgai_client.get_credits()
        print(f"Credits Info: {credits}")
        
    except APIError as e:
        print(f"Error: {e}")
    finally:
        await sgai_client.close()

if __name__ == "__main__":
    asyncio.run(main()) 