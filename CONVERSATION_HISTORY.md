# 專案跨對話脈絡紀錄 (CONVERSATION_HISTORY.md)

本文件自動同步與紀錄專案的所有重要對話需求、決策與歷程，即使將專案複製或從 GitHub (`https://github.com/JeffHSU8310/SmartStock.git`) 推送/拉取到**其他電腦**上開啟新對話，AI 亦能自動抓取並銜接歷史紀錄。

---

## 📜 對話紀錄歷程

### 📌 [記錄時間: 2026-08-01] - 看盤大廳五大原生 UI 版面重構發布 v1.0.3 (v1.0.3)

- **使用者需求 (User Prompt)**:
  - 【看盤大廳 (Market Overview)】：深化永豐金 Shioaji 實時 Tick 與全週期 K線圖動態訂閱。
  - 版面需求：
    1. 自選股清單（支援新增、刪除、上移、下移，放在主圖區左方）。
    2. 主圖區 (K線圖, 占比最大) & 副圖區 (技術指標, 放在主圖下方)。
    3. 五檔即時報價欄（放在主圖區左方）。
    4. 下單工具欄（放在主圖區左方）。
    5. 訊息欄（放在副圖下方）。

- **系統處理與決策 (System Action & Decision)**:
  - 於 [`src/widgets/watchlist_widget.py`](file:///E:/SmartStock/src/widgets/watchlist_widget.py) 實作自選股清單元件（含新增、刪除、上移 `⬆️`、下移 `⬇️` 按鈕列）。
  - 於 [`src/widgets/five_bids_widget.py`](file:///E:/SmartStock/src/widgets/five_bids_widget.py) 實作五檔報價元件。
  - 於 [`src/widgets/order_toolbar.py`](file:///E:/SmartStock/src/widgets/order_toolbar.py) 實作快捷下單工具欄。
  - 於 [`src/widgets/message_console.py`](file:///E:/SmartStock/src/widgets/message_console.py) 實作日誌訊息欄。
  - 於 [`src/gui_host_qt.py`](file:///E:/SmartStock/src/gui_host_qt.py) 透過 `QSplitter` 佈局重構【看盤大廳】為五大原生版面。
  - 沙盒測試零 Exception，自動 Commit 並 Push 至 GitHub (`https://github.com/JeffHSU8310/SmartStock.git`) `main` 分支。

- **當前專案狀態**:
  - **本機工作目錄**: `E:\SmartStock`
  - **軟體版本**: v1.0.3 (恪遵 Rule 13 `+0.0.1` 遞增)
  - **GitHub 儲存庫**: `https://github.com/JeffHSU8310/SmartStock.git`
  - **Git 分支**: main

---

### 📌 [記錄時間: 2026-08-01] - 全盤語言與套件診斷確認 & 發布 v1.0.2 (v1.0.2)

- **使用者需求 (User Prompt)**:
  - 詢問本機是否有安裝相關 Python & C++ & C# & C 套件。
  - 用戶確認同意並指示開始記錄。

- **系統處理與決策 (System Action & Decision)**:
  - 完成全盤環境診斷：Python 3.13.9, GCC 15.2.0, CMake 4.4.1, .NET SDK 10.0.400 均完整齊備。
  - 於 [`E:\SmartStock\CHANGELOG.md`](file:///E:/SmartStock/CHANGELOG.md) 紀錄 `v1.0.2` 變更。
