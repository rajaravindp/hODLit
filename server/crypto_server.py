import os
from dotenv import load_dotenv
import httpx
from fastmcp import FastMCP, Context
from fastmcp.exceptions import ToolError
from pydantic import Field
import asyncio

load_dotenv()
CG_API_KEY = os.getenv("CG_API_KEY")
mcp = FastMCP(name="cryptoServer", instructions="Get cryptocurrency data using CoinGecko API.")
client = httpx.AsyncClient(timeout=15)


@mcp.tool(
    name="list_supported_cryptocurrencies",
    description="List supported cryptocurrencies from CoinGecko API"
)
async def get_supported_cryptocurrencies() -> str:
    """Fetch a list of supported cryptocurrencies from CoinGecko API."""
    try:
        url = "https://api.coingecko.com/api/v3/simple/supported_vs_currencies"
        headers = {
            "accept": "application/json",
            "x-cg-demo-api-key": CG_API_KEY
        }
        response = await client.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()

        return ", ".join(data)

    except Exception as e:
        raise ToolError(f"Error fetching supported cryptocurrencies: {str(e)}")


@mcp.tool(
    name="get_coin_ticker_by_ID",
    description="Get the ticker information for a cryptocurrency by its ID from CoinGecko API"
)
async def get_coin_ticker_by_ID(
    crypto_id: str = Field(..., description="The ID of the cryptocurrency")
) -> str:
    """Fetch the ticker information for a cryptocurrency by its ID from CoinGecko API."""
    try:
        url = f"https://api.coingecko.com/api/v3/coins/{crypto_id}/tickers"
        headers = {
            "accept": "application/json",
            "x-cg-demo-api-key": CG_API_KEY
        }
        response = await client.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()

        return data["tickers"][0]["base"]

    except Exception as e:
        raise ToolError(f"Error fetching coin ticker: {str(e)}")


@mcp.tool(
    name="get_crypto_price_vs_currency",
    description="Get the current price of a cryptocurrency from CoinGecko API"
)
async def get_crypto_price_vs_currency(
    crypto_id: str = Field(..., description="The ID of the cryptocurrency"),
    vs_currency: str = Field(default="usd", description="The target currency")
) -> float:
    """Fetch the current price of a cryptocurrency versus a target currency from CoinGecko API."""
    try: 
        url = f"https://api.coingecko.com/api/v3/simple/price?vs_currencies={vs_currency}&ids={crypto_id}"
        headers = {
            "accept": "application/json",
            "x-cg-demo-api-key": CG_API_KEY
        }
        response = await client.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()

        return data[crypto_id][vs_currency]
    
    except Exception as e:
        raise ToolError(f"Error fetching crypto price: {str(e)}")


@mcp.tool(
    name="get_historical_coin_data",
    description="Get historical data for a cryptocurrency from CoinGecko API"
)
async def get_historical_coin_data(
    crypto_id: str = Field(..., description="The ID of the cryptocurrency"),
    days: str = Field(..., description="The number of days to retrieve historical data for"),
    vs_currency: str = Field(default="usd", description="The target currency")
) -> dict:
    """
    Get the historical chart data of a coin including time in UNIX, price, market cap and 24hr volume
    Info returned: 
        A. prices: Array of [ [time, price], ... ]
        B. market_caps: Array of [ [time, market_cap], ... ]
        C. total_volumes: Array of [ [time, total_volume], ... ]
    """
    try:
        url = f"https://api.coingecko.com/api/v3/coins/{crypto_id}/market_chart?vs_currency={vs_currency}&days={days}"
        headers = {
            "accept": "application/json",
            "x-cg-demo-api-key": CG_API_KEY
        }
        response = await client.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()

        return data

    except Exception as e:
        raise ToolError(f"Error fetching historical coin data: {str(e)}")


@mcp.prompt(name="coin_data_prompt", description="Prompt for querying cryptocurrency data")
async def coin_data_prompt(
    query: str = Field(..., description="The query about cryptocurrencies"), 
    ctx: Context = Field(description="MCP context")
) -> str:
    return f"""
        Answer the following query about cryptocurrencies using the available tools and the context
        Query: {query}
    """


if __name__ == "__main__":
    asyncio.run(mcp.run_async(transport="stdio"))
