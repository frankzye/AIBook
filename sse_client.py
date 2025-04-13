import requests
import json
import time

def sse_client(url):
    """
    Simple SSE client that connects to a server and processes server-sent events.
    
    Args:
        url (str): The URL of the SSE endpoint
    """
    try:
        # Make a GET request with stream=True to handle the SSE connection
        response = requests.get(url, stream=True, headers={
            'Accept': 'text/event-stream',
            'Cache-Control': 'no-cache',
            'Connection': 'keep-alive',
        })
        
        # Ensure the request was successful
        response.raise_for_status()
        
        # Process the event stream
        for line in response.iter_lines():
            if line:
                # Decode the line from bytes to string
                line = line.decode('utf-8')
                
                # Skip empty lines
                if not line.strip():
                    continue
                    
                # Process the event
                if line.startswith('data:'):
                    # Extract the data part
                    data = line[5:].strip()
                    try:
                        # Try to parse as JSON
                        event_data = json.loads(data)
                        print(f"Received event: {event_data}")
                    except json.JSONDecodeError:
                        # If not JSON, print as plain text
                        print(f"Received event: {data}")
                        
    except requests.exceptions.RequestException as e:
        print(f"Error connecting to SSE endpoint: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")

if __name__ == "__main__":
    # Example usage
    server_url = "http://localhost:8000/events"  # Replace with your SSE endpoint
    print(f"Connecting to SSE endpoint: {server_url}")
    sse_client(server_url) 