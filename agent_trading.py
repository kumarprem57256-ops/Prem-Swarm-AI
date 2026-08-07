import asyncio

class TradingAgent:
    def __init__(self, api_key=None, access_token=None):
        self.name = "Trading_Agent_Beta"
        self.api_key = api_key
        self.access_token = access_token
        self.kite = None

    async def analyze_and_trade(self, symbol, action="BUY", quantity=1):
        if not self.kite:
            print(f"[{self.name}] Zerodha API credentials not configured. Running in SIMULATION mode.")
            return {"status": "simulated", "symbol": symbol, "action": action, "quantity": quantity}
        
        try:
            quote = self.kite.quote(f"NSE:{symbol}")
            price = quote[f"NSE:{symbol}"]["last_price"]
            print(f"[{self.name}] Live Price for {symbol}: ₹{price}")
            
            order_id = self.kite.place_order(
                tradingsymbol=symbol,
                exchange=self.kite.EXCHANGE_NSE,
                transaction_type=self.kite.TRANSACTION_TYPE_BUY if action == "BUY" else self.kite.TRANSACTION_TYPE_SELL,
                quantity=quantity,
                order_type=self.kite.ORDER_TYPE_MARKET,
                product=self.kite.PRODUCT_MIS
            )
            return {"status": "executed", "order_id": order_id, "price": price}
        except Exception as e:
            raise RuntimeError(f"Trading Execution Failed: {str(e)}")
