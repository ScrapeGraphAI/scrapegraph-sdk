"""
Health Check Example - Synchronous

This example demonstrates how to use the health check endpoint to monitor
the ScrapeGraphAI API service status. This is particularly useful for:
- Production monitoring and alerting
- Health checks in containerized environments (Kubernetes, Docker)
- Ensuring service availability before making API calls
- Integration with monitoring tools (Prometheus, Datadog, etc.)

The health check endpoint (/healthz) provides a quick way to verify that
the API service is operational and ready to handle requests.
"""

from scrapegraph_py import Client

def main():
    """
    Demonstrates the health check functionality with the ScrapeGraphAI API.
    
    The healthz endpoint returns status information about the service,
    which can be used for monitoring and alerting purposes.
    """
    # Initialize the client from environment variables
    # Ensure SGAI_API_KEY is set in your environment
    client = Client.from_env()
    
    try:
        print("🏥 Checking ScrapeGraphAI API health status...")
        print("-" * 50)
        
        # Perform health check
        health_status = client.healthz()
        
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
    
    finally:
        # Clean up
        client.close()


def monitoring_example():
    """
    Example of using health check in a monitoring/alerting context.
    
    This function demonstrates how you might integrate the health check
    into a monitoring system or scheduled health check script.
    """
    client = Client.from_env()
    
    try:
        health_status = client.healthz()
        
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
    
    finally:
        client.close()


if __name__ == "__main__":
    # Run the main health check example
    main()
    
    # Uncomment to run monitoring example
    # exit_code = monitoring_example()
    # exit(exit_code)

