#ifndef TAIWAN_QUANT_TYPES_HPP
#define TAIWAN_QUANT_TYPES_HPP

#include <string>
#include <vector>
#include <map>
#include <chrono>
#include <iostream>
#include <iomanip>

namespace TaiwanQuant {

// 市場分類
enum class MarketType {
    TWSE_STOCK,  // 上市股票
    TPEX_STOCK,  // 上櫃股票
    TAIFEX_FUT,  // 台指期貨
    TAIFEX_OPT   // 選擇權
};

inline std::string marketTypeToString(MarketType market) {
    switch (market) {
        case MarketType::TWSE_STOCK: return "上市股票(TWSE)";
        case MarketType::TPEX_STOCK: return "上櫃股票(TPEX)";
        case MarketType::TAIFEX_FUT: return "台指期貨(TAIFEX)";
        case MarketType::TAIFEX_OPT: return "選擇權(TAIFEX)";
    }
    return "未知市場";
}

// 週期定義
enum class PeriodType {
    TICK,
    MIN_1,
    MIN_5,
    MIN_15,
    MIN_60,
    DAILY,
    WEEKLY,
    MONTHLY
};

// K線單根數據
struct KBar {
    std::string timestamp; // 時間戳記 YYYY-MM-DD HH:MM:SS
    double open{0.0};
    double high{0.0};
    double low{0.0};
    double close{0.0};
    int64_t volume{0};    // 成交量(股或口)
    double amount{0.0};   // 成交金額
};

// 基本面數據 (Fundamental)
struct FundamentalData {
    std::string symbol;
    std::string date;
    double monthlyRevenue{0.0};      // 當月營收(千元)
    double revenueMoM{0.0};           // 營收月增率 %
    double revenueYoY{0.0};           // 營收年增率 %
    double eps{0.0};                  // 近四季累積 EPS
    double peRatio{0.0};              // 本益比 PE
    double pbRatio{0.0};              // 股價淨值比 PB
    double roe{0.0};                  // 股東權益報酬率 ROE %
    double roa{0.0};                  // 資產報酬率 ROA %
    double grossMargin{0.0};          // 毛利率 %
    double dividendYield{0.0};        // 殖利率 %
};

// 籌碼面數據 (Chip/Institutional)
struct ChipData {
    std::string symbol;
    std::string date;
    int64_t foreignBuyNet{0};         // 外資買賣超(股/口)
    int64_t trustBuyNet{0};           // 投信買賣超(股/口)
    int64_t dealerBuyNet{0};          // 自營商買賣超(股/口)
    int64_t marginBalance{0};         // 融資餘額(張/口)
    int64_t shortBalance{0};          // 融券餘額(張/口)
    double marginShortRatio{0.0};     // 券資比 %
    double majorHoldRatio{0.0};       // 大股東持股比例 %
};

// 消息面數據 (News & Macro)
struct NewsData {
    std::string id;
    std::string timestamp;
    std::string symbol;              // 空字串代表總經消息
    std::string title;
    std::string content;
    std::string source;
    double sentimentScore{0.0};      // 情感得分 (-1.0 極悲觀 至 +1.0 極樂觀)
};

// 技術指標集 (Technical Indicators)
struct TechnicalIndicators {
    double ma5{0.0};
    double ma20{0.0};
    double ma60{0.0};
    double rsi14{0.0};
    double macdDIF{0.0};
    double macdDEA{0.0};
    double macdHist{0.0};
    double kdK{0.0};
    double kdD{0.0};
    double bbUpper{0.0};
    double bbMiddle{0.0};
    double bbLower{0.0};
    std::string patternName;          // K線型態識別 (如: 錘子線, 吞噬型態, 晨星)
};

// 交易訊號
struct Signal {
    std::string symbol;
    std::string name;
    MarketType market;
    std::string timestamp;
    std::string type;                 // "BUY" (買進), "SELL" (賣出), "HOLD" (觀望)
    double score{0.0};                // 智慧選股評分 (0 ~ 100)
    std::string reason;               // 觸發條件說明
    double triggerPrice{0.0};
};

// 回測結果報告
struct BacktestResult {
    std::string strategyName;
    int totalTrades{0};
    int winningTrades{0};
    int losingTrades{0};
    double winRate{0.0};              // 勝率 %
    double totalReturn{0.0};          // 總報酬率 %
    double annualizedReturn{0.0};     // 年化報酬率 %
    double sharpeRatio{0.0};          // 夏普比率
    double maxDrawdown{0.0};          // 最大回撤 MDD %
    double profitFactor{0.0};         // 獲利因子
    std::vector<Signal> executedTrades;
};

} // namespace TaiwanQuant

#endif // TAIWAN_QUANT_TYPES_HPP
