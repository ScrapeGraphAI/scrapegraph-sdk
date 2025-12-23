/**
 * Example of using the crawl endpoint with path filtering.
 *
 * This example demonstrates how to use includePaths and excludePaths
 * to control which pages are crawled on a website.
 */

import { crawl, getCrawlRequest } from 'scrapegraph-js';
import dotenv from 'dotenv';

dotenv.config();

const SGAI_API_KEY = process.env.SGAI_APIKEY || process.env.SGAI_API_KEY;

// Define your output schema
const productSchema = {
  type: 'object',
  properties: {
    products: {
      type: 'array',
      items: {
        type: 'object',
        properties: {
          name: { type: 'string', description: 'Product name' },
          price: { type: 'string', description: 'Product price' },
          description: { type: 'string', description: 'Product description' },
          category: { type: 'string', description: 'Product category' }
        },
        required: ['name', 'price']
      }
    },
    total_products: {
      type: 'number',
      description: 'Total number of products found'
    }
  },
  required: ['products', 'total_products']
};

// Helper function to wait for crawl completion
async function waitForCrawl(taskId, maxAttempts = 60, delay = 5000) {
  for (let attempt = 0; attempt < maxAttempts; attempt++) {
    await new Promise(resolve => setTimeout(resolve, delay));

    const status = await getCrawlRequest(SGAI_API_KEY, taskId);
    const state = status.state || 'UNKNOWN';

    console.log(`Attempt ${attempt + 1}: Status = ${state}`);

    if (state === 'SUCCESS') {
      console.log('\n✨ Crawl completed successfully!');
      return status.result;
    } else if (state === 'FAILURE' || state === 'REVOKED') {
      console.log(`\n❌ Crawl failed with status: ${state}`);
      throw new Error(`Crawl failed: ${state}`);
    }
  }

  throw new Error('Timeout: Crawl took too long');
}

async function example1() {
  console.log('\n📝 Example 1: Crawl only /products/* pages');
  console.log('-'.repeat(50));

  const result = await crawl(
    SGAI_API_KEY,
    'https://example.com',
    'Extract product information including name, price, and description',
    productSchema,
    {
      depth: 2,
      maxPages: 10,
      includePaths: ['/products/*', '/items/*'],  // Only crawl product pages
      excludePaths: ['/products/archived/*']      // But skip archived products
    }
  );

  console.log(`Task ID: ${result.task_id}`);
  console.log('\n✅ Crawl job started successfully!');

  return result.task_id;
}

async function example2() {
  console.log('\n📝 Example 2: Crawl all pages except admin and API');
  console.log('-'.repeat(50));

  const result = await crawl(
    SGAI_API_KEY,
    'https://example.com',
    'Extract all relevant information from the website',
    productSchema,
    {
      depth: 2,
      maxPages: 20,
      excludePaths: [
        '/admin/*',      // Skip all admin pages
        '/api/*',        // Skip all API endpoints
        '/private/*',    // Skip private pages
        '/*.json'        // Skip JSON files
      ]
    }
  );

  console.log(`Task ID: ${result.task_id}`);
  console.log('\n✅ Crawl job started successfully!');

  return result.task_id;
}

async function example3() {
  console.log('\n📝 Example 3: Complex path filtering with wildcards');
  console.log('-'.repeat(50));

  const blogSchema = {
    type: 'object',
    properties: {
      posts: {
        type: 'array',
        items: {
          type: 'object',
          properties: {
            title: { type: 'string' },
            author: { type: 'string' },
            date: { type: 'string' },
            content: { type: 'string' }
          }
        }
      }
    }
  };

  const result = await crawl(
    SGAI_API_KEY,
    'https://example.com',
    'Extract blog posts with title, author, date, and content',
    blogSchema,
    {
      depth: 3,
      maxPages: 15,
      sitemap: true,  // Use sitemap for better coverage
      includePaths: [
        '/blog/**',           // Include all blog pages (any depth)
        '/articles/*',        // Include top-level articles
        '/news/2024/*'        // Include 2024 news only
      ],
      excludePaths: [
        '/blog/draft/*',      // Skip draft blog posts
        '/blog/*/comments'    // Skip comment pages
      ]
    }
  );

  console.log(`Task ID: ${result.task_id}`);
  console.log('\n✅ Crawl job started successfully!');

  return result.task_id;
}

async function main() {
  try {
    console.log('🔍 Starting crawl with path filtering...');
    console.log('='.repeat(50));

    // Run example 1
    const taskId1 = await example1();

    // Run example 2
    const taskId2 = await example2();

    // Run example 3 and wait for completion
    const taskId3 = await example3();

    // Optionally wait for one of the crawls to complete
    console.log(`\n⏳ Waiting for example 3 to complete (task: ${taskId3})...`);
    const result = await waitForCrawl(taskId3);

    console.log('\n📊 Crawl Results:');
    console.log(JSON.stringify(result, null, 2));

    // Print guide
    console.log('\n' + '='.repeat(50));
    console.log('📚 Path Filtering Guide:');
    console.log('='.repeat(50));
    console.log('• Use \'/*\' to match a single path segment');
    console.log('  Example: \'/products/*\' matches \'/products/item1\' but not \'/products/cat/item1\'');
    console.log('\n• Use \'/**\' to match any number of path segments');
    console.log('  Example: \'/blog/**\' matches \'/blog/2024/post\' and \'/blog/category/2024/post\'');
    console.log('\n• excludePaths takes precedence over includePaths');
    console.log('  You can include a broad pattern and exclude specific subsets');
    console.log('\n• Paths must start with \'/\'');
    console.log('  Example: \'/products/*\' is valid, \'products/*\' is not');
    console.log('\n💡 Tips:');
    console.log('• Combine with sitemap: true for better page discovery');
    console.log('• Use includePaths to focus on content-rich sections');
    console.log('• Use excludePaths to skip duplicate or irrelevant content');

  } catch (error) {
    console.error('❌ Error:', error.message);
    process.exit(1);
  }
}

main();
