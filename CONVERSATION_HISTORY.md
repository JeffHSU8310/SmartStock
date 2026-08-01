# 專案跨對話脈絡紀錄 (CONVERSATION_HISTORY.md)

本文件自動同步與紀錄專案的所有重要對話需求、決策與歷程，即使將專案複製或從 GitHub (`https://github.com/JeffHSU8310/SmartStock.git`) 推送/拉取到**其他電腦**上開啟新對話，AI 亦能自動抓取並銜接歷史紀錄。

---

## 📜 對話紀錄歷程

### 📌 [記錄時間: 2026-08-01] - K 棒間距再拉開一倍 & 發布 v1.0.21 (v1.0.21)

- **使用者需求 (User Prompt)**:
  - 要求：「K棒還是黏在一起。在拉開一倍」。

- **系統處理與決策 (System Action & Decision)**:
  - 於 [`src/widgets/candlestick_chart.py`](file:///E:/SmartStock/src/widgets/candlestick_chart.py) 將預設視野顯示數量由 120 根縮縮減為 60 根，每根 K 棒之間的間距直接拉開 1 倍 (放大 100%)。
  - 將 K 棒半寬 `w` 調大至 `0.38`，呈現飽滿大方之視角。
  - 沙盒測試通過，Commit 並 Push 至 GitHub (`https://github.com/JeffHSU8310/SmartStock.git`) 的 `main` 分支。

- **當前專案狀態**:
  - **本機工作目錄**: `E:\SmartStock`
  - **軟體版本**: v1.0.21 (恪遵 Rule 13 `+0.0.1` 遞增)
  - **GitHub 儲存庫**: `https://github.com/JeffHSU8310/SmartStock.git`
  - **Git 分支**: main

---

### 📌 [記錄時間: 2026-08-01] - 修復 NameError & 發布 v1.0.20 (v1.0.20)

- **使用者需求 (User Prompt)**:
  - 修復 NameError: name 'pd' is not defined。
