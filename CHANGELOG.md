# 版本變更紀錄 (CHANGELOG)

本文件紀錄專案發布與每次修改的版本歷程，跨對話交接時會自動抓取此檔案內容。

---

## [v2.1.0] - 2026-07-31

### 全彩控制台與自包含發布打包 (ANSI Colorful Terminal & Package)
- **C++ 控制台全彩 VT100 ANSI 視覺化**：
  - 開啟 Windows 控制台 VT100 虛擬終端能力 (`ENABLE_VIRTUAL_TERMINAL_PROCESSING`)。
  - 控制台輸出採用**台灣市場專屬色彩**：上漲/買進亮**炫彩台股紅 (`\033[1;31m`)**，下跌/賣出亮**極光翡翠綠 (`\033[1;32m`)**，標題/選單亮**霓虹青 (`\033[1;36m`)**，評分亮**金黃 (`\033[1;33m`)**。
- **發布打包獨立綠色封裝 (Standalone Distribution)**：
  - 打包生成獨立免安裝綠色包 [`dist/TaiwanSmartQuant_v2.1_Standalone`](file:///e:/Rot/dist/TaiwanSmartQuant_v2.1_Standalone) 與 [`TaiwanSmartQuant_v2.1_Standalone.zip`](file:///e:/Rot/TaiwanSmartQuant_v2.1_Standalone.zip)。
  - 包含 C++ 純自包含 `.exe` 與全彩 HTML5/CSS3/JS GUI 資源，解壓即可雙擊執行全彩版軟體！

### 備註 (Notes)
- 已 Commit 並自動同步至 **origin/main**。

---

## [v2.0.0] - 2026-07-31

### 炫彩 GUI 視窗軟體重大升級 (Major GUI Release)
- **全新高階深色玻璃 (Dark Glassmorphism) 視覺介面**。

---

## [v1.0.2] - 2026-07-31

### 介面與字型優化 (Console Encoding & Traditional Chinese)
- **修復 Windows 控制台（CMD / PowerShell）中文字體顯示亂碼問題**。

---

## [v1.0.1] - 2026-07-31

### 錯誤排除與發布優化 (Hotfix & Standalone Build)
- **排除「無法找到程序輸入點」動態庫錯誤**。

---

## [v1.0.0] - 2026-07-31

### 重大功能發布 (Major Feature Release)
- **台灣智慧機器人選股與回測系統正式上線**。
