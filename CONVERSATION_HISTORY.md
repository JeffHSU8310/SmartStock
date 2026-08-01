# 專案跨對話脈絡紀錄 (CONVERSATION_HISTORY.md)

本文件自動同步與紀錄專案的所有重要對話需求、決策與歷程，即使將專案複製或從 GitHub (`https://github.com/JeffHSU8310/SmartStock.git`) 推送/拉取到**其他電腦**上開啟新對話，AI 亦能自動抓取並銜接歷史紀錄。

---

## 📜 對話紀錄歷程

### 📌 [記錄時間: 2026-08-01] - 本機專案路徑切換至 E:\SmartStock & 版本升級 v1.0.1 (v1.0.1)

- **使用者需求 (User Prompt)**:
  - 本機位置已經更換至 `E:\SmartStock`。

- **系統處理與決策 (System Action & Decision)**:
  - 將專案工作路徑完整同步更新至 [`E:\SmartStock`](file:///E:/SmartStock)。
  - 於 [`E:\SmartStock\smartstock_core.dll`](file:///E:/SmartStock/smartstock_core.dll) 重建與驗證 C++ 動態庫載入。
  - 於 [`E:\SmartStock\CHANGELOG.md`](file:///E:/SmartStock/CHANGELOG.md) 紀錄 `v1.0.1` 變更。
  - 沙盒測試 C++ 算力與 PySide6 GUI 在新路徑上完全無縫通過驗證。
  - 自動完成 Git Commit 並 Push 同步至 GitHub (`https://github.com/JeffHSU8310/SmartStock.git`) `main` 分支。

- **當前專案狀態**:
  - **本機工作目錄**: `E:\SmartStock`
  - **軟體版本**: v1.0.1 (恪遵 Rule 13 `+0.0.1` 遞增)
  - **GitHub 儲存庫**: `https://github.com/JeffHSU8310/SmartStock.git`
  - **Git 分支**: main

---

### 📌 [記錄時間: 2026-08-01] - SmartStock 全新歸零重啟 & PySide6 純原生桌面視窗架構 (v1.0.0)

- **使用者需求 (User Prompt)**:
  - 開新的專案，重新開始，一切歸零。
  - 強調不要用 Web/HTML 方式，本系統僅限使用 **C++ & Python & C & C#**。
  - 要求無條件遵循 18 項最新重點規則（0~17），每次修改版本號嚴格 `+0.0.1` 遞增，並自動同步 GitHub (`https://github.com/JeffHSU8310/SmartStock.git`)。

- **系統處理與決策 (System Action & Decision)**:
  - 於 [`PROJECT_RULES.md`](file:///E:/SmartStock/PROJECT_RULES.md) 寫入完整的 18 項重點規則。
  - 徹底拋棄 Web/HTML/pywebview，採用 **PySide6 (Qt6 for Python)** + **pyqtgraph** 原生繪圖模組建立 100% 獨立純原生桌面 GUI 應用程式。
  - 於 [`src/core/`](file:///E:/SmartStock/src/core/), [`src/technical/`](file:///E:/SmartStock/src/technical/), [`src/strategy/`](file:///E:/SmartStock/src/strategy/), [`src/backtest/`](file:///E:/SmartStock/src/backtest/) 撰寫 C++ 核心算力引擎。
  - 於 [`src/sinopac_engine.py`](file:///E:/SmartStock/src/sinopac_engine.py) 實作永豐金 Shioaji API 憑證激活、行情下載與委託。
