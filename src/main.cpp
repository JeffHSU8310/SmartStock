#include "core/types.hpp"
#include "data/storage_engine.hpp"
#include "technical/indicators.hpp"
#include "strategy/robot_selector.hpp"
#include "backtest/backtest_engine.hpp"
#include "notification/telegram_bot.hpp"

#include <iostream>
#include <iomanip>
#include <vector>
#include <string>
#include <cstdlib>

#ifdef _WIN32
#include <windows.h>
#include <shellapi.h>
#endif

using namespace TaiwanQuant;

void printHeader() {
    std::cout << "========================================================\n"
              << "  🇹🇼 台灣智慧機器人選股與回測系統 (TaiwanSmartQuant v2.0 GUI)\n"
              << "  覆蓋市場: 上市(TWSE) | 上櫃(TPEX) | 台指期貨/選擇權(TAIFEX)\n"
              << "========================================================\n" << std::flush;
}

void launchGUIWindow() {
    std::cout << "\n🚀 [GUI 模式開啟中] 正在啟動炫彩高階視窗介面...\n" << std::flush;
    #ifdef _WIN32
    // 自動開啟 Windows 高階視窗載入炫彩 GUI index.html
    char cwd[MAX_PATH];
    GetCurrentDirectoryA(MAX_PATH, cwd);
    std::string htmlPath = std::string(cwd) + "\\gui\\index.html";
    ShellExecuteA(NULL, "open", htmlPath.c_str(), NULL, NULL, SW_SHOWNORMAL);
    #endif
}

int main() {
    #ifdef _WIN32
    SetConsoleOutputCP(65001);
    SetConsoleCP(65001);
    system("chcp 65001 > nul");
    #endif

    StorageEngine storage;
    storage.generateSampleData(); // 載入數據庫

    RobotSelector robot(storage);
    BacktestEngine backtester(storage);
    TelegramBot tgBot;

    printHeader();

    // 預設自動啟動 GUI 炫彩視覺視窗介面
    launchGUIWindow();

    std::cout << "\n軟體已於 GUI 視窗中運行，亦可於主控制台輸入選單代碼 [1-6] 控制：\n";
    std::cout << "1. 📊 打開 GUI 看盤大廳\n"
              << "2. 🤖 執行智慧機器人選股\n"
              << "3. 📈 執行 C++ 回測引擎\n"
              << "4. 🛠️ 數據資料庫 CRUD 管理\n"
              << "5. 📱 測試 Telegram 手機推播\n"
              << "6. ❌ 關閉系統\n";

    int choice = 0;
    while (true) {
        std::cout << "\n請選擇指令 [1-6]: " << std::flush;
        if (!(std::cin >> choice)) {
            break;
        }

        if (choice == 1) {
            launchGUIWindow();
        } else if (choice == 2) {
            std::cout << "\n=================== 智慧機器人選股結果 ===================\n";
            auto signals = robot.runSmartSelection();
            for (const auto& sig : signals) {
                std::cout << "標的: " << sig.name << " (" << sig.symbol << ")\n"
                          << "評分: " << sig.score << " 分 | 建議: [" << sig.type << "]\n"
                          << "詳情: " << sig.reason << "\n"
                          << "------------------------------------------------------------\n";
                if (sig.type == "BUY") {
                    tgBot.sendSignalNotification(sig);
                }
            }
        } else if (choice == 3) {
            std::cout << "\n=================== C++ 策略回測引擎 ===================\n";
            auto result = backtester.runBacktest("2330.TW", 1000000.0);
            std::cout << "策略名稱: " << result.strategyName << "\n"
                      << "總報酬率: " << result.totalReturn << " %\n"
                      << "年化報酬: " << result.annualizedReturn << " %\n"
                      << "勝率    : " << result.winRate << " %\n"
                      << "最大回撤: " << result.maxDrawdown << " %\n"
                      << "夏普比率: " << result.sharpeRatio << "\n";
            tgBot.sendBacktestReport(result);
        } else if (choice == 4) {
            std::cout << "\n=================== 數據 CRUD 管理 ===================\n";
            FundamentalData fund{"2330.TW", "2026-07-31", 230000.0, 8.5, 22.0, 42.0, 22.1, 5.5, 30.0, 18.0, 55.0, 3.2};
            storage.saveFundamental(fund);
            std::cout << "✅ [修改成功] 已更新 台積電(2330.TW) 最新基本面數據！\n";
        } else if (choice == 5) {
            Signal testSig{"2330.TW", "台積電", MarketType::TWSE_STOCK, "2026-07-31 13:30:00", "BUY", 92.5, "四大面多頭共振，籌碼三大法人同步大買！", 1020.0};
            tgBot.sendSignalNotification(testSig);
        } else if (choice == 6) {
            std::cout << "\n系統安全關閉中...\n";
            break;
        }
    }

    return 0;
}
