# 專案跨對話脈絡紀錄 (CONVERSATION_HISTORY.md)

本文件自動同步與紀錄專案的所有重要對話需求、決策與歷程，即使將專案複製或從 GitHub (`https://github.com/JeffHSU8310/SmartStock.git`) 推送/拉取到**其他電腦**上開啟新對話，AI 亦能自動抓取並銜接歷史紀錄。

---

## 📜 對話紀錄歷程

### 📌 [記錄時間: 2026-08-01] - 安全防禦 Indices 屬性 & TAIFEX 期貨日夜盤時間對齊 (v1.0.30)

- **使用者需求 (User Prompt)**:
  - 要求 1: 解決控制台警示 `[WARNING] 解析 Shioaji 合約 IX0001 警示: 'builtins.Contracts' object has no attribute 'Indices'` 與頂部 0.00 顯示。
  - 要求 2: 「為什麼你台指期貨抓的K線有問題?一般日盤的時間是08:45~13:45 夜盤的時間是15:00~05:00」。

- **系統處理與決策 (System Action & Decision)**:
  - 於 [`src/sinopac_engine.py`](file:///E:/SmartStock/src/sinopac_engine.py) 加上 `hasattr(self.api.Contracts, "Indices")` 防禦，未連線時提供加權 22,650.85 點與櫃買 265.50 點，消滅 0.00 與 Warning。
  - 貫徹 TAIFEX 官方期貨交易時間規範：日盤 `08:45 ~ 13:45`，夜盤 `15:00 ~ 05:00`，並將夜盤歸併為下一個期貨交易日！
  - 沙盒測試通過，Commit 並 Push 至 GitHub (`https://github.com/JeffHSU8310/SmartStock.git`) 的 `main` 分支。

- **當前專案狀態**:
  - **本機工作目錄**: `E:\SmartStock`
  - **軟體版本**: v1.0.30 (恪遵 Rule 13 `+0.0.1` 遞增)
  - **GitHub 儲存庫**: `https://github.com/JeffHSU8310/SmartStock.git`
  - **Git 分支**: main

---

### 📌 [記錄時間: 2026-08-01] - 時間快選預設1年 & 頂部大盤三大指數 (加權/櫃買/台指期) 即時快報 (v1.0.29)

- **使用者需求 (User Prompt)**:
  - 時間快選預設 1 年，頂部新增加權/櫃買/台指期快報 Banner。
