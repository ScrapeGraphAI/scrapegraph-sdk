import axios from 'axios';
import handleError from './utils/handleError.js';
import { ZodType } from 'zod';
import { zodToJsonSchema } from 'zod-to-json-schema';
import { isMockEnabled, getMockConfig } from './utils/mockConfig.js';
import { getMockResponse, createMockAxiosResponse } from './utils/mockResponse.js';

/**
 * Scrape and extract structured data from a webpage using ScrapeGraph AI.
 *
 * Supports three types of input (must provide exactly one):
 * - url: Scrape from a URL
 * - websiteHtml: Process local HTML content
 * - websiteMarkdown: Process local Markdown content
 *
 * @param {string} apiKey - Your ScrapeGraph AI API key
 * @param {string} url - The URL of the webpage to scrape (can be null if using websiteHtml or websiteMarkdown)
 * @param {string} prompt - Natural language prompt describing what data to extract
 * @param {Object} [schema] - Optional schema object defining the output structure
 * @param {number} [numberOfScrolls] - Optional number of times to scroll the page (0-100). If not provided, no scrolling will be performed.
 * @param {number} [totalPages] - Optional number of pages to scrape (1-10). If not provided, only the first page will be scraped.
 * @param {Object} [cookies] - Optional cookies object for authentication and session management
 * @param {Object} [options] - Optional configuration object
 * @param {boolean} [plain_text] - Optional flag to return plain text instead of structured data
 * @param {boolean} [renderHeavyJs] - Optional flag to enable heavy JavaScript rendering on the page
 * @param {boolean} [stealth] - Optional flag to enable stealth mode to avoid bot detection
 * @param {string} [websiteHtml] - Optional raw HTML content to process (max 2MB, mutually exclusive with url and websiteMarkdown)
 * @param {string} [websiteMarkdown] - Optional Markdown content to process (max 2MB, mutually exclusive with url and websiteHtml)
 * @returns {Promise<string>} Extracted data in JSON format matching the provided schema
 * @throws - Will throw an error in case of an HTTP failure or validation error.
 */
export async function smartScraper(apiKey, url, prompt, schema = null, numberOfScrolls = null, totalPages = null, cookies = null, options = {}, plain_text = false, renderHeavyJs = false, stealth = false, websiteHtml = null, websiteMarkdown = null) {
  const { mock = null } = options;

  // Validate that exactly one of url, websiteHtml, or websiteMarkdown is provided
  const inputsProvided = [url, websiteHtml, websiteMarkdown].filter(input => input !== null && input !== undefined).length;

  if (inputsProvided === 0) {
    throw new Error('Exactly one of url, websiteHtml, or websiteMarkdown must be provided');
  }

  if (inputsProvided > 1) {
    throw new Error('Only one of url, websiteHtml, or websiteMarkdown can be provided');
  }

  // Validate content size for HTML and Markdown (max 2MB)
  const MAX_SIZE = 2 * 1024 * 1024; // 2MB in bytes

  if (websiteHtml && Buffer.byteLength(websiteHtml, 'utf8') > MAX_SIZE) {
    throw new Error('websiteHtml content exceeds maximum size of 2MB');
  }

  if (websiteMarkdown && Buffer.byteLength(websiteMarkdown, 'utf8') > MAX_SIZE) {
    throw new Error('websiteMarkdown content exceeds maximum size of 2MB');
  }

  // Check if mock mode is enabled
  const useMock = mock !== null ? mock : isMockEnabled();

  if (useMock) {
    console.log('🧪 Mock mode active. Returning stub for smartScraper request');
    const mockConfig = getMockConfig();
    const mockData = getMockResponse('POST', 'https://api.scrapegraphai.com/v1/smartscraper', mockConfig.customResponses, mockConfig.customHandler);
    return mockData;
  }

  const endpoint = 'https://api.scrapegraphai.com/v1/smartscraper';
  const headers = {
    'accept': 'application/json',
    'SGAI-APIKEY': apiKey,
    'Content-Type': 'application/json',
  };

  const payload = {
    user_prompt: prompt,
    plain_text: plain_text,
  };

  // Add the appropriate input source to the payload
  if (url) {
    payload.website_url = url;
  } else if (websiteHtml) {
    payload.website_html = websiteHtml;
  } else if (websiteMarkdown) {
    payload.website_markdown = websiteMarkdown;
  }

  if (renderHeavyJs) {
    payload.render_heavy_js = renderHeavyJs;
  }

  if (cookies) {
    if (typeof cookies === 'object' && cookies !== null) {
      payload.cookies = cookies;
    } else {
      throw new Error('Cookies must be an object with key-value pairs');
    }
  }

  if (schema) {
    if (schema instanceof ZodType) {
      payload.output_schema = zodToJsonSchema(schema);
    } else {
      throw new Error('The schema must be an instance of a valid Zod schema');
    }
  }

  if (numberOfScrolls !== null) {
    if (!Number.isInteger(numberOfScrolls) || numberOfScrolls < 0 || numberOfScrolls > 100) {
      throw new Error('numberOfScrolls must be an integer between 0 and 100');
    }
    payload.number_of_scrolls = numberOfScrolls;
  }

  if (totalPages !== null) {
    if (!Number.isInteger(totalPages) || totalPages < 1 || totalPages > 10) {
      throw new Error('totalPages must be an integer between 1 and 10');
    }
    payload.total_pages = totalPages;
  }

  if (stealth) {
    payload.stealth = stealth;
  }

  try {
    const response = await axios.post(endpoint, payload, { headers });
    return response.data;
  } catch (error) {
    handleError(error);
  }
}

/**
 * Retrieve the status or the result of a smartScraper request. It also allows you to see the result of old requests.
 *
 * @param {string} apiKey - Your ScrapeGraph AI API key
 * @param {string} requestId - The request ID associated with the output of a smartScraper request.
 * @returns {Promise<Object>} A promise that resolves to an object containing:
 *   - status: The current status of the request ('pending', 'completed', 'failed')
 *   - result: The extracted data in JSON format (when status is 'completed')
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
 *   const result = await getSmartScraperRequest(apiKey, requestId);
 *   if (result.status === 'completed') {
 *     console.log('Extracted data:', result.result);
 *   } else if (result.status === 'pending') {
 *     console.log('Request is still processing');
 *   } else {
 *     console.log('Request failed:', result.error);
 *   }
 * } catch (error) {
 *   console.error('Error fetching request:', error);
 * }
 */
export async function getSmartScraperRequest(apiKey, requestId, options = {}) {
  const { mock = null } = options;

  // Check if mock mode is enabled
  const useMock = mock !== null ? mock : isMockEnabled();
  
  if (useMock) {
    console.log('🧪 Mock mode active. Returning stub for getSmartScraperRequest');
    const mockConfig = getMockConfig();
    const mockData = getMockResponse('GET', `https://api.scrapegraphai.com/v1/smartscraper/${requestId}`, mockConfig.customResponses, mockConfig.customHandler);
    return mockData;
  }

  const endpoint = 'https://api.scrapegraphai.com/v1/smartscraper/' + requestId;
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
