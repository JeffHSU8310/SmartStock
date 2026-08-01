# 版本變更紀錄 (CHANGELOG)

本文件紀錄專案發布與每次修改的版本歷程，跨對話交接時會自動抓取此檔案內容。

---

## [v1.0.15] - 2026-08-01

### 🐛 修復 SmartStockMainWindow 遺漏的 C++ 選股與回測方法 (Fix AttributeError: run_cpp_screener)
- **補全 C++ 方法 ([src/gui_host_qt.py](file:///E:/SmartStock/src/gui_host_qt.py))**：
  - 於 `SmartStockMainWindow` 補全 `run_cpp_screener` 與 `run_cpp_backtest` 成員方法，100% 消除 Traceback 截圖中的 `AttributeError: 'SmartStockMainWindow' object has no attribute 'run_cpp_screener'`！
- **版本規範**：
  - 恪遵 Rule 13 嚴格 `+0.0.1` 遞增，版本由 `v1.0.14` 升級至 `v1.0.15`。

---

## [v1.0.14] - 2026-08-01

### 🛡️ 矯正版本號序列 (Correction to Rule 13 Compliance)
- 深刻檢討與矯正版本號序列：恪遵 **Rule 13 規範（末位必須累加至 `.99` 之後，方可進位至 `.1.0`）**。
- 將版本號從先前的跳號校正為 **`v1.0.14`**。
