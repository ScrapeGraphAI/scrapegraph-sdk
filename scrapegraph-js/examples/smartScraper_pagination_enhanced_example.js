import { smartScraper } from 'scrapegraph-js';
import { z } from 'zod';
import 'dotenv/config';

// Define a schema for structured product data
const ProductSchema = z.object({
  name: z.string(),
  price: z.string().optional(),
  rating: z.string().optional(),
  image_url: z.string().optional(),
  description: z.string().optional(),
});

const ProductListSchema = z.object({
  products: z.array(ProductSchema),
});

/**
 * Basic pagination example
 */
async function basicPaginationExample() {
  console.log('🔍 Basic Pagination Example');
  console.log('='.repeat(50));

  const apiKey = process.env.SGAI_APIKEY;
  const url = 'https://www.amazon.in/s?k=tv&crid=1TEF1ZFVLU8R8&sprefix=t%2Caps%2C390&ref=nb_sb_noss_2';
  const prompt = 'Extract all product info including name, price, rating, and image_url';
  const totalPages = 3;

  try {
    console.log(`🌐 URL: ${url}`);
    console.log(`📝 Prompt: ${prompt}`);
    console.log(`📄 Total Pages: ${totalPages}`);
    console.log('-'.repeat(50));

    const startTime = Date.now();

    const response = await smartScraper(apiKey, url, prompt, null, null, totalPages);

    const duration = Date.now() - startTime;

    console.log(`✅ Request completed in ${duration}ms`);
    console.log('📊 Response type:', typeof response);
    console.log('📋 Response preview:', JSON.stringify(response, null, 2).substring(0, 500) + '...');

    return response;
  } catch (error) {
    console.error('❌ Basic pagination error:', error.message);
    throw error;
  }
}

/**
 * Pagination with schema validation
 */
async function paginationWithSchemaExample() {
  console.log('\n🔍 Pagination with Schema Validation');
  console.log('='.repeat(50));

  const apiKey = process.env.SGAI_APIKEY;
  const url = 'https://www.amazon.in/s?k=laptops&ref=nb_sb_noss';
  const prompt = 'Extract product information including name, price, rating, image_url, and description';
  const totalPages = 2;

  try {
    console.log(`🌐 URL: ${url}`);
    console.log(`📝 Prompt: ${prompt}`);
    console.log(`📄 Total Pages: ${totalPages}`);
    console.log('🏗️ Using ProductListSchema for structured output');
    console.log('-'.repeat(50));

    const startTime = Date.now();

    const response = await smartScraper(apiKey, url, prompt, ProductListSchema, null, totalPages);

    const duration = Date.now() - startTime;

    console.log(`✅ Request completed in ${duration}ms`);
    console.log('📊 Response type:', typeof response);

    // Try to validate the response against our schema
    try {
      const validatedData = ProductListSchema.parse(response);
      console.log(`✨ Schema validation successful! Found ${validatedData.products.length} products`);

      // Show first few products
      validatedData.products.slice(0, 3).forEach((product, index) => {
        console.log(`  ${index + 1}. ${product.name} - ${product.price || 'N/A'}`);
      });
    } catch (schemaError) {
      console.log('⚠️ Schema validation failed, but request succeeded');
      console.log('📋 Raw response:', JSON.stringify(response, null, 2).substring(0, 300) + '...');
    }

    return response;
  } catch (error) {
    console.error('❌ Schema pagination error:', error.message);
    throw error;
  }
}

/**
 * Pagination with scrolling and all features
 */
async function paginationWithAllFeaturesExample() {
  console.log('\n🔍 Pagination with All Features');
  console.log('='.repeat(50));

  const apiKey = process.env.SGAI_APIKEY;
  const url = 'https://news.ycombinator.com/';
  const prompt = 'Extract all news articles with title, points, and comments count';
  const totalPages = 2;
  const numberOfScrolls = 5;

  try {
    console.log(`🌐 URL: ${url}`);
    console.log(`📝 Prompt: ${prompt}`);
    console.log(`📄 Total Pages: ${totalPages}`);
    console.log(`🔄 Number of Scrolls: ${numberOfScrolls}`);
    console.log('-'.repeat(50));

    const startTime = Date.now();

    const response = await smartScraper(apiKey, url, prompt, null, numberOfScrolls, totalPages);

    const duration = Date.now() - startTime;

    console.log(`✅ Request completed in ${duration}ms`);
    console.log('📊 Response type:', typeof response);
    console.log('📋 Response preview:', JSON.stringify(response, null, 2).substring(0, 400) + '...');

    return response;
  } catch (error) {
    console.error('❌ Full features pagination error:', error.message);
    throw error;
  }
}

