import axios from 'axios';
import handleError from './utils/handleError.js';

/**
 * Converts a webpage into clean, well-structured markdown format.
 *
 * @param {string} apiKey - Your ScrapeGraph AI API key.
 * @param {string} url - The URL of the webpage to be converted.
 * @param {string[]} [steps] - Optional array of interactive steps to perform on the website before conversion (e.g., ['click on accept cookies', 'wait for 1 second', 'click on main content'])
 * @returns {Promise<string>} A promise that resolves to the markdown representation of the webpage.
 * @throws {Error} Throws an error if the HTTP request fails.
 */
export async function markdownify(apiKey, url, steps = null) {
  const endpoint = 'https://api.scrapegraphai.com/v1/markdownify';
  const headers = {
    'accept': 'application/json',
    'SGAI-APIKEY': apiKey,
  };

  const payload = {
    website_url: url,
  };

  if (steps !== null) {
    if (!Array.isArray(steps)) {
      throw new Error('steps must be an array of strings');
    }
    if (steps.some(step => typeof step !== 'string')) {
      throw new Error('All steps must be strings');
    }
    payload.steps = steps;
  }

  try {
    const response = await axios.post(endpoint, payload, { headers });
    return response.data;
  } catch (error) {
    handleError(error);
  }
}

/**
 * Retrieves the status or result of a markdownify request, with the option to review results from previous requests.
 *
 * @param {string} apiKey - Your ScrapeGraph AI API key.
 * @param {string} requestId - The unique identifier for the markdownify request whose result you want to retrieve.
 * @returns {Promise<Object>} A promise that resolves to an object containing:
 *   - status: The current status of the request ('pending', 'completed', 'failed')
 *   - result: The markdown content when status is 'completed'
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
 *   const result = await getMarkdownifyRequest(apiKey, requestId);
 *   if (result.status === 'completed') {
 *     console.log('Markdown content:', result.result);
 *   } else if (result.status === 'pending') {
 *     console.log('Conversion is still in progress');
 *   } else {
 *     console.log('Conversion failed:', result.error);
 *   }
 * } catch (error) {
 *   console.error('Error fetching markdown:', error);
 * }
 * 
 * @note The markdown content includes:
 *   - Properly formatted headers
 *   - Lists and tables
 *   - Code blocks with language detection
 *   - Links and images
 *   - Text formatting (bold, italic, etc.)
 */
export async function getMarkdownifyRequest(apiKey, requestId) {
  const endpoint = 'https://api.scrapegraphai.com/v1/markdownify/' + requestId;
  const headers = {
    'accept': 'application/json',
    'SGAI-APIKEY': apiKey,
  };

  try {
    const response = await axios.get(endpoint, { headers });
    return response.data;
  } catch (error) {
    handleError(error);
  }
}
