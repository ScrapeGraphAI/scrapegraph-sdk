import axios from 'axios';
import handleError from './utils/handleError.js';

/**
 * Send feedback to the API.
 * 
 * @param {string} apiKey - Your ScrapeGraph AI API key
 * @param {string} requestId - The request ID associated with the feedback
 * @param {number} rating - The rating score
 * @param {string} feedbackText - Optional feedback message to send
 * @returns {Promise<string>} Response from the API in JSON format
 */
export async function sendFeedback(apiKey, requestId, rating, feedbackText = null) {
  const endpoint = 'https://api.scrapegraphai.com/v1/feedback';
  const headers = {
    'accept': 'application/json',
    'SGAI-APIKEY': apiKey,
    'Content-Type': 'application/json'
  };

  const feedbackData = {
    request_id: requestId,
    rating: rating,
    feedback_text: feedbackText
  };

  try {
    const response = await axios.post(endpoint, feedbackData, { headers });
    return response.data;
  } catch (error) {
    handleError(error);
  }
} 