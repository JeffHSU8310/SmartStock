#ifndef TAIWAN_QUANT_INDICATORS_HPP
#define TAIWAN_QUANT_INDICATORS_HPP

#include "../core/types.hpp"
#include <vector>
#include <string>

namespace TaiwanQuant {

class TechnicalAnalysis {
public:
    // 移動平均線 MA
    static std::vector<double> calculateSMA(const std::vector<KBar>& kbars, int period);

    // 指數移動平均線 EMA
    static std::vector<double> calculateEMA(const std::vector<KBar>& kbars, int period);

    // 相對強弱指標 RSI
    static std::vector<double> calculateRSI(const std::vector<KBar>& kbars, int period = 14);

    // MACD (DIF, DEA, Histogram)
    struct MACDResult {
        std::vector<double> dif;
        std::vector<double> dea;
        std::vector<double> histogram;
    };
    static MACDResult calculateMACD(const std::vector<KBar>& kbars, int fastPeriod = 12, int slowPeriod = 26, int signalPeriod = 9);

    // 隨機指標 KD (Stochastic Oscillator)
    struct KDResult {
        std::vector<double> k;
        std::vector<double> d;
    };
    static KDResult calculateKD(const std::vector<KBar>& kbars, int period = 9);

    // 布林通道 Bollinger Bands
    struct BBResult {
        std::vector<double> upper;
        std::vector<double> middle;
        std::vector<double> lower;
    };
    static BBResult calculateBollingerBands(const std::vector<KBar>& kbars, int period = 20, double multiplier = 2.0);

    // K線型態識別 (Pattern Recognition)
    static std::string detectPattern(const std::vector<KBar>& kbars, size_t index);

    // 整合計算最新技術指標
    static TechnicalIndicators getLatestIndicators(const std::vector<KBar>& kbars);
};

} // namespace TaiwanQuant

#endif // TAIWAN_QUANT_INDICATORS_HPP
