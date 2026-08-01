#pragma once
#include "../core/types.hpp"
#include <vector>

namespace SmartStock {

class BacktestEngine {
public:
    // 執行 MA 雙均線穿透交叉回測策略
    static BacktestResult runMABacktest(const std::vector<KBar>& history, int fastPeriod = 5, int slowPeriod = 20, double initialCapital = 1000000.0);
};

} // namespace SmartStock
