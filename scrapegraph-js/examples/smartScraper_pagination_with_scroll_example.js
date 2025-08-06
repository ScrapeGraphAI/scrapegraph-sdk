import { smartScraper } from 'scrapegraph-js';
import { z } from 'zod';
import 'dotenv/config';

// Define schema for product data
const ProductSchema = z.object({
  name: z.string().describe('The product name'),
  price: z.string().optional().describe('The product price'),
  rating: z.string().optional().describe('The product rating'),
  image_url: z.string().optional().describe('The product image URL'),
  availability: z.string().optional().describe('Product availability status'),
});

const ProductListSchema = z.object({
  products: z.array(ProductSchema).describe('List of products found'),
  total_count: z.number().optional().describe('Total number of products'),
  page_info: z.object({
    current_page: z.number().optional(),
    total_pages: z.number().optional(),
  }).optional().describe('Pagination information'),
});

const apiKey = process.env.SGAI_APIKEY;
const url = 'https://www.amazon.in/s?k=tv&crid=1TEF1ZFVLU8R8&sprefix=t%2Caps%2C390&ref=nb_sb_noss_2';
const prompt = 'Extract all product information including name, price, rating, image_url, and availability. Also extract pagination info if available.';
const numberOfScrolls = 5; // Scroll to load more products on each page
const totalPages = 3; // Scrape 3 pages total

console.log('🚀 SmartScraper with Pagination and Scrolling');
console.log('='.repeat(60));
console.log(`🌐 URL: ${url}`);
console.log(`📝 Prompt: ${prompt}`);
console.log(`🔄 Number of Scrolls per page: ${numberOfScrolls}`);
console.log(`📄 Total Pages: ${totalPages}`);
console.log(`🏗️ Using structured schema: ProductListSchema`);
console.log('-'.repeat(60));

try {
  const startTime = Date.now();

  const response = await smartScraper(
    apiKey,
    url,
    prompt,
    ProductListSchema,
    numberOfScrolls,
    totalPages
  );

  const duration = Date.now() - startTime;

  console.log(`✅ Request completed in ${duration}ms`);
  console.log('📊 Response type:', typeof response);

  // Validate and display the response
  try {
    const validatedData = ProductListSchema.parse(response);
    console.log(`\n✨ Schema validation successful!`);
    console.log(`📦 Found ${validatedData.products.length} products`);

    if (validatedData.page_info) {
      console.log(`📄 Page info: ${validatedData.page_info.current_page}/${validatedData.page_info.total_pages}`);
    }

    if (validatedData.total_count) {
      console.log(`🔢 Total products: ${validatedData.total_count}`);
    }

    console.log('\n📋 Product Examples:');
    validatedData.products.slice(0, 5).forEach((product, index) => {
      console.log(`  ${index + 1}. ${product.name}`);
      console.log(`     💰 Price: ${product.price || 'N/A'}`);
      console.log(`     ⭐ Rating: ${product.rating || 'N/A'}`);
      console.log(`     📦 Availability: ${product.availability || 'N/A'}`);
      console.log(`     🖼️ Image: ${product.image_url ? 'Available' : 'N/A'}`);
      console.log('');
    });

    if (validatedData.products.length > 5) {
      console.log(`     ... and ${validatedData.products.length - 5} more products`);
    }

  } catch (validationError) {
    console.log('⚠️ Schema validation failed, showing raw response:');
    console.log(JSON.stringify(response, null, 2));
    console.log('\nValidation error:', validationError.message);
  }

  console.log('\n' + '='.repeat(60));
  console.log('✅ Pagination with scrolling completed successfully!');
  console.log('\nFeatures demonstrated:');
  console.log('✓ Multi-page scraping (pagination)');
  console.log('✓ Infinite scrolling on each page');
  console.log('✓ Structured data extraction with Zod schema');
  console.log('✓ Comprehensive error handling');
  console.log('✓ Performance timing');

} catch (error) {
  console.error('\n❌ Error occurred:', error.message);

  // Provide specific error guidance
  if (error.message.includes('totalPages')) {
    console.error('\n🔧 Pagination Error:');
    console.error('- totalPages must be an integer between 1 and 10');
    console.error('- Current value:', totalPages);
  } else if (error.message.includes('numberOfScrolls')) {
    console.error('\n🔧 Scrolling Error:');
    console.error('- numberOfScrolls must be an integer between 0 and 100');
    console.error('- Current value:', numberOfScrolls);
  } else if (error.message.includes('SGAI_APIKEY')) {
    console.error('\n🔧 API Key Error:');
    console.error('- Please set SGAI_APIKEY environment variable');
    console.error('- export SGAI_APIKEY="your-api-key-here"');
  } else {
    console.error('\n🔧 General troubleshooting:');
    console.error('- Check your internet connection');
    console.error('- Verify the website URL is accessible');
    console.error('- Try with fewer pages or scrolls');
    console.error('- Check API key validity');
  }
}
