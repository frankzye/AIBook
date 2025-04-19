# server.py
from mcp.server.fastmcp import FastMCP
import uvicorn
import logging
from gnews import GNews

# Create an MCP server
mcp = FastMCP("Demo")
google_news = GNews(max_results=5)

# Add an addition tool
caches = {}


@mcp.tool()
def get_weather(city: str) -> int:
    """get the weather of the city"""
    return "cloudy"

# Add an addition tool


@mcp.tool()
def search_google(search: str):
    """search information in web, and return relative news in full text, you need to analysis and give summary to user"""
    if caches.get("str") is not None:
        logging.info("search with cache completed")
        return caches[str]

    news = google_news.get_news(search)
    caches[str] = news
    logging.info("search completed")
    return news


if __name__ == "__main__":
    uvicorn.run(mcp.sse_app(), host="0.0.0.0", port=8000, reload=False, log_level="debug")
