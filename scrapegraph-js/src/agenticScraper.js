import axios from 'axios';
import handleError from './utils/handleError.js';
import { isMockEnabled, getMockConfig } from './utils/mockConfig.js';
import { getMockResponse } from './utils/mockResponse.js';

/**
 * Perform automated browser actions on a webpage using AI-powered agentic scraping.
 *
 * @param {string} apiKey - Your ScrapeGraph AI API key
 * @param {string} url - The URL of the webpage to interact with
 * @param {string[]} steps - Array of steps to perform on the webpage (e.g., ["Type email@gmail.com in email input box", "click on login"])
 * @param {boolean} [useSession=true] - Whether to use session for the scraping operations
 * @param {string} [userPrompt=null] - Prompt for AI extraction (required when aiExtraction=true)
 * @param {Object} [outputSchema=null] - Schema for structured data extraction (optional, used with aiExtraction=true)
 * @param {boolean} [aiExtraction=false] - Whether to use AI for data extraction from the scraped content
 * @param {Object} options - Optional configuration options
 * @param {boolean} options.mock - Override mock mode for this request
 * @param {boolean} options.renderHeavyJs - Whether to render heavy JavaScript on the page
 * @param {boolean} [options.stealth=false] - Enable stealth mode to avoid bot detection
 * @returns {Promise<Object>} Response from the API containing request_id and initial status
 * @throws {Error} Will throw an error in case of an HTTP failure or invalid parameters.
 *
 * @example
 * // Example usage for basic automated login (no AI extraction):
 * const apiKey = 'your-api-key';
 * const url = 'https://dashboard.scrapegraphai.com/';
 * const steps = [
 *   'Type email@gmail.com in email input box',
 *   'Type test-password@123 in password inputbox',
 *   'click on login'
 * ];
 *
 * try {
 *   const result = await agenticScraper(apiKey, url, steps, true);
 *   console.log('Request ID:', result.request_id);
 *   console.log('Status:', result.status);
 * } catch (error) {
 *   console.error('Error:', error.message);
 * }
 *
 * @example
 * // Example usage with AI extraction:
 * const outputSchema = {
 *   user_info: {
 *     type: "object",
 *     properties: {
 *       username: { type: "string" },
 *       email: { type: "string" },
 *       dashboard_sections: { type: "array", items: { type: "string" } }
 *     }
 *   }
 * };
 *
 * try {
 *   const result = await agenticScraper(
 *     apiKey,
 *     url,
 *     steps,
 *     true,
 *     "Extract user information and available dashboard sections",
 *     outputSchema,
 *     true
 *   );
 *   console.log('Request ID:', result.request_id);
 * } catch (error) {
 *   console.error('Error:', error.message);
 * }
 */
export async function agenticScraper(apiKey, url, steps, useSession = true, userPrompt = null, outputSchema = null, aiExtraction = false, options = {}) {
  const { mock = null, renderHeavyJs = false, stealth = false } = options;

  // Check if mock mode is enabled
  const useMock = mock !== null ? mock : isMockEnabled();
  
  if (useMock) {
    console.log('🧪 Mock mode active. Returning stub for agenticScraper request');
    const mockConfig = getMockConfig();
    const mockData = getMockResponse('POST', 'https://api.scrapegraphai.com/v1/agentic-scrapper', mockConfig.customResponses, mockConfig.customHandler);
    return mockData;
  }

  const endpoint = 'https://api.scrapegraphai.com/v1/agentic-scrapper';
  const headers = {
    'accept': 'application/json',
    'SGAI-APIKEY': apiKey,
    'Content-Type': 'application/json',
  };

  // Validate inputs
  if (!apiKey || typeof apiKey !== 'string') {
    throw new Error('API key must be a non-empty string');
  }

  if (!url || typeof url !== 'string') {
    throw new Error('URL must be a non-empty string');
  }

  if (!url.startsWith('http://') && !url.startsWith('https://')) {
    throw new Error('URL must start with http:// or https://');
  }

  if (!Array.isArray(steps) || steps.length === 0) {
    throw new Error('Steps must be a non-empty array');
  }

  if (steps.some(step => !step || typeof step !== 'string' || !step.trim())) {
    throw new Error('All steps must be non-empty strings');
  }

  if (typeof useSession !== 'boolean') {
    throw new Error('useSession must be a boolean value');
  }

  if (typeof aiExtraction !== 'boolean') {
    throw new Error('aiExtraction must be a boolean value');
  }

  // Validate AI extraction parameters
  if (aiExtraction) {
    if (!userPrompt || typeof userPrompt !== 'string' || !userPrompt.trim()) {
      throw new Error('userPrompt is required and must be a non-empty string when aiExtraction=true');
    }
    
    if (outputSchema !== null && (typeof outputSchema !== 'object' || Array.isArray(outputSchema))) {
      throw new Error('outputSchema must be an object or null');
    }
  }

  const payload = {
    url: url,
    use_session: useSession,
    steps: steps,
    ai_extraction: aiExtraction,
    render_heavy_js: renderHeavyJs,
  };

  if (stealth) {
    payload.stealth = stealth;
  }

  // Add AI extraction parameters if enabled
  if (aiExtraction) {
    payload.user_prompt = userPrompt;
    if (outputSchema) {
      payload.output_schema = outputSchema;
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
 * Retrieve the status or result of an agentic scraper request.
 *
 * @param {string} apiKey - Your ScrapeGraph AI API key
 * @param {string} requestId - The request ID associated with the agentic scraper request
 * @returns {Promise<Object>} A promise that resolves to an object containing:
 *   - status: The current status of the request ('pending', 'completed', 'failed')
 *   - result: The extracted data or automation result when status is 'completed'
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
 *   const result = await getAgenticScraperRequest(apiKey, requestId);
 *   if (result.status === 'completed') {
 *     console.log('Automation completed:', result.result);
 *   } else if (result.status === 'pending') {
 *     console.log('Automation is still in progress');
 *   } else {
 *     console.log('Automation failed:', result.error);
 *   }
 * } catch (error) {
 *   console.error('Error fetching request:', error);
 * }
 *
 * @note The agentic scraper performs browser automation steps sequentially,
 * allowing for complex interactions like form filling, clicking buttons,
 * and navigating through multi-step workflows with session management.
 */
export async function getAgenticScraperRequest(apiKey, requestId, options = {}) {
  const { mock = null } = options;

  // Check if mock mode is enabled
  const useMock = mock !== null ? mock : isMockEnabled();
  
  if (useMock) {
    console.log('🧪 Mock mode active. Returning stub for getAgenticScraperRequest');
    const mockConfig = getMockConfig();
    const mockData = getMockResponse('GET', `https://api.scrapegraphai.com/v1/agentic-scrapper/${requestId}`, mockConfig.customResponses, mockConfig.customHandler);
    return mockData;
  }

  const endpoint = 'https://api.scrapegraphai.com/v1/agentic-scrapper/' + requestId;
  const headers = {
    'accept': 'application/json',
    'SGAI-APIKEY': apiKey,
  };

  // Validate inputs
  if (!apiKey || typeof apiKey !== 'string') {
    throw new Error('API key must be a non-empty string');
  }

  if (!requestId || typeof requestId !== 'string') {
    throw new Error('Request ID must be a non-empty string');
  }

  try {
    const response = await axios.get(endpoint, { headers });
    return response.data;
  } catch (error) {
    handleError(error);
  }
}
