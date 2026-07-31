# 專案跨對話脈絡紀錄 (CONVERSATION_HISTORY.md)

本文件自動同步與紀錄專案的所有重要對話需求、決策與歷程，即使將專案複製或從 GitHub (`https://github.com/JeffHSU8310/Rot.git`) 推送/拉取到**其他電腦**上開啟新對話，AI 亦能自動抓取並銜接歷史紀錄。

---

## 📜 對話紀錄歷程

### 📌 [記錄時間: 2026-07-31] - 整合永豐金證券 Shioaji API 雙引擎 (Python SDK & C++ Bridge) (v6.0.0)

- **使用者需求 (User Prompt)**:
  - 提供永豐金 Shioaji 官方文件網址 (`https://sinotrade.github.io/zh/`)，要求 **Python 與 C++ 兩種 API 介面都要整合與支援**。

- **系統處理與決策 (System Action & Decision)**:
  - 擷取 Shioaji 官方 API 文件規格，成功安裝 `shioaji` Python SDK (v1.7.1)。
  - **完成 C++/Python 雙引擎全套整合**：
    1. 撰寫 [`src/sinopac_engine.py`](file:///e:/Rot/src/sinopac_engine.py)：提供 Shioaji 登入、股票/期貨合約抓取與即時 Tick 報價訂閱。
    2. 撰寫 [`src/data/sinopac_cxx_bridge.hpp`](file:///e:/Rot/src/data/sinopac_cxx_bridge.hpp)：提供 C++ 核心極致低延遲行情接收與算力適配器。
  - 編譯驗證 C++ 核心與打包 [`dist/TaiwanSmartQuant_GUI.exe`](file:///e:/Rot/dist/TaiwanSmartQuant_GUI.exe)。
  - 打包發布獨立綠色包 [`TaiwanSmartQuant_v6.0_SinoPac_Standalone.zip`](file:///e:/Rot/TaiwanSmartQuant_v6.0_SinoPac_Standalone.zip)。
  - 更新 [`CHANGELOG.md`](file:///e:/Rot/CHANGELOG.md) 至 `v6.0.0` 並全數 Commit & Push 至 GitHub `main` 分支。

- **當前專案狀態**:
  - **軟體版本**: v6.0.0 (永豐金 Shioaji API 雙引擎原生 GUI 桌面軟體)
  - **券商API**: 永豐金證券 Shioaji API (Python SDK & C++ Core Bridge 雙支援)
  - **獨立GUI執行檔**: `E:\Rot\dist\TaiwanSmartQuant_GUI.exe`
  - **GitHub 狀態**: 已與 `https://github.com/JeffHSU8310/Rot.git` 遠端 `main` 完全同步。
  - **Git 分支**: main (tracking origin/main)

---

### 📌 [記錄時間: 2026-07-31] - 全套重構五大全彩版面並發布 v5.0.0 純原生 GUI 桌面軟體 (v5.0.0)

- **使用者需求 (User Prompt)**:
  - 要求套用規則 12，重新做出五大全彩豐富功能的軟體版面。
