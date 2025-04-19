import os
import asyncio
import json
from clients.client import CustomMCPClient
from clients.github import GitHubMCPClient
from openai import OpenAI
import logging
from dotenv import load_dotenv
load_dotenv()  # load environment variables from .env

# Load the English prompt file into a string


def load_english_prompt():
    prompt_path = os.path.join(os.path.dirname(__file__), 'english_prompt.md')
    with open(prompt_path, 'r', encoding='utf-8') as file:
        english_prompt = file.read()
    return english_prompt


# Load the prompt
english_prompt = load_english_prompt()

custom_client = None
github_client = None
github_tools = None
custom_tools = None


client = OpenAI(
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),
    base_url=os.getenv("AZURE_OPENAI_ENDPOINT"),
)


async def connect():
    global custom_client, github_client
    custom_client = CustomMCPClient()
    github_client = GitHubMCPClient()
    await custom_client.connect_to_server()
    await github_client.connect_to_server()


async def get_tools():
    global github_tools, custom_tools
    github_tools = await github_client.get_tools()
    custom_tools = await custom_client.get_tools()

    # Merge custom_tools into github_tools
    return str(github_tools.tools)+'\n'+str(custom_tools.tools)


# connect mcp servers, list the tools, and create the system prompt
async def connect_mcp():
    await connect()
    tools = await get_tools()
    prompt = english_prompt.replace('{{tool_lists}}', tools)

    messages = [
        {
            "role": "system",
            "content": prompt
        }
    ]
    return messages


# call the llm and send the messages
async def get_response(messages):
    completion = client.chat.completions.create(
        model="qwen-max",
        messages=messages,
        temperature=0)
    content = completion.choices[0].message.content
    
    api_call = None

    if await check_tool(content, messages):
        api_call = content
        logging.info("call mcp tool completed, and wait for the LLM response")
        content, _ = await get_response(messages)

    return content, api_call

# check the return of message if json format, and is mcp tool call, and yes,
# use mcp client execute the call and return the chat message, and append to chat messages
async def check_tool(content: str, messages: list):
    try:
        if content.startswith('```json'):
            content = content.replace('```json', '').replace('```', '')
        mcp_tool = json.loads(content)

        if mcp_tool.get("name") in [t.name for t in github_tools.tools]:
            res = await github_client.call_tool(mcp_tool.get("name"), mcp_tool.get("args"))
            messages.append({"role": "user", "content": "the response of api:" + str(res)})
            return True

        if mcp_tool.get("name") in [t.name for t in custom_tools.tools]:
            res = await custom_client.call_tool(mcp_tool.get("name"), mcp_tool.get("args"))
            messages.append({"role": "user", "content": "the response of api:" + str(res)})
            return True

    except Exception as ex:
        return False

    return False
