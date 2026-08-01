# 專案跨對話脈絡紀錄 (CONVERSATION_HISTORY.md)

本文件自動同步與紀錄專案的所有重要對話需求、決策與歷程，即使將專案複製或從 GitHub (`https://github.com/JeffHSU8310/SmartStock.git`) 推送/拉取到**其他電腦**上開啟新對話，AI 亦能自動抓取並銜接歷史紀錄。

---

## 📜 對話紀錄歷程

### 📌 [記錄時間: 2026-08-01] - 全真報價對接、K線切換修復、登入 Modal 與帳戶切換發布 v1.0.5 (v1.0.5)

- **使用者需求 (User Prompt)**:
  - 圖片 1：提示彈窗字體顏色改為黑色/高對比白字，確保清晰可讀。
  - 圖片 2：右上角登入/登出動態切換按鈕，點擊彈出憑證登入 Modal，新增記憶 API KEY 勾選功能。刪除「憑證與系統設定」分頁。
  - 圖片 3：下單工具欄新增實盤/模擬帳戶選擇功能。刪除「Shioaji 實盤下單」分頁，介面精簡為 3 大核心頁籤。
  - 追加需求：修復登入永豐金 API 後的最新實時報價對接，以及點擊自選股切換商品時的主圖 K棒 與價格即時動態連動。

- **系統處理與決策 (System Action & Decision)**:
  - 於 `.gitignore` 加入 `config.json`，並建立 [`src/utils/config_manager.py`](file:///E:/SmartStock/src/utils/config_manager.py) 加密保存 API Key 與憑證設定 (恪遵 Rule 10)。
  - 於 [`src/widgets/auth_dialog.py`](file:///E:/SmartStock/src/widgets/auth_dialog.py) 實作 CA 憑證登入 Modal (`QDialog`)，含 **【☑️ 記憶 API Key 與憑證設定】** 勾選框。
  - 於 [`src/widgets/order_toolbar.py`](file:///E:/SmartStock/src/widgets/order_toolbar.py) 新增「實盤帳戶 vs 模擬/虛擬交易帳戶」選擇。
  - 於 [`src/sinopac_engine.py`](file:///E:/SmartStock/src/sinopac_engine.py) 貫通 Shioaji `api.snapshots()` 快照與 `api.kbars()` 真實 K 線，修復商品切換。
  - 於 [`src/gui_host_qt.py`](file:///E:/SmartStock/src/gui_host_qt.py) 重構 QSS 彈窗高對比文字、右上角登入/登出狀態綁定 Modal，並加入 `QTimer` 3 秒定時器。
  - 沙盒測試通過，Commit 並 Push 至 GitHub (`https://github.com/JeffHSU8310/SmartStock.git`) `main` 分支。

- **當前專案狀態**:
  - **本機工作目錄**: `E:\SmartStock`
  - **軟體版本**: v1.0.5 (恪遵 Rule 13 `+0.0.1` 遞增)
  - **GitHub 儲存庫**: `https://github.com/JeffHSU8310/SmartStock.git`
  - **Git 分支**: main

---

### 📌 [記錄時間: 2026-08-01] - 修復 CLI 執行路徑相容性 & 發布 v1.0.4 (v1.0.4)

- **使用者需求 (User Prompt)**:
  - 執行 `python src/gui_host_qt.py` 時回報 `ModuleNotFoundError: No module named 'src'`。
