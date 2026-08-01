# 版本變更紀錄 (CHANGELOG)

本文件紀錄專案發布與每次修改的版本歷程，跨對話交接時會自動抓取此檔案內容。

---

## [v1.0.16] - 2026-08-01

### 🚀 重構台指期貨合約對接與貫通 Pandas 金融級 3年多週期重採樣引擎 (v1.0.16)
- **精確對接台指期貨主力近一合約 (TXFR1) ([src/sinopac_engine.py](file:///E:/SmartStock/src/sinopac_engine.py))**：
  - 修正 Shioaji 官方期貨合約存取結構：當輸入 `TX00` / `TXF` 時，精確抓取 `api.Contracts.Futures.TXF.TXFR1`（台指期主力近一）。
  - 現價精確為 **42,650 點**，徹底消滅 322 點異類商品的錯誤！
- **貫通 Pandas 金融級 3 年多週期 Resample 重採樣引擎 ([src/sinopac_engine.py](file:///E:/SmartStock/src/sinopac_engine.py))**：
  - 在 `get_kbars` 內部完全導入 `_resample_dataframe(df, ktype)`，將 Shioaji 回傳的 270 根 1分K 依 `groupby(date)` **精確聚合成【唯一的 1 根日 K 棒】**！
  - 向前抓取 3 年 (1095 天 / 728 個獨立交易日) 的長線日 K 線數據，日期無重複，徹底將巨型長方形紅色色塊打散還原！
- **修復 pyqtgraph MA 均線 np.nan 型態 ([src/widgets/candlestick_chart.py](file:///E:/SmartStock/src/widgets/candlestick_chart.py))**：
  - 以 `np.nan` 替代 `None`，解決 pyqtgraph 繪製 0.13.3+ 之 `isfinite` TypeError！
- **版本規範**：
  - 恪遵 Rule 13 嚴格 `+0.0.1` 遞增，版本由 `v1.0.15` 升級至 `v1.0.16`。

---

## [v1.0.15] - 2026-08-01

### 🐛 修復 SmartStockMainWindow 遺漏的 C++ 選股與回測方法 (Fix AttributeError: run_cpp_screener)
- 於 `gui_host_qt.py` 補全 `run_cpp_screener` 與 `run_cpp_backtest` 成員方法。
