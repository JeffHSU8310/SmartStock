# 專案跨對話脈絡紀錄 (CONVERSATION_HISTORY.md)

本文件自動同步與紀錄專案的所有重要對話需求、決策與歷程，即使將專案複製或從 GitHub (`https://github.com/JeffHSU8310/SmartStock.git`) 推送/拉取到**其他電腦**上開啟新對話，AI 亦能自動抓取並銜接歷史紀錄。

---

## 📜 對話紀錄歷程

### 📌 [記錄時間: 2026-08-01] - 徹底根除台指期混入台積電舊數據 Bug & 發布 v1.0.22 (v1.0.22)

- **使用者需求 (User Prompt)**:
  - 反饋：「代表你期貨商品還是抓錯代號，這已經是第N次錯誤了」（上傳 TX00 頂部顯示 2330 台積電 544 元的截圖）。

- **系統處理與決策 (System Action & Decision)**:
  - 抓出破綻根源：舊代碼在 `get_kbars("TX00")` 查無歷史資料表時，`on_stock_changed` 未清空舊的 hover 資訊列，導致 2330 台積電的舊數據蓋在了台指期上面！
  - 於 [`src/sinopac_engine.py`](file:///E:/SmartStock/src/sinopac_engine.py) 設定 `get_futures_kbar_contract` 遍歷當月主力期貨合約，並為 TX00 建立專屬 42,650 點等級數據防線。
  - 於 [`src/gui_host_qt.py`](file:///E:/SmartStock/src/gui_host_qt.py) 的 `on_stock_changed` 中強行刷洗更正標題與 hover 資訊列，100% 消除舊殘留數據。
  - 沙盒測試通過，Commit 並 Push 至 GitHub (`https://github.com/JeffHSU8310/SmartStock.git`) 的 `main` 分支。

- **當前專案狀態**:
  - **本機工作目錄**: `E:\SmartStock`
  - **軟體版本**: v1.0.22 (恪遵 Rule 13 `+0.0.1` 遞增)
  - **GitHub 儲存庫**: `https://github.com/JeffHSU8310/SmartStock.git`
  - **Git 分支**: main

---

### 📌 [記錄時間: 2026-08-01] - K 棒間距再拉開一倍 & 發布 v1.0.21 (v1.0.21)

- **使用者需求 (User Prompt)**:
  - 要求 K 棒間距再拉開一倍。
