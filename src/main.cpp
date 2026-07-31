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

// 開啟純正獨立原生桌面軟體視窗（無 CMD 黑框、無瀏覽器頁籤、全彩 CSS3 玻璃美學與 ECharts 圖表）
void launchNativeChromiumAppWindow() {
    #ifdef _WIN32
    // 1. 徹底關閉並隱藏黑框黑視窗 CMD Console
    HWND hwndConsole = GetConsoleWindow();
    if (hwndConsole != NULL) {
        ShowWindow(hwndConsole, SW_HIDE);
        FreeConsole();
    }

    // 2. 獲取當前執行檔與 GUI html 路徑
    char cwd[MAX_PATH];
    GetCurrentDirectoryA(MAX_PATH, cwd);
    std::string htmlPath = std::string(cwd) + "\\gui\\index.html";

    // 3. 原生 App 模式啟動（無網址列、無搜尋列、無瀏覽器分頁頁籤，獨立高階全彩桌面視窗）
    std::string edgeAppCmd = "msedge.exe --app=\"file:///" + std::string(cwd) + "/gui/index.html\" --window-size=1440,900";
    std::string chromeAppCmd = "chrome.exe --app=\"file:///" + std::string(cwd) + "/gui/index.html\" --window-size=1440,900";
    
    STARTUPINFOA si;
    PROCESS_INFORMATION pi;
    ZeroMemory(&si, sizeof(si));
    si.cb = sizeof(si);
    ZeroMemory(&pi, sizeof(pi));

    // 優先嘗試合併啟動 MS Edge App 獨立視窗
    if (CreateProcessA(NULL, (LPSTR)edgeAppCmd.c_str(), NULL, NULL, FALSE, 0, NULL, NULL, &si, &pi)) {
        CloseHandle(pi.hProcess);
        CloseHandle(pi.hThread);
        return;
    }

    // 次之嘗試 Chrome App 獨立視窗
    if (CreateProcessA(NULL, (LPSTR)chromeAppCmd.c_str(), NULL, NULL, FALSE, 0, NULL, NULL, &si, &pi)) {
        CloseHandle(pi.hProcess);
        CloseHandle(pi.hThread);
        return;
    }

    // 預備方案： ShellExecute 獨立顯示
    ShellExecuteA(NULL, "open", htmlPath.c_str(), NULL, NULL, SW_SHOWNORMAL);
    #endif
}

#ifdef _WIN32
int WINAPI WinMain(HINSTANCE hInstance, HINSTANCE hPrevInstance, LPSTR lpCmdLine, int nCmdShow) {
    (void)hInstance; (void)hPrevInstance; (void)lpCmdLine; (void)nCmdShow;
    
    StorageEngine storage;
    storage.generateSampleData();

    launchNativeChromiumAppWindow();
    return 0;
}
#endif

int main(int argc, char* argv[]) {
    (void)argc; (void)argv;
    #ifdef _WIN32
    HWND hwndConsole = GetConsoleWindow();
    if (hwndConsole != NULL) {
        ShowWindow(hwndConsole, SW_HIDE);
        FreeConsole();
    }
    #endif

    StorageEngine storage;
    storage.generateSampleData();

    launchNativeChromiumAppWindow();
    return 0;
}
