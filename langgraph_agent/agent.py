from typing import List, Any
from langchain_aws import ChatBedrockConverse
from langgraph.prebuilt import create_react_agent
from langgraph.checkpoint.memory import InMemorySaver
from langchain_core.messages import HumanMessage
from config import config

class CryptoAgent:
    """Crypto agent wrapper for LangGraph ReAct agent."""
    def __init__(self):
        self.model = None
        self.agent = None
        self._initialize_model()
    
    def _initialize_model(self) -> None:
        """Initialize the ChatBedrockConverse model."""
        print("Initializing language model...")
        
        self.model = ChatBedrockConverse(
            model_id=config.model_id,
            aws_access_key_id=config.aws_access_key,
            aws_secret_access_key=config.aws_secret_key,
            region_name=config.aws_region
        )
        
        print(f"Model initialized: {config.model_id}")
    
    def create_agent(self, tools: List[Any]) -> None:
        """Create the ReAct agent with the provided tools."""
        print("Creating ReAct agent...")
        
        checkpointer = InMemorySaver()
        
        self.agent = create_react_agent(
            model=self.model, 
            tools=tools,
            checkpointer=checkpointer
        )
        
        print(f"Agent created with {len(tools)} tools")
    
    async def invoke(self, message: str, thread_id: str = "default") -> str:
        """Invoke the agent with a user message."""
        if self.agent is None:
            raise RuntimeError("Agent not created. Call create_agent() first.")
        
        config_dict = {"configurable": {"thread_id": thread_id}}
        
        response = await self.agent.ainvoke(
            {"messages": [HumanMessage(content=message)]},
            config=config_dict
        )
        
        return response['messages'][-1].content
    
    async def get_greeting(self) -> str:
        """Get an initial greeting from the agent."""
        greeting_prompt = "Greet the user and explain your capabilities. Keep it short and concise."
        return await self.invoke(greeting_prompt)