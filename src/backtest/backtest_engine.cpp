#include "backtest_engine.hpp"
#include "../technical/indicators.hpp"
#include <cmath>
#include <algorithm>

namespace SmartStock {

BacktestResult BacktestEngine::runMABacktest(const std::vector<KBar>& history, int fastPeriod, int slowPeriod, double initialCapital) {
    return runFastBacktest(history, fastPeriod, slowPeriod, initialCapital, 0.001425, 0.003, 0.0);
}

BacktestResult BacktestEngine::runFastBacktest(const std::vector<KBar>& history, int fastPeriod, int slowPeriod, double initialCapital, double feeRate, double taxRate, double slippage) {
    BacktestResult res = {0.0, 0.0, 0.0, 0.0, 0, 0, 0};
    if (history.size() < static_cast<size_t>(slowPeriod + 1)) return res;

    std::vector<double> closes;
    closes.reserve(history.size());
    for (const auto& kb : history) {
        closes.push_back(kb.close);
    }

    std::vector<double> fastMA = TechnicalEngine::calculateSMA(closes, fastPeriod);
    std::vector<double> slowMA = TechnicalEngine::calculateSMA(closes, slowPeriod);

    double capital = initialCapital;
    double maxCapital = capital;
    double maxDrawdown = 0.0;
    bool inPosition = false;
    double entryPrice = 0.0;
    int shares = 0;

    std::vector<double> returnsList;

    for (size_t i = slowPeriod; i < history.size(); ++i) {
        // 黃金交叉買入 Golden Cross (加入滑價與手續費)
        if (!inPosition && fastMA[i - 1] <= slowMA[i - 1] && fastMA[i] > slowMA[i]) {
            entryPrice = history[i].close + slippage;
            shares = static_cast<int>(capital / (entryPrice * 1000.0)) * 1000;
            if (shares > 0) {
                double entryFee = (entryPrice * shares) * feeRate;
                capital -= entryFee;
                inPosition = true;
            }
        }
        // 死亡交叉賣出 Death Cross (扣除手續費與證交稅)
        else if (inPosition && fastMA[i - 1] >= slowMA[i - 1] && fastMA[i] < slowMA[i]) {
            double exitPrice = history[i].close - slippage;
            double amount = exitPrice * shares;
            double exitFee = amount * feeRate;
            double exitTax = amount * taxRate;
            
            double grossPnl = (exitPrice - entryPrice) * shares;
            double netPnl = grossPnl - (exitFee + exitTax);
            capital += netPnl;
            res.total_trades++;

            double ret = (exitPrice - entryPrice) / entryPrice;
            returnsList.push_back(ret);

            if (netPnl > 0) res.winning_trades++;
            else res.losing_trades++;

            inPosition = false;
            shares = 0;
        }

        double currentAsset = capital;
        if (inPosition) {
            currentAsset = capital + (history[i].close - entryPrice) * shares;
        }
        if (currentAsset > maxCapital) {
            maxCapital = currentAsset;
        }
        double dd = (maxCapital > 0) ? ((maxCapital - currentAsset) / maxCapital * 100.0) : 0.0;
        if (dd > maxDrawdown) {
            maxDrawdown = dd;
        }
    }

    // 計算總表現與夏普率
    res.total_return_pct = (capital - initialCapital) / initialCapital * 100.0;
    res.win_rate = (res.total_trades > 0) ? (static_cast<double>(res.winning_trades) / res.total_trades * 100.0) : 0.0;
    res.max_drawdown_pct = maxDrawdown;

    if (!returnsList.empty()) {
        double mean = 0.0;
        for (double r : returnsList) mean += r;
        mean /= returnsList.size();

        double sq_sum = 0.0;
        for (double r : returnsList) sq_sum += (r - mean) * (r - mean);
        double stddev = std::sqrt(sq_sum / returnsList.size());

        if (stddev > 0) {
            res.sharpe_ratio = (mean / stddev) * std::sqrt(252.0);
        }
    }

    return res;
}

} // namespace SmartStock
