# 版本變更紀錄 (CHANGELOG)

本文件紀錄專案發布與每次修改的版本歷程，跨對話交接時會自動抓取此檔案內容。

---

## [v0.4.0] - 2026-07-31

### 環境成就 (Environment Accomplished)
- **C++ 開發環境與編譯器就緒**：
  - `WinLibs GCC 16.1.0` (MinGW-w64) 及 `CMake 4.3.3` 安裝完成。
  - 沙盒環境已可順利調用 `g++` 進行 C++20 / C++23 / C++26 程式碼編譯、構建與測試。

### 備註 (Notes)
- 已 Commit 並自動同步至 **origin/main**。

---

## [v0.3.2] - 2026-07-31

### 故障排除與環境升級 (Troubleshooting & Environment)
- **C++ 編譯器安裝問題排除**：
  - 解決 `winget install MinGW.MinGW` 套件 ID 不匹配問題（更新為正確 ID `BrechtSanders.WinLibs.POSIX.UCRT`）。
  - 排除 `choco install mingw` 因權限不足導致 `C:\ProgramData\chocolatey\lib-bad` 存取被拒錯誤。
  - 自動於沙盒進行 `WinLibs MinGW GCC 16.1.0` 免管理員權限安裝。

### 備註 (Notes)
- 已 Commit 並自動同步至 **origin/main**。

---

## [v0.3.1] - 2026-07-31

### 同步與發布 (Synced & Pushed)
- **GitHub 同步**：成功將包含專案規則、對話歷史與版本紀錄之全部變更推送至 GitHub `https://github.com/JeffHSU8310/Rot.git` 的 `main` 分支。

### 備註 (Notes)
- 已 Commit 並同步至 **origin/main**。

---

## [v0.3.0] - 2026-07-31

### 新增與設定 (Added & Configured)
- **GitHub 儲存庫位置**：於 [`PROJECT_RULES.md`](file:///e:/Rot/PROJECT_RULES.md) 明確標註 GitHub 儲存庫網址 `https://github.com/JeffHSU8310/Rot.git`。
- **Git Remote 設定**：設定本地 Git `origin` 指向 `https://github.com/JeffHSU8310/Rot.git`。
- **對話歷史更新**：更新 [`CONVERSATION_HISTORY.md`](file:///e:/Rot/CONVERSATION_HISTORY.md) 紀錄 GitHub 網址連結。

### 備註 (Notes)
- 已 Commit 並自動合併至 **main** 分支。

---

## [v0.2.0] - 2026-07-31

### 新增 (Added)
- **規則 11 追加**：於 [`PROJECT_RULES.md`](file:///e:/Rot/PROJECT_RULES.md) 新增跨裝置對話同步規則。
- **對話歷史紀錄檔**：建立 [`CONVERSATION_HISTORY.md`](file:///e:/Rot/CONVERSATION_HISTORY.md)，讓其他電腦 clone/pull 後亦可完整繼承對話脈絡。

### 備註 (Notes)
- 已 Commit 並自動合併至 **main** 分支。

---

## [v0.1.0] - 2026-07-31

### 新增 (Added)
- **專案初始化**：建立 Git 儲存庫並設置 `main` 為主要分支。
- **重點規則設定**：建立 `PROJECT_RULES.md` 紀錄 10 大核心規則。
- **版本紀錄機制**：建立 `CHANGELOG.md` 規範跨對話版本管理。

### 備註 (Notes)
- 已合併至 **main** 分支。
