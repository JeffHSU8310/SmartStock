#include "robot_selector.hpp"
#include "../technical/indicators.hpp"
#include <cstring>
#include <iostream>

namespace SmartStock {

std::vector<SelectionResult> RobotSelector::runSelection(const std::vector<KBar>& marketData, const std::string& code, const std::string& name) {
    std::vector<SelectionResult> results;
    if (marketData.size() < 20) return results;

    std::vector<double> closes;
    for (const auto& kb : marketData) {
        closes.push_back(kb.close);
    }

    std::vector<double> ma5 = TechnicalEngine::calculateSMA(closes, 5);
    std::vector<double> ma20 = TechnicalEngine::calculateSMA(closes, 20);
    std::vector<double> rsi = TechnicalEngine::calculateRSI(closes, 14);
    std::string pattern = TechnicalEngine::detectPattern(marketData);

    double latestClose = closes.back();
    double latestMA5 = ma5.back();
    double latestMA20 = ma20.back();
    double latestRSI = rsi.back();
    double pctChange = (marketData.back().close - marketData[marketData.size() - 2].close) / marketData[marketData.size() - 2].close * 100.0;

    // 多頭排列與強勢條件
    if (latestClose > latestMA5 && latestMA5 > latestMA20 && latestRSI > 50.0) {
        SelectionResult res;
        strncpy(res.code, code.c_str(), sizeof(res.code) - 1);
        strncpy(res.name, name.c_str(), sizeof(res.name) - 1);
        res.close = latestClose;
        res.pct_change = pctChange;

        // 計算綜合動能分數
        double score = 70.0 + (pctChange * 2.0) + (latestRSI - 50.0) * 0.5;
        if (score > 99.0) score = 99.0;
        res.score = score;

        std::string signal = "MA多頭強撐 + " + pattern;
        strncpy(res.signal_type, signal.c_str(), sizeof(res.signal_type) - 1);

        results.push_back(res);
    }

    return results;
}

} // namespace SmartStock
