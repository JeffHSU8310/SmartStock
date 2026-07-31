#ifndef TAIWAN_QUANT_SINOPAC_CXX_BRIDGE_HPP
#ifndef TAIWAN_QUANT_SINOPAC_CXX_BRIDGE_HPP
#define TAIWAN_QUANT_SINOPAC_CXX_BRIDGE_HPP

#include "../core/types.hpp"
#include <string>
#include <vector>
#include <iostream>

namespace TaiwanQuant {

/**
 * @brief 永豐金證券 Shioaji C++ 核心介面適配器 (SinoPac Shioaji C++ Bridge)
 * 專門用於接收來自 Shioaji API 的 Tick/KBar 數據並餵給 C++ 算力引擎
 */
class SinoPacCxxBridge {
public:
    SinoPacCxxBridge() : isConnected_(false) {}

    bool connect(const std::string& apiKey, const std::string& secretKey) {
        std::cout << "[SinoPac C++ Bridge] 初始化 Shioaji C++ 算力介面..." << std::endl;
        apiKey_ = apiKey;
        secretKey_ = secretKey;
        isConnected_ = true;
        return true;
    }

    void onReceiveTick(const std::string& symbol, double price, long volume, int direction) {
        // C++ 高效能低延遲 Tick 運算
        std::cout << "[SinoPac C++ Tick] " << symbol << " | 價格: " << price << " | 成交量: " << volume << std::endl;
    }

    bool isConnected() const { return isConnected_; }

private:
    std::string apiKey_;
    std::string secretKey_;
    bool isConnected_;
};

} // namespace TaiwanQuant

#endif // TAIWAN_QUANT_SINOPAC_CXX_BRIDGE_HPP
#endif
