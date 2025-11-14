import axios from 'axios';
import handleError from './utils/handleError.js';
import { ZodType } from 'zod';
import { zodToJsonSchema } from 'zod-to-json-schema';
import { isMockEnabled, getMockConfig } from './utils/mockConfig.js';
import { getMockResponse } from './utils/mockResponse.js';

/**
 * Search and extract information from multiple web sources using AI.
 *
 * @param {string} apiKey - Your ScrapeGraph AI API key
 * @param {string} prompt - Natural language prompt describing what data to extract
 * @param {number} [numResults=3] - Number of websites to scrape (3-20). Default is 3.
 *                                 More websites provide better research depth but cost more credits.
 *                                 Credit calculation: 30 base + 10 per additional website beyond 3.
 * @param {Object} [schema] - Optional schema object defining the output structure
 * @param {String} userAgent - the user agent like "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
 * @param {Object} options - Optional configuration options
 * @param {boolean} options.mock - Override mock mode for this request
 * @param {boolean} options.renderHeavyJs - Whether to render heavy JavaScript on the page
 * @param {boolean} [options.extractionMode=true] - Whether to use AI extraction (true) or markdown conversion (false).
 *                                                 AI extraction costs 10 credits per page, markdown conversion costs 2 credits per page.
 * @param {boolean} [options.stealth=false] - Enable stealth mode to avoid bot detection
 * @returns {Promise<string>} Extracted data in JSON format matching the provided schema
 * @throws - Will throw an error in case of an HTTP failure.
 */
export async function searchScraper(apiKey, prompt, numResults = 3, schema = null, userAgent = null, options = {}) {
  const { mock = null, renderHeavyJs = false, extractionMode = true, stealth = false } = options;

  // Check if mock mode is enabled
  const useMock = mock !== null ? mock : isMockEnabled();
  
  if (useMock) {
    console.log('🧪 Mock mode active. Returning stub for searchScraper request');
    const mockConfig = getMockConfig();
    const mockData = getMockResponse('POST', 'https://api.scrapegraphai.com/v1/searchscraper', mockConfig.customResponses, mockConfig.customHandler);
    return mockData;
  }
  const endpoint = 'https://api.scrapegraphai.com/v1/searchscraper';
  const headers = {
    'accept': 'application/json',
    'SGAI-APIKEY': apiKey,
    'Content-Type': 'application/json',
  };

  if (userAgent) headers['User-Agent'] = userAgent;

  // Validate numResults
  if (numResults < 3 || numResults > 20) {
    throw new Error('numResults must be between 3 and 20');
  }

  const payload = {
    user_prompt: prompt,
    num_results: numResults,
    render_heavy_js: renderHeavyJs,
    extraction_mode: extractionMode,
  };

  if (stealth) {
    payload.stealth = stealth;
  }

  if (schema) {
    if (schema instanceof ZodType) {
      payload.output_schema = zodToJsonSchema(schema);
    } else {
      throw new Error('The schema must be an instance of a valid Zod schema');
    }
  }

  try {
    const response = await axios.post(endpoint, payload, { headers });
    return response.data;
  } catch (error) {
    handleError(error);
  }
}

/**
 * Retrieve the status or result of a searchScraper request. This function allows you to check the progress
 * or retrieve results of both ongoing and completed search and extraction operations.
 *
 * @param {string} apiKey - Your ScrapeGraph AI API key
 * @param {string} requestId - The request ID associated with the output of a searchScraper request.
 * @returns {Promise<Object>} A promise that resolves to an object containing:
 *   - status: The current status of the request ('pending', 'completed', 'failed')
 *   - result: The extracted data in JSON format when status is 'completed', including:
 *     - extracted_data: The structured data extracted from search results
 *     - source_urls: Array of URLs that were used as sources
 *     - search_metadata: Information about the search operation
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
 *   const result = await getSearchScraperRequest(apiKey, requestId);
 *   if (result.status === 'completed') {
 *     console.log('Extracted data:', result.result.extracted_data);
 *     console.log('Sources:', result.result.source_urls);
 *   } else if (result.status === 'pending') {
 *     console.log('Search and extraction still in progress');
 *   } else {
 *     console.log('Operation failed:', result.error);
 *   }
 * } catch (error) {
 *   console.error('Error fetching search results:', error);
 * }
 *
 * @note The search operation typically processes multiple web pages to gather comprehensive
 * information based on the original search query. The results are structured according to
 * the schema provided in the original searchScraper call, if any.
 */
export async function getSearchScraperRequest(apiKey, requestId, options = {}) {
  const { mock = null } = options;

  // Check if mock mode is enabled
  const useMock = mock !== null ? mock : isMockEnabled();
  
  if (useMock) {
    console.log('🧪 Mock mode active. Returning stub for getSearchScraperRequest');
    const mockConfig = getMockConfig();
    const mockData = getMockResponse('GET', `https://api.scrapegraphai.com/v1/searchscraper/${requestId}`, mockConfig.customResponses, mockConfig.customHandler);
    return mockData;
  }

  const endpoint = 'https://api.scrapegraphai.com/v1/searchscraper/' + requestId;
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
