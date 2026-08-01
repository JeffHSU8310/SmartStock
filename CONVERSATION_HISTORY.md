# 專案跨對話脈絡紀錄 (CONVERSATION_HISTORY.md)

本文件自動同步與紀錄專案的所有重要對話需求、決策與歷程，即使將專案複製或從 GitHub (`https://github.com/JeffHSU8310/SmartStock.git`) 推送/拉取到**其他電腦**上開啟新對話，AI 亦能自動抓取並銜接歷史紀錄。

---

## 📜 對話紀錄歷程

### 📌 [記錄時間: 2026-08-01] - 追加第 19 條 TWSE 股票 vs ETF 升降單位雙軌規範 & 發布 v1.1.1 (v1.1.1)

- **使用者需求 (User Prompt)**:
  - 要求將「台灣證券交易所 (TWSE) 官方一般股票 vs ETF 升降單位雙軌權威規定」寫入規則中。

- **系統處理與決策 (System Action & Decision)**:
  - 於 [`PROJECT_RULES.md`](file:///E:/SmartStock/PROJECT_RULES.md) 完整寫入 Rule 19 TWSE 升降單位規範。
  - 於 [`CHANGELOG.md`](file:///E:/SmartStock/CHANGELOG.md) 紀錄 `v1.1.1` 變更。
  - 執行 Git Commit 與 Push 同步至 GitHub (`https://github.com/JeffHSU8310/SmartStock.git`) 的 `main` 分支。

- **當前專案狀態**:
  - **本機工作目錄**: `E:\SmartStock`
  - **軟體版本**: v1.1.1 (恪遵 Rule 13 `+0.0.1` 遞增)
  - **GitHub 儲存庫**: `https://github.com/JeffHSU8310/SmartStock.git`
  - **Git 分支**: main

---

### 📌 [記錄時間: 2026-08-01] - 徹底廢除寫死假數據、全真 Snapshots 快照連動與 Y軸 AutoRange 發布 v1.1.0 (v1.1.0)

- **使用者需求 (User Prompt)**:
  - 要求：「把系統中，之前寫死的全部刪除」。
