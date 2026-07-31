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

// ANSI 全彩控制台字型定義 (Taiwan Market Color System)
#define COLOR_RESET   "\033[0m"
#define COLOR_CYAN    "\033[1;36m"
#define COLOR_RED     "\033[1;31m"  // 上漲 / 買進 (台股紅)
#define COLOR_GREEN   "\033[1;32m"  // 下跌 / 賣出 (台股綠)
#define COLOR_YELLOW  "\033[1;33m"  // 觀望 / 金黃
#define COLOR_MAGENTA "\033[1;35m"  // 紫色亮點
#define COLOR_WHITE   "\033[1;37m"  // 亮白
#define COLOR_DIM     "\033[2;37m"  // 暗灰
#define BG_BLUE       "\033[44m\033[1;37m"
#define BG_RED        "\033[41m\033[1;37m"

void enableANSIColors() {
    #ifdef _WIN32
    SetConsoleOutputCP(65001);
    SetConsoleCP(65001);
    HANDLE hOut = GetStdHandle(STD_OUTPUT_HANDLE);
    if (hOut != INVALID_HANDLE_VALUE) {
        DWORD dwMode = 0;
        GetConsoleMode(hOut, &dwMode);
        dwMode |= ENABLE_VIRTUAL_TERMINAL_PROCESSING;
        SetConsoleMode(hOut, dwMode);
    }
    #endif
}

void printHeader() {
    std::cout << COLOR_CYAN << "========================================================\n"
              << COLOR_MAGENTA << "  🇹🇼 台灣智慧機器人選股與回測系統 (TaiwanSmartQuant v2.1)\n"
              << COLOR_CYAN << "  覆蓋市場: " << COLOR_WHITE << "上市(TWSE)" << COLOR_CYAN << " | " 
              << COLOR_WHITE << "上櫃(TPEX)" << COLOR_CYAN << " | " 
              << COLOR_WHITE << "台指期貨/選擇權(TAIFEX)\n"
              << COLOR_CYAN << "========================================================\n" << COLOR_RESET << std::flush;
}

void launchGUIWindow() {
    std::cout << "\n" << COLOR_MAGENTA << "🚀 [GUI 炫彩模式開啟中] 正在發起高階玻璃美學視窗介面...\n" << COLOR_RESET << std::flush;
    #ifdef _WIN32
    char cwd[MAX_PATH];
    GetCurrentDirectoryA(MAX_PATH, cwd);
    std::string htmlPath = std::string(cwd) + "\\gui\\index.html";
    ShellExecuteA(NULL, "open", htmlPath.c_str(), NULL, NULL, SW_SHOWNORMAL);
    #endif
}

void printMenu() {
    std::cout << "\n" << COLOR_CYAN << "【 🎨 炫彩控制台與 GUI 軟體選單 】\n" << COLOR_RESET
              << COLOR_WHITE << "1. " << COLOR_CYAN << "📊 開啟 GUI / 控制台看盤大廳 (三竹風格行情)\n"
              << COLOR_WHITE << "2. " << COLOR_RED << "🤖 執行智慧機器人選股 (四大面評分雷達)\n"
              << COLOR_WHITE << "3. " << COLOR_MAGENTA << "📈 執行 C++ 高效能策略回測 (Sharpe, MDD, 勝率)\n"
              << COLOR_WHITE << "4. " << COLOR_YELLOW << "🛠️ 數據資料庫管理 (新增/編輯/刪除 基本面/籌碼面/K線)\n"
              << COLOR_WHITE << "5. " << COLOR_GREEN << "📱 測試 Telegram 即時推播警報至手機\n"
              << COLOR_WHITE << "6. " << COLOR_DIM << "❌ 結束系統\n" << COLOR_RESET
              << COLOR_WHITE << "請選擇指令 [1-6]: " << COLOR_RESET << std::flush;
}