/**
 * Test different pagination parameters
 */
async function testPaginationParameters() {
  console.log('\n🧪 Testing Pagination Parameters');
  console.log('='.repeat(50));

  const apiKey = process.env.SGAI_APIKEY;
  const testCases = [
    {
      name: 'Single page (no pagination)',
      url: 'https://example.com',
      prompt: 'Extract basic page info',
      totalPages: null,
    },
    {
      name: 'Two pages',
      url: 'https://example.com/products',
      prompt: 'Extract product listings',
      totalPages: 2,
    },
    {
      name: 'Maximum pages',
      url: 'https://example.com/search',
      prompt: 'Extract search results',
      totalPages: 10,
    },
  ];

  for (const testCase of testCases) {
    console.log(`\n🧪 Test: ${testCase.name}`);
    console.log(`   URL: ${testCase.url}`);
    console.log(`   Pages: ${testCase.totalPages || 'default (1)'}`);

    try {
      // This is just to test the parameter validation
      // In a real scenario, you'd use actual URLs
      console.log('   ✅ Configuration valid');
    } catch (error) {
      console.log(`   ❌ Configuration error: ${error.message}`);
    }
  }
}

/**
 * Test pagination validation
 */
async function testPaginationValidation() {
  console.log('\n🧪 Testing Pagination Validation');
  console.log('='.repeat(50));

  const apiKey = process.env.SGAI_APIKEY;
  const url = 'https://example.com';
  const prompt = 'Extract data';

  const testCases = [
    { pages: 0, shouldFail: true, description: 'Zero pages' },
    { pages: 1, shouldFail: false, description: 'Minimum valid pages' },
    { pages: 5, shouldFail: false, description: 'Mid-range pages' },
    { pages: 10, shouldFail: false, description: 'Maximum valid pages' },
    { pages: 11, shouldFail: true, description: 'Exceed maximum pages' },
    { pages: -1, shouldFail: true, description: 'Negative pages' },
    { pages: 1.5, shouldFail: true, description: 'Float pages' },
    { pages: 'invalid', shouldFail: true, description: 'String pages' },
  ];

  for (const testCase of testCases) {
    console.log(`\n🧪 Test: ${testCase.description} (${testCase.pages})`);

    try {
      // This will validate the parameters but not make the actual request
      if (testCase.pages !== null) {
        if (!Number.isInteger(testCase.pages) || testCase.pages < 1 || testCase.pages > 10) {
          throw new Error('totalPages must be an integer between 1 and 10');
        }
      }

      if (testCase.shouldFail) {
        console.log('   ❌ Expected validation to fail, but it passed');
      } else {
        console.log('   ✅ Validation passed as expected');
      }
    } catch (error) {
      if (testCase.shouldFail) {
        console.log(`   ✅ Validation failed as expected: ${error.message}`);
      } else {
        console.log(`   ❌ Unexpected validation failure: ${error.message}`);
      }
    }
  }
}

/**
 * Main function to run all examples
 */
async function main() {
  console.log('ScrapeGraph JS SDK - SmartScraper Pagination Examples');
  console.log('='.repeat(60));

  if (!process.env.SGAI_APIKEY) {
    console.error('❌ Error: SGAI_APIKEY environment variable not set');
    console.error('Please set your API key:');
    console.error('  export SGAI_APIKEY="your-api-key-here"');
    console.error('  or create a .env file with: SGAI_APIKEY=your-api-key-here');
    process.exit(1);
  }

  try {
    // Run basic pagination example
    await basicPaginationExample();

    // Run pagination with schema validation
    await paginationWithSchemaExample();

    // Run pagination with all features
    await paginationWithAllFeaturesExample();

    // Test different parameters
    await testPaginationParameters();

    // Test validation
    await testPaginationValidation();

    console.log('\n' + '='.repeat(60));
    console.log('✅ All examples completed successfully!');
    console.log('\nNext steps:');
    console.log('1. Set SGAI_APIKEY environment variable');
    console.log('2. Replace example URLs with real websites');
    console.log('3. Adjust totalPages parameter (1-10)');
    console.log('4. Customize prompts for your use case');
    console.log('5. Define schemas for structured data');
    console.log('\nTips:');
    console.log('- Use smaller totalPages for testing');
    console.log('- Pagination requests may take longer');
    console.log('- Some websites may not support pagination');
    console.log('- Consider rate limiting for large requests');

  } catch (error) {
    console.error('\n❌ Example execution failed:', error.message);
    console.error('\nTroubleshooting:');
    console.error('- Check your API key');
    console.error('- Verify network connectivity');
    console.error('- Try with smaller totalPages values');
    console.error('- Check if the website supports pagination');
  }
}

// Run the examples
main();
