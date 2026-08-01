# 專案跨對話脈絡紀錄 (CONVERSATION_HISTORY.md)

本文件自動同步與紀錄專案的所有重要對話需求、決策與歷程，即使將專案複製或從 GitHub (`https://github.com/JeffHSU8310/SmartStock.git`) 推送/拉取到**其他電腦**上開啟新對話，AI 亦能自動抓取並銜接歷史紀錄。

---

## 📜 對話紀錄歷程

### 📌 [記錄時間: 2026-08-01] - 自選股群組全自動存檔 & 啟動無縫恢復 & 發布 v1.0.27 (v1.0.27)

- **使用者需求 (User Prompt)**:
  - 要求: 「自選股群組的修改系統要自動儲存」

- **系統處理與決策 (System Action & Decision)**:
  - 於 [`src/widgets/watchlist_widget.py`](file:///E:/SmartStock/src/widgets/watchlist_widget.py) 結合 `ConfigManager.save_config()`。
  - 當新增群組、改名、刪除、增刪股票或調換順序時，即時寫入 `config.json`；軟體啟動時自動完全無縫恢復。
  - 沙盒測試 `test_watchlist_autosave.py` 驗證通過，Commit 並 Push 至 GitHub (`https://github.com/JeffHSU8310/SmartStock.git`) 的 `main` 分支。

- **當前專案狀態**:
  - **本機工作目錄**: `E:\SmartStock`
  - **軟體版本**: v1.0.27 (恪遵 Rule 13 `+0.0.1` 遞增)
  - **GitHub 儲存庫**: `https://github.com/JeffHSU8310/SmartStock.git`
  - **Git 分支**: main

---

### 📌 [記錄時間: 2026-08-01] - 貫徹淺色背景純黑字鐵律 & TX00 K棒42650點100%對齊 (v1.0.26)

- **使用者需求 (User Prompt)**:
  - 要求貫徹淺色背景純黑字體鐵律並對齊 TX00 現價。
