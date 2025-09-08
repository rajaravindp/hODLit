## Overview
This is a language-driven cryptocurrency agent that leverages LangGraph, MCP, and AWS Bedrock LLMs to provide real-time crypto insights. Ask it anything about cryptocurrency prices, historical trends, and tickers

### Features
- Real-time cryptocurrency data using the CoinGecko API
- Historical price queries – daily averages, market charts, and more
- Language-first interaction – just ask, no SQL or API calls needed
- Multi-server support via MCP for scalable tool execution
- Langgraph agent - AWS Bedrock LLM integration with Amazon Nova Lite for natural language reasoning
- ADK agent - Gemini integration for natural language reasoning

### Frameworks
- FastMCP 
- Langgraph
- Google ADK

### Installation
1. Clone the repository:
   ```powershell
   git clone https://github.com/rajaravindp/hODLit
   cd mcp-lg
   ```
2. (Optional) Create and activate a virtual environment:
   ```powershell
   uv venv
   .venv\Scripts\Activate.ps1
   ```
3. Install dependencies:
   ```powershell
   uv sync
   ```
4. Run ADK agent
   ```powershell
    cd adk_agent.py
    uv run adk web
   ```
   Run Langgraph agent
   ```powershell
    cd langgraph_agent.py
    uv run main.py
   ```