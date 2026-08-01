# 專案跨對話脈絡紀錄 (CONVERSATION_HISTORY.md)

本文件自動同步與紀錄專案的所有重要對話需求、決策與歷程，即使將專案複製或從 GitHub (`https://github.com/JeffHSU8310/SmartStock.git`) 推送/拉取到**其他電腦**上開啟新對話，AI 亦能自動抓取並銜接歷史紀錄。

---

## 📜 對話紀錄歷程

### 📌 [記錄時間: 2026-08-01] - 修復成交量矩形牆與斜線對角殘影 Bug & 發布 v1.0.24 (v1.0.24)

- **使用者需求 (User Prompt)**:
  - 反饋：「成交量的繪製也很亂，錯誤一堆」（上傳成交量 Y 軸 36500~37500 被截斷拉伸成混亂滿屏矩形牆的截圖）。

- **系統處理與決策 (System Action & Decision)**:
  - 抓出死穴：`BarGraphItem` 缺少 `y0=0`，且 `p2` 未鎖定 Y 軸自 0 起算，導致 pyqtgraph 將微小量能放大切頭放大塞滿全屏。
  - 於 [`src/widgets/candlestick_chart.py`](file:///E:/SmartStock/src/widgets/candlestick_chart.py) 傳入 `y0=0` 並動態設定 `setYRange(0, max_visible_vol * 1.1)`，徹底解決混亂成交量牆問題。
  - 徹底 `clear()` 舊畫布，消滅均線對角斜拉殘影。
  - 沙盒測試通過，Commit 並 Push 至 GitHub (`https://github.com/JeffHSU8310/SmartStock.git`) 的 `main` 分支。

- **當前專案狀態**:
  - **本機工作目錄**: `E:\SmartStock`
  - **軟體版本**: v1.0.24 (恪遵 Rule 13 `+0.0.1` 遞增)
  - **GitHub 儲存庫**: `https://github.com/JeffHSU8310/SmartStock.git`
  - **Git 分支**: main

---

### 📌 [記錄時間: 2026-08-01] - 實作 1:1 K棒留白間隔 & 修復時間快選按鈕 & 發布 v1.0.23 (v1.0.23)

- **使用者需求 (User Prompt)**:
  - 要求 1:1 留白間隔並修復時間快選。
