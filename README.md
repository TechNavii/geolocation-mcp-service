# Geolocation MCP Service

A simple MCP (Model Context Protocol) server that provides geolocation information based on the server's public IP address.

## Features

- Returns current geolocation (city, region, country, latitude, longitude)
- Built with FastMCP
- Ready to deploy on Render
- Health check endpoint for monitoring
- Rate limiting and timeout configuration

## Deployment on Render

1. Fork or push this code to your GitHub repository
2. Connect your GitHub account to Render
3. Create a new Web Service on Render
4. Connect it to your repository
5. Render will automatically detect the `render.yaml` file and configure the deployment
6. The service will be deployed with Python runtime

## Environment Variables

Configure these in your Render dashboard or `render.yaml`:

- `LOG_LEVEL`: Logging level (default: INFO)
- `REQUEST_TIMEOUT`: API request timeout in seconds (default: 10)
- `RATE_LIMIT_DELAY`: Delay between API requests in seconds (default: 1.0)
- `GEOLOCATION_API_URL`: Geolocation API endpoint (default: http://ip-api.com/json/)
- `PORT`: Server port (default: 8000)
- `HOST`: Server host (default: 0.0.0.0)

## Usage

Once deployed, your MCP server will be available at your Render service URL. The server exposes:

- MCP tool: `get_current_geolocation()` - Returns geolocation information
- Health endpoint: `/health` - For service monitoring

## Local Development

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Run the server:
   ```bash
   python remote_mcp.py
   ```

The server will start on `http://localhost:8000` by default.

## Claude App Integration

Once deployed on Render, you can add your MCP service to Claude App by providing the service URL.