import { smartScraper } from '../../index.js';
import 'dotenv/config';

/**
 * Example: Using SmartScraper with HTML content
 *
 * This example demonstrates how to use the SmartScraper with local HTML content
 * instead of fetching from a URL. This is useful when you already have HTML
 * content (e.g., from another source) and want to extract structured data from it.
 */

const apiKey = process.env.SGAI_APIKEY;

if (!apiKey) {
  console.error('❌ Error: SGAI_APIKEY environment variable is not set');
  console.log('💡 Please set your API key: export SGAI_APIKEY="your-api-key"');
  process.exit(1);
}

// Sample HTML content (e.g., from a file or API response)
const htmlContent = `
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Product Catalog</title>
</head>
<body>
  <div class="container">
    <h1>Product Catalog</h1>

    <div class="product" data-id="1">
      <h2>Laptop Pro 15</h2>
      <div class="brand">TechCorp</div>
      <div class="price">$1,299.99</div>
      <div class="rating">4.5/5</div>
      <div class="stock">In Stock</div>
      <p class="description">High-performance laptop with 15-inch display, 16GB RAM, and 512GB SSD</p>
    </div>

    <div class="product" data-id="2">
      <h2>Wireless Mouse Elite</h2>
      <div class="brand">PeripheralCo</div>
      <div class="price">$29.99</div>
      <div class="rating">4.8/5</div>
      <div class="stock">In Stock</div>
      <p class="description">Ergonomic wireless mouse with precision tracking</p>
    </div>

    <div class="product" data-id="3">
      <h2>USB-C Hub Pro</h2>
      <div class="brand">ConnectTech</div>
      <div class="price">$49.99</div>
      <div class="rating">4.3/5</div>
      <div class="stock">Out of Stock</div>
      <p class="description">7-in-1 USB-C hub with HDMI, USB 3.0, and SD card reader</p>
    </div>

    <div class="reviews">
      <h2>Customer Reviews</h2>
      <div class="review">
        <p class="text">"The Laptop Pro 15 is amazing! Fast and reliable."</p>
        <p class="author">- John D.</p>
      </div>
      <div class="review">
        <p class="text">"Great mouse, very comfortable for long work sessions."</p>
        <p class="author">- Sarah M.</p>
      </div>
    </div>

    <div class="shipping-info">
      <h2>Shipping Information</h2>
      <p>Free shipping on orders over $50. Standard delivery takes 3-5 business days.</p>
    </div>
  </div>
</body>
</html>
`;

async function runExample() {
  console.log('🚀 SmartScraper HTML Example');
  console.log('='.repeat(60));
  console.log('');

  try {
    console.log('📄 Processing HTML content...');
    console.log(`📏 Content size: ${(Buffer.byteLength(htmlContent, 'utf8') / 1024).toFixed(2)} KB`);
    console.log('');

    const prompt = 'Extract all products with their names, brands, prices, ratings, and stock status';

    console.log('🔍 Prompt:', prompt);
    console.log('⏳ Sending request to ScrapeGraph AI...');
    console.log('');

    const result = await smartScraper(
      apiKey,
      null, // url is null when using HTML
      prompt,
      null, // schema (optional)
      null, // numberOfScrolls (not applicable for local HTML)
      null, // totalPages (not applicable for local HTML)
      null, // cookies (not applicable for local HTML)
      {}, // options
      false, // plain_text
      false, // renderHeavyJs (not applicable for local HTML)
      false, // stealth (not applicable for local HTML)
      htmlContent, // websiteHtml
      null // websiteMarkdown
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
console.log('  - Processing local HTML content');
console.log('  - Extracting structured data from HTML');
console.log('  - Using null for URL parameter when using HTML');
console.log('  - Content size validation (max 2MB)');
console.log('');

runExample();
