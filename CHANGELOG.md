# 版本變更紀錄 (CHANGELOG)

本文件紀錄專案發布與每次修改的版本歷程，跨對話交接時會自動抓取此檔案內容。

---

## [v1.0.21] - 2026-08-01

### 📏 K 棒間距再拉開一倍與視野大擴張 (v1.0.21)
- **視覺間距拉開 100% ([src/widgets/candlestick_chart.py](file:///E:/SmartStock/src/widgets/candlestick_chart.py))**：
  - 將預設視野 K 棒數量由 120 根縮減為 60 根（約 60 根精選舒適寬度），K 棒間距精確拉開一倍！
  - 將 K 棒半寬 `w` 由 `0.32` 放大至 `0.38`，K 棒實體呈現飽滿立體高顏值！
- **版本規範**：
  - 恪遵 Rule 13 嚴格 `+0.0.1` 遞增，版本由 `v1.0.20` 升級至 `v1.0.21`。

---

## [v1.0.20] - 2026-08-01

### 🐛 徹底修復 NameError: name 'pd' is not defined 與視角縮放體驗優化 (v1.0.20)
- 於 `candlestick_chart.py` 補上 `import pandas as pd`，徹底消滅登入切換商品時的 NameError 崩潰。
