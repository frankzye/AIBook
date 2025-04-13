# server.py
from starlette.applications import Starlette
from starlette.routing import Mount, Host
from mcp.server.fastmcp import FastMCP
import uvicorn

# Create an MCP server
mcp = FastMCP("Demo")


# Add an addition tool
@mcp.tool()
def get_weather(city: str) -> int:
    """get the weather of the city"""
    return "cloudy"


@mcp.prompt()
def review_code(code: str) -> str:
    """ review code """
    return f"Please review this code:\n\n{code}"

# Add a dynamic greeting resource


@mcp.resource("greeting://{name}")
def get_greeting(name: str) -> str:
    """Get a personalized greeting"""
    return f"Hello, {name}!"


# Mount the SSE server to the existing ASGI server
app = Starlette(
    routes=[
        Mount('/', app=mcp.sse_app()),
    ]
)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=False, log_level="debug")
