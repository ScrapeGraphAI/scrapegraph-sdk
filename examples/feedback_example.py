import os
from dotenv import load_dotenv
from scrapegraphaiapisdk.credits import status
from scrapegraphaiapisdk.feedback import feedback

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
    feedback_message = "This is a test feedback message."
    feedback_response = feedback(api_key, feedback_message)  # Call the feedback function
    print(f"Feedback Response: {feedback_response}")  # Print the response

if __name__ == "__main__":
    main() 