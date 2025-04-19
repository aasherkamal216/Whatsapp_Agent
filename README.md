# WhatsApp Agent

A Chainlit agent that interacts with WhatsApp using an MCP (Message Control Protocol) server.

## Prerequisites

*   Python 3.10+
*   An OpenAI API key (or compatible service like DeepSeek)
*   A running WhatsApp MCP server (see `whatsapp-mcp-server/`)
*   [uv](https://github.com/astral-sh/uv) (or pip)

## Installation

1.  Clone the repository:

    ```bash
    git clone <repository_url>
    cd whatsapp_agent
    ```

2.  Create a virtual environment:

    ```
    uv venv
    source .venv/bin/activate # On Mac
    .venv\Scripts\activate # On Windows
    ```

3.  Install dependencies using uv:

    ```bash
    uv sync
    ```

4.  Create a `.env` file based on `.env.example` and fill in your API key and other necessary configuration.

## Usage

1.  Start the WhatsApp MCP server (follow instructions in the `whatsapp-mcp-server/` directory).

2.  Run the Chainlit app:

    ```bash
    chainlit run whatsapp_agent/main.py
    ```
