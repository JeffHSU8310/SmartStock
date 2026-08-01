#include "indicators.hpp"
#include <cmath>
#include <algorithm>
#include <numeric>

namespace SmartStock {

std::vector<double> TechnicalEngine::calculateSMA(const std::vector<double>& prices, int period) {
    size_t n = prices.size();
    std::vector<double> sma(n, 0.0);
    if (n < static_cast<size_t>(period) || period <= 0) return sma;

    double sum = 0.0;
    for (int i = 0; i < period; ++i) {
        sum += prices[i];
    }
    sma[period - 1] = sum / period;

    for (size_t i = period; i < n; ++i) {
        sum += prices[i] - prices[i - period];
        sma[i] = sum / period;
    }
    return sma;
}

std::vector<double> TechnicalEngine::calculateEMA(const std::vector<double>& prices, int period) {
    size_t n = prices.size();
    std::vector<double> ema(n, 0.0);
    if (n < static_cast<size_t>(period) || period <= 0) return ema;

    double multiplier = 2.0 / (period + 1.0);
    double sum = 0.0;
    for (int i = 0; i < period; ++i) {
        sum += prices[i];
    }
    ema[period - 1] = sum / period;

    for (size_t i = period; i < n; ++i) {
        ema[i] = (prices[i] - ema[i - 1]) * multiplier + ema[i - 1];
    }
    return ema;
}

std::vector<double> TechnicalEngine::calculateRSI(const std::vector<double>& prices, int period) {
    size_t n = prices.size();
    std::vector<double> rsi(n, 50.0);
    if (n <= static_cast<size_t>(period) || period <= 0) return rsi;

    double avg_gain = 0.0, avg_loss = 0.0;
    for (int i = 1; i <= period; ++i) {
        double change = prices[i] - prices[i - 1];
        if (change > 0) avg_gain += change;
        else avg_loss += std::abs(change);
    }
    avg_gain /= period;
    avg_loss /= period;

    if (avg_loss == 0.0) rsi[period] = 100.0;
    else rsi[period] = 100.0 - (100.0 / (1.0 + avg_gain / avg_loss));

    for (size_t i = period + 1; i < n; ++i) {
        double change = prices[i] - prices[i - 1];
        double gain = (change > 0) ? change : 0.0;
        double loss = (change < 0) ? std::abs(change) : 0.0;

        avg_gain = (avg_gain * (period - 1) + gain) / period;
        avg_loss = (avg_loss * (period - 1) + loss) / period;

        if (avg_loss == 0.0) rsi[i] = 100.0;
        else rsi[i] = 100.0 - (100.0 / (1.0 + avg_gain / avg_loss));
    }
    return rsi;
}

void TechnicalEngine::calculateMACD(const std::vector<double>& prices,
                                    std::vector<double>& outMACD,
                                    std::vector<double>& outSignal,
                                    std::vector<double>& outHist) {
    size_t n = prices.size();
    outMACD.assign(n, 0.0);
    outSignal.assign(n, 0.0);
    outHist.assign(n, 0.0);

    if (n < 26) return;

    std::vector<double> ema12 = calculateEMA(prices, 12);
    std::vector<double> ema26 = calculateEMA(prices, 26);

    for (size_t i = 0; i < n; ++i) {
        outMACD[i] = ema12[i] - ema26[i];
    }
    outSignal = calculateEMA(outMACD, 9);

    for (size_t i = 0; i < n; ++i) {
        outHist[i] = outMACD[i] - outSignal[i];
    }
}

void TechnicalEngine::calculateKD(const std::vector<KBar>& kbars,
                                  std::vector<double>& outK,
                                  std::vector<double>& outD) {
    size_t n = kbars.size();
    outK.assign(n, 50.0);
    outD.assign(n, 50.0);

    if (n < 9) return;

    double lastK = 50.0;
    double lastD = 50.0;

    for (size_t i = 8; i < n; ++i) {
        double highest_high = kbars[i].high;
        double lowest_low = kbars[i].low;

        for (size_t j = i - 8; j <= i; ++j) {
            highest_high = std::max(highest_high, kbars[j].high);
            lowest_low = std::min(lowest_low, kbars[j].low);
        }

        double rsv = 50.0;
        if (highest_high != lowest_low) {
            rsv = (kbars[i].close - lowest_low) / (highest_high - lowest_low) * 100.0;
        }

        lastK = (2.0 / 3.0) * lastK + (1.0 / 3.0) * rsv;
        lastD = (2.0 / 3.0) * lastD + (1.0 / 3.0) * lastK;

        outK[i] = lastK;
        outD[i] = lastD;
    }
}

std::string TechnicalEngine::detectPattern(const std::vector<KBar>& kbars) {
    if (kbars.size() < 2) return "無明顯型態";

    const auto& prev = kbars[kbars.size() - 2];
    const auto& curr = kbars.back();

    bool prev_bear = prev.close < prev.open;
    bool curr_bull = curr.close > curr.open;

    // 看漲吞噬 Bullish Engulfing
    if (prev_bear && curr_bull && curr.open <= prev.close && curr.close >= prev.open) {
        return "🔥 看漲吞噬 (Bullish Engulfing)";
    }

    // 錘子強撐 Hammer
    double body = std::abs(curr.close - curr.open);
    double lower_shadow = std::min(curr.open, curr.close) - curr.low;
    double upper_shadow = curr.high - std::max(curr.open, curr.close);

    if (lower_shadow >= 2.0 * body && upper_shadow <= body * 0.5 && body > 0) {
        return "🔨 錘子線 (Hammer Support)";
    }

    // 長紅突破 Long Bullish
    double pct = (curr.close - curr.open) / curr.open * 100.0;
    if (pct >= 3.5) {
        return "🚀 長紅大陽線 (Long Bullish Breakout)";
    }

    return "趨勢整理 (Consolidating)";
}

} // namespace SmartStock
