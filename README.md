# MCP Services: Geolocation & Tokyo Time

This repository contains two MCP (Model Context Protocol) services:
1. **Geolocation Service** - Provides location information based on server's public IP
2. **Tokyo Time Service** - Returns current date/time in Tokyo with Japanese formatting

## Services

### 1. Geolocation Service (remote_mcp.py)

Provides geolocation information based on the server's public IP address.

**Features:**
- Returns current geolocation (city, region, country, latitude, longitude)
- Built with FastMCP
- Rate limiting and timeout configuration
- Ready to deploy on Render

**MCP Tool:** `get_current_geolocation()`

### 2. Tokyo Time Service (time_mcp.py)

Returns the current date and time in Tokyo with Japanese date formatting.

**Features:**
- Tokyo timezone (JST: UTC+9)
- Japanese era support (令和/平成)
- Japanese date format: `令和6年5月17日 (金)`
- Japanese time format: `15時30分45秒`
- Includes weekday names in Japanese
- Returns both Japanese and ISO formats

**MCP Tool:** `get_time()`

## Deployment Options

### Deploy Geolocation Service

Use the default `render.yaml` file which is configured for the geolocation service:

```yaml
services:
  - type: web
    name: geolocation-mcp
    runtime: python
    buildCommand: pip install -r requirements.txt
    startCommand: python remote_mcp.py
```

### Deploy Tokyo Time Service

To deploy the Tokyo Time service instead, update `render.yaml`:

```yaml
services:
  - type: web
    name: tokyo-time-mcp
    runtime: python
    buildCommand: pip install -r requirements.txt
    startCommand: python time_mcp.py
```

Or create a separate `render-time.yaml` file with the Tokyo Time configuration.

## Environment Variables

Configure these in your Render dashboard or `render.yaml`:

- `LOG_LEVEL`: Logging level (default: INFO)
- `PORT`: Server port (default: 8000)
- `HOST`: Server host (default: 0.0.0.0)

### Geolocation-specific Variables
- `REQUEST_TIMEOUT`: API request timeout in seconds (default: 10)
- `RATE_LIMIT_DELAY`: Delay between API requests in seconds (default: 1.0)
- `GEOLOCATION_API_URL`: Geolocation API endpoint (default: http://ip-api.com/json/)

## Local Development

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Run either service:
   ```bash
   # For geolocation service
   python remote_mcp.py
   
   # For Tokyo time service
   python time_mcp.py
   ```

The server will start on `http://localhost:8000` by default.

## Switching Between Services

To switch which service is deployed on Render:

1. Update the `startCommand` in `render.yaml` to use the desired Python file
2. Commit and push the changes
3. Render will automatically redeploy with the new service

## Claude App Integration

Once deployed on Render, you can add your MCP service to Claude App by providing the service URL.

## Response Examples

### Geolocation Service Response
```json
{
  "city": "San Francisco",
  "region": "California",
  "country": "United States",
  "latitude": 37.7749,
  "longitude": -122.4194,
  "ip_address": "xxx.xxx.xxx.xxx"
}
```

### Tokyo Time Service Response
```json
{
  "japanese_date": "令和6年5月17日 (金)",
  "japanese_time": "15時30分45秒",
  "full_japanese": "令和6年5月17日 (金) 15時30分45秒",
  "iso_format": "2024-05-17T15:30:45+09:00",
  "timestamp": 1715928645.123456,
  "timezone": "JST (UTC+9)",
  "weekday": "金",
  "era": {
    "name": "令和",
    "year": 6
  }
}
```