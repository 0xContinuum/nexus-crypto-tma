import pandas as pd
import numpy as np

def calculate_all_indicators(df: pd.DataFrame) -> dict:
    """
    df: 'open', 'high', 'low', 'close', 'volume' sütunlarını içeren Pandas DataFrame
    """
    close = df['close']
    high = df['high']
    low = df['low']
    volume = df['volume']
    
    # 1. Gelişmiş Formasyon Merkezi V2 (Pivot & Trend Slope)
    # Son 10 barın pivot tepe/dipleri
    ph = high.rolling(window=10, center=True).max()
    pl = low.rolling(window=10, center=True).min()
    pattern_signal = "FORMAYON ARANIYOR"
    if not ph.dropna().empty and not pl.dropna().empty:
        if close.iloc[-1] > ph.dropna().iloc[-1]:
            pattern_signal = "YÜKSELEN ÜÇGEN (BREAKOUT)"
        elif close.iloc[-1] < pl.dropna().iloc[-1]:
            pattern_signal = "ALÇALAN ÜÇGEN (BREAKOUT)"

    # 2. Squeeze & Liquidity Breakout (Bollinger + Keltner + Pinbar)
    basis = close.rolling(20).mean()
    dev = 2.0 * close.rolling(20).std()
    upper_bb = basis + dev
    lower_bb = basis - dev
    
    range_ma = (high - low).rolling(20).mean()
    upper_kc = basis + range_ma * 1.5
    lower_kc = basis - range_ma * 1.5
    
    sqz_on = (lower_bb > lower_kc) and (upper_bb < upper_kc)
    sqz_status = "SQUEEZE (SIKIŞMA)" if sqz_on.iloc[-1] else "VOLATİLİTE GENİŞLEMESİ"

    # 3. Dynamic HMA Momentum Starter (HMA 24 & ATR)
    def hma(series, length):
        wma1 = series.ewm(span=length//2).mean()
        wma2 = series.ewm(span=length).mean()
        diff = 2 * wma1 - wma2
        return diff.ewm(span=int(np.sqrt(length))).mean()
    
    hma24 = hma(close, 24)
    hma_trend = "BULLISH MOMENTUM 🚀" if hma24.iloc[-1] > hma24.iloc[-2] else "BEARISH MOMENTUM 📉"

    # 4. Dynamic Elasticity & MFI Reversal (HMA 55 + MFI 9)
    # MFI Hesaplaması
    typical_price = (high + low + close) / 3
    money_flow = typical_price * volume
    positive_flow = money_flow.where(typical_price > typical_price.shift(1), 0).rolling(9).sum()
    negative_flow = money_flow.where(typical_price < typical_price.shift(1), 0).rolling(9).sum()
    mfi = 100 - (100 / (1 + (positive_flow / negative_flow)))
    
    mfi_val = mfi.iloc[-1] if not np.isnan(mfi.iloc[-1]) else 50
    reversal_signal = "NEUTRAL"
    if mfi_val < 15:
        reversal_signal = "OVERSOLD REVERSAL 🟢"
    elif mfi_val > 85:
        reversal_signal = "OVERBOUGHT REVERSAL 🔴"

    # 5 & 6. Macro Cycle & Valuation / Extreme Reversal (50 EMA & 200 SMA)
    ema50 = close.ewm(span=50).mean()
    sma200 = close.rolling(200).mean()
    
    macro_state = "NORMAL VALUE"
    if not sma200.dropna().empty:
        if close.iloc[-1] <= sma200.iloc[-1] * 1.01:
            macro_state = "ACCUMULATION ZONE 🟢"
        elif close.iloc[-1] >= sma200.iloc[-1] * 1.12:
            macro_state = "BUBBLE ZONE 🚨"

    # 7. Tiered Signal Engine (Tier-1, Tier-2, Tier-3)
    # RSI (14)
    delta = close.diff()
    gain = (delta.where(delta > 0, 0)).rolling(14).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(14).mean()
    rs = gain / loss
    rsi14 = 100 - (100 / (1 + rs))
    
    rsi_val = rsi14.iloc[-1]
    tier_signal = "✦ RAPID (TIER-3)"
    if rsi_val < 30 and hma24.iloc[-1] > hma24.iloc[-2]:
        tier_signal = "👑 ELITE LONG (TIER-1)"
    elif rsi_val > 70 and hma24.iloc[-1] < hma24.iloc[-2]:
        tier_signal = "👑 ELITE SHORT (TIER-1)"

    # Özet Sonuç Matrisi
    return {
        "pattern_center": pattern_signal,
        "squeeze_status": sqz_status,
        "hma_momentum": hma_trend,
        "mfi_reversal": reversal_signal,
        "macro_cycle": macro_state,
        "tier_signal": tier_signal
    }
