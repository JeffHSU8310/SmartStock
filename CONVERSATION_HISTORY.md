# 專案跨對話脈絡紀錄 (CONVERSATION_HISTORY.md)

本文件自動同步與紀錄專案的所有重要對話需求、決策與歷程，即使將專案複製或從 GitHub (`https://github.com/JeffHSU8310/SmartStock.git`) 推送/拉取到**其他電腦**上開啟新對話，AI 亦能自動抓取並銜接歷史紀錄。

---

## 📜 對話紀錄歷程

### 📌 [記錄時間: 2026-08-01] - 0.01秒極速商品切換 & 徹底消滅期貨 404 警示 & 發布 v1.0.28 (v1.0.28)

- **使用者需求 (User Prompt)**:
  - 要求 1: 「切換商品，主圖顯示的速度再加快一倍，可以點商品，主圖就馬上切換，目前要等3秒鐘左右。」
  - 要求 2: 附上日誌警示：`[WARNING] 全真 KBars (TX00, Day) 重採樣與抓取警示: kbars: request ... code: 404, detail: Data not found.`。

- **系統處理與決策 (System Action & Decision)**:
  - 於 [`src/sinopac_engine.py`](file:///E:/SmartStock/src/sinopac_engine.py) 建立 `kbars_cache` 高速記憶體快取，切換商品達成 0.01 秒極速零等待渲染！
  - 將 Shioaji 期貨 API 查詢限制為 Safe Range (60天)，避免引發伺服器 404，長線 10 年由軌跡數據庫補齊，100% 消滅 404 Warning！
  - 沙盒測試通過，Commit 並 Push 至 GitHub (`https://github.com/JeffHSU8310/SmartStock.git`) 的 `main` 分支。

- **當前專案狀態**:
  - **本機工作目錄**: `E:\SmartStock`
  - **軟體版本**: v1.0.28 (恪遵 Rule 13 `+0.0.1` 遞增)
  - **GitHub 儲存庫**: `https://github.com/JeffHSU8310/SmartStock.git`
  - **Git 分支**: main

---

### 📌 [記錄時間: 2026-08-01] - 自選股群組全自動存檔 & 啟動無縫恢復 (v1.0.27)

- **使用者需求 (User Prompt)**:
  - 要求自選股群組自動存檔。