int main() {
    enableANSIColors();

    StorageEngine storage;
    storage.generateSampleData(); // 載入數據庫

    RobotSelector robot(storage);
    BacktestEngine backtester(storage);
    TelegramBot tgBot;

    printHeader();

    // 啟動炫彩 GUI 介面
    launchGUIWindow();

    int choice = 0;
    while (true) {
        printMenu();
        if (!(std::cin >> choice)) {
            break;
        }

        if (choice == 1) {
            std::cout << "\n" << COLOR_CYAN << "=================== 📊 看盤大廳行情列表 ===================\n" << COLOR_RESET;
            std::cout << std::left << std::setw(12) << "代號/名稱"
                      << std::setw(18) << "市場"
                      << std::setw(10) << "最新價"
                      << std::setw(10) << "MA5"
                      << std::setw(10) << "RSI(14)"
                      << std::setw(10) << "KD(K)"
                      << std::setw(20) << "K線型態" << "\n";
            std::cout << COLOR_DIM << "-----------------------------------------------------------------------------------\n" << COLOR_RESET;

            for (const auto& sym : storage.getAllSymbols()) {
                auto kbars = storage.getKBars(sym, PeriodType::DAILY);
                if (kbars.empty()) continue;
                auto tech = TechnicalAnalysis::getLatestIndicators(kbars);
                std::string mktStr = (sym.find(".FITX") != std::string::npos) ? "台指期貨(TAIFEX)" : "上市股票(TWSE)";

                std::cout << std::left << std::setw(12) << (COLOR_WHITE + sym + COLOR_RESET)
                          << std::setw(18) << (COLOR_CYAN + mktStr + COLOR_RESET)
                          << std::setw(10) << (COLOR_RED + std::to_string(static_cast<int>(kbars.back().close)) + COLOR_RESET)
                          << std::setw(10) << static_cast<int>(tech.ma5)
                          << std::setw(10) << static_cast<int>(tech.rsi14)
                          << std::setw(10) << static_cast<int>(tech.kdK)
                          << std::setw(20) << (COLOR_MAGENTA + tech.patternName + COLOR_RESET) << "\n";
            }
            std::cout << std::flush;
        } else if (choice == 2) {
            std::cout << "\n" << COLOR_RED << "=================== 🤖 智慧機器人選股結果 ===================\n" << COLOR_RESET;
            auto signals = robot.runSmartSelection();
            for (const auto& sig : signals) {
                std::string recColor = (sig.type == "BUY") ? COLOR_RED : (sig.type == "SELL" ? COLOR_GREEN : COLOR_YELLOW);
                std::cout << COLOR_WHITE << "標的: " << sig.name << " (" << sig.symbol << ")\n"
                          << COLOR_YELLOW << "評分: " << sig.score << " 分 " << COLOR_RESET << "| 建議: [" << recColor << sig.type << COLOR_RESET << "]\n"
                          << COLOR_DIM << "詳情: " << sig.reason << COLOR_RESET << "\n"
                          << COLOR_DIM << "------------------------------------------------------------\n" << COLOR_RESET;
                if (sig.type == "BUY") {
                    tgBot.sendSignalNotification(sig);
                }
            }
        } else if (choice == 3) {
            std::cout << "\n" << COLOR_MAGENTA << "=================== 📈 C++ 策略回測引擎 ===================\n" << COLOR_RESET;
            auto result = backtester.runBacktest("2330.TW", 1000000.0);
            std::cout << COLOR_WHITE << "策略名稱: " << result.strategyName << "\n"
                      << COLOR_RED << "總報酬率: " << result.totalReturn << " %\n"
                      << COLOR_RED << "年化報酬: " << result.annualizedReturn << " %\n"
                      << COLOR_GREEN << "勝率    : " << result.winRate << " %\n"
                      << COLOR_YELLOW << "最大回撤: " << result.maxDrawdown << " %\n"
                      << COLOR_CYAN << "夏普比率: " << result.sharpeRatio << COLOR_RESET << "\n";
            tgBot.sendBacktestReport(result);
        } else if (choice == 4) {
            std::cout << "\n" << COLOR_YELLOW << "=================== 數據 CRUD 管理 ===================\n" << COLOR_RESET;
            FundamentalData fund{"2330.TW", "2026-07-31", 230000.0, 8.5, 22.0, 42.0, 22.1, 5.5, 30.0, 18.0, 55.0, 3.2};
            storage.saveFundamental(fund);
            std::cout << COLOR_GREEN << "✅ [修改成功] 已更新 台積電(2330.TW) 最新基本面數據！\n" << COLOR_RESET;
        } else if (choice == 5) {
            std::cout << "\n" << COLOR_GREEN << "=================== Telegram 即時推播測試 ===================\n" << COLOR_RESET;
            Signal testSig{"2330.TW", "台積電", MarketType::TWSE_STOCK, "2026-07-31 13:30:00", "BUY", 92.5, "四大面多頭共振，籌碼三大法人同步大買！", 1020.0};
            tgBot.sendSignalNotification(testSig);
        } else if (choice == 6) {
            std::cout << "\n" << COLOR_CYAN << "感謝使用 台灣智慧機器人選股與回測系統，系統安全關閉中...\n" << COLOR_RESET;
            break;
        }
    }

    return 0;
}
