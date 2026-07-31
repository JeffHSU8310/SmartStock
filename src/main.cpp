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

// 隱藏黑框控制台，開啟純原生 Windows 獨立桌面軟體視窗
void launchNativeDesktopGUIWindow() {
    #ifdef _WIN32
    // 1. 徹底關閉並隱藏黑框黑視窗 CMD Console
    HWND hwndConsole = GetConsoleWindow();
    if (hwndConsole != NULL) {
        ShowWindow(hwndConsole, SW_HIDE);
        FreeConsole();
    }

    // 2. 獲取當前執行檔路徑並以原生獨立 App 視窗模式開啟 (mshta / native app host)
    char cwd[MAX_PATH];
    GetCurrentDirectoryA(MAX_PATH, cwd);
    std::string htmlPath = std::string(cwd) + "\\gui\\index.html";

    // 使用 mshta 建立純獨立原生桌面視窗 (非瀏覽器分頁，無控制台黑框)
    std::string cmdArgs = "mshta.exe \"file:///" + std::string(cwd) + "/gui/index.html\"";
    
    STARTUPINFOA si = { sizeof(si) };
    PROCESS_INFORMATION pi;
    si.dwFlags = STARTF_USESHOWWINDOW;
    si.wShowWindow = SW_SHOWMAXIMIZED;

    if (CreateProcessA(NULL, (LPSTR)cmdArgs.c_str(), NULL, NULL, FALSE, 0, NULL, NULL, &si, &pi)) {
        CloseHandle(pi.hProcess);
        CloseHandle(pi.hThread);
    } else {
        // Fallback: 獨立視窗
        ShellExecuteA(NULL, "open", htmlPath.c_str(), NULL, NULL, SW_SHOWNORMAL);
    }
    #endif
}

#ifdef _WIN32
int WINAPI WinMain(HINSTANCE hInstance, HINSTANCE hPrevInstance, LPSTR lpCmdLine, int nCmdShow) {
    (void)hInstance; (void)hPrevInstance; (void)lpCmdLine; (void)nCmdShow;
    
    StorageEngine storage;
    storage.generateSampleData();

    launchNativeDesktopGUIWindow();
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

    launchNativeDesktopGUIWindow();
    return 0;
}
