#ifndef TAIWAN_QUANT_BACKTEST_ENGINE_HPP
#define TAIWAN_QUANT_BACKTEST_ENGINE_HPP

#include "../core/types.hpp"
#include "../data/storage_engine.hpp"
#include <string>
#include <vector>

namespace TaiwanQuant {

class BacktestEngine {
public:
    explicit BacktestEngine(const StorageEngine& storage);

    // 執行事件驅動策略回測
    BacktestResult runBacktest(const std::string& symbol, double initialCapital = 1000000.0);

private:
    const StorageEngine& storage_;
};

} // namespace TaiwanQuant

#endif // TAIWAN_QUANT_BACKTEST_ENGINE_HPP
