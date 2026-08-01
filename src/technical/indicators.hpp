#pragma once
#include "../core/types.hpp"
#include <vector>

namespace SmartStock {

class TechnicalEngine {
public:
    // 計算簡單移動平均線 (SMA)
    static std::vector<double> calculateSMA(const std::vector<double>& prices, int period);

    // 計算指數移動平均線 (EMA)
    static std::vector<double> calculateEMA(const std::vector<double>& prices, int period);

    // 計算相對強弱指標 (RSI)
    static std::vector<double> calculateRSI(const std::vector<double>& prices, int period = 14);

    // 計算 MACD (Fast=12, Slow=26, Signal=9)
    static void calculateMACD(const std::vector<double>& prices,
                              std::vector<double>& outMACD,
                              std::vector<double>& outSignal,
                              std::vector<double>& outHist);

    // 計算 KD 指標 (Stochastic Oscillator: N=9, M1=3, M2=3)
    static void calculateKD(const std::vector<KBar>& kbars,
                            std::vector<double>& outK,
                            std::vector<double>& outD);

    // 識別 K 線形態 (例如: 看漲吞噬 Bullish Engulfing, 錘子強撐 Hammer, 長紅突破)
    static std::string detectPattern(const std::vector<KBar>& kbars);
};

} // namespace SmartStock
