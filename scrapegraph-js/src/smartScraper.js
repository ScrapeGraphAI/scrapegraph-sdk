import axios from 'axios';

/**
 * Scrape and extract structured data from a webpage using ScrapeGraph AI.
 * 
 * @param {string} apiKey - Your ScrapeGraph AI API key
 * @param {string} url - The URL of the webpage to scrape
 * @param {string} prompt - Natural language prompt describing what data to extract
 * @param {Object} [schema] - Optional schema object defining the output structure
 * @returns {Promise<string>} Extracted data in JSON format matching the provided schema
 */
export async function smartScraper(apiKey, url, prompt, schema = null) {
  const endpoint = "https://api.scrapegraphai.com/v1/smartscraper";
  const headers = {
    "accept": "application/json",
    "SGAI-APIKEY": apiKey,
    "Content-Type": "application/json"
  };

  const payload = {
    website_url: url,
    user_prompt: prompt
  };

  if (schema) {
    payload.output_schema = {
      description: schema.title || "Schema",
      name: schema.title || "Schema",
      properties: schema.properties || {},
      required: schema.required || []
    };
  }

  try {
    const response = await axios.post(endpoint, payload, { headers });
    return JSON.stringify(response.data);
  } catch (error) {
    if (error.response) {
      if (error.response.status === 403) {
        return JSON.stringify({
          error: "Access forbidden (403)",
          message: "You do not have permission to access this resource."
        });
      }
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

/**
 * Retrieve the status or the result of a scraping request. It also allows you to see the result of old requests.
 * 
 * @param {string} apiKey - Your ScrapeGraph AI API key
 * @param {string} requestId - The request ID associated with the feedback
 * @returns {Promise<string>} Information related to the status or result of a scraping request.
 */
export async function smartScraperInfo(apiKey, requestId) {
  const endpoint = "https://api.scrapegraphai.com/v1/smartscraper/" + requestId;
  const headers = {
    "accept": "application/json",
    "SGAI-APIKEY": apiKey,
  };

  try {
    const response = await axios.get(endpoint, { headers });
    return JSON.stringify(response.data)
  } catch (error) {
    if (error.response) {
      if (error.response.status === 403) {
        return JSON.stringify({
          error: "Access forbidden (403)",
          message: "You do not have permission to access this resource."
        });
      }
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