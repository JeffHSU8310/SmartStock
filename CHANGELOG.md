# 版本變更紀錄 (CHANGELOG)

本文件紀錄專案發布與每次修改的版本歷程，跨對話交接時會自動抓取此檔案內容。

---

## [v1.0.14] - 2026-08-01

### 🛡️ 矯正版本號序列 (Correction to Rule 13 Compliance)
- **校正版本號序列 ([PROJECT_RULES.md](file:///E:/SmartStock/PROJECT_RULES.md) & [gui_host_qt.py](file:///E:/SmartStock/src/gui_host_qt.py))**：
  - 深刻檢討與矯正版本號序列：恪遵 **Rule 13 規範（末位必須累加至 `.99` 之後，方可進位至 `.1.0`）**。
  - 將版本號從先前的跳號校正為 **`v1.0.14`**。

---

## [v1.0.13] - 2026-08-01

### 🐛 修正五檔元件 get_twse_tick_size 參數容錯 (Fix AttributeError: float has no startswith)
- 於 `five_bids_widget.py` 中加入 `Union[str, float]` 型態防禦，徹底消除 Traceback 中的 `AttributeError: 'float' object has no attribute 'startswith'`！

---

## [v1.0.12] - 2026-08-01

### 🛡️ 追加第 20 條核心規則：沙盒測試結果完整報告規範 (Rule 20 Added)
- 核心規則新增第 20 條。

---

## [v1.0.11] - 2026-08-01

### 🛡️ 追加第 19 條核心規則：TWSE 官方股票 vs ETF 升降單位雙軌規範 (Rule 19 Added)
- 寫入台灣證券交易所 (TWSE) 官方「一般股票 vs ETF」升降單位雙軌權威規定。
