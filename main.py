import asyncio
import os
from dotenv import load_dotenv
import shutil
from typing import cast

from openai import AsyncOpenAI
from openai.types.responses import ResponseTextDeltaEvent

from agents import (
    Agent, 
    Runner, 
    OpenAIChatCompletionsModel,
    RunConfig,
    )

from agents.mcp import MCPServerStdio

import chainlit as cl 

# Load environment variables from .env file
_ = load_dotenv()

# Initialize OpenAI client with API key and base URL
client = AsyncOpenAI(
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    base_url="https://api.novita.ai/v3/openai",
)

@cl.on_chat_start 
async def main():
    """
    Main function to initialize and run the agent within Chainlit.
    """
    # Create the model instance
    model = OpenAIChatCompletionsModel(model="deepseek/deepseek-v3-0324", openai_client=client)

    # Configure the run settings for the agent
    config = RunConfig(
        model=model,
        model_provider=client,
        tracing_disabled=True, 
    )

    # Initialize the MCPServer
    server = MCPServerStdio(
        name="WhatsApp MCP",
        params={
            "command": "C:\\Users\\Aasher Kamal\\.local\\bin\\uv.exe",
            "args": [
                "--directory",
                "D:\\Projects and Learning\\Whatsapp_Agents\\whatsapp-mcp\\whatsapp-mcp-server",
                "run",
                "main.py"
            ]
        },
    )
    await server.__aenter__()  # Manually enter the async context

    agent = Agent(
        name="Assistant",
        instructions="Use the tools to perform actions related to WhatsApp",
        mcp_servers=[server],
    )

    cl.user_session.set("agent", agent)  # Store the agent in the user session
    cl.user_session.set("config", config)  # Store the config in the user session
    cl.user_session.set("server", server)  # Store the server in the user session

    # Initialize the chat history in the user session
    cl.user_session.set("history", [])

    await cl.Message(content="Welcome to the WhatsApp Agent!").send()  # Initial message

@cl.on_message  
async def handle_message(message: str):
    """
    Handles incoming messages from the user and runs the agent.
    """
    agent = cl.user_session.get("agent")  # Retrieve the agent from the user session
    config = cl.user_session.get("config")  # Retrieve the config from the user session

    # Retrieve the chat history from the user session
    chat_history = cl.user_session.get("history")

    # Append the user's message to the chat history
    chat_history.append({"role": "user", "content": message.content})

    msg = cl.Message(content="")

    # Get Config and Agent from user session
    agent: Agent = cast(Agent, cl.user_session.get("agent"))
    config: RunConfig = cast(RunConfig, cl.user_session.get("config"))

    try:
        # Stream agent's response
        result = Runner.run_streamed(
            starting_agent=agent,
            input=chat_history,
            run_config=config
        )

        full_response = "" 

        # Stream the message in app
        async for event in result.stream_events():
            if event.type == "raw_response_event" and isinstance(event.data, ResponseTextDeltaEvent):
                if token := event.data.delta or "":
                    await msg.stream_token(token)
        
                full_response += token 
        await msg.send()

        # Update chat history
        chat_history.append({"role": "assistant", "content": full_response})

        cl.user_session.set("history", chat_history)

    except Exception as e:
        await cl.Message(content=f"An error occurred: {e}").send()  # Send error message

@cl.on_chat_end
async def on_chat_end():
    """
    Cleanup resources when the chat ends.
    """
    server = cl.user_session.get("server")
    if server:
        await server.__aexit__(None, None, None)  # Manually exit the async context

if __name__ == "__main__":
    # Check if uv is installed
    if not shutil.which("uv"):
        raise RuntimeError(
            "uv is not installed."
        )