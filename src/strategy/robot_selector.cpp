#include "robot_selector.hpp"
#include <algorithm>
#include <sstream>

namespace TaiwanQuant {

RobotSelector::RobotSelector(const StorageEngine& storage)
    : storage_(storage) {}

double RobotSelector::evaluateFundamental(const FundamentalData& fund) {
    double score = 10.0; // 基礎分
    if (fund.revenueYoY > 15.0) score += 5.0;
    else if (fund.revenueYoY > 0.0) score += 2.0;

    if (fund.eps > 0.0) score += 3.0;
    if (fund.roe > 15.0) score += 4.0;
    if (fund.peRatio > 0.0 && fund.peRatio < 20.0) score += 3.0;
    return std::min(25.0, score);
}

double RobotSelector::evaluateChip(const ChipData& chip) {
    double score = 10.0;
    if (chip.foreignBuyNet > 0) score += 5.0;
    if (chip.trustBuyNet > 0) score += 5.0;
    if (chip.dealerBuyNet > 0) score += 2.0;
    if (chip.majorHoldRatio > 60.0) score += 3.0;
    return std::min(25.0, score);
}

double RobotSelector::evaluateTechnical(const TechnicalIndicators& tech, double currentPrice) {
    double score = 10.0;
    // 多頭排列
    if (tech.ma5 > tech.ma20 && tech.ma20 > tech.ma60) score += 8.0;
    // KD 黃金交叉或黃金區域
    if (tech.kdK > tech.kdD && tech.kdK < 80.0) score += 4.0;
    // MACD 柱狀體轉正
    if (tech.macdHist > 0) score += 4.0;
    // RSI 多方強勢
    if (tech.rsi14 > 50.0 && tech.rsi14 < 75.0) score += 4.0;

    return std::min(30.0, score);
}

double RobotSelector::evaluateNews(const std::vector<NewsData>& newsList) {
    if (newsList.empty()) return 10.0;
    double sum = 0.0;
    for (const auto& news : newsList) {
        sum += news.sentimentScore;
    }
    double avgSentiment = sum / newsList.size();
    double score = 10.0 + (avgSentiment * 10.0);
    return std::clamp(score, 0.0, 20.0);
}

Signal RobotSelector::evaluateSymbol(const std::string& symbol) {
    auto kbars = storage_.getKBars(symbol, PeriodType::DAILY);
    MarketType market = (symbol.find(".FITX") != std::string::npos) ? MarketType::TAIFEX_FUT : MarketType::TWSE_STOCK;

    if (kbars.empty()) {
        return Signal{symbol, symbol, market, "2026-07-31", "HOLD", 0.0, "無數據", 0.0};
    }

    double currentPrice = kbars.back().close;
    auto fund = storage_.getFundamental(symbol);
    auto chip = storage_.getChip(symbol);
    auto news = storage_.getNews(symbol);
    auto tech = TechnicalAnalysis::getLatestIndicators(kbars);

    double fundScore = evaluateFundamental(fund);
    double chipScore = evaluateChip(chip);
    double techScore = evaluateTechnical(tech, currentPrice);
    double newsScore = evaluateNews(news);

    double totalScore = fundScore + chipScore + techScore + newsScore;

    std::string type = "HOLD";
    std::ostringstream reason;
    reason << "[智慧機器人評分 " << static_cast<int>(totalScore) << " 分] ";

    if (totalScore >= 75.0) {
        type = "BUY";
        reason << "符合多頭選股條件 (基本面:" << static_cast<int>(fundScore)
               << ", 籌碼面:" << static_cast<int>(chipScore)
               << ", 技術面:" << static_cast<int>(techScore)
               << ", 消息面:" << static_cast<int>(newsScore) << ")";
        if (!tech.patternName.empty() && tech.patternName != "常規型態") {
            reason << " [K線型態: " << tech.patternName << "]";
        }
    } else if (totalScore < 40.0) {
        type = "SELL";
        reason << "綜合評分偏低，建議減碼避險";
    } else {
        type = "HOLD";
        reason << "表現平穩，持續觀察中";
    }

    return Signal{
        symbol,
        (symbol == "2330.TW") ? "台積電" : ((symbol == "TX00.FITX") ? "台指期全月" : symbol),
        market,
        kbars.back().timestamp,
        type,
        totalScore,
        reason.str(),
        currentPrice
    };
}

std::vector<Signal> RobotSelector::runSmartSelection() {
    auto symbols = storage_.getAllSymbols();
    std::vector<Signal> signals;
    for (const auto& sym : symbols) {
        signals.push_back(evaluateSymbol(sym));
    }
    // 依智慧評分降序排序
    std::sort(signals.begin(), signals.end(), [](const Signal& a, const Signal& b) {
        return a.score > b.score;
    });
    return signals;
}

} // namespace TaiwanQuant
