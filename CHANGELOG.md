# 版本變更紀錄 (CHANGELOG)

本文件紀錄專案發布與每次修改的版本歷程，跨對話交接時會自動抓取此檔案內容。

---

## [v4.1.0] - 2026-07-31

### 規則 12 細化與技術架構明確劃分 (Rule Refinement & Module Architecture)
- **細化與強調規則 12 於 [`PROJECT_RULES.md`](file:///e:/Rot/PROJECT_RULES.md)**：
  - **C++ 核心職責**：主要掌管 **K線圖計算、實時/歷史報價引擎、事件驅動策略回測、四大面智慧選股**。
  - **Python 輔助職責**：主要掌管 **GUI 原生視窗版面、炫彩視覺排版渲染與獨立軟體封裝**。
- **儲存庫與對話歷史自動同步**：
  - 更新 [`CONVERSATION_HISTORY.md`](file:///e:/Rot/CONVERSATION_HISTORY.md) 紀錄明確分工原則。

### 備註 (Notes)
- 已 Commit 並自動同步至 **origin/main**。

---

## [v4.0.0] - 2026-07-31

### 規則 12 追加與 C++/Python 雙引擎純原生 GUI 軟體發布 (Dual-Engine Native GUI Release)
- 追加規則 12，發布純原生視窗軟體 [`dist/TaiwanSmartQuant_GUI.exe`](file:///e:/Rot/dist/TaiwanSmartQuant_GUI.exe)。

---

## [v3.1.0] - 2026-07-31

### 原生全彩視窗修復與離線圖表整合 (Native App Window & Offline ECharts)
- 修復舊版指令碼錯誤，本地整合 ECharts。

---

## [v3.0.0] - 2026-07-31

### 純原生 Windows 桌面軟體重大發布 (Pure Windows Native Desktop GUI)
- 徹底移除黑框 CMD 控制台終端機。
