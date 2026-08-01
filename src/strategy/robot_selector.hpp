#pragma once
#include "../core/types.hpp"
#include <vector>
#include <string>

namespace SmartStock {

class RobotSelector {
public:
    // AI 智慧機器人多維度篩選股票
    static std::vector<SelectionResult> runSelection(const std::vector<KBar>& marketData, const std::string& code, const std::string& name);
};

} // namespace SmartStock
