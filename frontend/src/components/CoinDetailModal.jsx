import React from 'react';
import { Lock, Play, X, ShieldAlert, Zap, Compass, Activity } from 'lucide-react';

export default function CoinDetailModal({ coin, isUnlocked, onWatchAd, onClose }) {
  if (!coin) return null;

  return (
    <div className="fixed inset-0 bg-black/85 backdrop-blur-md flex items-center justify-center p-4 z-50 animate-fade-in">
      <div className="bg-slate-900 border border-slate-800 w-full max-w-md rounded-2xl p-6 relative shadow-2xl overflow-hidden">
        
        {/* Modal Kapat Butonu */}
        <button 
          onClick={onClose} 
          className="absolute top-4 right-4 text-slate-400 hover:text-white bg-slate-800/50 p-1.5 rounded-full">
          <X size={18} />
        </button>

        {/* Coin Başlık */}
        <div className="flex items-center gap-3 mb-6">
          <div className="w-10 h-10 rounded-full bg-cyan-950 border border-cyan-700/50 flex items-center justify-center font-black text-cyan-400 text-sm">
            {coin.symbol.substring(0, 3)}
          </div>
          <div>
            <h3 className="text-lg font-black text-white">{coin.name} ({coin.symbol})</h3>
            <p className="text-xs text-slate-400 font-mono">${coin.price.toLocaleString()} USDT</p>
          </div>
        </div>

        {/* KİLİTLİ ALAN / İÇERİK */}
        {!isUnlocked ? (
          <div className="bg-slate-950/90 border border-slate-800 rounded-xl p-6 text-center my-4">
            <div className="w-12 h-12 bg-cyan-950/80 rounded-full flex items-center justify-center mx-auto mb-3 text-cyan-400 border border-cyan-800/50">
              <Lock size={22} />
            </div>
            <h4 className="text-sm font-bold text-white mb-2">Pro İndikatör Analizi Kilitli</h4>
            <p className="text-xs text-slate-400 mb-6 leading-relaxed">
              Formasyon Merkezi çizgi hedeflerini, Tier-1 Elite sinyal seviyelerini ve canlı alarmları aktif etmek için ödüllü reklamı izleyin.
            </p>
            
            <button 
              onClick={onWatchAd}
              className="w-full bg-gradient-to-r from-cyan-600 to-blue-600 hover:from-cyan-500 hover:to-blue-500 text-white font-bold py-3.5 px-4 rounded-xl text-xs tracking-wider flex items-center justify-center gap-2 shadow-lg shadow-cyan-900/40 transition-all active:scale-95">
              <Play size={16} fill="white" /> Ödüllü Reklamı İzle & Kilidi Aç
            </button>
          </div>
        ) : (
          /* KİLİT AÇILDIĞINDA GÖRÜNECEK DETAYLI İNDİKATÖR RAPORU */
          <div className="space-y-3 my-4 max-h-[60vh] overflow-y-auto pr-1">
            <div className="bg-slate-950 p-3 rounded-lg border border-slate-800/80">
              <span className="text-[10px] text-slate-500 uppercase font-semibold flex items-center gap-1">
                <Compass size={12} className="text-cyan-400"/> Formasyon Merkezi V2
              </span>
              <p className="text-xs font-bold text-cyan-300 mt-1">{coin.indicators?.pattern_center || "Trend Takip Ediliyor"}</p>
            </div>

            <div className="bg-slate-950 p-3 rounded-lg border border-slate-800/80">
              <span className="text-[10px] text-slate-500 uppercase font-semibold flex items-center gap-1">
                <Activity size={12} className="text-purple-400"/> Volatilite & Squeeze
              </span>
              <p className="text-xs font-bold text-purple-300 mt-1">{coin.indicators?.squeeze_status || "Stabil"}</p>
            </div>

            <div className="bg-slate-950 p-3 rounded-lg border border-slate-800/80">
              <span className="text-[10px] text-slate-500 uppercase font-semibold flex items-center gap-1">
                <Zap size={12} className="text-emerald-400"/> Multi-Tier Sinyal Motoru
              </span>
              <p className="text-xs font-bold text-emerald-400 mt-1">{coin.indicators?.tier_signal || "Tier-3 Rapid"}</p>
            </div>

            <div className="bg-slate-950 p-3 rounded-lg border border-slate-800/80">
              <span className="text-[10px] text-slate-500 uppercase font-semibold flex items-center gap-1">
                <ShieldAlert size={12} className="text-amber-400"/> Makro Döngü & Değerleme
              </span>
              <p className="text-xs font-bold text-amber-300 mt-1">{coin.indicators?.macro_cycle || "Normal Seviye"}</p>
            </div>
          </div>
        )}

      </div>
    </div>
  );
}
