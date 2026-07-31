#include "indicators.hpp"
#include <cmath>
#include <algorithm>
#include <numeric>

namespace TaiwanQuant {

std::vector<double> TechnicalAnalysis::calculateSMA(const std::vector<KBar>& kbars, int period) {
    std::vector<double> result(kbars.size(), 0.0);
    if (kbars.size() < static_cast<size_t>(period) || period <= 0) return result;

    double sum = 0.0;
    for (int i = 0; i < period; ++i) {
        sum += kbars[i].close;
    }
    result[period - 1] = sum / period;

    for (size_t i = period; i < kbars.size(); ++i) {
        sum += kbars[i].close - kbars[i - period].close;
        result[i] = sum / period;
    }
    return result;
}

std::vector<double> TechnicalAnalysis::calculateEMA(const std::vector<KBar>& kbars, int period) {
    std::vector<double> result(kbars.size(), 0.0);
    if (kbars.empty() || period <= 0) return result;

    double multiplier = 2.0 / (period + 1.0);
    result[0] = kbars[0].close;

    for (size_t i = 1; i < kbars.size(); ++i) {
        result[i] = (kbars[i].close - result[i - 1]) * multiplier + result[i - 1];
    }
    return result;
}

std::vector<double> TechnicalAnalysis::calculateRSI(const std::vector<KBar>& kbars, int period) {
    std::vector<double> rsi(kbars.size(), 50.0);
    if (kbars.size() <= static_cast<size_t>(period)) return rsi;

    double avgGain = 0.0, avgLoss = 0.0;
    for (int i = 1; i <= period; ++i) {
        double change = kbars[i].close - kbars[i - 1].close;
        if (change > 0) avgGain += change;
        else avgLoss += std::abs(change);
    }
    avgGain /= period;
    avgLoss /= period;

    if (avgLoss != 0) {
        double rs = avgGain / avgLoss;
        rsi[period] = 100.0 - (100.0 / (1.0 + rs));
    } else {
        rsi[period] = 100.0;
    }

    for (size_t i = period + 1; i < kbars.size(); ++i) {
        double change = kbars[i].close - kbars[i - 1].close;
        double gain = (change > 0) ? change : 0.0;
        double loss = (change < 0) ? std::abs(change) : 0.0;

        avgGain = (avgGain * (period - 1) + gain) / period;
        avgLoss = (avgLoss * (period - 1) + loss) / period;

        if (avgLoss != 0) {
            double rs = avgGain / avgLoss;
            rsi[i] = 100.0 - (100.0 / (1.0 + rs));
        } else {
            rsi[i] = 100.0;
        }
    }
    return rsi;
}

TechnicalAnalysis::MACDResult TechnicalAnalysis::calculateMACD(const std::vector<KBar>& kbars, int fastPeriod, int slowPeriod, int signalPeriod) {
    MACDResult res;
    size_t n = kbars.size();
    res.dif.resize(n, 0.0);
    res.dea.resize(n, 0.0);
    res.histogram.resize(n, 0.0);

    auto emaFast = calculateEMA(kbars, fastPeriod);
    auto emaSlow = calculateEMA(kbars, slowPeriod);

    for (size_t i = 0; i < n; ++i) {
        res.dif[i] = emaFast[i] - emaSlow[i];
    }

    // 計算 DEA (DIF 的 EMA)
    double multiplier = 2.0 / (signalPeriod + 1.0);
    res.dea[0] = res.dif[0];
    for (size_t i = 1; i < n; ++i) {
        res.dea[i] = (res.dif[i] - res.dea[i - 1]) * multiplier + res.dea[i - 1];
        res.histogram[i] = (res.dif[i] - res.dea[i]) * 2.0;
    }
    return res;
}

TechnicalAnalysis::KDResult TechnicalAnalysis::calculateKD(const std::vector<KBar>& kbars, int period) {
    KDResult res;
    size_t n = kbars.size();
    res.k.resize(n, 50.0);
    res.d.resize(n, 50.0);

    if (n < static_cast<size_t>(period)) return res;

    for (size_t i = period - 1; i < n; ++i) {
        double highest = kbars[i].high;
        double lowest = kbars[i].low;
        for (size_t j = i - period + 1; j <= i; ++j) {
            highest = std::max(highest, kbars[j].high);
            lowest = std::min(lowest, kbars[j].low);
        }

        double rsv = 50.0;
        if (highest != lowest) {
            rsv = (kbars[i].close - lowest) / (highest - lowest) * 100.0;
        }

        double prevK = (i > 0) ? res.k[i - 1] : 50.0;
        double prevD = (i > 0) ? res.d[i - 1] : 50.0;

        res.k[i] = (2.0 / 3.0) * prevK + (1.0 / 3.0) * rsv;
        res.d[i] = (2.0 / 3.0) * prevD + (1.0 / 3.0) * res.k[i];
    }
    return res;
}

TechnicalAnalysis::BBResult TechnicalAnalysis::calculateBollingerBands(const std::vector<KBar>& kbars, int period, double multiplier) {
    BBResult res;
    size_t n = kbars.size();
    res.upper.resize(n, 0.0);
    res.middle.resize(n, 0.0);
    res.lower.resize(n, 0.0);

    auto sma = calculateSMA(kbars, period);
    res.middle = sma;

    for (size_t i = period - 1; i < n; ++i) {
        double mean = sma[i];
        double sumSq = 0.0;
        for (size_t j = i - period + 1; j <= i; ++j) {
            double diff = kbars[j].close - mean;
            sumSq += diff * diff;
        }
        double stdDev = std::sqrt(sumSq / period);
        res.upper[i] = mean + multiplier * stdDev;
        res.lower[i] = mean - multiplier * stdDev;
    }
    return res;
}

std::string TechnicalAnalysis::detectPattern(const std::vector<KBar>& kbars, size_t index) {
    if (index == 0 || index >= kbars.size()) return "標準K線";

    const auto& curr = kbars[index];
    const auto& prev = kbars[index - 1];

    double body = std::abs(curr.close - curr.open);
    double range = curr.high - curr.low;
    double upperShadow = curr.high - std::max(curr.open, curr.close);
    double lowerShadow = std::min(curr.open, curr.close) - curr.low;

    // 錘子線 Hammer
    if (range > 0 && lowerShadow >= 2.0 * body && upperShadow <= 0.2 * body) {
        return "錘子線 (Hammer 止跌看漲)";
    }
    // 看漲吞噬 Bullish Engulfing
    if (prev.close < prev.open && curr.close > curr.open &&
        curr.close >= prev.open && curr.open <= prev.close) {
        return "看漲吞噬 (Bullish Engulfing)";
    }
    // 看跌吞噬 Bearish Engulfing
    if (prev.close > prev.open && curr.close < curr.open &&
        curr.open >= prev.close && curr.close <= prev.open) {
        return "看跌吞噬 (Bearish Engulfing)";
    }
    // 多方砲 / 強勢紅K
    if (curr.close > curr.open && (curr.close - curr.open) / curr.open >= 0.04) {
        return "長紅突破 (Long White Candle)";
    }

    return "常規型態";
}

TechnicalIndicators TechnicalAnalysis::getLatestIndicators(const std::vector<KBar>& kbars) {
    TechnicalIndicators ti;
    if (kbars.empty()) return ti;

    size_t n = kbars.size();
    auto ma5 = calculateSMA(kbars, 5);
    auto ma20 = calculateSMA(kbars, 20);
    auto ma60 = calculateSMA(kbars, 60);
    auto rsi = calculateRSI(kbars, 14);
    auto macd = calculateMACD(kbars);
    auto kd = calculateKD(kbars);
    auto bb = calculateBollingerBands(kbars);

    ti.ma5 = ma5[n - 1];
    ti.ma20 = ma20[n - 1];
    ti.ma60 = ma60[n - 1];
    ti.rsi14 = rsi[n - 1];
    ti.macdDIF = macd.dif[n - 1];
    ti.macdDEA = macd.dea[n - 1];
    ti.macdHist = macd.histogram[n - 1];
    ti.kdK = kd.k[n - 1];
    ti.kdD = kd.d[n - 1];
    ti.bbUpper = bb.upper[n - 1];
    ti.bbMiddle = bb.middle[n - 1];
    ti.bbLower = bb.lower[n - 1];
    ti.patternName = detectPattern(kbars, n - 1);

    return ti;
}

} // namespace TaiwanQuant
