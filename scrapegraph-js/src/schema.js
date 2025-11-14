/**
 * Schema generation functionality for ScrapeGraph JavaScript SDK
 */

import handleError from './utils/handleError.js';

/**
 * Generate a JSON schema from a user prompt
 * 
 * @param {string} userPrompt - The user's search query to be refined into a schema
 * @param {Object} existingSchema - Optional existing JSON schema to modify/extend
 * @param {Object} options - Additional options for the request
 * @param {string} options.apiKey - API key for authentication
 * @param {string} options.baseUrl - Base URL for the API (optional, defaults to production)
 * @returns {Promise<Object>} API response containing the generated schema
 */
export async function generateSchema(userPrompt, existingSchema = null, options = {}) {
    try {
        const { apiKey, baseUrl = 'https://api.scrapegraph.ai' } = options;
        
        if (!apiKey) {
            throw new Error('API key is required. Please provide it in the options or set SGAI_API_KEY environment variable.');
        }

        if (!userPrompt || typeof userPrompt !== 'string' || userPrompt.trim() === '') {
            throw new Error('userPrompt is required and must be a non-empty string');
        }

        const payload = {
            user_prompt: userPrompt.trim()
        };

        if (existingSchema) {
            if (typeof existingSchema !== 'object' || existingSchema === null) {
                throw new Error('existingSchema must be a valid object');
            }
            payload.existing_schema = existingSchema;
        }

        const response = await fetch(`${baseUrl}/v1/generate_schema`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'SGAI-APIKEY': apiKey
            },
            body: JSON.stringify(payload)
        });

        if (!response.ok) {
            const errorData = await response.json().catch(() => ({}));
            throw new Error(
                `HTTP ${response.status}: ${errorData.error || response.statusText}`
            );
        }

        const result = await response.json();
        return result;

    } catch (error) {
        return handleError(error, 'generateSchema');
    }
}

/**
 * Get the status of a schema generation request
 * 
 * @param {string} requestId - The request ID returned from generateSchema
 * @param {Object} options - Additional options for the request
 * @param {string} options.apiKey - API key for authentication
 * @param {string} options.baseUrl - Base URL for the API (optional, defaults to production)
 * @returns {Promise<Object>} Current status and results of the schema generation
 */
export async function getSchemaStatus(requestId, options = {}) {
    try {
        const { apiKey, baseUrl = 'https://api.scrapegraph.ai' } = options;
        
        if (!apiKey) {
            throw new Error('API key is required. Please provide it in the options or set SGAI_APIKEY environment variable.');
        }

        if (!requestId || typeof requestId !== 'string' || requestId.trim() === '') {
            throw new Error('requestId is required and must be a non-empty string');
        }

        // Validate UUID format (basic check)
        const uuidRegex = /^[0-9a-f]{8}-[0-9a-f]{4}-[1-5][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$/i;
        if (!uuidRegex.test(requestId.trim())) {
            throw new Error('requestId must be a valid UUID format');
        }

        const response = await fetch(`${baseUrl}/v1/generate_schema/${requestId.trim()}`, {
            method: 'GET',
            headers: {
                'SGAI-APIKEY': apiKey
            }
        });

        if (!response.ok) {
            const errorData = await response.json().catch(() => ({}));
            throw new Error(
                `HTTP ${response.status}: ${errorData.error || response.statusText}`
            );
        }

        const result = await response.json();
        return result;

    } catch (error) {
        return handleError(error, 'getSchemaStatus');
    }
}

/**
 * Poll for schema generation completion
 * 
 * @param {string} requestId - The request ID returned from generateSchema
 * @param {Object} options - Additional options for polling
 * @param {string} options.apiKey - API key for authentication
 * @param {string} options.baseUrl - Base URL for the API (optional, defaults to production)
 * @param {number} options.maxAttempts - Maximum number of polling attempts (default: 30)
 * @param {number} options.delay - Delay between attempts in milliseconds (default: 2000)
 * @param {Function} options.onProgress - Callback function called on each status check
 * @returns {Promise<Object>} Final result when schema generation is complete
 */
export async function pollSchemaGeneration(requestId, options = {}) {
    try {
        const { 
            apiKey, 
            baseUrl = 'https://api.scrapegraph.ai',
            maxAttempts = 30,
            delay = 2000,
            onProgress = null
        } = options;

        if (!apiKey) {
            throw new Error('API key is required. Please provide it in the options or set SGAI_APIKEY environment variable.');
        }

        if (!requestId || typeof requestId !== 'string' || requestId.trim() === '') {
            throw new Error('requestId is required and must be a non-empty string');
        }

        let attempt = 0;
        
        while (attempt < maxAttempts) {
            attempt++;
            
            if (onProgress) {
                onProgress({ attempt, maxAttempts, status: 'checking' });
            }

            const statusResponse = await getSchemaStatus(requestId, { apiKey, baseUrl });
            
            if (statusResponse.error) {
                throw new Error(`Schema generation failed: ${statusResponse.error}`);
            }

            const currentStatus = statusResponse.status;
            
            if (onProgress) {
                onProgress({ attempt, maxAttempts, status: currentStatus, response: statusResponse });
            }

            if (currentStatus === 'completed') {
                return statusResponse;
            } else if (currentStatus === 'failed') {
                throw new Error(`Schema generation failed with status: ${currentStatus}`);
            } else if (currentStatus === 'pending' || currentStatus === 'processing') {
                if (attempt < maxAttempts) {
                    await new Promise(resolve => setTimeout(resolve, delay));
                }
            } else {
                console.warn(`Unknown status: ${currentStatus}`);
                if (attempt < maxAttempts) {
                    await new Promise(resolve => setTimeout(resolve, delay));
                }
            }
        }

        throw new Error(`Schema generation did not complete within ${maxAttempts} attempts. Last status: ${statusResponse?.status || 'unknown'}`);

    } catch (error) {
        return handleError(error, 'pollSchemaGeneration');
    }
}
