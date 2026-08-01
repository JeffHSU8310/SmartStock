#include "core/types.hpp"
#include "technical/indicators.hpp"
#include "strategy/robot_selector.hpp"
#include "backtest/backtest_engine.hpp"
#include <cstring>
#include <iostream>

#if defined(_WIN32) || defined(_WIN64)
#define EXPORT_API __declspec(dllexport)
#else
#define EXPORT_API __attribute__((visibility("default")))
#endif

extern "C" {

// C 介面：執行選股
EXPORT_API int run_stock_selection(const SmartStock::KBar* kbars, int count, const char* code, const char* name, SmartStock::SelectionResult* outResult) {
    if (!kbars || count <= 0 || !outResult) return 0;

    std::vector<SmartStock::KBar> data(kbars, kbars + count);
    auto results = SmartStock::RobotSelector::runSelection(data, code, name);
    if (!results.empty()) {
        *outResult = results[0];
        return 1;
    }
    return 0;
}

// C 介面：執行回測
EXPORT_API void run_backtest_ma(const SmartStock::KBar* kbars, int count, int fastMA, int slowMA, double capital, SmartStock::BacktestResult* outResult) {
    if (!kbars || count <= 0 || !outResult) return;

    std::vector<SmartStock::KBar> data(kbars, kbars + count);
    *outResult = SmartStock::BacktestEngine::runMABacktest(data, fastMA, slowMA, capital);
}

// C 介面：測試 C++ 引擎版本與連線
EXPORT_API const char* get_engine_version() {
    return "SmartStock C++ Core Engine v1.0.0 (High Performance Quant)";
}

}
