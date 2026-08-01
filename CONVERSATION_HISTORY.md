# 專案跨對話脈絡紀錄 (CONVERSATION_HISTORY.md)

本文件自動同步與紀錄專案的所有重要對話需求、決策與歷程，即使將專案複製或從 GitHub (`https://github.com/JeffHSU8310/SmartStock.git`) 推送/拉取到**其他電腦**上開啟新對話，AI 亦能自動抓取並銜接歷史紀錄。

---

## 📜 對話紀錄歷程

### 📌 [記錄時間: 2026-08-01] - 補全 run_cpp_screener 方法修復 AttributeError & 發布 v1.0.15 (v1.0.15)

- **使用者需求 (User Prompt)**:
  - 傳送截圖：`AttributeError: 'SmartStockMainWindow' object has no attribute 'run_cpp_screener'`，要求修復。

- **系統處理與決策 (System Action & Decision)**:
  - 於 [`src/gui_host_qt.py`](file:///E:/SmartStock/src/gui_host_qt.py) 補全 `run_cpp_screener` 與 `run_cpp_backtest` 方法。
  - 沙盒測試通過，Commit 並 Push 至 GitHub (`https://github.com/JeffHSU8310/SmartStock.git`) 的 `main` 分支。

- **當前專案狀態**:
  - **本機工作目錄**: `E:\SmartStock`
  - **軟體版本**: v1.0.15 (恪遵 Rule 13 `+0.0.1` 遞增)
  - **GitHub 儲存庫**: `https://github.com/JeffHSU8310/SmartStock.git`
  - **Git 分支**: main

---

### 📌 [記錄時間: 2026-08-01] - 矯正版本號序列為 v1.0.14 (恪遵 Rule 13 末位累加至 .99 才進位規範) (v1.0.14)

- **使用者需求 (User Prompt)**:
  - 要求嚴格遵守版本號末位累加至 `.99` 規範。
