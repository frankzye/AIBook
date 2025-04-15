## prequirements
1. install python libraries
```
pip install -r requirements.txt
```

## python sdk
use mcp python sdk to create mcp server and client
https://github.com/modelcontextprotocol/python-sdk


## create custom MCP server

### tools
1. search in google with keyword
2. provide the weather of the city 

## create github mcp server
connect github with personal token , and provide the tools like search the repo and check the issues...  

### tools 
https://github.com/github/github-mcp-server

## create github mcp client and custom mcp server client
1. create connection(from sse or stdio)
2. create session 
3. list tools
4. call tools

## create chat agent
1. connect the mcp clients
2. create openai chat client
3. load the predifine prompt, train the LLM how to use and call the MCP tools
3. handle chat response and call mcp tool

## create chat ui application
1. use gradio app create a simple chat
2. provide the option enable mcp
3. import agent and handle LLM chat response
