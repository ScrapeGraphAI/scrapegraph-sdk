import { crawl, getCrawlRequest } from '../index.js';
import 'dotenv/config';

// Example .env file:
// SGAI_APIKEY=your_sgai_api_key

const apiKey = process.env.SGAI_APIKEY;

const schema = {
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "ScrapeGraphAI Website Content",
  "type": "object",
  "properties": {
    "company": {
      "type": "object",
      "properties": {
        "name": { "type": "string" },
        "description": { "type": "string" },
        "features": { "type": "array", "items": { "type": "string" } },
        "contact_email": { "type": "string", "format": "email" },
        "social_links": {
          "type": "object",
          "properties": {
            "github": { "type": "string", "format": "uri" },
            "linkedin": { "type": "string", "format": "uri" },
            "twitter": { "type": "string", "format": "uri" }
          },
          "additionalProperties": false
        }
      },
      "required": ["name", "description"]
    },
    "services": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "service_name": { "type": "string" },
          "description": { "type": "string" },
          "features": { "type": "array", "items": { "type": "string" } }
        },
        "required": ["service_name", "description"]
      }
    },
    "legal": {
      "type": "object",
      "properties": {
        "privacy_policy": { "type": "string" },
        "terms_of_service": { "type": "string" }
      },
      "required": ["privacy_policy", "terms_of_service"]
    }
  },
  "required": ["company", "services", "legal"]
};

const url = 'https://scrapegraphai.com/';
const prompt = 'What does the company do? and I need text content from there privacy and terms';

(async () => {
  if (!apiKey) {
    console.error('SGAI_APIKEY not found in environment. Please set it in your .env file.');
    process.exit(1);
  }

  try {
    // Start the crawl job
    console.log(`\nStarting crawl for: ${url}`);
    const crawlResponse = await crawl(apiKey, url, prompt, schema, {
      cacheWebsite: true,
      depth: 2,
      maxPages: 2,
      sameDomainOnly: true,
      sitemap: true, // Use sitemap for better page discovery
      batchSize: 1,
    });
    console.log('\nCrawl job started. Response:');
    console.log(JSON.stringify(crawlResponse, null, 2));

    // If the crawl is asynchronous and returns an ID, fetch the result
    const crawlId = crawlResponse.id || crawlResponse.task_id;
    if (crawlId) {
      console.log('\nPolling for crawl result...');
      for (let i = 0; i < 10; i++) {
        await new Promise((resolve) => setTimeout(resolve, 5000));
        const result = await getCrawlRequest(apiKey, crawlId);
        if (result.status === 'success' && result.result) {
          console.log(`\nCrawl completed. Result:`);
          console.log(JSON.stringify(result.result.llm_result, null, 2));
          break;
        } else if (result.status === 'failed') {
          console.log('\nCrawl failed. Result:');
          console.log(JSON.stringify(result, null, 2));
          break;
        } else {
          console.log(`Status: ${result.status}, waiting...`);
        }
      }
    } else {
      console.log('No crawl ID found in response. Synchronous result:');
      console.log(JSON.stringify(crawlResponse, null, 2));
    }
  } catch (error) {
    console.error('Error occurred:', error);
  }
})();
