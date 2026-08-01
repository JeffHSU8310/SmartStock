# 版本變更紀錄 (CHANGELOG)

本文件紀錄專案發布與每次修改的版本歷程，跨對話交接時會自動抓取此檔案內容。

---

## [v1.0.23] - 2026-08-01

### 🎯 實作 1:1 K 棒留白間隔 (w=0.25) & 徹底修復時間快選按鈕 (v1.0.23)
- **實作 1:1 完美留白間隔 ([src/widgets/candlestick_chart.py](file:///E:/SmartStock/src/widgets/candlestick_chart.py))**：
  - 將 K 棒半寬 `w` 定義為 `0.25`（實體寬度 `0.5`，兩棒中心距 `1.0` ➔ 留白間隔恰好為 `0.5`，**精確等於一根 K 棒的寬度！**）。
- **徹底修復時間快選按鈕 ([src/widgets/candlestick_chart.py](file:///E:/SmartStock/src/widgets/candlestick_chart.py) & [src/gui_host_qt.py](file:///E:/SmartStock/src/gui_host_qt.py))**：
  - 於 `set_view_range_months` 中移除覆蓋 X 軸的 `autoRange()` 呼叫，改為自適應可視區間 Y 軸 Range，**點擊 `6個月`, `1年`, `2年`, `5年`, `10年` 按鈕 100% 精確縮放生效！**
  - 增加快選按鈕高亮藍底選中狀態。
- **版本規範**：
  - 恪遵 Rule 13 嚴格 `+0.0.1` 遞增，版本由 `v1.0.22` 升級至 `v1.0.23`。

---

## [v1.0.22] - 2026-08-01

### 🎯 徹底根除台指期混入台積電舊數據 Bug & 雙軌期貨 K 棒對接 (v1.0.22)
- 新增 `get_futures_kbar_contract` 機制，為台指期建立專屬 42,650 點軌跡數據防線。
