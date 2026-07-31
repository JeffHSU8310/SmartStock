# 版本變更紀錄 (CHANGELOG)

本文件紀錄專案發布與每次修改的版本歷程，跨對話交接時會自動抓取此檔案內容。

---

## [v2.0.0] - 2026-07-31

### 炫彩 GUI 視窗軟體重大升級 (Major GUI Release)
- **全新高階深色玻璃 (Dark Glassmorphism) 視覺介面**：
  - **看盤大廳 (Market Dashboard)**：三竹風格彩色行情列表 + 交互式 ECharts K線圖與成交量圖表。
  - **智慧選股雷達 (Robot Selector)**：四大面（基本面/籌碼面/技術面/消息面）綜合評分雷達卡片與排行榜。
  - **C++ 回測儀表板 (Backtest Station)**：策略資產權益曲線圖 (Equity Curve)、勝率、MDD 儀表、Sharpe Ratio 展示。
  - **數據 CRUD 與推播管理**：提供數據管理表格與 Telegram Bot 手機一鍵測試發送。
- **自動化視窗啟動引導**：
  - 雙擊執行 [`TaiwanSmartQuant.exe`](file:///e:/Rot/build/TaiwanSmartQuant.exe) 將自動啟動炫彩 GUI 視窗介面。

### 備註 (Notes)
- 已 Commit 並自動同步至 **origin/main**。

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
