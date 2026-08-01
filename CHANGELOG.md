# 版本變更紀錄 (CHANGELOG)

本文件紀錄專案發布與每次修改的版本歷程，跨對話交接時會自動抓取此檔案內容。

---

## [v1.1.3] - 2026-08-01

### 🐛 修正五檔元件 get_twse_tick_size 參數容錯 (Fix AttributeError: float has no startswith)
- **五檔元件參數型態強容錯 ([src/widgets/five_bids_widget.py](file:///E:/SmartStock/src/widgets/five_bids_widget.py))**：
  - 於 `get_twse_tick_size(code, price)` 中加入 `Union[str, float]` 型態防禦，當單獨傳入浮點數價格 (如 2425.0) 時自動完成轉譯，徹底消除 Traceback 截圖中的 `AttributeError: 'float' object has no attribute 'startswith'`！
- **主介面五檔呼叫端同步 ([src/gui_host_qt.py](file:///E:/SmartStock/src/gui_host_qt.py))**：
  - 顯式傳遞 `set_mock_bids(self.current_code, latest_price)`。
- **版本規範**：
  - 恪遵 Rule 13 嚴格 `+0.0.1` 遞增，版本由 `v1.1.2` 升級至 `v1.1.3`。

---

## [v1.1.2] - 2026-08-01

### 🛡️ 追加第 20 條核心規則：沙盒測試結果完整報告規範 (Rule 20 Added)
- **寫入 Rule 20 沙盒測試結果完整報告規範 ([PROJECT_RULES.md](file:///E:/SmartStock/PROJECT_RULES.md))**：
  - 核心規則新增第 20 條。
