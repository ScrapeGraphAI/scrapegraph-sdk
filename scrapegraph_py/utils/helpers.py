from urllib.parse import urlparse
import socket
import requests
from scrapegraph_py.logger import sgai_logger as logger

def validate_website_url(url: str) -> None:
    """Validate if website URL is reachable."""
    logger.info(f"🔍 Validating website URL: {url}")
    
    try:
        # Validate URL format
        parsed = urlparse(url)
        if not all([parsed.scheme, parsed.netloc]):
            logger.error(f"❌ Invalid URL format: {url}")
            raise ValueError("Invalid URL format")
        logger.info("✅ URL format is valid")
            
        # Try to resolve domain
        logger.info(f"🔍 Checking domain accessibility: {parsed.netloc}")
        socket.gethostbyname(parsed.netloc)
        
        # Try to make a HEAD request to verify the website responds
        logger.info(f"🔍 Verifying website response...")
        response = requests.head(url, timeout=5, allow_redirects=True)
        response.raise_for_status()
        logger.info(f"✅ Website is accessible and responding")
        
    except socket.gaierror:
        error_msg = f"Could not resolve domain: {url}"
        logger.error(f"❌ {error_msg}")
        raise ValueError(error_msg)
    except requests.exceptions.RequestException as e:
        error_msg = f"Website not reachable: {url} - {str(e)}"
        logger.error(f"❌ {error_msg}")
        raise ValueError(error_msg)
    except Exception as e:
        error_msg = f"Invalid URL: {str(e)}"
        logger.error(f"❌ {error_msg}")
        raise ValueError(error_msg) 