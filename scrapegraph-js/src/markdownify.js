import axios from 'axios';
import handleError from './utils/handleError.js';

/**
 * Converts a webpage into clean, well-structured markdown format.
 *
 * @param {string} apiKey - Your ScrapeGraph AI API key.
 * @param {string} url - The URL of the webpage to be converted.
 * @returns {Promise<string>} A promise that resolves to the markdown representation of the webpage.
 * @throws {Error} Throws an error if the HTTP request fails.
 */
export async function markdownify(apiKey, url) {
  const endpoint = 'https://api.scrapegraphai.com/v1/markdownify';
  const headers = {
    'accept': 'application/json',
    'SGAI-APIKEY': apiKey,
  };

  const payload = {
    website_url: url,
  };

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
 * @returns {Promise<string>} A promise that resolves with details about the status or outcome of the specified request.
 * @throws {Error} Throws an error if the HTTP request fails.
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
