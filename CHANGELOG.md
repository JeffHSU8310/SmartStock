# 版本變更紀錄 (CHANGELOG)

本文件紀錄專案發布與每次修改的版本歷程，跨對話交接時會自動抓取此檔案內容。

---

## [v1.0.17] - 2026-08-01

### 🏷️ 實作官方商品中文名稱動態解析器 (get_symbol_name) (v1.0.17)
- **實作官方商品中文名稱動態解析器 ([src/sinopac_engine.py](file:///E:/SmartStock/src/sinopac_engine.py))**：
  - 新增 `get_symbol_name(code)` 方法，自動解析 00878 (國泰永續高股息)、00919 (群益台灣精選高息)、00929 (復華台灣科技優息) 與 TX00 (台指期主力) 等官方標準中文名稱。
  - 徹底解決輸入代碼顯示「股票 00878」的名稱顯示問題！
- **自選股表格與主圖連動 ([src/widgets/watchlist_widget.py](file:///E:/SmartStock/src/widgets/watchlist_widget.py) & [src/gui_host_qt.py](file:///E:/SmartStock/src/gui_host_qt.py))**：
  - 新增股票或全真快照刷新時，自選股表格與主圖頂部 100% 同步顯示正確商品名稱。
- **版本規範**：
  - 恪遵 Rule 13 嚴格 `+0.0.1` 遞增，版本由 `v1.0.16` 升級至 `v1.0.17`。

---

## [v1.0.16] - 2026-08-01

### 🚀 重構台指期貨合約對接與貫通 Pandas 金融級 3年多週期重採樣引擎 (v1.0.16)
- 修正 Shioaji 官方期貨合約存取結構：當輸入 `TX00` / `TXF` 時，精確抓取 `api.Contracts.Futures.TXF.TXFR1`（台指期主力近一）。
- 貫通 Pandas 金融級 3 年多週期 Resample 重採樣引擎。
