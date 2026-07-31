#ifndef TAIWAN_QUANT_ROBOT_SELECTOR_HPP
#define TAIWAN_QUANT_ROBOT_SELECTOR_HPP

#include "../core/types.hpp"
#include "../data/storage_engine.hpp"
#include "../technical/indicators.hpp"
#include <vector>
#include <string>

namespace TaiwanQuant {

class RobotSelector {
public:
    explicit RobotSelector(const StorageEngine& storage);

    // 執行全市場標的智慧機器人選股與綜合評分
    std::vector<Signal> runSmartSelection();

    // 單標的評分與訊號生成
    Signal evaluateSymbol(const std::string& symbol);

private:
    const StorageEngine& storage_;

    // 基本面評分 (0 ~ 25)
    double evaluateFundamental(const FundamentalData& fund);
    // 籌碼面評分 (0 ~ 25)
    double evaluateChip(const ChipData& chip);
    // 技術面評分 (0 ~ 30)
    double evaluateTechnical(const TechnicalIndicators& tech, double currentPrice);
    // 消息面評分 (0 ~ 20)
    double evaluateNews(const std::vector<NewsData>& newsList);
};

} // namespace TaiwanQuant

#endif // TAIWAN_QUANT_ROBOT_SELECTOR_HPP
