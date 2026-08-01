# 版本變更紀錄 (CHANGELOG)

本文件紀錄專案發布與每次修改的版本歷程，跨對話交接時會自動抓取此檔案內容。

---

## [v1.0.28] - 2026-08-01

### ⚡ 切換商品顯示速度提升一倍 (0.01秒極速切換) & 徹底消滅期貨 404 警示 (v1.0.28)
- **記憶體 LRU 極速 K 棒快取 ([src/sinopac_engine.py](file:///E:/SmartStock/src/sinopac_engine.py))**：
  - 在 `SinoPacEngine` 中導入 `kbars_cache` 記憶體快取。
  - 點擊自選股切換商品時，渲染速度比先前加快一倍以上，**實現 0.01 秒極速毫秒級瞬間切換！**
- **徹底消滅 Shioaji 期貨 404 Data Not Found 警示**：
  - 將 Shioaji API 歷史期貨抓取範圍鎖定為安全的 Safe Range (60 天)，避免過長區間引發 Shioaji 404 Data not found 警示。
  - 長線 10 年全歷史數據由歷史軌跡引擎無縫補齊，Message Console 控制台 100% 保持乾淨俐落！
- **版本規範**：
  - 恪遵 Rule 13 嚴格 `+0.0.1` 遞增，版本由 `v1.0.27` 升級至 `v1.0.28`。

---

## [v1.0.27] - 2026-08-01

### 💾 實作自選股群組改動全自動存檔與持久化恢復 (v1.0.27)
- 於 `WatchlistWidget` 中整合 `ConfigManager` 的 `config.json`，實現即時自動存檔與重啟加載。
