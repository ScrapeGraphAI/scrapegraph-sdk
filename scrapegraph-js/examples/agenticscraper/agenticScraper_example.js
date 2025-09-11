import { agenticScraper } from 'scrapegraph-js';
import 'dotenv/config';

const apiKey = process.env.SGAI_APIKEY;

// Example 1: Basic scraping without AI extraction
console.log('🤖 Example 1: Basic Agentic Scraping (No AI)');
console.log('='.repeat(50));

const url = 'https://dashboard.scrapegraphai.com/';
const steps = [
  'Type email@gmail.com in email input box',
  'Type test-password@123 in password inputbox',
  'click on login'
];

try {
  const response = await agenticScraper(
    apiKey, 
    url, 
    steps, 
    true,  // useSession
    null,  // userPrompt (not needed for basic scraping)
    null,  // outputSchema (not needed for basic scraping)
    false  // aiExtraction = false
  );
  
  console.log('✅ Basic Agentic Scraper Request Submitted');
  console.log('Request ID:', response.request_id);
  console.log('Status:', response.status);
  console.log('Full Response:', JSON.stringify(response, null, 2));
} catch (error) {
  console.error('❌ Error:', error.message);
}

// Example 2: AI extraction for structured data
console.log('\n\n🧠 Example 2: Agentic Scraping with AI Extraction');
console.log('='.repeat(50));

const aiExtractionSchema = {
  dashboard_info: {
    type: "object",
    properties: {
      username: { type: "string" },
      email: { type: "string" },
      available_sections: { 
        type: "array", 
        items: { type: "string" } 
      },
      credits_remaining: { type: "number" }
    },
    required: ["username", "available_sections"]
  }
};

const userPrompt = "Extract the user's dashboard information including username, email, available dashboard sections, and remaining credits";

try {
  const aiResponse = await agenticScraper(
    apiKey,
    url,
    [...steps, 'wait for dashboard to load completely'], // Add wait step for AI extraction
    true,       // useSession
    userPrompt, // userPrompt for AI extraction
    aiExtractionSchema, // outputSchema for structured data
    true        // aiExtraction = true
  );
  
  console.log('✅ AI Extraction Request Submitted');
  console.log('Request ID:', aiResponse.request_id);
  console.log('Status:', aiResponse.status);
  console.log('User Prompt:', userPrompt);
  console.log('Schema Provided:', aiExtractionSchema ? 'Yes' : 'No');
  console.log('Full Response:', JSON.stringify(aiResponse, null, 2));
} catch (error) {
  console.error('❌ AI Extraction Error:', error.message);
}
