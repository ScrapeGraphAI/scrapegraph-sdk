import axios from 'axios';
import handleError from './utils/handleError.js';

/**
 * Retrieve credits from the API.
 * 
 * @param {string} apiKey - Your ScrapeGraph AI API key
 * @returns {Promise<string>} Response from the API in JSON format
 */
export async function getCredits(apiKey) {
  const endpoint = 'https://api.scrapegraphai.com/v1/credits';
  const headers = {
    'accept': 'application/json',
    'SGAI-APIKEY': apiKey
  };

  try {
    const response = await axios.get(endpoint, { headers });
    return response.data;
  } catch (error) {
    handleError(error)
  }
} 