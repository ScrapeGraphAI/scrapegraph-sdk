#!/usr/bin/env node
/**
 * Example script demonstrating the Generate Schema API endpoint using ScrapeGraph JavaScript SDK.
 * 
 * This script shows how to:
 * 1. Generate a new JSON schema from a search query
 * 2. Modify an existing schema
 * 3. Handle different types of search queries
 * 4. Check the status of schema generation requests
 * 5. Poll for completion with progress tracking
 * 
 * Requirements:
 * - Node.js 16+
 * - scrapegraph-js package
 * - SGAI_API_KEY environment variable
 * 
 * Usage:
 *     SGAI_API_KEY=your_api_key node schema_generation_example.js
 */

import { generateSchema, getSchemaStatus, pollSchemaGeneration } from '../index.js';

class GenerateSchemaExample {
    constructor(apiKey, baseUrl = null) {
        this.apiKey = apiKey;
        this.baseUrl = baseUrl;
        
        if (!this.apiKey) {
            throw new Error(
                'API key must be provided. Set SGAI_API_KEY environment variable or pass it to the constructor.'
            );
        }
    }

    printSchemaResponse(response, title = 'Schema Generation Response') {
        console.log(`\n${'='.repeat(60)}`);
        console.log(` ${title}`);
        console.log(`${'='.repeat(60)}`);

        if (response.error) {
            console.log(`❌ Error: ${response.error}`);
            return;
        }

        console.log(`✅ Request ID: ${response.request_id || 'N/A'}`);
        console.log(`📊 Status: ${response.status || 'N/A'}`);
        console.log(`🔍 User Prompt: ${response.user_prompt || 'N/A'}`);
        console.log(`✨ Refined Prompt: ${response.refined_prompt || 'N/A'}`);

        if (response.generated_schema) {
            console.log(`\n📋 Generated Schema:`);
            console.log(JSON.stringify(response.generated_schema, null, 2));
        }
    }

    async runExamples() {
        console.log('🚀 Generate Schema API Examples using ScrapeGraph JavaScript SDK');
        console.log('='.repeat(60));

        // Example 1: Generate schema for e-commerce products
        console.log('\n1️⃣ Example: E-commerce Product Search');
        const ecommercePrompt = 'Find laptops with specifications like brand, processor, RAM, storage, and price';
        try {
            const response = await generateSchema(ecommercePrompt, null, {
                apiKey: this.apiKey,
                baseUrl: this.baseUrl
            });
            this.printSchemaResponse(response, 'E-commerce Products Schema');
        } catch (error) {
            console.log(`❌ Error in e-commerce example: ${error.message}`);
        }

        // Example 2: Generate schema for job listings
        console.log('\n2️⃣ Example: Job Listings Search');
        const jobPrompt = 'Search for software engineering jobs with company name, position, location, salary range, and requirements';
        try {
            const response = await generateSchema(jobPrompt, null, {
                apiKey: this.apiKey,
                baseUrl: this.baseUrl
            });
            this.printSchemaResponse(response, 'Job Listings Schema');
        } catch (error) {
            console.log(`❌ Error in job listings example: ${error.message}`);
        }

        // Example 3: Generate schema for news articles
        console.log('\n3️⃣ Example: News Articles Search');
        const newsPrompt = 'Find technology news articles with headline, author, publication date, category, and summary';
        try {
            const response = await generateSchema(newsPrompt, null, {
                apiKey: this.apiKey,
                baseUrl: this.baseUrl
            });
            this.printSchemaResponse(response, 'News Articles Schema');
        } catch (error) {
            console.log(`❌ Error in news articles example: ${error.message}`);
        }

        // Example 4: Modify existing schema
        console.log('\n4️⃣ Example: Modify Existing Schema');
        const existingSchema = {
            $defs: {
                ProductSchema: {
                    title: 'ProductSchema',
                    type: 'object',
                    properties: {
                        name: { title: 'Name', type: 'string' },
                        price: { title: 'Price', type: 'number' }
                    },
                    required: ['name', 'price']
                }
            },
            title: 'ProductList',
            type: 'object',
            properties: {
                products: {
                    title: 'Products',
                    type: 'array',
                    items: { $ref: '#/$defs/ProductSchema' }
                }
            },
            required: ['products']
        };

        const modificationPrompt = 'Add brand, category, and rating fields to the existing product schema';
        try {
            const response = await generateSchema(modificationPrompt, existingSchema, {
                apiKey: this.apiKey,
                baseUrl: this.baseUrl
            });
            this.printSchemaResponse(response, 'Modified Product Schema');
        } catch (error) {
            console.log(`❌ Error in schema modification example: ${error.message}`);
        }

        // Example 5: Complex nested schema
        console.log('\n5️⃣ Example: Complex Nested Schema');
        const complexPrompt = 'Create a schema for a company directory with departments, each containing employees with contact info and projects';
        try {
            const response = await generateSchema(complexPrompt, null, {
                apiKey: this.apiKey,
                baseUrl: this.baseUrl
            });
            this.printSchemaResponse(response, 'Company Directory Schema');
        } catch (error) {
            console.log(`❌ Error in complex schema example: ${error.message}`);
        }
    }

