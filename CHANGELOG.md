# 版本變更紀錄 (CHANGELOG)

本文件紀錄專案發布與每次修改的版本歷程，跨對話交接時會自動抓取此檔案內容。

---

## [v1.0.6] - 2026-08-01

### 📈 永豐金 Shioaji 全真字典對接、8大全週期 K線、游標懸停高亮與 DateAxis 時間軸
- **Shioaji 官方標準商品字典與全真快照與 KBars 實測 ([src/sinopac_engine.py](file:///E:/SmartStock/src/sinopac_engine.py))**：
  - 對接永豐金官方字典：`api.Contracts.Stocks` (股票: 2330, 2317, 2454, 0050 等), `api.Contracts.Futures` (期貨: TX00 主力), `api.Contracts.Indices.TSE` (加權指數)。
  - **沙盒實測通過**：使用用戶授權之 API Key 與 CA 憑證，成功激活憑證 (`CA 憑證激活成功: True`) 並連線取得 3 個帳戶，下載全真日 K 與 5分 K 棒數據！
- **8 大全週期 K 線切換 ([src/gui_host_qt.py](file:///E:/SmartStock/src/gui_host_qt.py))**：
  - 實現 8 大全週期切換按鈕列：`[1分]` `[5分]` `[15分]` `[30分]` `[60分]` `[日]` `[週]` `[月]`。
- **游標懸停 K 棒資訊動態高亮 ([src/widgets/candlestick_chart.py](file:///E:/SmartStock/src/widgets/candlestick_chart.py))**：
  - 綁定 `sigMouseMoved` 懸停 Listener，移至任一 K 棒時，即時於頂部高亮顯示：`日期時間 | 開高低收 | 漲跌點數 (漲跌幅%) | 成交量 (張)`。
- **X 軸 DateAxis 時間軸格式化 ([src/widgets/candlestick_chart.py](file:///E:/SmartStock/src/widgets/candlestick_chart.py))**：
  - 自訂 `DateAxisItem` 替換預設數字 index，呈現真實日期時間格式 (如 `2026-07-31` 或 `10:30`)。
- **QSS 下拉選單文字顏色修正 ([src/gui_host_qt.py](file:///E:/SmartStock/src/gui_host_qt.py))**：
  - 修正 `QComboBox` 下拉選項主題，採用高對比純白文字 (`#FFFFFF`) 與深灰背景，解決白底看不清問題。
- **版本規範**：
  - 恪遵 Rule 13 嚴格 `+0.0.1` 遞增，版本升級至 `v1.0.6`。
