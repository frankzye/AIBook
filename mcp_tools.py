import json
from sse_client import sse_client

def handle_mcp_tools_event(event_data):
    """
    Handle MCP tools events and display them in a formatted way.
    
    Args:
        event_data (dict): The event data received from the SSE stream
    """
    if isinstance(event_data, dict):
        if 'tools' in event_data:
            print("\nMCP Tools List:")
            print("-" * 50)
            for tool in event_data['tools']:
                print(f"Tool: {tool.get('name', 'N/A')}")
                print(f"Description: {tool.get('description', 'N/A')}")
                print(f"Parameters: {json.dumps(tool.get('parameters', {}), indent=2)}")
                print("-" * 50)
        else:
            print(f"Received event: {event_data}")

def main():
    # MCP tools SSE endpoint
    mcp_tools_url = "http://localhost:8000/mcp/tools"  # Replace with actual MCP tools endpoint
    
    print(f"Connecting to MCP tools SSE endpoint: {mcp_tools_url}")
    print("Waiting for tools list...")
    
    # Connect to the SSE endpoint and process events
    sse_client(mcp_tools_url)

if __name__ == "__main__":
    main() 