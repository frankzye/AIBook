import gradio as gr
import logging
from agent import get_response, connect_mcp


initialed = False
messages = None
tool_messages = None

# config logging and provide console output
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler()
    ]
)


async def load():
    global initialed, tool_messages, messages
    await connect_mcp()


async def chat(message, history, v):

    if len(history) == 0 and messages != None:
        for content in messages:
            history.append(content)

    chat_messages = []
    chat_messages.append({
        "role": "user",
        "content": message
    })

    md = None

    async for assistant_output, api_call in get_response(history, chat_messages):
        if api_call and v is not None:
            md = gr.Markdown(value=(v+"   \n"+api_call))
        yield assistant_output, md


with gr.Blocks() as demo:
    def on_check(f):
        global messages
        if f:
            messages = tool_messages
        else:
            messages = None
    demo.load(load, inputs=[])

    code = gr.Markdown(render=False)
    check = gr.Checkbox(render=False, label="use mcp", value=True)
    with gr.Row():
        check.render()
    with gr.Row():
        with gr.Column():
            gr.ChatInterface(
                chat,
                additional_inputs=[code],
                additional_outputs=[code],
                type="messages"
            )
    check.change(on_check, inputs=[check])

demo.launch()
