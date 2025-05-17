# remote_mcp.py

from fastmcp import FastMCP
import os
import requests
import logging
from typing import Optional, Dict, Any
import time

# Configure logging
logging.basicConfig(
    level=os.environ.get("LOG_LEVEL", "INFO"),
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Environment configuration
REQUEST_TIMEOUT = int(os.environ.get("REQUEST_TIMEOUT", "10"))
API_URL = os.environ.get("GEOLOCATION_API_URL", "http://ip-api.com/json/")
RATE_LIMIT_DELAY = float(os.environ.get("RATE_LIMIT_DELAY", "1.0"))

mcp = FastMCP(
    name="Geolocation Service",
    instructions="When you are asked for the current geolocation, call get_current_geolocation()."
)

# Track last request time for rate limiting
last_request_time = 0


@mcp.tool()
def get_current_geolocation() -> Dict[str, Any]:
    """
    Returns the current geolocation information based on the server's public IP address.
    Information includes city, region, country, latitude, and longitude.
    
    Returns:
        A dictionary containing geolocation data or an error message.
    """
    global last_request_time
    
    # Basic rate limiting
    current_time = time.time()
    time_since_last_request = current_time - last_request_time
    if time_since_last_request < RATE_LIMIT_DELAY:
        time.sleep(RATE_LIMIT_DELAY - time_since_last_request)
    
    last_request_time = time.time()
    
    try:
        logger.info("Fetching geolocation data")
        response = requests.get(API_URL, timeout=REQUEST_TIMEOUT)
        response.raise_for_status()
        data = response.json()
        
        if data.get("status") == "success":
            result = {
                "city": data.get("city"),
                "region": data.get("regionName"),
                "country": data.get("country"),
                "latitude": data.get("lat"),
                "longitude": data.get("lon"),
                "ip_address": data.get("query")
            }
            logger.info(f"Successfully retrieved geolocation for {result.get('ip_address')}")
            return result
        else:
            error_msg = data.get("message", "Unknown error from API")
            logger.error(f"API returned error: {error_msg}")
            return {"error": "Failed to retrieve geolocation data", "details": error_msg}
            
    except requests.exceptions.Timeout:
        logger.error("Request timeout occurred")
        return {"error": "Request timed out", "details": f"Timeout after {REQUEST_TIMEOUT} seconds"}
    except requests.exceptions.ConnectionError:
        logger.error("Connection error occurred")
        return {"error": "Connection error", "details": "Failed to connect to geolocation service"}
    except requests.exceptions.HTTPError as e:
        logger.error(f"HTTP error occurred: {e}")
        return {"error": "HTTP error", "details": str(e)}
    except requests.exceptions.RequestException as e:
        logger.error(f"Request exception occurred: {e}")
        return {"error": "Failed to connect to geolocation service", "details": str(e)}
    except Exception as e:
        logger.error(f"Unexpected error occurred: {e}")
        return {"error": "An unexpected error occurred", "details": str(e)}


@mcp.get("/health")
async def health_check() -> Dict[str, str]:
    """Health check endpoint for monitoring"""
    return {"status": "healthy", "service": "geolocation-mcp"}


if __name__ == "__main__":
    import asyncio
    port = int(os.environ.get("PORT", 8000))
    host = os.environ.get("HOST", "0.0.0.0")
    log_level = os.environ.get("LOG_LEVEL", "info").lower()
    
    logger.info(f"Starting MCP server on {host}:{port}")
    
    asyncio.run(
        mcp.run_sse_async(
            host=host,
            port=port,
            log_level=log_level
        )
    )