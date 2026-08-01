# 專案跨對話脈絡紀錄 (CONVERSATION_HISTORY.md)

本文件自動同步與紀錄專案的所有重要對話需求、決策與歷程，即使將專案複製或從 GitHub (`https://github.com/JeffHSU8310/SmartStock.git`) 推送/拉取到**其他電腦**上開啟新對話，AI 亦能自動抓取並銜接歷史紀錄。

---

## 📜 對話紀錄歷程

### 📌 [記錄時間: 2026-08-01] - Shioaji 期貨 TX00/TXF 合約對接與 KBars 安全型態校驗發布 v1.0.9 (v1.0.9)

- **使用者需求 (User Prompt)**:
  - 貼出日誌警告：`[WARNING] 抓取全真 KBars (TX00, 日) 失敗，啟用備用引擎: expected BaseContract, Contract, or contract Info`，要求修復。

- **系統處理與決策 (System Action & Decision)**:
  - 於 [`src/sinopac_engine.py`](file:///E:/SmartStock/src/sinopac_engine.py) 對接永豐金 Shioaji 官方期貨合約 `api.Contracts.Futures.TXFR1` / `TXF` 與 `api.Contracts.Indices.TSE.IX0001` 指數合約。
  - 在傳入 `api.kbars` 之前進行 `contract` 屬性與非空校驗，徹底消除 `expected BaseContract, Contract, or contract Info` 警告。
  - 沙盒測試通過，Commit 並 Push 至 GitHub (`https://github.com/JeffHSU8310/SmartStock.git`) `main` 分支。

- **當前專案狀態**:
  - **本機工作目錄**: `E:\SmartStock`
  - **軟體版本**: v1.0.9 (恪遵 Rule 13 `+0.0.1` 遞增)
  - **GitHub 儲存庫**: `https://github.com/JeffHSU8310/SmartStock.git`
  - **Git 分支**: main

---

### 📌 [記錄時間: 2026-08-01] - 切換商品 K線資訊重置修復、8大週期 Resample、MA趨勢箭頭與一字K厚度發布 v1.0.8 (v1.0.8)

- **使用者需求 (User Prompt)**:
  - 依最新截圖 6 大紅框批註與切換商品反饋：修復切換商品 K 線資訊重置、8大週期按鈕選中高亮、頂部 MA5/MA20 趨勢箭頭、自選股價格刷新與一字/十字 K 棒視覺厚度。
