import axios from 'axios';
import handleError from './utils/handleError.js';
import { ZodType } from 'zod';
import { zodToJsonSchema } from 'zod-to-json-schema';

/**
 * Scrape and extract structured data from a webpage using ScrapeGraph AI.
 *
 * @param {string} apiKey - Your ScrapeGraph AI API key
 * @param {string} url - The URL of the webpage to scrape
 * @param {string} prompt - Natural language prompt describing what data to extract
 * @param {Object} [schema] - Optional schema object defining the output structure
 * @param {number} [numberOfScrolls] - Optional number of times to scroll the page (0-100). If not provided, no scrolling will be performed.
 * @returns {Promise<string>} Extracted data in JSON format matching the provided schema
 * @throws - Will throw an error in case of an HTTP failure.
 */
export async function smartScraper(apiKey, url, prompt, schema = null, numberOfScrolls = null) {
  const endpoint = 'https://api.scrapegraphai.com/v1/smartscraper';
  const headers = {
    'accept': 'application/json',
    'SGAI-APIKEY': apiKey,
    'Content-Type': 'application/json',
  };

  const payload = {
    website_url: url,
    user_prompt: prompt,
  };

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
export async function getSmartScraperRequest(apiKey, requestId) {
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
