from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Nexus Alpha TMA Backend", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

TOP_SYMBOLS = [
    {"symbol": "BTC", "name": "Bitcoin"},
    {"symbol": "ETH", "name": "Ethereum"},
    {"symbol": "BNB", "name": "BNB"},
    {"symbol": "SOL", "name": "Solana"},
    {"symbol": "XRP", "name": "XRP"},
    {"symbol": "ADA", "name": "Cardano"},
    {"symbol": "AVAX", "name": "Avalanche"},
    {"symbol": "DOGE", "name": "Dogecoin"},
    {"symbol": "DOT", "name": "Polkadot"},
    {"symbol": "LINK", "name": "Chainlink"},
]

@app.get("/")
def read_root():
    return {"status": "online", "project": "Nexus Alpha TMA Engine"}

@app.get("/api/market-overview")
def get_market_overview():
    market_data = []
    
    for item in TOP_SYMBOLS:
        market_data.append({
            "symbol": item["symbol"],
            "name": item["name"],
            "trend_matrix": "BULLISH MOMENTUM 🚀",
            "squeeze_status": "BREAKOUT ACTIVE",
            "tier1_signal": "👑 ELITE LONG",
            "macro_cycle": "ACCUMULATION ZONE 🟢"
        })

    return {"status": "success", "data": market_data}
