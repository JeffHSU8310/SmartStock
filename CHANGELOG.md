# 版本變更紀錄 (CHANGELOG)

本文件紀錄專案發布與每次修改的版本歷程，跨對話交接時會自動抓取此檔案內容。

---

## [v1.0.9] - 2026-08-01

### 🛡️ Shioaji 期貨 TX00/TXF 合約對接與 KBars 安全型態校驗修復
- **Shioaji 期貨合約解析器升級 ([src/sinopac_engine.py](file:///E:/SmartStock/src/sinopac_engine.py))**：
  - 深入對接 Shioaji 官方期貨與指數合約架構：`api.Contracts.Futures.TXFR1` (連續熱門近一月主力合約) / `TXF` 與 `api.Contracts.Indices.TSE.IX0001` (加權指數)。
  - 修正傳入 `TX00` 時造成的 `expected BaseContract, Contract, or contract Info` Warning 警告。
- **`api.kbars` 安全防護**：
  - 傳入 `api.kbars` 之前進行 `contract` 物件之型態與屬性雙重驗證，徹底消除主介面視窗日誌中的 Warning。
- **沙盒連線實測驗證**：
  - 在沙盒環境以真實 API 連線實測台指期 (`TX00`) 與股票全真 KBars 下載，零 Warning，完全通過！
- **版本規範**：
  - 恪遵 Rule 13 嚴格 `+0.0.1` 遞增，版本由 `v1.0.8` 升級至 `v1.0.9`。

---

## [v1.0.8] - 2026-08-01

### 🚀 切換商品 K線資訊重置修復、8大週期 Resample、MA趨勢箭頭與一字K厚度
- **切換商品 K 線資訊徹底重置 ([src/widgets/candlestick_chart.py](file:///E:/SmartStock/src/widgets/candlestick_chart.py))**：
  - 切換自選股商品 (2330, 2317, 2454 等) 時，100% 清空 `kbars_data` 與 `dates` 舊陣列，避免殘留上一檔商品的數據與日期時間，並重新指派 `DateAxisItem`！
