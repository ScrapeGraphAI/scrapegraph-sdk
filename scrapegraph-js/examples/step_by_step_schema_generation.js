#!/usr/bin/env node
/**
 * Step-by-step example for schema generation using ScrapeGraph JavaScript SDK.
 * 
 * This script demonstrates the basic workflow for schema generation:
 * 1. Initialize the client
 * 2. Generate a schema from a prompt
 * 3. Check the status of the request
 * 4. Retrieve the final result
 * 
 * Requirements:
 * - Node.js 16+
 * - scrapegraph-js package
 * - SGAI_API_KEY environment variable
 * 
 * Usage:
 *     SGAI_API_KEY=your_api_key node step_by_step_schema_generation.js
 */

import { generateSchema, getSchemaStatus } from '../index.js';

function printStep(stepNumber, title, description = '') {
    console.log(`\n${'='.repeat(60)}`);
    console.log(`STEP ${stepNumber}: ${title}`);
    console.log(`${'='.repeat(60)}`);
    if (description) {
        console.log(description);
    }
    console.log();
}

function printResponse(response, title = 'API Response') {
    console.log(`\n📋 ${title}`);
    console.log('-'.repeat(40));
    
    if (response.error) {
        console.log(`❌ Error: ${response.error}`);
        return;
    }

    for (const [key, value] of Object.entries(response)) {
        if (key === 'generated_schema' && value) {
            console.log(`🔧 ${key}:`);
            console.log(JSON.stringify(value, null, 2));
        } else {
            console.log(`🔧 ${key}: ${value}`);
        }
    }
}

async function main() {
    // Step 1: Check API key and initialize
    printStep(1, 'Initialize Client', 'Setting up the ScrapeGraph client with your API key');
    
    const apiKey = process.env.SGAI_API_KEY;
    if (!apiKey) {
        console.log('❌ Error: SGAI_API_KEY not found in environment variables');
        console.log('Please set your API key:');
        console.log('export SGAI_API_KEY=your_api_key_here');
        console.log('Or run: SGAI_API_KEY=your_api_key node step_by_step_schema_generation.js');
        return;
    }
    
    console.log('✅ API key found in environment variables');
    console.log('✅ Client ready to use');

    // Step 2: Define the schema generation request
    printStep(2, 'Define Request', 'Creating a prompt for schema generation');
    
    const userPrompt = 'Find laptops with specifications like brand, processor, RAM, storage, and price';
    console.log(`💭 User Prompt: ${userPrompt}`);
    
    // Step 3: Generate the schema
    printStep(3, 'Generate Schema', 'Sending the schema generation request to the API');
    
    try {
        const response = await generateSchema(userPrompt, null, { apiKey });
        console.log('✅ Schema generation request sent successfully');
        printResponse(response, 'Initial Response');
        
        // Extract the request ID for status checking
        const requestId = response.request_id;
        if (!requestId) {
            console.log('❌ No request ID returned from the API');
            return;
        }
            
    } catch (error) {
        console.log(`❌ Failed to generate schema: ${error.message}`);
        return;
    }

    // Step 4: Check the status (polling)
    printStep(4, 'Check Status', 'Polling the API to check the status of the request');
    
    const maxAttempts = 10;
    let attempt = 0;
    let requestId = null;
    
    // Get the request ID from the previous step
    try {
        const initialResponse = await generateSchema(userPrompt, null, { apiKey });
        requestId = initialResponse.request_id;
    } catch (error) {
        console.log(`❌ Error getting request ID: ${error.message}`);
        return;
    }
    
    while (attempt < maxAttempts) {
        attempt++;
        console.log(`🔍 Attempt ${attempt}/${maxAttempts}: Checking status...`);
        
        try {
            const statusResponse = await getSchemaStatus(requestId, { apiKey });
            const currentStatus = statusResponse.status || 'unknown';
            
            console.log(`📊 Current Status: ${currentStatus}`);
            
            if (currentStatus === 'completed') {
                console.log('✅ Schema generation completed successfully!');
                printResponse(statusResponse, 'Final Result');
                break;
            } else if (currentStatus === 'failed') {
                console.log('❌ Schema generation failed');
                printResponse(statusResponse, 'Error Response');
                break;
            } else if (currentStatus === 'pending' || currentStatus === 'processing') {
                console.log('⏳ Request is still being processed, waiting...');
                if (attempt < maxAttempts) {
                    await new Promise(resolve => setTimeout(resolve, 2000)); // Wait 2 seconds
                }
            } else {
                console.log(`⚠️  Unknown status: ${currentStatus}`);
                break;
            }
                
        } catch (error) {
            console.log(`❌ Error checking status: ${error.message}`);
            break;
        }
    }
    
    if (attempt >= maxAttempts) {
        console.log('⚠️  Maximum attempts reached. The request might still be processing.');
        console.log('You can check the status later using the request ID.');
    }

    // Step 5: Demonstrate schema modification
    printStep(5, 'Schema Modification', 'Demonstrating how to modify an existing schema');
    
    const existingSchema = {
        type: 'object',
        properties: {
            name: { type: 'string' },
            price: { type: 'number' }
        },
        required: ['name', 'price']
    };
    
    const modificationPrompt = 'Add brand and rating fields to the existing schema';
    console.log(`💭 Modification Prompt: ${modificationPrompt}`);
    console.log(`📋 Existing Schema: ${JSON.stringify(existingSchema, null, 2)}`);
    
    try {
        const modificationResponse = await generateSchema(modificationPrompt, existingSchema, { apiKey });
        console.log('✅ Schema modification request sent successfully');
        printResponse(modificationResponse, 'Modification Response');
        
    } catch (error) {
        console.log(`❌ Failed to modify schema: ${error.message}`);
    }

    // Step 6: Cleanup
    printStep(6, 'Cleanup', 'All operations completed successfully');
    
    console.log('✅ All operations completed successfully');
    console.log('✅ No cleanup needed for JavaScript SDK');

    console.log('\n🎉 Schema generation demonstration completed!');
    console.log(`📝 Request ID for reference: ${requestId}`);
}

// Run the main function
main().catch(console.error);
