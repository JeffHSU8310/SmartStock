# 專案跨對話脈絡紀錄 (CONVERSATION_HISTORY.md)

本文件自動同步與紀錄專案的所有重要對話需求、決策與歷程，即使將專案複製或從 GitHub (`https://github.com/JeffHSU8310/SmartStock.git`) 推送/拉取到**其他電腦**上開啟新對話，AI 亦能自動抓取並銜接歷史紀錄。

---

## 📜 對話紀錄歷程

### 📌 [記錄時間: 2026-08-01] - 全面導入 TAIFEX 期貨開盤參考價 (Reference Price) 漲跌計算引擎 (v1.0.34)

- **使用者需求 (User Prompt)**:
  - 專業指出: 「我知道你期貨報價哪裡出問題了，你只是單純的計算 開盤/收盤 之間的價差，但是期貨應該是要用它的參考價為起點來計算。所以，你抓到的資料確實是有問題的，沒有抓到期貨開盤的參考價，導致發生收盤結果有很大的出入。你要去找出期貨的參考價數據」。

- **系統處理與決策 (System Action & Decision)**:
  - 於 [`src/sinopac_engine.py`](file:///E:/SmartStock/src/sinopac_engine.py) 徹底廢除 `Close - Open` 算法，全面導入 Shioaji 官方 `snap.reference_price`（開盤參考價 / 結算價）。
  - 以 `最新價 - 參考價 (43727.00)` 精確計算台指期漲跌點數 `-1077.00` 點與漲跌幅 `-2.46%`！
  - 沙盒測試通過，Commit 並 Push 至 GitHub (`https://github.com/JeffHSU8310/SmartStock.git`) 的 `main` 分支。

- **當前專案狀態**:
  - **本機工作目錄**: `E:\SmartStock`
  - **軟體版本**: v1.0.34 (恪遵 Rule 13 `+0.0.1` 遞增)
  - **GitHub 儲存庫**: `https://github.com/JeffHSU8310/SmartStock.git`
  - **Git 分支**: main

---

### 📌 [記錄時間: 2026-08-01] - 獨立防護 Snapshots 串流 (v1.0.33)

- **使用者需求 (User Prompt)**:
  - 獨立防護與對接 TXFR1。
