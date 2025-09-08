from typing import List, Any
from langchain_mcp_adapters.client import MultiServerMCPClient
from config import config

class CryptoMCPClient:
    """Wrapper for MultiServerMCPClient with crypto-specific configuration."""
    def __init__(self):
        self.client = None
        self._tools = None
    
    async def initialize(self) -> None:
        """Initialize the MCP client with crypto server configuration."""
        print("Initializing MCP client...")
        
        server_config = {
            "cryptoServer": {
                "command": "uv",
                "args": ["run", "python", "crypto_server.py"],
                "transport": "stdio",
                "cwd": str(config.crypto_server_dir)
            }
        }
        
        self.client = MultiServerMCPClient(server_config)
        print("MCP client initialized successfully")
    
    async def get_tools(self) -> List[Any]:
        """Get available tools from the MCP server."""
        if self.client is None:
            raise RuntimeError("MCP client not initialized. Call initialize() first.")
        
        if self._tools is None:
            print("Fetching tools from crypto server...")
            self._tools = await self.client.get_tools()
            print(f"Loaded {len(self._tools)} tools")
        
        return self._tools
    
    async def close(self) -> None:
        """Close the MCP client connection."""
        if self.client:
            print("MCP client connection closed")
            pass