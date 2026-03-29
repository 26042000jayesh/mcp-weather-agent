from mcp.server.fastmcp import FastMCP
import httpx
from pydantic import BaseModel, Field

# Initialize our MCP Server
mcp = FastMCP("WeatherService")

# --- DATA VALIDATION ---
class WeatherQuery(BaseModel):
    latitude: float = Field(
        ...,
        description= "Latitude of the location in decimal degrees (e.g., 12.9716)"
    )
    longitude: float = Field(
        ...,
        description="Longitude of the location in decimal degrees (e.g., 77.5946)"
    )

# --- THE ACTION LAYER (TOOL) ---
@mcp.tool()
async def get_current_weather(query: WeatherQuery) -> str:
    """Fetches real-time temperature and wind speed for a given location."""
    url = ("https://api.open-meteo.com/v1/forecast"
        f"?latitude={query.latitude}&longitude={query.longitude}"
        "&current=temperature_2m,wind_speed_10m")
    
    # Context manager ensures network sockets are cleanly closed under load
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        response.raise_for_status()
        data = response.json()

    current = data.get("current", {})
    temp = current.get("temperature_2m")
    wind = current.get("wind_speed_10m")
    
    # Return concise data to preserve LLM token context limits
    return f"Current temperature is {temp}°C and wind speed is {wind} km/h."

# --- THE TEMPLATE LAYER (PROMPT) ---
@mcp.prompt()
def analyze_fleet_weather(latitude: float, longitude: float) -> str:
    """Provides instructions to the LLM for analyzing weather impact on EV operations."""
    return f"""
You are an EV Fleet Operations Manager.

Analyze the weather conditions for the location:
Latitude: {latitude}
Longitude: {longitude}

First, use the get_current_weather tool to fetch the live data.

Based on the retrieved data, generate a report structured around:

1. Expected Battery Drain:
- Consider how temperature impacts EV battery performance.
- Note that colder temperatures increase battery drain.

2. Safe Riding Conditions:
- Evaluate wind speed and its impact on rider safety.
- Highlight any risks due to high wind speeds.

Provide a clear and concise operational summary.
"""

if __name__ == "__main__":
    # Binds to stdio for JSON-RPC communication
    mcp.run()