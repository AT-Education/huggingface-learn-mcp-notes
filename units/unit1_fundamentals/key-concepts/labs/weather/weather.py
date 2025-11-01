import httpx
from typing import Any
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("weather_service")

# region Constants

NWS_API_BASE = "https://api.weather.gov"
USER_AGENT = "weather-app/1.0"

# endregion


# region helper functions

async def make_nws_request(url: str) -> dict[str, Any] | None:
    '''Make an asynchronous request to the NWS API and return the JSON response.'''
    headers = {
        "User-Agent": USER_AGENT,
        "Accept": "application/geo+json"
        }
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, headers=headers)
            if response.status_code == 200:
                return response.json()
        except httpx.RequestError as e:
            print(f"An error occurred while requesting {e.request.url!r}.")
            return None
        
def format_alert(feature: dict) -> str:
    """Format an alert feature into a readable string."""
    props = feature["properties"]
    return f"""
Event: {props.get('event', 'Unknown')}
Area: {props.get('areaDesc', 'Unknown')}
Severity: {props.get('severity', 'Unknown')}
Description: {props.get('description', 'No description available')}
Instructions: {props.get('instruction', 'No specific instructions provided')}
"""

# endregion     


# region MCP Tools

@mcp.tool()
async def get_alerts(state: str) -> str:
    """
    Fetch and return weather alerts for a US State.
    
    Args:
        state (str): The two-letter abbreviation of the US State (e.g., 'CA' for California).    
    """
    alerts_url = f"{NWS_API_BASE}/alerts/active/area/{state}"
    data = await make_nws_request(alerts_url)
    
    if not data or "features" not in data:
        return "Unable to fetch alerts or no alerts found."

    if not data["features"]:
        return "No active alerts for this state."

    alerts = [format_alert(feature) for feature in data["features"]]
    return "\n---\n".join(alerts)


@mcp.tool()
async def get_forecast(latitude: float, longitude: float) -> str:
    """
    Fetch and return the weather forecast for a given latitude and longitude.
    
    Args:
        latitude (float): The latitude of the location.
        longitude (float): The longitude of the location.
    """
    points_url = f"{NWS_API_BASE}/points/{latitude},{longitude}"
    points_data = await make_nws_request(points_url)
    
    if not points_data or "properties" not in points_data:
        return "Unable to fetch forecast data."

    forecast_url = points_data["properties"].get("forecast")
    if not forecast_url:
        return "Forecast URL not found."

    forecast_data = await make_nws_request(forecast_url)
    if not forecast_data or "properties" not in forecast_data:
        return "Unable to fetch forecast data."

    periods = forecast_data["properties"].get("periods", [])
    if not periods:
        return "No forecast data available."

    forecasts = []
    for period in periods[:5]:  # Get forecast for the next 5 periods
        forecast = f"""
            {period['name']}: 
            Temperature: {period['temperature']} {period['temperatureUnit']}
            Wind: {period['windSpeed']} {period['windDirection']}
            Short Forecast: {period['shortForecast']}
            Forecast Details: {period['detailedForecast']}
        """
        forecasts.append(forecast.strip())
        
    return "\n---\n".join(forecasts)

# endregion     

# region MCP Server Start

def main():
    mcp.run(transport="stdio")

if __name__ == "__main__":
    main()
    
# endregion   