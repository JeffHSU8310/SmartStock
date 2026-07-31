# 專案跨對話脈絡紀錄 (CONVERSATION_HISTORY.md)

本文件自動同步與紀錄專案的所有重要對話需求、決策與歷程，即使將專案複製或從 GitHub (`https://github.com/JeffHSU8310/Rot.git`) 推送/拉取到**其他電腦**上開啟新對話，AI 亦能自動抓取並銜接歷史紀錄。

---

## 📜 對話紀錄歷程

### 📌 [記錄時間: 2026-07-31] - 規則 12 細化：C++ (K線/報價/回測/選股) 與 Python (版面) 明確分工 (v4.1.0)

- **使用者需求 (User Prompt)**:
  - 「C++核心主要是K線圖、報價、回測、選股。Python主要是版面----這列入規則」

- **系統處理與決策 (System Action & Decision)**:
  - 於 [`PROJECT_RULES.md`](file:///e:/Rot/PROJECT_RULES.md) 更新與強調 **規則 12**：
    - **C++ 核心職責**：K線圖計算、報價數據引擎、策略回測、智慧選股評分。
    - **Python 輔助職責**：原生桌面 GUI 版面排版、炫彩視覺渲染、視窗打包。
  - 更新 [`CHANGELOG.md`](file:///e:/Rot/CHANGELOG.md) 至 `v4.1.0`。
  - 執行 Git Commit 並全數自動 Push 同步至 GitHub `main` 分支。

- **當前專案狀態**:
  - **軟體版本**: v4.1.0 (明確分工規則載入)
  - **分工架構**: C++ (K線/報價/回測/選股核心) + Python (版面/GUI)
  - **獨立GUI執行檔**: `E:\Rot\dist\TaiwanSmartQuant_GUI.exe`
  - **GitHub 狀態**: 已與 `https://github.com/JeffHSU8310/Rot.git` 遠端 `main` 完全同步。
  - **Git 分支**: main (tracking origin/main)

---

### 📌 [記錄時間: 2026-07-31] - 追加規則 12，升級 C++/Python 雙引擎純原生 GUI 桌面軟體 (v4.0.0)

- **使用者需求 (User Prompt)**:
  - 要求做出真正獨立的視窗軟體，允許使用 Python 作為輔助，並寫入規則。
