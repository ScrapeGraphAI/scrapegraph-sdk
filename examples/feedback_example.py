import os
from dotenv import load_dotenv
from scrapegraph_py.credits import status
from scrapegraph_py.feedback import feedback

# Load environment variables from .env file
load_dotenv()

def main():
    # Get API key from environment variables
    api_key = os.getenv("SCRAPEGRAPH_API_KEY")
    
    # Check API status
    try:
        result = status(api_key)
        print(f"API Status: {result}")
    except Exception as e:
        print(f"Error occurred: {e}")

    # Example usage of feedback function
    request_id = "3fa85f64-5717-4562-b3fc-2c963f66afa6"
    rating = 5
    feedback_message = "This is a test feedback message."
    feedback_response = feedback(api_key, request_id, rating, feedback_message)  # Call the feedback function
    print(f"Feedback Response: {feedback_response}")  # Print the response

if __name__ == "__main__":
    main() 