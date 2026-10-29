from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import requests

app = FastAPI(title="Nexus Alpha TMA Backend", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

TOP_SYMBOLS = ["BTC", "ETH", "BNB", "SOL", "XRP", "ADA", "AVAX", "DOGE", "DOT", "LINK"]

@app.get("/")
def read_root():
    return {"status": "online", "project": "Nexus Alpha TMA Engine"}

@app.get("/api/market-overview")
def get_market_overview():
    market_data = []
    
    try:
        # CoinCap API (Bulut sunucularında engellenmez, anlık ve güvenilirdir)
        res = requests.get("https://api.coincap.io/v2/assets?limit=20", timeout=5)
        if res.status_code == 200:
            coins_raw = res.json().get("data", [])
            coins_map = {item["symbol"]: item for item in coins_raw}
            
            for sym in TOP_SYMBOLS:
                c_info = coins_map.get(sym, {})
                price = float(c_info.get("priceUsd", 0.0))
                change_24h = float(c_info.get("changePercent24Hr", 0.0))
                
                market_data.append({
                    "symbol": sym,
                    "name": c_info.get("name", sym),
                    "price": price,
                    "change_24h": round(change_24h, 2),
                    "trend_matrix": "BULLISH MOMENTUM 🚀" if change_24h >= 0 else "BEARISH MOMENTUM 📉",
                    "squeeze_status": "BREAKOUT ACTIVE" if abs(change_24h) > 3.5 else "CONSOLIDATION",
                    "tier1_signal": "👑 ELITE LONG" if change_24h > 2 else "✦ RAPID",
                    "macro_cycle": "ACCUMULATION ZONE 🟢"
                })
    except Exception as e:
        print(f"API Error: {e}")

    # İstek başarısız olursa boş dönmesin
    if not market_data:
        for sym in TOP_SYMBOLS:
            market_data.append({
                "symbol": sym, "name": sym, "price": 0.0, "change_24h": 0.0,
                "trend_matrix": "NEUTRAL", "squeeze_status": "NORMAL", "tier1_signal": "✦ RAPID", "macro_cycle": "STABLE"
            })

    return {"status": "success", "data": market_data}
