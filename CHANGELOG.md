# 版本變更紀錄 (CHANGELOG)

本文件紀錄專案發布與每次修改的版本歷程，跨對話交接時會自動抓取此檔案內容。

---

## [v4.0.0] - 2026-07-31

### 規則 12 追加與 C++/Python 雙引擎純原生 GUI 軟體發布 (Dual-Engine Native GUI Release)
- **寫入規則 12 於 [`PROJECT_RULES.md`](file:///e:/Rot/PROJECT_RULES.md)**：
  - 核心原則：**C++ 語言掌管核心計算與架構，Python 語言作為輔助開發（原生桌面 GUI 視窗軟體與對接）**。
- **純原生獨立桌面軟體 (Pure Native Desktop Software Window)**：
  - 採用 `pywebview` + Microsoft Edge Native Window Host 引擎，於 [`src/gui_host.py`](file:///e:/Rot/src/gui_host.py) 建立原生視窗。
  - **0 CMD 黑框** (無命令列終端機視窗)
  - **0 瀏覽器分頁 (無 Chrome/Edge 網頁分頁頁籤，無網址列，無搜尋列)**
  - **100% 純正獨立桌面應用程式視窗**！
- **全新獨立執行檔與發布綠色封裝 (v4.0.0 Release)**：
  - 打包生成單一獨立執行檔 [`dist/TaiwanSmartQuant_GUI.exe`](file:///e:/Rot/dist/TaiwanSmartQuant_GUI.exe) 與綠色封裝包 [`TaiwanSmartQuant_v4.0_NativeGUI_Standalone.zip`](file:///e:/Rot/TaiwanSmartQuant_v4.0_NativeGUI_Standalone.zip)。
  - 100% 離線渲染深色玻璃美學、三竹風格行情列表、ECharts K線圖、選股雷達與回測圖表。

### 備註 (Notes)
- 已 Commit 並自動同步至 **origin/main**。

---

## [v3.1.0] - 2026-07-31

### 原生全彩視窗修復與離線圖表整合 (Native App Window & Offline ECharts)
- 修復 MSHTA 舊版 IE 兼向導致白屏與 Script Error 問題。

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
