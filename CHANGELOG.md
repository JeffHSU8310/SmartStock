# 版本變更紀錄 (CHANGELOG)

本文件紀錄專案發布與每次修改的版本歷程，跨對話交接時會自動抓取此檔案內容。

---

## [v5.0.0] - 2026-07-31

### 五大全彩版面與 C++/Python 雙引擎重構發布 (Five Rich-Color Layout Tabs Release)
- **全新重構五大功能版面 (Five Rich-Color Layout Tabs)**：
  - **看盤大廳**：三竹股市風格列表（台股紅漲/綠跌/MA/RSI/KD/型態）+ C++ 計算之全週期 K 線燭台圖與雙副圖。
  - **智慧選股雷達**：四大面評分卡片與排行榜。
  - **C++ 回測儀表板**：資產權益曲線圖、勝率、MDD 防禦卡、Sharpe Ratio。
  - **消息面與個股重訊**：總經數據與新聞 AI 情感得分儀 (Sentiment Score)。
  - **數據 CRUD 與推播管理**：表格編輯數據（連動 C++ 數據庫）與 Telegram 一鍵測試推播。
- **純原生桌面軟體獨立打包 (v5.0.0 Release)**：
  - 打包生成獨立執行檔 [`dist/TaiwanSmartQuant_GUI.exe`](file:///e:/Rot/dist/TaiwanSmartQuant_GUI.exe) 與綠色壓縮包 [`TaiwanSmartQuant_v5.0_NativeGUI_Standalone.zip`](file:///e:/Rot/TaiwanSmartQuant_v5.0_NativeGUI_Standalone.zip)。

### 備註 (Notes)
- 已 Commit 並自動同步至 **origin/main**。

---

## [v4.1.0] - 2026-07-31

### 規則 12 細化與技術架構明確劃分 (Rule Refinement & Module Architecture)
- **細化與強調規則 12 於 [`PROJECT_RULES.md`](file:///e:/Rot/PROJECT_RULES.md)**：
  - C++ 掌管 K線圖、報價、回測、選股核心計算。
  - Python 掌管 GUI 原生視窗版面與軟體打包。

---

## [v4.0.0] - 2026-07-31

### 規則 12 追加與 C++/Python 雙引擎純原生 GUI 軟體發布 (Dual-Engine Native GUI Release)
- 追加規則 12，發布純原生視窗軟體 `TaiwanSmartQuant_GUI.exe`。
