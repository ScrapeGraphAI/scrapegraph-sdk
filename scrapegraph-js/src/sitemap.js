import axios from 'axios';
import handleError from './utils/handleError.js';
import { isMockEnabled, getMockConfig } from './utils/mockConfig.js';
import { getMockResponse } from './utils/mockResponse.js';

/**
 * Extract all URLs from a website's sitemap.
 * Automatically discovers sitemap from robots.txt or common sitemap locations.
 *
 * @param {string} apiKey - Your ScrapeGraph AI API key.
 * @param {string} websiteUrl - The URL of the website to extract sitemap from.
 * @param {Object} options - Optional configuration options.
 * @param {boolean} options.mock - Override mock mode for this request.
 * @returns {Promise<Object>} A promise that resolves to an object containing:
 *   - urls: Array of URLs extracted from the sitemap
 * @throws {Error} Throws an error if the HTTP request fails.
 *
 * @example
 * // Basic usage:
 * const apiKey = 'your-api-key';
 * const websiteUrl = 'https://example.com';
 *
 * try {
 *   const result = await sitemap(apiKey, websiteUrl);
 *   console.log('Sitemap URLs:', result.urls);
 *   console.log('Total URLs found:', result.urls.length);
 * } catch (error) {
 *   console.error('Error:', error);
 * }
 *
 * @example
 * // Processing sitemap URLs:
 * const result = await sitemap(apiKey, 'https://example.com');
 * result.urls.forEach(url => {
 *   console.log('Found URL:', url);
 * });
 */
export async function sitemap(apiKey, websiteUrl, options = {}) {
  const { mock = null } = options;

  // Check if mock mode is enabled
  const useMock = mock !== null ? mock : isMockEnabled();

  if (useMock) {
    console.log('🧪 Mock mode active. Returning stub for sitemap request');
    const mockConfig = getMockConfig();
    const mockData = getMockResponse('POST', 'https://api.scrapegraphai.com/v1/sitemap', mockConfig.customResponses, mockConfig.customHandler);
    return mockData;
  }

  const endpoint = 'https://api.scrapegraphai.com/v1/sitemap';
  const headers = {
    'accept': 'application/json',
    'SGAI-APIKEY': apiKey,
    'Content-Type': 'application/json',
  };

  const payload = {
    website_url: websiteUrl,
  };

  try {
    const response = await axios.post(endpoint, payload, { headers });
    return response.data;
  } catch (error) {
    handleError(error);
  }
}
