from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import requests

app = FastAPI(title="Nexus Alpha TMA Backend", version="1.0.0")

# CORS ayarları (Mini App'in frontend'inden gelecek isteklere izin vermek için)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# İlk 10 Major Coin Listesi
TOP_COINS = [
    {"symbol": "BTC", "name": "Bitcoin", "binance": "BTCUSDT"},
    {"symbol": "ETH", "name": "Ethereum", "binance": "ETHUSDT"},
    {"symbol": "BNB", "name": "BNB", "binance": "BNBUSDT"},
    {"symbol": "SOL", "name": "Solana", "binance": "SOLUSDT"},
    {"symbol": "XRP", "name": "XRP", "binance": "XRPUSDT"},
    {"symbol": "ADA", "name": "Cardano", "binance": "ADAUSDT"},
    {"symbol": "AVAX", "name": "Avalanche", "binance": "AVAXUSDT"},
    {"symbol": "DOGE", "name": "Dogecoin", "binance": "DOGEUSDT"},
    {"symbol": "DOT", "name": "Polkadot", "binance": "DOTUSDT"},
    {"symbol": "LINK", "name": "Chainlink", "binance": "LINKUSDT"},
]

@app.get("/")
def read_root():
    return {"status": "online", "project": "Nexus Alpha TMA Engine"}

@app.get("/api/market-overview")
def get_market_overview():
    market_data = []
    
    # Binance'den güncel fiyatları toplu çekme
    try:
        res = requests.get("https://api.binance.com/api/v3/ticker/24hr", timeout=5)
        tickers = {item['symbol']: item for item in res.json()}
    except:
        tickers = {}

    for coin in TOP_COINS:
        ticker = tickers.get(coin["binance"], {})
        price = float(ticker.get("lastPrice", 0.0))
        change_24h = float(ticker.get("priceChangePercent", 0.0))
        
        # Senin geliştirdiğin indikatörlerin simüle edilmiş sinyal matrisi
        # Backend tarafında pandas ile gerçek hesaplamalar buraya entegre edilecek
        market_data.append({
            "symbol": coin["symbol"],
            "name": coin["name"],
            "price": price,
            "change_24h": change_24h,
            "trend_matrix": "BULLISH MOMENTUM 🚀" if change_24h > 0 else "BEARISH MOMENTUM 📉",
            "squeeze_status": "BREAKOUT ACTIVE" if abs(change_24h) > 3.5 else "CONSOLIDATION",
            "tier1_signal": "👑 ELITE LONG" if change_24h > 2 else "✦ RAPID",
            "macro_cycle": "ACCUMULATION ZONE 🟢"
        })

    return {"status": "success", "data": market_data}
