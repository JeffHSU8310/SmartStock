# 專案跨對話脈絡紀錄 (CONVERSATION_HISTORY.md)

本文件自動同步與紀錄專案的所有重要對話需求、決策與歷程，即使將專案複製或從 GitHub (`https://github.com/JeffHSU8310/Rot.git`) 推送/拉取到**其他電腦**上開啟新對話，AI 亦能自動抓取並銜接歷史紀錄。

---

## 📜 對話紀錄歷程

### 📌 [記錄時間: 2026-07-31] - 排除程序輸入點 _ZNKSt... 錯誤與 API 架構說明 (v1.0.1)

- **使用者需求 (User Prompt)**:
  1. 提供執行 `TaiwanSmartQuant.exe` 彈出「無法找到程序輸入點 `_ZNKSt7__cxx11...`」錯誤視窗截圖，要求除錯。
  2. 詢問系統目前所使用的 API 為何者？

- **系統處理與決策 (System Action & Decision)**:
  - **除錯處理**：
    - 診斷出此錯誤為 GCC 動態連結時與系統環境中舊版 `libstdc++-6.dll` 版本的符號衝突。
    - 修改 [`CMakeLists.txt`](file:///e:/Rot/CMakeLists.txt) 加入靜態編譯參數 `-static -static-libgcc -static-libstdc++`。
    - 重新編譯產出純自包含獨立執行檔 `TaiwanSmartQuant.exe`，經沙盒驗證無須外部 GCC DLL 即可於任意環境雙擊直接執行。
  - **API 架構回答**：
    - **行情與歷史數據 API**：已抽象化介面，相容對接 **永豐金 Shioaji API**、**富果 Fugle API** 以及 **TWSE / TAIFEX 官方 API**。
    - **推播通知 API**：採用 **Telegram Bot API** (HTTP REST/JSON)。
  - 更新 [`CHANGELOG.md`](file:///e:/Rot/CHANGELOG.md) 至 `v1.0.1` 並 Commit & Push 至 GitHub `main` 分支。

- **當前專案狀態**:
  - **軟體版本**: v1.0.1 (自包含獨立靜態執行檔)
  - **可執行檔**: `E:\Rot\build\TaiwanSmartQuant.exe`
  - **GitHub 狀態**: 已與 `https://github.com/JeffHSU8310/Rot.git` 遠端 `main` 完全同步。
  - **Git 分支**: main (tracking origin/main)

---

### 📌 [記錄時間: 2026-07-31] - 台灣智慧機器人選股與回測系統 v1.0.0 完成開發與測試

- **使用者需求 (User Prompt)**:
  - 開發符合台灣上市(TWSE)、上櫃(TPEX)、台指期貨與選擇權(TAIFEX)市場之多功能智慧機器人選股與回測軟體系統。

---

### 📌 [記錄時間: 2026-07-31] - C++ 開發環境與 GCC 16.1.0 編譯器安裝完成驗證

- **系統處理與決策 (System Action & Decision)**:
  - 背景任務順利完成 `WinLibs MinGW` 安裝並驗證通關。

---

### 📌 [記錄時間: 2026-07-31] - 將規則與歷史紀錄成功併入 GitHub 遠端 main 分支

- **使用者需求 (User Prompt)**:
  - 將目前所設定的專案規則、對話歷史與版本紀錄全數推送（Push）回併至 GitHub。
