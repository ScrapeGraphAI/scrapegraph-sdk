#!/usr/bin/env node

/**
 * Example script demonstrating the ScrapeGraphAI Crawler markdown conversion mode.
 *
 * This example shows how to use the crawler in markdown conversion mode:
 * - Cost-effective markdown conversion (NO AI/LLM processing)
 * - 2 credits per page (80% savings compared to AI mode)
 * - Clean HTML to markdown conversion with metadata extraction
 *
 * Requirements:
 * - Node.js 14+
 * - dotenv
 * - A .env file with your API_KEY
 *
 * Example .env file:
 * API_KEY=your_api_key_here
 */

import 'dotenv/config';

// Configuration - API key from environment or fallback
const API_KEY = process.env.TEST_API_KEY || "sgai-xxx"; // Load from .env file
const BASE_URL = process.env.BASE_URL || "http://localhost:8001"; // Can be overridden via env

/**
 * Make an HTTP request to the API.
 * @param {string} url - The URL to make the request to
 * @param {Object} data - The data to send in the request body
 * @returns {Promise<Object>} The response JSON
 */
async function makeRequest(url, data) {
  const headers = {
    "Content-Type": "application/json",
    "SGAI-APIKEY": API_KEY
  };

  const response = await fetch(url, {
    method: 'POST',
    headers: headers,
    body: JSON.stringify(data)
  });

  return await response.json();
}

/**
 * Poll for the result of a crawl job with rate limit handling.
 * @param {string} taskId - The task ID to poll for
 * @returns {Promise<Object>} The response JSON
 */
async function pollResult(taskId) {
  const headers = { "SGAI-APIKEY": API_KEY };
  const url = `${BASE_URL}/v1/crawl/${taskId}`;

  const response = await fetch(url, {
    method: 'GET',
    headers: headers
  });

  if (response.status === 429) {
    // Rate limited - return special status to handle in polling loop
    return { status: "rate_limited", retry_after: 60 };
  }

  return await response.json();
}

/**
 * Poll for crawl results with intelligent backoff to avoid rate limits.
 * @param {string} taskId - The task ID to poll for
 * @param {number} maxAttempts - Maximum number of polling attempts
 * @returns {Promise<Object>} The final result or throws an exception on timeout/failure
 */
async function pollWithBackoff(taskId, maxAttempts = 20) {
  console.log("⏳ Starting to poll for results with rate-limit protection...");

  // Initial wait to give the job time to start processing
  await new Promise(resolve => setTimeout(resolve, 15000));

  for (let attempt = 0; attempt < maxAttempts; attempt++) {
    try {
      const result = await pollResult(taskId);
      const status = result.status;

      if (status === "rate_limited") {
        const waitTime = Math.min(90, 30 + (attempt * 10)); // Exponential backoff for rate limits
        console.log(`⚠️ Rate limited! Waiting ${waitTime}s before retry...`);
        await new Promise(resolve => setTimeout(resolve, waitTime * 1000));
        continue;
      } else if (status === "success") {
        return result;
      } else if (status === "failed") {
        throw new Error(`Crawl failed: ${result.error || 'Unknown error'}`);
      } else {
        // Calculate progressive wait time: start at 15s, increase gradually
        const baseWait = 15;
        const progressiveWait = Math.min(60, baseWait + (attempt * 3)); // Cap at 60s

        console.log(`⏳ Status: ${status} (attempt ${attempt + 1}/${maxAttempts}) - waiting ${progressiveWait}s...`);
        await new Promise(resolve => setTimeout(resolve, progressiveWait * 1000));
      }
    } catch (error) {
      if (error.message.toLowerCase().includes('rate') || error.message.includes('429')) {
        const waitTime = Math.min(90, 45 + (attempt * 10));
        console.log(`⚠️ Rate limit detected in error, waiting ${waitTime}s...`);
        await new Promise(resolve => setTimeout(resolve, waitTime * 1000));
        continue;
      } else {
        console.log(`❌ Error polling for results: ${error.message}`);
        if (attempt < maxAttempts - 1) {
          await new Promise(resolve => setTimeout(resolve, 20000)); // Wait before retry
          continue;
        }
        throw error;
      }
    }
  }

  throw new Error(`⏰ Timeout: Job did not complete after ${maxAttempts} attempts`);
}

/**
 * Markdown Conversion Mode (NO AI/LLM Used)
 *
 * This example demonstrates cost-effective crawling that converts pages to clean markdown
 * WITHOUT any AI processing. Perfect for content archival and when you only need clean markdown.
 */
