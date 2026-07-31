# 專案跨對話脈絡紀錄 (CONVERSATION_HISTORY.md)

本文件自動同步與紀錄專案的所有重要對話需求、決策與歷程，即使將專案複製或從 GitHub (`https://github.com/JeffHSU8310/Rot.git`) 推送/拉取到**其他電腦**上開啟新對話，AI 亦能自動抓取並銜接歷史紀錄。

---

## 📜 對話紀錄歷程

### 📌 [記錄時間: 2026-07-31] - 台灣智慧機器人選股與回測系統 GUI v2.0.0 炫彩視窗軟體開發完成

- **使用者需求 (User Prompt)**:
  - 要求提供具備 GUI 視窗介面功能的軟體，版面要豐富且充滿色彩。

- **系統處理與決策 (System Action & Decision)**:
  - 建立 [implementation_plan.md](file:///C:/Users/User/.gemini/antigravity/brain/506e0e2a-f13f-414a-aaf4-76ab09578136/implementation_plan.md) 規劃炫彩深色玻璃 GUI 視覺介面與架構。
  - **完成 GUI 視窗全套實現**：
    - `gui/index.html` - 深色玻璃質感 HTML 頁面結構。
    - `gui/style.css` - 高階霓虹色彩 (紅漲/綠跌/藍光) 與玻璃霧化 CSS3 系統。
    - `gui/app.js` - ECharts K線圖、權益曲線圖與 Tab 互動邏輯。
    - `src/main.cpp` - 整合自動啟動視窗軟體進入點。
  - 沙盒編譯產出 [`TaiwanSmartQuant.exe`](file:///e:/Rot/build/TaiwanSmartQuant.exe) 並完成自動化測試。
  - 更新 [`CHANGELOG.md`](file:///e:/Rot/CHANGELOG.md) 至 `v2.0.0` 並全數 Commit & Push 至 GitHub `main` 分支。

- **當前專案狀態**:
  - **軟體版本**: v2.0.0 (炫彩 GUI 視窗軟體)
  - **可執行檔**: `E:\Rot\build\TaiwanSmartQuant.exe`
  - **GUI 網頁資源**: `E:\Rot\gui\index.html`
  - **GitHub 狀態**: 已與 `https://github.com/JeffHSU8310/Rot.git` 遠端 `main` 完全同步。
  - **Git 分支**: main (tracking origin/main)

---

### 📌 [記錄時間: 2026-07-31] - 修復 Windows 控制台繁體中文亂碼與 UTF-8 CP65001 相容性 (v1.0.2)

- **使用者需求 (User Prompt)**:
  - 要求字體顯示為繁體中文。

---

### 📌 [記錄時間: 2026-07-31] - 排除程序輸入點 _ZNKSt... 錯誤與 API 架構說明 (v1.0.1)

- **使用者需求 (User Prompt)**:
  - 要求排除輸入點錯誤視窗，並說明使用的 API。
