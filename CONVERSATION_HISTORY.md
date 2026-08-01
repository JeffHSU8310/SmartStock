# 專案跨對話脈絡紀錄 (CONVERSATION_HISTORY.md)

本文件自動同步與紀錄專案的所有重要對話需求、決策與歷程，即使將專案複製或從 GitHub (`https://github.com/JeffHSU8310/SmartStock.git`) 推送/拉取到**其他電腦**上開啟新對話，AI 亦能自動抓取並銜接歷史紀錄。

---

## 📜 對話紀錄歷程

### 📌 [記錄時間: 2026-08-01] - 實作官方中文名稱動態解析器 & 發布 v1.0.17 (v1.0.17)

- **使用者需求 (User Prompt)**:
  - 反饋：「我輸入股票代號，名稱也沒有顯示正確。」（上傳 00878 顯示「股票 00878」的截圖）。

- **系統處理與決策 (System Action & Decision)**:
  - 於 [`src/sinopac_engine.py`](file:///E:/SmartStock/src/sinopac_engine.py) 實作 `get_symbol_name(code)` 方法，動態解析官方標準中文名稱（00878 ➔ 國泰永續高股息）。
  - 於 [`src/widgets/watchlist_widget.py`](file:///E:/SmartStock/src/widgets/watchlist_widget.py) 與 [`src/gui_host_qt.py`](file:///E:/SmartStock/src/gui_host_qt.py) 貫通中文名稱動態更新。
  - 沙盒測試通過，Commit 並 Push 至 GitHub (`https://github.com/JeffHSU8310/SmartStock.git`) 的 `main` 分支。

- **當前專案狀態**:
  - **本機工作目錄**: `E:\SmartStock`
  - **軟體版本**: v1.0.17 (恪遵 Rule 13 `+0.0.1` 遞增)
  - **GitHub 儲存庫**: `https://github.com/JeffHSU8310/SmartStock.git`
  - **Git 分支**: main

---

### 📌 [記錄時間: 2026-08-01] - 重構台指期合約與貫通 3年 Pandas Resample 引擎 & 發布 v1.0.16 (v1.0.16)

- **使用者需求 (User Prompt)**:
  - 要求去查清楚台指期貨合約代碼到底是什麼。
