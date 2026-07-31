#include "backtest_engine.hpp"
#include "../technical/indicators.hpp"
#include <cmath>
#include <numeric>
#include <algorithm>

namespace TaiwanQuant {

BacktestEngine::BacktestEngine(const StorageEngine& storage)
    : storage_(storage) {}

BacktestResult BacktestEngine::runBacktest(const std::string& symbol, double initialCapital) {
    BacktestResult res;
    res.strategyName = "C++ 智慧機器人雙均線與 KD 綜合突破策略";
    
    auto kbars = storage_.getKBars(symbol, PeriodType::DAILY, 500);
    if (kbars.size() < 30) {
        return res;
    }

    double capital = initialCapital;
    double maxCapital = initialCapital;
    double maxDrawdown = 0.0;

    bool inPosition = false;
    double buyPrice = 0.0;
    int positionShares = 0;

    auto ma5 = TechnicalAnalysis::calculateSMA(kbars, 5);
    auto ma20 = TechnicalAnalysis::calculateSMA(kbars, 20);
    auto kd = TechnicalAnalysis::calculateKD(kbars);

    std::vector<double> dailyReturns;
    double grossProfit = 0.0;
    double grossLoss = 0.0;

    for (size_t i = 20; i < kbars.size(); ++i) {
        double price = kbars[i].close;
        double prevCapital = capital;

        // 進場條件: MA5 上穿 MA20 且 K > D (黃金交叉)
        bool buyCondition = (ma5[i] > ma20[i] && ma5[i - 1] <= ma20[i - 1] && kd.k[i] > kd.d[i]);
        // 出場條件: MA5 下穿 MA20 或 K < D (死亡交叉)
        bool sellCondition = (ma5[i] < ma20[i] && ma5[i - 1] >= ma20[i - 1]);

        if (!inPosition && buyCondition) {
            inPosition = true;
            buyPrice = price;
            positionShares = static_cast<int>(capital / (price * 1.001425)); // 考慮手續費
            capital -= positionShares * price * 1.001425;

            Signal sig{symbol, symbol, MarketType::TWSE_STOCK, kbars[i].timestamp, "BUY", 85.0, "均線黃金交叉進場", price};
            res.executedTrades.push_back(sig);
        } else if (inPosition && (sellCondition || i == kbars.size() - 1)) {
            inPosition = false;
            double sellProceeds = positionShares * price * (1.0 - 0.001425 - 0.003); // 考慮手續費與證交稅
            capital += sellProceeds;
            double pnl = sellProceeds - (positionShares * buyPrice * 1.001425);

            res.totalTrades++;
            if (pnl > 0) {
                res.winningTrades++;
                grossProfit += pnl;
            } else {
                res.losingTrades++;
                grossLoss += std::abs(pnl);
            }

            Signal sig{symbol, symbol, MarketType::TWSE_STOCK, kbars[i].timestamp, "SELL", 35.0, "均線死亡交叉出場", price};
            res.executedTrades.push_back(sig);
        }

        double currentAsset = capital + (inPosition ? positionShares * price : 0.0);
        maxCapital = std::max(maxCapital, currentAsset);
        double drawdown = (maxCapital - currentAsset) / maxCapital * 100.0;
        maxDrawdown = std::max(maxDrawdown, drawdown);

        if (prevCapital > 0) {
            dailyReturns.push_back((currentAsset - prevCapital) / prevCapital);
        }
    }

    double finalAsset = capital + (inPosition ? positionShares * kbars.back().close : 0.0);
    res.totalReturn = (finalAsset - initialCapital) / initialCapital * 100.0;
    res.winRate = (res.totalTrades > 0) ? (static_cast<double>(res.winningTrades) / res.totalTrades * 100.0) : 0.0;
    res.maxDrawdown = maxDrawdown;
    res.profitFactor = (grossLoss > 0) ? (grossProfit / grossLoss) : (grossProfit > 0 ? 99.0 : 0.0);

    // 計算夏普比率 Sharpe Ratio
    if (!dailyReturns.empty()) {
        double meanReturn = std::accumulate(dailyReturns.begin(), dailyReturns.end(), 0.0) / dailyReturns.size();
        double variance = 0.0;
        for (double r : dailyReturns) {
            variance += (r - meanReturn) * (r - meanReturn);
        }
        double stdDev = std::sqrt(variance / dailyReturns.size());
        res.sharpeRatio = (stdDev > 0) ? (meanReturn / stdDev * std::sqrt(252.0)) : 0.0;
    }
    res.annualizedReturn = res.totalReturn * (252.0 / std::max(static_cast<size_t>(1), kbars.size()));

    return res;
}

} // namespace TaiwanQuant
