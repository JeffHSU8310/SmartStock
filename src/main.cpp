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

using namespace TaiwanQuant;

void printHeader() {
    std::cout << "========================================================\n"
              << "  台灣智慧機器人選股與回測系統 (TaiwanSmartQuant v1.0)\n"
              << "  覆蓋市場: 上市(TWSE) | 上櫃(TPEX) | 台指期貨/選擇權(TAIFEX)\n"
              << "========================================================\n" << std::flush;
}

void printMenu() {
    std::cout << "\n【軟體功能選單】\n"
              << "1. 查看看盤行情列表 (三竹風格看盤大廳)\n"
              << "2. 執行智慧機器人選股 (四大面綜合評分與篩選)\n"
              << "3. 執行 C++ 高效能策略回測 (Sharpe, MDD, 勝率)\n"
              << "4. 數據資料庫管理 (新增/編輯/刪除 基本面/籌碼面/K線)\n"
              << "5. 測試 Telegram 即時推播警報至手機\n"
              << "6. 結束系統\n"
              << "請選擇功能 [1-6]: " << std::flush;
}

int main() {
    StorageEngine storage;
    storage.generateSampleData(); // 載入上市/上櫃/期貨數據庫

    RobotSelector robot(storage);
    BacktestEngine backtester(storage);
    TelegramBot tgBot;

    printHeader();

    int choice = 0;
    while (true) {
        printMenu();
        if (!(std::cin >> choice)) {
            break;
        }

        if (choice == 1) {
            std::cout << "\n=================== 看盤大廳行情列表 ===================\n";
            std::cout << std::left << std::setw(12) << "代號/名稱"
                      << std::setw(18) << "市場"
                      << std::setw(10) << "最新價"
                      << std::setw(10) << "MA5"
                      << std::setw(10) << "RSI(14)"
                      << std::setw(10) << "KD(K)"
                      << std::setw(20) << "K線型態" << "\n";
            std::cout << "-----------------------------------------------------------------------------------\n";

            for (const auto& sym : storage.getAllSymbols()) {
                auto kbars = storage.getKBars(sym, PeriodType::DAILY);
                if (kbars.empty()) continue;
                auto tech = TechnicalAnalysis::getLatestIndicators(kbars);
                std::string mktStr = (sym.find(".FITX") != std::string::npos) ? "台指期貨(TAIFEX)" : "上市股票(TWSE)";

                std::cout << std::left << std::setw(12) << sym
                          << std::setw(18) << mktStr
                          << std::setw(10) << kbars.back().close
                          << std::setw(10) << static_cast<int>(tech.ma5)
                          << std::setw(10) << static_cast<int>(tech.rsi14)
                          << std::setw(10) << static_cast<int>(tech.kdK)
                          << std::setw(20) << tech.patternName << "\n";
            }
            std::cout << std::flush;
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
            std::cout << std::flush;
        } else if (choice == 3) {
            std::cout << "\n=================== C++ 策略回測引擎 ===================\n";
            std::string targetSymbol = "2330.TW";
            std::cout << "正在對 " << targetSymbol << " 進行歷史事件驅動回測...\n";
            auto result = backtester.runBacktest(targetSymbol, 1000000.0);
            
            std::cout << "策略名稱: " << result.strategyName << "\n";
            std::cout << "總報酬率: " << result.totalReturn << " %\n";
            std::cout << "年化報酬: " << result.annualizedReturn << " %\n";
            std::cout << "勝率    : " << result.winRate << " % (" << result.winningTrades << "/" << result.totalTrades << " 勝)\n";
            std::cout << "最大回撤: " << result.maxDrawdown << " %\n";
            std::cout << "夏普比率: " << result.sharpeRatio << "\n";
            std::cout << "獲利因子: " << result.profitFactor << "\n";

            tgBot.sendBacktestReport(result);
            std::cout << std::flush;
        } else if (choice == 4) {
            std::cout << "\n=================== 資料庫數據 CRUD 管理 ===================\n";
            std::cout << "1. 編輯個股基本面營收數據\n";
            std::cout << "2. 刪除指定標的數據庫快取\n";
            std::cout << "請選擇功能 [1-2]: " << std::flush;
            int subChoice = 0;
            if (std::cin >> subChoice) {
                if (subChoice == 1) {
                    FundamentalData fund{"2330.TW", "2026-07-31", 230000.0, 8.5, 22.0, 42.0, 22.1, 5.5, 30.0, 18.0, 55.0, 3.2};
                    storage.saveFundamental(fund);
                    std::cout << " [修改成功] 已更新 台積電(2330.TW) 最新月營收與基本面數據！\n";
                } else if (subChoice == 2) {
                    storage.deleteFundamental("2454.TW");
                    std::cout << " [刪除成功] 已清除 聯發科(2454.TW) 舊數據快取！\n";
                }
            }
            std::cout << std::flush;
        } else if (choice == 5) {
            std::cout << "\n=================== Telegram 即時推播測試 ===================\n";
            Signal testSig{"2330.TW", "台積電", MarketType::TWSE_STOCK, "2026-07-31 13:30:00", "BUY", 92.5, "四大面多頭共振，籌碼三大法人同步大買！", 1020.0};
            tgBot.sendSignalNotification(testSig);
            std::cout << std::flush;
        } else if (choice == 6) {
            std::cout << "\n感謝使用 台灣智慧機器人選股與回測系統，系統安全關閉中...\n" << std::flush;
            break;
        } else {
            std::cout << "無效選擇，請重新輸入。\n" << std::flush;
        }
    }

    return 0;
}
