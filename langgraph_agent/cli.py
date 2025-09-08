from typing import Optional

class CryptoCLI:
    """Command line interface for the crypto agent."""
    def __init__(self):
        self.quit_commands = {'qq', 'quit', 'exit', 'q'}
    
    def print_welcome(self) -> None:
        """Print welcome message."""
        print("\n" + "="*50)
        print("🚀 CRYPTO AGENT")
        print("="*50)
    
    def print_goodbye(self) -> None:
        """Print goodbye message."""
        print("\n Goodbye! Thanks for using Crypto Agent!")
    
    def get_user_input(self) -> Optional[str]:
        """Get user input with proper handling."""
        try:
            user_input = input("\n💬 Crypto Query (or 'qq' to quit): ").strip()
            
            if user_input.lower() in self.quit_commands:
                return None
            
            if not user_input:
                print("Please enter a query or 'qq' to quit.")
                return self.get_user_input()
            
            return user_input
            
        except KeyboardInterrupt:
            print("\n\nInterrupted by user. Exiting...")
            return None
        except EOFError:
            print("\n\nEnd of input. Exiting...")
            return None
    
    def print_agent_response(self, response: str) -> None:
        """Print formatted agent response."""
        print(f"\n🤖 {response}")
    
    def print_error(self, error: str) -> None:
        """Print formatted error message."""
        print(f"\n❌ Error: {error}")
    
    def print_status(self, status: str) -> None:
        """Print status message."""
        print(f"{status}")
    
    def confirm_exit(self) -> bool:
        """Confirm exit with user."""
        try:
            confirm = input("\n❓ Are you sure you want to exit? (y/N): ").strip().lower()
            return confirm in {'y', 'yes'}
        except (KeyboardInterrupt, EOFError):
            return True