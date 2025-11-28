#!/usr/bin/env node

/**
 * Example demonstrating the ScrapeGraphAI Crawler markdown conversion mode.
 *
 * This example shows how to use the crawler in markdown conversion mode:
 * - Cost-effective markdown conversion (NO AI/LLM processing)
 * - 2 credits per page (80% savings compared to AI mode)
 * - Clean HTML to markdown conversion with metadata extraction
 *
 * Requirements:
 * - Node.js 14+
 * - scrapegraph-js
 * - dotenv
 * - A valid API key (set in .env file as SGAI_APIKEY=your_key or environment variable)
 *
 * Usage:
 *   node crawl_markdown_example.js
 */

import { crawl, getCrawlRequest } from '../index.js';
import 'dotenv/config';

// Example .env file:
// SGAI_APIKEY=your_sgai_api_key

const apiKey = process.env.SGAI_APIKEY;

/**
 * Poll for crawl results with intelligent backoff to avoid rate limits.
 * @param {string} crawlId - The crawl ID to poll for
 * @param {number} maxAttempts - Maximum number of polling attempts
 * @returns {Promise<Object>} The final result or throws an exception on timeout/failure
 */
async function pollForResult(crawlId, maxAttempts = 20) {
  console.log("⏳ Starting to poll for results with rate-limit protection...");

  // Initial wait to give the job time to start processing
  await new Promise(resolve => setTimeout(resolve, 15000));

  for (let attempt = 0; attempt < maxAttempts; attempt++) {
    try {
      const result = await getCrawlRequest(apiKey, crawlId);
      const status = result.status;

      if (status === "success") {
        return result;
      } else if (status === "failed") {
        throw new Error(`Crawl failed: ${result.error || 'Unknown error'}`);
      } else {
        // Calculate progressive wait time: start at 15s, increase gradually
        const baseWait = 15000;
        const progressiveWait = Math.min(60000, baseWait + (attempt * 3000)); // Cap at 60s

        console.log(`⏳ Status: ${status} (attempt ${attempt + 1}/${maxAttempts}) - waiting ${progressiveWait/1000}s...`);
        await new Promise(resolve => setTimeout(resolve, progressiveWait));
      }
    } catch (error) {
      if (error.message.toLowerCase().includes('rate') || error.message.includes('429')) {
        const waitTime = Math.min(90000, 45000 + (attempt * 10000));
        console.log(`⚠️ Rate limit detected in error, waiting ${waitTime/1000}s...`);
        await new Promise(resolve => setTimeout(resolve, waitTime));
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

  // Target URL for markdown conversion
  const url = "https://scrapegraphai.com/";

  console.log(`🌐 Target URL: ${url}`);
  console.log("🤖 AI Prompt: None (no AI processing)");
  console.log("📊 Crawl Depth: 2");
  console.log("📄 Max Pages: 2");
  console.log("🗺️ Use Sitemap: true");
  console.log("💡 Mode: Pure HTML to markdown conversion");
  console.log();

  // Start the markdown conversion job
  console.log("🚀 Starting markdown conversion job...");

  try {
    // Call crawl with extractionMode=false for markdown conversion
    const response = await crawl(apiKey, url, null, null, {
      extractionMode: false, // FALSE = Markdown conversion mode (NO AI/LLM used)
      depth: 2,
      maxPages: 2,
      sameDomainOnly: true,
      sitemap: true, // Use sitemap for better page discovery
      // Note: No prompt or dataSchema needed when extractionMode=false
    });

    const crawlId = response.id || response.task_id || response.crawl_id;

    if (!crawlId) {
      console.log("❌ Failed to start markdown conversion job");
      return;
    }

    console.log(`📋 Crawl ID: ${crawlId}`);
    console.log("⏳ Polling for results...");
    console.log();

    // Poll for results with rate-limit protection
    const result = await pollForResult(crawlId, 20);

    console.log("✅ Markdown conversion completed successfully!");
    console.log();

    const resultData = result.result || {};
    const pages = resultData.pages || [];
    const crawledUrls = resultData.crawled_urls || [];
    const creditsUsed = resultData.credits_used || 0;
    const pagesProcessed = resultData.pages_processed || 0;

    // Prepare JSON output
    const jsonOutput = {
      conversion_results: {
        pages_processed: pagesProcessed,
        credits_used: creditsUsed,
        cost_per_page: pagesProcessed > 0 ? creditsUsed / pagesProcessed : 0,
        crawled_urls: crawledUrls
      },
      markdown_content: {
        total_pages: pages.length,
        pages: []
      }
    };

    // Add page details to JSON
    pages.forEach((page, i) => {
      const metadata = page.metadata || {};
      const pageData = {
        page_number: i + 1,
        url: page.url,
        title: page.title,
        metadata: {
          word_count: metadata.word_count || 0,
          headers: metadata.headers || [],
          links_count: metadata.links_count || 0
        },
        markdown_content: page.markdown || ""
      };
      jsonOutput.markdown_content.pages.push(pageData);
    });

    // Print JSON output
    console.log("📊 RESULTS IN JSON FORMAT:");
    console.log("-".repeat(40));
    console.log(JSON.stringify(jsonOutput, null, 2));

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
  if (!apiKey) {
    console.log("⚠️ Please set your API key in the environment variable SGAI_APIKEY");
    console.log("   Option 1: Create a .env file with: SGAI_APIKEY=your_api_key_here");
    console.log("   Option 2: Set environment variable: export SGAI_APIKEY=your_api_key_here");
    console.log();
    console.log("   You can get your API key from: https://dashboard.scrapegraphai.com");
    return;
  }

  console.log(`🔑 Using API key: ${apiKey.substring(0, 10)}...`);
  console.log();

  // Run the markdown conversion example
  await markdownCrawlingExample();

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
