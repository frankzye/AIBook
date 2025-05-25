import os
import asyncio
import json
from clients.client import CustomMCPClient
from openai import OpenAI
import logging
from dotenv import load_dotenv
from pydantic import BaseModel
from typing import List
from agents import Agent, Runner
from openai import AsyncOpenAI
from agents import set_default_openai_client
from agents.mcp import MCPServerSse, MCPServerStdio
from agents.models import _openai_shared

load_dotenv()  # load environment variables from .env


custom_client = AsyncOpenAI(
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),
    base_url=os.getenv("AZURE_OPENAI_ENDPOINT"),
)

_openai_shared.set_use_responses_by_default(False)
set_default_openai_client(custom_client, use_for_tracing=False)


agent = None


async def connect_mcp():
    server1 = MCPServerSse(
        name="SSE Python Server",
        client_session_timeout_seconds=300,
        params={
            "url": "http://localhost:8000/sse",
        },
    )
    server2 = MCPServerStdio(name="github",
                             params={
                                 "command": "podman",
                                 "args": ['run', '-i', '--rm', '-e', 'GITHUB_PERSONAL_ACCESS_TOKEN', 'ghcr.io/github/github-mcp-server'],
                                 "env": {
                                     "GITHUB_PERSONAL_ACCESS_TOKEN": os.environ.get("GITHUB_TOKEN")
                                 }
                             })
    await server1.connect()
    await server2.connect()
    global agent
    agent = Agent(name="Assistant", instructions="You are a helpful assistant", model="qwen-max", mcp_servers=[
        server1, server2
    ])


# call the llm and send the messages
async def get_response(history, messages):
    from openai.types.responses import ResponseTextDeltaEvent

    try:
        for h in history:
            if h["role"] == "assistant":
                h["content"] = [{
                    "type": "output_text",
                    "text": h["content"],
                }]
            h["type"] = "message"

        api_call = None
        result = Runner.run_streamed(agent, history + messages)
        content = {
            "type": "message",
            "role": "assistant",
            "content": ""
        }

        async for event in result.stream_events():
            if event.type == "raw_response_event" and isinstance(event.data, ResponseTextDeltaEvent):
                content["content"] += event.data.delta
                yield content, api_call
            elif event.type == "run_item_stream_event":
                if event.item.type == "tool_call_item":
                    api_call = event.item.raw_item.name + event.item.raw_item.arguments
                    yield content, api_call

    except Exception as ex:
        raise ex
