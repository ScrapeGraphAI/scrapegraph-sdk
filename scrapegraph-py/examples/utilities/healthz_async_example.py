"""
Health Check Example - Asynchronous

This example demonstrates how to use the health check endpoint asynchronously
to monitor the ScrapeGraphAI API service status. This is particularly useful for:
- Async production monitoring and alerting
- Health checks in async web frameworks (FastAPI, Sanic, aiohttp)
- Concurrent health monitoring of multiple services
- Integration with async monitoring tools

The health check endpoint (/healthz) provides a quick way to verify that
the API service is operational and ready to handle requests.
"""

import asyncio
from scrapegraph_py import AsyncClient


async def main():
    """
    Demonstrates the async health check functionality with the ScrapeGraphAI API.
    
    The healthz endpoint returns status information about the service,
    which can be used for monitoring and alerting purposes.
    """
    # Initialize the async client from environment variables
    # Ensure SGAI_API_KEY is set in your environment
    async with AsyncClient.from_env() as client:
        try:
            print("🏥 Checking ScrapeGraphAI API health status (async)...")
            print("-" * 50)
            
            # Perform health check
            health_status = await client.healthz()
            
            # Display results
            print("\n✅ Health Check Response:")
            print(f"Status: {health_status.get('status', 'unknown')}")
            
            if 'message' in health_status:
                print(f"Message: {health_status['message']}")
            
            # Additional fields that might be returned
            for key, value in health_status.items():
                if key not in ['status', 'message']:
                    print(f"{key.capitalize()}: {value}")
            
            print("\n" + "-" * 50)
            print("✨ Health check completed successfully!")
            
            # Example: Use in a monitoring context
            if health_status.get('status') == 'healthy':
                print("\n✓ Service is healthy and ready to accept requests")
            else:
                print("\n⚠️  Service may be experiencing issues")
                
        except Exception as e:
            print(f"\n❌ Health check failed: {e}")
            print("The service may be unavailable or experiencing issues")


async def monitoring_example():
    """
    Example of using health check in an async monitoring/alerting context.
    
    This function demonstrates how you might integrate the health check
    into an async monitoring system or scheduled health check script.
    """
    async with AsyncClient.from_env() as client:
        try:
            health_status = await client.healthz()
            
            # Simple health check logic
            is_healthy = health_status.get('status') == 'healthy'
            
            if is_healthy:
                print("✓ Health check passed")
                return 0  # Success exit code
            else:
                print("✗ Health check failed")
                return 1  # Failure exit code
                
        except Exception as e:
            print(f"✗ Health check error: {e}")
            return 2  # Error exit code


async def concurrent_health_checks():
    """
    Example of performing concurrent health checks.
    
    This demonstrates how you can efficiently check the health status
    multiple times or monitor multiple aspects concurrently.
    """
    async with AsyncClient.from_env() as client:
        print("🏥 Performing concurrent health checks...")
        
        # Perform multiple health checks concurrently
        results = await asyncio.gather(
            client.healthz(),
            client.healthz(),
            client.healthz(),
            return_exceptions=True
        )
        
        # Analyze results
        successful_checks = sum(
            1 for r in results 
            if isinstance(r, dict) and r.get('status') == 'healthy'
        )
        
        print(f"\n✓ Successful health checks: {successful_checks}/{len(results)}")
        
        if successful_checks == len(results):
            print("✓ All health checks passed - service is stable")
        elif successful_checks > 0:
            print("⚠️  Some health checks failed - service may be unstable")
        else:
            print("✗ All health checks failed - service is down")


async def fastapi_health_endpoint_example():
    """
    Example of how to integrate the health check into a FastAPI endpoint.
    
    This demonstrates a pattern for creating a health check endpoint
    in your own FastAPI application that checks the ScrapeGraphAI API.
    """
    # This is a demonstration of the pattern, not a runnable endpoint
    print("\n📝 FastAPI Integration Pattern:")
    print("-" * 50)
    print("""
from fastapi import FastAPI, HTTPException
from scrapegraph_py import AsyncClient

app = FastAPI()

@app.get("/health")
async def health_check():
    '''Health check endpoint that verifies ScrapeGraphAI API status'''
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
    """)
    print("-" * 50)


if __name__ == "__main__":
    # Run the main health check example
    asyncio.run(main())
    
    # Uncomment to run other examples
    # exit_code = asyncio.run(monitoring_example())
    # exit(exit_code)
    
    # asyncio.run(concurrent_health_checks())
    # asyncio.run(fastapi_health_endpoint_example())

