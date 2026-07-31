# 版本變更紀錄 (CHANGELOG)

本文件紀錄專案發布與每次修改的版本歷程，跨對話交接時會自動抓取此檔案內容。

---

## [v3.0.0] - 2026-07-31

### 純原生 Windows 桌面軟體重大發布 (Pure Windows Native Desktop GUI)
- **徹底移除黑框 CMD 控制台終端機 (No Console Window)**：
  - 於 [`CMakeLists.txt`](file:///e:/Rot/CMakeLists.txt) 配置 `WIN32` 子系統軟體編譯旗標（`-mwindows`）。
  - 於 [`main.cpp`](file:///e:/Rot/src/main.cpp) 加上 `FreeConsole()` 與 `ShowWindow(SW_HIDE)` 雙重防護，雙擊 `.exe` **100% 不會彈出任何黑色命令列視窗**。
- **原生獨立桌面視窗 (Native Desktop App Window)**：
  - 移除瀏覽器分頁頁籤格式，雙擊 `TaiwanSmartQuant.exe` 即可直接啟動**獨立軟體視窗（Native Window）**，就像安裝過的三竹股市、TradingView 或一般 Windows 桌面軟體一樣！
- **發布打包獨立綠色封裝 (v3.0.0 Release)**：
  - 產生獨立發布綠色壓縮包 [`TaiwanSmartQuant_v3.0_NativeGUI_Standalone.zip`](file:///e:/Rot/TaiwanSmartQuant_v3.0_NativeGUI_Standalone.zip) 與發布目錄 [`dist/TaiwanSmartQuant_v3.0_NativeGUI_Standalone`](file:///e:/Rot/dist/TaiwanSmartQuant_v3.0_NativeGUI_Standalone)。

### 備註 (Notes)
- 已 Commit 並自動同步至 **origin/main**。

---

## [v2.1.0] - 2026-07-31

### 全彩控制台與自包含發布打包 (ANSI Colorful Terminal & Package)
- **C++ 控制台全彩 VT100 ANSI 視覺化**。

---

## [v2.0.0] - 2026-07-31

### 炫彩 GUI 視窗軟體重大升級 (Major GUI Release)
- **全新高階深色玻璃 (Dark Glassmorphism) 視覺介面**。

---

## [v1.0.2] - 2026-07-31

### 介面與字型優化 (Console Encoding & Traditional Chinese)
- **修復 Windows 控制台（CMD / PowerShell）中文字體顯示亂碼問題**。

---

## [v1.0.1] - 2026-07-31

### 錯誤排除與發布優化 (Hotfix & Standalone Build)
- **排除「無法找到程序輸入點」動態庫錯誤**。

---

## [v1.0.0] - 2026-07-31

### 重大功能發布 (Major Feature Release)
- **台灣智慧機器人選股與回測系統正式上線**。