async function markdownCrawlingExample() {
  console.log("=".repeat(60));
  console.log("MARKDOWN CONVERSION MODE (NO AI/LLM)");
  console.log("=".repeat(60));
  console.log("Use case: Get clean markdown content without AI processing");
  console.log("Cost: 2 credits per page (80% savings!)");
  console.log("Features: Clean markdown conversion, metadata extraction");
  console.log("⚠️ NO AI/LLM PROCESSING - Pure HTML to markdown conversion only!");
  console.log();

  // Markdown conversion request - NO AI/LLM processing
  const requestData = {
    url: "https://scrapegraphai.com/",
    extraction_mode: false, // FALSE = Markdown conversion mode (NO AI/LLM used)
    depth: 2,
    max_pages: 2,
    same_domain_only: true,
    sitemap: false, // Use sitemap for better coverage
    // Note: No prompt needed when extraction_mode = false
  };

  console.log(`🌐 Target URL: ${requestData.url}`);
  console.log("🤖 AI Prompt: None (no AI processing)");
  console.log(`📊 Crawl Depth: ${requestData.depth}`);
  console.log(`📄 Max Pages: ${requestData.max_pages}`);
  console.log(`🗺️ Use Sitemap: ${requestData.sitemap}`);
  console.log("💡 Mode: Pure HTML to markdown conversion");
  console.log();

  // Start the markdown conversion job
  console.log("🚀 Starting markdown conversion job...");
  const response = await makeRequest(`${BASE_URL}/v1/crawl`, requestData);
  const taskId = response.task_id;

  if (!taskId) {
    console.log("❌ Failed to start markdown conversion job");
    return;
  }

  console.log(`📋 Task ID: ${taskId}`);
  console.log("⏳ Polling for results...");
  console.log();

  // Poll for results with rate-limit protection
  try {
    const result = await pollWithBackoff(taskId, 20);

    console.log("✅ Markdown conversion completed successfully!");
    console.log();

    const resultData = result.result || {};
    const pages = resultData.pages || [];
    const crawledUrls = resultData.crawled_urls || [];
    const creditsUsed = resultData.credits_used || 0;
    const pagesProcessed = resultData.pages_processed || 0;

    console.log("📊 CONVERSION RESULTS:");
    console.log("-".repeat(40));
    console.log(`📄 Pages processed: ${pagesProcessed}`);
    console.log(`💰 Credits used: ${creditsUsed}`);
    console.log(`💵 Cost per page: ${pagesProcessed > 0 ? (creditsUsed / pagesProcessed).toFixed(1) : 0} credits`);
    if (crawledUrls.length > 0) {
      console.log(`🔗 URLs processed: ${JSON.stringify(crawledUrls)}`);
    }
    console.log();

    console.log("📝 MARKDOWN CONTENT:");
    console.log("-".repeat(40));
    if (pages.length > 0) {
      console.log(`📄 Total pages with markdown: ${pages.length}`);
      pages.slice(0, 3).forEach((page, i) => { // Show first 3 pages
        console.log(`\n📄 Page ${i + 1}:`);
        console.log(`   URL: ${page.url || 'N/A'}`);
        console.log(`   Title: ${page.title || 'None'}`);

        const metadata = page.metadata || {};
        console.log(`   📊 Word count: ${metadata.word_count || 0}`);
        console.log(`   📋 Headers: ${JSON.stringify((metadata.headers || []).slice(0, 3))}`); // First 3 headers
        console.log(`   🔗 Links: ${metadata.links_count || 0}`);

        // Show markdown preview
        const markdownContent = page.markdown || "";
        let markdownPreview = markdownContent.substring(0, 200);
        if (markdownContent.length > 200) {
          markdownPreview += "...";
        }
        console.log(`   📝 Content preview: ${markdownPreview}`);
      });

      if (pages.length > 3) {
        console.log(`\n   ... and ${pages.length - 3} more pages with markdown content`);
      }
    } else {
      console.log("No markdown content available");
    }

  } catch (error) {
    console.log(`❌ Markdown conversion failed: ${error.message}`);
  }
}

/**
 * Main function to run the markdown crawling example.
 */
async function main() {
  console.log("🌐 ScrapeGraphAI Crawler - Markdown Conversion Example");
  console.log("Cost-effective HTML to Markdown conversion (NO AI/LLM)");
  console.log("=".repeat(60));

  // Check if API key is set
  if (API_KEY === "sgai-xxx") {
    console.log("⚠️ Please set your API key in the .env file");
    console.log("   Create a .env file with your API key:");
    console.log("   API_KEY=your_api_key_here");
    console.log();
    console.log("   You can get your API key from: https://dashboard.scrapegraphai.com");
    console.log();
    console.log("   Example .env file:");
    console.log("   API_KEY=sgai-your-actual-api-key-here");
    console.log("   BASE_URL=https://api.scrapegraphai.com  # Optional");
    return;
  }

  console.log(`🔑 Using API key: ${API_KEY.substring(0, 10)}...`);
  console.log(`🌐 Base URL: ${BASE_URL}`);
  console.log();

  // Run the single example
  await markdownCrawlingExample(); // Markdown conversion mode (NO AI)

  console.log("\n" + "=".repeat(60));
  console.log("🎉 Example completed!");
  console.log("💡 This demonstrates markdown conversion mode:");
  console.log("   • Cost-effective: Only 2 credits per page");
  console.log("   • No AI/LLM processing - pure HTML to markdown conversion");
  console.log("   • Perfect for content archival and documentation");
  console.log("   • 80% cheaper than AI extraction modes!");
}

// Run the example
main().catch(console.error);
