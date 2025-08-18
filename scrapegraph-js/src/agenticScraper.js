import axios from 'axios';
import handleError from './utils/handleError.js';

/**
 * Perform automated browser actions on a webpage using AI-powered agentic scraping.
 *
 * @param {string} apiKey - Your ScrapeGraph AI API key
 * @param {string} url - The URL of the webpage to interact with
 * @param {string[]} steps - Array of steps to perform on the webpage (e.g., ["Type email@gmail.com in email input box", "click on login"])
 * @param {boolean} [useSession=true] - Whether to use session for the scraping operations
 * @returns {Promise<Object>} Response from the API containing request_id and initial status
 * @throws {Error} Will throw an error in case of an HTTP failure or invalid parameters.
 *
 * @example
 * // Example usage for automated login:
 * const apiKey = 'your-api-key';
 * const url = 'https://dashboard.scrapegraphai.com/';
 * const steps = [
 *   'Type email@gmail.com in email input box',
 *   'Type test-password@123 in password inputbox',
 *   'click on login'
 * ];
 *
 * try {
 *   const result = await agenticScraper(apiKey, url, steps, true);
 *   console.log('Request ID:', result.request_id);
 *   console.log('Status:', result.status);
 * } catch (error) {
 *   console.error('Error:', error.message);
 * }
 */
export async function agenticScraper(apiKey, url, steps, useSession = true) {
  const endpoint = 'https://api.scrapegraphai.com/v1/agentic-scrapper';
  const headers = {
    'accept': 'application/json',
    'SGAI-APIKEY': apiKey,
    'Content-Type': 'application/json',
  };

  // Validate inputs
  if (!apiKey || typeof apiKey !== 'string') {
    throw new Error('API key must be a non-empty string');
  }

  if (!url || typeof url !== 'string') {
    throw new Error('URL must be a non-empty string');
  }

  if (!url.startsWith('http://') && !url.startsWith('https://')) {
    throw new Error('URL must start with http:// or https://');
  }

  if (!Array.isArray(steps) || steps.length === 0) {
    throw new Error('Steps must be a non-empty array');
  }

  if (steps.some(step => !step || typeof step !== 'string' || !step.trim())) {
    throw new Error('All steps must be non-empty strings');
  }

  if (typeof useSession !== 'boolean') {
    throw new Error('useSession must be a boolean value');
  }

  const payload = {
    url: url,
    use_session: useSession,
    steps: steps,
  };

  try {
    const response = await axios.post(endpoint, payload, { headers });
    return response.data;
  } catch (error) {
    handleError(error);
  }
}

/**
 * Retrieve the status or result of an agentic scraper request.
 *
 * @param {string} apiKey - Your ScrapeGraph AI API key
 * @param {string} requestId - The request ID associated with the agentic scraper request
 * @returns {Promise<Object>} A promise that resolves to an object containing:
 *   - status: The current status of the request ('pending', 'completed', 'failed')
 *   - result: The extracted data or automation result when status is 'completed'
 *   - error: Error message if the request failed (when status is 'failed')
 *   - created_at: Timestamp of when the request was created
 *   - completed_at: Timestamp of when the request was completed (if applicable)
 * @throws {Error} Throws an error if the HTTP request fails or if the API key is invalid
 *
 * @example
 * // Example usage:
 * const apiKey = 'your-api-key';
 * const requestId = 'previously-obtained-request-id';
 *
 * try {
 *   const result = await getAgenticScraperRequest(apiKey, requestId);
 *   if (result.status === 'completed') {
 *     console.log('Automation completed:', result.result);
 *   } else if (result.status === 'pending') {
 *     console.log('Automation is still in progress');
 *   } else {
 *     console.log('Automation failed:', result.error);
 *   }
 * } catch (error) {
 *   console.error('Error fetching request:', error);
 * }
 *
 * @note The agentic scraper performs browser automation steps sequentially,
 * allowing for complex interactions like form filling, clicking buttons,
 * and navigating through multi-step workflows with session management.
 */
export async function getAgenticScraperRequest(apiKey, requestId) {
  const endpoint = 'https://api.scrapegraphai.com/v1/agentic-scrapper/' + requestId;
  const headers = {
    'accept': 'application/json',
    'SGAI-APIKEY': apiKey,
  };

  // Validate inputs
  if (!apiKey || typeof apiKey !== 'string') {
    throw new Error('API key must be a non-empty string');
  }

  if (!requestId || typeof requestId !== 'string') {
    throw new Error('Request ID must be a non-empty string');
  }

  try {
    const response = await axios.get(endpoint, { headers });
    return response.data;
  } catch (error) {
    handleError(error);
  }
}
