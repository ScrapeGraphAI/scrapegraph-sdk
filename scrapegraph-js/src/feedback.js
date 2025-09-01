import axios from 'axios';
import handleError from './utils/handleError.js';
import { isMockEnabled, getMockConfig } from './utils/mockConfig.js';
import { getMockResponse } from './utils/mockResponse.js';

/**
 * Send feedback to the API.
 *
 * @param {string} apiKey - Your ScrapeGraph AI API key
 * @param {string} requestId - The request ID associated with the feedback
 * @param {number} rating - The rating score
 * @param {string} feedbackText - Optional feedback message to send
 * @param {Object} options - Optional configuration options
 * @param {boolean} options.mock - Override mock mode for this request
 * @returns {Promise<string>} Response from the API in JSON format
 */
export async function sendFeedback(apiKey, requestId, rating, feedbackText = null, options = {}) {
  const { mock = null } = options;

  // Check if mock mode is enabled
  const useMock = mock !== null ? mock : isMockEnabled();
  
  if (useMock) {
    console.log('🧪 Mock mode active. Returning stub for sendFeedback request');
    const mockConfig = getMockConfig();
    const mockData = getMockResponse('POST', 'https://api.scrapegraphai.com/v1/feedback', mockConfig.customResponses, mockConfig.customHandler);
    return mockData;
  }

  const endpoint = 'https://api.scrapegraphai.com/v1/feedback';
  const headers = {
    'accept': 'application/json',
    'SGAI-APIKEY': apiKey,
    'Content-Type': 'application/json',
  };

  const feedbackData = {
    request_id: requestId,
    rating: rating,
    feedback_text: feedbackText,
  };

  try {
    const response = await axios.post(endpoint, feedbackData, { headers });
    return response.data;
  } catch (error) {
    handleError(error);
  }
}
