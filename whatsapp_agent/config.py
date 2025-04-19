import os
from dotenv import load_dotenv

_ = load_dotenv()

class Settings:
    """
    Configuration settings for the WhatsApp agent.
    """

    DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")
    DEEPSEEK_BASE_URL = os.getenv("DEEPSEEK_BASE_URL", "https://api.novita.ai/v3/openai")
    DEEPSEEK_MODEL = "deepseek/deepseek-v3-0324"
    
    MCP_COMMAND = os.getenv("MCP_COMMAND", "uv")
    MCP_ARGS = [
        "--directory",
        os.getenv("MCP_DIRECTORY"),
        "run",
        "main.py"
    ]

    @classmethod
    def validate(cls):
        """
        Validates that essential settings are configured.
        """
        if not cls.DEEPSEEK_API_KEY:
            raise ValueError("DEEPSEEK_API_KEY must be set in the environment.")
            
settings = Settings()
settings.validate() # Validate settings on import