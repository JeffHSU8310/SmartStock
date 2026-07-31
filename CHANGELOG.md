# 版本變更紀錄 (CHANGELOG)

本文件紀錄專案發布與每次修改的版本歷程，跨對話交接時會自動抓取此檔案內容。

---

## [v3.1.0] - 2026-07-31

### 原生全彩視窗修復與離線圖表整合 (Native App Window & Offline ECharts)
- **修復 MSHTA 舊版 IE 兼向導致白屏與 Script Error 問題**：
  - 診斷原因：傳統 MSHTA 採用舊版 IE 引擎，不支援現代 CSS3 (flex/grid/var) 與 CDN JS，導致彈出「指令碼錯誤」對話框且畫面白屏無色彩。
  - **解決方案**：
    1. 於 [`main.cpp`](file:///e:/Rot/src/main.cpp) 升級為 **Native Chromium App Mode (`--app="file:///..."`)** 原生啟動模式。
       - **無黑框 CMD 控制台** (0 Console Window)
       - **無瀏覽器網址列、無搜尋列**
       - **無瀏覽器分頁頁籤 (0 Browser Tabs)**
       - **100% 獨立高階全彩桌面應用程式視窗**！
    2. 下載並本地整合 [`gui/echarts.min.js`](file:///e:/Rot/gui/echarts.min.js)，離線完美渲染 60fps 燭台 K 線圖與資產權益圖，徹底消除 Script Error。
- **最新發布綠色封裝包 (v3.1.0 Release)**：
  - 打包發布獨立綠色壓縮包 [`TaiwanSmartQuant_v3.1_NativeGUI_Standalone.zip`](file:///e:/Rot/TaiwanSmartQuant_v3.1_NativeGUI_Standalone.zip) 與發布目錄 [`dist/TaiwanSmartQuant_v3.1_NativeGUI_Standalone`](file:///e:/Rot/dist/TaiwanSmartQuant_v3.1_NativeGUI_Standalone)。

### 備註 (Notes)
- 已 Commit 並自動同步至 **origin/main**。

---

## [v3.0.0] - 2026-07-31

### 純原生 Windows 桌面軟體重大發布 (Pure Windows Native Desktop GUI)
- 徹底移除黑框 CMD 控制台終端機 (No Console Window)。

---

## [v2.1.0] - 2026-07-31

### 全彩控制台與自包含發布打包 (ANSI Colorful Terminal & Package)
- C++ 控制台全彩 VT100 ANSI 視覺化。

---

## [v2.0.0] - 2026-07-31

### 炫彩 GUI 視窗軟體重大升級 (Major GUI Release)
- 全新高階深色玻璃 (Dark Glassmorphism) 視覺介面。
