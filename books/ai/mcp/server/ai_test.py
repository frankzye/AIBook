import os
import asyncio
import json
from clients.client import CustomMCPClient
from clients.github import GitHubMCPClient
from openai import OpenAI
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
    # 若没有配置环境变量，请用百炼API Key将下行替换为：api_key="sk-xxx",
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
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
    # 初始化一个 messages 数组
    messages = [
        {
            "role": "system",
            "content": prompt
        }
    ]
    return messages


async def run():
    await connect()
    tools = await get_tools()
    prompt = english_prompt.replace('{{tool_lists}}', tools)

    # 初始化一个 messages 数组
    messages = [
        {
            "role": "system",
            "content": prompt
        }
    ]

    messages.append(
        {
            "role": "user",
            "content": "user question: list the name of my most starts repo in github"
        }
    )

    assistant_output = get_response(messages).choices[0].message.content
    # 将大模型的回复信息添加到messages列表中
    messages.append({"role": "assistant", "content": assistant_output})
    print(f"模型输出：{assistant_output}")

    # execute if there is mcp tool call
    await check_tool(assistant_output, messages)

    assistant_output = get_response(messages).choices[0].message.content
    print(f"模型输出：{assistant_output}")

    # try ask another
    messages.append(
        {
            "role": "user",
            "content": "user question: check if good to go to the city guangzhou"
        }
    )
    assistant_output = get_response(messages).choices[0].message.content
    print(f"模型输出：{assistant_output}")

    await check_tool(assistant_output, messages)
    assistant_output = get_response(messages).choices[0].message.content
    print(f"模型输出：{assistant_output}")

    await github_client.close()
    await custom_client.close()


def get_response(messages):

    # 模型列表：https://help.aliyun.com/zh/model-studio/getting-started/models
    completion = client.chat.completions.create(model="qwen-plus", messages=messages)
    return completion
