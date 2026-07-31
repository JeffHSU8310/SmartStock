# 專案跨對話脈絡紀錄 (CONVERSATION_HISTORY.md)

本文件自動同步與紀錄專案的所有重要對話需求、決策與歷程，即使將專案複製或從 GitHub (`https://github.com/JeffHSU8310/Rot.git`) 推送/拉取到**其他電腦**上開啟新對話，AI 亦能自動抓取並銜接歷史紀錄。

---

## 📜 對話紀錄歷程

### 📌 [記錄時間: 2026-07-31] - 修復指令碼錯誤與白屏，升級 Native App Mode 與離線 ECharts (v3.1.0)

- **使用者需求 (User Prompt)**:
  - 提供執行後彈出「指令碼錯誤 (Script Error)」及畫面無 CSS3 炫彩樣式變白屏之截圖，要求繼續除錯並修復為豐富色彩版面。

- **系統處理與決策 (System Action & Decision)**:
  - 診斷原因：傳統 MSHTA 預設調用舊版 IE 兼向核心，不支援 CSS3 (flex/grid/var) 與外網 CDN，造成 `echarts.min.js` 載入失敗報錯且畫面白屏。
  - **修復措施**：
    1. 於 [`src/main.cpp`](file:///e:/Rot/src/main.cpp) 升級為 **Native Chromium App Mode (`--app="file:///..."`)** 啟動模式，無 CMD 黑框、無網址列、無瀏覽器頁籤分頁，開啟純正 100% 獨立高階桌面軟體視窗。
    2. 下載並本地打包 [`gui/echarts.min.js`](file:///e:/Rot/gui/echarts.min.js)，實現 100% 離線渲染 K 線與資產權益圖，徹底解決指令碼錯誤對話框。
  - 沙盒測試：`.exe` 雙擊啟動後呈現深色玻璃質感主題，三竹看盤大廳、K 線燭台圖、選股雷達與回測圖表 100% 豐富全彩渲染成功！
  - 打包生成 [`TaiwanSmartQuant_v3.1_NativeGUI_Standalone.zip`](file:///e:/Rot/TaiwanSmartQuant_v3.1_NativeGUI_Standalone.zip)。
  - 更新 [`CHANGELOG.md`](file:///e:/Rot/CHANGELOG.md) 至 `v3.1.0` 並全數 Commit & Push 至 GitHub `main` 分支。

- **當前專案狀態**:
  - **軟體版本**: v3.1.0 (Native App Mode 獨立炫彩桌面軟體)
  - **可執行檔**: `E:\Rot\build\TaiwanSmartQuant.exe`
  - **綠色發布檔**: `E:\Rot\TaiwanSmartQuant_v3.1_NativeGUI_Standalone.zip`
  - **GitHub 狀態**: 已與 `https://github.com/JeffHSU8310/Rot.git` 遠端 `main` 完全同步。
  - **Git 分支**: main (tracking origin/main)

---

### 📌 [記錄時間: 2026-07-31] - 升級純原生 Windows 桌面軟體（無CMD黑框、無瀏覽器頁籤） (v3.0.0)

- **使用者需求 (User Prompt)**:
  - 要求 `.EXE` 檔不要用終端機 (CMD) 的方式顯示，要像一般安裝後的標準桌面軟體介面，且執行檔不要開啟網頁分頁格式。
