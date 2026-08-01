# 版本變更紀錄 (CHANGELOG)

本文件紀錄專案發布與每次修改的版本歷程，跨對話交接時會自動抓取此檔案內容。

---

## [v1.0.6] - 2026-08-01

### 📈 永豐金 Shioaji 全真字典對接、8大全週期 K線、游標懸停高亮與 DateAxis 時間軸
- **Shioaji 官方標準商品字典與全真快照 ([src/sinopac_engine.py](file:///E:/SmartStock/src/sinopac_engine.py))**：
  - 對接永豐金官方字典：`api.Contracts.Stocks` (股票), `api.Contracts.Futures` (期貨), `api.Contracts.Indices.TSE` (加權指數)。
  - 修正自選股「價格錯誤」問題，使用 `api.snapshots` 獲取真實成交價、漲跌點與漲跌幅。
- **8 大全週期 K 線切換 ([src/gui_host_qt.py](file:///E:/SmartStock/src/gui_host_qt.py))**：
  - 實現 8 大全週期切換按鈕列：`[1分]` `[5分]` `[15分]` `[30分]` `[60分]` `[日]` `[週]` `[月]`。
- **游標懸停 K 棒資訊動態高亮 ([src/widgets/candlestick_chart.py](file:///E:/SmartStock/src/widgets/candlestick_chart.py))**：
  - 綁定 `sigMouseMoved` 懸停 Listener，移至任一 K 棒時，即時於頂部高亮顯示：`日期時間 | 開高低收 | 漲跌點數 (漲跌幅%) | 成交量 (張)`。
- **X 軸 DateAxis 時間軸格式化 ([src/widgets/candlestick_chart.py](file:///E:/SmartStock/src/widgets/candlestick_chart.py))**：
  - 自訂 `DateAxisItem` 替換預設數字 index，呈現真實日期時間格式 (如 `2026-07-31` 或 `10:30`)。
- **QSS 下拉選單文字顏色修正 ([src/gui_host_qt.py](file:///E:/SmartStock/src/gui_host_qt.py))**：
  - 修正 `QComboBox` 下拉選項主題，採用高對比純白文字 (`#FFFFFF`) 與深灰背景，解決白底看不清問題。
- **版本規範**：
  - 恪遵 Rule 13 嚴格 `+0.0.1` 遞增，版本由 `v1.0.5` 升級至 `v1.0.6`。

---

## [v1.0.5] - 2026-08-01

### 🚀 永豐金 API 全真行情對接、K線切換修復、登入 Modal 與帳戶切換
- **圖片 1 提示彈窗文字高對比度修復 ([src/gui_host_qt.py](file:///E:/SmartStock/src/gui_host_qt.py))**：
  - 獨立客製化 `QMessageBox` 與 `QDialog` QSS 主題，採用高質感深灰背景 (`#16191E`) 與純白字體 (`#FFFFFF`)，徹底解決對比度看不清問題。
- **圖片 2 右上角登入/登出動態按鈕與憑證 Modal 整合 ([src/widgets/auth_dialog.py](file:///E:/SmartStock/src/widgets/auth_dialog.py), [src/utils/config_manager.py](file:///E:/SmartStock/src/utils/config_manager.py))**：
  - 移除獨立「⚙️ 憑證與系統設定」分頁。
  - 右上角改為動態連線狀態按鈕：未登入時點擊彈出原生 CA 憑證登入 Modal (`AuthDialog`)；Modal 內新增【☑️ 記憶 API Key 與憑證設定】勾選框。
