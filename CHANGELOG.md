# 版本變更紀錄 (CHANGELOG)

本文件紀錄專案發布與每次修改的版本歷程，跨對話交接時會自動抓取此檔案內容。

---

## [v1.1.1] - 2026-08-01

### 🛡️ 追加第 19 條核心規則：TWSE 官方股票 vs ETF 升降單位雙軌規範 (Rule 19 Added)
- **寫入 Rule 19 TWSE 升降單位規範 ([PROJECT_RULES.md](file:///E:/SmartStock/PROJECT_RULES.md))**：
  - 核心規則新增第 19 條：寫入台灣證券交易所 (TWSE) 官方「一般股票 vs ETF」升降單位雙軌權威規定（ETF 未滿 50 元跳動 0.01 元，50 元以上跳動 0.05 元；一般股票 1000 元以上跳動 5.0 元）。
  - 每次對話與任何程式修改均無條件遵守。
- **版本規範**：
  - 恪遵 Rule 13 嚴格 `+0.0.1` 遞增，版本由 `v1.1.0` 升級至 `v1.1.1`。

---

## [v1.1.0] - 2026-08-01

### 🔥 徹底廢除全系統寫死假數據、全真 Snapshots 快照連動與 ViewBox Y軸 AutoRange
- **徹底廢除寫死假數據 mock_info ([src/sinopac_engine.py](file:///E:/SmartStock/src/sinopac_engine.py))**：
  - 100% 移除 `sinopac_engine.py` 中寫死的假數字 `mock_info` (如台積電 965元、元大高股息 100元)。
