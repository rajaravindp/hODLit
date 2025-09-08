import os
from pathlib import Path
from dotenv import load_dotenv

class Config:
    """Application configuration class."""
    
    def __init__(self):
        load_dotenv()
        self._validate_environment()
    
    @property
    def aws_access_key(self) -> str:
        """Get AWS access key from environment."""
        return os.getenv("AWS_ACCESS_KEY")
    
    @property
    def aws_secret_key(self) -> str:
        """Get AWS secret key from environment."""
        return os.getenv("AWS_SECRET_ACCESS_KEY")
    
    @property
    def aws_region(self) -> str:
        """Get AWS region."""
        return os.getenv("AWS_REGION", "us-east-1")
    
    @property
    def model_id(self) -> str:
        """Get the model ID for Bedrock."""
        return os.getenv("MODEL_ID", "amazon.nova-lite-v1:0")
    
    @property
    def base_dir(self) -> Path:
        """Get the base directory path."""
        return Path(__file__).parent.parent.absolute()
    
    @property
    def crypto_server_dir(self) -> Path:
        """Get the crypto server directory path."""
        return self.base_dir / "server"
    
    def _validate_environment(self):
        """Validate that required environment variables are set."""
        required_vars = ["AWS_ACCESS_KEY", "AWS_SECRET_ACCESS_KEY"]
        missing_vars = [var for var in required_vars if not os.getenv(var)]
        
        if missing_vars:
            raise ValueError(f"Missing required environment variables: {', '.join(missing_vars)}")

config = Config()