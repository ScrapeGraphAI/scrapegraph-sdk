/**
 * Example demonstrating how to use the Scrape API with the scrapegraph-js SDK.
 *
 * This example shows how to:
 * 1. Set up the API request for Scrape
 * 2. Make the API call to get HTML content from a website
 * 3. Handle the response and save the HTML content
 * 4. Demonstrate both regular and heavy JS rendering modes
 * 5. Display the results and metadata
 *
 * Requirements:
 * - Node.js 16+
 * - scrapegraph-js
 * - A valid API key
 *
 * Usage:
 * node scrape_example.js
 */

import { scrape, getScrapeRequest } from '../index.js';
import fs from 'fs/promises';
import path from 'path';

// Configuration
const API_KEY = process.env.SGAI_API_KEY || 'your-api-key-here';
const OUTPUT_DIR = 'scrape_output';

/**
 * Get HTML content from a website using the Scrape API.
 *
 * @param {string} websiteUrl - The URL of the website to get HTML from
 * @param {Object} options - Options for the scrape request
 * @returns {Object} The API response containing HTML content and metadata
 */
async function scrapeWebsite(websiteUrl, options = {}) {
  const { renderHeavyJs = false, branding = false, headers = {} } = options;
  
  const jsMode = renderHeavyJs ? 'with heavy JS rendering' : 'without JS rendering';
  const brandingMode = branding ? 'with branding' : 'without branding';
  console.log(`Getting HTML content from: ${websiteUrl}`);
  console.log(`Mode: ${jsMode}, ${brandingMode}`);

  const startTime = Date.now();
  
  try {
    const result = await scrape(API_KEY, websiteUrl, {
      renderHeavyJs,
      branding,
      headers
    });
    
    const executionTime = (Date.now() - startTime) / 1000;
    console.log(`Execution time: ${executionTime.toFixed(2)} seconds`);
    
    return result;
  } catch (error) {
    console.error(`Error: ${error.message}`);
    throw error;
  }
}

/**
 * Save HTML content to a file.
 *
 * @param {string} htmlContent - The HTML content to save
 * @param {string} filename - The name of the file (without extension)
 * @param {string} outputDir - The directory to save the file in
 * @returns {string} Path to the saved file
 */
async function saveHtmlContent(htmlContent, filename, outputDir = OUTPUT_DIR) {
  // Create output directory if it doesn't exist
  try {
    await fs.mkdir(outputDir, { recursive: true });
  } catch (error) {
    if (error.code !== 'EEXIST') {
      throw error;
    }
  }

  // Save HTML file
  const htmlFile = path.join(outputDir, `${filename}.html`);
  await fs.writeFile(htmlFile, htmlContent, 'utf8');

  console.log(`HTML content saved to: ${htmlFile}`);
  return htmlFile;
}

/**
 * Analyze HTML content and provide basic statistics.
 *
 * @param {string} htmlContent - The HTML content to analyze
 * @returns {Object} Basic statistics about the HTML content
 */
function analyzeHtmlContent(htmlContent) {
  const stats = {
    totalLength: htmlContent.length,
    lines: htmlContent.split('\n').length,
    hasDoctype: htmlContent.trim().startsWith('<!DOCTYPE'),
    hasHtmlTag: htmlContent.toLowerCase().includes('<html'),
    hasHeadTag: htmlContent.toLowerCase().includes('<head'),
    hasBodyTag: htmlContent.toLowerCase().includes('<body'),
    scriptTags: (htmlContent.match(/<script/gi) || []).length,
    styleTags: (htmlContent.match(/<style/gi) || []).length,
    divTags: (htmlContent.match(/<div/gi) || []).length,
    pTags: (htmlContent.match(/<p/gi) || []).length,
    imgTags: (htmlContent.match(/<img/gi) || []).length,
    linkTags: (htmlContent.match(/<link/gi) || []).length,
  };

  return stats;
}

/**
 * Main function demonstrating Scrape API usage.
 */
async function main() {
  // Example websites to test
  const testWebsites = [
    {
      url: 'https://example.com',
      name: 'example',
      renderHeavyJs: false,
      branding: false,
      description: 'Simple static website',
    },
    {
      url: 'https://www.cubic.dev/',
      name: 'cubic_dev',
      renderHeavyJs: false,
      branding: true,
      description: 'Website with branding enabled',
    },
    {
      url: 'https://httpbin.org/html',
      name: 'httpbin_html',
      renderHeavyJs: false,
      branding: false,
      description: 'HTTP testing service',
    },
  ];

  console.log('Scrape API Example with scrapegraph-js SDK');
  console.log('='.repeat(60));

  // Check API key
  if (!API_KEY || API_KEY === 'your-api-key-here') {
    console.error('❌ Please set your SGAI_API_KEY environment variable');
    console.error('Example: export SGAI_API_KEY=your_api_key_here');
    process.exit(1);
  }

  console.log('✅ API key configured');

  for (const website of testWebsites) {
    console.log(`\nTesting: ${website.description}`);
    console.log('-'.repeat(40));

    try {
      // Get HTML content
      const result = await scrapeWebsite(website.url, {
        renderHeavyJs: website.renderHeavyJs,
        branding: website.branding
      });

      // Display response metadata
      console.log(`Request ID: ${result.scrape_request_id || 'N/A'}`);
      console.log(`Status: ${result.status || 'N/A'}`);
      console.log(`Error: ${result.error || 'None'}`);

      // Analyze HTML content
      const htmlContent = result.html || '';
      if (htmlContent) {
        const stats = analyzeHtmlContent(htmlContent);
        console.log('\nHTML Content Analysis:');
        console.log(`  Total length: ${stats.totalLength.toLocaleString()} characters`);
        console.log(`  Lines: ${stats.lines.toLocaleString()}`);
        console.log(`  Has DOCTYPE: ${stats.hasDoctype}`);
        console.log(`  Has HTML tag: ${stats.hasHtmlTag}`);
        console.log(`  Has Head tag: ${stats.hasHeadTag}`);
        console.log(`  Has Body tag: ${stats.hasBodyTag}`);
        console.log(`  Script tags: ${stats.scriptTags}`);
        console.log(`  Style tags: ${stats.styleTags}`);
        console.log(`  Div tags: ${stats.divTags}`);
        console.log(`  Paragraph tags: ${stats.pTags}`);
        console.log(`  Image tags: ${stats.imgTags}`);
        console.log(`  Link tags: ${stats.linkTags}`);

        // Save HTML content
        const brandingSuffix = website.branding ? '_branding' : '';
        const filename = `${website.name}_${website.renderHeavyJs ? 'js' : 'nojs'}${brandingSuffix}`;
        await saveHtmlContent(htmlContent, filename);

        // Show first 500 characters as preview
        const preview = htmlContent.substring(0, 500).replace(/\n/g, ' ').trim();
        console.log(`\nHTML Preview (first 500 chars):`);
        console.log(`  ${preview}...`);
      } else {
        console.log('No HTML content received');
      }

    } catch (error) {
      console.error(`Error processing ${website.url}: ${error.message}`);
    }

    console.log('\n' + '='.repeat(60));
  }

  console.log(`\n📁 Output saved to: ${OUTPUT_DIR}/`);
  console.log('✅ Scrape example completed successfully');
}

// Run the example
if (import.meta.url === `file://${process.argv[1]}`) {
  main().catch(error => {
    console.error('❌ Fatal error:', error.message);
    process.exit(1);
  });
}
