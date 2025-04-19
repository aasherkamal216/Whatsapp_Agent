from openai import AsyncOpenAI
from agents import (
    Agent,  
    OpenAIChatCompletionsModel,
    RunConfig,
)
from agents.mcp import MCPServer

from .config import settings
from .prompts import WA_AGENT_PROMPT

class WhatsAppAgent:
    def __init__(self):
        self._api_key = settings.DEEPSEEK_API_KEY
        self.base_url = settings.DEEPSEEK_BASE_URL
        self.model_name = settings.DEEPSEEK_MODEL
        self.prompt = WA_AGENT_PROMPT

    def get_model_config(self):
        """
        Initializes the OpenAI client and model, returns a RunConfig object.
        """
        client = AsyncOpenAI(
            api_key=self._api_key,
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
            instructions=self.prompt,
            mcp_servers=[mcp_server],
        )
