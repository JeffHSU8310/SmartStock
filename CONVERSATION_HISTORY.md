# 專案跨對話脈絡紀錄 (CONVERSATION_HISTORY.md)

本文件自動同步與紀錄專案的所有重要對話需求、決策與歷程，即使將專案複製或從 GitHub (`https://github.com/JeffHSU8310/SmartStock.git`) 推送/拉取到**其他電腦**上開啟新對話，AI 亦能自動抓取並銜接歷史紀錄。

---

## 📜 對話紀錄歷程

### 📌 [記錄時間: 2026-08-01] - 修復 NameError & 發布 v1.0.20 (v1.0.20)

- **使用者需求 (User Prompt)**:
  - 提供 `NameError: name 'pd' is not defined` 追蹤日誌。
  - Clarify 時間快選按鈕語意：6個月為顯示近 6 個月視野，放大縮小移動可滑動至更久的 10 年歷史資料。

- **系統處理與決策 (System Action & Decision)**:
  - 於 [`src/widgets/candlestick_chart.py`](file:///E:/SmartStock/src/widgets/candlestick_chart.py) 補上 `import pandas as pd` 徹底消滅 NameError。
  - 精確鎖定快選按鈕 `set_view_range_months` 為 X 軸視角平滑縮放，完全保留底層 10 年數據供使用者自由滾動與檢視。
  - 沙盒測試通過，Commit 並 Push 至 GitHub (`https://github.com/JeffHSU8310/SmartStock.git`) 的 `main` 分支。

- **當前專案狀態**:
  - **本機工作目錄**: `E:\SmartStock`
  - **軟體版本**: v1.0.20 (恪遵 Rule 13 `+0.0.1` 遞增)
  - **GitHub 儲存庫**: `https://github.com/JeffHSU8310/SmartStock.git`
  - **Git 分支**: main

---

### 📌 [記錄時間: 2026-08-01] - 10年數據預設6個月視角、精準十字線吸附與 MACD 三層圖表重構 & 發布 v1.0.19 (v1.0.19)

- **使用者需求 (User Prompt)**:
  - 需求重構 MACD、十字線精準吸附、10年數據與預設6個月視角。