    async demonstrateStatusChecking() {
        console.log('\n🔄 Demonstrating Status Checking...');
        
        // Generate a simple schema first
        const prompt = 'Find restaurants with name, cuisine, rating, and address';
        try {
            const response = await generateSchema(prompt, null, {
                apiKey: this.apiKey,
                baseUrl: this.baseUrl
            });
            
            const requestId = response.request_id;
            
            if (requestId) {
                console.log(`📝 Generated schema request with ID: ${requestId}`);
                
                // Check the status
                console.log('🔍 Checking status...');
                const statusResponse = await getSchemaStatus(requestId, {
                    apiKey: this.apiKey,
                    baseUrl: this.baseUrl
                });
                this.printSchemaResponse(statusResponse, `Status Check for ${requestId}`);
            } else {
                console.log('⚠️  No request ID returned from schema generation');
            }
                
        } catch (error) {
            console.log(`❌ Error in status checking demonstration: ${error.message}`);
        }
    }

    async demonstratePolling() {
        console.log('\n🔄 Demonstrating Polling with Progress Tracking...');
        
        const prompt = 'Find movies with title, director, cast, rating, and release date';
        try {
            const response = await generateSchema(prompt, null, {
                apiKey: this.apiKey,
                baseUrl: this.baseUrl
            });
            
            const requestId = response.request_id;
            
            if (requestId) {
                console.log(`📝 Generated schema request with ID: ${requestId}`);
                console.log('🔄 Polling for completion with progress tracking...');
                
                const finalResult = await pollSchemaGeneration(requestId, {
                    apiKey: this.apiKey,
                    baseUrl: this.baseUrl,
                    maxAttempts: 15,
                    delay: 3000,
                    onProgress: ({ attempt, maxAttempts, status, response }) => {
                        if (status === 'checking') {
                            console.log(`🔍 Attempt ${attempt}/${maxAttempts}: Checking status...`);
                        } else {
                            console.log(`📊 Attempt ${attempt}/${maxAttempts}: Status = ${status}`);
                            if (response && response.refined_prompt) {
                                console.log(`   Refined prompt: ${response.refined_prompt}`);
                            }
                        }
                    }
                });
                
                console.log('✅ Polling completed successfully!');
                this.printSchemaResponse(finalResult, 'Final Result from Polling');
                
            } else {
                console.log('⚠️  No request ID returned from schema generation');
            }
                
        } catch (error) {
            console.log(`❌ Error in polling demonstration: ${error.message}`);
        }
    }

    async runConcurrentExamples() {
        console.log('\n🔄 Running Concurrent Examples...');

        const prompts = [
            'Find restaurants with name, cuisine, rating, and address',
            'Search for books with title, author, genre, and publication year',
            'Find movies with title, director, cast, rating, and release date'
        ];

        try {
            const tasks = prompts.map(prompt => 
                generateSchema(prompt, null, {
                    apiKey: this.apiKey,
                    baseUrl: this.baseUrl
                })
            );
            
            const results = await Promise.all(tasks);

            for (let i = 0; i < prompts.length; i++) {
                const prompt = prompts[i];
                const result = results[i];
                this.printSchemaResponse(result, `Concurrent Example ${i + 1}: ${prompt.substring(0, 30)}...`);
            }
                
        } catch (error) {
            console.log(`❌ Error in concurrent examples: ${error.message}`);
        }
    }
}

async function main() {
    // Check if API key is available
    const apiKey = process.env.SGAI_API_KEY;
    if (!apiKey) {
        console.log('Error: SGAI_API_KEY not found in environment variables');
        console.log('Please set your API key:');
        console.log('export SGAI_API_KEY=your_api_key_here');
        console.log('Or run: SGAI_API_KEY=your_api_key node schema_generation_example.js');
        return;
    }

    // Initialize the example class
    const example = new GenerateSchemaExample(apiKey);

    try {
        // Run synchronous examples
        await example.runExamples();

        // Demonstrate status checking
        await example.demonstrateStatusChecking();

        // Demonstrate polling with progress tracking
        await example.demonstratePolling();

        // Run concurrent examples
        await example.runConcurrentExamples();

    } catch (error) {
        console.log(`❌ Unexpected Error: ${error.message}`);
    }
}

// Run the examples if this file is executed directly
if (import.meta.url === `file://${process.argv[1]}`) {
    main().catch(console.error);
}
