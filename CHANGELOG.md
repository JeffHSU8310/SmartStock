# 版本變更紀錄 (CHANGELOG)

本文件紀錄專案發布與每次修改的版本歷程，跨對話交接時會自動抓取此檔案內容。

---

## [v1.0.8] - 2026-08-01

### 🚀 切換商品 K線資訊重置修復、8大週期 Resample、MA趨勢箭頭與一字K厚度
- **切換商品 K 線資訊徹底重置 ([src/widgets/candlestick_chart.py](file:///E:/SmartStock/src/widgets/candlestick_chart.py))**：
  - 切換自選股商品 (2330, 2317, 2454 等) 時，100% 清空 `kbars_data` 與 `dates` 舊陣列，避免殘留上一檔商品的數據與日期時間，並重新指派 `DateAxisItem`！
- **預設 [日K] 週期與按鈕選中高亮 ([src/gui_host_qt.py](file:///E:/SmartStock/src/gui_host_qt.py))**：
  - 預設切換至 `[日]` 週期，且 `[日]` 按鈕呈現高亮藍底 (`background-color: #0066FF; color: #FFFFFF;`)。
- **頂部均線趨勢箭頭顯示 ([src/widgets/candlestick_chart.py](file:///E:/SmartStock/src/widgets/candlestick_chart.py))**：
  - 即時計算並顯示當前 MA5/MA20 走勢：`MA5: 2418.50 ⬆️` (亮紅) / `MA20: 2402.00 ⬇️` (亮綠) / `➡️` (持平)。
- **自選股與五檔全真現價動態同步 ([src/gui_host_qt.py](file:///E:/SmartStock/src/gui_host_qt.py))**：
  - 每 3 秒呼叫 `refresh_realtime_quotes()`，刷新自選股表格每一檔股票的全真成交價與漲跌點，五檔報價圍繞當前最新真實現價動態計算。
- **Shioaji K 棒全週期重採樣演算法 ([src/sinopac_engine.py](file:///E:/SmartStock/src/sinopac_engine.py))**：
  - 實作 Resample Engine，將原始行情數據依 `1m`, `5m`, `15m`, `30m`, `60m`, `Day`, `Week`, `Month` 精確聚合開高低收與總成交量。
- **修復 open == close 橫線 K 棒厚度 ([src/widgets/candlestick_chart.py](file:///E:/SmartStock/src/widgets/candlestick_chart.py))**：
  - 當 `open == close` (一字/十字線) 時自動賦予標準視覺厚度矩形，防止被畫成微小橫線，並清晰高亮上下影線。
- **版本規範**：
  - 恪遵 Rule 13 嚴格 `+0.0.1` 遞增，版本由 `v1.0.7` 升級至 `v1.0.8`。

---

## [v1.0.7] - 2026-08-01

### 🛡️ 追加第 18 條核心規則：交易安全規範 (Rule 18 Added)
- **寫入 Rule 18 交易安全規範 ([PROJECT_RULES.md](file:///E:/SmartStock/PROJECT_RULES.md))**：
  - 核心規則新增第 18 條：「**交易安全規範：所有測試與測試下單一律嚴格限定於 Shioaji 模擬環境 (`simulation=True`) 或模擬帳戶，確保絕無實盤金錢下單風險！**」
