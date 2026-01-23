import axios from 'axios';
import handleError from './utils/handleError.js';
import { ZodType } from 'zod';
import { zodToJsonSchema } from 'zod-to-json-schema';
import { isMockEnabled, getMockConfig } from './utils/mockConfig.js';
import { getMockResponse } from './utils/mockResponse.js';

/**
 * Start a crawl job using the ScrapeGraphAI API.
 *
 * @param {string} apiKey - Your ScrapeGraph AI API key
 * @param {string} url - The starting URL for the crawl
 * @param {string|null} prompt - The prompt to guide the crawl and extraction (null for markdown mode)
 * @param {Object|ZodType|null} schema - JSON schema or Zod schema defining the structure of the extracted data (null for markdown mode)
 * @param {Object} [options] - Optional crawl parameters
 * @param {boolean} [options.extractionMode=true] - true for AI extraction, false for markdown conversion (NO AI/LLM)
 * @param {boolean} [options.cacheWebsite=true] - Whether to cache the website content
 * @param {number} [options.depth=2] - Maximum depth of the crawl (1-10)
 * @param {number} [options.maxPages=2] - Maximum number of pages to crawl (1-100)
 * @param {boolean} [options.sameDomainOnly=true] - Whether to only crawl pages from the same domain
 * @param {boolean} [options.sitemap] - Whether to use sitemap for better page discovery
 * @param {number} [options.batchSize=1] - Batch size for processing pages (1-10)
 * @param {boolean} [options.mock] - Override mock mode for this request
 * @param {boolean} [options.renderHeavyJs=false] - Whether to render heavy JavaScript on the page
 * @param {boolean} [options.stealth=false] - Enable stealth mode to avoid bot detection
 * @param {Array<string>} [options.includePaths] - List of path patterns to include (e.g., ['/products/*', '/blog/**']). Supports wildcards: * matches any characters, ** matches any path segments
 * @param {Array<string>} [options.excludePaths] - List of path patterns to exclude (e.g., ['/admin/*', '/api/*']). Supports wildcards and takes precedence over includePaths
 * @param {string} [options.webhookUrl] - URL to receive webhook notifications when the crawl job completes
 * @returns {Promise<Object>} The crawl job response
 * @throws {Error} Throws an error if the HTTP request fails
 */
export async function crawl(
  apiKey,
  url,
  prompt,
  schema,
  options = {}
) {
  const { mock = null, renderHeavyJs = false, stealth = false, includePaths = null, excludePaths = null, webhookUrl = null } = options;

  // Check if mock mode is enabled
  const useMock = mock !== null ? mock : isMockEnabled();
  
  if (useMock) {
    console.log('🧪 Mock mode active. Returning stub for crawl request');
    const mockConfig = getMockConfig();
    const mockData = getMockResponse('POST', 'https://api.scrapegraphai.com/v1/crawl', mockConfig.customResponses, mockConfig.customHandler);
    return mockData;
  }
  const endpoint = 'https://api.scrapegraphai.com/v1/crawl';
  const headers = {
    'accept': 'application/json',
    'SGAI-APIKEY': apiKey,
    'Content-Type': 'application/json',
  };

  let schemaPayload = null;
  if (schema !== null && schema !== undefined) {
    if (schema instanceof ZodType) {
      schemaPayload = zodToJsonSchema(schema);
    } else if (typeof schema === 'object') {
      schemaPayload = schema;
    } else {
      throw new Error('The schema must be a Zod schema, a plain object, or null');
    }
  }

  const {
    cacheWebsite = true,
    depth = 2,
    maxPages = 2,
    sameDomainOnly = true,
    sitemap = false,
    batchSize = 1,
  } = options;

  const payload = {
    url,
    prompt,
    schema: schemaPayload,
    cache_website: cacheWebsite,
    depth,
    max_pages: maxPages,
    same_domain_only: sameDomainOnly,
    sitemap,
    batch_size: batchSize,
    render_heavy_js: renderHeavyJs,
  };

  if (stealth) {
    payload.stealth = stealth;
  }

  if (includePaths) {
    payload.include_paths = includePaths;
  }

  if (excludePaths) {
    payload.exclude_paths = excludePaths;
  }

  if (webhookUrl) {
    payload.webhook_url = webhookUrl;
  }

  try {
    const response = await axios.post(endpoint, payload, { headers });
    return response.data;
  } catch (error) {
    handleError(error);
  }
}

/**
 * Get the result of a crawl job by ID.
 *
 * @param {string} apiKey - Your ScrapeGraph AI API key
 * @param {string} crawlId - The crawl job ID
 * @returns {Promise<Object>} The crawl result
 * @throws {Error} Throws an error if the HTTP request fails
 */
export async function getCrawlRequest(apiKey, crawlId, options = {}) {
  const { mock = null } = options;

  // Check if mock mode is enabled
  const useMock = mock !== null ? mock : isMockEnabled();
  
  if (useMock) {
    console.log('🧪 Mock mode active. Returning stub for getCrawlRequest');
    const mockConfig = getMockConfig();
    const mockData = getMockResponse('GET', `https://api.scrapegraphai.com/v1/crawl/${crawlId}`, mockConfig.customResponses, mockConfig.customHandler);
    return mockData;
  }

  const endpoint = `https://api.scrapegraphai.com/v1/crawl/${crawlId}`;
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
