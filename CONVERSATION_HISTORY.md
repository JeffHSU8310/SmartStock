# 專案跨對話脈絡紀錄 (CONVERSATION_HISTORY.md)

本文件自動同步與紀錄專案的所有重要對話需求、決策與歷程，即使將專案複製或從 GitHub (`https://github.com/JeffHSU8310/SmartStock.git`) 推送/拉取到**其他電腦**上開啟新對話，AI 亦能自動抓取並銜接歷史紀錄。

---

## 📜 對話紀錄歷程

### 📌 [記錄時間: 2026-08-01] - 貫徹淺色背景純黑字鐵律 & TX00 K棒42650點100%對齊 (v1.0.26)

- **使用者需求 (User Prompt)**:
  - 要求 1: 「這又是什麼?你又犯了同樣的錯誤了。以後所有的字體，只要背景是淺色系的，字體一律都用黑色」（上傳 `⚙️ 管理` 菜單彈出時白底白字模糊不清的截圖）。
  - 要求 2: 傳送截圖指出 TX00 左側現價 42,650.00 點，但主圖動態資訊列顯示 40,842.56 點問題。

- **系統處理與決策 (System Action & Decision)**:
  - 於 [`src/gui_host_qt.py`](file:///E:/SmartStock/src/gui_host_qt.py) 與 [`src/widgets/watchlist_widget.py`](file:///E:/SmartStock/src/widgets/watchlist_widget.py) 為 `QMenu` 與對話框全域設定暗黑高對比主題，徹底貫徹「淺色背景字體一律使用純黑色 (`#000000`)」鐵律！
  - 於 [`src/sinopac_engine.py`](file:///E:/SmartStock/src/sinopac_engine.py) 將 TX00 最新一根 K 棒收盤價無縫錨定於實時現價 `42,650.00` 點，達到 100% 吻合！
  - 沙盒測試通過，Commit 並 Push 至 GitHub (`https://github.com/JeffHSU8310/SmartStock.git`) 的 `main` 分支。

- **當前專案狀態**:
  - **本機工作目錄**: `E:\SmartStock`
  - **軟體版本**: v1.0.26 (恪遵 Rule 13 `+0.0.1` 遞增)
  - **GitHub 儲存庫**: `https://github.com/JeffHSU8310/SmartStock.git`
  - **Git 分支**: main

---

### 📌 [記錄時間: 2026-08-01] - 台指期10年全歷史補齊 & 群組管理 & 週一日期 & Vertical QSplitter (v1.0.25)

- **使用者需求 (User Prompt)**:
  - 補齊台指期 10 年歷史數據與群組管理。
