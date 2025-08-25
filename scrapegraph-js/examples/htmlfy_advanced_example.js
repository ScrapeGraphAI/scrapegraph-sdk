/**
 * Advanced example demonstrating comprehensive usage of the HTMLfy API with the scrapegraph-js SDK.
 *
 * This example shows how to:
 * 1. Set up the client for HTMLfy with various configurations
 * 2. Handle different types of websites and rendering modes
 * 3. Implement error handling and retry logic
 * 4. Process multiple websites concurrently
 * 5. Save and analyze HTML content with detailed metadata
 * 6. Use custom headers and cookies for authentication
 * 7. Compare different rendering modes
 *
 * Requirements:
 * - Node.js 16+
 * - scrapegraph-js
 * - A valid API key
 *
 * Usage:
 * node htmlfy_advanced_example.js
 */

import { htmlfy, getHtmlfyRequest } from '../index.js';
import fs from 'fs/promises';
import path from 'path';

// Configuration
const API_KEY = process.env.SGAI_API_KEY || 'your-api-key-here';
const OUTPUT_DIR = 'htmlfy_advanced_output';

/**
 * HTMLfy processor with advanced features
 */
class HtmlfyProcessor {
  constructor(apiKey) {
    this.apiKey = apiKey;
    this.retryDelays = [1000, 2000, 4000]; // Exponential backoff delays
  }

  /**
   * Get HTML content from a website using the HTMLfy API with retry logic.
   *
   * @param {string} websiteUrl - The URL of the website to get HTML from
   * @param {Object} options - Options for the HTMLfy request
   * @returns {Object} The API response with additional metadata
   */
  async htmlfyWebsite(websiteUrl, options = {}) {
    const { renderHeavyJs = false, headers = {}, maxRetries = 3 } = options;
    
    const jsMode = renderHeavyJs ? 'with heavy JS rendering' : 'without JS rendering';
    console.log(`🌐 Getting HTML content from: ${websiteUrl}`);
    console.log(`🔧 Mode: ${jsMode}`);
    
    for (let attempt = 0; attempt < maxRetries; attempt++) {
      try {
        const startTime = Date.now();
        const result = await htmlfy(this.apiKey, websiteUrl, {
          renderHeavyJs,
          headers
        });
        const executionTime = (Date.now() - startTime) / 1000;
        
        console.log(`✅ Success! Execution time: ${executionTime.toFixed(2)} seconds`);
        return {
          ...result,
          executionTime,
          attempts: attempt + 1
        };
        
      } catch (error) {
        console.error(`❌ Attempt ${attempt + 1} failed: ${error.message}`);
        if (attempt < maxRetries - 1) {
          const waitTime = this.retryDelays[attempt] || 2000;
          console.log(`⏳ Waiting ${waitTime}ms before retry...`);
          await new Promise(resolve => setTimeout(resolve, waitTime));
        } else {
          console.error(`💥 All ${maxRetries} attempts failed for ${websiteUrl}`);
          throw error;
        }
      }
    }
  }

  /**
   * Process multiple websites concurrently.
   *
   * @param {Array} websites - Array of website configurations
   * @param {number} maxConcurrency - Maximum number of concurrent requests
   * @returns {Array} Results for each website
   */
  async processWebsiteBatch(websites, maxConcurrency = 3) {
    const results = [];
    
    // Process websites in batches to control concurrency
    for (let i = 0; i < websites.length; i += maxConcurrency) {
      const batch = websites.slice(i, i + maxConcurrency);
      const batchPromises = batch.map(website => 
        this.processSingleWebsite(website)
      );
      
      const batchResults = await Promise.allSettled(batchPromises);
      
      for (let j = 0; j < batchResults.length; j++) {
        const result = batchResults[j];
        if (result.status === 'fulfilled') {
          results.push(result.value);
          console.log(`✅ Completed: ${batch[j].url}`);
        } else {
          const website = batch[j];
          console.error(`❌ Failed: ${website.url} - ${result.reason.message}`);
          results.push({
            website,
            error: result.reason.message,
            status: 'failed'
          });
        }
      }
    }
    
    return results;
  }

