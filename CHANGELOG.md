# 版本變更紀錄 (CHANGELOG)

本文件紀錄專案發布與每次修改的版本歷程，跨對話交接時會自動抓取此檔案內容。

---

## [v1.1.0] - 2026-08-01

### 🔥 徹底廢除全系統寫死假數據、全真 Snapshots 快照連動與 ViewBox Y軸 AutoRange
- **徹底廢除寫死假數據 mock_info ([src/sinopac_engine.py](file:///E:/SmartStock/src/sinopac_engine.py))**：
  - 100% 移除 `sinopac_engine.py` 中寫死的假數字 `mock_info` (如台積電 965元、元大高股息 100元)。
  - 全面貫通永豐金官方 `api.snapshots()` 全真快照與 `api.kbars()` 歷史 K 棒，無報價時自動根據 Shioaji 全真日 K 棒最後一筆取得最新真實成交價 (如 2330 的 2425元、0056 的 49.4元、2317 的 250.5元)。
- **自選股動態更新與消除 AttributeError ([src/widgets/watchlist_widget.py](file:///E:/SmartStock/src/widgets/watchlist_widget.py))**：
  - 廢除預設表格中寫死的假價格與假漲跌。
  - 實作 `update_quote(code, price, pct_change)`：當全真快照下載完成時，即時將真實現價寫入自選股表格與高亮漲跌顏色，徹底消除 Traceback。
- **主圖 Y 軸價格座標 AutoRange 自動重置 ([src/widgets/candlestick_chart.py](file:///E:/SmartStock/src/widgets/candlestick_chart.py))**：
  - 切換商品時，強制呼叫 `self.p1.enableAutoRange(axis='y', enable=True)` 與 `self.p1.autoRange()`，解決從高價股切換到低價股時主圖空白與大叉叉 K 棒落在視窗外面的問題。
- **版本規範**：
  - 恪遵 Rule 13 規範，由 `v1.0.9` 進位升級至 `v1.1.0`。

---

## [v1.0.9] - 2026-08-01

### 🛡️ Shioaji 期貨 TX00/TXF 合約對接與 KBars 安全型態校驗修復
- **Shioaji 期貨合約解析器升級 ([src/sinopac_engine.py](file:///E:/SmartStock/src/sinopac_engine.py))**：
  - 深入對接 Shioaji 官方期貨與指數合約架構：`api.Contracts.Futures.TXFR1` (連續熱門近一月主力合約) / `TXF` 與 `api.Contracts.Indices.TSE.IX0001` (加權指數)。
