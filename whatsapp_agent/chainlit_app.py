import chainlit as cl

from agents.mcp import MCPServerStdio
from agents import Agent, RunConfig, Runner

from openai.types.responses import ResponseTextDeltaEvent

from agent import create_whatsapp_agent, get_model_config
from config import settings

@cl.on_chat_start 
async def on_chat_start():

    # Initialize the MCPServer
    server = MCPServerStdio(
        name="WhatsApp MCP",
        params={
            "command": settings.MCP_COMMAND,
            "args": settings.MCP_ARGS
        },
    )
    try:
        await server.__aenter__()  # Manually enter the async context
    except Exception as e:
        cl.Message(content=f"Failed to start MCP Server: {e}").send()
        return

    agent = create_whatsapp_agent(server)
    config = get_model_config()

    # Store the initialized components in the user session
    cl.user_session.set("agent", agent) 
    cl.user_session.set("config", config)
    cl.user_session.set("server", server)

    # Initialize the chat history in the user session
    cl.user_session.set("history", [])

    await cl.Message(content="Welcome to the WhatsApp Agent!").send()


@cl.on_message  
async def handle_message(message: str):
    """
    Handles incoming messages from the user and runs the agent.
    """
    agent: Agent = cl.user_session.get("agent")
    config: RunConfig = cl.user_session.get("config")

    # Retrieve the chat history from the user session
    chat_history = cl.user_session.get("history")

    # Append the user's message to the chat history
    chat_history.append({"role": "user", "content": message.content})

    msg = cl.Message(content="")

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