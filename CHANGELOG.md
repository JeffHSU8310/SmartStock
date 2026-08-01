# 版本變更紀錄 (CHANGELOG)

本文件紀錄專案發布與每次修改的版本歷程，跨對話交接時會自動抓取此檔案內容。

---

## [v1.0.19] - 2026-08-01

### 🚀 10年數據預設6個月視角、精準十字線吸附與 MACD 三層圖表重構 (v1.0.19)
- **台指期 404 Data Not Found 警示徹底修復 ([src/sinopac_engine.py](file:///E:/SmartStock/src/sinopac_engine.py))**：
  - 針對期貨商品（TX00, MX00, TM00）自動設定安全的 90 天查詢天數，解決 Shioaji API 查詢過長傳回 404 的問題，**台指期主圖不再空白**！
- **週 K / 月 K 時間標籤修正**：
  - 週 K 棒與月 K 棒時間戳修正記錄為該週/當月的第一個交易日日期（如週一 `2025-12-01`）。
- **完全對齊用戶專業圖表視覺與 MACD 副圖 ([src/widgets/candlestick_chart.py](file:///E:/SmartStock/src/widgets/candlestick_chart.py))**：
  - 重構為 Plot 1 (K棒+MA5/20/60/120)、Plot 2 (Volume)、Plot 3 (MACD DIF/DEA/Bar) 三層圖表結構。
  - 實作十字線 `x_idx = round(mouse_x)` 精準吸附每根 K 棒正中央。
  - 拉開 K 棒適當比例間距 `w = 0.32`，告別黏在一起的感覺。
- **10 年數據與 5 大時間視角快選按鈕 ([src/gui_host_qt.py](file:///E:/SmartStock/src/gui_host_qt.py))**：
  - 股票支援向 Shioaji 抓取跨越 10 年 (2500 交易日) 的全歷史數據。
  - 主圖預設顯示最新 6 個月 (120 根日K) 精美視野。
  - 新增 5 大時間快選按鈕 (`6個月`, `1年`, `2年`, `5年`, `10年`)，點擊一鍵瞬間縮放！
- **版本規範**：
  - 恪遵 Rule 13 嚴格 `+0.0.1` 遞增，版本由 `v1.0.18` 升級至 `v1.0.19`。

---

## [v1.0.18] - 2026-08-01

### 🎨 未登入前主圖保持乾淨空白，登入後載入全真數據 (v1.0.18)
- 於 `SinoPacEngine.get_kbars` 中設定：當未登入永豐金 API 時，直接傳回空清單 `[]`，主圖呈現深色乾淨空白。
