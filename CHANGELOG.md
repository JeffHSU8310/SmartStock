# 版本變更紀錄 (CHANGELOG)

本文件紀錄專案發布與每次修改的版本歷程，跨對話交接時會自動抓取此檔案內容。

---

## [v1.0.7] - 2026-08-01

### 🛡️ 追加第 18 條核心規則：交易安全規範 (Rule 18 Added)
- **寫入 Rule 18 交易安全規範 ([PROJECT_RULES.md](file:///E:/SmartStock/PROJECT_RULES.md))**：
  - 核心規則新增第 18 條：「**交易安全規範：所有測試與測試下單一律嚴格限定於 Shioaji 模擬環境 (`simulation=True`) 或模擬帳戶，確保絕無實盤金錢下單風險！**」
  - 每次對話與任何程式修改均無條件遵守。
- **版本規範**：
  - 恪遵 Rule 13 嚴格 `+0.0.1` 遞增，版本由 `v1.0.6` 升級至 `v1.0.7`。

---

## [v1.0.6] - 2026-08-01

### 📈 永豐金 Shioaji 全真字典對接、8大全週期 K線、游標懸停高亮與 DateAxis 時間軸
- **Shioaji 官方標準商品字典與全真快照與 KBars 實測 ([src/sinopac_engine.py](file:///E:/SmartStock/src/sinopac_engine.py))**：
  - 對接永豐金官方字典：`api.Contracts.Stocks` (股票: 2330, 2317, 2454, 0050 等), `api.Contracts.Futures` (期貨: TX00 主力), `api.Contracts.Indices.TSE` (加權指數)。
  - **沙盒實測通過**：使用用戶授權之 API Key 與 CA 憑證，成功激活憑證 (`CA 憑證激活成功: True`) 並連線取得 3 個帳戶，下載全真日 K 與 5分 K 棒數據！
- **8 大全週期 K 線切換 ([src/gui_host_qt.py](file:///E:/SmartStock/src/gui_host_qt.py))**：
  - 實現 8 大全週期切換按鈕列：`[1分]` `[5分]` `[15分]` `[30分]` `[60分]` `[日]` `[週]` `[月]`。
