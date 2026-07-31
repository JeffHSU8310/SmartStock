# 版本變更紀錄 (CHANGELOG)

本文件紀錄專案發布與每次修改的版本歷程，跨對話交接時會自動抓取此檔案內容。

---

## [v1.0.2] - 2026-07-31

### 介面與字型優化 (Console Encoding & Traditional Chinese)
- **修復 Windows 控制台（CMD / PowerShell）中文字體顯示亂碼問題**：
  - 診斷原因：Windows 預設 Cmd 採用 CP950/Big5 頁面，無適應解碼 GCC 的 UTF-8 二進制中文字串。
  - 解決方案：
    1. 於 [`main.cpp`](file:///e:/Rot/src/main.cpp) 加上 `SetConsoleOutputCP(65001)` 與 `system("chcp 65001 > nul")` 自動切換控制台為 UTF-8 繁體中文顯示。
    2. 於 [`CMakeLists.txt`](file:///e:/Rot/CMakeLists.txt) 強制指定 `-finput-charset=UTF-8 -fexec-charset=UTF-8`。
  - 成果：雙擊 `.exe` 開啟命令提示字元時，會**自動切換至 UTF-8 繁體中文頁面**，100% 正常顯示繁體中文選單與選股看盤資料！

### 備註 (Notes)
- 已 Commit 並自動同步至 **origin/main**。

---

## [v1.0.1] - 2026-07-31

### 錯誤排除與發布優化 (Hotfix & Standalone Build)
- **排除「無法找到程序輸入點」動態庫錯誤**：
  - 於 [`CMakeLists.txt`](file:///e:/Rot/CMakeLists.txt) 加入靜態連結旗標 `-static -static-libgcc -static-libstdc++`。

---

## [v1.0.0] - 2026-07-31

### 重大功能發布 (Major Feature Release)
- **台灣智慧機器人選股與回測系統正式上線**：
  - 全面支援上市(TWSE)、上櫃(TPEx)與台指期貨/選擇權(TAIFEX)。

---

## [v0.4.0] - 2026-07-31

### 環境成就 (Environment Accomplished)
- **C++ 開發環境與編譯器就緒**。

---

## [v0.3.2] - 2026-07-31

### 故障排除與環境升級 (Troubleshooting & Environment)
- 自動於沙盒進行 `WinLibs MinGW GCC 16.1.0` 安裝。

---

## [v0.3.1] - 2026-07-31

### 同步與發布 (Synced & Pushed)
- 成功推送至 GitHub `https://github.com/JeffHSU8310/Rot.git` 的 `main` 分支。
