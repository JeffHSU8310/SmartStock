# 專案跨對話脈絡紀錄 (CONVERSATION_HISTORY.md)

本文件自動同步與紀錄專案的所有重要對話需求、決策與歷程，即使將專案複製或從 GitHub (`https://github.com/JeffHSU8310/Rot.git`) 推送/拉取到**其他電腦**上開啟新對話，AI 亦能自動抓取並銜接歷史紀錄。

---

## 📜 對話紀錄歷程

### 📌 [記錄時間: 2026-07-31] - 修復 Windows 控制台繁體中文亂碼與 UTF-8 CP65001 相容性 (v1.0.2)

- **使用者需求 (User Prompt)**:
  - 提供 Windows CMD 執行 `TaiwanSmartQuant.exe` 視窗顯示亂碼之截圖，要求字體顯示為**繁體中文**。

- **系統處理與決策 (System Action & Decision)**:
  - 診斷原因：Windows 預設 Cmd 採用 CP950/ANSI 頁面，無法直接渲染 UTF-8 二進制中文字串。
  - **解決方案**：
    1. 在 [`main.cpp`](file:///e:/Rot/src/main.cpp) 的入口程式加入 `SetConsoleOutputCP(65001)` 與 `system("chcp 65001 > nul")` 指令，使視窗在雙擊啟動時自動切換至 UTF-8 繁體中文 Code Page。
    2. 在 [`CMakeLists.txt`](file:///e:/Rot/CMakeLists.txt) 加入 `-finput-charset=UTF-8 -fexec-charset=UTF-8`。
  - 沙盒測試：執行 `.exe` 時繁體中文選單與選股表格 100% 清晰正常顯示。
  - 更新 [`CHANGELOG.md`](file:///e:/Rot/CHANGELOG.md) 至 `v1.0.2` 並全數 Commit & Push 至 GitHub `main` 分支。

- **當前專案狀態**:
  - **軟體版本**: v1.0.2 (控制台 UTF-8 CP65001 繁體中文適應版)
  - **可執行檔**: `E:\Rot\build\TaiwanSmartQuant.exe`
  - **GitHub 狀態**: 已與 `https://github.com/JeffHSU8310/Rot.git` 遠端 `main` 完全同步。
  - **Git 分支**: main (tracking origin/main)

---

### 📌 [記錄時間: 2026-07-31] - 排除程序輸入點 _ZNKSt... 錯誤與 API 架構說明 (v1.0.1)

- **使用者需求 (User Prompt)**:
  1. 提供執行 `TaiwanSmartQuant.exe` 彈出「無法找到程序輸入點 `_ZNKSt7__cxx11...`」錯誤視窗截圖，要求除錯。
  2. 詢問系統目前所使用的 API 為何者？

---

### 📌 [記錄時間: 2026-07-31] - 台灣智慧機器人選股與回測系統 v1.0.0 完成開發與測試

- **使用者需求 (User Prompt)**:
  - 開發符合台灣上市(TWSE)、上櫃(TPEx)、台指期貨與選擇權(TAIFEX)市場之多功能智慧機器人選股與回測軟體系統。
