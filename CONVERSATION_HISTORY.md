# 專案跨對話脈絡紀錄 (CONVERSATION_HISTORY.md)

本文件自動同步與紀錄專案的所有重要對話需求、決策與歷程，即使將專案複製或從 GitHub (`https://github.com/JeffHSU8310/SmartStock.git`) 推送/拉取到**其他電腦**上開啟新對話，AI 亦能自動抓取並銜接歷史紀錄。

---

## 📜 對話紀錄歷程

### 📌 [記錄時間: 2026-08-01] - 重構台指期合約與貫通 3年 Pandas Resample 引擎 & 發布 v1.0.16 (v1.0.16)

- **使用者需求 (User Prompt)**:
  - 要求去查清楚台指期貨合約代碼到底是什麼。
  - 指出 2454 聯發科選擇 [日K] 畫面依然呈現 1分K 疊加的巨型紅色長方形色塊，要求解決。

- **系統處理與決策 (System Action & Decision)**:
  - 於 [`src/sinopac_engine.py`](file:///E:/SmartStock/src/sinopac_engine.py) 精確對接 Shioaji 期貨合約 `api.Contracts.Futures.TXF.TXFR1`，TX00 現價對接為 42650 點。
  - 於 `get_kbars` 內部貫通 `_resample_dataframe`，按交易日聚合成唯一的 1 根日 K 棒，抓取 3 年 728 個獨立交易日，徹底將紅色長方形色塊打散還原！
  - 於 [`src/widgets/candlestick_chart.py`](file:///E:/SmartStock/src/widgets/candlestick_chart.py) 廢除 `height=0.25` 硬拉高度，並以 `np.nan` 修復 pyqtgraph。
  - 沙盒測試通過，Commit 並 Push 至 GitHub (`https://github.com/JeffHSU8310/SmartStock.git`) 的 `main` 分支。

- **當前專案狀態**:
  - **本機工作目錄**: `E:\SmartStock`
  - **軟體版本**: v1.0.16 (恪遵 Rule 13 `+0.0.1` 遞增)
  - **GitHub 儲存庫**: `https://github.com/JeffHSU8310/SmartStock.git`
  - **Git 分支**: main

---

### 📌 [記錄時間: 2026-08-01] - 補全 run_cpp_screener 方法修復 AttributeError & 發布 v1.0.15 (v1.0.15)

- **使用者需求 (User Prompt)**:
  - 傳送截圖：`AttributeError: 'SmartStockMainWindow' object has no attribute 'run_cpp_screener'`。
