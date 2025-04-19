from openai import AsyncOpenAI
from agents import (
    Agent, 
    Runner, 
    OpenAIChatCompletionsModel,
    RunConfig,
)
from agents.mcp import MCPServer

from .config import settings

class WhatsAppAgent:
    def __init__(self):
        self.api_key = settings.DEEPSEEK_API_KEY
        self.base_url = settings.DEEPSEEK_BASE_URL
        self.model_name = settings.DEEPSEEK_MODEL

    def get_model_config(self):
        """
        Initializes the OpenAI client and model, returns a RunConfig object.
        """
        client = AsyncOpenAI(
            api_key=self.api_key,
            base_url=self.base_url,
        )
        model = OpenAIChatCompletionsModel(model=self.model_name, openai_client=client)
        return RunConfig(
            model=model,
            model_provider=client,
            tracing_disabled=True,
        )

    def create_whatsapp_agent(self, mcp_server: MCPServer):
        """
        Creates and returns an Agent instance for WhatsApp actions.
        """
        return Agent(
            name="Assistant",
            instructions="Use the tools to perform actions related to WhatsApp",
            mcp_servers=[mcp_server],
        )
