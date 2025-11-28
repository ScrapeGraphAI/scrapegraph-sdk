/**
 * Health Check Example - Basic
 * 
 * This example demonstrates how to use the health check endpoint to monitor
 * the ScrapeGraphAI API service status. This is particularly useful for:
 * - Production monitoring and alerting
 * - Health checks in containerized environments (Kubernetes, Docker)
 * - Ensuring service availability before making API calls
 * - Integration with monitoring tools (Prometheus, Datadog, etc.)
 * 
 * The health check endpoint (/healthz) provides a quick way to verify that
 * the API service is operational and ready to handle requests.
 */

import { healthz } from 'scrapegraph-js';
import 'dotenv/config';

const apiKey = process.env.SGAI_APIKEY;

console.log('🏥 Checking ScrapeGraphAI API health status...');
console.log('-'.repeat(50));

try {
  // Perform health check
  const healthStatus = await healthz(apiKey);
  
  // Display results
  console.log('\n✅ Health Check Response:');
  console.log(`Status: ${healthStatus.status || 'unknown'}`);
  
  if (healthStatus.message) {
    console.log(`Message: ${healthStatus.message}`);
  }
  
  // Display any additional fields
  Object.keys(healthStatus).forEach(key => {
    if (key !== 'status' && key !== 'message') {
      console.log(`${key.charAt(0).toUpperCase() + key.slice(1)}: ${healthStatus[key]}`);
    }
  });
  
  console.log('\n' + '-'.repeat(50));
  console.log('✨ Health check completed successfully!');
  
  // Example: Use in a monitoring context
  if (healthStatus.status === 'healthy') {
    console.log('\n✓ Service is healthy and ready to accept requests');
    process.exit(0);
  } else {
    console.log('\n⚠️  Service may be experiencing issues');
    process.exit(1);
  }
  
} catch (error) {
  console.error('\n❌ Health check failed:', error.message);
  console.error('The service may be unavailable or experiencing issues');
  process.exit(2);
}

