import { smartScraper } from '../../index.js';
import 'dotenv/config';

/**
 * Example: Using SmartScraper with Markdown content
 *
 * This example demonstrates how to use the SmartScraper with local Markdown content
 * instead of fetching from a URL. This is useful when you already have markdown
 * content and want to extract structured data from it.
 */

const apiKey = process.env.SGAI_APIKEY;

if (!apiKey) {
  console.error('❌ Error: SGAI_APIKEY environment variable is not set');
  console.log('💡 Please set your API key: export SGAI_APIKEY="your-api-key"');
  process.exit(1);
}

// Sample markdown content (e.g., from a file or API response)
const markdownContent = `
# Product Catalog

## Featured Products

### Laptop Pro 15
- **Brand**: TechCorp
- **Price**: $1,299.99
- **Rating**: 4.5/5
- **In Stock**: Yes
- **Description**: High-performance laptop with 15-inch display, 16GB RAM, and 512GB SSD

### Wireless Mouse Elite
- **Brand**: PeripheralCo
- **Price**: $29.99
- **Rating**: 4.8/5
- **In Stock**: Yes
- **Description**: Ergonomic wireless mouse with precision tracking

### USB-C Hub Pro
- **Brand**: ConnectTech
- **Price**: $49.99
- **Rating**: 4.3/5
- **In Stock**: No
- **Description**: 7-in-1 USB-C hub with HDMI, USB 3.0, and SD card reader

## Customer Reviews

> "The Laptop Pro 15 is amazing! Fast and reliable." - John D.

> "Great mouse, very comfortable for long work sessions." - Sarah M.

## Shipping Information

Free shipping on orders over $50. Standard delivery takes 3-5 business days.
`;

async function runExample() {
  console.log('🚀 SmartScraper Markdown Example');
  console.log('='.repeat(60));
  console.log('');

  try {
    console.log('📝 Processing Markdown content...');
    console.log(`📏 Content size: ${(Buffer.byteLength(markdownContent, 'utf8') / 1024).toFixed(2)} KB`);
    console.log('');

    const prompt = 'Extract all products with their names, brands, prices, ratings, and stock status';

    console.log('🔍 Prompt:', prompt);
    console.log('⏳ Sending request to ScrapeGraph AI...');
    console.log('');

    const result = await smartScraper(
      apiKey,
      null, // url is null when using markdown
      prompt,
      null, // schema (optional)
      null, // numberOfScrolls (not applicable for markdown)
      null, // totalPages (not applicable for markdown)
      null, // cookies (not applicable for markdown)
      {}, // options
      false, // plain_text
      false, // renderHeavyJs (not applicable for markdown)
      false, // stealth (not applicable for markdown)
      null, // websiteHtml
      markdownContent // websiteMarkdown
    );

    console.log('✅ Success! Extraction completed.');
    console.log('');
    console.log('📊 Extracted Data:');
    console.log('='.repeat(60));
    console.log(JSON.stringify(result, null, 2));
    console.log('='.repeat(60));

  } catch (error) {
    console.error('❌ Error:', error.message);
    if (error.response) {
      console.error('API Response:', error.response.data);
    }
    process.exit(1);
  }
}

console.log('💡 This example demonstrates:');
console.log('  - Processing local Markdown content');
console.log('  - Extracting structured data from markdown');
console.log('  - Using null for URL parameter when using markdown');
console.log('  - Content size validation (max 2MB)');
console.log('');

runExample();