  /**
   * Process a single website and return results.
   *
   * @param {Object} website - Website configuration
   * @returns {Object} Processing result
   */
  async processSingleWebsite(website) {
    try {
      // Get HTML content
      const result = await this.htmlfyWebsite(website.url, {
        renderHeavyJs: website.renderHeavyJs || false,
        headers: website.headers
      });
      
      // Analyze HTML content
      const htmlContent = result.html || '';
      if (htmlContent) {
        const stats = this.analyzeHtmlContent(htmlContent);
        result.analysis = stats;
        
        // Save HTML content
        const filename = this.generateFilename(website, result);
        const savedFile = await this.saveHtmlContent(htmlContent, filename);
        result.savedFile = savedFile;
        
        // Generate summary
        result.summary = this.generateSummary(stats, result);
      }
      
      return {
        website,
        result,
        status: 'success'
      };
      
    } catch (error) {
      return {
        website,
        error: error.message,
        status: 'failed'
      };
    }
  }

  /**
   * Analyze HTML content and provide comprehensive statistics.
   *
   * @param {string} htmlContent - The HTML content to analyze
   * @returns {Object} Comprehensive statistics about the HTML content
   */
  analyzeHtmlContent(htmlContent) {
    const stats = {
      basic: {
        totalLength: htmlContent.length,
        lines: htmlContent.split('\n').length,
        words: htmlContent.split(/\s+/).length,
        charactersNoSpaces: htmlContent.replace(/\s/g, '').length,
      },
      structure: {
        hasDoctype: htmlContent.trim().startsWith('<!DOCTYPE'),
        hasHtmlTag: htmlContent.toLowerCase().includes('<html'),
        hasHeadTag: htmlContent.toLowerCase().includes('<head'),
        hasBodyTag: htmlContent.toLowerCase().includes('<body'),
        hasTitleTag: htmlContent.toLowerCase().includes('<title'),
        metaTags: (htmlContent.match(/<meta/gi) || []).length,
      },
      elements: {
        scriptTags: (htmlContent.match(/<script/gi) || []).length,
        styleTags: (htmlContent.match(/<style/gi) || []).length,
        divTags: (htmlContent.match(/<div/gi) || []).length,
        pTags: (htmlContent.match(/<p/gi) || []).length,
        imgTags: (htmlContent.match(/<img/gi) || []).length,
        linkTags: (htmlContent.match(/<link/gi) || []).length,
        aTags: (htmlContent.match(/<a/gi) || []).length,
        spanTags: (htmlContent.match(/<span/gi) || []).length,
        tableTags: (htmlContent.match(/<table/gi) || []).length,
        formTags: (htmlContent.match(/<form/gi) || []).length,
      },
      content: {
        hasJavaScript: htmlContent.toLowerCase().includes('<script'),
        hasCss: htmlContent.toLowerCase().includes('<style'),
        hasForms: htmlContent.toLowerCase().includes('<form'),
        hasTables: htmlContent.toLowerCase().includes('<table'),
        hasImages: htmlContent.toLowerCase().includes('<img'),
        hasLinks: htmlContent.toLowerCase().includes('<a'),
      }
    };
    
    return stats;
  }

  /**
   * Generate a human-readable summary of the HTML content.
   *
   * @param {Object} stats - HTML content statistics
   * @param {Object} result - API response result
   * @returns {string} Human-readable summary
   */
  generateSummary(stats, result) {
    const basic = stats.basic;
    const elements = stats.elements;
    
    let summary = `HTML document with ${basic.totalLength.toLocaleString()} characters `;
    summary += `(${basic.lines.toLocaleString()} lines, ${basic.words.toLocaleString()} words). `;
    
    if (elements.divTags > 0) {
      summary += `Contains ${elements.divTags} div elements, `;
    }
    if (elements.pTags > 0) {
      summary += `${elements.pTags} paragraphs, `;
    }
    if (elements.imgTags > 0) {
      summary += `${elements.imgTags} images, `;
    }
    if (elements.scriptTags > 0) {
      summary += `${elements.scriptTags} script tags, `;
    }
    if (elements.styleTags > 0) {
      summary += `${elements.styleTags} style tags. `;
    }
    
    const executionTime = result.executionTime || 0;
    summary += `Processed in ${executionTime.toFixed(2)} seconds.`;
    
    return summary;
  }

