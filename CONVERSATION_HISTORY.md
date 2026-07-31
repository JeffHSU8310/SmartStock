# 專案跨對話脈絡紀錄 (CONVERSATION_HISTORY.md)

本文件自動同步與紀錄專案的所有重要對話需求、決策與歷程，即使將專案複製或從 GitHub (`https://github.com/JeffHSU8310/Rot.git`) 推送/拉取到**其他電腦**上開啟新對話，AI 亦能自動抓取並銜接歷史紀錄。

---

## 📜 對話紀錄歷程

### 📌 [記錄時間: 2026-07-31] - 追加規則 14：永豐金 Shioaji 官方全庫文檔研讀與實作規範 (v6.0.3)

- **使用者需求 (User Prompt)**:
  - 「https://sinotrade.github.io/zh/ 這個網站內所有的資料，你必須要研究學習，對未來寫的功能程式都有幫助。也列入規則中」

- **系統處理與決策 (System Action & Decision)**:
  - 研讀並吸收永豐金證券 Shioaji API 官方文檔 (`https://sinotrade.github.io/zh/`)，整理其六大核心領域（CA憑證激活、股票/期貨字典、Tick/BidAsk/KBar 即時報價、歷史數據、財務/籌碼面、ROD/IOC/FOK 下單委託與成交回報）。
  - 於 [`PROJECT_RULES.md`](file:///e:/Rot/PROJECT_RULES.md) 新增 **規則 14**：
    - **Shioaji 全庫學習與實作規範**：必須深入研讀 Shioaji 官方文件全內容，並將其技術架構全面融入專案未來的開發中。
  - 更新 [`CHANGELOG.md`](file:///e:/Rot/CHANGELOG.md) 至 `v6.0.3`（恪遵 `+0.0.1` 遞增規則）。
  - 執行 Git Commit 並全數自動 Push 同步至 GitHub `main` 分支。

- **當前專案狀態**:
  - **軟體版本**: v6.0.3 (Shioaji 官方全庫學習規範載入)
  - **學習網站**: `https://sinotrade.github.io/zh/`
  - **獨立GUI執行檔**: `E:\Rot\dist\TaiwanSmartQuant_GUI.exe`
  - **GitHub 狀態**: 已與 `https://github.com/JeffHSU8310/Rot.git` 遠端 `main` 完全同步。
  - **Git 分支**: main (tracking origin/main)

---

### 📌 [記錄時間: 2026-07-31] - 細化規則 13：累積至 0.0.99 再進位至 0.1.0 (v6.0.2)

- **使用者需求 (User Prompt)**:
  - 要求累積到 0.0.99 再進位到 0.1.0 並同步更新規則。
