#include "telegram_bot.hpp"
#include <iostream>
#include <sstream>

namespace TaiwanQuant {

TelegramBot::TelegramBot(std::string botToken, std::string chatId)
    : botToken_(std::move(botToken)), chatId_(std::move(chatId)) {}

void TelegramBot::setCredentials(const std::string& botToken, const std::string& chatId) {
    botToken_ = botToken;
    chatId_ = chatId;
}

bool TelegramBot::sendMessage(const std::string& message) const {
    std::cout << "\n[TelegramBot 即時推播模組 - 模擬發送中...]" << std::endl;
    std::cout << "----------------------------------------" << std::endl;
    std::cout << "接收目標 (Chat ID): " << (chatId_.empty() ? "未設定 (預設手機頻道)" : chatId_) << std::endl;
    std::cout << "內容:\n" << message << std::endl;
    std::cout << "----------------------------------------" << std::endl;
    return true;
}

bool TelegramBot::sendSignalNotification(const Signal& signal) const {
    std::ostringstream oss;
    oss << "🚨 【台灣智慧機器人選股即時警報】🚨\n"
        << "📌 標的: " << signal.name << " (" << signal.symbol << ")\n"
        << "🏛️ 市場: " << marketTypeToString(signal.market) << "\n"
        << "⏱️ 時間: " << signal.timestamp << "\n"
        << "🎯 訊號: " << (signal.type == "BUY" ? "🟢 買進突破" : (signal.type == "SELL" ? "🔴 賣出避險" : "🟡 觀望")) << "\n"
        << "💰 觸發價格: $" << signal.triggerPrice << "\n"
        << "📊 綜合得分: " << signal.score << " 分\n"
        << "📝 理由: " << signal.reason;
    return sendMessage(oss.str());
}

bool TelegramBot::sendBacktestReport(const BacktestResult& report) const {
    std::ostringstream oss;
    oss << "📊 【C++ 策略回測績效報告】📊\n"
        << "策略名稱: " << report.strategyName << "\n"
        << "----------------------------------------\n"
        << "📈 總報酬率: " << report.totalReturn << " %\n"
        << "⚡ 年化報酬率: " << report.annualizedReturn << " %\n"
        << "🎯 交易勝率: " << report.winRate << " % (" << report.winningTrades << "/" << report.totalTrades << " 勝)\n"
        << "🛡️ 最大回撤 (MDD): " << report.maxDrawdown << " %\n"
        << "💎 夏普比率 (Sharpe): " << report.sharpeRatio << "\n"
        << "⚖️ 獲利因子 (Profit Factor): " << report.profitFactor;
    return sendMessage(oss.str());
}

} // namespace TaiwanQuant
