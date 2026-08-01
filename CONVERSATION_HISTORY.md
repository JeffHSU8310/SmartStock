# 專案跨對話脈絡紀錄 (CONVERSATION_HISTORY.md)

本文件自動同步與紀錄專案的所有重要對話需求、決策與歷程，即使將專案複製或從 GitHub (`https://github.com/JeffHSU8310/SmartStock.git`) 推送/拉取到**其他電腦**上開啟新對話，AI 亦能自動抓取並銜接歷史紀錄。

---

## 📜 對話紀錄歷程

### 📌 [記錄時間: 2026-08-01] - 修復 CLI 執行路徑相容性 & 發布 v1.0.4 (v1.0.4)

- **使用者需求 (User Prompt)**:
  - 執行 `python src/gui_host_qt.py` 時回報 `ModuleNotFoundError: No module named 'src'`。

- **系統處理與決策 (System Action & Decision)**:
  - 於 [`src/gui_host_qt.py`](file:///E:/SmartStock/src/gui_host_qt.py) 頂端動態導入 `root_dir` 至 `sys.path`，並實作雙層 import 回退相容性。
  - 沙盒測試命令 `python src/gui_host_qt.py` 100% 成功通過。
  - 升級版本至 `v1.0.4` 並 Commit / Push 至 GitHub (`https://github.com/JeffHSU8310/SmartStock.git`) `main` 分支。

- **當前專案狀態**:
  - **本機工作目錄**: `E:\SmartStock`
  - **軟體版本**: v1.0.4 (恪遵 Rule 13 `+0.0.1` 遞增)
  - **GitHub 儲存庫**: `https://github.com/JeffHSU8310/SmartStock.git`
  - **Git 分支**: main

---

### 📌 [記錄時間: 2026-08-01] - 看盤大廳五大原生 UI 版面重構發布 v1.0.3 (v1.0.3)

- **使用者需求 (User Prompt)**:
  - 【看盤大廳 (Market Overview)】：深化永豐金 Shioaji 實時 Tick 與全週期 K線圖動態訂閱。
