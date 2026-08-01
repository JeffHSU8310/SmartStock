#pragma once
#include <string>
#include <vector>
#include <cstdint>

namespace SmartStock {

// 原生 K線數據結構 (Native KBar Struct)
struct KBar {
    char datetime[32]; // 時間戳記 ISO Format
    double open;       // 開盤價
    double high;       // 最高價
    double low;        // 最低價
    double close;      // 收盤價
    int64_t volume;    // 成交量 (股/張)
};

// 即時 Tick 報價結構 (Real-time Tick Quote Struct)
struct TickQuote {
    char code[16];     // 商品代碼 (例如: 2330, TX00)
    char name[32];     // 商品名稱 (例如: 台積電)
    double price;      // 成交價
    double change;     // 漲跌點數
    double pct_change; // 漲跌幅 (%)
    int64_t volume;    // 當前 Tick 量
    int64_t total_vol; // 累計總量
    char time[16];     // 成交時間 HH:MM:SS
};

// 選股成果結構 (Stock Selection Result Struct)
struct SelectionResult {
    char code[16];
    char name[32];
    double close;
    double pct_change;
    double score;        // AI 綜合動能評分 (0 ~ 100)
    char signal_type[64]; // 訊號類型 (例如: 均線多頭+長紅突破)
};

// 回測績效指標 (Backtest Performance Summary)
struct BacktestResult {
    double total_return_pct; // 總報酬率 (%)
    double win_rate;         // 勝率 (%)
    double max_drawdown_pct; // 最大回撤 MDD (%)
    double sharpe_ratio;     // 夏普值 Sharpe Ratio
    int total_trades;        // 總交易次數
    int winning_trades;      // 獲利次數
    int losing_trades;       // 虧損次數
};

} // namespace SmartStock
