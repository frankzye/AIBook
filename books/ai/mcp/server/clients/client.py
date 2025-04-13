from mcp import ClientSession, types
from mcp.client.sse import sse_client
from contextlib import AsyncExitStack

url = "http://localhost:8000/sse"


class CustomMCPClient:
    def __init__(self):
        self.exit_stack = AsyncExitStack()
        pass

    async def connect_to_server(self):
        stdio_transport = await self.exit_stack.enter_async_context(sse_client(url=url))
        self.stdio, self.write = stdio_transport
        self.session = await self.exit_stack.enter_async_context(ClientSession(self.stdio, self.write))
        await self.session.initialize()

    async def get_tools(self):
        return await self.session.list_tools()

    async def call_tool(self, name, arguments):
        return await self.session.call_tool(name, arguments=arguments)

    async def close(self):
        await self.exit_stack.aclose()
