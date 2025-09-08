import os
from dotenv import load_dotenv
from google.adk.agents import LlmAgent
from google.adk.tools.mcp_tool import MCPToolset, StdioConnectionParams

load_dotenv()
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CRYPTO_SERVER_DIR = os.path.join(BASE_DIR, "server")

SYS_INSTRUCTIONS = (
    "You are a helpful assistant that provides cryptocurrency data using the CoinGecko API. "
    "Use the provided tools to fetch data as needed. "
    "If you don't know the answer, say 'I don't know'. "
    "Always provide accurate and up-to-date information. "
    "Do not attempt to answer unrelated questions or use tools for other purposes."
)

def create_agent() -> LlmAgent:
    """Constructs the ADK cryptocurrency agent."""
    return LlmAgent(
        model="gemini-2.5-flash",
        name="crypto_agent",
        description="An agent that can help with cryptocurrency conversions",
        instruction=SYS_INSTRUCTIONS,
        tools=[
            MCPToolset(
                connection_params=StdioConnectionParams(
                    server_params={
                        "command": "uv",
                        "args": ["run", "python", "crypto_server.py"],
                        "cwd": CRYPTO_SERVER_DIR
                    }
                )
            )
        ],
    )

root_agent = create_agent()
