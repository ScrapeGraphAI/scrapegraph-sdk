import axios from 'axios';
import handleError from './utils/handleError.js';

/**
 * Converts a webpage into HTML format with optional JavaScript rendering.
 *
 * @param {string} apiKey - Your ScrapeGraph AI API key.
 * @param {string} url - The URL of the webpage to be converted.
 * @param {Object} options - Optional configuration options.
 * @param {boolean} options.renderHeavyJs - Whether to render heavy JavaScript (defaults to false).
 * @param {Object} options.headers - Optional custom headers to send with the request.
 * @returns {Promise<Object>} A promise that resolves to the HTML content and metadata.
 * @throws {Error} Throws an error if the HTTP request fails.
 *
 * @example
 * // Basic usage:
 * const apiKey = 'your-api-key';
 * const url = 'https://example.com';
 *
 * try {
 *   const result = await htmlfy(apiKey, url);
 *   console.log('HTML content:', result.html);
 *   console.log('Status:', result.status);
 * } catch (error) {
 *   console.error('Error:', error);
 * }
 *
 * @example
 * // With JavaScript rendering:
 * const result = await htmlfy(apiKey, url, {
 *   renderHeavyJs: true
 * });
 *
 * @example
 * // With custom headers:
 * const result = await htmlfy(apiKey, url, {
 *   renderHeavyJs: false,
 *   headers: {
 *     'User-Agent': 'Custom Agent',
 *     'Cookie': 'session=123'
 *   }
 * });
 */
export async function htmlfy(apiKey, url, options = {}) {
  const {
    renderHeavyJs = false,
    headers: customHeaders = {}
  } = options;

  const endpoint = 'https://api.scrapegraphai.com/v1/htmlfy';
  const headers = {
    'accept': 'application/json',
    'SGAI-APIKEY': apiKey,
    'Content-Type': 'application/json',
    ...customHeaders
  };

  const payload = {
    website_url: url,
    render_heavy_js: renderHeavyJs,
  };

  // Only include headers in payload if they are provided
  if (Object.keys(customHeaders).length > 0) {
    payload.headers = customHeaders;
  }

  try {
    const response = await axios.post(endpoint, payload, { headers });
    return response.data;
  } catch (error) {
    handleError(error);
  }
}

/**
 * Retrieves the status or result of an HTMLfy request.
 *
 * @param {string} apiKey - Your ScrapeGraph AI API key.
 * @param {string} requestId - The unique identifier for the HTMLfy request.
 * @returns {Promise<Object>} A promise that resolves to an object containing:
 *   - status: The current status of the request ('pending', 'completed', 'failed')
 *   - html: The HTML content when status is 'completed'
 *   - htmlfy_request_id: The request identifier
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
 *   const result = await getHtmlfyRequest(apiKey, requestId);
 *   if (result.status === 'completed') {
 *     console.log('HTML content:', result.html);
 *     console.log('Request ID:', result.htmlfy_request_id);
 *   } else if (result.status === 'pending') {
 *     console.log('HTML conversion is still in progress');
 *   } else {
 *     console.log('HTML conversion failed:', result.error);
 *   }
 * } catch (error) {
 *   console.error('Error fetching HTML:', error);
 * }
 *
 * @note The HTML content includes:
 *   - Full HTML structure with DOCTYPE
 *   - Head section with meta tags, title, and styles
 *   - Body content with all elements
 *   - JavaScript code (if renderHeavyJs was enabled)
 *   - CSS styles and formatting
 *   - Images, links, and other media elements
 */
export async function getHtmlfyRequest(apiKey, requestId) {
  const endpoint = 'https://api.scrapegraphai.com/v1/htmlfy/' + requestId;
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
