import httpx

async def get_binance_price(symbol: str) -> float:
    async with httpx.AsyncClient() as client:
        r = await client.get("https://api.binance.com/api/v3/ticker/price", params={"symbol": symbol})
        r.raise_for_status()
        return float(r.json()["price"])
