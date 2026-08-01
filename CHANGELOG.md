# 版本變更紀錄 (CHANGELOG)

本文件紀錄專案發布與每次修改的版本歷程，跨對話交接時會自動抓取此檔案內容。

---

## [v1.0.25] - 2026-08-01

### 🚀 台指期10年全歷史數據補齊 & 自選股群組管理 & QSplitter 上下拖拉 (v1.0.25)
- **台指期 10 年全歷史數據補齊 ([src/sinopac_engine.py](file:///E:/SmartStock/src/sinopac_engine.py))**：
  - 提供跨越 2016 ~ 2026 長達 10 年 (2500 筆) 台指期日 K 棒數據，完美支援 C++ 策略回測引擎進行長線回測與指標運算！
- **自選股多群組管理功能 ([src/widgets/watchlist_widget.py](file:///E:/SmartStock/src/widgets/watchlist_widget.py))**：
  - 新增群組 ComboBox 下拉選單與 ⚙️ 群組管理選單。
  - 支援 **➕ 新增群組**、**✏️ 重新命名當前群組**、**🗑️ 刪除當前群組** 與無縫資料切換！
- **週 K 棒時間戳 100% 精確週一算法**：
  - 統一對週 K 棒計算 `dt - timedelta(days=dt.weekday())`，時間標籤 100% 精確固定為週一首日日期（例如 `2026-07-27`）。
- **主圖/副圖與訊息欄 QSplitter 上下拖拉高度 ([src/widgets/candlestick_chart.py](file:///E:/SmartStock/src/widgets/candlestick_chart.py) & [src/gui_host_qt.py](file:///E:/SmartStock/src/gui_host_qt.py))**：
  - 看盤大廳右側與 K 線圖內部全面升級為原生 `QSplitter(QtCore.Qt.Vertical)`。
  - 系統廣播訊息欄預設高度減半，允許滑鼠上下拖拉任意調整與主圖的高度比例！
  - 主圖、成交量副圖與 MACD 副圖允許滑鼠上下拖拉任意調整相對高度！
- **版本規範**：
  - 恪遵 Rule 13 嚴格 `+0.0.1` 遞增，版本由 `v1.0.24` 升級至 `v1.0.25`。

---

## [v1.0.24] - 2026-08-01

### 📊 徹底修復成交量矩形牆與畫面斜線對角殘影 Bug (v1.0.24)
- 於 `BarGraphItem` 傳入 `y0=0`，成交量自 0 起算並徹底清空舊畫布對角殘影。
