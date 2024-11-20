import os
from dotenv import load_dotenv
from scrapegraph_py import ScrapeGraphClient, feedback, status

# Load environment variables from .env file
load_dotenv()

def main():
    # Get API key from environment variables
    api_key = os.getenv("SCRAPEGRAPH_API_KEY")
    client = ScrapeGraphClient(api_key)
    
    # Check API status
    try:
        result = status(client)
        print(f"API Status: {result}")
    except Exception as e:
        print(f"Error occurred: {e}")

    # Example usage of feedback function
    request_id = "3fa85f64-5717-4562-b3fc-2c963f66afa6"
    rating = 5
    feedback_message = "This is a test feedback message."
    feedback_response = feedback(client, request_id, rating, feedback_message)
    print(f"Feedback Response: {feedback_response}")

if __name__ == "__main__":
    main() 