import axios from 'axios';
import handleError from './utils/handleError.js';
import { ZodType } from 'zod';
import { zodToJsonSchema } from 'zod-to-json-schema';

/**
 * Extract structured data from local HTML content using ScrapeGraph AI.
 *
 * @param {string} apiKey - The API key for ScrapeGraph AI.
 * @param {string} websiteHtml - HTML content as a string from the local web page to scrape.
 * @param {string} prompt - A natural language description of the data to extract.
 * @param {Object} [schema] - (Optional) Schema object defining the structure of the desired output.
 * @returns {Promise<string>} A JSON string containing the extracted data, formatted to match the schema.
 * @throws {Error} If an HTTP error or validation issue occurs.
 */
export async function localScraper(apiKey, websiteHtml, prompt, schema = null) {
  const endpoint = 'https://api.scrapegraphai.com/v1/localscraper';
  const headers = {
    'accept': 'application/json',
    'SGAI-APIKEY': apiKey,
    'Content-Type': 'application/json',
  };

  const payload = {
    website_html: websiteHtml,
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
 * Retrieve the status or result of a localScraper request, including results of previous requests.
 *
 * @param {string} apiKey - The API key for ScrapeGraph AI.
 * @param {string} requestId - The unique ID associated with the localScraper request.
 * @returns {Promise<string>} A JSON string containing the status or result of the scraping request.
 * @throws {Error} If an error occurs while retrieving the request details.
 */
export async function getLocalScraperRequest(apiKey, requestId) {
  const endpoint = 'https://api.scrapegraphai.com/v1/localscraper/' + requestId;
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
