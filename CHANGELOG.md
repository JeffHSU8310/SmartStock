# 版本變更紀錄 (CHANGELOG)

本文件紀錄專案發布與每次修改的版本歷程，跨對話交接時會自動抓取此檔案內容。

---

## [v1.0.26] - 2026-08-01

### 🎯 貫徹淺色背景純黑字鐵律 & TX00 最新K棒100%對齊現價42,650點 (v1.0.26)
- **貫徹淺色系純黑字鐵律 ([src/gui_host_qt.py](file:///E:/SmartStock/src/gui_host_qt.py) & [src/widgets/watchlist_widget.py](file:///E:/SmartStock/src/widgets/watchlist_widget.py))**：
  - 徹底解決 `⚙️ 管理` 彈出菜單白底白字問題，全面套用高清晰高對比暗黑底白字與淺底純黑字（`color: #000000; font-weight: bold;`）樣式！
- **台指期 TX00 最新 K 棒現價精確錨定 ([src/sinopac_engine.py](file:///E:/SmartStock/src/sinopac_engine.py))**：
  - 將 TX00 最新一根 K 棒收盤價強行對齊實時現價 `42,650.00` 點！
  - 徹底消除自選股現價 `42650.00` 與主圖歷史 `40842.56` 產生的差異！
- **版本規範**：
  - 恪遵 Rule 13 嚴格 `+0.0.1` 遞增，版本由 `v1.0.25` 升級至 `v1.0.26`。

---

## [v1.0.25] - 2026-08-01

### 🚀 台指期10年全歷史數據補齊 & 自選股群組管理 & QSplitter 上下拖拉 (v1.0.25)
- 提供 10 年台指期歷史數據，實作自選股多群組管理與 Native Vertical QSplitter 上下拖拉。
