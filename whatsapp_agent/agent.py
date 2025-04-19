from openai import AsyncOpenAI

from agents import (
    Agent, 
    Runner, 
    OpenAIChatCompletionsModel,
    RunConfig,
    )
from agents.mcp import MCPServer

from config import settings

def get_model_config():
    # Initialize client with API key and base URL
    client = AsyncOpenAI(
        api_key=settings.DEEPSEEK_API_KEY,
        base_url=settings.DEEPSEEK_BASE_URL,
    )

    model = OpenAIChatCompletionsModel(model=settings.DEEPSEEK_MODEL, openai_client=client)

    return RunConfig(
        model=model,
        model_provider=client,
        tracing_disabled=True, 
    )

def create_whatsapp_agent(mcp_server: MCPServer):
    return Agent(
        name="Assistant",
        instructions="Use the tools to perform actions related to WhatsApp",
        mcp_servers=[mcp_server],
    )
