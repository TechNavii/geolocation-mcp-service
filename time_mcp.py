# tokyo_time_mcp.py

from fastmcp import FastMCP
import os
import logging
from datetime import datetime, timezone, timedelta
from typing import Dict, Any

# Configure logging
logging.basicConfig(
    level=os.environ.get("LOG_LEVEL", "INFO"),
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

mcp = FastMCP(
    name="Tokyo Time Service",
    instructions="When you are asked for the current time, call get_time()."
)


@mcp.tool()
def get_time() -> Dict[str, Any]:
    """
    Returns the current date and time in Tokyo with Japanese date formatting.
    Information includes Japanese era, date, time, and weekday.
    
    Returns:
        A dictionary containing Tokyo time data in Japanese format.
    """
    try:
        # Create Tokyo timezone (JST: UTC+9)
        tokyo_tz = timezone(timedelta(hours=9))
        
        # Get current time in Tokyo
        tokyo_time = datetime.now(tokyo_tz)
        
        # Format date in Japanese style
        # Year (年), Month (月), Day (日)
        year = tokyo_time.year
        month = tokyo_time.month
        day = tokyo_time.day
        hour = tokyo_time.hour
        minute = tokyo_time.minute
        second = tokyo_time.second
        
        # Days of the week in Japanese
        weekdays_jp = ['月', '火', '水', '木', '金', '土', '日']
        weekday = weekdays_jp[tokyo_time.weekday()]
        
        # Japanese era (令和: Reiwa era started May 1, 2019)
        reiwa_start = datetime(2019, 5, 1, tzinfo=tokyo_tz)
        if tokyo_time >= reiwa_start:
            era_name = "令和"
            era_year = year - 2019 + 1
        else:
            era_name = "平成"
            era_year = year - 1989 + 1
        
        # Format the date in Japanese style
        japanese_date = f"{era_name}{era_year}年{month}月{day}日 ({weekday})"
        japanese_time = f"{hour}時{minute}分{second}秒"
        
        # Also provide standard ISO format
        iso_format = tokyo_time.isoformat()
        
        # Create response
        result = {
            "japanese_date": japanese_date,
            "japanese_time": japanese_time,
            "full_japanese": f"{japanese_date} {japanese_time}",
            "iso_format": iso_format,
            "timestamp": tokyo_time.timestamp(),
            "timezone": "JST (UTC+9)",
            "weekday": weekday,
            "era": {
                "name": era_name,
                "year": era_year
            }
        }
        
        logger.info(f"Successfully retrieved time: {result['full_japanese']}")
        return result
        
    except Exception as e:
        logger.error(f"Error getting time: {e}")
        return {"error": "Failed to get time", "details": str(e)}


# Health checks are handled by the MCP server itself


if __name__ == "__main__":
    import asyncio
    port = int(os.environ.get("PORT", 8001))
    host = os.environ.get("HOST", "0.0.0.0")
    log_level = os.environ.get("LOG_LEVEL", "info").lower()
    
    logger.info(f"Starting Tokyo Time MCP server on {host}:{port}")
    
    # Run the FastMCP server with SSE transport
    asyncio.run(
        mcp.run_sse_async(
            host="0.0.0.0",  # Changed from 127.0.0.1 to allow external connections
            port=port,
            log_level="debug"
        )
    )
