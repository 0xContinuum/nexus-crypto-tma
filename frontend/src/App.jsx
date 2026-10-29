import React, { useState, useEffect } from 'react';

export default function App() {
  const [coins, setCoins] = useState([]);
  const [loading, setLoading] = useState(true);
  const [selectedCoin, setSelectedCoin] = useState(null);
  const [isUnlocked, setIsUnlocked] = useState(false);
  const [activeTab, setActiveTab] = useState('overview');

  useEffect(() => {
    // Backend API'den ilk 10 coin verisini çekme (Render URL'in eklendi)
    fetch('https://nexus-crypto-tma.onrender.com/api/market-overview')
      .then(res => res.json())
      .then(data => {
        if (data.status === 'success') {
          setCoins(data.data);
        }
        setLoading(false);
      })
      .catch(err => {
        console.error("API Error:", err);
        setLoading(false);
      });
  }, []);

  // Adsgram Ödüllü Reklam Tetikleyicisi
  const handleWatchAdToUnlock = (coin) => {
    setSelectedCoin(coin);
    
    if (window.Adsgram) {
      window.Adsgram.init({ blockId: "SENIN_ADSGRAM_BLOCK_ID" }).show()
        .then((result) => {
          // Reklam başarıyla izlendi, içerik kilidini aç
          setIsUnlocked(true);
        })
        .catch((err) => {
          console.log("Reklam tamamlanamadı", err);
          // Test ortamı için doğrudan açılış opsiyonu bırakılabilir
          setIsUnlocked(true);
        });
    } else {
      // Tarayıcı test ortamı simülasyonu
      alert("Adsgram SDK yüklü değil (Telegram ortamında çalışır). Test için kilit açılıyor.");
      setIsUnlocked(true);
    }
  };

  return (
    <div className="min-h-screen bg-[#0b0e14] text-slate-100 font-sans p-4 pb-20">
      {/* HEADER */}
      <header className="flex justify-between items-center mb-6 border-b border-slate-800 pb-4">
        <div>
          <h1 className="text-xl font-black tracking-wider text-cyan-400 flex items-center gap-2">
            NEXUS ALPHA <span className="text-xs bg-cyan-950 text-cyan-300 px-2 py-0.5 rounded border border-cyan-800">PRO</span>
          </h1>
          <p className="text-xs text-slate-400">Institutional Crypto & Macro Intelligence</p>
        </div>
        <div className="text-right">
          <span className="inline-block w-2.5 h-2.5 rounded-full bg-emerald-500 animate-pulse mr-1.5"></span>
          <span className="text-xs text-emerald-400 font-medium">Live Feed</span>
        </div>
      </header>

      {/* TABS */}
      <div className="flex gap-2 mb-6">
        <button 
          onClick={() => setActiveTab('overview')} 
          className={`flex-1 py-2 text-xs font-bold rounded-lg transition-all ${activeTab === 'overview' ? 'bg-cyan-600 text-white shadow-lg shadow-cyan-900/50' : 'bg-slate-900 text-slate-400 border border-slate-800'}`}>
          Top 10 Matrix
        </button>
        <button 
          onClick={() => setActiveTab('macro')} 
          className={`flex-1 py-2 text-xs font-bold rounded-lg transition-all ${activeTab === 'macro' ? 'bg-cyan-600 text-white shadow-lg shadow-cyan-900/50' : 'bg-slate-900 text-slate-400 border border-slate-800'}`}>
          Macro & Astro
        </button>
      </div>

      {/* COIN LIST */}
      {loading ? (
        <div className="text-center py-20 text-cyan-500 animate-pulse font-mono">Loading Market Matrix...</div>
      ) : (
        <div className="space-y-3">
          {coins.map((coin, index) => (
            <div key={index} className="bg-slate-900/80 border border-slate-800/80 rounded-xl p-4 hover:border-cyan-500/50 transition-all">
              <div className="flex justify-between items-center mb-2">
                <div className="flex items-center gap-2">
                  <span className="font-black text-white text-base">{coin.symbol}</span>
                  <span className="text-xs text-slate-500">{coin.name}</span>
                </div>
                <div className="text-right">
                  <div className="font-mono font-bold text-white">${coin.price.toLocaleString()}</div>
                  <div className={`text-xs font-semibold ${coin.change_24h >= 0 ? 'text-emerald-400' : 'text-rose-400'}`}>
                    {coin.change_24h >= 0 ? '+' : ''}{coin.change_24h}%
                  </div>
                </div>
              </div>

              {/* Indicator Badges */}
              <div className="grid grid-cols-2 gap-2 mt-3 pt-3 border-t border-slate-800/60 text-xs">
                <div className="bg-slate-950 p-2 rounded border border-slate-800">
                  <span className="text-slate-500 block text-[10px]">Trend Matrix</span>
                  <span className="font-bold text-cyan-300">{coin.trend_matrix}</span>
                </div>
                <div className="bg-slate-950 p-2 rounded border border-slate-800 flex justify-between items-center">
                  <div>
                    <span className="text-slate-500 block text-[10px]">Elite Signal</span>
                    <span className="font-bold text-purple-300">{coin.tier1_signal}</span>
                  </div>
                  <button 
                    onClick={() => handleWatchAdToUnlock(coin)}
                    className="bg-cyan-500/20 hover:bg-cyan-500/30 text-cyan-300 text-[10px] px-2.5 py-1 rounded border border-cyan-500/40 font-bold transition-all">
                    Unlock 🔓
                  </button>
                </div>
              </div>
            </div>
          ))}
        </div>
      )}

      {/* UNLOCK / REWARDED AD MODAL */}
      {selectedCoin && (
        <div className="fixed inset-0 bg-black/80 backdrop-blur-sm flex items-center justify-center p-4 z-50">
          <div className="bg-slate-900 border border-slate-700 w-full max-w-sm rounded-2xl p-6 text-center shadow-2xl">
            <h3 className="text-lg font-bold text-white mb-2">{selectedCoin.symbol} Elite Analysis</h3>
            <p className="text-xs text-slate-400 mb-6">
              Gelişmiş Formasyon Merkezi çizgilerini, çoklu zaman dilimi detaylarını ve anlık alarm kurma özelliğini aktif etmek için kısa bir ödüllü video izleyin.
            </p>
            
            {isUnlocked ? (
              <div className="bg-emerald-950/50 border border-emerald-500 text-emerald-300 p-4 rounded-xl mb-4 text-xs font-bold">
                🎉 Kilit Açıldı! Sinyal Detayları ve Altyapı Aktif.
              </div>
            ) : (
              <button 
                onClick={() => handleWatchAdToUnlock(selectedCoin)}
                className="w-full bg-gradient-to-r from-cyan-600 to-blue-600 hover:from-cyan-500 hover:to-blue-500 text-white font-bold py-3 rounded-xl text-xs tracking-wider shadow-lg shadow-cyan-900/50 transition-all mb-3">
                📺 Ödüllü Reklamı İzle & Kilidi Aç
              </button>
            )}

            <button 
              onClick={() => { setSelectedCoin(null); setIsUnlocked(false); }}
              className="text-xs text-slate-500 hover:text-slate-300 font-medium">
              Kapat
            </button>
          </div>
        </div>
      )}
    </div>
  );
}
