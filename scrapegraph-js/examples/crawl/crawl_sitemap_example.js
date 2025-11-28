#!/usr/bin/env node

/**
 * Example demonstrating the ScrapeGraphAI Crawler with sitemap functionality.
 *
 * This example shows how to use the crawler with sitemap enabled for better page discovery:
 * - Sitemap helps discover more pages efficiently
 * - Better coverage of website content
 * - More comprehensive crawling results
 *
 * Requirements:
 * - Node.js 14+
 * - scrapegraph-js
 * - dotenv
 * - A valid API key (set in .env file as SGAI_APIKEY=your_key or environment variable)
 *
 * Usage:
 *   node crawl_sitemap_example.js
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
 * Sitemap-enabled Crawling Example
 *
 * This example demonstrates how to use sitemap for better page discovery.
 * Sitemap helps the crawler find more pages efficiently by using the website's sitemap.xml.
 */
async function sitemapCrawlingExample() {
  console.log("=".repeat(60));
  console.log("SITEMAP-ENABLED CRAWLING EXAMPLE");
  console.log("=".repeat(60));
  console.log("Use case: Comprehensive website crawling with sitemap discovery");
  console.log("Benefits: Better page coverage, more efficient crawling");
  console.log("Features: Sitemap-based page discovery, structured data extraction");
  console.log();

  // Target URL - using a website that likely has a sitemap
  const url = "https://www.giemmeagordo.com/risultati-ricerca-annunci/?sort=newest&search_city=&search_lat=null&search_lng=null&search_category=0&search_type=0&search_min_price=&search_max_price=&bagni=&bagni_comparison=equal&camere=&camere_comparison=equal";

  // Schema for real estate listings
  const schema = {
    "type": "object",
    "properties": {
      "listings": {
        "type": "array",
        "items": {
          "type": "object",
          "properties": {
            "title": { "type": "string" },
            "price": { "type": "string" },
            "location": { "type": "string" },
            "description": { "type": "string" },
            "features": { "type": "array", "items": { "type": "string" } },
            "url": { "type": "string" }
          }
        }
      }
    }
  };

  const prompt = "Extract all real estate listings with their details including title, price, location, description, and features";

  console.log(`🌐 Target URL: ${url}`);
  console.log("🤖 AI Prompt: Extract real estate listings");
  console.log("📊 Crawl Depth: 1");
  console.log("📄 Max Pages: 10");
  console.log("🗺️ Use Sitemap: true (enabled for better page discovery)");
  console.log("🏠 Same Domain Only: true");
  console.log("💾 Cache Website: true");
  console.log("💡 Mode: AI extraction with sitemap discovery");
  console.log();

  // Start the sitemap-enabled crawl job
  console.log("🚀 Starting sitemap-enabled crawl job...");

  try {
    // Call crawl with sitemap=true for better page discovery
    const response = await crawl(apiKey, url, prompt, schema, {
      extractionMode: true, // AI extraction mode
      depth: 1,
      maxPages: 10,
      sameDomainOnly: true,
      cacheWebsite: true,
      sitemap: true, // Enable sitemap for better page discovery
    });

    const crawlId = response.id || response.task_id || response.crawl_id;

    if (!crawlId) {
      console.log("❌ Failed to start sitemap-enabled crawl job");
      return;
    }

    console.log(`📋 Crawl ID: ${crawlId}`);
    console.log("⏳ Polling for results...");
    console.log();

    // Poll for results with rate-limit protection
    const result = await pollForResult(crawlId, 20);

    console.log("✅ Sitemap-enabled crawl completed successfully!");
    console.log();

    const resultData = result.result || {};
    const llmResult = resultData.llm_result || {};
    const crawledUrls = resultData.crawled_urls || [];
    const creditsUsed = resultData.credits_used || 0;
    const pagesProcessed = resultData.pages_processed || 0;

    // Prepare JSON output
    const jsonOutput = {
      crawl_results: {
        pages_processed: pagesProcessed,
        credits_used: creditsUsed,
        cost_per_page: pagesProcessed > 0 ? creditsUsed / pagesProcessed : 0,
        crawled_urls: crawledUrls,
        sitemap_enabled: true
      },
      extracted_data: llmResult
    };

    // Print JSON output
    console.log("📊 RESULTS IN JSON FORMAT:");
    console.log("-".repeat(40));
    console.log(JSON.stringify(jsonOutput, null, 2));

    // Print summary
    console.log("\n" + "=".repeat(60));
    console.log("📈 CRAWL SUMMARY:");
    console.log("=".repeat(60));
    console.log(`✅ Pages processed: ${pagesProcessed}`);
    console.log(`💰 Credits used: ${creditsUsed}`);
    console.log(`🔗 URLs crawled: ${crawledUrls.length}`);
    console.log(`🗺️ Sitemap enabled: Yes`);
    console.log(`📊 Data extracted: ${llmResult.listings ? llmResult.listings.length : 0} listings found`);

  } catch (error) {
    console.log(`❌ Sitemap-enabled crawl failed: ${error.message}`);
  }
}

/**
 * Main function to run the sitemap crawling example.
 */
async function main() {
  console.log("🌐 ScrapeGraphAI Crawler - Sitemap Example");
  console.log("Comprehensive website crawling with sitemap discovery");
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

  // Run the sitemap crawling example
  await sitemapCrawlingExample();

  console.log("\n" + "=".repeat(60));
  console.log("🎉 Example completed!");
  console.log("💡 This demonstrates sitemap-enabled crawling:");
  console.log("   • Better page discovery using sitemap.xml");
  console.log("   • More comprehensive website coverage");
  console.log("   • Efficient crawling of structured websites");
  console.log("   • Perfect for e-commerce, news sites, and content-heavy websites");
}

// Run the example
main().catch(console.error);
