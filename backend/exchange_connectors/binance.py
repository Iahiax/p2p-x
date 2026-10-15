# backend/exchange_connectors/binance.py

import httpx

BASE_URL = "https://api.binance.com"

async def get_binance_price(symbol: str) -> float:
    """
    يجلب سعر زوج مثل BTCUSDT أو ETHUSDT من Binance (مجاني).
    """
    async with httpx.AsyncClient() as client:
        r = await client.get(f"{BASE_URL}/api/v3/ticker/price", params={"symbol": symbol})
        r.raise_for_status()
        return float(r.json()["price"])

async def get_order_book(symbol: str, limit: int = 5):
    """
    يجلب دفتر الأوامر (اختياري).
    """
    async with httpx.AsyncClient() as client:
        r = await client.get(f"{BASE_URL}/api/v3/depth", params={"symbol": symbol, "limit": limit})
        r.raise_for_status()
        return r.json()
