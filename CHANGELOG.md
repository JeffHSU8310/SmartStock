# 版本變更紀錄 (CHANGELOG)

本文件紀錄專案發布與每次修改的版本歷程，跨對話交接時會自動抓取此檔案內容。

---

## [v1.0.36] - 2026-08-02

### 🎯 跨 AI 模型 (Claude / GPT / Gemini 等) 無條件自動讀取與恪遵專案規則規範 (v1.0.36)
- **新增專案重點規則 Rule 21 ([PROJECT_RULES.md](file:///E:/SmartStock/PROJECT_RULES.md))**：
  - 不論切換或使用哪一個 AI 模型（包含 Claude、GPT、Gemini 等所有模型），開啟對話與執行任務時都必須自動讀取 `PROJECT_RULES.md` 專案重點規則，並無條件嚴格遵守專案所有 22 項規則。
- **版本規範**：
  - 版號升級至 v1.0.36，嚴格遵守 Rule 13 (+0.0.1)。

---

## [v1.0.35] - 2026-08-02

### 🎯 下單帳戶預設虛擬帳號 + 左側面板欄寬自動伸縮 (v1.0.35)
- **下單帳戶預設為虛擬帳號 ([src/widgets/order_toolbar.py](file:///E:/SmartStock/src/widgets/order_toolbar.py))**：
  - 啟動時下單帳戶 ComboBox 預設選擇「🟡 智慧模擬/虛擬交易帳戶 (Paper Trading)」，避免誤操作實盤帳戶。
- **左側面板欄寬全自動伸縮 ([src/widgets/watchlist_widget.py](file:///E:/SmartStock/src/widgets/watchlist_widget.py), [src/widgets/five_bids_widget.py](file:///E:/SmartStock/src/widgets/five_bids_widget.py), [src/widgets/order_toolbar.py](file:///E:/SmartStock/src/widgets/order_toolbar.py))**：
  - 自選股表格 4 欄 (代碼/名稱/成交價/漲跌幅) 全部改為 `QHeaderView.Stretch` 隨面板拉寬自動等比伸縮。
  - 五檔委買委賣表格 4 欄亦改為逐欄 `Stretch`，確保各欄隨面板寬度自動調整。
  - 下單工具欄 GridLayout 增加 `setColumnStretch`，輸入欄位隨面板寬度自適應。
- **版本規範**：
  - 版號升級至 v1.0.35，嚴格遵守 Rule 13 (+0.0.1)。

---

## [v1.0.34] - 2026-08-01

### 🎯 全面導入 TAIFEX 官方期貨開盤參考價 (Reference Price) 漲跌計算引擎 (v1.0.34)
- **期貨開盤參考價 (Reference Price / Settlement Price) 引擎 ([src/sinopac_engine.py](file:///E:/SmartStock/src/sinopac_engine.py))**：
  - 感謝用戶專業指出！將原先誤用的 `收盤 - 開盤` 徹底廢除，更正為台灣期貨交易所 (TAIFEX) 官方標準：
    - **漲跌點數** = `最新成交價 - 開盤參考價 (Reference Price)`
    - **漲跌幅 (%)** = `(漲跌點數 / 開盤參考價) * 100%`
  - 台指期貨近月 (`TXFR1`)：前日結算參考價 `43,727.00` 點，當前價 `42,650.00` 點 ➔ 精確計算出 **`-1,077.00 點 (-2.46%)`**！
- **版本規範**：
  - 恪遵 Rule 13 嚴格 `+0.0.1` 遞增，版本由 `v1.0.33` 升級至 `v1.0.34`。

---

## [v1.0.33] - 2026-08-01

### 🎯 獨立防護 Snapshots 串流 & 登入後 100% 刷洗為 [全真實盤] (v1.0.33)
- 重構獨立防護 Snapshots 串流，連線後 100% 刷洗為 `[全真實盤]`，期貨鎖定 `TXFR1`。
