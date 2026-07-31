# 專案跨對話脈絡紀錄 (CONVERSATION_HISTORY.md)

本文件自動同步與紀錄專案的所有重要對話需求、決策與歷程，即使將專案複製或從 GitHub (`https://github.com/JeffHSU8310/Rot.git`) 推送/拉取到**其他電腦**上開啟新對話，AI 亦能自動抓取並銜接歷史紀錄。

---

## 📜 對話紀錄歷程

### 📌 [記錄時間: 2026-07-31] - 追加規則 12，升級 C++/Python 雙引擎純原生 GUI 桌面軟體 (v4.0.0)

- **使用者需求 (User Prompt)**:
  - 反應先前檔仍會開啟網頁，要求做出真正獨立的視窗軟體。
  - **允許使用 Python 作為輔助 GUI**。
  - **要求將「C++ 掌管核心架構，Python 作為輔助」寫入專案重點規則中**。

- **系統處理與決策 (System Action & Decision)**:
  - 於 [`PROJECT_RULES.md`](file:///e:/Rot/PROJECT_RULES.md) 新增 **規則 12**（C++ 掌管核心架構，Python 為輔助 GUI 與打包）。
  - **完成 C++/Python 雙引擎 Native Window 全套實現**：
    - 撰寫 [`src/gui_host.py`](file:///e:/Rot/src/gui_host.py) 調用原生 `pywebview` / WebView2 視窗。
    - 升級 [`src/main.cpp`](file:///e:/Rot/src/main.cpp) 整合雙引擎載入機制。
    - 使用 PyInstaller 將 Python Native Host 打包為獨立執行檔 [`dist/TaiwanSmartQuant_GUI.exe`](file:///e:/Rot/dist/TaiwanSmartQuant_GUI.exe)。
  - **測試驗證**：雙擊 `TaiwanSmartQuant_GUI.exe` **無 CMD 黑框，無 Chrome/Edge 網頁分頁頁籤，直接跳出純獨立高階桌面選股軟體視窗**！
  - 打包生成 [`TaiwanSmartQuant_v4.0_NativeGUI_Standalone.zip`](file:///e:/Rot/TaiwanSmartQuant_v4.0_NativeGUI_Standalone.zip)。
  - 更新 [`CHANGELOG.md`](file:///e:/Rot/CHANGELOG.md) 至 `v4.0.0` 並全數 Commit & Push 至 GitHub `main` 分支。

- **當前專案狀態**:
  - **軟體版本**: v4.0.0 (C++ 核心 + Python 輔助純原生 GUI 桌面軟體)
  - **獨立GUI執行檔**: `E:\Rot\dist\TaiwanSmartQuant_GUI.exe`
  - **C++核心執行檔**: `E:\Rot\build\TaiwanSmartQuant.exe`
  - **發布綠色壓縮包**: `E:\Rot\TaiwanSmartQuant_v4.0_NativeGUI_Standalone.zip`
  - **GitHub 狀態**: 已與 `https://github.com/JeffHSU8310/Rot.git` 遠端 `main` 完全同步。
  - **Git 分支**: main (tracking origin/main)

---

### 📌 [記錄時間: 2026-07-31] - 修復指令碼錯誤與白屏，升級 Native App Mode 與離線 ECharts (v3.1.0)

- **使用者需求 (User Prompt)**:
  - 反應指令碼錯誤與白屏，要求繼續除錯。
