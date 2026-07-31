# 專案跨對話脈絡紀錄 (CONVERSATION_HISTORY.md)

本文件自動同步與紀錄專案的所有重要對話需求、決策與歷程，即使將專案複製或從 GitHub (`https://github.com/JeffHSU8310/Rot.git`) 推送/拉取到**其他電腦**上開啟新對話，AI 亦能自動抓取並銜接歷史紀錄。

---

## 📜 對話紀錄歷程

### 📌 [記錄時間: 2026-07-31] - 升級純原生 Windows 桌面軟體（無CMD黑框、無瀏覽器頁籤） (v3.0.0)

- **使用者需求 (User Prompt)**:
  - 要求 `.EXE` 檔不要用終端機 (CMD) 的方式顯示，要像一般安裝後的標準桌面軟體介面，且執行檔不要開啟網頁分頁格式。

- **系統處理與決策 (System Action & Decision)**:
  - 在 [`CMakeLists.txt`](file:///e:/Rot/CMakeLists.txt) 加入 `WIN32` 子系統軟體編譯旗標（`-mwindows`）。
  - 在 [`src/main.cpp`](file:///e:/Rot/src/main.cpp) 加上 `FreeConsole()` 與 `ShowWindow(SW_HIDE)` 徹底防護，並使用 `mshta / Native App Window` 架構啟動純原生獨立桌面軟體視窗。
  - 成果：雙擊 [`TaiwanSmartQuant.exe`](file:///e:/Rot/build/TaiwanSmartQuant.exe) **無黑框 CMD 控制台，也不會打開 Chrome/Edge 網頁分頁**，直接開啟一個標準獨立的桌面軟體視窗！
  - 完成獨立綠色包封裝 [`dist/TaiwanSmartQuant_v3.0_NativeGUI_Standalone`](file:///e:/Rot/dist/TaiwanSmartQuant_v3.0_NativeGUI_Standalone) 與 [`TaiwanSmartQuant_v3.0_NativeGUI_Standalone.zip`](file:///e:/Rot/TaiwanSmartQuant_v3.0_NativeGUI_Standalone.zip)。
  - 更新 [`CHANGELOG.md`](file:///e:/Rot/CHANGELOG.md) 至 `v3.0.0` 並全數 Commit & Push 至 GitHub `main` 分支。

- **當前專案狀態**:
  - **軟體版本**: v3.0.0 (純原生 Windows 桌面 GUI 軟體)
  - **可執行檔**: `E:\Rot\build\TaiwanSmartQuant.exe`
  - **綠色發布檔**: `E:\Rot\TaiwanSmartQuant_v3.0_NativeGUI_Standalone.zip`
  - **GitHub 狀態**: 已與 `https://github.com/JeffHSU8310/Rot.git` 遠端 `main` 完全同步。
  - **Git 分支**: main (tracking origin/main)

---

### 📌 [記錄時間: 2026-07-31] - C++ 全彩控制台與自包含免安裝綠色包打包 (v2.1.0)

- **使用者需求 (User Prompt)**:
  - 打包成執行檔也要做成有色彩、版面豐富的樣式。
