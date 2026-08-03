#pragma once
#include "../core/types.hpp"
#include <vector>

namespace SmartStock {

class BacktestEngine {
public:
    // 執行 MA 雙均線穿透交叉回測策略 (C++ 超級算力)
    static BacktestResult runMABacktest(const std::vector<KBar>& history, int fastPeriod = 5, int slowPeriod = 20, double initialCapital = 1000000.0);

    // 通用通用高速 C++ 回測介面 (支援滑價與費率)
    static BacktestResult runFastBacktest(const std::vector<KBar>& history, int fastPeriod, int slowPeriod, double initialCapital, double feeRate, double taxRate, double slippage);
};

} // namespace SmartStock
