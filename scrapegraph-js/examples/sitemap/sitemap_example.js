import { sitemap } from 'scrapegraph-js';
import fs from 'fs';
import 'dotenv/config';

/**
 * Example: Extract sitemap URLs from a website
 *
 * This example demonstrates how to use the sitemap endpoint to extract
 * all URLs from a website's sitemap.xml file.
 */

// Get API key from environment variable
const apiKey = process.env.SGAI_APIKEY;

// Target website URL
const url = 'https://scrapegraphai.com/';

console.log('🗺️  Extracting sitemap from:', url);
console.log('⏳ Please wait...\n');

try {
  // Call the sitemap endpoint
  const response = await sitemap(apiKey, url);

  console.log('✅ Sitemap extracted successfully!');
  console.log(`📊 Total URLs found: ${response.urls.length}\n`);

  // Display first 10 URLs
  console.log('📄 First 10 URLs:');
  response.urls.slice(0, 10).forEach((url, index) => {
    console.log(`   ${index + 1}. ${url}`);
  });

  if (response.urls.length > 10) {
    console.log(`   ... and ${response.urls.length - 10} more URLs`);
  }

  // Save the complete list to a file
  saveUrlsToFile(response.urls, 'sitemap_urls.txt');

  // Save as JSON for programmatic use
  saveUrlsToJson(response, 'sitemap_urls.json');

} catch (error) {
  console.error('❌ Error:', error.message);
  process.exit(1);
}

/**
 * Helper function to save URLs to a text file
 */
function saveUrlsToFile(urls, filename) {
  try {
    const content = urls.join('\n');
    fs.writeFileSync(filename, content);
    console.log(`\n💾 URLs saved to: ${filename}`);
  } catch (err) {
    console.error('❌ Error saving file:', err.message);
  }
}

/**
 * Helper function to save complete response as JSON
 */
function saveUrlsToJson(response, filename) {
  try {
    fs.writeFileSync(filename, JSON.stringify(response, null, 2));
    console.log(`💾 JSON saved to: ${filename}`);
  } catch (err) {
    console.error('❌ Error saving JSON:', err.message);
  }
}
