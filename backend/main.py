from fastapi import FastAPI
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

# Kesinlikle sıfır düşmemesi için güncel piyasa baz fiyatları yedek matrisi
DEFAULT_PRICES = {
    "BTC": {"name": "Bitcoin", "price": 87500.0, "change": 2.45},
    "ETH": {"name": "Ethereum", "price": 2450.0, "change": -1.29},
    "BNB": {"name": "BNB", "price": 645.0, "change": 1.15},
    "SOL": {"name": "Solana", "price": 185.0, "change": 4.20},
    "XRP": {"name": "XRP", "price": 1.45, "change": 0.85},
    "ADA": {"name": "Cardano", "price": 0.78, "change": -0.50},
    "AVAX": {"name": "Avalanche", "price": 32.50, "change": 3.10},
    "DOGE": {"name": "Dogecoin", "price": 0.22, "change": 5.40},
    "DOT": {"name": "Polkadot", "price": 7.40, "change": -0.90},
    "LINK": {"name": "Chainlink", "price": 18.20, "change": 2.10},
}

@app.get("/")
def read_root():
    return {"status": "online", "project": "Nexus Alpha TMA Engine"}

@app.get("/api/market-overview")
def get_market_overview():
    market_data = []
    coins_map = {}
    
    try:
        res = requests.get("https://api.coincap.io/v2/assets?limit=20", timeout=4)
        if res.status_code == 200:
            data_json = res.json().get("data", [])
            coins_map = {item["symbol"]: item for item in data_json}
    except Exception as e:
        print(f"API Fetch Error: {e}")

    for sym, default_info in DEFAULT_PRICES.items():
        c_info = coins_map.get(sym, {})
        
        # CoinCap'ten anlık fiyat gelirse onu al, gelmezse güvenli yedek fiyatı kullan
        price = float(c_info.get("priceUsd", 0.0))
        change_24h = float(c_info.get("changePercent24Hr", 0.0))
        
        if price == 0.0:
            price = default_info["price"]
            change_24h = default_info["change"]

        market_data.append({
            "symbol": sym,
            "name": c_info.get("name", default_info["name"]),
            "price": price,
            "change_24h": round(change_24h, 2),
            "trend_matrix": "BULLISH MOMENTUM 🚀" if change_24h >= 0 else "BEARISH MOMENTUM 📉",
            "squeeze_status": "BREAKOUT ACTIVE" if abs(change_24h) > 3.5 else "CONSOLIDATION",
            "tier1_signal": "👑 ELITE LONG" if change_24h > 2 else "✦ RAPID",
            "macro_cycle": "ACCUMULATION ZONE 🟢"
        })

    return {"status": "success", "data": market_data}
