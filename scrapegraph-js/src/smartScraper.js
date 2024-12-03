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
 * @returns {Promise<string>} Extracted data in JSON format matching the provided schema
 * @throws - Will throw an error in case of an HTTP failure.
 */
export async function smartScraper(apiKey, url, prompt, schema = null) {
  const endpoint = 'https://api.scrapegraphai.com/v1/smartscraper';
  const headers = {
    'accept': 'application/json',
    'SGAI-APIKEY': apiKey,
    'Content-Type': 'application/json'
  };

  const payload = {
    website_url: url,
    user_prompt: prompt
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
    handleError(error)
  }
}

/**
 * Retrieve the status or the result of a smartScraper request. It also allows you to see the result of old requests.
 * 
 * @param {string} apiKey - Your ScrapeGraph AI API key
 * @param {string} requestId - The request ID associated with the output of a smartScraper request.
 * @returns {Promise<string>} Information related to the status or result of a scraping request.
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
    handleError(error)
  }
}