import axios from 'axios';
import handleError from './utils/handleError.js';
import { ZodType } from 'zod';
import { zodToJsonSchema } from 'zod-to-json-schema';

/**
 * Search and extract information from multiple web sources using AI.
 *
 * @param {string} apiKey - Your ScrapeGraph AI API key
 * @param {string} prompt - Natural language prompt describing what data to extract
 * @param {Object} [schema] - Optional schema object defining the output structure
 * @param {String} userAgent - the user agent like "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
 * @returns {Promise<string>} Extracted data in JSON format matching the provided schema
 * @throws - Will throw an error in case of an HTTP failure.
 */
export async function searchScraper(apiKey, prompt, schema = null, userAgent = null) {
  const endpoint = 'https://api.scrapegraphai.com/v1/searchscraper';
  const headers = {
    'accept': 'application/json',
    'SGAI-APIKEY': apiKey,
    'Content-Type': 'application/json',
  };

  if (userAgent) headers['User-Agent'] = userAgent;

  const payload = {
    user_prompt: prompt,
  };

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
 * Retrieve the status or the result of searchScraper request. It also allows you to see the result of old requests.
 *
 * @param {string} apiKey - Your ScrapeGraph AI API key
 * @param {string} requestId - The request ID associated with the output of a searchScraper request.
 * @returns {Promise<string>} Information related to the status or result of a scraping request.
 */
export async function getSearchScraperRequest(apiKey, requestId) {
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
