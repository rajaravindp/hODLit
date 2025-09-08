import asyncio
import sys
from config import config
from mcp_client import CryptoMCPClient
from agent import CryptoAgent
from cli import CryptoCLI

class CryptoApp:
    """Main application class that orchestrates all components."""
    def __init__(self):
        self.mcp_client = CryptoMCPClient()
        self.agent = CryptoAgent()
        self.cli = CryptoCLI()
    
    async def initialize(self) -> bool:
        """Initialize all application components."""
        try:
            await self.mcp_client.initialize()
            tools = await self.mcp_client.get_tools()
            self.agent.create_agent(tools)
            
            return True
            
        except Exception as e:
            self.cli.print_error(f"Failed to initialize application: {str(e)}")
            return False
    
    async def run_greeting(self) -> None:
        """Display initial greeting from the agent."""
        try:
            greeting = await self.agent.get_greeting()
            self.cli.print_agent_response(greeting)
        except Exception as e:
            self.cli.print_error(f"Failed to get greeting: {str(e)}")
            self.cli.print_status("Agent is ready for queries despite greeting error.")
    
    async def run_chat_loop(self) -> None:
        """Run the main chat loop."""
        while True:
            user_input = self.cli.get_user_input()
            if user_input is None:
                break
            
            try:
                response = await self.agent.invoke(user_input)
                self.cli.print_agent_response(response)
                
            except Exception as e:
                self.cli.print_error(f"Failed to process query: {str(e)}")
                self.cli.print_status("Please try again with a different query.")
    
    async def cleanup(self) -> None:
        """Cleanup application resources."""
        try:
            await self.mcp_client.close()
        except Exception as e:
            self.cli.print_error(f"Error during cleanup: {str(e)}")
    
    async def run(self) -> int:
        """Main application entry point."""
        self.cli.print_welcome()
        
        if not await self.initialize():
            return 1
        
        try:
            await self.run_greeting()
            await self.run_chat_loop()
            
        except Exception as e:
            self.cli.print_error(f"Unexpected error: {str(e)}")
            return 1
        
        finally:
            await self.cleanup()
            self.cli.print_goodbye()
        
        return 0

async def main() -> None:
    """Application entry point."""
    app = CryptoApp()
    exit_code = await app.run()
    sys.exit(exit_code)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n\n Application interrupted by user. Goodbye!")
        sys.exit(0)
    except Exception as e:
        print(f"\n Fatal error: {str(e)}")
        sys.exit(1)