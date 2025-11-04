# Health Check Endpoint

## Overview

The health check endpoint (`/healthz`) has been added to both the Python and JavaScript SDKs to facilitate production monitoring and service health checks. This endpoint provides a quick way to verify that the ScrapeGraphAI API service is operational and ready to handle requests.

**Related:** [GitHub Issue #62](https://github.com/ScrapeGraphAI/scrapegraph-sdk/issues/62)

## Use Cases

- **Production Monitoring**: Regular health checks for alerting and monitoring systems
- **Container Health Checks**: Kubernetes liveness/readiness probes, Docker HEALTHCHECK
- **Load Balancer Health Checks**: Ensure service availability before routing traffic
- **Integration with Monitoring Tools**: Prometheus, Datadog, New Relic, etc.
- **Pre-request Validation**: Verify service is available before making API calls
- **Service Discovery**: Health status for service mesh and discovery systems

## Python SDK

### Installation

The health check endpoint is available in the latest version of the Python SDK:

```bash
pip install scrapegraph-py
```

### Usage

#### Synchronous Client

```python
from scrapegraph_py import Client

# Initialize client
client = Client.from_env()

# Check health status
health = client.healthz()
print(health)
# {'status': 'healthy', 'message': 'Service is operational'}

# Clean up
client.close()
```

#### Asynchronous Client

```python
import asyncio
from scrapegraph_py import AsyncClient

async def check_health():
    async with AsyncClient.from_env() as client:
        health = await client.healthz()
        print(health)
        # {'status': 'healthy', 'message': 'Service is operational'}

asyncio.run(check_health())
```

### API Reference

#### `Client.healthz()`

Check the health status of the ScrapeGraphAI API service.

**Returns:**
- `dict`: Health status information with at least the following fields:
  - `status` (str): Health status (e.g., 'healthy', 'unhealthy', 'degraded')
  - `message` (str): Human-readable status message

**Raises:**
- `APIError`: If the API returns an error response
- `ConnectionError`: If unable to connect to the API

#### `AsyncClient.healthz()`

Asynchronous version of the health check method.

**Returns:**
- `dict`: Health status information (same structure as sync version)

**Raises:**
- Same exceptions as synchronous version

### Examples

#### Basic Health Check with Error Handling

```python
from scrapegraph_py import Client

client = Client.from_env()

try:
    health = client.healthz()
    
    if health.get('status') == 'healthy':
        print("✓ Service is operational")
    else:
        print(f"⚠ Service status: {health.get('status')}")
        
except Exception as e:
    print(f"✗ Health check failed: {e}")
    
finally:
    client.close()
```

#### Integration with FastAPI

```python
from fastapi import FastAPI, HTTPException
from scrapegraph_py import AsyncClient

app = FastAPI()

@app.get("/health")
async def health_check():
    """Health check endpoint for load balancers"""
    try:
        async with AsyncClient.from_env() as client:
            health = await client.healthz()
            
            if health.get('status') == 'healthy':
                return {
                    "status": "healthy",
                    "scrape_graph_api": "operational"
                }
            else:
                raise HTTPException(
                    status_code=503,
                    detail="ScrapeGraphAI API is unhealthy"
                )
    except Exception as e:
        raise HTTPException(
            status_code=503,
            detail=f"Health check failed: {str(e)}"
        )
```

#### Kubernetes Liveness Probe Script

```python
#!/usr/bin/env python3
"""
Kubernetes liveness probe script for ScrapeGraphAI
Returns exit code 0 if healthy, 1 if unhealthy
"""
import sys
from scrapegraph_py import Client

def main():
    try:
        client = Client.from_env()
        health = client.healthz()
        client.close()
        
        if health.get('status') == 'healthy':
            sys.exit(0)
        else:
            sys.exit(1)
    except Exception:
        sys.exit(1)

if __name__ == "__main__":
    main()
```

### Mock Mode Support

The health check endpoint supports mock mode for testing:

```python
from scrapegraph_py import Client

# Enable mock mode
client = Client(
    api_key="sgai-00000000-0000-0000-0000-000000000000",
    mock=True
)

health = client.healthz()
print(health)
# {'status': 'healthy', 'message': 'Service is operational'}
```

**Custom Mock Responses:**

```python
from scrapegraph_py import Client

custom_response = {
    "status": "degraded",
    "message": "Custom mock response",
    "uptime": 12345
}

client = Client(
    api_key="sgai-00000000-0000-0000-0000-000000000000",
    mock=True,
    mock_responses={"/v1/healthz": custom_response}
)

health = client.healthz()
print(health)
# {'status': 'degraded', 'message': 'Custom mock response', 'uptime': 12345}
```

## JavaScript SDK

### Installation

The health check endpoint is available in the latest version of the JavaScript SDK:

```bash
npm install scrapegraph-sdk
```

### Usage

```javascript
import { healthz } from 'scrapegraph-js';

const apiKey = process.env.SGAI_APIKEY;

// Check health status
const health = await healthz(apiKey);
console.log(health);
// { status: 'healthy', message: 'Service is operational' }
```

### API Reference

#### `healthz(apiKey, options)`

Check the health status of the ScrapeGraphAI API service.

**Parameters:**
- `apiKey` (string): Your ScrapeGraph AI API key
- `options` (object, optional):
  - `mock` (boolean): Whether to use mock mode for this request

**Returns:**
- `Promise<Object>`: Health status information with at least:
  - `status` (string): Health status (e.g., 'healthy', 'unhealthy', 'degraded')
  - `message` (string): Human-readable status message

### Examples

#### Basic Health Check

```javascript
import { healthz } from 'scrapegraph-js';
import 'dotenv/config';

const apiKey = process.env.SGAI_APIKEY;

try {
  const health = await healthz(apiKey);
  
  if (health.status === 'healthy') {
    console.log('✓ Service is operational');
    process.exit(0);
  } else {
    console.log(`⚠ Service status: ${health.status}`);
    process.exit(1);
  }
} catch (error) {
  console.error('✗ Health check failed:', error.message);
  process.exit(2);
}
```

#### Integration with Express.js

```javascript
import express from 'express';
import { healthz } from 'scrapegraph-js';

const app = express();
const apiKey = process.env.SGAI_APIKEY;

// Health check endpoint for load balancers
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

app.listen(3000, () => {
  console.log('Server running on port 3000');
});
```

#### Health Check with Retry Logic

```javascript
import { healthz } from 'scrapegraph-js';

async function healthCheckWithRetry(apiKey, maxRetries = 3, initialDelay = 1000) {
  for (let attempt = 1; attempt <= maxRetries; attempt++) {
    try {
      console.log(`Attempt ${attempt}/${maxRetries}...`);
      const health = await healthz(apiKey);
      
      if (health.status === 'healthy') {
        console.log('✓ Service is healthy');
        return { success: true, attempts: attempt, data: health };
      }
      
      if (attempt < maxRetries) {
        const delay = initialDelay * Math.pow(2, attempt - 1);
        console.log(`Waiting ${delay}ms before retry...`);
        await new Promise(resolve => setTimeout(resolve, delay));
      }
    } catch (error) {
      console.log(`✗ Attempt ${attempt} failed:`, error.message);
      
      if (attempt < maxRetries) {
        const delay = initialDelay * Math.pow(2, attempt - 1);
        await new Promise(resolve => setTimeout(resolve, delay));
      }
    }
  }
  
  return { success: false, attempts: maxRetries };
}

const apiKey = process.env.SGAI_APIKEY;
const result = await healthCheckWithRetry(apiKey);
console.log(result);
```

### Mock Mode Support

```javascript
import { healthz, enableMock, disableMock } from 'scrapegraph-js';

// Enable mock mode
enableMock();

const health = await healthz('your-api-key', { mock: true });
console.log(health);
// { status: 'healthy', message: 'Service is operational' }

// Disable mock mode
disableMock();
```

**Custom Mock Responses:**

```javascript
import { healthz, initMockConfig, disableMock } from 'scrapegraph-js';

// Set custom mock response
initMockConfig({
  enabled: true,
  customResponses: {
    '/v1/healthz': {
      status: 'degraded',
      message: 'Custom mock status',
      uptime: 12345
    }
  }
});

const health = await healthz('your-api-key');
console.log(health);
// { status: 'degraded', message: 'Custom mock status', uptime: 12345 }

disableMock();
```

## Response Format

### Success Response

```json
{
  "status": "healthy",
  "message": "Service is operational"
}
```

### Possible Status Values

- `healthy`: Service is fully operational
- `degraded`: Service is operational but experiencing issues
- `unhealthy`: Service is not operational

Note: The actual status values and additional fields may vary based on the API implementation.

## Docker Health Check

### Dockerfile Example

```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

# Health check using the SDK
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD python -c "from scrapegraph_py import Client; import sys; c = Client.from_env(); h = c.healthz(); c.close(); sys.exit(0 if h.get('status') == 'healthy' else 1)"

CMD ["python", "app.py"]
```

### docker-compose.yml Example

```yaml
version: '3.8'
services:
  app:
    build: .
    environment:
      - SGAI_API_KEY=${SGAI_API_KEY}
    healthcheck:
      test: ["CMD", "python", "-c", "from scrapegraph_py import Client; import sys; c = Client.from_env(); h = c.healthz(); c.close(); sys.exit(0 if h.get('status') == 'healthy' else 1)"]
      interval: 30s
      timeout: 3s
      retries: 3
      start_period: 5s
```

## Kubernetes Deployment

### Liveness and Readiness Probes

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: scrapegraph-app
spec:
  replicas: 3
  template:
    spec:
      containers:
      - name: app
        image: your-app:latest
        env:
        - name: SGAI_API_KEY
          valueFrom:
            secretKeyRef:
              name: scrapegraph-secret
              key: api-key
        
        # Liveness probe - restarts container if unhealthy
        livenessProbe:
          exec:
            command:
            - python
            - -c
            - |
              from scrapegraph_py import Client
              import sys
              c = Client.from_env()
              h = c.healthz()
              c.close()
              sys.exit(0 if h.get('status') == 'healthy' else 1)
          initialDelaySeconds: 10
          periodSeconds: 30
          timeoutSeconds: 5
          failureThreshold: 3
        
        # Readiness probe - removes from service if not ready
        readinessProbe:
          exec:
            command:
            - python
            - -c
            - |
              from scrapegraph_py import Client
              import sys
              c = Client.from_env()
              h = c.healthz()
              c.close()
              sys.exit(0 if h.get('status') == 'healthy' else 1)
          initialDelaySeconds: 5
          periodSeconds: 10
          timeoutSeconds: 5
          failureThreshold: 2
```

## Examples Location

### Python Examples
- Basic: `scrapegraph-py/examples/utilities/healthz_example.py`
- Async: `scrapegraph-py/examples/utilities/healthz_async_example.py`

### JavaScript Examples
- Basic: `scrapegraph-js/examples/utilities/healthz_example.js`
- Advanced: `scrapegraph-js/examples/utilities/healthz_monitoring_example.js`

## Tests

### Python Tests
- `scrapegraph-py/tests/test_client.py` - Synchronous tests
- `scrapegraph-py/tests/test_async_client.py` - Asynchronous tests
- `scrapegraph-py/tests/test_healthz_mock.py` - Mock mode tests

### JavaScript Tests
- `scrapegraph-js/test/healthz_test.js` - Comprehensive test suite

## Running Tests

### Python

```bash
# Run all tests
cd scrapegraph-py
pytest tests/test_healthz_mock.py -v

# Run specific test
pytest tests/test_healthz_mock.py::test_healthz_mock_sync -v
```

### JavaScript

```bash
# Run health check tests
cd scrapegraph-js
node test/healthz_test.js
```

## Best Practices

1. **Implement Timeout**: Always set a reasonable timeout for health checks (3-5 seconds recommended)
2. **Use Appropriate Intervals**: Don't check too frequently; 30 seconds is a good default
3. **Handle Failures Gracefully**: Implement retry logic with exponential backoff
4. **Monitor and Alert**: Integrate with monitoring systems for automated alerting
5. **Test in Mock Mode**: Use mock mode in CI/CD pipelines to avoid API calls
6. **Log Health Check Results**: Keep records of health check outcomes for debugging

## Support

For issues, questions, or contributions, please visit:
- [GitHub Repository](https://github.com/ScrapeGraphAI/scrapegraph-sdk)
- [Issue #62](https://github.com/ScrapeGraphAI/scrapegraph-sdk/issues/62)
- [Documentation](https://docs.scrapegraphai.com)

