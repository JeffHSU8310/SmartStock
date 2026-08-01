# 專案跨對話脈絡紀錄 (CONVERSATION_HISTORY.md)

本文件自動同步與紀錄專案的所有重要對話需求、決策與歷程，即使將專案複製或從 GitHub (`https://github.com/JeffHSU8310/SmartStock.git`) 推送/拉取到**其他電腦**上開啟新對話，AI 亦能自動抓取並銜接歷史紀錄。

---

## 📜 對話紀錄歷程

### 📌 [記錄時間: 2026-08-01] - 徹底廢除寫死假數據、全真 Snapshots 快照連動與 Y軸 AutoRange 發布 v1.1.0 (v1.1.0)

- **使用者需求 (User Prompt)**:
  - 要求：「把系統中，之前寫死的全部刪除」。

- **系統處理與決策 (System Action & Decision)**:
  - 於 [`src/sinopac_engine.py`](file:///E:/SmartStock/src/sinopac_engine.py) 100% 刪除 `mock_info` 寫死假價格字典，全面直連 Shioaji 全真快照 `snapshots` 與 `kbars` 官方數據。
  - 於 [`src/widgets/watchlist_widget.py`](file:///E:/SmartStock/src/widgets/watchlist_widget.py) 刪除初始寫死價格，實作 `update_quote` 即時更新全真最新現價。
  - 於 [`src/widgets/candlestick_chart.py`](file:///E:/SmartStock/src/widgets/candlestick_chart.py) 實作 `enableAutoRange(axis='y', enable=True)`，徹底修復從 2425元切換至 49.2元時大叉叉 K 棒落到畫面下方看不見的問題。
  - 沙盒測試通過，Commit 並 Push 至 GitHub (`https://github.com/JeffHSU8310/SmartStock.git`) `main` 分支。

- **當前專案狀態**:
  - **本機工作目錄**: `E:\SmartStock`
  - **軟體版本**: v1.1.0 (恪遵 Rule 13 進位升級)
  - **GitHub 儲存庫**: `https://github.com/JeffHSU8310/SmartStock.git`
  - **Git 分支**: main

---

### 📌 [記錄時間: 2026-08-01] - Shioaji 期貨 TX00/TXF 合約對接與 KBars 安全型態校驗發布 v1.0.9 (v1.0.9)

- **使用者需求 (User Prompt)**:
  - 貼出日誌警告：`[WARNING] 抓取全真 KBars (TX00, 日) 失敗，啟用備用引擎: expected BaseContract, Contract, or contract Info`，要求修復。
