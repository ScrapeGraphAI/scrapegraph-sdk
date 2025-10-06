/**
 * Enhanced SearchScraper Example
 *
 * This example demonstrates the SearchScraper API with configurable website limits.
 * Issue #144 enhancement allows users to search up to 20 websites (increased from the previous limit of 3)
 * with a dynamic credit pricing system.
 *
 * Key Features:
 * - Configurable website limits (3-20 websites)
 * - Dynamic credit pricing: 30 credits base + 10 credits per additional website
 * - Enhanced research depth and accuracy
 * - Backward compatibility with existing applications
 *
 * Cost Structure:
 * - Base cost: 30 credits for 3 websites (default)
 * - Additional websites: 10 credits each (e.g., 5 websites = 30 + 2*10 = 50 credits)
 * - Maximum websites: 20 (total cost: 30 + 17*10 = 200 credits)
 *
 * Requirements:
 * - Node.js
 * - scrapegraph-js package
 * - dotenv package
 * - A .env file with your SGAI_APIKEY
 *
 * Example .env file:
 * SGAI_APIKEY=your_api_key_here
 */

import { searchScraper } from 'scrapegraph-js';
import 'dotenv/config';

/**
 * Calculate the required credits for a SearchScraper request.
 * @param {number} numWebsites - Number of websites to scrape (3-20)
 * @returns {number} Total credits required
 */
function calculateCredits(numWebsites) {
    // Validate website count
    const validatedCount = Math.max(3, Math.min(20, numWebsites));

    // Calculate credits: 30 base + 10 per extra website
    if (validatedCount <= 3) {
        return 30;
    } else {
        const extraWebsites = validatedCount - 3;
        return 30 + (extraWebsites * 10);
    }
}

/**
 * Query the Enhanced SearchScraper API for search results.
 * @param {string} userPrompt - The search prompt string
 * @param {number} numResults - Number of websites to scrape (3-20). Default is 3.
 * @returns {Promise<Object>} The search results with metadata
 */
async function searchScraperQuery(userPrompt, numResults = 3) {
    const apiKey = process.env.SGAI_APIKEY;

    if (!apiKey) {
        throw new Error('SGAI_APIKEY not found in environment variables. Please create a .env file with: SGAI_APIKEY=your_api_key_here');
    }

    // Validate and calculate credits
    const validatedWebsites = Math.max(3, Math.min(20, numResults));
    const requiredCredits = calculateCredits(validatedWebsites);

    console.log(`🔍 Search Prompt: ${userPrompt}`);
    console.log(`🌐 Requested websites: ${numResults} → Validated: ${validatedWebsites}`);
    console.log(`💳 Required credits: ${requiredCredits}`);
    console.log('-'.repeat(60));

    const startTime = Date.now();

    try {
        const response = await searchScraper(apiKey, userPrompt, numResults);
        const executionTime = (Date.now() - startTime) / 1000;

        console.log(`⏱️  Execution time: ${executionTime.toFixed(2)} seconds`);

        // Extract result data
        const resultData = {
            result: response.result || '',
            references: response.reference_urls || [],
            metadata: {
                request_id: response.request_id,
                num_results: validatedWebsites,
                execution_time: executionTime,
                required_credits: requiredCredits,
            },
        };

        console.log(`✅ Found ${resultData.references.length} reference sources`);
        console.log(`📊 Credits used: ${requiredCredits}`);

        return resultData;

    } catch (error) {
        const executionTime = (Date.now() - startTime) / 1000;
        console.log(`⏱️  Execution time: ${executionTime.toFixed(2)} seconds`);
        console.log(`❌ Error: ${error.message}`);
        throw error;
    }
}

/**
 * Demonstrate the benefits of different website scaling options.
 */
function demonstrateScalingBenefits() {
    console.log('💰 SEARCHSCRAPER CREDIT SCALING');
    console.log('='.repeat(50));

    const scalingExamples = [
        [3, 'Standard Search (Default)'],
        [5, 'Enhanced Search (More Sources)'],
        [10, 'Comprehensive Search (Deep Research)'],
        [15, 'Extensive Search (Maximum Coverage)'],
        [20, 'Ultimate Search (Complete Coverage)'],
    ];

    scalingExamples.forEach(([websites, description]) => {
        const credits = calculateCredits(websites);
        const extraWebsites = Math.max(0, websites - 3);
        const efficiency = websites / credits;

        console.log(`🌐 ${websites.toString().padStart(2)} websites (${description})`);
        console.log(`   💳 ${credits.toString().padStart(3)} credits (base: 30 + ${extraWebsites} × 10)`);
        console.log(`   📊 Efficiency: ${efficiency.toFixed(3)} websites/credit`);
        console.log();
    });
}

/**
 * Run the same query with different website limits to show the benefit.
 */
async function runComparisonExample() {
    const query = 'Latest advancements in artificial intelligence 2024';

    console.log('🔬 COMPARISON: STANDARD vs ENHANCED SEARCH');
    console.log('='.repeat(60));
    console.log(`Query: ${query}`);
    console.log();

    // Test different configurations
    const configurations = [
        { websites: 3, description: 'Standard Search' },
        { websites: 7, description: 'Enhanced Search' },
    ];

    const results = {};

    for (const config of configurations) {
        const { websites, description } = config;

        console.log(`🚀 Running ${description} (${websites} websites)...`);
        try {
            const result = await searchScraperQuery(query, websites);
            results[websites] = result;
            console.log(`✅ ${description} completed successfully`);
            console.log(`   📄 Result length: ${result.result.length} characters`);
            console.log(`   🔗 References: ${result.references.length} sources`);
            console.log();
        } catch (error) {
            console.log(`❌ ${description} failed: ${error.message}`);
            console.log();
        }
    }

    // Show comparison summary
    const resultKeys = Object.keys(results);
    if (resultKeys.length > 1) {
        console.log('📊 COMPARISON SUMMARY');
        console.log('-'.repeat(40));
        resultKeys.forEach(websites => {
            const result = results[websites];
            const metadata = result.metadata;
            console.log(
                `🌐 ${websites} websites: ${result.references.length} sources, ` +
                `${metadata.required_credits} credits, ` +
                `${metadata.execution_time.toFixed(1)}s`
            );
        });
    }
}

