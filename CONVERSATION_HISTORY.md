# 專案跨對話脈絡紀錄 (CONVERSATION_HISTORY.md)

本文件自動同步與紀錄專案的所有重要對話需求、決策與歷程，即使將專案複製或從 GitHub (`https://github.com/JeffHSU8310/Rot.git`) 推送/拉取到**其他電腦**上開啟新對話，AI 亦能自動抓取並銜接歷史紀錄。

---

## 📜 對話紀錄歷程

### 📌 [記錄時間: 2026-07-31] - 追加規則 13：版本號每次嚴格遞增 +0.0.1 (v6.0.1)

- **使用者需求 (User Prompt)**:
  - 「你的版本變更數字跳太快，每一次跳0.0.1就好了----寫進規則」

- **系統處理與決策 (System Action & Decision)**:
  - 於 [`PROJECT_RULES.md`](file:///e:/Rot/PROJECT_RULES.md) 新增 **規則 13**：
    - **版本號遞增規範**：每次版本號變更必須嚴格以 `+0.0.1` 遞增（如 v6.0.0 ➔ v6.0.1 ➔ v6.0.2），不可大幅跳號。
  - 更新 [`CHANGELOG.md`](file:///e:/Rot/CHANGELOG.md) 至 `v6.0.1`（恪遵 `+0.0.1` 規則）。
  - 執行 Git Commit 並全數自動 Push 同步至 GitHub `main` 分支。

- **當前專案狀態**:
  - **軟體版本**: v6.0.1 (版本號遞增規範載入)
  - **遞增規則**: 每次修改固定 `+0.0.1`
  - **獨立GUI執行檔**: `E:\Rot\dist\TaiwanSmartQuant_GUI.exe`
  - **GitHub 狀態**: 已與 `https://github.com/JeffHSU8310/Rot.git` 遠端 `main` 完全同步。
  - **Git 分支**: main (tracking origin/main)

---

### 📌 [記錄時間: 2026-07-31] - 整合永豐金證券 Shioaji API 雙引擎 (Python SDK & C++ Bridge) (v6.0.0)

- **使用者需求 (User Prompt)**:
  - 提供永豐金 Shioaji 官方文件網址，要求 Python 與 C++ 兩種 API 介面都要整合。
