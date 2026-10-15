# backend/market_maker.py

from backend.exchange_connectors.binance import get_binance_price

async def mm_quote(src_token: str, dst_token: str, amount: float):
    """
    Market Maker بسيط:
    - يجلب سعر من Binance
    - يضيف سبريد بسيط
    - يحسب القيمة النهائية والرسوم
    """
    symbol = f"{src_token}{dst_token}"  # مثال: BTCUSDT, ETHUSDT, USDTUSD (لو متاح)

    try:
        price = await get_binance_price(symbol)
    except Exception:
        # في حال فشل جلب السعر، نستخدم سعر افتراضي
        price = 1.0

    spread = 0.003  # 0.3%
    final_rate = price * (1 - spread)
    final_amount = amount * final_rate
    fee = amount * spread

    return {
        "pair": symbol,
        "price": price,
        "spread": spread,
        "rate": final_rate,
        "final_amount": final_amount,
        "fee": fee,
        "mode": "MM"
    }
