import gradio as gr
import asyncio
from ai_test import connect_mcp, get_response, check_tool


initialed = False
messages = None

MCP_ENABLED = False


async def load():
    global initialed, messages
    if initialed is not True:
        initialed = True
        if MCP_ENABLED:
            messages = await connect_mcp()


async def chat(message, history, v):

    if len(history) == 0 and messages != None:
        for content in messages:
            history.append(content)

    chat_messages = []
    for content in history:
        chat_messages.append(content)
    chat_messages.append({
        "role": "user",
        "content": "user question: "+message
    })

    md = None
    api_request_content = get_response(chat_messages).choices[0].message.content
    if await check_tool(api_request_content, chat_messages):
        assistant_output = get_response(chat_messages).choices[0].message.content
        md = gr.Markdown(value=(v+"   \n"+api_request_content))
    else:
        assistant_output = api_request_content

    return assistant_output, md


with gr.Blocks() as demo:
    demo.load(load, inputs=[])
    code = gr.Markdown(render=False)
    with gr.Row():
        with gr.Column():
            gr.ChatInterface(
                chat,
                additional_inputs=[code],
                additional_outputs=[code],
                type="messages"
            )


demo.launch()
