import axios from 'axios';
import handleError from './utils/handleError.js';
import { isMockEnabled, getMockConfig } from './utils/mockConfig.js';
import { getMockResponse, createMockAxiosResponse } from './utils/mockResponse.js';

/**
 * Converts a webpage into HTML format with optional JavaScript rendering.
 *
 * @param {string} apiKey - Your ScrapeGraph AI API key.
 * @param {string} url - The URL of the webpage to be converted.
 * @param {Object} options - Optional configuration options.
 * @param {boolean} options.renderHeavyJs - Whether to render heavy JavaScript (defaults to false).
 * @param {boolean} [options.branding=false] - Whether to include branding in the response (defaults to false).
 * @param {Object} options.headers - Optional custom headers to send with the request.
 * @param {boolean} [options.stealth=false] - Enable stealth mode to avoid bot detection
 * @returns {Promise<Object>} A promise that resolves to the HTML content and metadata.
 * @throws {Error} Throws an error if the HTTP request fails.
 *
 * @example
 * // Basic usage:
 * const apiKey = 'your-api-key';
 * const url = 'https://example.com';
 *
 * try {
 *   const result = await scrape(apiKey, url);
 *   console.log('HTML content:', result.html);
 *   console.log('Status:', result.status);
 * } catch (error) {
 *   console.error('Error:', error);
 * }
 *
 * @example
 * // With JavaScript rendering:
 * const result = await scrape(apiKey, url, {
 *   renderHeavyJs: true
 * });
 *
 * @example
 * // With branding enabled:
 * const result = await scrape(apiKey, url, {
 *   branding: true
 * });
 *
 * @example
 * // With custom headers:
 * const result = await scrape(apiKey, url, {
 *   renderHeavyJs: false,
 *   headers: {
 *     'User-Agent': 'Custom Agent',
 *     'Cookie': 'session=123'
 *   }
 * });
 */
export async function scrape(apiKey, url, options = {}) {
  const {
    renderHeavyJs = false,
    branding = false,
    headers: customHeaders = {},
    mock = null,
    stealth = false
  } = options;

  // Check if mock mode is enabled
  const useMock = mock !== null ? mock : isMockEnabled();
  
  if (useMock) {
    console.log('🧪 Mock mode active. Returning stub for scrape request');
    const mockConfig = getMockConfig();
    const mockData = getMockResponse('POST', 'https://api.scrapegraphai.com/v1/scrape', mockConfig.customResponses, mockConfig.customHandler);
    return mockData;
  }

  const endpoint = 'https://api.scrapegraphai.com/v1/scrape';
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

  if (branding) {
    payload.branding = branding;
  }

  if (stealth) {
    payload.stealth = stealth;
  }

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
 * Retrieves the status or result of a scrape request.
 *
 * @param {string} apiKey - Your ScrapeGraph AI API key.
 * @param {string} requestId - The unique identifier for the scrape request.
 * @returns {Promise<Object>} A promise that resolves to an object containing:
 *   - status: The current status of the request ('pending', 'completed', 'failed')
 *   - html: The HTML content when status is 'completed'
 *   - scrape_request_id: The request identifier
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
 *   const result = await getScrapeRequest(apiKey, requestId);
 *   if (result.status === 'completed') {
 *     console.log('HTML content:', result.html);
 *     console.log('Request ID:', result.scrape_request_id);
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
export async function getScrapeRequest(apiKey, requestId, options = {}) {
  const { mock = null } = options;

  // Check if mock mode is enabled
  const useMock = mock !== null ? mock : isMockEnabled();
  
  if (useMock) {
    console.log('🧪 Mock mode active. Returning stub for getScrapeRequest');
    const mockConfig = getMockConfig();
    const mockData = getMockResponse('GET', `https://api.scrapegraphai.com/v1/scrape/${requestId}`, mockConfig.customResponses, mockConfig.customHandler);
    return mockData;
  }

  const endpoint = 'https://api.scrapegraphai.com/v1/scrape/' + requestId;
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
