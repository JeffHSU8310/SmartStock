# 專案跨對話脈絡紀錄 (CONVERSATION_HISTORY.md)

本文件自動同步與紀錄專案的所有重要對話需求、決策與歷程，即使將專案複製或從 GitHub (`https://github.com/JeffHSU8310/Rot.git`) 推送/拉取到**其他電腦**上開啟新對話，AI 亦能自動抓取並銜接歷史紀錄。

---

## 📜 對話紀錄歷程

### 📌 [記錄時間: 2026-07-31] - C++ 全彩控制台與自包含免安裝綠色包打包 (v2.1.0)

- **使用者需求 (User Prompt)**:
  - 打包成執行檔也要做成有色彩、版面豐富的樣式。

- **系統處理與決策 (System Action & Decision)**:
  - 在 [`src/main.cpp`](file:///e:/Rot/src/main.cpp) 啟用 Windows Console VT100 虛擬終端能力 (`ENABLE_VIRTUAL_TERMINAL_PROCESSING`)。
  - 將 C++ 控制台輸出升級為**全彩 ANSI 霓虹配色系統**（紅漲/綠跌/青標題/金黃評分/紫型態）。
  - 將 C++ 自包含 `.exe` 與全彩 HTML5/CSS3/JS GUI 資源進行發布封裝，打包生成 [`dist/TaiwanSmartQuant_v2.1_Standalone`](file:///e:/Rot/dist/TaiwanSmartQuant_v2.1_Standalone) 與 [`TaiwanSmartQuant_v2.1_Standalone.zip`](file:///e:/Rot/TaiwanSmartQuant_v2.1_Standalone.zip)。
  - 更新 [`CHANGELOG.md`](file:///e:/Rot/CHANGELOG.md) 至 `v2.1.0` 並全數 Commit & Push 至 GitHub `main` 分支。

- **當前專案狀態**:
  - **軟體版本**: v2.1.0 (全彩控制台 + 炫彩 GUI 自包含獨立打包)
  - **發布壓縮包**: `E:\Rot\TaiwanSmartQuant_v2.1_Standalone.zip`
  - **發布目錄**: `E:\Rot\dist\TaiwanSmartQuant_v2.1_Standalone`
  - **GitHub 狀態**: 已與 `https://github.com/JeffHSU8310/Rot.git` 遠端 `main` 完全同步。
  - **Git 分支**: main (tracking origin/main)

---

### 📌 [記錄時間: 2026-07-31] - 台灣智慧機器人選股與回測系統 GUI v2.0.0 炫彩視窗軟體開發完成

- **使用者需求 (User Prompt)**:
  - 要求提供具備 GUI 視窗介面功能的軟體，版面要豐富且充滿色彩。
