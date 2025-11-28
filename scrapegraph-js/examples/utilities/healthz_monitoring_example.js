/**
 * Health Check Example - Advanced Monitoring
 * 
 * This example demonstrates advanced patterns for using the health check endpoint
 * in production monitoring scenarios, including:
 * - Periodic health checks
 * - Integration with Express.js
 * - Retry logic with exponential backoff
 * - Health check aggregation
 */

import { healthz } from 'scrapegraph-js';
import 'dotenv/config';

const apiKey = process.env.SGAI_APIKEY;

/**
 * Simple monitoring function that checks health status
 */
async function simpleHealthCheck() {
  console.log('🏥 Performing health check...');
  
  try {
    const health = await healthz(apiKey);
    
    if (health.status === 'healthy') {
      console.log('✓ Health check passed');
      return { success: true, data: health };
    } else {
      console.log('✗ Health check failed - service unhealthy');
      return { success: false, data: health };
    }
  } catch (error) {
    console.log('✗ Health check error:', error.message);
    return { success: false, error: error.message };
  }
}

/**
 * Health check with retry logic and exponential backoff
 */
async function healthCheckWithRetry(maxRetries = 3, initialDelay = 1000) {
  console.log('\n🔄 Health check with retry logic...');
  
  for (let attempt = 1; attempt <= maxRetries; attempt++) {
    try {
      console.log(`Attempt ${attempt}/${maxRetries}...`);
      const health = await healthz(apiKey);
      
      if (health.status === 'healthy') {
        console.log('✓ Service is healthy');
        return { success: true, attempts: attempt, data: health };
      }
      
      console.log(`⚠️  Service returned: ${health.status}`);
      
      if (attempt < maxRetries) {
        const delay = initialDelay * Math.pow(2, attempt - 1);
        console.log(`Waiting ${delay}ms before retry...`);
        await new Promise(resolve => setTimeout(resolve, delay));
      }
    } catch (error) {
      console.log(`✗ Attempt ${attempt} failed:`, error.message);
      
      if (attempt < maxRetries) {
        const delay = initialDelay * Math.pow(2, attempt - 1);
        console.log(`Waiting ${delay}ms before retry...`);
        await new Promise(resolve => setTimeout(resolve, delay));
      }
    }
  }
  
  return { success: false, attempts: maxRetries };
}

/**
 * Periodic health check that runs at intervals
 */
async function periodicHealthCheck(intervalMs = 30000) {
  console.log(`\n⏰ Starting periodic health checks every ${intervalMs}ms...`);
  console.log('Press Ctrl+C to stop\n');
  
  const checkHealth = async () => {
    const timestamp = new Date().toISOString();
    console.log(`[${timestamp}] Running health check...`);
    
    try {
      const health = await healthz(apiKey);
      
      if (health.status === 'healthy') {
        console.log(`[${timestamp}] ✓ Service is healthy\n`);
      } else {
        console.log(`[${timestamp}] ⚠️  Service status: ${health.status}\n`);
      }
    } catch (error) {
      console.log(`[${timestamp}] ✗ Health check failed: ${error.message}\n`);
    }
  };
  
  // Run initial check
  await checkHealth();
  
  // Schedule periodic checks
  setInterval(checkHealth, intervalMs);
}

/**
 * Example Express.js health endpoint
 * 
 * This demonstrates how to integrate the health check into an Express.js
 * application for Kubernetes liveness/readiness probes or load balancer checks.
 */
function expressHealthEndpointExample() {
  console.log('\n📝 Express.js Integration Pattern:');
  console.log('-'.repeat(50));
  console.log(`
import express from 'express';
import { healthz } from 'scrapegraph-js';

const app = express();
const apiKey = process.env.SGAI_APIKEY;

// Health check endpoint for load balancers/Kubernetes
app.get('/health', async (req, res) => {
  try {
    const health = await healthz(apiKey);
    
    if (health.status === 'healthy') {
      res.status(200).json({
        status: 'healthy',
        timestamp: new Date().toISOString(),
        scrapeGraphApi: 'operational'
      });
    } else {
      res.status(503).json({
        status: 'unhealthy',
        timestamp: new Date().toISOString(),
        scrapeGraphApi: health.status
      });
    }
  } catch (error) {
    res.status(503).json({
      status: 'error',
      timestamp: new Date().toISOString(),
      error: error.message
    });
  }
});

// Liveness probe - checks if the app is running
app.get('/healthz/live', (req, res) => {
  res.status(200).json({ status: 'alive' });
});

// Readiness probe - checks if the app can handle requests
app.get('/healthz/ready', async (req, res) => {
  try {
    const health = await healthz(apiKey);
    
    if (health.status === 'healthy') {
      res.status(200).json({ status: 'ready' });
    } else {
      res.status(503).json({ status: 'not ready' });
    }
  } catch (error) {
    res.status(503).json({ status: 'not ready', error: error.message });
  }
});

app.listen(3000, () => {
  console.log('Server running on port 3000');
});
  `);
  console.log('-'.repeat(50));
}

/**
 * Main function - demonstrates different monitoring patterns
 */
async function main() {
  console.log('🏥 ScrapeGraphAI Health Check - Advanced Monitoring Examples');
  console.log('='.repeat(60));
  
  // 1. Simple health check
  await simpleHealthCheck();
  
  // 2. Health check with retry logic
  await healthCheckWithRetry(3, 1000);
  
  // 3. Show Express.js integration example
  expressHealthEndpointExample();
  
  // Uncomment to run periodic health checks
  // await periodicHealthCheck(30000); // Check every 30 seconds
}

// Run the examples
main().catch(console.error);

