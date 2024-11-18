import axios from 'axios';

/**
 * Retrieve credits from the API.
 * 
 * @param {string} apiKey - Your ScrapeGraph AI API key
 * @returns {Promise<string>} Response from the API in JSON format
 */
export async function credits(apiKey) {
  const endpoint = "https://sgai-api.onrender.com/api/v1/credits";
  const headers = {
    "accept": "application/json",
    "SGAI-API-KEY": apiKey
  };

  try {
    const response = await axios.get(endpoint, { headers });
    return JSON.stringify(response.data);
  } catch (error) {
    if (error.response) {
      return JSON.stringify({
        error: "HTTP error occurred",
        message: error.message,
        status_code: error.response.status
      });
    }
    return JSON.stringify({
      error: "An error occurred",
      message: error.message
    });
  }
} 