  /**
   * Generate a filename for the saved HTML content.
   *
   * @param {Object} website - Website configuration
   * @param {Object} result - API response result
   * @returns {string} Generated filename
   */
  generateFilename(website, result) {
    const name = website.name || 'website';
    const jsMode = website.renderHeavyJs ? 'js' : 'nojs';
    const timestamp = Date.now();
    return `${name}_${jsMode}_${timestamp}`;
  }

  /**
   * Save HTML content to a file with metadata.
   *
   * @param {string} htmlContent - The HTML content to save
   * @param {string} filename - The name of the file (without extension)
   * @param {string} outputDir - The directory to save the file in
   * @returns {string} Path to the saved file
   */
  async saveHtmlContent(htmlContent, filename, outputDir = OUTPUT_DIR) {
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
    
    // Save metadata file
    const metadataFile = path.join(outputDir, `${filename}_metadata.json`);
    const metadata = {
      filename,
      savedAt: new Date().toISOString(),
      fileSize: htmlContent.length,
      encoding: 'utf-8'
    };
    
    await fs.writeFile(metadataFile, JSON.stringify(metadata, null, 2), 'utf8');
    
    console.log(`💾 HTML content saved to: ${htmlFile}`);
    console.log(`📊 Metadata saved to: ${metadataFile}`);
    return htmlFile;
  }
}

/**
 * Main function demonstrating comprehensive HTMLfy usage.
 */
async function main() {
  // Example websites with different configurations
  const testWebsites = [
    {
      url: 'https://example.com',
      name: 'example',
      renderHeavyJs: false,
      description: 'Simple static website',
      headers: {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
      }
    },
    {
      url: 'https://httpbin.org/html',
      name: 'httpbin_html',
      renderHeavyJs: false,
      description: 'HTTP testing service',
    },
    {
      url: 'https://httpbin.org/json',
      name: 'httpbin_json',
      renderHeavyJs: false,
      description: 'JSON endpoint',
    },
    {
      url: 'https://httpbin.org/headers',
      name: 'httpbin_headers',
      renderHeavyJs: false,
      description: 'Headers endpoint',
      headers: {
        'User-Agent': 'ScrapeGraph-HTMLfy-Example/1.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'
      }
    }
  ];
  
  console.log('🚀 Comprehensive HTMLfy API Example with scrapegraph-js SDK');
  console.log('='.repeat(70));
  
  // Check API key
  if (!API_KEY || API_KEY === 'your-api-key-here') {
    console.error('❌ Please set your SGAI_API_KEY environment variable');
    console.error('Example: export SGAI_API_KEY=your_api_key_here');
    process.exit(1);
  }
  
  try {
    const processor = new HtmlfyProcessor(API_KEY);
    console.log('✅ HTMLfy processor initialized successfully');
    
    console.log('\n📋 Processing websites...');
    
    // Process websites with controlled concurrency
    const results = await processor.processWebsiteBatch(
      testWebsites,
      2 // Limit concurrent requests
    );
    
    // Display summary
    console.log('\n📊 Processing Summary');
    console.log('='.repeat(50));
    
    const successful = results.filter(r => r.status === 'success');
    const failed = results.filter(r => r.status === 'failed');
    
    console.log(`✅ Successful: ${successful.length}`);
    console.log(`❌ Failed: ${failed.length}`);
    
    if (successful.length > 0) {
      console.log('\n🎯 Successful Results:');
      for (const result of successful) {
        const website = result.website;
        const data = result.result;
        const summary = data.summary || 'No summary available';
        console.log(`  🌐 ${website.url}: ${summary}`);
      }
    }
    
    if (failed.length > 0) {
      console.log('\n💥 Failed Results:');
      for (const result of failed) {
        const website = result.website;
        const error = result.error;
        console.log(`  🌐 ${website.url}: ${error}`);
      }
    }
    
    console.log(`\n📁 Output saved to: ${OUTPUT_DIR}/`);
    
  } catch (error) {
    console.error(`❌ Fatal error: ${error.message}`);
    process.exit(1);
  }
}

// Run the example
if (import.meta.url === `file://${process.argv[1]}`) {
  main().catch(error => {
    console.error('❌ Fatal error:', error.message);
    process.exit(1);
  });
}