/**
 * Run concurrent searches to demonstrate parallel processing
 */
async function runConcurrentExample() {
    console.log('🚀 CONCURRENT REQUESTS EXAMPLE');
    console.log('='.repeat(50));

    // Define multiple queries with different website limits
    const queries = [
        ['JavaScript best practices 2024', 3],
        ['React vs Vue comparison', 5],
        ['Node.js performance optimization', 4],
    ];

    console.log('🔄 Running concurrent searches...');
    const startTime = Date.now();

    try {
        // Create promises for concurrent execution
        const promises = queries.map(([query, numResults]) =>
            searchScraperQuery(query, numResults)
        );

        // Wait for all requests to complete
        const results = await Promise.allSettled(promises);
        const totalTime = (Date.now() - startTime) / 1000;

        console.log(`⏱️  Total concurrent execution time: ${totalTime.toFixed(2)} seconds`);
        console.log();

        const successfulResults = results.filter(r => r.status === 'fulfilled').map(r => r.value);
        const failedResults = results.filter(r => r.status === 'rejected');

        console.log(`✅ Successful requests: ${successfulResults.length}`);
        console.log(`❌ Failed requests: ${failedResults.length}`);

        if (successfulResults.length > 0) {
            const totalCredits = successfulResults.reduce((sum, r) => sum + r.metadata.required_credits, 0);
            const totalSources = successfulResults.reduce((sum, r) => sum + r.references.length, 0);
            console.log(`💳 Total credits used: ${totalCredits}`);
            console.log(`🔗 Total sources gathered: ${totalSources}`);
        }

        if (failedResults.length > 0) {
            console.log('\n❌ Failed requests:');
            failedResults.forEach((result, index) => {
                console.log(`   ${index + 1}. ${result.reason.message}`);
            });
        }

    } catch (error) {
        console.log(`❌ Concurrent execution failed: ${error.message}`);
    }

    console.log();
}

/**
 * Main function demonstrating enhanced SearchScraper features.
 */
async function main() {
    console.log('🚀 ENHANCED SEARCHSCRAPER DEMONSTRATION');
    console.log('🔗 Issue #144: SearchScraper Website Limit Enhancement');
    console.log('='.repeat(70));
    console.log();

    // Check API key
    const apiKey = process.env.SGAI_APIKEY;
    if (!apiKey) {
        console.log('❌ Error: SGAI_APIKEY not found in .env file');
        console.log('Please create a .env file with your API key:');
        console.log('SGAI_APIKEY=your_api_key_here');
        console.log();
        console.log('📖 Showing credit scaling demonstration without API calls...');
        console.log();
        demonstrateScalingBenefits();
        return;
    }

    try {
        // 1. Show credit scaling
        demonstrateScalingBenefits();

        // 2. Run basic example
        console.log('🎯 BASIC EXAMPLE');
        console.log('='.repeat(30));

        const userPrompt = 'What are the latest trends in machine learning?';
        const numResults = 5; // Enhanced search with 5 websites

        try {
            const results = await searchScraperQuery(userPrompt, numResults);

            console.log();
            console.log('📋 RESULTS SUMMARY:');
            console.log(`   🔍 Query: ${userPrompt}`);
            console.log(`   🌐 Websites scraped: ${results.metadata.num_results}`);
            console.log(`   💳 Credits used: ${results.metadata.required_credits}`);
            console.log(`   ⏱️  Execution time: ${results.metadata.execution_time.toFixed(1)}s`);
            console.log(`   🔗 Reference sources: ${results.references.length}`);
            console.log();

            // Show a portion of the result
            const resultText = results.result;
            if (resultText.length > 300) {
                console.log(`📄 Result preview: ${resultText.substring(0, 300)}...`);
            } else {
                console.log(`📄 Result: ${resultText}`);
            }
            console.log();

            // Show references
            console.log('🔗 REFERENCE SOURCES:');
            results.references.slice(0, 5).forEach((ref, i) => {
                console.log(`   ${i + 1}. ${ref}`);
            });
            if (results.references.length > 5) {
                console.log(`   ... and ${results.references.length - 5} more sources`);
            }
            console.log();

        } catch (error) {
            console.log(`❌ Error: ${error.message}`);
            console.log();
        }

        // 3. Run comparison example
        await runComparisonExample();

        // 4. Run concurrent example
        await runConcurrentExample();

        console.log('✨ Enhanced SearchScraper demonstration completed!');
        console.log();
        console.log('🎯 Key Enhancement Benefits:');
        console.log('   • Configurable website limits (3-20)');
        console.log('   • Transparent credit pricing');
        console.log('   • Better research depth and accuracy');
        console.log('   • Maintained backward compatibility');
        console.log('   • Enhanced data validation through multiple sources');
        console.log('   • Concurrent request support for better performance');

    } catch (error) {
        console.log(`❌ Unexpected error: ${error.message}`);
    }
}

// Run the demonstration
main().catch(console.error);
