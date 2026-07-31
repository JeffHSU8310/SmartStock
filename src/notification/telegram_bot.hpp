#ifndef TAIWAN_QUANT_TELEGRAM_BOT_HPP
#define TAIWAN_QUANT_TELEGRAM_BOT_HPP

#include "../core/types.hpp"
#include <string>
#include <vector>

namespace TaiwanQuant {

class TelegramBot {
public:
    TelegramBot(std::string botToken = "", std::string chatId = "");

    void setCredentials(const std::string& botToken, const std::string& chatId);

    // 發送即時文字訊息至手機 Telegram
    bool sendMessage(const std::string& message) const;

    // 發送選股觸發訊號卡片
    bool sendSignalNotification(const Signal& signal) const;

    // 發送回測結果摘要
    bool sendBacktestReport(const BacktestResult& report) const;

private:
    std::string botToken_;
    std::string chatId_;
};

} // namespace TaiwanQuant

#endif // TAIWAN_QUANT_TELEGRAM_BOT_HPP
