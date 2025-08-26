/**
 * Advanced example demonstrating comprehensive usage of the Scrape API with the scrapegraph-js SDK.
 *
 * This example shows how to:
 * 1. Set up the client for Scrape with various configurations
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
 * node scrape_advanced_example.js
 */

import { scrape, getScrapeRequest } from '../index.js';
import fs from 'fs/promises';
import path from 'path';

// Configuration
const API_KEY = process.env.SGAI_API_KEY || 'your-api-key-here';
const OUTPUT_DIR = 'scrape_advanced_output';

/**
 * Scrape processor with advanced features
 */
class ScrapeProcessor {
  constructor(apiKey) {
    this.apiKey = apiKey;
    this.retryDelays = [1000, 2000, 4000]; // Exponential backoff delays
  }

  /**
   * Get HTML content from a website using the Scrape API with retry logic.
   *
   * @param {string} websiteUrl - The URL of the website to get HTML from
   * @param {Object} options - Options for the scrape request
   * @returns {Object} The API response with additional metadata
   */
  async scrapeWebsite(websiteUrl, options = {}) {
    const { renderHeavyJs = false, headers = {}, maxRetries = 3 } = options;
    
    const jsMode = renderHeavyJs ? 'with heavy JS rendering' : 'without JS rendering';
    console.log(`🌐 Getting HTML content from: ${websiteUrl}`);
    console.log(`🔧 Mode: ${jsMode}`);
    
    for (let attempt = 0; attempt < maxRetries; attempt++) {
      try {
        const startTime = Date.now();
        const result = await scrape(this.apiKey, websiteUrl, {
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
      
      // Process batch results
      batchResults.forEach((result, index) => {
        const website = batch[index];
        if (result.status === 'fulfilled') {
          results.push({
            website: website.url,
            success: true,
            data: result.value
          });
        } else {
          results.push({
            website: website.url,
            success: false,
            error: result.reason.message
          });
        }
      });
      
      // Add a small delay between batches to be respectful to the API
      if (i + maxConcurrency < websites.length) {
        await new Promise(resolve => setTimeout(resolve, 1000));
      }
    }
    
    return results;
  }

  /**
   * Process a single website with comprehensive analysis.
   *
   * @param {Object} website - Website configuration object
   * @returns {Object} Processing results
   */
  async processSingleWebsite(website) {
    const { url, name, renderHeavyJs = false, description, headers = {} } = website;
    
    console.log(`\n🔍 Processing: ${description}`);
    console.log(`📍 URL: ${url}`);
    console.log(`⚙️  Render Heavy JS: ${renderHeavyJs}`);
    
    try {
      // Get HTML content
      const result = await this.scrapeWebsite(url, {
        renderHeavyJs,
        headers
      });
      
      // Analyze the HTML content
      const analysis = this.analyzeHtmlContent(result.html);
      
      // Save the HTML content
      const filename = `${name}_${renderHeavyJs ? 'js' : 'nojs'}`;
      const savedFile = await this.saveHtmlContent(result.html, filename);
      
      // Create comprehensive result object
      const processedResult = {
        website: url,
        name,
        description,
        renderHeavyJs,
        success: true,
        requestId: result.scrape_request_id,
        status: result.status,
        executionTime: result.executionTime,
        attempts: result.attempts,
        analysis,
        savedFile,
        metadata: {
          timestamp: new Date().toISOString(),
          userAgent: headers['User-Agent'] || 'Default',
          hasCustomHeaders: Object.keys(headers).length > 0
        }
      };
      
      console.log(`✅ Successfully processed ${url}`);
      console.log(`📊 Analysis: ${analysis.totalLength.toLocaleString()} chars, ${analysis.lines.toLocaleString()} lines`);
      console.log(`💾 Saved to: ${savedFile}`);
      
      return processedResult;
      
    } catch (error) {
      console.error(`❌ Failed to process ${url}: ${error.message}`);
      return {
        website: url,
        name,
        description,
        renderHeavyJs,
        success: false,
        error: error.message,
        timestamp: new Date().toISOString()
      };
    }
  }

  /**
   * Analyze HTML content and provide detailed statistics.
   *
   * @param {string} htmlContent - The HTML content to analyze
   * @returns {Object} Detailed analysis of the HTML content
   */
  analyzeHtmlContent(htmlContent) {
    if (!htmlContent) {
      return {
        totalLength: 0,
        lines: 0,
        hasDoctype: false,
        hasHtmlTag: false,
        hasHeadTag: false,
        hasBodyTag: false,
        scriptTags: 0,
        styleTags: 0,
        divTags: 0,
        pTags: 0,
        imgTags: 0,
        linkTags: 0,
        aTags: 0,
        spanTags: 0,
        tableTags: 0,
        formTags: 0,
        inputTags: 0,
        buttonTags: 0,
        metaTags: 0,
        titleTags: 0,
        h1Tags: 0,
        h2Tags: 0,
        h3Tags: 0,
        h4Tags: 0,
        h5Tags: 0,
        h6Tags: 0,
        listTags: 0,
        codeTags: 0,
        preTags: 0,
        blockquoteTags: 0,
        iframeTags: 0,
        canvasTags: 0,
        svgTags: 0,
        videoTags: 0,
        audioTags: 0,
        embedTags: 0,
        objectTags: 0,
        paramTags: 0,
        sourceTags: 0,
        trackTags: 0,
        mapTags: 0,
        areaTags: 0,
        baseTags: 0,
        bdoTags: 0,
        brTags: 0,
        hrTags: 0,
        imgTags: 0,
        inputTags: 0,
        linkTags: 0,
        metaTags: 0,
        paramTags: 0,
        sourceTags: 0,
        trackTags: 0,
        wbrTags: 0
      };
    }

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
      aTags: (htmlContent.match(/<a/gi) || []).length,
      spanTags: (htmlContent.match(/<span/gi) || []).length,
      tableTags: (htmlContent.match(/<table/gi) || []).length,
      formTags: (htmlContent.match(/<form/gi) || []).length,
      inputTags: (htmlContent.match(/<input/gi) || []).length,
      buttonTags: (htmlContent.match(/<button/gi) || []).length,
      metaTags: (htmlContent.match(/<meta/gi) || []).length,
      titleTags: (htmlContent.match(/<title/gi) || []).length,
      h1Tags: (htmlContent.match(/<h1/gi) || []).length,
      h2Tags: (htmlContent.match(/<h2/gi) || []).length,
      h3Tags: (htmlContent.match(/<h3/gi) || []).length,
      h4Tags: (htmlContent.match(/<h4/gi) || []).length,
      h5Tags: (htmlContent.match(/<h5/gi) || []).length,
      h6Tags: (htmlContent.match(/<h6/gi) || []).length,
      listTags: (htmlContent.match(/<(ul|ol|li)/gi) || []).length,
      codeTags: (htmlContent.match(/<code/gi) || []).length,
      preTags: (htmlContent.match(/<pre/gi) || []).length,
      blockquoteTags: (htmlContent.match(/<blockquote/gi) || []).length,
      iframeTags: (htmlContent.match(/<iframe/gi) || []).length,
      canvasTags: (htmlContent.match(/<canvas/gi) || []).length,
      svgTags: (htmlContent.match(/<svg/gi) || []).length,
      videoTags: (htmlContent.match(/<video/gi) || []).length,
      audioTags: (htmlContent.match(/<audio/gi) || []).length,
      embedTags: (htmlContent.match(/<embed/gi) || []).length,
      objectTags: (htmlContent.match(/<object/gi) || []).length,
      paramTags: (htmlContent.match(/<param/gi) || []).length,
      sourceTags: (htmlContent.match(/<source/gi) || []).length,
      trackTags: (htmlContent.match(/<track/gi) || []).length,
      mapTags: (htmlContent.match(/<map/gi) || []).length,
      areaTags: (htmlContent.match(/<area/gi) || []).length,
      baseTags: (htmlContent.match(/<base/gi) || []).length,
      bdoTags: (htmlContent.match(/<bdo/gi) || []).length,
      brTags: (htmlContent.match(/<br/gi) || []).length,
      hrTags: (htmlContent.match(/<hr/gi) || []).length,
      wbrTags: (htmlContent.match(/<wbr/gi) || []).length
    };

    return stats;
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
    try {
      await fs.mkdir(outputDir, { recursive: true });
    } catch (error) {
      if (error.code !== 'EEXIST') {
        throw error;
      }
    }

    const htmlFile = path.join(outputDir, `${filename}.html`);
    await fs.writeFile(htmlFile, htmlContent, 'utf8');

    return htmlFile;
  }

  /**
   * Generate a comprehensive report of all processing results.
   *
   * @param {Array} results - Array of processing results
   * @param {string} outputDir - Output directory for the report
   */
  async generateReport(results, outputDir = OUTPUT_DIR) {
    const report = {
      summary: {
        totalWebsites: results.length,
        successful: results.filter(r => r.success).length,
        failed: results.filter(r => !r.success).length,
        timestamp: new Date().toISOString(),
        apiKey: this.apiKey.substring(0, 8) + '...'
      },
      results: results,
      statistics: {
        averageExecutionTime: 0,
        totalExecutionTime: 0,
        averageAttempts: 0,
        totalAttempts: 0
      }
    };

    // Calculate statistics
    const successfulResults = results.filter(r => r.success);
    if (successfulResults.length > 0) {
      report.statistics.averageExecutionTime = 
        successfulResults.reduce((sum, r) => sum + (r.executionTime || 0), 0) / successfulResults.length;
      report.statistics.totalExecutionTime = 
        successfulResults.reduce((sum, r) => sum + (r.executionTime || 0), 0);
      report.statistics.averageAttempts = 
        successfulResults.reduce((sum, r) => sum + (r.attempts || 1), 0) / successfulResults.length;
      report.statistics.totalAttempts = 
        successfulResults.reduce((sum, r) => sum + (r.attempts || 1), 0);
    }

    // Save report as JSON
    const reportFile = path.join(outputDir, 'processing_report.json');
    await fs.writeFile(reportFile, JSON.stringify(report, null, 2), 'utf8');

    // Save summary as text
    const summaryFile = path.join(outputDir, 'summary.txt');
    const summaryText = this.formatSummary(report);
    await fs.writeFile(summaryFile, summaryText, 'utf8');

    console.log(`\n📊 Report generated:`);
    console.log(`   📄 JSON: ${reportFile}`);
    console.log(`   📝 Summary: ${summaryFile}`);

    return { reportFile, summaryFile };
  }

  /**
   * Format the summary report as readable text.
   *
   * @param {Object} report - The processing report
   * @returns {string} Formatted summary text
   */
  formatSummary(report) {
    const { summary, statistics } = report;
    
    let text = 'SCRAPE API PROCESSING REPORT\n';
    text += '='.repeat(50) + '\n\n';
    text += `Generated: ${summary.timestamp}\n`;
    text += `Total Websites: ${summary.totalWebsites}\n`;
    text += `Successful: ${summary.successful}\n`;
    text += `Failed: ${summary.failed}\n`;
    text += `Success Rate: ${((summary.successful / summary.totalWebsites) * 100).toFixed(1)}%\n\n`;
    
    if (summary.successful > 0) {
      text += `PERFORMANCE STATISTICS\n`;
      text += '-'.repeat(30) + '\n';
      text += `Average Execution Time: ${statistics.averageExecutionTime.toFixed(2)}s\n`;
      text += `Total Execution Time: ${statistics.totalExecutionTime.toFixed(2)}s\n`;
      text += `Average Attempts: ${statistics.averageAttempts.toFixed(1)}\n`;
      text += `Total Attempts: ${statistics.totalAttempts}\n\n`;
    }
    
    text += `DETAILED RESULTS\n`;
    text += '-'.repeat(30) + '\n';
    
    report.results.forEach((result, index) => {
      text += `${index + 1}. ${result.website}\n`;
      text += `   Status: ${result.success ? '✅ Success' : '❌ Failed'}\n`;
      if (result.success) {
        text += `   Execution Time: ${result.executionTime?.toFixed(2)}s\n`;
        text += `   Attempts: ${result.attempts}\n`;
        text += `   Saved: ${result.savedFile}\n`;
      } else {
        text += `   Error: ${result.error}\n`;
      }
      text += '\n';
    });
    
    return text;
  }
}

/**
 * Main function demonstrating advanced Scrape API usage.
 */
async function main() {
  // Example websites to test with different configurations
  const testWebsites = [
    {
      url: 'https://example.com',
      name: 'example',
      renderHeavyJs: false,
      description: 'Simple static website',
      headers: {}
    },
    {
      url: 'https://httpbin.org/html',
      name: 'httpbin_html',
      renderHeavyJs: false,
      description: 'HTTP testing service',
      headers: {}
    },
    {
      url: 'https://httpbin.org/user-agent',
      name: 'httpbin_user_agent',
      renderHeavyJs: false,
      description: 'User agent testing with custom headers',
      headers: {
        'User-Agent': 'Custom Scraper Bot/1.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'
      }
    }
  ];

  console.log('🚀 Advanced Scrape API Example with scrapegraph-js SDK');
  console.log('='.repeat(70));

  // Check API key
  if (!API_KEY || API_KEY === 'your-api-key-here') {
    console.error('❌ Please set your SGAI_API_KEY environment variable');
    console.error('Example: export SGAI_API_KEY=your_api_key_here');
    process.exit(1);
  }

  console.log('✅ API key configured');
  console.log(`📊 Processing ${testWebsites.length} websites with advanced features\n`);

  try {
    // Initialize the processor
    const processor = new ScrapeProcessor(API_KEY);
    
    // Process websites with controlled concurrency
    const results = await processor.processWebsiteBatch(testWebsites, 2);
    
    // Generate comprehensive report
    await processor.generateReport(results);
    
    // Display final summary
    const successful = results.filter(r => r.success).length;
    const failed = results.filter(r => !r.success).length;
    
    console.log('\n🎯 FINAL SUMMARY');
    console.log('='.repeat(30));
    console.log(`✅ Successful: ${successful}`);
    console.log(`❌ Failed: ${failed}`);
    console.log(`📊 Success Rate: ${((successful / results.length) * 100).toFixed(1)}%`);
    console.log(`📁 Output saved to: ${OUTPUT_DIR}/`);
    
    if (failed > 0) {
      console.log('\n❌ Failed websites:');
      results.filter(r => !r.success).forEach(result => {
        console.log(`   - ${result.website}: ${result.error}`);
      });
    }
    
    console.log('\n✅ Advanced scrape example completed successfully');
    
  } catch (error) {
    console.error('💥 Fatal error:', error.message);
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
