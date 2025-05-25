from mcp import ClientSession, types
from mcp.client.sse import sse_client
from contextlib import AsyncExitStack
from agents.mcp import MCPServer


url = "http://localhost:8000/sse"


class CustomMCPClient(MCPServer):
    def __init__(self):
        self.exit_stack = AsyncExitStack()
        pass
    
    def name(self) -> str:
        return "my mcp server"
         
    async def connect(self):
        stdio_transport = await self.exit_stack.enter_async_context(sse_client(url=url))
        self.stdio, self.write = stdio_transport
        self.session = await self.exit_stack.enter_async_context(ClientSession(self.stdio, self.write))
        await self.session.initialize()

    async def list_tools(self):
        return await self.session.list_tools()

    async def call_tool(self, tool_name, arguments):
        return await self.session.call_tool(tool_name, arguments=arguments)

    async def cleanup(self):
        await self.exit_stack.aclose()


async def test():
    client = CustomMCPClient()
    await client.connect_to_server()
    print(await client.get_tools())
    await client.close()

if __name__ == "__main__":
    import asyncio
    asyncio.run(test())
