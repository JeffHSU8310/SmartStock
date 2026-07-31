#include "core/types.hpp"
#include "data/storage_engine.hpp"
#include "data/sinopac_cxx_bridge.hpp"
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

// C++ 掌管核心架構與計算，調用 Native GUI 視窗載入器 (帶 Shioaji 雙引擎適配)
void launchNativeDesktopApplication() {
    #ifdef _WIN32
    HWND hwndConsole = GetConsoleWindow();
    if (hwndConsole != NULL) {
        ShowWindow(hwndConsole, SW_HIDE);
        FreeConsole();
    }

    char cwd[MAX_PATH];
    GetCurrentDirectoryA(MAX_PATH, cwd);
    std::string pyScript = std::string(cwd) + "\\src\\gui_host.py";
    std::string cmdArgs = "pythonw.exe \"" + pyScript + "\"";
    
    STARTUPINFOA si;
    PROCESS_INFORMATION pi;
    ZeroMemory(&si, sizeof(si));
    si.cb = sizeof(si);
    ZeroMemory(&pi, sizeof(pi));

    if (CreateProcessA(NULL, (LPSTR)cmdArgs.c_str(), NULL, NULL, FALSE, CREATE_NO_WINDOW, NULL, NULL, &si, &pi)) {
        CloseHandle(pi.hProcess);
        CloseHandle(pi.hThread);
        return;
    }

    std::string pyCmd = "python.exe \"" + pyScript + "\"";
    if (CreateProcessA(NULL, (LPSTR)pyCmd.c_str(), NULL, NULL, FALSE, CREATE_NO_WINDOW, NULL, NULL, &si, &pi)) {
        CloseHandle(pi.hProcess);
        CloseHandle(pi.hThread);
        return;
    }
    #endif
}

#ifdef _WIN32
int WINAPI WinMain(HINSTANCE hInstance, HINSTANCE hPrevInstance, LPSTR lpCmdLine, int nCmdShow) {
    (void)hInstance; (void)hPrevInstance; (void)lpCmdLine; (void)nCmdShow;
    
    StorageEngine storage;
    storage.generateSampleData();

    SinoPacCxxBridge sinopacBridge;
    sinopacBridge.connect("SHIOAJI_KEY", "SHIOAJI_SECRET");

    launchNativeDesktopApplication();
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

    SinoPacCxxBridge sinopacBridge;
    sinopacBridge.connect("SHIOAJI_KEY", "SHIOAJI_SECRET");

    launchNativeDesktopApplication();
    return 0;
}
