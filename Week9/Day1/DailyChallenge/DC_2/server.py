import logging
from mcp.server.fastmcp import FastMCP

logging.basicConfig(level=logging.INFO)

mcp = FastMCP("WeatherDemo")

CITY_DATA = {
    "paris": {"temp_c": 21, "condition": "sunny"},
    "london": {"temp_c": 18, "condition": "cloudy"},
    "new york": {"temp_c": 24, "condition": "breezy"},
}

@mcp.tool()
def get_weather(city: str) -> dict:
    """Return simple weather info for a supported city."""
    key = city.strip().lower()
    data = CITY_DATA.get(key)
    if not data:
        return {"error": f"Unsupported city: {city}. Try one of: {', '.join(CITY_DATA)}"}
    logging.info("get_weather called for %s", key)
    return {"city": key, **data}

@mcp.resource("cities://list")
def list_cities() -> str:
    """Return supported cities as newline-separated text."""
    return "".join(sorted(CITY_DATA))

if __name__ == "__main__":
    mcp.run()
