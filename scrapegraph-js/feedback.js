import axios from 'axios';

/**
 * Send feedback to the API.
 * 
 * @param {string} apiKey - Your ScrapeGraph AI API key
 * @param {string} requestId - The request ID associated with the feedback
 * @param {number} rating - The rating score
 * @param {string} feedbackText - The feedback message to send
 * @returns {Promise<string>} Response from the API in JSON format
 */
export async function feedback(apiKey, requestId, rating, feedbackText) {
  const endpoint = "https://sgai-api.onrender.com/api/v1/feedback";
  const headers = {
    "accept": "application/json",
    "SGAI-API-KEY": apiKey,
    "Content-Type": "application/json"
  };

  const feedbackData = {
    request_id: requestId,
    rating: rating,
    feedback_text: feedbackText
  };

  try {
    const response = await axios.post(endpoint, feedbackData, { headers });
    return JSON.stringify(response.data);
  } catch (error) {
    if (error.response) {
      return JSON.stringify({
        error: "HTTP error occurred",
        message: error.message,
        status_code: error.response.status
      });
    }
    return JSON.stringify({
      error: "An error occurred",
      message: error.message
    });
  }
} 