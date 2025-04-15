import os
import asyncio
import json
from clients.client import CustomMCPClient
from clients.github import GitHubMCPClient
from openai import AzureOpenAI
import openai
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


client = AzureOpenAI(
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),
    api_version="2024-05-01-preview",
    azure_endpoint="https://trish-m9gy5pk8-eastus2.cognitiveservices.azure.com",
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


async def check_tool(content: str, messages: list):
    try:
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
        print(ex)
        return False

    return False


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


def get_response(messages):
    completion = client.chat.completions.create(model="gpt-4.5-preview", messages=messages)
    return completion
